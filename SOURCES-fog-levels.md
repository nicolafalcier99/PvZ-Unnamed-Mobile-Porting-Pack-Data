# Sources: Fog levels (rules-fog-levels.json, feature `fogLevels`)

Plan 5 Task 3. Study (source of truth): the research notes (w4-fog) sections 4 "Fog rules" and 5 "Levels 4-1..4-10",
unresolved U9 and U12. Exe = the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only (study export
the research notes (hooks2) through the research notes (w4_show); nothing run). Code: `app/src/Mod/Unnamed/FogLevels.*` (pure
rules), `app/src/Mod/Engine/FogLevels.*` (engine side, site in `Board::LeftFogColumn`), tests
`app/tests/test_fog_levels.cpp` (its last test compares this JSON with the test's values).

| Keys | Value | Evidence | Conf |
|---|---|---|---|
| `fogLevels.fullFog` | 0 | Hook 145 at 0x41C1C6 (entry of `Board::LeftFogColumn` 0x41C1C0) -> 0x7A8310: `if (byte 0x800298 == 0 && mode != 0x7C) -> vanilla 0x41C1CC else return 0` (fog from column 0 = the whole lawn). No writer of 0x800298 was found (study U9: options panel handlers not read), so the shipped value is 0. Kept as a rule so the option can be switched on; 1 = whole lawn in every fog stage (the hook sits before the Air Raid / minigame tests). Mode 0x7C is a mod minigame (later plan). | H (hook), M (default 0: no writer found) |
| `fogLevels.fogColumn.<31..40>` | 4-1: 6; 4-2..4-6: 5; 4-7..4-10: 4 | Vanilla `LeftFogColumn` 0x41C1CC (GOTY/PvZ-Portable `Board.cpp` LeftFogColumn: level 31 -> 6, 32..36 -> 5, 37..40 -> 4). Not changed by the mod; data so it can be modded. 4-10 keeps its column but has no fog (stormy night, `StageHasFog`). Minigames (5) and Air Raid (6) stay engine values. | H |
| `poolLevels.poolSpawn.<31..40>.count` / `.points` | 4-1, 4-2: 2 / 3; 4-3..4-5: 3 / 5; 4-6..4-10: 3 / 7 | `Board::SpawnZombiesFromPool` 0x4128F0..0x41296C: `cmp [ebx+0x5550]` against 0x1F/0x20 -> 2 / 3; 0x21..0x23 -> 3 / 5; else 3 / 7 (read for `SOURCES-pool-levels.md`, which left the fog rows to this plan). Identical to PvZ-Portable. Read by the Pool site (`poolLevels` feature), so the fog lawn's final-wave pool risers follow the same table, the hook-81 hypnosis and the hook-86 grave loop. | H |

## Not data here (and why)

- **Blover fog blow 4000 cs**: hook 342 (0x466603 -> 0x7A8450) writes `mFogBlownCountDown` (Board+0x5D4) = 4000, or 1 in
  mod mode 0x7C. 4000 = vanilla (`Plant::BlowAwayFliers`, `Plant.cpp`), so Adventure is unchanged. Blover itself is the
  Fog plants task; no fog key is needed.
- **Plantern fog radius 20** (patch 0x41A702): Fog plants task (`Board.cpp` fog clearing). Torchwood radius 1 and the
  fade speeds are vanilla.
- **Mod mode 0x7C** (hook 135: projectiles of types 4..6 clear fog; hook 145/342 values): not an Adventure mode.
- **Wave budget, U12 resolved**: hook 22 (0x409887 -> 0x79AB00 -> 0xA878A4): only when `eax == 0x8B` does the exe
  run the vanilla multiplier chain (x3 for levels 10/20/30/40 = `[app+0x82C]+0x24` 0x0A/0x14/0x1E/0x28 or mode 0x2F,
  x2 for 45 / modes 0x2E / 0x30); `eax == 0x7A` -> x2; everything else -> 0x79AB09 `cmp eax,0x11; jmp 0x409960` -> x4
  (as the research notes (levels) 3.3). So in Adventure all of 4-1..4-10 are x4
  (`dayLevels.waveBudgetMultiplier`, Plan 2), and **4-10 goes from vanilla x3 (stormy night) to x4**. The study's
  "x3 for 10/20/30" is the mode-0x8B branch.
- **Start sun, U12 resolved**: hook 30 chain (0x7981A0 -> 0x7A2385 -> 0xC00670 -> 0x95C0E0 -> 0xC12FD0 -> 0xC05CC0)
  sets sun only for levels 51..72 and mod modes (0x73, 0x7F, 0x80, 0x83, 0x8A, 0x8C, 0x92), I, Zombie (150) and
  first-time 1-1 (150); else 0xC05CC0 writes 50. 4-5 (Vasebreaker, level 35) is set to 0 by vanilla InitLevel before
  the hook. So 4-1..4-10 start with vanilla sun.
- **Waves, allowed zombies**: `gZombieWaves` 0x6A34E8 and `gZombieAllowedLevels` 0x6A35B0 are vanilla for 31..40
  (study `w4_levels.py`); hook 176 rewrites allowed lists only for 61..73, hook 20 wave counts only for modes >= 0x65.
- **4-5 Vasebreaker** (vanilla pots, `Challenge.cpp`; mod pot hooks 141/166/187 only for modes 0x7D/0x8F) and
  **4-10 conveyor** (vanilla stormy night: no fog, lightning) are vanilla plus the cross-world rules (x4 budget,
  zombie values, elites, +133 px start, final-wave re-roll).

## Levels 4-1..4-10 (checked on the Mac)

Run: `pvz-portable -pvzu-mode unnamed|vanilla -pvzu-pack <pack> -pvzu-width 1300 -pvzu-level 31..40 -pvzu-seed 7
-pvzu-autoplay 1-100000 -pvzu-log-waves <file> -pvzu-dev-fog log -pvzu-hidden -pvzu-quit-frame 7000`
(`SDL_AUDIO_DRIVER=dummy`). Wave lists (`waves`/`allowed`/`total` lines) are identical to the app build before this
task (2492410) in both modes, and vanilla logs are identical line for line; the `fog`/`fogPlay` lines below agree in both
modes except `source` (rule / engine). Budgets: sum of zombie values over all waves, seed 7, first-time Adventure.

| Level | Waves (flags) | Allowed (engine = exe 0x6A35B0; Flag on flag waves) | Start sun | Fog col | Fog | Pool final wave | Budget vanilla / Unnamed | Award (engine, vanilla) |
|---|---|---|---|---|---|---|---|---|
| 4-1 (31) | 10 (1) | Normal, Cone, Jack | 50 | 6 | yes | 2 / 3 pts | 29 / 97 | Plantern (25) |
| 4-2 (32) | 20 (2) | Normal, Cone, Football, Jack | 50 | 5 | yes | 2 / 3 | 96 / 333 | Cactus (26) |
| 4-3 (33) | 10 (1) | Normal, Cone, Balloon | 50 | 5 | yes | 3 / 5 | 28 / 97 | Blover (27) |
| 4-4 (34) | 20 (2) | Normal, Cone, Dolphin, Balloon | 50 | 5 | yes | 3 / 5 | 93 / 333 | taco (shop) (`Zombie.cpp` coin for level 34) |
| 4-5 (35) | (Vasebreaker: pots, the wave table is not used) | Normal, Cone | 0 | 5 | no (Vasebreaker stage) | - | - | Split Pea (28) |
| 4-6 (36) | 10 (1) | Normal, Cone, Digger | 50 | 5 | yes | 3 / 7 | 30 / 97 | Starfruit (29) |
| 4-7 (37) | 20 (2) | Normal, Cone, Pail, Jack, Digger | 50 | 4 | yes | 3 / 7 | 97 / 333 | Pumpkin (30) |
| 4-8 (38) | 10 (1) | Normal, Cone, Pogo | 50 | 4 | yes | 3 / 7 | 31 / 97 | Magnet-shroom (31) |
| 4-9 (39) | 20 (2) | Normal, Cone, Pail, Balloon, Pogo | 50 | 4 | yes | 3 / 7 | 96 / 333 | note (level-end fade; `Zombie.cpp` coin for 9/19/29/39/49) |
| 4-10 (40) | 20 (2) | Normal, Cone, Pail, Jack, Balloon, Digger, Pogo | 50 (conveyor) | 4 (unused) | no (stormy night) | 3 / 7 | 253 (x3) / 333 (x4) | Cabbage-pult (32, conveyor) |

- Award pairs: as world 3 (study U6 there), `GetAwardSeedForLevel` names seed 28 for 4-4 and 4-5 and seed 32 for 4-9
  and 4-10, but the drop is a taco on 34 and a note on 39, so Split Pea comes after 4-5 and Cabbage-pult after 4-10.
  The w4 study table put Cabbage-pult on 4-9 and "?" on 4-10; the engine (vanilla, no hook) is what the port keeps.
- Full fog (`fogLevels.fullFog` 1, scratch copy of this pack): 4-7 logs `leftFogColumn=0 source=rule fullFog=1`, and
  the screenshot showed fog from the lawn's left edge (columns 0..3 covered; vanilla 4-7 starts at column 4).
