"""Monte Carlo model of a solo run's gold, level by level. README.md describes the model and its assumptions."""

import bisect
import collections
import json
import math
import random
import statistics
from dataclasses import dataclass, field
from typing import Any, Callable

COPPER = 1
SILVER = 100
GOLD = 10000

# The level each bracket opens at, in the order of regions.ALL_REGIONS.
BRACKETS = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
REGION_INDEX = {f"Levels {max(lo, 1):02d}-{lo + 5:02d}": i for i, lo in enumerate(BRACKETS)}

CLASS_IDS = {"warrior": 1, "paladin": 2, "hunter": 3, "rogue": 4, "priest": 5, "shaman": 7, "mage": 8, "warlock": 9, "druid": 11}

GEAR_FILLERS = {
    "Random Uncommon Weapon": ("weapon", 2),
    "Random Rare Weapon": ("weapon", 3),
    "Random Uncommon Armor": ("armor", 2),
    "Random Rare Armor": ("armor", 3),
    "Random Uncommon Jewelry": ("jewelry", 2),
    "Random Rare Jewelry": ("jewelry", 3),
}

# Riding ranks sold for gold as checks: spell, (name, level, priority). A character saves up for a rank before
# buying anything from the shop that isn't progression, except Artisan Riding: nobody puts 5000g ahead of it.
RIDING = {
    33388: ("Apprentice", 20, 1),
    33391: ("Journeyman", 40, 1),
    34090: ("Expert", 60, 1),
    34091: ("Artisan", 70, 3),
    54197: ("Cold Weather", 77, 1),
}

# The armor type each class wears below level 40 and from it on: see GearPool::AllowedArmorMask in the module.
CLOTH, LEATHER, MAIL, PLATE = 1, 2, 3, 4
ARMOR_BY_CLASS = {
    1: (MAIL, PLATE),
    2: (MAIL, PLATE),
    3: (LEATHER, MAIL),
    4: (LEATHER, LEATHER),
    5: (CLOTH, CLOTH),
    7: (LEATHER, MAIL),
    8: (CLOTH, CLOTH),
    9: (CLOTH, CLOTH),
    11: (LEATHER, LEATHER),
}

PriceTable = list[tuple[int, int]]


def goal_level(seed: dict[str, Any]) -> int:
    """The level a level goal is won at, or 0 for a goal won otherwise: AP_Character::GetGoalLevel in the module."""
    return seed["level_cap"] if seed["max_level"] < seed["level_cap"] else 0


def step_price(table: PriceTable, level: int) -> int:
    price = table[0][1]
    for tier, tier_price in table:
        if level >= tier:
            price = tier_price
    return price


def smooth(table: dict[str, float], radius: int = 2) -> dict[int, float]:
    """Mean over neighbouring levels, so a level with a handful of quests or creatures doesn't swing the curve."""
    values = {int(k): v for k, v in table.items()}
    out: dict[int, float] = {}
    for level in range(1, 81):
        near = [v for k, v in values.items() if abs(k - level) <= radius]
        out[level] = sum(near) / len(near) if near else values[min(values, key=lambda k: abs(k - level))]
    return out


