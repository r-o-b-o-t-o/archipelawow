"""Generates solo seeds and writes what each location holds, one seed per line.

From the Archipelago root: python -m worlds.worldofwarcraft.tools.gold_sim.sample_seeds <out.jsonl> <seeds> <goal> [workers] [option=value ...]
"""

import json
import logging
import multiprocessing
import random
import sys
import time
from typing import Any


def combinations() -> list[tuple[str, str]]:
    from ...options import PLAYABLE_COMBINATIONS, CharacterClass, CharacterRace

    return [(CharacterRace.get_option_name(r).lower().replace(" ", "_"), CharacterClass.get_option_name(c).lower()) for r, c in PLAYABLE_COMBINATIONS]


def generate(job: tuple[dict[str, Any], int]) -> dict[str, Any]:
    logging.disable(logging.CRITICAL)
    from test.general import setup_multiworld

    from Fill import FillError, distribute_items_restrictive
    from worlds.AutoWorld import call_all

    from ...locations.spells import SPELLS_CONTAINER
    from ...world import World

    options, seed = job
    spells = {loc.name: loc.data.id for loc in SPELLS_CONTAINER.all_spells}
    try:
        multiworld = setup_multiworld(World, seed=seed, options=options)
        distribute_items_restrictive(multiworld, "swap")
        call_all(multiworld, "post_fill")
    except FillError:
        return dict(options=options, seed=seed, ok=False)

    world = multiworld.worlds[1]
    assert isinstance(world, World)
    locations = []
    for loc in multiworld.get_locations(1):
        if loc.address is None or loc.item is None or loc.parent_region is None:
            continue
        entry: list[Any] = [loc.parent_region.name, loc.name, loc.item.name, int(loc.item.classification)]
        if loc.name in spells:
            entry.append(spells[loc.name])
        locations.append(entry)
    return dict(options=options, seed=seed, ok=True, max_level=world.max_location_level(), level_cap=world.level_cap(), locations=locations)


def main() -> None:
    out, count, goal = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    extra = dict(arg.split("=", 1) for arg in sys.argv[5:])
    rng = random.Random(1234)
    pairs = combinations()
    jobs = []
    for _ in range(count):
        race, character_class = rng.choice(pairs)
        jobs.append((dict(goal=goal, character_race=race, character_class=character_class, **extra), rng.randrange(1 << 30)))

    started = time.time()
    with open(out, "w", encoding="utf-8") as f, multiprocessing.Pool(workers) as pool:
        for n, result in enumerate(pool.imap_unordered(generate, jobs), 1):
            f.write(json.dumps(result) + "\n")
            print(f"{n}/{count} in {time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
