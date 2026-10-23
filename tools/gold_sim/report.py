"""Reports how hard the shop is to buy out, and what it costs the riding checks.

python -m worlds.worldofwarcraft.tools.gold_sim.report <db.json> <seeds.jsonl> [more seeds.jsonl ...] [--detail] [--activity 0.7 1.0 1.4]
"""

import argparse
import collections

from . import sim

TRACKED_RIDING = ("Apprentice", "Journeyman", "Expert")


def last_tier(seed_max_level: int) -> int:
    return max(lo for lo in sim.BRACKETS if lo <= seed_max_level)


def summary(results: list[sim.Result], items_per_tier: int) -> str:
    """One line: how long a tier's last item waits, how often progression waits 5+ levels behind gold, and pouch share."""
    final = last_tier(results[0].max_level)
    lags = [
        result.bought.get((f"shop{tier}", items_per_tier - 1), result.max_level + 10) - tier
        for result in results
        for tier in sim.BRACKETS
        if 10 <= tier < final
    ]
    shop_late = sum(1 for r in results if any(lag >= 5 and kind.startswith("shop") for kind, lag in r.stalls))
    riding_late = sum(1 for r in results if any(lag >= 5 and kind in TRACKED_RIDING + ("Cold Weather",) for kind, lag in r.stalls))
    riding = collections.defaultdict(list)
    for r in results:
        for (kind, _), level in r.bought.items():
            if kind in TRACKED_RIDING:
                riding[kind].append(level)
    income: dict[str, float] = collections.defaultdict(float)
    for r in results:
        for kind, copper in r.income.items():
            income[kind] += copper
    return (
        f"last item of a tier after {sim.median(lags):>3.0f} levels (p90 {sim.percentile(lags, 0.9):>2})"
        f" | shop progression 5+ levels late in {shop_late / len(results):>4.0%} of runs, riding progression in {riding_late / len(results):>4.0%}"
        f" | riding bought at "
        + ", ".join(f"{kind} {sim.median(levels):.0f}" for kind, levels in riding.items())
        + f" | pouches {income['pouch'] / sum(income.values()):.0%} of income"
    )


def detail(results: list[sim.Result], settings: sim.Settings, seed: dict, items_per_tier: int) -> None:
    print("tier      price     pouch   levels until item 1 / middle / last is bought: median (p90)")
    for tier in sim.BRACKETS:
        if tier > seed["max_level"]:
            break
        tier = max(1, tier)
        cells = []
        for n in (0, items_per_tier // 2, items_per_tier - 1):
            lags = [r.bought.get((f"shop{tier}", n), r.max_level + 10) - tier for r in results]
            cells.append(f"{sim.median(lags):>3.0f} ({sim.percentile(lags, 0.9):>2})")
        price = settings.price(tier, sim.goal_level(seed), items_per_tier) / sim.GOLD
        pouch = settings.pouch(tier, sim.goal_level(seed)) / sim.GOLD
        print(f"{tier:>4} {price:>9.2f}g {pouch:>8.2f}g   " + "   ".join(cells))
    artisan = [level for r in results for (kind, _), level in r.bought.items() if kind == "Artisan"]
    if any(kind == "Artisan" for r in results for kind, _ in r.stalls) or artisan:
        print(f"Artisan Riding bought in {len(artisan) / len(results):.0%} of runs")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("db")
    parser.add_argument("seeds", nargs="+")
    parser.add_argument("--activity", type=float, nargs="+", default=[0.7, 1.0, 1.4])
    parser.add_argument("--detail", action="store_true")
    args = parser.parse_args()

    econ = sim.load_economy(args.db)
    for path in args.seeds:
        seeds = sim.load_seeds(path)
        items_per_tier = max(1, sum(1 for loc in seeds[0]["locations"] if loc[1].startswith("Stone Shop: Level 05 ")))
        print(f"== {path}: {len(seeds)} seeds, level cap {seeds[0]['level_cap']}, {items_per_tier} shop items per tier")
        for settings in (sim.BEFORE, sim.CURRENT):
            for activity in args.activity:
                results = sim.run_batch(econ, seeds, settings, activity=activity)
                print(f"{settings.label:<8} x{activity:<4} {summary(results, items_per_tier)}")
                if args.detail and activity == 1.0:
                    detail(results, settings, seeds[0], items_per_tier)


if __name__ == "__main__":
    main()