class Economy:
    """Per-level income and cost curves from the world database, calibrated on a recorded playthrough."""

    def __init__(self, db: dict[str, Any]):
        self.xp_needed = {int(k): v for k, v in db["xp_needed"].items()}
        self.coin = smooth(db["mob_coin"])
        self.drop = smooth(db["drop_value"])
        quests = db["quests"]
        self.quest_money = smooth({k: q["money"] for k, q in quests.items()})
        self.quest_items = smooth({k: q["items"] for k, q in quests.items()})
        self.quest_xp = smooth({k: q["xp"] for k, q in quests.items() if q["xp"] > 0})
        self.training = {int(c): {int(lvl): cost for lvl, cost in t.items()} for c, t in db["training"].items()}
        self.riding = {int(k): v[1] for k, v in db["riding"].items()}

        # The recorded levels say how a level's experience splits between kills and quests, and how the
        # database's averages compare with what the character actually looted, earned and vendored.
        rows = db["calibration"]
        xp = sum(r["xp_kill"] + r["xp_quest"] + r["xp_explore"] for r in rows)
        self.kill_share = sum(r["xp_kill"] for r in rows) / xp
        self.quest_share = sum(r["xp_quest"] for r in rows) / xp
        looted = sum(r["money_looted"] for r in rows)
        vendored = sum(r["money_gained"] for r in rows) - looted - db["calibration_quest_money"]
        self.coin_factor = looted / sum(r["kills"] * self.coin[int(r["level"])] for r in rows)
        self.quest_money_factor = db["calibration_quest_money"] / sum(r["quests"] * self.quest_money[int(r["level"])] for r in rows)
        self.sell_share = vendored / sum(r["kills"] * self.drop[int(r["level"])] + r["quests"] * self.quest_items[int(r["level"])] for r in rows)

        self.gear: dict[tuple[str, int], list[tuple[int, int, int, int]]] = collections.defaultdict(list)
        for category, quality, level, allowed, armor, price in db["gear"]:
            self.gear[(category, quality)].append((level, allowed, armor, price))
        for items in self.gear.values():
            items.sort()
        self._gear_cache: dict[tuple[str, int, int, int], list[int]] = {}

    @staticmethod
    def kill_xp(level: int) -> int:
        """Experience for a kill of the character's level, in the content of its level."""
        base = 45 if level < 60 else 235 if level < 70 else 580
        return level * 5 + base

    def baseline_income(self, level: int) -> float:
        """Copper a character earns over one level from kills and quests, at the recorded pace."""
        xp = self.xp_needed[level]
        kills = xp * self.kill_share / self.kill_xp(level)
        quests = xp * self.quest_share / self.quest_xp[level]
        coin = kills * self.coin[level] * self.coin_factor
        money = quests * self.quest_money[level] * self.quest_money_factor
        vendor = (kills * self.drop[level] + quests * self.quest_items[level]) * self.sell_share
        return coin + money + vendor

    def gear_prices(self, category: str, quality: int, level: int, class_id: int, window: int = 3) -> list[int]:
        """Vendor prices of the pieces a gear filler could hand out, widened as GearPool::Roll widens."""
        key = (category, quality, level, class_id)
        if key not in self._gear_cache:
            mask = 1 << (class_id - 1)
            armor = ARMOR_BY_CLASS[class_id][0 if level < 40 else 1]
            items = [
                (lvl, price)
                for lvl, allowed, sub, price in self.gear[(category, quality)]
                if allowed & mask and (category != "armor" or sub in (armor, 0))
            ]
            levels = [lvl for lvl, _ in items]
            low, high = level - window, level + window
            while True:
                lo, hi = bisect.bisect_left(levels, low), bisect.bisect_right(levels, high)
                if hi - lo >= 10 or (low <= 1 and high >= 80):
                    break
                low, high = low - 2, high + 2
            self._gear_cache[key] = [price for _, price in items[lo:hi]] or [0]
        return self._gear_cache[key]


