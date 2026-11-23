# Sources: Night zombies and elite forms (`data/rules-night-zombies.json`)

Plan 3 Task 2. Evidence: the research notes (w2-night) section 2 (and the research notes (zombies)
Appendix A for the +0x134 codes), plus reads of Unnamed 1.3beta2 `PlantsVsZombies.exe` made for this task with the
study's read-only tools (the research notes (w2_show) over `out/hooks2.jsonl`; the research notes (w2_r2) / radare2 for code
hooks2 does not export; the exe was never run). Code wins over the Almanac and the video. App code:
`app/src/Mod/Unnamed/NightZombies.*` (rules), `app/src/Mod/Engine/NightEliteZombies.*` (engine sites),
`app/src/Mod/Unnamed/ReanimCompiled32.*` (Unnamed's own reanim), feature `nightZombies` in `mod.json`. A missing key
plays that rule like vanilla (value in the "vanilla" column). "(new)" = read from the exe for this task, not in the
study.

Zombie fields: +0x134 = `ZombieState.variant`, +0x14C = `ZombieState.subVariant` (new), +0x12C = `ZombieState.stored`
(new; 0x104 Dancers: -1 = random follower types). The Dancer "carnival" count (every 12 backups all graves rise) is
Night levels' and lives in `ZombieState.counter`. Codes are the exe's: gold Football 0x102 (258), random summoner
0x104 (260), knife 0x31, Almanac paper 0x2A, Tall-nut door 6, trophy 9, moonwalker 10; subVariant 1 = football-head
Newspaper, 0x1A = green Football. 0 = no form (Day convention; the exe writes -1).

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| nightZombies.newspaper.bodyHp / knifeBodyHp | 500 / 1500 | 270 | 2.1 | hook 517, 0x901D50 `cmp [edi+0x134],0x31; mov [edi+0xc8],0x5dc / 0x1f4` |
| nightZombies.newspaper.eliteRollRange | 5 | 0 (no roll) | 2.1 | 0xC05770 `setne al; add eax,4; Rand` (not in I, Zombie) |
| nightZombies.newspaper.footballHeadMaxRoll | 1 | - | 2.1 | 0xC05825 `cmp r,2; jl` -> +0x14C = 1, anim_head1 = IMAGE_ZOMBIEFOOTBALLHEAD |
| nightZombies.newspaper.almanacRoll / almanacAfterPlayerLevel / almanacPaperHp | 2 / 60 / 300 | - | 2.1 | 0x7A1A16; 0xC06230 (player level > 60 or a finished adventure); 0x7AA100 (not level 70); 0x7A1A41 paper >= 0x12C |
| nightZombies.newspaper.almanacBodyPerPaperHit | 15 | 0 | 2.1 | hook 695 (study) |
| nightZombies.newspaper.knifeRoll | 3 | - | 2.1 | 0xC0584C -> 0x901CE5 `+0x134 = 0x31; +0xBC = 1; show Zombie_knife` |
| nightZombies.newspaper.footballHeadWalkMul | 1.5 | 1 | 2.1 | hook 663, 0xC058C0 -> 0xC034BA `fmul [0xC034CE]` (= 1.5) on the walk rate |
| nightZombies.newspaper.footballHeadPaperSoaksBody | 1 | 0 | 2.1 | hook 702, 0xC05970: reading (0x1D) + sub 1 -> TakeShieldDamage(dmg, 0), body damage 0 |
| nightZombies.newspaper.madChecksPerTick | 3 | 1 | 2.1 | hook 632, 0x79C000: phase 0x1F calls 0x52F4C0 three times |
| nightZombies.newspaper.madBiteRemainderMin / Max | 1 / 5 | 0 / 0 | 2.1 | hook 672, 0x79C31A `cmp [edi+0x28],0x1f; je 0x79c340` (bites when age % ticks is 1..5) |
| nightZombies.newspaper.madButterCs | 500 | 400 | 2.1 | hook 720, 0x95A700 `type 5 && phase 0x1F -> +0xB0 = 0x1F4` |
| nightZombies.newspaper.eatZombieDamage / eatBossDamage | 13 / 2 | 4 | 2.1 | hook 689, 0x7C0000 (2 vs Zomboss unless reading) |
| nightZombies.eatZombie.damageFlags | 8 | 9 | (new) | 0x7C0014 / 0x7C0036: every hypnotised eater bites with flags 8 (vanilla 9) |
| nightZombies.knife.madAnimDiv | 3.0 | 1 | 2.1 | 0x901DB5 `type 5 && 0x31 && phase 0x1F: fdiv 3.0` (ApplyAnimRate) |
| nightZombies.knife.killDelayCs | 32 | off | 2.1 (resolves unresolved 2) | 0x901DEB: the chew sets plant +0xB8 (mEatenFlashCountdown) = 0x10020; 0xC0270D kills at 0x10000, i.e. 32 cs later |
| nightZombies.knife.skipsNormalBite | 1 | 0 | 2.1 | 0xC02730 `cmp [ebp+0x134],0x31 -> 0x651232` (no 4-HP bite, any phase) |
| nightZombies.door.tallnutRollRange | 5 | 0 | 2.2 | hook 486, 0x796159 `Rand(5); cmp eax,0` -> variant 6 (not I, Zombie) |
| nightZombies.door.reflect / reflectCostHp | 1 / 1 | off | 2.2 (resolves unresolved 9) | hook 709: 0x7960A6 (shield 1, flags & 0xB == 0), 0x7966FC (source is a projectile), 0x7960C3 (not type 6/7, not motion 9), 0xC10DF0 `dec eax; add [esi+0xdc],eax`, 0x955E90 (motion 6 + range flags 0, or motion 0 + flags 1 if the door walks backwards; +0x88 = 1) |
| nightZombies.door.tallnutShieldFirst | 1 | 0 | 2.2 | 0x796104 / 0x7961C0: variant 6 (not Boss) always hits the shield and ignores HITS_SHIELD_AND_BODY |
| nightZombies.football.helmHp | 2800 | 1400 | 2.3 | 0x522BAA `mov [edi+0xd0],0xaf0` |
| nightZombies.football.greenRollRange / greenBodyHp / greenHelmHp | 4 / 300 / 3000 | - | 2.3 | 0xC12B5A `mov eax,4` -> 0xC123E2 Rand; 0xC124A2..0xC124C0 |
| nightZombies.football.goldRollRange / goldBodyHp / goldHelmHp | 13 / 540 / 1260 | - | 2.3 | 0x9DD37A `Rand(0xd)`; 0xC12BCD 0x102; 0x9DD3D6..0x9DD3F4 (0x21c / 0x4ec) |
| nightZombies.football.greenGoldBodyHp / greenGoldHelmHp | 600 / 1400 | - | 2.3 | 0xC12500 (0x258 / 0x578) |
| nightZombies.football.extraRollRange | 3 | - | (new) | 0x9DD406 `Rand(3)` drawn when not gold (black armour above player level 60); kept so the Rand sequence matches |
| nightZombies.football.goldWalkMul | 1.5 | 1 | (new) | 0xC125E5 `cmp [esi+0x134],0x102` -> 0xC034B4 `fmul 1.5` |
| nightZombies.football.goldSquishes | 1 | 0 | (new) | 0xC11242 -> 0xC034F9 `cmp [esi+0x134],0x102; je 0x52ad71` (CheckSquish, no cripple test) |
| nightZombies.football.greenBiteRemainderMax | 1 | - | (new) | 0x79C326 -> 0xC02170: not chilled, bites when age % 4 < 2; chilled, at every check |
| nightZombies.football.greenWalkBase / greenWalkHelmK / greenWalkBodyK | 1.1 / 2.0 / 1.57 | - | (new) | 0xC12560: x (2 - helm/max) x (1 + 1.57 abs(sin(1.57 (1 - body/max)))) x 1.1 (consts 0xC125F4..0xC12600, 0xC12C80) |
| nightZombies.football.greenHelmDropAgeCs / greenHelmDropMaxPlayerLevel | 800 / 70 | - | (new) | hook 640, 0xC12CAA `cmp [edi+0x60],0x320`; 0xC13180 `cmp level,0x46; jg` -> DropHelm(0) |
| nightZombies.football.greenChewBodyBonus / greenChewBonusMaxPlayerLevel | 1000 / 60 | - | (new) | 0xC12E03 `add [edi+0xc8],0x3e8` (above 60: Gatling-head form, world 7) |
| nightZombies.dancer.bodyHp | 1000 | 500 | 2.4 | 0x52352A |
| nightZombies.dancer.eliteRollRange / randomFollowerMaxRoll / trophyMaxRoll / moonwalkMaxRoll | 60 / 2 / 6 / 14 | - | 2.4 | 0x79682F `0xf + 0x2d`; 0x796848 `cmp 3`; 0xC043E0 `cmp 0xf`; 0x79686E `cmp 6; setg; +9` |
| nightZombies.dancer.trophyHpLoss | 500 | - | 2.4 | 0x79689E `sub [edi+0xc8],0x1f4` |
| nightZombies.dancer.randomFollowerDanceInCs | 3000 | 300 + Rand(12) | 2.4 | 0xC052A0 `mov [edi+0x68],0xbb8` |
| nightZombies.dancer.randomFollowerRollRange / randomFollowerJalapenoAfterPlayerLevel | 33 / 70 | - | 2.4 | 0xC03A6F (accepted 0, 2-9, 15, 22-24, 26, 27, 30-32; 28 only above level 70) |
| nightZombies.dancer.snapWithoutCountdown | 1 | 0 | (new) | 0x528CC2: GOTY bytes `75 50` (jne) are `70 50` (jo) in Unnamed, so a Dancer re-summons at the next frame-12 moment, not 100 cs later |
| nightZombies.dancer.resummonAll | 1 | 0 | 2.4 | 0x5289B7 -> 0xC04030: every summon lets living backups walk off as normal zombies and fills all 4 slots |
| nightZombies.dancer.moonwalkVelX / moonwalkAnimRate | 0.5 / 24 | - | 2.4 | 0x7A95F1 `fld [0x6793c0]` (0.5), `[0x679638]` (24); hooks 668/717/719 |
| nightZombies.dancer.randomSummonerWhite | 1 | 0 | 2.4 | hook 649, 0xC03A1A: reanim+0x98 (mFilterEffect) = 2 (FILTER_EFFECT_WHITE) at each draw |

Fixed in code (not rules): the trophy skips the summon-counter test (hook 594, 0x79692D), so it snaps at every frame-12
moment (endless summons); the moonwalker skips UpdateZombieDancer (hook 625) and keeps moonwalking (StartWalkAnim
0x7A95D0, RemoveIceTrap 0x7A9560, RemoveButter 0x7A9501) and, staying in the dancing-in phase, never eats; the
football-head Newspaper keeps its head when mad (hook 552) and ignores Garlic (hook 637); the knife plays `anim_gasp1` /
`anim_eat_nopaper1` (0x901D6F / 0x901D92); a hypnotised knife or a Potato Mine gets no mark; any eater biting a marked
plant cuts its countdown to 0x10001 (dies next tick); the Tall-nut door and the shovel ladder keep their door image
(hook 696); a reflected shot (+0x88 = 1) lives through Projectile::Die once (0x956010 -> 0x651CE7); with range flags 0
it hits plants (hook 380, 0x795E39) and, failing that, hypnotised zombies (hook 381, magic 0x114514).

For Night levels: `GoldRaisesGraveFootballs` (variant 0x102 dies -> every grave raises a Football, 0xC03520) and
`DancerCountsCarnival` (false for 0x104) are exposed in `NightEliteZombies.h`; the grave spawns are theirs.

## Unnamed's own Newspaper reanim

`assets/compiled/reanim/Zombie_paper.reanim.compiled` is a 32-bit 1051 compiled file the GOTY engine cannot load. It
has GOTY's 31 tracks (same 216 frames, within 0.3 px) plus 37 appended frames and 4 tracks: `anim_eat_nopaper1`
(frames from 216), `anim_gasp1` (from 240), `Zombie_knife` (IMAGE_REANIM_KNIFE = `reanim/knife.png`) and
`anim_football` (the I, Zombie helmet). In Unnamed mode the engine reads it (ReanimCompiled32) and uses Unnamed's
definition for `reanim/Zombie_paper.reanim`; `Zombie_knife` and `anim_football` are hidden on every Newspaper but the
knife, on board and off (street preview, Almanac pictures). If the file is missing or does not line up, GOTY's
definition stays and the knife keeps its behaviour without the blade.

## Elite art (study 7)

| form | track -> file |
|---|---|
| Newspaper football head (sub 1) | anim_head1 -> particles/ZombieFootballHead (the Football Zombie's own head; shows once berserk, the reading face is anim_head_look) |
| Newspaper knife 0x31 | show Zombie_knife (Unnamed's track, reanim/knife.png) |
| Newspaper Almanac paper 0x2A | Zombie_paper_paper -> images/SelectorScreen_AlmanacHighlight |
| Screen Door Tall-nut 6 | anim_screendoor -> reanim/Tallnut_cracked2 |
| Football green 0x1A | zombie_football_{helmet, leftarm_hand, leftleg_lower, rightleg_lower, rightarm_hand, upperbody, upperbody2, upperbody3} -> images/green_football_*; helmet damage 1/2 -> green_football_helmet2/3 |
| Football gold 0x102 | anim_head1 -> reanim/coin_gold_dollar |
| Dancer trophy 9 | anim_head1 -> images/trophy; hide anim_hair, anim_head2 |
| Dancer moonwalker 10 | anim_head1 -> reanim/Zombie_paper_madhead; hide anim_hair |
| Dancer random summoner 0x104 | white filter |

If one image of a form is missing, the whole look is dropped (base zombie drawn); the form keeps its behaviour.

## Text (`strings/en-corrections-night-zombies.txt`)

Code wins over the Almanac: the football-head and knife Newspapers, the green and gold Footballs and the white random
summoner roll in world 2 but are missing from Unnamed's Almanac; the Screen Door's reflected shots hit plants; the
knife kills at the first berserk chew; the gold Football crushes plants.

## Rulings (port choices: what, why, cost if wrong)

- The 0x104 Dancer's random followers rise from the ground like grave zombies at the slot's column and then act as
  their own type; the exe makes them dance in step (UpdateZombieBackupDancer with per-type animations, hooks 589-593,
  table 0xC0418A). Why: GOTY's per-type updates fight a dancer phase on non-dancer types. Cost: a 5 % form's
  followers do not dance in step.
- The knife's kill sets plant HP to 0 and calls Plant::Die with the gulp sound and the plants-eaten count; the exe
  calls its damage routine 0x950000(plant, HP + 1, 1). Why: same end, no new damage path. Cost: a 0x950000 side
  effect, if it has one, is missing.
- `elite.mode` (0x800258) is fixed at 0, as for Day. Branches above player level 60/70 (I, Zombie football helmet,
  black Football armour, Gatling-head green Football) are not ported (world 7). Plan 9 R4 (`SOURCES-elite-gaps.md`,
  feature `eliteGaps`) ports them, the Newspaper's I, Zombie roll and its profile > 70 branch, and corrects two readings
  here: hook 640 runs in Zombie::Animate's walking branch (not at the chew), and its +1000 body applies at every profile
  level (`greenChewBonusMaxPlayerLevel` 60 is wrong; kept for packs without `eliteGaps`).
- A reflected shot hits plants through GOTY's FindCollisionTargetPlant; hook 374's exclusions for zombie shots
  (hiding Scaredy-shroom, Starfruit, Flower Pot, some +80 seeds) are not ported. Cost: a reflected pea can hit a
  hiding Scaredy-shroom.
- A reflected shot skips all of Projectile::Die once; the exe still ends the shot's attachment there for most types.
  Cost: a reflected Snow Pea keeps its trail.
- Butter: only the berserk Newspaper's 500 cs is ported; hook 720's "add 400 / Kernel tiers" for others belongs to the
  Kernel-pult (world 5).
- Dev only: a type given to -pvzu-force-variant / -pvzu-force-subvariant rolls nothing, so forced runs draw fewer
  Rand values than natural ones.
