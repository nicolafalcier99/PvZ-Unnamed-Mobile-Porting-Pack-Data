# Sources: Dr. Zomboss, default settings (`data/rules-zomboss.json`)

Plan 6 Task 4 (level 5-10). Evidence: the research notes (w5-roof) section 4.1 (B1-B10) and 4.3, plus
the hook asm in the research notes (hooks2) (read with the research notes (w5_show); read-only reads of Unnamed 1.3beta2
`PlantsVsZombies.exe`, the exe was never run). Code wins over the Almanac and the video. App code:
`app/src/Mod/Unnamed/Zomboss.*` (rules), `app/src/Mod/Engine/ZombossSites.*` (engine sites), feature `zomboss` in
`mod.json`. A missing key plays that rule like vanilla.

Not ported: the "[quote not included]" Legendary Zomboss option (study 4.2, exe `[0x8001a8]`, off by default, not saved; its spawn
picker below 4/5 HP is NOPped out in 1.3beta2). Everything under it (120000 HP, 3x summon, Bucketheads every 256 cs,
repeated spawns, Jalapeno-head burn roll) stays off.

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| boss.hpAdventure / boss.hpOther | 50000 / 80000 | 40000 / 60000 | B1 | hook 505 0xc02040 -> 0xc00a20; .text 0x523618 `neg/sbb/and 0x7530/add 0xc350` (mode 0x8c = 500 and Legendary 120000 not ported) |
| boss.lateSpawnRoll | 33 | vanilla 13-type list | B3 | hook 735 0x9579b0: `Rand(0x21)` re-rolled; only after the vanilla age steps (< 3500 Normal, < 8000 Cone, < 12500 Bucket) |
| boss.lateSpawnExclude | 0,1,9,10,11,13,14,16,17,20,24,25 | - | B3 | 0x9579ba..0x9579f4 `cmp eax, n / jz 0x9579b0` |
| boss.lateSpawnExcludeRow0 | 23, 32 | (vanilla drops the Gargantuar in row 0) | B3 | 0x9579f6 `cmp [esi+0x130], 0` (mTargetRow) then 0x17, 0x20 |
| boss.lateSpawnExcludeYetiKilled | 19 | - | B3 | 0x957a09 `cmp byte [Board+0x5760], 1` (mKilledYeti) then 0x13 |
| boss.copiesHypnosis | 1 | 0 | B3, B8 | spawn tail 0x957970 (via hook 736 chain); bungees 0x957dc5 `mov [esi+0xb8], boss.[0xb8]` |
| boss.stompNothingHeal | 1800 | 0 (just returns) | B4 | hook 737 0xc02800: `add [esi+0xc8], 0x708` then `jmp 0x534f48`; no cap |
| boss.crushHypnotisedDamage | 1800 | 0 | B5 | stomp row test hook 738 0x957e50, stomp contact hook 739 0x957ef0, RV hook 731 -> 0x957bf0: `EffectedByDamage(0x8d)` (0xd for a hypnotised boss), `TakeDamage(0x708, 1)`; zombie columns from `GetZombieRect` via 0x957680 (`round(x/80)-1`, `round((x+w)/80)-1`) |
| boss.crushOpensPots | 1 | 0 | B5 | 0x959b80 (stomp row test), 0x959be0 (stomp), 0x959c50 (RV): GridItem type 7 -> `Challenge::ScaryPotterOpenPot` |
| boss.umbrellaRvDamage, boss.umbrellaRvRowsBefore/After, boss.umbrellaRvColsBefore/After | 100, 2/3, 2/4 | no block | B6 | hook 731 0xc02b20: plant type 0x25, not squished (+0x142), +0x134 != 2, not dead, row in [tr-2, tr+3], col in [tc-2, tc+4] -> `sub [esi+0x40], 0x64`, `Plant::DoSpecial`, flag 0xc02bba; hook 732 0xc02bd0 skips the plant crush when the flag is set |
| boss.spitPicksHarderBall | 1 | 0 (Rand(2)) | B7 | hook 745 0x957a50: counts packet type 0x14 vs 0xe over `SeedBank+0x24` packets (type 0x30 -> +0x38 imitater type); fewer Jalapenos -> ice, more -> fire, equal -> `jmp 0x5354a0` (vanilla Rand) |
| boss.bungeeJackForced | 1 | 0 | B8 | hook 741 0xc04458: flag 0xc04476 = 1 around `ZombieInitialize`; 0xc04440 forces the passing Bungee roll to 0x17 |
| boss.bungeeEliteRoll / boss.bungeeEliteBelow | 12 / 3 | - | B8, 2.1 | hook 488 0x796eb2 `Rand(0xc)`, `cmp eax, 2 / jg` |
| boss.jackBungeeGrabCs | 0 | 300 | 2.1 | hook 527 0x796ffd (Jack-head bungee: AT_BOTTOM counter 0) |
| boss.jackBungeeJackDx | -30 | - | 2.1 | hook 529 0x797051: `AddZombieInRow(JACK, plant row)`, x = GridToPixelX(plant col) - 30, Jack +0x68 = 0 |
| boss.everyBossBalls | 1 | 0 (first boss only, hypnotised too) | B9 | hook 340 0x957810 (IceZombies: every type 0x19 with +0xb8 != 1 -> BossDestroyFireball), hook 341 0x9577c0 (BurnRow: same, row == +0x148 -> BossDestroyIceballInRow) |
| boss.oneHpRefusesFreeze | 1 | 0 | B9 | hook 713 0xc10ae0: type 0x19 and body HP == 1 -> CanBeFrozen false (also active under poolZombies, its first port) |