@dataclass
class Settings:
    label: str
    prices: PriceTable
    pouch: Callable[[int, int], int]
    """Copper in a Gold Pouch at a level, given the seed's goal level (see goal_level)."""
    weights: dict[str, int]
    cap_last_tier: bool = False
    """Price the last tier before a level goal like the one before it: there is no bracket after it to save in."""
    scale_by_items: bool = False
    """The table prices 3 items per tier; a tier of more items shares that price out between them."""

    def price(self, tier: int, goal: int, items_per_tier: int) -> int:
        level = min(tier, goal - 6) if self.cap_last_tier and goal else tier
        price = step_price(self.prices, level)
        return max(1, price * 3 // items_per_tier) if self.scale_by_items else price


@dataclass
class Result:
    bought: dict[tuple[str, int], int] = field(default_factory=dict)
    """The level each paid check was bought at, by kind and order."""
    stalls: list[tuple[str, int]] = field(default_factory=list)
    """For each paid check holding progression, the levels between it going on sale and being bought."""
    income: dict[str, float] = field(default_factory=lambda: collections.defaultdict(float))
    max_level: int = 0


class Run:
    """One character's run through one generated seed."""

    def __init__(self, econ: Economy, seed: dict[str, Any], settings: Settings, rng: random.Random, activity: float, gear_sold: float, upkeep: float):
        self.econ = econ
        self.settings = settings
        self.rng = rng
        self.activity = activity * math.exp(rng.gauss(0, 0.15))
        self.gear_sold = gear_sold
        self.upkeep = upkeep
        self.class_id = CLASS_IDS[seed["options"]["character_class"]]
        self.max_level: int = seed["max_level"]
        self.goal = goal_level(seed)
        self.seed = seed
        self.items_per_tier = max(1, sum(1 for loc in seed["locations"] if loc[1].startswith("Stone Shop: Level 05 ")))

    def reroll(self, item: str) -> str:
        """Filler drawn again with the settings' weights, so weights can be tried without generating again."""
        if item not in self.settings.weights:
            return item
        names = list(self.settings.weights)
        return self.rng.choices(names, weights=[self.settings.weights[n] for n in names])[0]

    def item_value(self, item: str, level: int) -> int:
        """Copper an item adds to the character's purse when it arrives."""
        if item == "Gold Pouch":
            return self.settings.pouch(level, self.goal)
        if item in GEAR_FILLERS and self.rng.random() < self.gear_sold:
            category, quality = GEAR_FILLERS[item]
            return self.rng.choice(self.econ.gear_prices(category, quality, level, self.class_id))
        return 0

    def simulate(self) -> Result:
        econ, rng = self.econ, self.rng
        result = Result(max_level=self.max_level)
        arrivals: dict[int, list[str]] = collections.defaultdict(list)
        # [on sale from, price, kind, item, priority, progression]
        purchases: list[list[Any]] = []
        for region, name, item, classification, *spell in self.seed["locations"]:
            progression = bool(classification & 1)
            item = item if progression else self.reroll(item)
            if name.startswith("Stone Shop:"):
                tier = int(name.split("Level ")[1][:2])
                # The shop shows what each item holds, so its progression is bought first.
                price = self.settings.price(tier, self.goal, self.items_per_tier)
                purchases.append([tier, price, f"shop{tier}", item, 0 if progression else 2, progression])
            elif spell and spell[0] in RIDING:
                kind, level, priority = RIDING[spell[0]]
                purchases.append([level, econ.riding[spell[0]], kind, item, priority, progression])
            else:
                # The rest of a bracket's checks are made at some level of the bracket.
                lo = BRACKETS[REGION_INDEX[region]]
                arrivals[rng.randint(max(1, lo), min(lo + 4, self.max_level))].append(item)

        money = 0.0
        pending: list[list[Any]] = []
        training_debt = 0.0
        xp_bonus = 0
        for level in range(1, self.max_level + 1):
            # The experience rate bonus shortens the grind between level checks, so half of it goes into
            # fewer kills and quests per level.
            play = econ.baseline_income(level) * self.activity * math.exp(rng.gauss(0, 0.1)) / (1 + xp_bonus / 200)
            result.income["play"] += play
            money += play * (1 - self.upkeep)
            for item in arrivals.get(level, []):
                if item == "Progressive Experience Rate":
                    xp_bonus = min(120, xp_bonus + 40)
                money += self.receive(item, level, result)

            training_debt += econ.training[self.class_id].get(level, 0)
            pending += [p for p in purchases if p[0] == level]
            pending.sort(key=lambda p: (p[4], p[1]))

            # Training comes first, then the checks: the cheapest of each priority, saving up for shop
            # progression and riding rather than buying anything after them.
            paid = min(money, training_debt)
            money -= paid
            training_debt -= paid
            saving = training_debt > 0
            unpaid = []
            for p in pending:
                if not saving and money >= p[1]:
                    money -= p[1]
                    result.bought[(p[2], sum(1 for k in result.bought if k[0] == p[2]))] = level
                    if p[5]:
                        result.stalls.append((p[2], level - p[0]))
                    money += self.receive(p[3], level, result)
                else:
                    unpaid.append(p)
                    saving = saving or p[4] < 2
            pending = unpaid
        result.stalls += [(p[2], self.max_level + 1 - p[0]) for p in pending if p[5]]
        return result

    def receive(self, item: str, level: int, result: Result) -> int:
        value = self.item_value(item, level)
        if item == "Gold Pouch":
            result.income["pouch"] += value
        elif item in GEAR_FILLERS:
            result.income["gear"] += value
        return value


def run_batch(
    econ: Economy,
    seeds: list[dict[str, Any]],
    settings: Settings,
    runs_per_seed: int = 2,
    activity: float = 1.0,
    gear_sold: float = 0.75,
    upkeep: float = 0.05,
    rng_seed: int = 7,
) -> list[Result]:
    rng = random.Random(rng_seed)
    return [Run(econ, seed, settings, rng, activity, gear_sold, upkeep).simulate() for seed in seeds for _ in range(runs_per_seed)]


def load_economy(path: str) -> Economy:
    with open(path, encoding="utf-8") as f:
        return Economy(json.load(f))


def load_seeds(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [seed for seed in map(json.loads, f) if seed.get("ok")]


def percentile(values: list[int], q: float) -> int:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * q))]


def median(values: list[int]) -> float:
    return statistics.median(values) if values else 0.0


