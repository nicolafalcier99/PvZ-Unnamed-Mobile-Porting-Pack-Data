# Sources: Roof zombies and elite forms (`data/rules-roof-zombies.json`)

Plan 6 Task 2. Evidence: the research notes (w5-roof) sections 0 (G2, G7), 2.1-2.7, 6, 7 and 8
(read-only reads of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe was never run). A few hooks were re-read for this
task with the research notes (w5_show) (Ghidra export) and radare2 `pd` (static disassembly, nothing run): 487, 488, 498,
513, 514, 522, 524, 525, 527, 529, 544, 565, 566, 568, 600, 601, 619, 630, 647 (0x95c230), 655, 662 (0x7a6be3), 672,
694, 696, 702, 705, 710, 722 (DetachShield 0x5330e0), 790, 793. Code wins over the Almanac and the video. App code:
`app/src/Mod/Unnamed/RoofZombies.*` (rules), `app/src/Mod/Engine/RoofEliteZombies.*` (engine sites), feature
`roofZombies` in `mod.json`. A missing key plays that rule like vanilla (value in the "vanilla" column).

Zombie fields: +0x134 = `ZombieState.variant` (Bungee wheelbarrow 0x16, Jack head 0x17; Ladder shovel 0x18, pile 0x35,
ghost 0x37; Catapult pole head 0x19; Gargantuar / Giga staff 0x106). The pile's spare ladders (exe Board+0x5888 side
array, stride 0x15c, by zombie id) = `ZombieState.counter` (saved since Plan 2). Balls = the vanilla mSummonCounter.

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| roofZombies.bungee.eliteRoll / eliteBelow | 12 / 3 | no roll | 2.1 | hook 488 0x796eb2: `r = Rand(12)`, `r < 3` -> 0xc04440: `(r & 1) + 0x16` (0 / 2 wheelbarrow, 1 Jack head); in I, Zombie (0x4537d0) or with flag 0xc04476 (Zomboss bungees) -> 0x17 (0x796ecf) |
| roofZombies.bungee.wheelbarrowHpBonus | 750 | - | 2.1 | 0xc04440: `+0xc8 += 0x2ee` for 0x16 only (450 -> 1200) |
| roofZombies.bungee.wheelbarrowBottomCs / jackBottomCs | 2147483647 / 0 | 300 | 2.1 | hook 527 0x796ffd: +0x68 at the bottom |
| roofZombies.bungee.noPlantRadius | 1 | - | 2.1 | hook 46 0x796f2b -> 0xc04890 -> 0x796f8b: a live (+0xec), headed (+0xba), not hypnotised (+0xb8) Bungee in phase 6 with 0x16 -> CanPlantAt "not here" for row +-1, mTargetCol +-1 |
| roofZombies.bungee.jackOffsetPx | 30 | - | 2.1 | hook 529 0x797051: 0x17 on board -> `AddZombieInRow(0xf, plant row)`, `mPosX = GridToPixelX - [0x679318]` (30.0), Jack +0x68 = 0 |
| roofZombies.bungee.carryZombies / carryMaxHp | 1 / 120000 | 0 | 2.1 | hook 522 0x959000 / 0xc02530 / 0x959023 / 0x957680: same row, `EffectedByDamage(bungee hypnotised ? 1 : 0x81)`, max HP < 0x1d4c1, not Bungee / Boss, rect covers the target column -> bungee +0xf0 = its id, its +0x64 (height) = 9, no plant; hook 524 0x959100: rising with it plays foley 0x44 (FLOOP) and lifts no plant |
| roofZombies.ladder.shovelRoll / shovelHit | 4 / 2 | no roll | 2.2 | hook 487 0x796d1e: `Rand(4) == 2` -> 0x18, shield +0xdc += 0x172 (its max +0xe0 stays 500), image 0x6a7368 |
| roofZombies.ladder.shovelShieldBonus | 370 | - | 2.2 | same |
| roofZombies.ladder.secondRoll / ghostMinPlants | 4 / 5 | no roll | 2.2 | 0x95aa10 (only after a failed shovel roll, not with option 1): `Rand(4)`: 1 -> 0x37 when Board+0xbc >= 5, else 0x35; 0 -> 0x35 |
| roofZombies.ladder.pileSpares / pileSparesLate / pileSparesLateLevel | 5 / 11 / 60 | - | 2.2 | 0xc02cc0: side counter = 5 if PlayerInfo+0x24 < 0x3c else 11 |
| roofZombies.ladder.pileLadderHp | 500 | - | 2.2 | hook 722 0x95ab40 (DetachShield 0x5330e0 + 0x8a, the start of the ladder branch): spares-- , shield type 3, 500 / 500, AttachShield, image 0x6a76b0, return (no phase change) |
| roofZombies.ladder.pileCarrySpeed / pileFreeSpeed | 1.6 / 3.0 | 1 | 2.2 | hook 662 chain -> 0x7a6be3: shield type 3 -> anim-rate factor 0x3fcccccd (1.6), else 0x40400000 (3) |
| roofZombies.ladder.ghostSpeed | 2.0 | 1 | 2.2 | 0x95c380: 0x37 and not eating (+0x51) -> 0x40000000 |
| roofZombies.ladder.ghostTeleportAge / ghostTeleportStepPx | 2 / 80 | - | 2.2 | hook 619 0x95c2a0: age (+0x60) == 2, on board, height 0, not hypnotised: x = (max column of plants in its row without a ladder (0x95c330) + 1) * 0x50; 0 when none |
| roofZombies.ladder.ghostOneBiteMaxHp / ghostToughBite | 1000 / 1 | 4 | 2.2 | hook 790 0x95c3b0: plant max HP (+0x44) < 0x3e9 -> bite = HP + 1, else 1 |
| roofZombies.ladder.ghostAlpha | 128 | 255 | 2.2 | hook 647 -> 0x95c230: colour (255, 255, 255, 0x80), chilled (75, 75, 255, 0x80) |
| roofZombies.catapult.hp | 1350 | 850 | 2.3 | in-place patch 0x522e87 |
| roofZombies.catapult.poleHeadRoll / poleHeadBelow / poleHeadAllEliteBelow | 100 / 50 / 60 | no roll | 2.3 | hook 498 0x796e09: `Rand(100) <= 0x31` -> 0x19, image 0x6a75b0; 50..59: world-7 vase 0x70 when PlayerInfo level > 60, else 0x19 only with option 2 |
| roofZombies.catapult.faithLockHp | 190 | - | 2.3 | hook 705 -> 0xc00000 (via 0x95a120 / 0xc019ed): not Wall-nut Bowling, balls (+0x114) != 0, `body - damage <= 190` -> damage &= 1, body = 190; hook 793 0x95a500: with balls it takes TakeDamage, never the burned path |
| roofZombies.garg.gigaHp | 7200 | 6000 | 2.4 | hook 514 0xc11620: `+0xc8 = 0x1c20` after the red-eye head |
| roofZombies.garg.staffMod / staffHit | 20 / 1 | - | 2.4 | hook 513 0xc116a0: `aPoleHit % 0x14 == 1` (or option 2; never option 1) -> 0x106, image 0xc11604 (`reanim/Zombie_gargantuar_staff.png`, mod resources.xml line 385) |
| roofZombies.garg.staffThrowRoll | 33 | - | 2.4 | hook 565 0xc11500: `Rand(0x21)` re-rolled while 1, or > 9 and not 12 / 15 and (< 17 or 19 or 25): 25 types; a Giga sets 0x800258 = 2 around the AddZombie (restored by hook 566) |
| roofZombies.garg.staffMaxBoardZombies | 50 | - | 2.4 | hook 568 0xc11660 / 0xc11700: Board+0xa0 < 0x33 and not hypnotised -> phase 0x45 (throwing) again |
| roofZombies.garg.throwAnyDistance | 1 | 0 | 2.4 | patch 0x527216 `70 2a` (`jp` -> `jo`): the "distance > 40" test is never taken |
| roofZombies.garg.throwMinDistanceAlways | 1 | 0 | 2.4 | patch 0x527056 `test ah, 0x41; nop; nop`: the clamp's jump is gone, the distance is always the minimum (40 lawn, -140 roof) |
| roofZombies.imp.thrownSkipsHouse | 1 | 0 | 2.5 | hook 630 0x7a0281: phases 0x47 / 0x48 skip the "reached the house" check (the headless 1800 damage stays) |

