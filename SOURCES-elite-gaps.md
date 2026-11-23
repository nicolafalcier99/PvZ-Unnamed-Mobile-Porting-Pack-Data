# Sources: Football gaps and elite-option-0 branches (`data/rules-elite-gaps.json`)

Plan 9 topic R4. Evidence: the research notes (r4-football) (radare2 `pd` and python byte scans
of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe was never run). Code wins over the Almanac and the video. App code:
`app/src/Mod/Unnamed/EliteGaps.*` (rules), `app/src/Mod/Engine/EliteGaps.*` (engine sites), feature `eliteGaps` in
`mod.json`. A missing key plays that rule as before (vanilla or the earlier port). The Night (`nightZombies.football.*`
ranges, green age / drop level / +1000) and World-7 (`world7Zombies.football.blackExtraHit`, `above60.level`) keys are
reused, not repeated.

## Keys

| key | Unnamed | without | study | exe evidence |
|---|---|---|---|---|
| black.walkMul / eatMul | 0.85 / 1.2 | x1 | 1 | hook 705 0x5317c4 -> 0xc05900 -> 0x818063 -> 0x95a120 -> 0x818069: type 7 and +0x14c == 0x19: `fild ebp`, `cmp byte [esi+0x51],0` (mIsEating), `fmul` 0x3f59999a / 0x3f99999a, `fistp` (nearest). Almanac -40 % / +25 %: code wins |
| black.zeroBecomes | 1 | 0 | 1 | 0x8180b7 `test ebp,ebp; jne; inc ebp` (skipped when the per-frame flag 0xc01c3d is set; not ported, always 0) |
| black.smallHitBelow / smallHitRoll | 5 / 5 | no roll | 1 | 0xc00710 `cmp ebp,5; jge`, `Rand(5)`, `cmp ebp,eax; jg`, else `ebp = 0` |
| black.refusesFreeze | 1 | 0 | 2 | CanBeFrozen hook 712 -> 0x7cd050 -> 0x81803b `cmp [ecx+0x14c],0x19` -> 0x531a7b (`xor al,al; ret`) |
| football.goldDrawsBlackRoll | 1 | 0 | 3 | 0xc12500 -> 0xc12535 `test bl,bl` with `bl = 3` (profile > 60) -> 0x9dd406 Rand(3) -> 0x9dd419 -> 0x9dd423 (gold + black 900 / 2200) |
| football.graveSkipsGold | 1 | 0 | 3 | [0x9dd48e] = 1 around SpawnZombiesFromGraves at the gold death (0xc0353d..0xc0355e): 0x9dd346 (no Rand(13) for plain), 0xc12bc2 (green: gold refused) |
| green.walkEvent | 1 | 0 | 4 | hook 640 sits in Zombie::Animate 0x52bca0 (not the chew): `cmp byte [edi+0x51],0; je 0x52be4e` -> 0xc12b80 -> 0xc131c0 -> 0xc12caa; both paths `call 0x52f050` (UpdateAnimSpeed) |
| green.gatlingAbovePlayerLevel | 60 | never | 4 | 0xc13195 `cmp esi,0x3c; jle 0xc12e02` (esi = PlayerInfo+0x24); `cmp esi,0x46; jg` skips DropHelm (0xc13186) |
| gatling.headX / headY / headRot / headSx / headSy | 83 / 0 / 0.2 / -1 / 1 | - | 4 | 0xc12dc0..0xc12de0: floats 0xc12e1e, 0xc12e1a, 0x67953c, 0x679378, fld1 -> 0x5125d0 (TodScaleRotateTransformMatrix) on the AttachReanim offset of REANIM_GATLINGPEA (type 0x50) on `anim_head1` |
| gatling.startCounter | 150 | - | 4 | 0xc12dee `mov [eax+0x68],0x96`; 0xc12df8 `+0x134 = 0x6b` |
| gatling.extraShots | [1,20,39,64,83,102,121,146] | none | 4 | hook 575 0x527769 -> 0xc12e80: type 7 -> these values `je 0x52783d` (fire), then the vanilla 0x12/0x23/0x33/0x44 |
| gatling.spreads | 0 | 1 | 4 | 0xc12f00 / 0xc12f16 `cmp [ebx+0x24],7; je 0x795e1f` (after the hypnotised setup 0x795c91) |
| gatling.skipPhase | 50 | - | 4 | hook 628 0x52b25f -> 0xc12e40 (type 7 and 0x6b, or type 0x1d) -> 0xc03f70 `cmp [esi+0x28],0x32; je` (PHASE_DANCER_RISING) |
| newspaper.above70Level | 70 | - | 5 | 0xc05791 `cmp [ebx+0x24],0x46; setg cl`, `jle 0xc05825` |
| newspaper.paperFromCounter / paperFullCounter / paperFullHp / paperDivisor | 1200 / 30000 / 3000 / 10 | - | 5 | 0xc057b2 -> 0xc05f00 (Board+0x556c = mEffectCounter) -> 0xc057bb `cmp eax,0x4b0; jle`, `cmp eax,0x7530; jl`, `mov eax,0xbb8` / `idiv 10`, `mov [edi+0xdc],eax` |
| newspaper.rollsInIZombie | 1 | 0 | 6 | hook 502 chain 0x7a19fc -> 0xc109a2 -> 0xc05770: only option 1 skips (0x7a1a0b); no IsIZombieLevel test before Rand(5) |
| helm.iZombieRoll / hp | 3 / 2800 | - | 6 | 0xc109bf: IsIZombieLevel (0x4537d0) -> 0xc13610 `jne 0xc13640` -> 0xc109cf `Rand(3)`, `test al,al; jne` -> helm type 3, +0xd0 = 0xaf0, `anim_football` shown (0x473a40) |
| helm.boardLevelAbove / waveAbove | 70 / 25 | - | 6 | 0xc13621 `cmp [eax+0x557c],0x19; jle`, `cmp [eax+0x5550],0x46; jg 0xc109e1` (board, not profile) |
| iZombieNormal.coinRoll / coinRollHelm / coinMaxRollPlusOne | 7 / 30 / 3 | - | 6 | 0xc111d5 `ebx = 1; eax = 7`, `cmp [edi+0xc4],3; jne`, `add eax,0x17`; 0xc11171 `Rand; add eax,ebx; cmp eax,4; jl 0xc1118f` (0x105) |

