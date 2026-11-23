# Sources for data/rules-fog-plants.json

Every key below comes from Unnamed 1.3beta2 `PlantsVsZombies.exe` code, read in
the research notes (w4-fog) (section in brackets; addresses are the exe's, hook numbers are rows of
the research notes (hook-triage)). The app's fallback for each key is the vanilla behaviour, and every rule is off while the
`fogPlants` feature is off (vanilla mode). Booleans are 0/1. App code: `app/src/Mod/Unnamed/FogPlants.*` (rules),
`app/src/Mod/Engine/FogPlantSites.*` (engine glue, dev layout), sites marked `// PVZU:` in `Plant.cpp`,
`Projectile.cpp`, `Zombie.cpp`, `Board.cpp`. The exe never checks the level in these hooks, so the rules hold on every
lawn in Unnamed mode, not only in world 4.

Table changes (already in `data/plants.json` / `data/projectiles.json`, Plan 1 tables, not repeated here): Plantern
150 / 3600, Cactus 175, Blover 150 / 1000, Split Pea 175, Starfruit 175 / 2500 / launch rate 250, Pumpkin 200 / 2400,
Magnet-shroom 125, Cattail 200, `PROJECTILE_SPIKE` and `PROJECTILE_STAR` damage 1.

Shared rules not repeated here: Sea-shroom's 39 % freeze of its eater is `nightPlants.puff.*` (one hook, 688, for Puff
and Sea; `rules-night-plants.json`); chill +10 body damage is the cross-world Night rule (X2).

## Plantern [2.2]
- `fogPlants.plantern.fogRadius` = 20: in-place patch `8d 5a fb` (`lea ebx,[edx-5]`) at 0x41a702 in
  `Board::UpdateFog`: `ClearFogAroundPlant(plant, seed - 5)` = 20 for seed 0x19 (vanilla `seed - 0x15` = 4). 20
  columns / rows cover the whole lawn; Torchwood keeps 1
- `fogPlants.plantern.speedupMinRate` = 100, `speedupDivisor` = 2, `speedupAddGatlingCattail` = 25: cave 0x651670,
  jumped to from `Plant::UpdateShooter` 0x45f8bf after `r = Rand(15)`: the first live Plantern (`+0x141 == 0`) with
  `|row - row'| <= 1` and `|col - col'| <= 1`; `rate = [+0x5c]`; `cmp rate,0x64; jl` (no bonus below 100);
  `sar rate,1`; Gloom-shroom (0x2a) and 0x7a: full rate; Cattail (0x2b) and Gatling (0x28): `rate/2 + 0x19`;
  `mLaunchCounter = rate - r`
- `fogPlants.plantern.healTickCs` = 4, `healPerTick` = 1, `maxHpDecayBelowHalf` = 1: hook 306 (0x46323e in
  `UpdateAbilities`, before `UpdateShooting`) → 0x95b840: Plantern with `[+0x54] < 1`: for every plant in its 3x3
  (itself too) 0xc06190 `if (hp < maxHp >> 1) maxHp -= 1`, 0x95b8b2 `if (hp < maxHp) hp += 1`; then `[+0x54] = 4`.
  Not in the Almanac

## Cactus [2.3]
- `fogPlants.cactus.secondVolleyAtCounter` = 25: hook 290 (0x7a8850) in `UpdateShooter`: at `mLaunchCounter == 25`
  state 0x20 (high) → `FindTargetAndFire(row, 0)`, state 0x1e (low) → `FindTargetAndFire(row, 1)`
- `fogPlants.cactus.animRate` = 45, `shootingCounter` = 23: hook 282 (0x7a88a0) in `FindTargetAndFire`: every Cactus
  shot sets the body anim rate to float 0x679680 (45.0) and `mShootingCounter = 23` (vanilla: 35 / 23 high, 35 / 35 low)
- `fogPlants.cactus.toSpikeweed` = 1: cave 0x6519c0 in `Plant::Squish`: Cactus squished by Zomboni (0xc) or Catapult
  (0x16) → `mVisible = 0`, `Board::AddPlant(col, row, SEED_SPIKEWEED)`, then the vanilla squish. Other squishers vanilla
- `fogPlants.cactus.spikePierceMax` = 64: hook 806 (0x959a50) in the `Projectile::Die` cave 0x651ce7: type 8 with
  `[+0x18] < 0x40` and caller `EBP == ESI` → `[+0x18] += 1`, not killed. The port applies it on the impact path
  (`DoImpact`) only, the one caller where the projectile is its own caller register; a spike leaving the screen dies
  as vanilla. Cattail's homing spikes are left out: their `[+0x88]` is their target, so the Die cave's first branch
  (below, Starfruit) takes their first hit and clears the target, and a homing shot without a target never hits again

