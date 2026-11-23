# Sources: Pool levels (rules-pool-levels.json, feature `poolLevels`)

Plan 4 Task 3. Study (source of truth): the research notes (w3-pool) sections "Pool rules" and "Levels 3-1..3-10".
Exe = the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only (study exports, and static r2
disassembly through the research notes (w2_r2); nothing run). Code: `app/src/Mod/Unnamed/PoolLevels.*` (pure rules),
`app/src/Mod/Engine/PoolLevels.*` (engine side), tests `app/tests/test_pool_levels.cpp`.

| Keys | Value | Evidence | Conf |
|---|---|---|---|
| `poolLevels.poolSpawn.<21..30>.count` / `.points` | 3-1, 3-2: 2 / 3; 3-3..3-5: 3 / 5; 3-6..3-10: 3 / 7 | `Board::SpawnZombiesFromPool` 0x4128F0..0x41296C: `cmp [ebx+0x5550]` against 0x15/0x16/0x1F/0x20 -> `[esp+0x10]=2, ebp=3`; 0x17..0x19/0x21..0x23 -> 3 / 5; else 3 / 7. Identical to PvZ-Portable (`Board.cpp` SpawnZombiesFromPool): the table is data so it can be modded, not a change. Fog levels (31..35) are left to the Fog plan. | H |
| `poolLevels.finalWave.gravesAfterPool` | 1 | Hook 86 at 0x412CF5 (`SpawnZombiesFromGraves` 0x412CE0) -> 0x9588A0 -> 0xC05580 -> 0x9588A7: background 2/3 -> `push edi; call 0x4128F0` (pool spawn), background 4/5 -> 0x412C30 (sky), then `jmp 0x412D24` = the grave loop (IterateGridItems, type 1, counter >= 100). Vanilla 1051 returned after the pool spawn (0x412DC9 `call 0x4128F0; ...; ret`), and so does PvZ-Portable. So graves on a pool lawn (Pole Vaulter vault graves, `dayLevels.poleGrave`) also raise zombies on the final wave, with the hook-88 re-roll. | H (flow read; not seen in game) |
| `poolLevels.poolSpawn.passesHypnosis` / `.hypnoRollRange` | 1 / 3 | Hook 81 at 0x412A4D (after `AddZombieInRow` 0x40DDC0 in the pool spawn) -> 0x959790: `cmp [esp+0xbc],1; jnz; mov byte [ebx+0xb8],1; mov eax,3; call 0x5AF400 (Rand)`, then the replaced `call 0x531C90` (RiseFromGrave). `[esp+0xbc]` there is SpawnZombiesFromGraves' stack argument (frame: 0x80 locals + 4 pushes in the pool function, return, board; 0x10 locals + ebx/esi + ebp + return in the grave function). The only caller that pushes it is the Death Carnival (0x959750: `movzx ecx, byte [ebx+0xB8]; push ecx; call 0x412CE0`, the Dancer's mMindControlled). Resolves study U5. The grave-loop twin is 0x959770 `cmp [esp+0x20],1` (Night port `GraveRiseRisen`). | H (asm), M (stack offset of the argument) |
| `poolLevels.iceTrail.timerBelowX` | 933 | `Zombie::UpdateZamboni` 0x52A7B0, in-place edit at 0x52A8A2 `cmp eax,0x3a5; jge` (vanilla 800) before `mov [board+row*4+0x624], 0xBB8` (mIceTimer = 3000). Matches the +133 px start (`dayZombies.startOffsetPx`, hook 480); unconditional in the exe. The Zomboni itself still starts at 800 + Rand(10) (its ZombieInitialize case sets mPosX after hook 480's +133), so in Unnamed its ice timer starts at once (Mac: tick 1 after spawn at x 801, vanilla at x 681). | H (value), M (Zomboni start in the exe not re-read) |

Levels 3-1..3-10 (no other keys; vanilla engine or already built):

Checked on the Mac (`-pvzu-level 21..30 -pvzu-seed 7 -pvzu-log-waves`, both modes): waves, flags, allowed list and
start sun below are what the engine uses; Unnamed and vanilla agree on all of them.

| Level | Waves (flags) | Allowed (exe 0x6A35B0 = PvZ-Portable; Flag on flag waves, Ducky Tube in pool rows) | Pool final wave | Start sun | Award (engine, vanilla) |
|---|---|---|---|---|---|
| 3-1 (21) | 10 (1) | Normal, Cone | 2 zombies | 50 | Squash |
| 3-2 (22) | 20 (2) | Normal, Cone, Bucket, Newspaper, Football | 2 | 50 | Threepeater |
| 3-3 (23) | 20 (2) | Normal, Cone, Snorkel | 3 | 50 | Tangle Kelp |
| 3-4 (24) | 30 (3) | Normal, Cone, Pole, Bucket, Newspaper, Snorkel | 3 | 50 | car keys (shop) (`Zombie.cpp` coin for level 24) |
| 3-5 (25) | 20 (2) | Normal, Cone, Football, Snorkel | 3 | 50 | Jalapeño (Big Trouble Little Zombie, vanilla) |
| 3-6 (26) | 20 (2) | Normal, Cone, Zomboni, Bobsled | 3 | 50 | Spikeweed |
| 3-7 (27) | 30 (3) | Normal, Cone, Bucket, Snorkel, Zomboni, Bobsled | 3 | 50 | Torchwood |
| 3-8 (28) | 20 (2) | Normal, Cone, Dolphin | 3 | 50 | Tall-nut |
| 3-9 (29) | 30 (3) | Normal, Cone, Pole, Bucket, Zomboni, Bobsled, Dolphin | 3 | 50 | note (level-end fade) |
| 3-10 (30) | 30 (3) | Normal, Cone, Bucket, Snorkel, Zomboni, Bobsled, Dolphin | 3 | 50 | Sea-shroom (conveyor) |

- Waves and allowed lists: `gZombieWaves` 0x6A34E8 and `gZombieAllowedLevels` 0x6A35B0 are byte-identical to
  PvZ-Portable for 21..30 (the research notes (w3_level_tables)); no `.NewSec` code compares the level with 21..30
  (study, M). Budgets: Plan 2 x4 (`dayLevels.waveBudgetMultiplier`, hook 22) on every adventure level, 3-5 and 3-10
  included (ledger ruling for 2-10). Zombie values/weights (Zomboni 5/1000 etc.): `data/zombies.json`.
- Award pairs (study U6): `LawnApp::GetAwardSeedForLevel` names seed 20 for 3-4 and 3-5 and seed 24 for 3-9 and
  3-10, but the drop in `Zombie::DropLoot` is car keys on 24 and a note on 29, so the seeds come after 3-5 and 3-10
  (video agrees). Vanilla engine, nothing ported.
- Not ported here: hook 316 (plant with HP below 0 dies at the start of Plant::Update) belongs with the Tall-nut
  rule (Pool plants task); the War and Peas branch of hook 86 (modes 16/32 skip pool/sky but still run the grave
  loop in the exe) is a minigame rule (later plan).
