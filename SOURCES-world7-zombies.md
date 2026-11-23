# Sources: world-7 zombies and the ZomBotany zombies in Unnamed (`data/rules-world7-zombies.json`)

Plan 7 Task 2. Evidence: the research notes (w6-w7-and-new-content) sections 2.4, 4, 4.1, 7 item 4
and 8 items 5-9 (read-only reads of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe was never run). For this task the
hooks were re-read with the research notes (w67_fn) (Ghidra export) and radare2 `pd` / `pf` (static disassembly, nothing
run): 9, 10, 91, 268, 489 (0x9dd310..0x9dd489, 0xc046f0, 0xc123d0, 0xc123e2, 0xc12af0, 0xc11df0, 0xc12bc0), 498
(0x796e09, 0x910000), 507-511 and the in-place bytes around them (0x523930..0x523acc), 537 (0x7a1940), 549, 565, 571,
572 (0xc03ed0), 573, 575 / 576 (0x795c91, 0x795ce6, 0x795d88, 0xc12e80), 577-584, 627-629, 640 (0xc12caa), 663
(0xc12560), 672 (0xc02170), 700 / 701 (0xc126c0, 0xc12700), 707 (0x7a0a70, TakeDamage 0x5317c0..0x53187b), and the
world-7 gate 0x7aa4c0 / boss-level test 0x7aa100. Image globals were named with the research notes (dayzombies_resmap).
Code wins over the Almanac and the video. App code: `app/src/Mod/Unnamed/World7Zombies.*` (rules),
`app/src/Mod/Engine/World7EliteZombies.*` (engine sites), feature `world7Zombies` in `mod.json`. A missing key plays
that rule like vanilla.

## The gates

- **World 7** = exe 0x7aa4c0: `LawnApp+0x7f8 (mGameMode) == 0` (Adventure), `PlayerInfo != 0`, `61 <= PlayerInfo+0x24
  (profile level) <= 70`. The board's level is never read. Keys `world7.firstLevel` / `lastLevel` = 61 / 70.
- **Profile level > 60** = `cmp [PlayerInfo+0x24], 0x3c; jle`, no mode test (true in 71-73 and in minigames with such a
  profile). Key `above60.level` = 60. Used by: black Football, vase Catapult, Tree of Wisdom HP (with "or finished").
- The 7-10 boss level test 0x7aa100 (`mode 0x83` or board level 0x46) is used once here (the pole-head Catapult shot).