Already ported elsewhere (not repeated here): freeze damage 200 for every HitIceTrap (hook 718) =
`nightPlants.iceTrap.damage` in `rules-night-plants.json` (the test checks it is 200); elite rolls for the boss's spawned
zombies (B10) happen in the normal ZombieInitialize path (Day/Night/Pool/Fog forms today, Roof forms with
`roofZombies`).

## Engine notes and rulings

- The boss's bungee hook (exe flag 0xC04476) is `pvzu::engine::ZombossBungeeSpawning()`, open while `BossBungeeSpawn`
  adds each bungee (`ZombossBungeeScope`). The Roof zombies task owns the Bungee elite (feature `roofZombies`): its roll
  must force the passing roll to 0x17 while that scope is open. Until that feature is on, `ZombossSites.cpp` rolls the
  boss's bungees itself (Rand(12) < 3 -> 0x17, Jack-box head image on `anim_head1`) and runs the Jack-head behaviour
  (grab at once, a Jack at plant x - 30 that pops at once); with `roofZombies` on those fallbacks return vanilla so
  nothing runs twice.
- Bungee +0xF4 (the boss id, hook 743) = the bungee's vanilla `mFollowerZombieID[0]` (saved, unused by bungee code).
- No new saved state: the heal changes the vanilla `mBodyHealth` (it may pass the max, as in the exe), the Jack-head
  bungee is `ZombieState.variant` 0x17. Checked: a boss healed to 52600 / 50000 loaded back at 52600
  (`-pvzu-dev-continue`).
- An empty stomp keeps the vanilla phase handling after it (the exe's heal jumps to the same return): the stomp phase
  still reaches its contact event once with the previous target row.
- A hypnotised boss crushes normal zombies and never plants (0x957ed6, 0x957f7d, 0x957c89); ported, unreachable with
  default settings.
- Mirror-mode (`0x52bee0` / hook 641) column shifts in the crush areas and the bungee roll are not ported (not used by
  Adventure 5-10).

## Checked on the Mac (5-10, seed 7, `-pvzu-log-zombies`)

Run: `pvz-portable -pvzu-mode unnamed -pvzu-pack <pack> -pvzu-width 1300 -pvzu-level 50 -pvzu-seed 7 -pvzu-hidden`
with a click script for Dave's lines and the `-pvzu-dev-boss-*` options (`app/src/Mod/Engine/ZombossSites.h`):
start HP 50000 (vanilla mode 40000, no `boss` lines); late spawns from the 21-type list (Catapult, Tall-nut head,
Gargantuar, Screen Door, Dancer, Giga at 600 px); hypnotised Normals crushed by the stomp (2 hit) and by the RV (2 hit);
empty stomps heal 49000 -> 50800 -> 52600; an Umbrella Leaf in column 1 stopped an RV aimed at (row 2, col 2) and
went 300 -> 200; a Jack-head boss bungee grabbed a Flower Pot at once and dropped a Jack at x 90 (GridToPixelX 120 - 30);
Ice-shroom broke the fireball (the boss took 200 per Ice-shroom), Jalapeno broke the iceball; with seed 3 the spit took
the rule's pick (ice) from the conveyor bank instead of the roll.

Found while checking (not a boss rule): five Jalapenos at once on 5-10 (`-pvzu-dev-plant JALAPENO:0`) crash in
`Projectile::DoImpact` -> `ReanimationHolder::AllocReanimation` (Pool Jalapeno barrage, 69 fireballs each); it crashes
the same with `"zomboss": false`.
