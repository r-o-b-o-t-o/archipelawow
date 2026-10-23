"""Exports what the gold model needs from the world and characters databases to a JSON file.

python -m worlds.worldofwarcraft.tools.gold_sim.export_db <out.json> <QuestXP.dbc> [--mysql PATH] [--user root]
    [--password root] [--world acore_world] [--characters acore_characters] [--guid N]

QuestXP.dbc comes from the server's dbc folder: the core reads quest experience from it, not from questxp_dbc.
--guid picks the calibration character: one played without the module, levelled with mod-playthrough-stats.
"""

import argparse
import collections
import json
import struct
import subprocess
from typing import Any

QUEST_ITEM_CLASS = 12


class Database:
    def __init__(self, args: argparse.Namespace):
        self.args = args

    def query(self, sql: str, database: str) -> list[list[float]]:
        a = self.args
        out = subprocess.run(
            [a.mysql, f"-u{a.user}", f"-p{a.password}", "--batch", "--skip-column-names", database, "-e", sql],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout
        return [[float(v) if v not in ("NULL", "") else 0.0 for v in line.split("\t")] for line in out.splitlines() if line]

    def world(self, sql: str) -> list[list[float]]:
        return self.query(sql, self.args.world)


def read_quest_xp(path: str) -> dict[int, list[int]]:
    """QuestXP.dbc: by quest level, the experience of each RewardXPDifficulty."""
    with open(path, "rb") as f:
        data = f.read()
    _, records, fields, size, _ = struct.unpack("<4s4I", data[:20])
    rows = [struct.unpack(f"<{fields}i", data[20 + i * size : 20 + (i + 1) * size]) for i in range(records)]
    return {row[0]: list(row[1:]) for row in rows}


def spawn_weighted(rows: list[list[float]], value: Any) -> dict[int, float]:
    """Mean of value(row) by creature level, weighted by spawns. Rows are minlevel, maxlevel, ..., spawns."""
    sums: dict[int, list[float]] = collections.defaultdict(lambda: [0.0, 0.0])
    for row in rows:
        level = round((row[0] + row[1]) / 2)
        sums[level][0] += row[-1] * value(row)
        sums[level][1] += row[-1]
    return {level: total / n for level, (total, n) in sorted(sums.items()) if n}


def loot_values(db: Database) -> Any:
    """Expected vendor value of a creature's loot, quest items left out."""
    sell = {int(e): (p, int(c)) for e, p, c in db.world("SELECT entry, SellPrice, Class FROM item_template")}
    templates: dict[str, dict[int, list[list[float]]]] = {}
    for table in ("creature_loot_template", "reference_loot_template"):
        store: dict[int, list[list[float]]] = collections.defaultdict(list)
        for row in db.world(f"SELECT Entry, Item, Reference, Chance, QuestRequired, GroupId, MinCount, MaxCount FROM {table}"):
            store[int(row[0])].append(row[1:])
        templates[table] = store
    memo: dict[tuple[str, int], float] = {}

    def value(table: str, entry: int) -> float:
        if (table, entry) in memo:
            return memo[(table, entry)]
        memo[(table, entry)] = 0.0
        groups: dict[float, list[tuple[float, float]]] = collections.defaultdict(list)
        total = 0.0
        for item, ref, chance, quest, group, low, high in templates[table].get(entry, []):
            if quest:
                continue
            if ref:
                worth = value("reference_loot_template", int(ref)) * max(1.0, high)
            else:
                price, item_class = sell.get(int(item), (0.0, 0))
                worth = 0.0 if item_class == QUEST_ITEM_CLASS else price * (low + high) / 2
            if group:
                groups[group].append((chance, worth))
            else:
                total += chance / 100 * worth
        # A group drops one of its items: those without a chance share what the others leave.
        for entries in groups.values():
            total += sum(c / 100 * w for c, w in entries if c > 0)
            equal = [w for c, w in entries if c == 0]
            if equal:
                total += max(0.0, 100 - sum(c for c, _ in entries if c > 0)) / 100 * sum(equal) / len(equal)
        memo[(table, entry)] = total
        return total

    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out")
    parser.add_argument("quest_xp_dbc")
    parser.add_argument("--mysql", default="mysql")
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", default="root")
    parser.add_argument("--world", default="acore_archipelawow_world")
    parser.add_argument("--characters", default="acore_archipelawow_characters")
    parser.add_argument("--guid", type=int, default=280)
    args = parser.parse_args()
    db = Database(args)
    out: dict[str, Any] = {}

    out["xp_needed"] = {int(level): int(xp) for level, xp in db.world("SELECT Level, Experience FROM player_xp_for_level")}

    # Killable creatures, by level and spawn count: friendly NPCs have no loot table.
    creatures = db.world("""SELECT ct.minlevel, ct.maxlevel, ct.mingold, ct.maxgold, ct.lootid, COUNT(*) FROM creature_template ct
        JOIN creature c ON c.id = ct.entry
        WHERE ct.`rank` = 0 AND ct.type <> 8 AND ct.lootid > 0 AND ct.minlevel BETWEEN 1 AND 83
        GROUP BY ct.entry""")
    out["mob_coin"] = spawn_weighted(creatures, lambda row: (row[2] + row[3]) / 2)
    loot = loot_values(db)
    out["drop_value"] = spawn_weighted(creatures, lambda row: loot("creature_loot_template", int(row[4])))

    # Solo quests that give experience: money, experience and the vendor value of their item rewards, by
    # quest level. Dailies, weeklies, group, dungeon, raid and PvP quests are left out.
    quest_xp = read_quest_xp(args.quest_xp_dbc)
    money_reward = {int(row[0]): row[1:] for row in db.world("SELECT * FROM quest_money_reward")}
    sell = {int(e): p for e, p in db.world("SELECT entry, SellPrice FROM item_template WHERE SellPrice > 0")}
    sums: dict[int, list[float]] = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for row in db.world("""SELECT QuestLevel, RewardMoney, RewardMoneyDifficulty, RewardXPDifficulty,
        RewardItem1, RewardAmount1, RewardItem2, RewardAmount2, RewardItem3, RewardAmount3, RewardItem4, RewardAmount4,
        RewardChoiceItemID1, RewardChoiceItemID2, RewardChoiceItemID3, RewardChoiceItemID4, RewardChoiceItemID5, RewardChoiceItemID6
        FROM quest_template
        WHERE QuestLevel BETWEEN 1 AND 80 AND (Flags & 0x9000) = 0 AND QuestInfoID NOT IN (1, 41, 62, 81, 85, 88, 89)
        AND SuggestedGroupNum <= 1 AND RewardXPDifficulty > 0"""):
        level, money, money_difficulty, xp_difficulty = int(row[0]), row[1], int(row[2]), int(row[3])
        # Quest::GetRewOrReqMoney: a money difficulty replaces RewardMoney with the table's amount.
        if money_difficulty and level in money_reward:
            money = money_reward[level][money_difficulty]
        items = sum(sell.get(int(row[4 + 2 * i]), 0) * max(1, row[5 + 2 * i]) for i in range(4))
        choice = max(sell.get(int(e), 0) for e in row[12:18])
        s = sums[level]
        s[0] += 1
        s[1] += max(0.0, money)
        s[2] += quest_xp.get(level, [0] * 10)[min(xp_difficulty, 9)]
        s[3] += items + choice
    out["quests"] = {level: dict(count=n, money=m / n, xp=x / n, items=i / n) for level, (n, m, x, i) in sorted(sums.items())}

    # Each class's training, from its fullest trainer, by level. Riding is a check of its own.
    trainers: dict[tuple[int, int], list[tuple[int, float]]] = collections.defaultdict(list)
    for class_id, trainer, level, cost in db.world(
        "SELECT t.Requirement, t.Id, ts.ReqLevel, ts.MoneyCost FROM trainer t JOIN trainer_spell ts ON ts.TrainerId = t.Id WHERE t.Type = 0"
    ):
        trainers[(int(class_id), int(trainer))].append((int(level), cost))
    fullest: dict[int, list[tuple[int, float]]] = {}
    for (class_id, _), spells in trainers.items():
        if len(spells) > len(fullest.get(class_id, [])):
            fullest[class_id] = spells
    training: dict[int, dict[int, float]] = {}
    for class_id, spells in fullest.items():
        per_level: dict[int, float] = collections.defaultdict(float)
        for level, cost in spells:
            per_level[max(1, level)] += cost
        training[class_id] = dict(sorted(per_level.items()))
    out["training"] = training
    out["riding"] = {
        int(spell): (int(level), cost)
        for spell, level, cost in db.world(
            "SELECT SpellId, MIN(ReqLevel), MIN(MoneyCost) FROM trainer_spell WHERE SpellId IN (33388, 33391, 34090, 34091, 54197) GROUP BY SpellId"
        )
    }

    # The gear the Random gear fillers draw from: see GearPool::Build in the module. Rows are category,
    # quality, required level, AllowableClass, armor subclass (-1 for anything but armor) and vendor price.
    gear = []
    for _, item_class, sub, inventory, quality, level, allowed, price in db.world(
        """SELECT entry, Class, SubClass, InventoryType, Quality, RequiredLevel, AllowableClass, SellPrice FROM item_template
        WHERE Quality IN (2, 3) AND RequiredLevel BETWEEN 2 AND 80 AND RequiredSkill = 0 AND RequiredSpell = 0
        AND RequiredReputationFaction = 0 AND requiredhonorrank = 0 AND Class IN (2, 4)
        AND (entry IN (SELECT Item FROM creature_loot_template) OR entry IN (SELECT Item FROM reference_loot_template)
            OR entry IN (SELECT Item FROM gameobject_loot_template) OR entry IN (SELECT Item FROM item_loot_template)
            OR entry IN (SELECT item FROM npc_vendor) OR entry IN (SELECT RewardChoiceItemID1 FROM quest_template)
            OR entry IN (SELECT RewardChoiceItemID2 FROM quest_template) OR entry IN (SELECT RewardChoiceItemID3 FROM quest_template)
            OR entry IN (SELECT RewardChoiceItemID4 FROM quest_template) OR entry IN (SELECT RewardItem1 FROM quest_template))"""
    ):
        item_class, sub, inventory = int(item_class), int(sub), int(inventory)
        if item_class == 2:
            category = None if sub in (9, 11, 12, 14, 17, 20) else "weapon"
        elif sub in (1, 2, 3, 4) or (sub == 0 and inventory == 16):
            category = "armor"
        elif sub == 6 or (sub == 0 and inventory == 23):
            category = "weapon"
        elif sub in (7, 8, 9, 10) or (sub == 0 and inventory in (2, 11, 12)):
            category = "jewelry"
        else:
            category = None
        if category:
            gear.append([category, int(quality), int(level), int(allowed), sub if item_class == 4 else -1, int(price)])
    out["gear"] = gear

    # Calibration: the recorded levels of a character played without the module.
    columns = ["level", "kills", "xp_kill", "xp_quest", "xp_explore", "money_looted", "money_gained", "quests"]
    rows = db.query(
        f"SELECT {', '.join(columns)} FROM playthrough_stats_level WHERE guid = {args.guid} AND partial = 0 AND kills > 0 ORDER BY level",
        args.characters,
    )
    out["calibration"] = [dict(zip(columns, row)) for row in rows]
    levels = [int(row[0]) for row in rows]
    out["calibration_quest_money"] = sum(
        money
        for _, money in db.query(
            f"""SELECT q.QuestLevel, GREATEST(q.RewardMoney, 0) FROM character_queststatus_rewarded r
            JOIN {args.world}.quest_template q ON q.ID = r.quest WHERE r.guid = {args.guid} AND q.QuestLevel <= {max(levels)}""",
            args.characters,
        )
    )

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
