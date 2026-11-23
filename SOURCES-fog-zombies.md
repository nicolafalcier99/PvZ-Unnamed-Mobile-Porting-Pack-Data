# Sources: Fog zombies and elite forms (`data/rules-fog-zombies.json`)

Plan 5 Task 2. Evidence: the research notes (w4-fog) sections 0 (X1, X3), 3.1-3.4, 6, 7, 8 and 9
(read-only reads of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe was never run). Code wins over the Almanac and the
video. App code: `app/src/Mod/Unnamed/FogZombies.*` (rules), `app/src/Mod/Engine/FogEliteZombies.*` (engine sites),
feature `fogZombies` in `mod.json`. A missing key plays that rule like vanilla (value in the "vanilla" column).

Zombie fields: +0x134 = `ZombieState.variant` (Jack ice head 0xE, potato head 0xF, Digger screwdriver 0x10, Pogo
chocolate 0x11, garlic 0x12, Balloon cloud 0x2B). Digger +0x14C (screwdriver surfacing x 80/160/240) =
`ZombieState.subVariant` (the same exe field the Night forms use; saved since Plan 3). Invisible garlic Pogo = the
vanilla `GameObject::mVisible` (saved). Board: the ice-head freeze (exe globals 0x800100 flag, 0x800104 counter) =
new `pvzu::unnamed::BoardState`, saved as its own chunk "PVZB" only while a freeze runs.

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| fogZombies.jack.bodyHp | 870 | 500 | 3.1 | in-place patch 0x522fc1 |
| fogZombies.jack.eliteRoll / eliteCount | 8 / 2 | no roll | 3.1 | hook 500 0x796a47: `r = Rand(8)`, `r < 2` -> 0xE + r; not in Vasebreaker; ignores the elite option |
| fogZombies.jack.iceFreezeCsPerPlant | 350 | - | 3.1 | 0x796aff..0x796b46: flag 0x800100 = 1, counter 0x800104 = 350 x Board.mPlants.mSize; hook 315 (Plant::Update -> 0x796045) one tick off per plant update, plant skipped while > 0 |
| fogZombies.jack.potatoPackets | 9 | - | 3.1 | 0x7a6571 -> 0x796ac1 -> 0x7a8530: packets 0..8 `mRefreshTime = GetRefreshTime`, `mActive = 0`, `mRefreshing = 1` (not in I, Zombie) |
| fogZombies.balloon.flyingHp | 50 | 20 | 3.2 | patch 0x5234b9 |
| fogZombies.balloon.flyVx | 0.45 | 0.23..0.37 | 3.2 | hook 521 0x797c79 (float 0x67963c): non-cloud Balloon not in phase 0x4B |
| fogZombies.balloon.ignoreMowers | 1 | 0 | 3.2 | LawnMower loop .text 0x458832 -> cave 0x651615: Balloon with mFlyingHealth != 0 skipped |
| fogZombies.balloon.eatWhileFlying | 1 | 0 | 3.2 | patch 0x52f63e (`90 90` after `call 0x534680` IsFlying); hook 676 0x959420 no-eat list (fixed in code, below) |
| fogZombies.balloon.cloudRoll / cloudHit | 7 / 3 | no roll | 3.2 | hook 503 0x7a6291: `Rand(7) == 3` -> 0x2B, not in I, Zombie |
| fogZombies.balloon.cloudBodyHp | 190 | 270 | 3.2 | hook 503 (Almanac 240 = 190 + 50) |
| fogZombies.balloon.cloudNeverPops | 1 | 0 | 3.2 | hook 551 0x7a6340: cloud in phase 0x49 -> no pop, no pool death, only mZombieHeight = FALLING |
| fogZombies.digger.helmHp | 370 | 100 | 3.3 | patch 0x522be9 |
| fogZombies.digger.eatsUnderground | 1 | 0 | 3.3 | hook 654 0x795787 (list fixed in code, below) |
| fogZombies.digger.eliteRoll / eliteBelow | 5 / 2 | no roll | 3.3 | hook 490 0x797461: `Rand(5) < 2` -> 0x10, not in I, Zombie |
| fogZombies.digger.surfaceRoll / surfaceStepPx | 3 / 80 | - | 3.3 | hook 490: +0x14C = (Rand(3) + 1) x 80 |
| fogZombies.digger.surfaceBasePx | 10 | 10 | 3.3 | hook 585 0x7974d7 (float 10.0): `mPosX < +0x14C + 10`; hook 586: the elite rises in phase 0x23 (RISE_WITHOUT_AXE) |
| fogZombies.pogo.eliteRoll / eliteRollAllElite | 5 / 2 | no roll | 3.4 | hook 501 0x796c05: option 0x800258 == 1 none, == 2 Rand(2), else Rand(5); r 0 chocolate, 1 garlic |
| fogZombies.pogo.chocolateHpDelta | -200 | - | 3.4 | hook 501 |
| fogZombies.pogo.garlicInvisibleRoll | 4 | - | 3.4 | hook 501: `mVisible = (Rand(4) != 0)` |
| fogZombies.pogo.noWindup | 1 | 0 | 3.4 | patch 0x5256eb (`jne` -> `jo`) + hook 533 0x959960 / 0x796c9e: target in reach (plant, or opposite-side zombie via FindZombieTarget 0x52e840) -> FORWARD_BOUNCE_2 at once, vx = (abs dx + 60) / 80 |
| fogZombies.pogo.chocolateBounceDx | 36 | - | 3.4 | 0x796cef, 0x959a06: chocolate always forward-bounces, vx = 96 / 80 = 1.2 |
| fogZombies.pogo.yuckyCounter | 100 | - | 3.4 | 0x959960 / 0x796cbd: garlic sets mYuckyFace = 1, mYuckyFaceCounter = 100 at every bounce end |
| fogZombies.pogo.landOnZombies / landFirstDamage / landOtherDamage | 1 / 1800 / 200 | - | 3.4 | hook 531 0x959840 (FORWARD_BOUNCE_2 at counter 70) |
| fogZombies.pogo.chocolateDamageMul | 1.6667 | - | 3.4 | hook 531: 3000 / 333 |
| fogZombies.pogo.landRectGrowPx | 32 | - | 3.4 | hook 531: attack rect x -32, width +32 |
| fogZombies.pogo.bonkGiantNuts | 1 | 0 | 3.4 | hook 532 0x959b60: Giant Wall-nut and Tall-nut+80 (103) bonk as the Tall-nut |

