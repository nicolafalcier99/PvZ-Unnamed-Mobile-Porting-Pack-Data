# Sources: Day zombies and elite forms (`data/rules-day-zombies.json`)

Plan 2 Task 4. Evidence: the research notes (zombies) (section numbers below), read from Unnamed 1.3beta2
`PlantsVsZombies.exe` (hook rows of the research notes (hook-triage), decompile in the research notes (hooks2)). Code wins over the
Almanac and the video. App code: `app/src/Mod/Unnamed/DayZombies.*` (rules), `app/src/Mod/Engine/EliteZombies.*`
(engine sites), feature `dayZombies` in `mod.json`. A missing key plays that rule like vanilla (value in the
"vanilla" column).

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| dayZombies.startOffsetPx | 133 | 0 | 1 | hook 480, 0x959500 `push 0x85; fiadd` (not types 15, 28) |
| dayZombies.pole.startX | 955 | 870 | 1 | hook 492 `add eax,0x3bb` (+Rand(10)) |
| dayZombies.zamboni.startX | 933 | 800 | R8 | hook 495 0x959549 `add eax,0x3a5` (spawn point forward: 0x320 = 800); study `gaps/r8-options.md` 5 |
| dayZombies.catapult.startX | 958 | 825 | R8 | hook 497 0x959563 `add eax,0x3be` (forward 0x339 = 825) |
| dayZombies.gargantuar.startX | 978 | 845 | R8 | hook 512 0x95957d `add eax,0x3d2` after Rand 0x523d38 (forward 0x34d = 845); Gargantuar + Giga (the vanilla 845 case) |
| dayZombies.normal.rollRange | 8 | 0 (no roll) | 2.1 | 0xC11130 `Rand(8)` |
| dayZombies.normal.stickyMaxRoll | 0 | - | 2.1 | `cmp eax,0; je` sticky |
| dayZombies.normal.coinMaxRoll | 3 | - | 2.1 | `cmp eax,4; jl` coin 0x105 |
| dayZombies.sticky.bodyHp | 640 | 270 | 2.2 | 0x794A28 `mov [edi+0xc8],0x280` |
| dayZombies.sticky.animRateMul | 3.0 | 1 | 2.2 | hook 662, 0x796770 `fmul 3.0` |
| dayZombies.sticky.eatsPlants | 0 | 1 | 2.2 | hook 675, 0xC01B44 `cmp [edi+0x134],1; je` past FindPlantTarget |
| dayZombies.elite.noYuckyFace | 1 | 0 | 2.2 | hook 634, 0x7A9350 `cmp [esi+0x134],1; jge skip` |
| dayZombies.coin.squishWhenCrippled | 1 | 0 | 2.3 | hook 614, 0xC11210 (no arm or no head -> CheckSquish) |
| dayZombies.coin.copyAtPlantHpMax | 8 | off | 2.3 | hook 686, 0xC1127A `cmp [esi+0x40],8; jg` |
| dayZombies.coin.footballAfterPlayerLevel | 60 | - | 2.3 | 0xC1128E `cmp [ebx+0x24],0x3c; jle` |
| dayZombies.coin.footballRollRange | 10 | - | 2.3 | 0xC11298 `mov eax,0xa; call Rand` |
| dayZombies.flag.bodyHp | 640 | 270 | 3 | hook 517, 0x797DD8 |
| dayZombies.flag.drainPeriodCs | 40 | off | 3 | 0x7953C3 `div 40` on the age before ++ |
| dayZombies.flag.drainMin / drainMax | 1 / 3 | - | 3 | 0x795423 `Rand(3)+1; sub [board+0x5560]`, clamp 0 |
| dayZombies.flag.biteRemainderMin / Max | 1 / 5 | 0 / 0 | 3 | hook 672, 0x79C340 `cmp edx,6; jge; test edx,edx; je` |
| dayZombies.cone.rollRange | 11 | 0 | 4.1 | hook 484, 0x795FB9 (0 -> 2, 1 -> 3) |
| dayZombies.bucket.rollRange | 9 | 0 | 5.1 | hook 485, 0x7970EB (0 -> 4, 1 -> 5) |
| dayZombies.pumpkin.bodyHp | 1100 | 270 | 5.1 | 0x797151 `mov [edi+0xc8],0x44c` |
| dayZombies.pumpkin.animRateMul | 0.33333331 | 1 | 5.2 | hook 662, 0x79679B (0x3EAAAAAA) |
| dayZombies.pumpkin.giveBucketHp | 1100 | - | 5.2 | 0x79474F..0x7947B8 |
| dayZombies.aura.periodCs | 650 | off | 4.2 | 0x797323 `cmp [esi+0x114],0x28a` |
| dayZombies.aura.rangePx / rows | 200 / 1 | - | 4.2 | 0x797381..0x7973B5 |
| dayZombies.dancerHead.summonOnDeath | 1 | 0 | 4.3 | hook 691, 0x79793F -> SummonBackupDancers 0x528970 |
| dayZombies.umbrella.skyDropOnDeath | 1 | 0 | 5.3 | 0x797981 -> SpawnZombiesFromSky 0x412C30 |
| dayZombies.skyDrop.typeRollRange | 25 | 0 (vanilla picker) | 5.3 | hook 85, 0x795C27 (accept r <= 7, 15, >= 21) |
| dayZombies.pole.bodyHp | 870 | 500 | 6.1 | 0x522CB9 `mov [edi+0xc8],0x366` |
| dayZombies.pole.rollRange | 22 | 0 | 6.2 | hook 491, 0x7A1B70 (13 + 9) |
| dayZombies.pole.skyDropRollRange / skyDropRollAdd | 19 / 3 | - | 6.2 | 0x7A1B70 (-3, +3 when `[0xC036CD]==1`) |
| dayZombies.pole.gloveMaxRoll | 2 | - | 6.2 | r 0..2 -> 0x32 |
| dayZombies.pole.roadSignMaxRoll / roadSignWorld | 9 / 7 | - | 6.2 | r 3..9 -> 0x29 only if 0x7AA4C0 (levels 61-70) |
| dayZombies.pole.vaseMaxRoll | 12 | - | 6.2 | r 10..12 -> 0x103 |
| dayZombies.glove.attackRectExtraPx | 112 | 0 | 6.2 | hook 493 (`x -= 112, w += 112`) |