## Blover [2.4]
- `fogPlants.blover.storm` = 1, `damage` = 20, `balloonChillCs` = 1000: `BlowAwayFliers` (0x4665b0) reworked through
  cave 0x651bc7 → hook 803 (0x9574d0) → 0x95b940: every zombie not dying (phase 1..3): hypnotised → nothing; Imp (0x18)
  → `mBlowingAway = 1`; `TakeDamage(20, 4 = DAMAGE_FREEZE)`; then armless (`[+0xbb] == 0`) → `mBlowingAway = 1`; phase
  0x49 (flying balloon) → `mChilledCounter = 1000`. Patch 0x466603 (`cmp eax,0x4a; jne; cmp eax,0x4a; je`) kills the
  vanilla "blow away flying balloons" store. `mFogBlownCountDown = 4000` stays vanilla (hook 342 changes it only in mod
  mode 0x7c). Almanac "60 damage, lane pushed back 200" not found in code (study U4): code wins

## Split Pea [2.5]
- `fogPlants.splitPea.fireFront` = 1: hook 352 (0x7978xx chance block): seed 0x1c: `type = (proj.mX < plant.mX)` →
  back shots are snow peas (type 1), front shots `ConvertToFireball`
- `fogPlants.splitPea.sweepRoll` = 10: hook 326 (0xc11ba0) at the front fire in `UpdateShooting`: idle (`[+0xEC] ==
  -1`) → `[+0xEC] += (Rand(10) == 0)` → 0 = sweeping
- `fogPlants.splitPea.sweepFallAbove` = 96, `sweepRiseBelow` = 31, `sweepSteps` = 6: hook 314 (0xc11b00), each tick
  while sweeping: `[+0xEC]++`, `[+0xE0]++`; `> 0x60 → [+0xE4] = 1`; `< 0x1f → [+0xE4] = 0`; `[+0xE4] == 1 → [+0xE0] -= 2`;
  `[+0xE8]++`, `== 6 → 0`
- `fogPlants.splitPea.sweepLaunchCounter` = 30, `sweepFireStep` = 3: hook 325 (0xc11940) in `UpdateShooting`: while
  sweeping `mLaunchCounter = 0x1e`; `[+0xE8] == 3` → the Split Pea fire block (a front shot every 6 cs)
- `fogPlants.splitPea.sweepDurationCs` = 500: hook 278 (0xc11990) in `FindTargetAndFire`: `499 < [+0xEC] → -1`
- `fogPlants.splitPea.sweepPhase` = -31.4, `sweepDiv` = 20, `sweepSpeedDiv` = 0.15, `sweepMotion` = 7,
  `sweepRangeFlags` = 1: hook 354 (0xc11a70) in `Plant::Fire`, front head only: `[p+0x58] = 7`, `[p+0x74] = 1`,
  `vx = sin((f[0xc11ad3] - angle) / f[0xc11ad7]) / f[0xc11adb]`, `vy = cos(...) / ...` (floats -31.4, 20, 0.15)
- `fogPlants.splitPea.sweepOnPlant` = 1 (V2, replaces the U6 "starts idle" ruling): `PlantInitialize` memsets Plant+0xC8..
  (0x45dc1c..0x45dcb4) so +0xEC = 0 and hook 314 sweeps at once (1.3beta1 "[quote not included]"); only the sweep end
  0xc119bc writes -1. Missing key = starts idle.
- Port ruling (the sweep end): the sweep ends at its first front shot
  with the timer at 500 or more (the exe's FindTargetAndFire check, reached by the port's sweep shot)

## Starfruit [2.6]
- `fogPlants.starfruit.starSpeedMult` = 1.5: hook 286 (0x95b090): each of the five stars with `[+0x80] == 0`
  (every Starfruit star): `vx *= 1.5`, `vy *= 1.5`
- Plan 9 R1 (study the research notes (r1-starfruit), all H): hook 286 also sets `[+0x88] = 0x114` (276) on those
  stars. 276 is a curve tag, not a hit counter (the Die cave 0x651ce7 that clears `[+0x88]` runs for motion 0 / 6 only,
  0x956010; stars are motion 7).
- `fogPlants.starfruit.returnAt` = 40, `returnAgainAt` = 120: Projectile::Update (hook 400 → 0x79f067 → 0x95b170, after
  age++): a type-7, motion-7 star with `[+0x80] == 0`, `[+0x84]` not 1 / 2 and `[+0x88] == 276` negates vx and vy at
  age 40 and at age 120 (0x95b1ab..0x95b1d4): Almanac "turns back after a while, and again after double the time".
