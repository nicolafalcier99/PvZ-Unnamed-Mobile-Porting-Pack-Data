# Sources: Roof levels (rules-roof-levels.json, feature `roofLevels`)

Plan 6 Task 3 (5-1..5-9; 5-10 Dr. Zomboss is Task 4). Study (source of truth): the research notes (w5-roof) sections 0
(G1, G5, G6), 3 (R1..R5) and 5. Exe = the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only (study
export the research notes (hooks2) through the research notes (w5_show), and a static `r2 pd` of 0x412C30; nothing run). Code:
`app/src/Mod/Unnamed/RoofLevels.*` (pure rules), `app/src/Mod/Engine/RoofLevels.*` (engine side, sites in
`Board::SpawnZombiesFromSky`), the sky-drop type pick in `app/src/Mod/Engine/EliteZombies.cpp` (`SkyDropZombieType`),
tests `app/tests/test_roof_levels.cpp` (its last test compares this JSON with the test's values).

| Keys | Value | Evidence | Conf |
|---|---|---|---|
| `roofLevels.skyDrop.<41..49>.count` / `.points` | 5-1, 5-2: 2 / 3; 5-3..5-5: 3 / 5; 5-6..5-9: 3 / 7 | `Board::SpawnZombiesFromSky` 0x412C30..0x412C81: `cmp [ebx+0x5550]` against 0x29/0x2A -> `esi=2, edi=3`; 0x2B..0x2D -> 3 / 5; else 3 / 7; `esi` capped at the drop grid count (0x412C91). Not changed by the mod (R1: "count 2 on 5-1/5-2, 3 on 5-3.."); identical to PvZ-Portable. Data so it can be modded, as the pool table. 5-10 has no row (boss level; the engine's 3 / 7 stays for a Buckethead umbrella drop there). | H |

## Rules built on keys of other packs (no new key)

- **R1 sky-drop type, 13 kinds** (`dayZombies.skyDrop.typeRollRange` 25, Plan 2): hook 85 at 0x412CA8 -> 0x795C27:
  `Rand(0x19)` drawn again while the roll is 8..14 or 16..20, so the type is uniform over Normal, Flag, Cone, Pole,
  Bucket, Newspaper, Screen Door, Football, Jack-in-the-Box, Ladder, Catapult, Gargantuar, Imp (0..7, 15, 21..24).
  One site for every sky drop (final wave on the roof and the Buckethead umbrella elite). **New in this task:** the exe
  still calls the vanilla picker `PickGraveRisingZombieType` (0x40D770, a weighted `Rand`) at 0x412CA3, *before* the
  hook's jump, and throws its result away. The port now draws it too (`SkyDropType` in `RoofLevels.h`), so the random
  sequence after a sky drop matches the exe; before, Unnamed mode skipped that draw. Test: 2000 drops never give an
  excluded type, each type 95..213 times (expected 154), the vanilla pick drawn once per drop and first. H.
- **R2 final-wave order** (no key): hook 86 (0x412CF5 -> 0x9588A0 -> 0xC05580 -> 0x9588A7): background 4/5 ->
  `call 0x412C30` (sky drop), then `jmp 0x412D24` = the grave loop. PvZ-Portable's `SpawnZombiesFromGraves` already
  runs the grave loop after `SpawnZombiesFromSky` on the roof (it only returns early after the pool spawn), so nothing
  changes; graves on the roof come from vaulting Pole Vaulters (`dayLevels.poleGrave`) and rise with the hook-88
  re-roll. The flag `[0xC035AE]` == 1 path (0xC05587, straight to the grave loop) is the gold Football death
  (`GraveRiseGravesOnly`, Night levels). The study's R2 line ("flag -> only the sky drop") reads that jump the other
  way; the asm jumps to 0x412D24, the grave loop. H (flow), checked on the Mac below (sky drop, then the grave).
- **R3 x4 budget, 5-5 Bungee Blitz** (`dayLevels.waveBudgetMultiplier` 4, hook 22): every Adventure level x4, so 5-5
  goes from vanilla x2 to x4. Its flag waves keep the vanilla 5 bungees and skip the budget (`PickZombieWaves`
  `continue`), as in the exe. Test row + Mac (5 BUNGEE on each flag wave in both modes). H.
- **R4 waves, allowed zombies, start sun** (G5, G6): vanilla tables (`gZombieWaves` 0x6A34E8, `gZombieAllowedLevels`
  0x6A35B0, start sun 50 at 0xC05CE8); the mod's list code (hook 176) only writes levels 51+. No key.
- **R5 Doom-shroom**: crater 24000 cs is `nightPlants.doom.craterCs` (Plan 3, in place 0x466884 / hook 345); it applies
  on the roof as everywhere. The study's "on the roof clears grid items" is not what hook 345 tests: 0xC118F5
  `cmp dword [ebx+0x138],0xf` is `Plant::mImitaterType == SEED_DOOMSHROOM`, not the roof; then every grid item of type 1
  (gravestone) dies and no crater is made (study w2 1.8, "Imitater Doom-shroom"). That is a Night-plants rule, not a
  roof rule, and the port's Imitater morph gives the new plant `mImitaterType = SEED_IMITATER` (48, `Plant.cpp`
  ImitaterMorph), so the test can never be true here; not built in this task (open point for the Imitater/shop plan).
- **R6** Zomboss/Imp out of Melon volleys: Roof plants task.

## Levels 5-1..5-9 (checked on the Mac)

Runs: `pvz-portable -pvzu-mode unnamed|vanilla -pvzu-pack <pack> -pvzu-width 1300 -pvzu-level 41..49 -pvzu-seed 7
-pvzu-autoplay 1-100000 -pvzu-log-waves <file> -pvzu-hidden -pvzu-quit-frame 3000` (`SDL_AUDIO_DRIVER=dummy`), with
`-pvzu-dev-fog log` (passes Dave and the seed chooser in both builds) and, for the final-wave lines,
`-pvzu-dev-roof final-grave` (a risen grave on row 0 col 6, then the real `SpawnZombiesFromGraves`). Wave lists
(`waves`/`allowed`/`graves`/`total` lines) are identical to the app build before this task (accb6e6) line for line in
**both** modes (the roof lines are new). Budgets: sum of zombie values over all waves, seed 7, first-time Adventure.

| Level | Waves (flags) | Allowed (engine = exe 0x6A35B0; Flag on flag waves) | Start sun | Pots (cols) | Sky drop vanilla / Unnamed (seed 7) | Budget vanilla / Unnamed | Award (engine, vanilla) |
|---|---|---|---|---|---|---|---|
| 5-1 (41) | 10 (1) | Normal, Cone, Bungee | 50 | 25 (0-4) | 2: Cone, Cone / Pole, Football | 29 / 97 | Flower Pot (33) |
| 5-2 (42) | 20 (2) | Normal, Cone, Pole, Bucket, Bungee | 50 | 20 (0-3) | 2: Cone, Normal / Flag, Imp | 95 / 333 | Kernel-pult (34) |
| 5-3 (43) | 20 (2) | Normal, Cone, Ladder | 50 | 15 (0-2) | 3: Normal x3 / Bucket, Ladder, Football | 93 / 333 | Coffee Bean (35) |
| 5-4 (44) | 30 (3) | Normal, Cone, Football, Pogo, Ladder | 50 | 15 (0-2) | 3: Normal x3 / Normal, Pole, Catapult | 197 / 718 | watering can (Zen Garden; `GetAwardSeedForLevel` names 36) |
| 5-5 (45) | 20 (2), conveyor | Normal, Cone, Bucket, Ladder + 5 Bungees per flag wave | 50 | 15 (0-2) | 3: Cone, Normal, Cone / Door, Ladder, Bucket | 188 (x2) / 328 (x4) | Garlic (36) |
| 5-6 (46) | 20 (2) | Normal, Cone, Catapult | 50 | 15 (0-2) | 3: Normal x3 / Imp, Ladder, Newspaper | 94 / 333 | Umbrella Leaf (37) |
| 5-7 (47) | 30 (3) | Normal, Cone, Bungee, Ladder, Catapult | 50 | 15 (0-2) | 3: Cone x3 / Pole, Catapult, Door | 196 / 718 | Marigold (38) |
| 5-8 (48) | 20 (2) | Normal, Cone, Gargantuar (Imps come with Gargantuars: pick weight 0) | 50 | 15 (0-2) | 3: Cone x3 / Bucket, Pole, Flag | 102 / 333 | Melon-pult (39) |
| 5-9 (49) | 30 (3) | Normal, Cone, Bucket, Jack, Bungee, Ladder, Catapult, Gargantuar | 50 | 15 (0-2) | 3: Normal x3 / Gargantuar x2, Bucket | 211 / 718 | note (level-end; seed 40 named) |

- Every final-wave run: `devRoof spawned` = 2 x count + 1 (a bungee per dropped zombie, then the grave's zombie) in both
  modes, so the grave loop runs after the sky drop (R2). Vanilla drops are Normal/Cone (vanilla picker); Unnamed drops
  are all in the 13-type list.
- Award pairs as worlds 3 and 4: `GetAwardSeedForLevel` names Garlic for 5-4 and 5-5, but 5-4 drops the watering can,
  so Garlic comes after 5-5; 5-9 drops the note (vanilla `Zombie.cpp` coin choice; the logs show the seed the engine
  names, no level was played to its end). The study table agrees.
- Not seen: a natural final wave (a 5-1 Unnamed autoplay run reached the zombies-won screen with no sky-drop line), the
  sky drop on screen, and elites of the dropped zombies (Roof zombies task).
