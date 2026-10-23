# Gold simulation

A Monte Carlo model of a solo run's gold, used to price the Stone Shop and size the Gold Pouch. It plays
generated seeds level by level: income from kills and quests, the Gold Pouches and sold gear the fillers
hand out, and the training, riding checks and shop items the character pays for.

Run everything from the Archipelago root, with `SKIP_REQUIREMENTS_UPDATE=1` set as for a generation.

```bash
# 1. The world database's income and cost curves. QuestXP.dbc is in the server's dbc folder.
python -m worlds.worldofwarcraft.tools.gold_sim.export_db out/db.json <server>/data/dbc/QuestXP.dbc

# 2. Seeds to play: <out.jsonl> <count> <goal> [workers] [option=value ...]
python -m worlds.worldofwarcraft.tools.gold_sim.sample_seeds out/seeds_80.jsonl 150 level_80 8
python -m worlds.worldofwarcraft.tools.gold_sim.sample_seeds out/seeds_80_most.jsonl 80 level_80 8 stone_shop_items_per_tier=9

# 3. The report, before and after the balancing, at three paces of play.
python -m worlds.worldofwarcraft.tools.gold_sim.report out/db.json out/seeds_80.jsonl out/seeds_80_most.jsonl --detail
```

`export_db` reads MySQL through the `mysql` client (`--mysql` for its path; `--user`, `--password`,
`--world` and `--characters` for the rest). Fillers are drawn again with the weights in `sim.py`, so new
weights can be tried without generating new seeds. For a new price table, `sim.income_curve(econ, 0.7)`
gives the smoothed curve the current one was rounded from.

## The model

- **Income per level.** A level's experience is split between kills and quests in the proportions of the
  calibration character. Kills pay the spawn-weighted average coin of creatures of that level and the
  vendor value of their loot tables; quests pay the average money and item rewards of solo quests of that
  level, with their experience from `QuestXP.dbc`.
- **Calibration.** `--guid` names a character levelled without the module while the
  mod-playthrough-stats module recorded it (280, Robotostats, a mage through level 14). Its looted coin,
  quest money and vendor sales scale the three income sources above: it looted 1.4 times the creature
  average, earned 0.8 times the quest average, and vendored 0.7 of what dropped.
- **Pace.** `activity` scales the kills and quests per level: 1.0 is the calibration character's pace,
  and each run varies by ±15%. The Progressive Experience Rate takes half its bonus off the kills and
  quests of a level.
- **Checks.** A bracket's free checks land at random levels of the bracket. Shop items and riding checks
  are bought: training first, then the shop's progression (the shop shows what it holds), then riding,
  then the rest of the shop, cheapest first. The character saves up for progression and riding rather
  than buying shop filler past them, but never for Artisan Riding.
- **Fillers.** A Gold Pouch pays what the module pays. A gear filler is sold 75% of the time, for the
  vendor price of a piece the module's gear pool could roll for the class at that level.
- **Upkeep.** Repairs and the like take 5% of the income.

## Reading the report

- *last item of a tier after N levels*: the median levels between a tier going on sale and its last
  item being bought, over the tiers from 10 up to the one before the last.
- *shop progression 5+ levels late*: the share of runs where a shop item holding progression for the
  character waits 5 levels or more for the gold. *riding progression* is the same for Apprentice,
  Journeyman, Expert and Cold Weather Flying.

## Limits

- The pace of an Archipelago run is the largest unknown: the calibration is a plain playthrough.
  Recording an Archipelago character with mod-playthrough-stats would pin `activity` down.
- The calibration covers levels 1 to 14; higher levels follow the database's averages.
- Only solo seeds are modelled: in a multiworld, the character's fillers arrive at other times.
