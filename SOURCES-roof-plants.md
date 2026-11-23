# Sources for data/rules-roof-plants.json

Every key below comes from Unnamed 1.3beta2 `PlantsVsZombies.exe` code, read in
the research notes (w5-roof) (section in brackets; addresses are the exe's, hook numbers are rows of
the research notes (hook-triage)). For this port the caves were read again statically with radare2 (`pd`, nothing run); where
that reading added to or corrected the study it says so below. The app's fallback for each key is the vanilla
behaviour, and every rule is off while the `roofPlants` feature is off (vanilla mode). Booleans are 0/1. App code:
`app/src/Mod/Unnamed/RoofPlants.*` (rules), `app/src/Mod/Engine/RoofPlantSites.*` (engine glue, dev layout), sites
marked `// PVZU:` in `Plant.cpp`, `Projectile.cpp`, `Zombie.cpp`, `Board.cpp`. The exe never checks the world in these
hooks (only the Cabbage-pult checks level 55), so the rules hold on every lawn in Unnamed mode, not only on the roof.

Table changes (already in `data/plants.json`, Plan 1 tables, not repeated here, G8): Flower Pot recharge 500; Garlic
100 / 1200; Marigold 150 / 6000; Melon-pult and Winter Melon launch rate 225. Coffee Bean: no change [1.4].

## Cabbage-pult [1.1]
- `roofPlants.cabbage.quickThrowRoll` = 2: hook 352 → 0xc05660 in `Plant::Fire`, after the projectile is made: seed
  0x20, `Rand(2)`, `test eax,eax; jne skip` → P = 1/2
- `quickThrowFreeLevel` = 55: 0xc10780 `cmp [board+0x5550],0x37; je` → on level 55 only the projectile part
- `quickThrowFlashCs` = 100, `quickThrowLaunch` = 50, `quickThrowHpCost` = 50: 0xc0567a `[+0xbc] = 0x64`
  (mBeghouledFlashCountdown), `[+0x58] = 0x32` (mLaunchCounter), `[+0x40] -= 0x32` (HP). The engine's `Plant::Update`
  kills a plant once HP < 0, so a Cabbage-pult at 0 HP dies at its next quick throw (seen on the Mac: 0 → -50)
- `bigVelZ` = -7.0, `bigAccZ` = 0.1: 0xc0568f `[proj+0x80] = 1`, `[proj+0x44] = 0xc0e00000` (-7.0),
  `[proj+0x48] = 0x3dcccccd` (0.1)
- `bigDamage` = 400 (**new, not in the study**): `Projectile::DoImpact` hook 397 → 0xc10bf0 → 0xc05700: type 2
  (cabbage) with `[+0x80] == 1` → the damage pushed for `TakeDamage` is 0x190 = 400 (table 40)
- `bigDrawScale` = 3.0 (**new**): `Projectile::Draw` hook 408 → 0xc056c0: type 2 with `[+0x80] == 1` draws
  `IMAGE_REANIM_CABBAGEPULT_CABBAGE` at scale 0x40400000 = 3.0. So the "quick throw" is a big cabbage: 400 damage, x3
- The Almanac's "raise fire rate, P = 1 - n/100, max +50%" ramp is dead code (study 1.1)

## Kernel-pult [1.3]
- `roofPlants.kernel.cobAfterKernels` = 15: hook 352 0x797643 (after the projectile is made): `[plant+0xc8] == 0xf` →
  `[proj+0x5c] = 0xb` (COBBIG); else a kernel (type 0xa) → counter + 1; butter or Cob → 0x95a780
  `[proj+0x88] = counter`, counter = 0. The 16th throw after 15 kernels is a Cob, whatever was rolled; the Cob is the
  vanilla Cob impact (1800 ash in a radius)
- `butterBaseCs` = 100, `butterMinCs` = 400, `butterFlatCs` = 500, `butterStacks` = 1, `butterFixedMode` = 70: hook 720
  (0x95a700) in `Zombie::ApplyButter`: Newspaper (5) with phase **!= 0x1f** (not mad: reading / maddening) or Catapult
  (0x16) with balls left (`[+0x114] != 0`) → `[+0xb0] = 500` (set). Else, unless game mode 0x46 (70, I, Zombie
  Endless) or no projectile (`EDI < 1000000`): `edx = 1; do { edx *= 2; n--; } while (n > 0)` with n = `[proj+0x88]`,
  T = edx × 100 = 100 × 2^max(n, 1), at least 400; then `[+0xb0] += T` (stacks). Note: the Night rule
  `nightZombies.newspaper.madButterCs` reads this hook as "mad → 500"; the asm (`cmp [esi+0x28],0x1f; jnz → 500`)
  says the opposite. With `roofPlants` on, this rule decides the whole hook
- Butter choice itself stays vanilla `Rand(4) == 0` (study 1.3)

## Garlic [1.5]
- `roofPlants.garlic.hp` = 900: PlantInitialize rewrite (triage row 267)
- `poisonPeriodCs` = 40, `poisonDamage` = 1, `poisonRangePx` = 120, `poisonBossMinCol` = 6: hook 618 → 0x7953c3 in
  `Zombie::Update`, before `mZombieAge++`: on board (0x52ae40) and `age % 40 == 0`; for every plant not squished
  (`+0x142`) of seed 0x24: 0xc02680 Boss → `garlic col >= 6`, else 0x794320 `|row diff| <= 1` and
  `garlic.mX - 120 <= zombie.mX <= garlic.mX + 120`; then `EffectedByDamage(9)` → `TakeDamage(1, 1)` (bit 0 bypasses
  the held shield; helmets still take it). Several Garlics stack
