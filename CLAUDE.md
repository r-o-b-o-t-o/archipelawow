# CLAUDE.md

Archipelago APWorld for World of Warcraft 3.3.5a. It runs inside an Archipelago checkout as
`worlds/worldofwarcraft`; `README.md` covers the setup.

## Related repositories

- `mod-i-found-your-sword` — the AzerothCore module that plays the seeds this world generates. Item and
  location names and IDs, and every key of `fill_slot_data()` in `world.py`, are parsed by the module
  (`src/network/AP_Client.cpp`). A change to any of those on one side needs a matching change on the
  other.
- `archipelawow-data-extractor` — generates `data/quests.json` and `data/spells.json`. Never hand-edit
  them: change the extractor and regenerate. A change to their shape needs a matching change in
  `quest_model.py` / `spell_model.py` here.

## Code

- Write straightforward code. Skip minor edge cases (ones only reachable with malformed data or
  options); point out notable ones (reachable in normal generation or play, or that would make a seed
  unbeatable) and let the user decide whether they are worth handling.
- Comment only when the code isn't obvious or there is an implication a future maintainer could easily
  miss. Keep comments brief and don't restate the code.
- Development uses Python 3.13, but the code must run on 3.11, the oldest Archipelago starts on: no
  newer syntax or stdlib. CI type-checks with pyright in `standard` mode at 3.11.
- Formatting is `black` and `isort --profile black`, both at line length 150; CI rejects anything else.

## Verifying changes

- There is no test suite; a generation is the check. From the Archipelago checkout:
  `SKIP_REQUIREMENTS_UPDATE=1 python Generate.py --player_files_path <dir> --seed <n>` (the variable
  stops `ModuleUpdate` blocking on an interactive pip prompt). The web host must be restarted to pick
  up code changes.
- The world must be registered exactly once: this repository cloned or linked as
  `worlds/worldofwarcraft` and no second copy anywhere under `worlds/`. A duplicate registers the game
  twice and every result is meaningless.
- For unit-style checks without a full generation, subclass `test.bases.WorldTestBase` from the
  Archipelago checkout and run from its root so its `test` and `worlds` packages resolve.

## Packaging

`.apignore` lists what stays out of the `.apworld`; add any new repository-only file (docs, CI, editor
or agent config) to it.

## Commits

- Conventional Commits with concise messages; one logical change per commit.