- `fogPlants.starfruit.extraStarsRoll` = 3, `extraStars` = 4: hook 287 (0x95b0d0 → 0x95b790 → 0x95b0e2): raw seed 0x1d
  only; `Rand(3) == 0` → four stars at (x + 25, y + 25), render order + 1, the plant's row, motion 7, velocity 0, damage
  flags of the primary weapon, `[+0x88] = 0..3` (0x95b0ee..0x95b159). Not x1.5.
- `fogPlants.starfruit.spiralSpeed` = 0.03, `spiralTurn` = 0.05, `spiralMaxTag` = 4: same filters as the boomerang, `0 <=
  [+0x88] <= 4`: `theta = age * 0.05 + ([+0x88] - 1) * pi / 2`, `vx = cos(theta) * age * 0.03`, `vy = sin(theta) * age *
  0.03` (0x95b1d9..0x95b232; floats 0x3d4ccccd, 0x3cf5c28f): four outward spirals 90 degrees apart, ~0.6 px per cs.
- The curve is skipped in mode 0x89, mode 0x8b and Adventure level 65 (0x95b700..0x95b73c).
- `fogPlants.starfruit.pierceLimit` = 255: Projectile::Die (0x46eb2b → 0x6511d9 → 0x651cdd → 0x956010 → 0x651d03 →
  0x959a50 → 0x959f30 → 0x959fac → 0x959a7a → 0x651d0d → 0x6511e3): a type-7 star with kind <= 0, 1 or > 5:
  `cmp dword [+0x18],0xff; jge die; cmp ebp,esi; jne die; inc` → lives. The dword starts at 1 (0x41dfde mVisible = 1),
  so 254 lives. EBP == the projectile for every Die made inside Projectile::CheckForCollision: its impact (DoImpact
  tail-jumps to Die with EBP restored) and its field-edge kills (0x46d047 `mov eax,ebp; call Die`). So stars pierce and
  also fly on past the lawn edges until the counter runs out. Port: an RAII scope in CheckForCollision, test in Die.
- Ruling: only stars the port tags curve (the five stars, the four extra stars); in the exe any type-7 kind-0 star with
  `[+0x88] == 0` would spiral, but no other such star exists in the port (Dream stars have a kind, Shrapnel stars
  `[+0x84]` 1 / 2, snake stars are in the skipped modes) — cost if wrong: an unknown kind-0 star flies straight.
- Ruling: the curve and pierce are gated by `fogPlants` (the exe has no gate) — cost if wrong: none in the Unnamed pack.

## Pumpkin [2.7]
- `fogPlants.pumpkin.explodeAtHp` = 72: cave 0x6513b6 in the per-bite block (cave 0x6512a0 from `EatPlant` 0x52fcdc):
  bitten Pumpkin with `HP <= 0x48` → seed = 2 (Cherry Bomb), `mDoSpecialCountdown = 1`, `mStateCountdown = 1` → explodes
  on its next update (1800 in radius, hook 155)
- `fogPlants.pumpkin.explodesWhenSmashed` = 1: cave 0x6519fd in `Plant::Squish`: Pumpkin squished by Gargantuar
  (0x17), Giga (0x20) or Squash-head zombie (0x1e) → seed = 2, then hook 800 (0xc10750) HP = -1, `DoSpecial`, `[+0x54] =
  1`. Vehicles: vanilla squish

## Magnet-shroom [2.8]
- `fogPlants.magnet.allRows` = 1: patch 0x4620a2 `lea edx,[esi+2]; cmp edx,4; jo` (vanilla `ja`: skip |row diff| > 2)
- `fogPlants.magnet.unlimitedRadius` = 1: patch 0x462124 after `GetCircleRectOverlap(270 / 320)`: `test al,al; jo`
  (vanilla `je`). The `x <= 800` test (0x46208e) stays

## Cattail [2.9]
- `fogPlants.cattail.cobRoll` = 100, `cobBelow` = 3: hook 352: seed 0x2b, `Rand(100) < 3` → `[proj+0x5c] = 0xb`
  (PROJECTILE_COBBIG) with Cattail's homing motion kept. It hits one zombie for the Cob's table damage (no ash: the
  homing collision calls `DoImpact`, not the Cob Cannon's radius kill). Damage cap code for this Cob not settled (U7)

## English (`strings/en-corrections-fog-plants.txt`)
Code wins over the Almanac text: Plantern also heals its 3x3; Blover deals 20 slowing damage to all and blows Imps and
one-armed zombies off the lawn, balloons only slowed (no 60 damage, no 200 push-back); Split Pea's 10 % sweep.