# What the shop and the fillers were before the balancing.
BEFORE_PRICES: PriceTable = [
    (1, 25 * COPPER),
    (5, 1 * SILVER),
    (10, 5 * SILVER),
    (15, 10 * SILVER),
    (20, 20 * SILVER),
    (25, 30 * SILVER),
    (30, 50 * SILVER),
    (35, 75 * SILVER),
    (40, 1 * GOLD),
    (45, 1 * GOLD + 50 * SILVER),
    (50, 2 * GOLD),
    (55, 2 * GOLD + 50 * SILVER),
    (60, 5 * GOLD),
    (65, 10 * GOLD),
    (70, 20 * GOLD),
    (75, 30 * GOLD),
]
BEFORE_WEIGHTS = {
    "Gold Pouch": 15,
    "Random Uncommon Weapon": 16,
    "Random Rare Weapon": 12,
    "Random Uncommon Armor": 20,
    "Random Rare Armor": 16,
    "Random Uncommon Jewelry": 12,
    "Random Rare Jewelry": 9,
    "Scroll of Divination": 6,
    "Tome of Insight": 6,
    "Enduring Soulstone": 6,
    "Random World Buff": 6,
}


def before_pouch(level: int, goal: int) -> int:
    level = max(5, level)
    result = 6.0731 * level**2.0641 if level <= 60 else 2.3e-6 * level**5.9408
    return round(result * 1.5)


# The balancing: SHOP_PRICES in the module's AP_StoneShop.cpp, the filler weights of items/, and a Gold
# Pouch worth a shop item. Keep them in step with the code they mirror.
SHOP_PRICES: PriceTable = [
    (1, 1 * SILVER + 40 * COPPER),
    (5, 7 * SILVER),
    (10, 35 * SILVER),
    (15, 60 * SILVER),
    (20, 1 * GOLD),
    (25, 1 * GOLD + 50 * SILVER),
    (30, 2 * GOLD + 40 * SILVER),
    (35, 4 * GOLD + 80 * SILVER),
    (40, 8 * GOLD),
    (45, 14 * GOLD),
    (50, 25 * GOLD),
    (55, 45 * GOLD),
    (60, 75 * GOLD),
    (65, 140 * GOLD),
    (70, 240 * GOLD),
    (75, 420 * GOLD),
]
FILLER_WEIGHTS = {
    "Gold Pouch": 8,
    "Random Uncommon Weapon": 18,
    "Random Rare Weapon": 13,
    "Random Uncommon Armor": 22,
    "Random Rare Armor": 18,
    "Random Uncommon Jewelry": 13,
    "Random Rare Jewelry": 10,
    "Scroll of Divination": 10,
    "Tome of Insight": 10,
    "Enduring Soulstone": 10,
    "Random World Buff": 10,
}


def shop_pouch(level: int, goal: int) -> int:
    return step_price(SHOP_PRICES, min(level, goal - 6) if goal else level)


BEFORE = Settings("before", BEFORE_PRICES, before_pouch, BEFORE_WEIGHTS)
CURRENT = Settings("current", SHOP_PRICES, shop_pouch, FILLER_WEIGHTS, cap_last_tier=True, scale_by_items=True)


def income_curve(econ: Economy, levels_of_play: float) -> PriceTable:
    """Tier prices at `levels_of_play` levels' worth of a bracket's average income, smoothed with a quadratic
    fit of their logarithm from level 10 on: a starting point for a new price table."""
    raw = {lo: levels_of_play * statistics.mean(econ.baseline_income(level) for level in range(max(1, lo), lo + 5)) for lo in BRACKETS}
    xs = [lo for lo in BRACKETS if lo >= 10]
    a, b, c = fit_quadratic(xs, [math.log(raw[lo]) for lo in xs])
    return [(max(1, lo), round(math.exp(a * lo * lo + b * lo + c) if lo >= 10 else raw[lo])) for lo in BRACKETS]


def fit_quadratic(xs: list[int], ys: list[float]) -> tuple[float, float, float]:
    sx = [float(sum(x**k for x in xs)) for k in range(5)]
    sxy = [sum(y * x**k for x, y in zip(xs, ys)) for k in range(3)]
    m = [[sx[4], sx[3], sx[2], sxy[2]], [sx[3], sx[2], sx[1], sxy[1]], [sx[2], sx[1], sx[0], sxy[0]]]
    for i in range(3):
        for j in range(i + 1, 3):
            f = m[j][i] / m[i][i]
            m[j] = [mj - f * mi for mj, mi in zip(m[j], m[i])]
    c = m[2][3] / m[2][2]
    b = (m[1][3] - m[1][2] * c) / m[1][1]
    a = (m[0][3] - m[0][2] * c - m[0][1] * b) / m[0][0]
    return a, b, c