Fixed in code (not rules): Normal/Ducky Tube share the Normal roll (hook 483); the pumpkin gives buckets to types
Normal, Flag, Cone, Bucket, Screen Door only (0x7973D2); auras skip boss-like zombies (body max > 120000, Boss,
Newspaper 0x7F; 0x7AA320); the Flag drain is off in Last Stand, Scary Potter Endless, I, Zombie and Adventure level 55
(0x798310); death effects need `mZombieHeight != bungee-dropped` and `mFromWave >= 0` (hook 691).

## Elite art (study 9)

Image overrides on the zombie's own body reanim; the jaw (`anim_head2`) is hidden for head swaps. Files are served
from `assets/` by the overlay under these names; if one is missing the base zombie is drawn and the form keeps its
behaviour.

| form | track -> file |
|---|---|
| Normal 1 sticky note | anim_head1 -> images/ZombieNoteSmall |
| Normal 0x105 silver coin | anim_head1 -> reanim/coin_silver_dollar |
| Cone 2 phonograph | anim_head1 -> images/Phonograph |
| Cone 3 dancer head | anim_head1 -> particles/ZombieDancerHead |
| Bucket 4 pumpkin | anim_head1 -> reanim/pumpkin_damage1 |
| Bucket 5 umbrella leaf | anim_head1 -> engine blank; hair and jaw hidden; Umbrella Leaf reanim `anim_idle` @15 attached at (65,-5), 0.2 rad, scale (-1,1) |
| Pole 0x32 glove | anim_head1 -> images/Zen_GardenGlove |
| Pole 0x103 vase pole | Zombie_polevaulter_pole2 -> reanim/Zombie_gargantuar_telephonepole; Zombie_polevaulter_pole -> particles/Zombie_seaweed |
| Pole 0x29 road sign (world 7) | Zombie_polevaulter_pole2 -> reanim/Zombie_gargantuar_duckxing; Zombie_polevaulter_pole -> particles/Zombie_seaweed |

## Text (`strings/en-corrections-day-zombies.txt`)

Code wins over the Almanac: the Browncoat's silver-coin form (P=3/8) and the Pole Vaulter's glove and telephone-pole
forms (P=3/22 each) roll in every world but are missing from the Almanac; the road sign is P=7/22 (not 1/3); the Flag
drains 1-3 sun every 0.4 s and bites 3x as often; the phonograph heals to full; the pumpkin walks 3x slower and
re-buckets itself too.

## Rulings (where the port decides)

- No elite roll for street-preview, Almanac and Zombatar zombies (`mFromWave` cutscene/UI/winner): the video says the
  level preview does not show variants; the exe's preview path was not traced (study 11.2).
- Coin copy: the plant is killed once through the vanilla "plant eaten" steps (gulp, plants-eaten count, Die,
  ZombieAtePlant) and the bite stops there; the exe calls Plant::Die and then runs the rest of the bite on the dead
  plant. The copy takes the eater's `mFromWave` (the exe's value was not traced, study 11.4).
- The Football copy (player level > 60) does not get the exe's forced Football form `[0x9DD48E]=2` (unknown form).
