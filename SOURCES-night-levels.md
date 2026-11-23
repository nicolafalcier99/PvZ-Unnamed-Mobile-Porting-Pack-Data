# Sources: Night levels (rules-night-levels.json, feature `nightLevels`)

Plan 3 Task 3. Study (source of truth): the research notes (w2-night) sections 2.3, 2.4, 3, 4, 5. Exe =
the Unnamed 1.3beta2 `PlantsVsZombies.exe` (read only via the study's exports; nothing run).
Code: `app/src/Mod/Unnamed/NightLevels.*` (pure rules), `app/src/Mod/Engine/NightLevels.*` (engine side),
tests `app/tests/test_night_levels.cpp`.

| Keys | Value | Evidence | Conf |
|---|---|---|---|
| `nightLevels.startGraves.<level>.firstCol`, `.c<col>` | exe table, see below | exe `Board::InitLevel` 0x40A945.. calls `AddGraveStones(col, count)` 0x408FC0 (w2 3.1). Only 2-8 differs from PvZ-Portable (Board.cpp `mLevel == 17 \|\| 18 \|\| 19` = 11 graves); the exe has `cmp eax,0x12` in the 7-grave group at 0x40A978. Whether 1051 vanilla or a mod patch is open (w2 8.10); the port follows the exe. | H |
| `nightLevels.allowExtra.count` / `.0.level` / `.0.type` | 1 / 11 / 2 | exe gZombieAllowedLevels 0x6A35B0 (stride 0xCC) vs PvZ-Portable Challenge.h:267: one difference, Conehead allowed on level 11 (2-1) (w2 4.1, `tools/w2_level_tables.py`) | H |
| `nightLevels.goldFootball.type` / `.variant` / `.graveType` | 7 / 258 (0x102) / 7 | DieNoLoot path 0xC03520 sets 0xC035AE = 1 and calls SpawnZombiesFromGraves 0x412CE0. With the flag set, hook 86 (0xC05580 asm: `cmp [0xc035ae],1; jz 0x412d24`) jumps straight to the grave loop (no pool/sky spawn) and hook 88 (0xC0358D) skips the Rand(25) re-roll and uses type 7 (w2 2.3; Day study 8.3). | M (flow read; not seen in game) |
| `nightLevels.carnival.summonerType` / `.everyBackups` / `.skipVariant` / `.passesHypnosis` | 8 / 12 / 260 (0x104) / 1 | SummonBackupDancer hook 587 0x528820 -> 0xC03A50 -> 0xC03AED -> 0x7966BA -> 0xC03B10 -> 0x7966C0 asm `cmp [ebx+0x12c],0xc; jl; mov [ebx+0x12c],0; call 0x412CE0`; not counted for variant 0x104 (which stores a type in +0x12C). The call passes the dancer's hypnosis flag (w2 2.4). Almanac "every 3rd summon" = 12 backups (3 x 4). | H (count), M (hypnosis argument) |

Start-grave table (column: count; column 8 = rightmost):

| Levels | Graves | Total |
|---|---|---|
| 2-1, 2-2, 2-3 (11-13) | 6:1, 7:1, 8:2 | 4 |
| 2-4, 2-6, 2-8 (14, 16, 18) | 5:1, 6:1, 7:2, 8:3 | 7 |
| 2-7, 2-9 (17, 19) | 4:1, 5:2, 6:2, 7:3, 8:3 | 11 |
| 2-10 (20) | 3:1, 4:2, 5:2, 6:2, 7:3, 8:3 | 13 |
| 2-5 Whack-a-Zombie (15) | no row: vanilla `WhackAZombiePlaceGraves(9)` | 9 |

No new keys (vanilla or already built):
- Final-wave grave re-roll (each of Normal, Flag, Cone, Pole, Bucket, Newspaper, Door, Football, Backup, Jack,
  Gargantuar, Imp 1/16; vanilla Normal/Cone pick 1/4; allow list not checked): hook 88 is one exe site for all
  levels, already in `rules-day-levels.json` (`dayLevels.graveRise.*`, Plan 2). test_night_levels pins the exact
  distribution.
- Wave counts and allowed lists other than 2-1: vanilla tables (exe 0x6A34E8, 0x6A35B0). Budgets: Plan 2 x4.
- Start sun 50: vanilla `Board::InitLevel` else-branch (w2 4.1, M).
- Whack-a-Zombie (2-5): vanilla spawner, 8 waves, 9 graves + top-up (w2 4.2, M: absence of hooks).
- Crazy Dave seed-slot offers: vanilla `CutScene::StartLevelIntro` (dialogs 1501 on 13..24 except 15/20/21, 1551 on
  16..24 except 20/21) and prices 75/500/2000/8000 x10 (w2 4.3, H).
