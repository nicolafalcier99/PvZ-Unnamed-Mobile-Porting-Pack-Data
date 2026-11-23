# Sources: Adventure levels 51-73 (levels-51-73.json, rules-later-levels.json, feature `laterLevels`)

Plan 7 Task 1 (infrastructure of worlds 6 and 7 and the hidden levels 71-73). Study (source of truth):
the research notes (w6-w7-and-new-content) sections 1.1, 1.2, 2.1, 2.2, 6, 7 and 8. Exe =
the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only (study export the research notes (hooks2) through
the research notes (w67_fn), and one static `r2 pD` of 0x41C1C0; nothing run). Code: `app/src/Mod/Unnamed/LaterLevels.*`
(pure rules and the table), `app/src/Mod/Engine/LaterLevels.*` (engine side), `app/src/Mod/Engine/SpecialLevels.*`
(empty hook points for Task 3), tests `app/tests/test_later_levels.cpp` (its last two tests compare both JSON files with
the study's table, transcribed separately in the test).

The special scripts of 55 (shooter), 65 (star snake), 70 (giant Newspaper boss) and 71-73 are **Task 3**: the table only
names them (`"special"`). World-7 zombie rules are **Task 2**.

## levels-51-73.json (one row per level, keyed by level number)

| Field | Meaning | Evidence | Conf |
|---|---|---|---|
| `background` | `DAY NIGHT POOL FOG ROOF NIGHT_ROOF MUSHROOM_GARDEN GREENHOUSE ZOMBIQUARIUM` = engine `BackgroundType` 0..8 = the exe's `Board+0x554c` codes | hook 24 -> 0x7a2501: level < 61 -> 5, 55 -> 6, 60 -> 4; 61..70 -> 7, 63/64 -> 8, 65 -> 0, 66 -> 4, 67 -> 3, 68 -> 2, 69 -> 1, 70 -> 0; > 70 -> vanilla `PickBackground` (level > 50 = day), written as `DAY` | H |
| `startSun` | sun at level start | hook 30: 0x7981a0 (51..60 -> 150, 60 -> 5000), 0x7a2385 (61..70), 0x95c0e0 (71 -> 150), 0xc12fd0 (72 -> 500). 73: no branch, vanilla 50, so no field | H |
| `waves` | replaces the vanilla `gZombieWaves` value | hook 19 -> 0x798100 (51-60, `cmp eax,idx; mov esi,N`), 0x7a2601 (61-70), 0x95c030 (71); 72, 73: the vanilla table clamped to index 49 = 30. The vanilla replay rule (+10 once the adventure is finished) runs after the hook, so it still applies | H |
| `allowed` | `Board::mZombieAllowed` (pack zombie keys) | hook 176 chain (0x797efd 51, 0x797f1b.. 52-60, 0x7a26c0 61-70, 0x95c040 71, 0xc130a0 72, 0xc132a0 73), decoded by the research notes (w67_allowed). Hook 28 (0x797e94): Adventure level > 50 skips the level table and runs `Challenge::InitZombieWaves` (= these lists) | H |
| `freePotColumns` | pre-placed Flower Pot columns | hook 222 -> 0x798250: 51-54 -> 4, 55 -> 0, 56-60 -> 5; 61+ -> vanilla (roof 3, so 7-6 has 3) | H |
| `firstWaveCountdown` | cs before the first wave | hook 29 -> 0xc134e0: level 73 -> 5000; every other Adventure level the vanilla 1800 | H |
| `fogColumn` | `Board::LeftFogColumn` | 7-7 (67) is the only fog stage past 40. The 1051 exe's `LeftFogColumn` (0x41C1CC, not hooked) tests 31 / 32..36 / 37..40 and otherwise **returns `eax` = mLevel** (static `r2 pD 110 @ 0x41c1c0`), so 7-7's fog starts at column 67: off the lawn, no fog cells. PvZ-Portable's copy asserts and is unreachable there. | H (asm) |
| `introTimer` | hook 220 (0x799090, after `CutScene::PlaceStreetZombies`): 6-10 sets a cut-scene field to 4000 | read by Task 3; Task 1 does not use it (meaning unclear, study U2) | M |
| `special` | `shooter` (55), `starSnake` (65), `boss` (70), `hidden1..3` (71-73) | study 2.3 / 3; ids only | H |

## rules-later-levels.json

| Key | Value | Evidence | Conf |
|---|---|---|---|
| `laterLevels.lastVanillaLevel` | 50 | the vanilla tables end at 50 (`GameConstants.h` NUM_LEVELS); rows apply above it | H |
| `laterLevels.finalLevel` | 73 | `.text` 0x452331 `cmp ecx, 0x49`: finishing 73 sets level 1 and `mFinishedAdventure += 1`, any other level sets level + 1, so 5-10 leads to 6-1. The award code after it (0x452529..0x45259f) is **not** patched and still compares with 50: after 5-10 the first time (`mFinishedAdventure` still 0) the credits / zombie note (award 1), then the profile is on 51; 51-73 show no award screen and give no plant (the next level starts at once); after 73 the next level is 1-1 | H |
| `laterLevels.allowTableIndexAbove` | 0 | `CanZombieSpawnOnLevel` 0x40d6c7..0x40d6cc: level - 1 >= 49 reads index 0 (level 1: Normal only). Used by the final wave's "put in every missing type" (`PutInMissingZombies`): a final wave of 51-73 without a Normal Zombie gets one. Study U13: mod patch or 1051 vanilla unknown; the code is what it is either way | H (code), M (origin) |
| `laterLevels.stageAreaMax` | 8 | display only: 61-70 are "7-x", 71-73 "8-x" (the level skip names them so, `确定跳关至：X-Y`); vanilla clamps the area to 6 (`LawnApp::GetStageString`, the menu sign) | M |
| `laterLevels.skip.needsFinishedAdventure` | 1 | hook 239 0x7a1600: only when `PlayerInfo+0x2c` (mFinishedAdventure) > 0, i.e. after 73 was beaten once | H |
| `laterLevels.skip.min` / `.max` | 1 / 71 | 0x7a1600: `if (temp < 1) temp = 1; if (0x47 < temp) temp = 0x47` | H |
| `laterLevels.skip.bigStep` / `.smallStep` | 10 / 1 | 0x7a1600: Mini-games (0x65) `temp += clickCount * 10`, Puzzle (0x66) `temp += clickCount`; Survival (0x6e) asks "[quote not included]" (OK/No) and OK writes `PlayerInfo+0x24`; a right click on Survival or a middle click (count 3) anywhere cancels ("[quote not included]"); other buttons work as usual and the mode stays on; a right click on Adventure opens the mode ("[quote not included]"), and once open starts the adventure as usual | H (logic), M (count -1 = right click) |
| `laterLevels.skip.longPressTicks` | 50 | **port, not the exe**: the phone has no right click, so a press held 0.5 s on a menu button counts as the right click (open the mode on Adventure, -10 / -1 on Mini-games / Puzzle, cancel on Survival). There is no touch middle click; a long press on Survival cancels | port |
| `laterLevels.rows.6` | `[1,1,1,1,1,0]` | hook 26 0x7982a5: background 6 (mushroom garden) or 9 -> rows 0-4 normal, row 5 dirt (engine `PlantRowType`: 0 dirt, 1 normal, 2 pool) | H |
| `laterLevels.rows.8` | `[1,2,2,2,1,0]` | hook 27 0x7a1e3a: background 8 (Zombiquarium) -> normal, pool, pool, pool, normal, dirt (the grid loop turns pool rows into pool squares for columns 0-8) | H |
| `laterLevels.roofBackgrounds` | `[7]` | V2 (2026-11-23, community "[quote not included]" = like a flat roof): `Board::StageHasRoof` 0x41c0b0 is patched to `cmp eax,7; je true` before the vanilla 4 / 5 tests, so the greenhouse of 7-1 / 7-2 counts as roof wherever the function is **called** (9 calls: CanPlantAt 0x40e23f / 0x40e2c4, InitLawnMowers 0x40bce2, 0x45b8b0 music, 0x460d5c UpdateSquash, 0x4652f1 UpdateShooting, 0x5335e7 zombie, 0x957ce4 / 0x957d14 boss). Inlined `bg==4\|\|bg==5` tests (CutScene 0x43921d / 0x439437 / 0x4397e3 etc.) are untouched, so no starting pots and no slope. Port: `engine::StageCountsAsRoof` at the two CanPlantAt tests (Flower Pot needed; Spikerock refused) and InitLawnMowers (no mowers without the Roof Cleaner). The music, Squash, shooting, zombie and boss calls are not mapped (open) | H (patch), M (site map) |

Strings: `strings/en-corrections-later-levels.txt` holds the four level-skip dialog texts (our English; the exe's own
are GBK strings at 0x8001b4/0x8001bc/0x8001f0/0x800200, not copied). The "on" text adds one line on how to use the
mode, because the exe shows nothing while you change the target. Chinese mode falls back to the English text.

## Rules that need no key (vanilla engine code already does what the exe does)

- **No falling sun and mushrooms awake on backgrounds 1, 3, 5, 6, 8** (hook 30 chain 0x95c0ff, hook 265 0x7a4770):
  the engine's `Board::StageIsNight` is exactly NIGHT, FOG, BOSS (night roof), MUSHROOM_GARDEN, ZOMBIQUARIUM. H.
- **Graves only on background 1** (hook 144 0x796531, `bg == 1` and not mod mode 0x6d): the engine's
  `StageHasGraveStones` is the same, so only 7-9 has graves; level 69 >= 20 takes the vanilla "level 20+" layout. H.
- **Greenhouse rows** (study U1): no mod row code; the engine's day branch (5 normal rows + dirt) is the vanilla path.
- **Wave budget**: Plan 2's x4 for every Adventure level (`dayLevels.waveBudgetMultiplier`, hook 22) applies to 51-73
  too; the study's "no world-6/7 multiplier" means no extra one. First-time formula (`wave / 3 + 1`) because
  `mFinishedAdventure` is 0 until 73 is beaten. H.
- **Money bag** at the end of 51-73 (PvZ-Portable's `Zombie::DropLoot` gives a bag above level 50; the exe's own drop
  code for > 50 was not read); no plant award. M.

## Mac checks (2026-11-23, app 8a7c894, hidden + silent, seed 7, width 1300)

- Wave logs (`-pvzu-log-waves`, `-pvzu-quit-after-waves`) for every level 51-73 in Unnamed: background, wave count and
  allow list as in the table above (`laterLevel` line); waves only hold allowed types plus Flag (flag waves) and a
  Normal added to the final wave; budgets x4 (20 waves: 333, 30: 718, 10: 97). Two runs give identical waves.
- Vanilla 1, 10, 25, 50 and Unnamed 1, 10, 25, 49, 50: wave logs byte-identical to the 1f4edc2 build.
- Play (`-pvzu-dev-fog log -pvzu-autoplay`, 4000 frames) of every level 51-73, first play tick (`laterPlay`): rows
  `111110` everywhere except 63/64 `122210` (Zombiquarium) and 67/68 `112211` (fog / pool); start sun as the table
  (73: 50); first-wave countdown 1800, 73: 5000; free pots 51-54: 20 (4 columns), 55: 0, 56-60: 25, 66: 15 (vanilla
  3); no falling sun (`sunCountDown=0`) on 51-59, 55, 63, 64, 67, 69; 7-9 has 13 graves (vanilla level 20+ layout),
  no other level has graves; 7-7 `fog=1` with fog column 67 (no fog drawn). No assert, crash or hang in 23 runs.
- Screenshots (viewed, deleted): 6-1 night roof with 4 pot columns; 6-5 mushroom garden (5 lawn rows on the garden
  art, Puff-shroom awake); 7-1 greenhouse; 7-3 Zombiquarium with Lily Pads on rows 1-3 only; 7-7 fog stage without fog.
  The three garden backgrounds draw as centred 800-wide boards (the engine's non-wide path), the lawn grid on top of
  art that was drawn for the Zen Garden.
- Finish chain (`-pvzu-dev-win 300`): Unnamed 5-10 -> profile 51, finished 0, credits / zombie note (award 1);
  vanilla 5-10 -> profile 1, finished 1, award 0 (unchanged); 6-1 -> 52, 6-10 -> 61, 7-10 -> 71 and 8-2 -> 73 start
  the next level at once (no award); 8-3 -> profile 1, finished 1. 6-1, 6-10 and 8-3 showed PvZ-Portable's
  achievement-only screen first (the dev autoplay earned an achievement; GOTY feature, not a level award).
- Saves: a game saved by the 1f4edc2 build at Unnamed 5-5 loads and plays on (`-pvzu-dev-continue`, Continue); a
  game saved at 7-3 loads with background 8, rows `122210`, wave 1/30 and its 6 plants; one saved at 8-3 loads with
  its countdown (4737 of 5000). A profile at 51 and at 73 loads; the menu sign reads "6-1" and "8-3".
- Level skip, scripted input on the menu (profile finished once via `-pvzu-dev-finished 1`): a 0.7 s press on
  Adventure opens the mode (dialog), 5 taps on Mini-games 1 -> 51, a long press on Puzzle -> 50, a tap -> 51, a tap
  on Survival asks "Skip to level 6-1?", OK writes 51 (next start: sign "6-1"); a long press on Survival cancels.

## Rulings

- Ruling: the award code keeps comparing with 50 (credits after the first 5-10, then 6-1) — the exe patched only the
  final-level compare (0x452331), not the award branch (0x452529) — cost if wrong: one extra credits screen after 5-10.
- Ruling: above 50 `CanZombieSpawnOnLevel` reads the level-1 column (0x40d6c7) — that is the code, whatever its origin
  (U13) — cost if wrong: final waves of 51-73 get an extra Normal Zombie instead of level 50's missing types.
- Ruling: the garden rows (hooks 26/27) apply to Adventure only for now — the exe applies them to every mode, but the
  Zombiquarium minigame was not tested with them and minigames are a later plan — cost if wrong: that minigame keeps
  vanilla rows until then.
- Ruling: 7-7 keeps the exe's fog column 67 (fog off the lawn) — the 1051 `LeftFogColumn` returns mLevel past 40 —
  cost if wrong: 7-7 should have had visible fog.
- Ruling: 71-73 are written as `DAY` instead of "vanilla PickBackground" — the vanilla chain gives day for any level
  past 50, same result — cost if wrong: none while the vanilla chain is unchanged.
- Ruling: a 0.5 s press is the phone's right click for the level skip, and the "on" dialog says how to use it — the
  phone has no right or middle click and the exe shows nothing while the target changes — cost if wrong: the owner wants
  another gesture or no hint; both are one rule / one string.
- Ruling: 7-10 keeps start sun 500000 in the table — the exe sets it (0x7a2385) — cost if wrong: none now; note the
  engine caps sun at 9990 when sun is added (`Board::AddSunMoney`), which the boss level (Task 3) must look at.