- `biteChillCs` = 250, `biteChillCap` = 400, `hypnoRoll` = 250: cave 0x651374 in the per-bite block (cave 0x6512a0
  from `EatPlant`): bitten seed 0x24 → `chill <= 400` (jg skip) → `chill += 250`; then not Flag (1) / Newspaper (5):
  `Rand(250)`, `cmp eax,0; jg skip` → `[+0xb8] = 1`. P = 1/250 per bite tick (the Almanac's 1.1952 % =
  1 - (1 - 1/250)^3). The port hypnotises with `Zombie::StartMindControlled` (the engine setter)

## Umbrella Leaf [1.6]
- The RV block (hook 731 → 0xc02b20 at the Zomboss RV landing: the first seed 0x25 plant, not squished, not rising
  with a bungee, not dead, in rows `[mTargetRow - 2, mTargetRow + 3]` and columns `[mTargetCol - 2, mTargetCol + 4]`
  takes 100 and bounces; the crush is skipped) has one copy: the Zomboss keys `boss.umbrellaRv*` (SOURCES-zomboss.md,
  B6). The `roofPlants.umbrella.*` keys of the same numbers were removed with their uncalled helper.

## Marigold [1.7]
- `roofPlants.marigold.shrink` = 1: patch 0x45fafa in `UpdateProductionPlant`: the Marigold branch jumps to cave
  0x6517b2 instead of `AddCoin` (no more coins)
- `maxTargetHp` = 120000: 0x7aa320 skips max body HP (`+0xcc`) > 0x1d4c0 and the Boss (0x19); 0x7aa130 skips the
  Newspaper (5) variant 0x7f; the cave skips dead (`+0xec`) and hypnotised (`+0xb8`); 0xc011f0 repeats the HP test
- `rangeFrontPx` = 80, `rangeBackPx` = 120: 0xc01200 `x = marigold.mX + 0x50`, 0x6517fc `+ marigold.w`
  (`zombie.mX <= x`), 0x651808 `x - 200 - marigold.w - zombie[+0x94]` (mZombieRect width) `<= zombie.mX`: so
  `zombie.mX` in `[mX - 120 - zombieRectW, mX + 80 + marigoldW]`; rows `|diff| <= 1`
- `shrinkScale` = 0.5, `shrinkHpDivisor` = 4, `chillAdd` = 1: `[+0x11c] *= [0x6793c0]`; `cdq; and edx,3; add; sar 2`
  (divide by 4 toward 0) on `+0xc8 +0xcc +0xd0 +0xd4 +0xdc +0xe0 +0xe4` (body, helm, shield and their max, flying HP;
  **the flying max `+0xe8` is not divided**, a correction to the study); `[+0xac] += 1`. No "already shrunk" guard
- Then particle 60 (`PARTICLE_GLOOMCLOUD`) at the Marigold's centre with image `IMAGE_REANIM_COIN_GOLD_DOLLAR` and
  colour (150, 100, 200, 255) (0x518a70, 0x518600, 0x518560), and `Plant::Die` (0x651970)
- `biteImmune` = 1: hook 680 adds Marigold to the `EatPlant` "instant plant" list: chewed while awake, no damage
- First pulse: the vanilla production timer (Marigold launch rate 2500); the initial counter is vanilla (study U4)

## Melon-pult / Winter Melon [1.8]
- `roofPlants.melon.volleyBasePct` = 10, `volleyWinterPct` = 10, `volleyPerZombiePct` = 4, `volleyAlwaysAt` = 100:
  hook 329 → 0x79751e in `UpdateShooting`: after `Fire(target)` (no target → nothing), seed 0x27 / 0x2c:
  `4n` with n = Board `+0xa0` (zombies on the board); `4n >= 100` → always (no roll); else `Rand(100) <= 9 +
  2 (seed - 0x27) + 4n` → fire. Then for every zombie except the target: not dead, not hypnotised, same row,
  `mX > plant.mX`, not Boss (0x19), phase not 0x49 / 0x4a (balloon flying / popping), 0x20 / 0x22 (digger tunnelling /
  paused), 0x47 (Imp being thrown), 1 / 2 / 3 (dying / burned / mowered) → `Plant::Fire(zombie, row, weapon)`.
  The Almanac's 9 % / 17 % is wrong (code: 10 % / 20 % + 4 % per zombie)

## Flower Pot [1.2]
- `roofPlants.flowerPot.zombieShotsSkip` = 1: hook 374 → 0xc02c30 in `FindCollisionTargetPlant`, for shots with
  `[+0x74] == 0` (basketballs, zombie peas): skip a Scaredy-shroom in state 0x15 (hiding), Starfruit (0x1d), Flower
  Pot (0x21) (and mod seeds 0x58 / 0x59 / 0x6d, which this port does not have). A basketball aimed at an empty pot
  passes over it and lands on the roof
- `noGraveOnPot` = 1: hook 18 → 0xc113c0 at the end of `CanAddGraveStoneAt`: `GetFlowerPotAt` (0x40d220) → refuse.
  The Pole Vaulter's vault grave does not ask `CanAddGraveStoneAt` (study day/levels.md), so on the roof this only
  matters to graves placed by level code

## English (`strings/en-corrections-roof-plants.txt`)
Code wins over the Almanac text: Cabbage-pult's 1/2 big quick throw (no fire-rate ramp); Garlic's hypnosis 0.4 % per
bite; Marigold's single pulse and death, no coins; Melon / Winter Melon 10 % / 20 % + 4 % per zombie on the lawn;
Umbrella Leaf blocks Dr. Zomboss's RV.