Helmet look (no keys): hook 519 (0x524169 -> 0xc10806) hides `anim_football` in SetupReanimLayers; hook 699
(0xc108c0) puts the football helmet damage images on `anim_football` for a non-Football; hook 697 (0xc10940) takes
DropHelm's particle position from `anim_football` and hides it. Unnamed's `assets/compiled/reanim/Zombie.reanim.compiled`
(43 tracks, 1 Unnamed-only: `anim_football`) is merged like `Zombie_paper` (needs the 32-bit loader of the Night port).

## Rulings

- The black armour floor-1 always applies: the per-frame flag 0xc01c3d (a zombie in mod phase 0x102, hook 92) is not
  ported. Cost: a 0-damage hit on a black Football during that phase deals 1.
- The black Football still chills: the exe's chill cave 0x817ffe is unreachable (no jump to it). Butter: no rule.
- A Gatling-head Football keeps the head reanim when it loses its head (DropHead's vanilla ZomBotany test), as the exe.
- The Night port's chew-site helmet drop (hook 640 read as the bite) is off while this feature is on; the walking event
  replaces it and its +1000 now applies at every profile level (`greenChewBonusMaxPlayerLevel` is not read here).
- The Dancer's football helmet has HP but no picture (Unnamed's Zombie_dancer has no `anim_football`), as the exe.
- 0xc014c2 (flag 3: black Footballs placed by a script) is not ported (its level/mode was not traced).

## Seen on the Mac (2026-11-23)

Runs `pvz-portable -pvzu-mode unnamed -pvzu-pack <clone> -pvzu-width 1300 -pvzu-hidden` (`SDL_AUDIO_DRIVER=dummy`):
- 1-4, profile 65, forced green: at age 800 `gaps green-walk helm-drop=1 gatling=1 body=1300`; screenshot: Gatling Pea
  heads on both Footballs firing dense pea streams (no spread); after save + Continue the 0x6b Football keeps its head
  and fires.
- 1-4, profile 65, forced black: peas `hit 20 -> 17` walking, `20 -> 24` eating.
- 1-4, profile 65, 120 natural Footballs: 22 black, 3 black+gold (900 / 2200), 2 gold, 27 green, 3 green+gold, 63 plain.
- I, Zombie (mode 61), 30 Normals + 30 Newspapers: 12 + 9 football helmets (2800, drawn on both), 10 silver coins,
  Newspapers 9 football head / 8 knife / 13 plain. Screenshot: red helmets on Normals and Newspapers.
- 1-4, profile 73, 12 Newspapers: all football-headed (2 Almanac + head, 1 knife + head), paper 150 -> 283 with the
  board's effect counter.
- 1-4, profile 41: Normal/Cone/Bucket/Newspaper/Door/Flag drawn without a stray helmet; vanilla mode: no `gaps` lines,
  GOTY Zombie.reanim, Football 270 + 1400.

## Almanac text (`strings/en-corrections-world7.txt`)

FOOTBALL_ZOMBIE_DESCRIPTION: green "after 8 s" (walking, not the first bite) and the World-7 Gatling head; black P=1/4
(3/13 + 1/52 gold-black) with -15 % / +20 % and no freeze (code wins over the mod's -40 % / +25 %). Shortened so it
fits the box (the previous text ran two lines past it at 1300 px width; seen on the Mac).
