# Sources: Catapult vase / bug-spray shots and the vase Catapult's volley (`data/rules-catapult-shots.json`)

Plan 9 R3. Evidence: the research notes (r3-catapult-shots) (static reads of Unnamed 1.3beta2
`PlantsVsZombies.exe` with radare2 and the research notes (tools)*`; the exe was never run). Code wins over the Almanac. App code:
`app/src/Mod/Unnamed/CatapultShots.*` (rules), `app/src/Mod/Engine/CatapultShots.*` (engine sites), feature
`catapultShots` in `mod.json`. Which catapult rolls which shot stays in `rules-world7-zombies.json` (`catapult.*`, the
vase form 0x70 and the pole head's world-7 roll). A missing key plays that rule like vanilla; with the feature off the
rolled shot stays a basketball (as before Plan 9).

## Keys

| key | Unnamed | vanilla | exe evidence |
|---|---|---|---|
| volleyRoll / volleyBelow | 100 / 35 | - | hooks 547 / 548: 0x958ec0 -> 0x910135: a not-hypnotised (+0xb8 != 1) variant-0x70 catapult at the fire event: `Rand(100) < 0x23` -> the volley instead of its one shot |
| volleyShotRoll | 3 | - | hook 537 0x7a1945: with `[0x701240] == 1` the shot type is `(Rand(3) & 1) * -0xe + 0x20` = 0x20, 0x12, 0x20 |
| volleyLastCol / volleySkipSeeds / volleySkipModSeeds | 8 / [21, 46] / [107] | - | 0x9101bc..0x910211 (+ 0x7c0800): every plant of the row (IteratePlants order), column 0..8, the first of each column, not seed 0x15 / 0x2e / 0x6b; `balls -= 1` and ZombieCatapultFire(plant) each |
| volleyMinBalls | 1 | - | 0x910217: balls < 1 -> 1 after the volley |
| ballTracksBelow | 5 | - | hook 549 0x91027a: after the loop-end ball, balls < 5 -> hide the first `abs(balls - 4) + 1` basketball tracks (vanilla hides one at == 4..1) |
| vaseDamage | 300 | 75 (basketball) | 0x7b08ce: type 0x12 -> 0x12c |
| vaseZombieRoll / vaseZombieReroll | 33 / [11, 12, 13, 14, 16, 20, 25] | - | hook 393 0x7a1426..0x7a1451 (copy in hook 382 0x7a1226): `Rand(0x21)` re-rolled on those types |
| vaseReflectedFlags | 1 | - | 0x7a140b: no vase when the shot's mDamageRangeFlags == 1 (Leaf Shield reflected) |
| sprayDamage | 100 | 75 | 0x7b090b: type 0x20 -> 0x64 |
| sprayKillRoll | 20 | - | 0x91036d: `Rand(0x14) == 0` -> damage HP + 1 |
| sprayRateStep / sprayRateCapExtra | 75 / 750 | - | 0x91038e..0x9103e5: cap = definition launch rate + 0x2ee; cap >= rate -> rate + 0x4b, else rate = cap |
| sprayFoley / sprayParticle | 71 / 88 | - | 0x910324 `mov eax, 0x47` -> PlayFoley (FOLEY_PRIZE in the vanilla order); 0x910335 `push 0x58` (PARTICLE_MIND_CONTROL) |
| sprayParticleDx / Dy / RenderOrder | 34 / 28 / 400000 | - | 0x910342..0x910351 (+0x1c on mY, +0x22 on mX), `push 0x61a80` |

Fixed in code (not keys): the vase kills every plant of the cell except a Squash in states 5..7, a squished, dead or
bungee-rising (+0x134 == 2) plant, each `Board+0x5798` (mPlantsEaten) += 1 (0x7aa380); the vase is grid item 7, state 3,
pot type 2, seed -1, sun -1, render order 302000 + row * 10000 (0x7aa450); art IMAGE_SCARY_POT cel 0 / IMAGE_BUG_SPRAY
at scale 1 (hook 405 chain 0x7a0df5 / 0x7a0e6d); both shots fly and collide as the basketball (hooks 390 / 391 / 392).

## Rulings

- The shots are basketballs with ProjectileState::modType 0x12 / 0x20 (the mod-shot carrier), so lob, umbrella and
  collision stay vanilla code; saved games keep the type.
- The exe damages plants through its routine 0x950000 (Charmed Tall-nut counting and state filters); the port subtracts
  the damage as its basketball does. Cost if wrong: a Charmed Tall-nut hit by these shots does not count them toward a
  summon.
- Foley 0x47 and particle 0x58 are read as indices into the vanilla tables (FOLEY_PRIZE, PARTICLE_MIND_CONTROL); the
  foley's pitch range is read from entry 78 in the exe (a copy slip) and its unconditional RandRangeFloat is not
  copied. Both indices are keys, so another reading is a data change.
- Nobody opens a catapult vase in a normal level except the mod's own openers (Dream Starfruit kind stars 0xc0288c,
  Vase Pole Vaulter landing hook 558, Zomboss stomps): the vase blocks its cell, as in the exe.

## Seen on the Mac (2026-11-23)

Runs: `pvz-portable -pvzu-mode unnamed -pvzu-pack <pack> -pvzu-width 1300 -pvzu-seed 7 -pvzu-dev-level 4
-pvzu-dev-player-level 65 -pvzu-force-variant CATAPULT:0x70|0x19 -pvzu-dev-plant PEASHOOTER:0,SUNFLOWER:1,WALLNUT:3,
REPEATER:4 -pvzu-dev-spawn CATAPULT -pvzu-dev-spawn-x 640 -pvzu-dev-spawn-count 5 -pvzu-dev-catapult-shot volley|spray|vase
-pvzu-log-zombies <f> -pvzu-hidden` (`SDL_AUDIO_DRIVER=dummy`):
- volley: 5 vase catapults, 4 shots each (balls 10 -> 6, loop end 5, next volley 5 -> 1); hits mixed vases and sprays;
  vases left with random zombies (e.g. 5, 17, 1), sprayed plants slowed 150 -> 225 -> 300 and one killed (1 in 20).
  Vases drawn on the lawn (question pots), the red spray particle on hit plants, the bug-spray cans in the cart.
- vase (pole head 0x19, world 7): balls 5, every shot a vase on the front-most plant (column 4).
- spray: single 0x20 shots; saved with shots in the air, Continue: they landed as bug spray.
- feature off: "(shot stays a basketball)", no catapultShots lines; vanilla mode: no world7 / catapultShots lines.