## Keys

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| flag.fillRows / topRow / topRowSixRows / bucketHp | 1 / 4 / 5 / 1500 | - | 2.4 | hook 91 0x7a1d2b (Board::SpawnZombieWave after its AddZombieInRow): world 7 and type 1 -> ESI = 4 (5 when mBackground is 2 or 3), down to 0: if ESI != the flag's row: PickRowForNewZombie(1) (result dropped) and AddZombieInRow(1, ESI); then on that zombie (or the flag itself in its own row) with a body reanim: helm type 2, 1500 / 1500, show `anim_bucket` |
| imp.gargRoll / gargHit / gargHpBonus | 3 / 1 / 930 | - | 2.4 | hook 571 0x7a1f36 (UpdateZombieImp, landing done, before `phase = 0`): world 7, `Rand(3) == 1` -> type 0x17 (Gargantuar), +0x134 = 0x2b, max and body += 0x3a2. The Imp keeps its own reanim |
| football.blackExtraHit / blackBodyHp / blackHelmHp | 0 / 800 / 4500 | - | 2.4, 8.5 | hook 489 with the elite option at its default (0x800258 = 0): c12af0 -> c123e2 `Rand(4)`; non-green -> 0x9dd321: `bl = profile level > 0x3c`, gold `Rand(13)`, else `Rand(3)`: 0 with bl -> 0xc11df0 (8 image overrides IMAGE_B1. .. IMAGE_RL, +0x14c = 0x19) -> 0x9dd460: body 800 / 800, helm 4500 / 4500 (0x9dd433: 900 / 2200 for a gold one, not reachable on this path). Green never turns black (bl is cleared). P = 3/13 at profile level > 60 |
| catapult.vaseRollFrom / vaseRollBelow / vaseBalls | 50 / 60 / 10 | - | 2.4 | hook 498 0x796e09 -> 0x910000: the Rand(100) of the pole-head roll, 50..59 and profile level > 0x3c -> +0x134 = 0x70, balls +0x114 = 0xa (the study said 5), the 4 `Zombie_catapult_basketball*` tracks (0x66ed08..) -> IMAGE_BUG_SPRAY (0x6a744c) |
| catapult.shotRoll / vaseShotBelow / poleShotBelow / poleShotBallCap | 100 / 35 / 50 / 5 | - | 2.4 | hook 537 0x7a1940 (ZombieCatapultFire, after ProjectileInitialize): 0x70 -> `Rand(100) < 0x23` -> projectile type 0x20; 0x19 on the board in world 7 or the boss level -> `Rand(100) < 0x32` -> type 0x12, balls > 4 -> 5. Hook 382: type 0x12 kills the plant of its cell and leaves a vase (grid item 7) with a random zombie `Rand(0x21)` (not 11-14, 16, 20, 25) |
| jack.popMaxBodyHp | 370 | - | 2.4 | hook 707 0x7a0a8c: world 7, type 0xf, +0x134 != -1 (an elite Jack), body `<= 0x172` (unsigned) -> +0x68 = 1 and `jmp 0x531877` = the `ret` of TakeDamage: the hit does no damage |
| coin.footballGold | 1 | - | 2.4 | hook 686 0xc11260 (Day 2.3): the profile-level > 60 Football copy is added with `[0x9dd48e] = 2`; hook 489: flag 2 -> c046f0 `jz 0x9dd39d` -> c12bc0 -> +0x134 = 0x102 (gold), no Rand drawn |
| tree.minHeight / maxExtraFeet | 100 / 200 | - | 2.4 | hook 268 0x7a1c60 (before `mPlantMaxHealth = mPlantHealth`): `[0x800254] != 1` (HARDWS, off by default), board exists, mGameMode 0, `byte PlayerInfo+0x22c (mPurchases[27] Tree) == 1`, `+0x2c (finished) >= 1` or `+0x24 >= 0x3d`, `+0xf4 (mChallengeRecords[49] = tree height) > 100`: HP = fistp(HP * (1 + min(h - 100, 200) / 100.0f)) |
| zombotany.peaHeadConeHp | 370 | - | 4.1 | hook 507 0x795957: helm type 1, 370 / 370, show `anim_cone` (every mode) |
| zombotany.wallnutHelmHp | 1600 | 1100 | 4.1 | in-place 0x523825 |
| zombotany.tallnutHelmHp | 2400 | 2200 | 4.1 | in-place 0x523957 (`mov [eax+0xd0], 0x960`) |
| zombotany.tallnutOddRoll | 12 | - | 4.1, 8.7 | hook 508 0xc033a0 sits at 0x523969, right after the Tall-nut case's `0x960`: `Rand(0xc) == 0` (never with option 1) -> +0x134 = 0x101. **It is the Tall-nut head's roll, not the Jalapeno's** (study table row 28 corrected). What 0x101 does (summons a Gargantuar or Football every 12 s, drawn purple at alpha 176) and the regeneration: `SOURCES-tallnut-zombie.md` (Plan 9 R7) |
| zombotany.jalapenoBodyHp | 870 | 500 | 4.1, 8.7 | in-place 0x523a81 `mov [esi+0xc8], 0x366` (resolves the study's open body HP) |
| zombotany.jalapenoConeHp / jalapenoDoorHp | 370 / 1100 | - | 4.1 | hook 509 0x797b36: shield type 1 (screen door) 1100 / 1100, AttachShield, helm type 1 370, `anim_cone` |
| zombotany.gatlingBucketHp | 1100 | - | 4.1 | hook 510 0x79599f: helm type 2 1100, `anim_bucket` |
| zombotany.squashBucketHp / squashDoorHp | 1100 / 1100 | - | 4.1 | hook 511 0x797bb4: door 1100 + bucket 1100 |
| gatling.spreadRoll / spreadBelow / spreadVx / spreadVy | 100 / 50 / 2.82117343 / 1.78649282 | - | 4.1 | hook 575 0x795ce6 (normal) / 0x795d88 (hypnotised), per pea: `Rand(100) <= 0x31` -> two more peas at the pea's mX / mY, render order - 1: motion 7, vx -[0x69adf0] (+ when hypnotised), vy +-[0x69af44]; type 0xd (0 and damage flags 1 when hypnotised) |
| heads.hypnotisedFirePlayerPeas | 1 | - | 4.1 | hook 572 0xc03f19 (Peashooter head: hypnotised -> AddProjectile type 0, +0x74 = 1) and 576 0x795c91 (Gatling head: motion 0, type 0, flags 1, mPosX = mX + 94.12 + 5.80, mX += 100, mPosY = mY + 8) |
| jalapeno.burnsHypnotised / iceTimer | 1 / 20 | - | 4.1 | hook 573 0x958130: not hypnotised -> every zombie that is the Zomboss with an ice ball in its row (other team) loses the ice ball; Zomboss or same row with `EffectedByDamage(0xff)` (= hypnotised ones) burns; then the vanilla plant burn and DieNoLoot. Hypnotised -> Plant::BurnRow(row) with a Jalapeno, `Board+0x624 + row*4 = 0x14`, DieNoLoot (no plant burn) |
| squash.jumpOnReach / landingZombieDamage | 1 / 1800 | - | 4.1 | hooks 577-584 (0x958200..0x9585c0): jumps when FindZombieTarget hits one it may damage (`EffectedByDamage(hypnotised ? 1 : 0x81)`) or, not hypnotised, FindPlantTarget(chew) finds a plant (vanilla: only once it eats); the target id / kind go to +0xf4 / +0xf8 and the head follows the target's x while it lives (0x9582f0); landing (0x958460): not hypnotised -> the squash, and every zombie of the other side whose rect covers the spot (Zomboss or same row) takes 1800 |
| almanac.zombieCount | 33 | 26 | 4 | loops `cmp 0x21` at 0x40324f / 0x403bd0; hooks 9 / 10 (0xa84a33 / 0xa849fe): types 0x1a..0x1f (not 0x20) take their name and `[%s_DESCRIPTION]` key from the 5-byte table 0xb232b9 (豌豆 坚果 辣椒 机枪 倭瓜 高坚果) |

Wave values / pick weights of 26-32 are in `data/zombies.json` (only Gatling 5 differs from vanilla; table at 0x69dd58,
`unnamed-tables.json`). Their mZombieName strings P_ZOMBIE .. K_ZOMBIE (0x955900) are not used by any screen this port
draws.

## Strings (`strings/en-corrections-world7.txt`)

The exe's ZomBotany Almanac keys are the Chinese words above. This port uses English keys PEASHOOTER_ZOMBIE,
WALLNUT_ZOMBIE, JALAPENO_ZOMBIE, GATLING_PEA_ZOMBIE, SQUASH_ZOMBIE, TALLNUT_ZOMBIE (+ `_DESCRIPTION`) with the en.txt
translation of the 豌豆.. entries. Code-wins corrections: Gatling toughness "high" -> 270+1100=1370 and "P=1/2"; Tall-nut
"extremely high" -> 270+2400=2670; Imp elite 1100 -> 270+930=1200; Football black 800+4500 with P=3/13 (Almanac
P=1/2); Catapult gets a line for the bug-spray form (P=1/10, world 7). The Peashooter, Wall-nut and Tall-nut skills are
kept as the mod wrote them although their code was not found (below).

## Reused, not repeated

- Gargantuar / Giga staff 0x106 (RoofZombies, `roofZombies.garg.staff*`): its 1-in-20 counter is the vanilla
  `aPoleHit = Rand(100)` (`% 20 == 1`, study 8.9 answered by the Roof port); the staff Giga's thrown zombie with
  elites forced (hook 565) is there too. Not world-gated.
- Pole Vaulter road sign 0x29 (DayZombies, `dayZombies.pole.roadSign*`, rolls 3..9 of Rand(22) = 7/22): its world
  number now comes from the world-7 gate (profile level), not the board level. The study's "0x32 road sign" is the
  glove (Day study correction).
- Newspaper Almanac paper (NightZombies, profile level > 60 or finished) and the silver-coin Normal 0x105 (DayZombies;
  its roll has no world gate, study 8.6 answered by the Day study).

## Not located, kept vanilla (study 8.8 and more)

- Peashooter Zombie fire-rate ramp, Wall-nut Zombie self-copy, Tall-nut Zombie regeneration: no code found.
- Football black armour damage: found later at hook 705 (0x818069, x0.85 / x1.2, not the Almanac's -40 % / +25 %) and
  ported with the Gatling-head green Football (variant 0x6b) and the gold + black option-0 path: `SOURCES-elite-gaps.md`
  (Plan 9 R4, feature `eliteGaps`). The "0x9dd433 not reachable" note in the table above is wrong at profile > 60.
  The black form shares the green one's faster bites (hook 672 tests `+0x14c != 0`), not its walk speed (0xc12560
  tests 0x1a) nor its helmet drop (640 tests 0x1a).
- The green Football's world-7 Gatling-head form (variant 0x6b): ported in Plan 9 R4, see SOURCES-elite-gaps.md
  (feature `eliteGaps`).
- Catapult projectiles 0x12 (vase) and 0x20 (bug spray), the vase Catapult's volley and hook 549: ported in Plan 9 R3,
  see SOURCES-catapult-shots.md (feature `catapultShots`; without it the shot stays a basketball, logged).
- Variant 0x101 of the Tall-nut head: rolled and saved, no behaviour found.
- Hook 549 (basketball tracks hidden as balls drop below 5): ported with the catapult shots (SOURCES-catapult-shots.md).
- Elite option 0x800258 (INFZOM) stays at its default 0, as for every other world.

## Rulings

- The Imp that becomes a Gargantuar keeps the Imp reanim, as the exe: its smash plays track 0 of the Imp reanim (log
  "Can't find track 'anim_smash'") and still kills the plant on the smash event. No Gargantuar damage images.
- ZomBotany HP / armour apply in every Unnamed mode (the exe patches are not gated), so Unnamed's ZomBotany minigames
  change too; vanilla mode is untouched.
- Jalapeno / Squash heads carry a screen door, so the Night screen-door rules (reflected shots) apply to them, as in
  the exe where those rules test the shield type.
- Squash landing hit box: a 100 x 100 rect from the landing x - 10 (the exe's 0x957680 cover test on the head's rect
  was not decoded to exact numbers).
- Almanac: 6 x 6 grid of 66 px windows (scale 0.868), order 0..24, 26..32, Zomboss last; the mod's own layout was not
  read. Types 26..31 keep start level 99, so their page opens after the adventure is finished (same rule as the
  others). Their small pictures use the zombie cache, which draws a plain zombie (no plant head); the big picture is
  right.

## Seen on the Mac (2026-11-23)

Runs: `pvz-portable -pvzu-mode unnamed -pvzu-pack <pack> -pvzu-width 1300 -pvzu-level 4 -pvzu-seed 7
-pvzu-dev-player-level 65|41 [-pvzu-force-variant ...] -pvzu-dev-spawn ... -pvzu-dev-plant ... -pvzu-log-zombies <f>
-pvzu-hidden -pvzu-quit-frame N` (`SDL_AUDIO_DRIVER=dummy`); board level 4 (1-4) in every run, only the profile level
changes:
- natural rolls, 50 spawns each, profile 65 / 41: Pole road sign 16 / 0, Football black 15 / 0 (green 8 / 8, gold
  3 / 3), Catapult vase 3 / 0 (pole head 31 / 31), Tall-nut 0x101 2 / 2.
- Flag wave (wave 10 of 1-4, profile 65): 4 Flags added in rows 4, 3, 1, 0 and all 5 with a 1500 bucket.
- Imp: of 5 landings 1 became a Gargantuar (body 1180 / 1200) and smashed the Peashooter in front of it.
- Jack (forced ice head): popped at body 370 when hit (`jack-pops`).
- ZomBotany spawns: Peashooter head cone 370, Wall-nut 1600, Jalapeno 870 + cone 370 + door 1100, Gatling bucket 1100
  with spread peas, Squash bucket + door (jumped onto the Wall-nut in column 5 as soon as it was in reach), Tall-nut 2400; drawn with cones,
  buckets and doors. Jalapeno burned its row.
- Tree of Wisdom 150 ft: Peashooters 300 -> 450 with profile 65, unchanged with profile 41 (not finished).
- black Football and vase Catapult drawn with their art; both kept form, HP, balls and art after save + Continue.
- Almanac (finished once): 33 windows, Gatling Pea Zombie page with its English name and corrected text. Vanilla mode:
  the vanilla 26-window page.
- vanilla mode with the same spawns and forced forms: 0 `world7` lines, vanilla HP (Wall-nut head 1100, Jalapeno 500,
  Catapult 850, Gargantuar 3000).

Not seen on the Mac: hypnotised Peashooter / Gatling heads, the hypnotised Jalapeno and Squash, the Zomboss ice ball
burn, the coin's gold Football copy, the pole-head ball cap in world 7, the Flag rows on a six-row lawn (unit tests
only).