Wave values and pick weights (Jack 2 / 1500, Pogo 2) were already in `data/zombies.json`. The +133 px start offset
skips Jack-in-the-Box since Plan 2 (`DayZombies` StartOffsetPx, X3; the off-switch flag 0x80027c has no writer and is
not ported).

Fixed in code (not rules): the flying Balloon's no-eat list (Wall-nut, Potato Mine, Tall-nut, Pumpkin, Explode-o-nut,
Giant Wall-nut, Garlic, the mod's Tall-nut+80 103; the mod's seed 0x53 does not exist in the port); the tunneling
Digger's bite list (Lily Pad, Flower Pot, Wall-nut, Tall-nut, Pumpkin, Chomper, Torchwood, Cactus, Spikeweed, Spikerock;
the unarmed Potato Mine as vanilla; everything else refused); the Jack outcomes by form (ice head: no kill, plant
freeze, PARTICLE_ICE_TRAP, shake (4, -6), DieNoLoot, ScaryPotterJackExplode in Vasebreaker; potato head: the packets;
hypnotised ice head: Plant::IceZombies on every zombie; hypnotised potato head: `mRefreshTime = 0` for packets 0..8;
potato head in I, Zombie: vanilla blast).

Art (study 8; every file is an engine resource, so the asset overlay serves Unnamed's file of the same name):
ice / potato head = `anim_head1` -> IMAGE_BLANK, `anim_hair` / `anim_head2` hidden, REANIM_ICESHROOM (28) /
REANIM_POTATOMINE (23) playing `anim_head_idle` (string 0x668c34) at 15 attached to `anim_head1` with helper
0x794800's transform (65, -5, 0.2 rad, -1, 1); neither plant reanim has that track and FindTrackIndex (0x472f30)
returns 0 on a miss, so the ice head plays track 0 `anim_idle` and the potato head track 0 `anim_armed` (the risen
mine; Plan 9 L1, the research notes (l1-jack-pogo-looks)); cloud = `Zombie_balloon_top` -> IMAGE_ZOMBIE_BOSS_ICEBALL_PARTICLES
(`particles/Zombie_boss_iceball_particles.png`, cel 0); screwdriver = `Zombie_digger_pickaxe` -> IMAGE_ZOMBOSS_PARTICLES
(`particles/Zomboss_particles.png`, cel 0); chocolate = `anim_head1` -> IMAGE_CHOCOLATE (`images/Chocolate`, Unnamed's
`assets/images/chocolate.png` through the overlay), `anim_head2` hidden; garlic = `anim_head1` ->
IMAGE_REANIM_GARLIC_BODY3 (`reanim/Garlic_body3.png`), `anim_head2` hidden. An invisible garlic Pogo keeps its shadow.

Rulings and open points (see also study 9):
- The freeze lives on the Board (exe: process globals), so it ends with its level and is saved with the game.
- A seed slot with no packet is skipped by the potato head (the exe would read the refresh table at -1).
- Pogo landing (hook 531) hits opposite-side zombies in the same row that are not flying or bungee-dropped (the
  cave's own filters were not read in full); any hit plays the bonk and the pogo loses its stick.
- The cloud's `RandRange(0.23, 0.30)` into the body reanim's +0x34 (U8) is drawn from the RNG and dropped. The cloud's
  first speed is the 0.45 of hook 521 (the speed is picked before the form roll, as in the exe's ZombieInitialize).
- The global elite option 0x800258 is fixed at 0 (default), as for Day, Night and Pool; only the Pogo reads it.
- Potato head look (fixed in Plan 9 L1): it used to play `anim_idle`, only frame 0 of PotatoMine.reanim (the buried
  mound), so no head was seen; it now plays the exe's `anim_head_idle`, which falls back to track 0 `anim_armed`.
  The garlic Pogo's lane change runs the vanilla yucky-face path (StartWalkAnim(20) at counter 170, exe 0x52b6a0 ->
  0x52f2e0, no hook covers Pogo phases), so it bounces on with `anim_walk` and no stick: the exe and the Sub Chub
  video (4-8, 37:13-37:30) agree, kept as is. The invisible garlic Pogo's shadow path is in place but its shadow
  was not seen on the night lawn.
- Not ported: Jack world-7 rule (hook 707), potato head "+7.5 s to cooling packets" (Almanac only, U15), the digger's
  bite animation while tunneling (U14, vanilla: none).