Wave values and pick weights (G7: Bungee 2, Ladder 3 / 2000, Catapult 3, Gargantuar 6) were already in
`data/zombies.json` (Plan 1 tables). Bungee body HP 450 is vanilla (0x522a15). The ladder body / shield 500 / 500 is
vanilla. Imp elites (hook 571) are world 7 only. Yeti (2.6) has no hook. Pole Vaulter graves and Flower-Pot graves
(2.7) are the Day / Roof-levels rules.

Fixed in code (not rules):
- Bungee steal guard: a plant already on a bungee (+0x134 / mOnBungeeState != 0) is not taken again (a fix the
  study lists with the bungee rows; the vanilla DO_FIX_BUGS block only clears the other bungee's target at lift time).
- Ladder targeting (hook 655 0x796dd6 / 0xc02c90): the shovel's and the pile's `aPlaceLadder` starts true (any plant is
  a ladder target, vanilla: Wall-nut / Tall-nut / Pumpkin); the pile chews only a plant that has a ladder and ladders
  only one without (attack types 0 / 3; vault and drive-over as vanilla).
- Shovel (hook 600 0x796d8f): foley 8 (FOLEY_USE_SHOVEL) and `Plant::Die` instead of the ladder; no sound, no climb, no
  DetachShield (continues at 0x52aa25). Its shield keeps the shovel image (hook 696: variants 6 and 0x18 skip the
  damage images).
- Pile (hooks 600 / 0x95ac80, 694, 702, 710, 672): each ladder it places calls
  `Challenge::IZombiePlaceZombie(BUNGEE, plant col, plant row)`; DropShield keeps the new ladder (0x95ac10); body damage
  also hits its ladder for `damage >> 1` (0xc02d0f); damage left after a ladder breaks goes into the next one
  (0x95ac40 loop); no bites while it carries a ladder (0x79c300).
- Ghost (hook 601 0x95c3f0): no DetachShield after placing a ladder (it climbs and keeps it).
- Catapult pole head (hook 544 0x796e70): keeps the plant with the largest column.

Art (study 7; every file is in the pack's assets, served through the asset overlay):
wheelbarrow = `anim_head1` -> IMAGE_ZEN_WHEELBARROW (`images/Zen_WheelBarrow.png`); Jack head = `anim_head1` ->
IMAGE_REANIM_ZOMBIE_JACKBOX_BOX (`reanim/Zombie_jackbox_box.png`); shovel = `Zombie_ladder_1` -> IMAGE_SHOVEL_HI_RES
(`images/Shovel_hi_res.png`); the pile's new ladders = `Zombie_ladder_1` -> IMAGE_REANIM_ZOMBIE_LADDER_1; pole head =
`Zombie_catapult_driver_head` -> IMAGE_ZOMBIEPOLEVAULTERHEAD (`particles/ZombiePoleVaulterHead.png`); staff =
`Zombie_gargantuar_telephonepole` -> `reanim/Zombie_gargantuar_staff.png` (Unnamed-only file, loaded by name).

Rulings and open points:
- The global elite option 0x800258 is fixed at 0 (default), as for the other worlds. Only a throwing staff Giga sets
  "all elites" (hook 565), and only the Roof rolls read it here (Ladder second roll, Catapult, Gargantuar staff); the
  Day / Night / Pool / Fog rolls of the zombies it throws keep their default.
- A staff Gargantuar's thrown zombie that is not an Imp has no throw animation in the port: it is set down where the
  Imp would land (the Imp's flight of UpdateZombieImp stepped at once: start x - 133, velX 3, altitude 88, the
  minimum throw distance), in the thrower's row, with its hypnosis and chill. A thrown Bungee keeps its own sky
  target. (What the exe does with a non-Imp in phase 0x47 was not traced.)
- Dr. Zomboss bungees (B8): the Bungee roll reads `ZombossBungeeSpawning()` of Plan 6 Task 4 (exe flag 0xc04476); a
  weak `false` stands in for it until that task is merged. Umbrella Leaf RV blocking is that task's (`boss.umbrellaRv*`).
- "Red ladder" 0x37 of the study is drawn half see-through (alpha 128, hook 647), so the code calls it "ghost".
- The ghost's teleport to x = 0 when its row has no unladdered plant is ported as read.
- Hypnotised-bungee landing branch (hook 525 0xc11d50) not ported (flow not read in full; study U11).
- Not found in code (study U1, U2): Catapult "shoots faster near death", Imp "ignores lawnmowers while thrown".

## Seen on the Mac (2026-11-23)

Runs: `pvz-portable -pvzu-mode unnamed -pvzu-pack <pack> -pvzu-width 1300 -pvzu-level 42|43|46|47|48 -pvzu-seed 7
-pvzu-dev-fog log -pvzu-force-variant <TYPE>:<n> -pvzu-dev-spawn <TYPE> -pvzu-dev-plant ... -pvzu-log-zombies <file>
-pvzu-hidden -pvzu-quit-frame N` (`SDL_AUDIO_DRIVER=dummy`), one screenshot per forced form:
- wheelbarrow (5-2): head drawn; three bungees stay at the bottom (counter 2147483647); Sunflowers planted in column 1
  went only into row 4, the 3x3 cells of the hanging wheelbarrows stayed empty.
- Jack head (5-2): counter 0, the Jack lands at plant x - 30 (170) and pops; it rolled its own form (an ice head froze
  the plants, a plain one blew).
- shovel (5-3): shovel drawn in place of the ladder, shield 870; each shovel digs the Flower Pot and then the plant on
  it, column by column (the pot comes first in FindPlantTarget's order, as the code reads).
- ladder pile (5-3): ladders a Wall-nut, then Peashooters and pots, a Bungee called onto each, spares 5 -> 2 seen.
- ghost (5-3): drawn half see-through; teleported on its 2nd tick from x 949 to 240 (last unladdered plant column 2),
  laddered the Wall-nut and kept its ladder, one-bite kills of 300 HP plants.
- pole head (5-6): the catapult driver wears the Pole Vaulter head (vanilla run: the bald driver), 1350 HP.
- staff (5-8): Gargantuar and Giga carry the staff; thrown types seen: Football, Screen Door, Buckethead, Giga, Pole
  Vaulter, Tall-nut head, Squash head (Giga: forcedElite=1); a Gargantuar threw again about every 190 cs.
- natural rolls (5-7, 20 spawns each): Bungee 4 wheelbarrow / 2 Jack head / 14 plain; Ladder 3 shovel / 4 pile /
  3 ghost / 10 plain; Catapult 10 pole head / 10 plain.
- vanilla mode (5-6, same forced options): 0 `roof` lines, vanilla HP (Catapult 850, Gargantuar 3000).
Not seen on the Mac: the bungee taking a hypnotised zombie, the catapult's front-most targeting and the 190 lock
(unit tests only), the thrown Imp's house check.
