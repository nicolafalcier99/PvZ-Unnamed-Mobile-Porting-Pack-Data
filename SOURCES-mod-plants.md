# Sources: mod-only plants (mod-plants.json, rules-mod-plants.json, feature `modPlants`)

Plan 8 part 1 (infrastructure of Unnamed's 26 mod-only plants, seeds 0x50..0x7f). Study (source of truth):
the research notes (w6-w7-and-new-content) sections 1.3, 5, 5.1, 7.2, 7.3. Exe =
the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only (study export the research notes (hooks2) through
the research notes (w67_fn), the decoded table the research notes (unnamed-tables) row `extended_plants_0x860000`, and one static
`r2 pd` of 0x959de0 / 0x7a3ce2; nothing run). Code: `app/src/Mod/Unnamed/ModPlants.*` (pure rules and the table),
`app/src/Mod/Engine/ModPlants.*` (engine side), `app/src/Mod/Engine/ModPlantSites.*` (empty per-plant hooks for part 2),
tests `app/tests/test_mod_plants.cpp` (its pack test compares both JSON files with the study's table, transcribed
separately in the test).

Behaviour of each plant is **part 2**: in part 1 every mod plant is planted as its base plant (seed - 0x50) and behaves
as that plant (including the Unnamed rules of the base).

## mod-plants.json (one row per plant, keyed by decimal seed; written by `tools/make_mod_plants.py`)

| Field | Meaning | Evidence | Conf |
|---|---|---|---|
| key | seed 0x50 + table index (stride 0x100 from 0x860000). 0x54 has an empty row (no name, cost 0) and is left out; seeds with no row (0x5a, 0x5e..0x66, ...) are not plants | table bytes; GetCost hook 364 / GetRefreshTime 368 index the table by `(seed - 0x50) * 0x100` | H |
| `base` | the vanilla plant at `seed - 0x50`: its reanim (table +0x08 equals the base's) is the mod plant's art, and in part 1 its behaviour | table +0x08 reanim and +0x0c packet index rows; no new plant art in resources.xml (study 5) | H |
| `name` `{en, zh}` | `zh` = table +0x34 (GBK), printed literally with "%s" (hook 365), not a `[KEY]`. `en` = our translation (study 5.1) | hook 365 | H |
| `tooltip` `{en, zh}` | `zh` = table +0x50 (hook 367); `en` ours. Loaded Cannon (0x7f) has none in the exe | hook 367 | H |
| `seedCost` | table +0x10 | hook 364 | H |
| `refreshTime` | table +0x14, cs | hook 368 | H |
| `launchRate`, `subclass` | table +0x1c / +0x18 in the 1051 PlantDefinition order. Kept for part 2; part 1 plants the base with the base's values (Sniper's 0 and normal subclass would stop the base Gatling Pea firing) | field order only | M |
| `tint` | table +0x24..+0x30, RGBA: the plant's reanim colour override. `0x7a3d0e`: `edx = idx * 0x100 + 0x860024`, four dwords copied into the body reanim's colour (Reanimation+0x48) in Plant::Draw's colour code (hook 313). Shadow plants (at least 0x50, 0x51, 0x58, 0x62, 0x63, 0x67, 0x69, 0x6d, 0x70 via 0x7b0660 / 0xc00dc0; the chain goes on in 0xc06130, not read) take another branch first (shadow state, Starfruit+80 flicker `Rand(6)`): part 2 | static asm of 0x7a3cb1 / 0x7a3d0e | H (tint), M (shadow branch) |

## rules-mod-plants.json

| Key | Value | Evidence | Conf |
|---|---|---|---|
| `modPlants.sproutBankRoll` | 48 | hook 67 (0x7a071a) on the seed-bank planting call of Board::MouseDownWithPlant: cursor seed 0x33 (Sprout), or 0x30 (Imitater) copying 0x33 -> the cursor plants an Imitater copying `Rand(0x30)` (Peashooter..Cob Cannon) | H |
| `modPlants.sproutCoinRoll` | 53 | hook 66 (0x957500) on the dropped-packet (usable coin) planting call: seed 0x33 or 0x30 -> an Imitater copying `Rand(0x35)` (every seed 0..52, so also the Imitater itself: it then morphs into another Imitater forever, as in the exe; 0x95750b `mov eax,0x35; call Rand` re-read 2026-11-23). **Port fix (not exe)**: at the morph an Imitater copying an Imitater re-picks once with `Rand(52)`, skipping 48, so it ends as a plant | H |
| `modPlants.packetCell` | 12 | hook 465 (0xc10a40): seeds 0x50..0x7f draw packet back cell 0xc (Gatling Pea cell 1) of Unnamed's 13-cell seeds.png (red back). The engine cuts that cell from `assets/images/seeds.png` itself (the overlay skips that sheet: its 13 cells do not fit the GOTY layout) | H |

## How they are obtained (no data; engine rules)

- **CARD** (exe flag 0x8001a0, typed `CARD`, hook 138; row of the cheat panel hook 764): on the phone a setting,
  `"card": true` in `pvzu-settings.json` (written only when on), and the dev flag `-pvzu-card`. A menu toggle comes later.
- **HasSeedType** (hook 256, 0x7a055c): with CARD on, seeds >= 0x31 answer "Imitater bought" (`PlayerInfo+0x1e0`). The
  exe also answers yes for 53..79 and the empty mod slots, which its chooser never lists (hooks 424 / 431 jump 0x35 ->
  0x50); the port answers no for them. With CARD off a mod seed is never available.
- **Chooser** (hooks 148, 423, 424, 431): CARD lists 0..0x34 then 0x50..0x7f. The exe stacks the extra rows under the
  vanilla grid (51 x 71 px, its 1067-wide layout); the port shows the 30 extra seeds (49..52, then the 26 plants) in a
  second panel ("MORE PLANTS") right of the vanilla one, 8 columns, the vanilla pitch.

## Port rulings (not in the exe)

- A planted mod plant is an engine Plant of its base seed with `mPvzu.modSeed` = its mod seed (saved in the plant's
  PVZU TLV field, 4 more bytes). Packets, the cursor and the chooser keep the mod seed like the exe.
- Placement: the base's CanPlantAt rules, except bases that vanilla plants only as an upgrade (Gatling Pea, Gloom-shroom,
  Cattail, Cob Cannon), which go on a free square like a Peashooter: the exe's CanPlantAt has no upgrade test for
  0x78 / 0x7a / 0x7b / 0x7f (IsUpgrade compares the exact vanilla seeds). The exe's own placement hooks for some mod
  plants (39, 40, 41, 47, 50-52, 62-65) are part 2.
- The modern HUD card (seed panel) has no packet back to recolour: there the plant's tint alone marks a mod plant.

---

# Behaviour rules (Plan 8 part 2)

# Sources for data/rules-mod-plants.json

Every key below comes from Unnamed 1.3beta2 `PlantsVsZombies.exe` code, read statically (radare2 `pD`, Python byte
reads, the Ghidra export the research notes (hooks2); nothing run) for
the research notes (mod-plants-behaviour), which has the rules in prose with confidence per rule.
Addresses are the exe's; hook numbers are rows of the research notes (hook-triage). Keys are written without the `modPlants.`
prefix. Booleans are 0/1; floats are the exe's float constants. App code: `app/src/Mod/Unnamed/ModPlantRules.*`
(pure rules, not yet wired into the engine). Mod plants do not exist in vanilla: while the `modPlants` feature (owned
by the mod-plant infrastructure) is off, or a key is missing, every rule has no effect.

Two keys change vanilla plants in Unnamed mode too: `strongCoffee.anyPlantOk` (the 0x40e137 patch also lets the vanilla
Coffee Bean go on an awake plant) and `coffeeHeal.*` (hook 362 heals for the vanilla Coffee Bean as well).

## Shadow state, Shadow Peashooter, Primal Sunflower, Toxic Shadow-shroom, Moonflower, Dusk-pult (group A)

- shadow.on / list: 0x7b0660 `cmp eax,0x50/0x58/0x62/0x63/0x69` -> 0xc00dc0 `0x70/0x67/0x6d/0x51` -> 0xc06130 `0x56`
- shadow.skipModeA/B 43/50: 0x7b06c5 `cmp edx,0x2b; je`, 0x7b06ce `cmp edx,0x32; je`
- shadow.rangeCells 1: 0x7b0706..0x7b071e `cmp edx,1; jg / cmp edx,-1; jl` on row and column deltas
- shadow.moonflowerPoint 1: 0x7b0738 `add ebx,1`; shadowedMoonflowerBonus 1: 0xc12bfa `cmp [ecx+0xcc],1; add ebx,1`
- shadow.threshold*: 0x7b074b `mov eax,1` (default), 0xc11460..0xc11492 -> 0x7b0756 `mov eax,3` (0x56, 0x6d, 0x69),
  0xc1147e `mov eax,2` (0x67); 0x7b075b `cmp ebx,eax; setge al`
- shadow.tintR/G/B/A 80/80/240/255: 0x7a3ce8..0x7a3cfc `mov [eax],0x50; [eax+4],0x50; [eax+8],0xf0; [eax+0xc],0xff`
- shadowPeashooter.projectileType 1, originDx 66, originDy 10, potDy -5: 0x7b00e0..0x7b0114 `add esi,0xa`, `sub
  esi,5` after GetFlowerPotAt, `push 1` (type), `add [esp],0x42`, call AddProjectile 0x40d620
- shadowPeashooter.beamDamage 30, beamDamageFlags 6: 0x7a915c `cmp [ebp+0x24],0x50` -> 0x7a4eef `mov edi,0x1e; mov
  [esp+0x44],6` inside DoRowAreaDamage (hook 274); beam call 0x7b0077 `push 2; push edi; call 0x45ed00`
- shadowPeashooter.beamPuffBase 7, beamPuffStepPx 80: 0x7b004f `mov ebx,7; sub ebx,[edi+0x1c]`, 0x7b0063 `push 0x50; fiadd`
- modSun.timerJitter 150: 0x7b02b2 `lea esi,[eax-0x96]`, `Rand(rate - (rate-150) + 1)`
- primalSunflower.sunCoin 4 / extraCoin 5 / mainMotion 2 / extraMotion 3: 0x7b02db `push 2; push 4`, 0x7b02ef `push
  3; push 5` (AddCoin 0x40cb10)
- primalSunflower.shadowSunCoin 6, packetRoll 25, packetBelow 5, packetCoin 16, packetSeeds: 0xc13207 `mov eax,0x19;
  call Rand`, 0xc13211 `push 2; push 6`, 0xc13217 `cmp eax,4; jg`, 0xc13226 `mov [esp],0x10`, 0xc13220 `mov bl,[eax+
  0xc13254]` (bytes 01 09 29 51 59), 0xc13246 `mov [eax+0x68],ebx`
- moonflower.sunCoin 5 / shadowSunCoin 4 / coinMotion 3: 0x7b030a `mov esi,5`, 0x7b0318 `mov esi,4` when `[edi+0xcc]
  == 1`, 0x7b031d `push 3; push esi`
- toxicShadowShroom.normalKind 1 / shadowKind 2 / poisonTimer 524287: 0x7a65b0..0x7a65e0 `cmp [ebp+0x140],2; je`,
  `mov ax,1` / `mov ax,2` when `[esi+0xcc]==1`, `mov [ebp+0x148],0x7ffff`; trigger EatPlant hook 688 0x52fd38
  (after `cmp [esi+0x40],0; jg`) -> 0x79b081 `jmp 0x7a65b0`
- toxicShadowShroom.poisonPeriod 64 / poisonDamage 20 / shadowFlashCs 25: 0x7a677b `test ebx,0x3f`, 0x7a6791 `push
  0x14; mov eax,0; call 0x5317c0` (kind 1), 0x7a67a2 `mov [esi+0x54],0x19; push 0; push 0x14; call 0x5312d0` (kind
  2), 0x7a67b3 `add ebx,-1`, 0x7a67c5 kind = 0; boss skip 0x7a674d `call 0x7aa320`
- dodgeZombieShots.on: hook 374 0xc02c55..0xc02c6a `cmp eax,0x58/0x59/0x6d; je 0x46cad0`
- repeaterPoison.damagePerTick 1: 0xc10ce6..0xc10d10 `cmp [eax+8],0; jle; dec [eax+8]; mov eax,0; push 1; call
  0x5317c0`
- duskPult.projectileType 33: 0x797915 `jmp 0x91040b` -> 0x91040b `cmp [ebp+0x24],0x70; mov [eax+0x5c],0x21`
- duskPult.shadowRows 1 / aboveDy -80 / aboveDz 80: 0x7a50b1..0x7a5127 (FindTargetZombie + Fire for row-1 and
  row+1 when `[edi+0xcc]==1`), 0x7a50ef `fld [0x67a0b8]` (= 80.0) `fsubr [eax+0x34]` / `fadd [eax+0x38]`; hook 279
  0x7a515c..0x7a51a5
- duskPult.splashRows 1 / splashBackPx 152 / splashWidenPx 256: 0x9104f1..0x9104ff `dec ecx` / `inc ecx; inc ecx`
  row bounds, 0x910516 `sub [ecx],0x98`, 0x910523 `add [ecx+8],0x100`, 0x91051c y 0, 0x91052a h 0x258; skip
  hypnotised 0x9104e8 `cmp byte [ebx+0xb8],1`
- duskPult.splashDamage 13 / splashFlags 1 / splashPushPx 5 / splashWeakenCs 200: 0x91054d `push 0xd`, 0xc06162
  `mov eax,1` -> 0x910554 `call 0x5317c0`; 0xc06153 `fadd [0xc0616c]` (= 5.0) on `[esi+0x2c]`; 0xc0615c `add word
  [esi+0x1a],0xc8`

## Element-shroom, Prism-shroom, Dream Starfruit / star kinds, Spirit-tail, Mystic-Ice Shooter (group B)

- elementShroom.firstElementCs 200 / elementPeriodCs 800: 0x7b1465 `cmp word [edi+0xce],0; jle; mov esi,0x320 | 0xc8; mov [edi+0x54],esi`
- elementShroom.shootingCounter 200: hook 281 0x7a8fc0 `mov [esi+0x90],200` (decompile)
- elementShroom.pulseCounters 126/98/70: 0x7b177d `cmp eax,0x7e / 0x62 / 0x46` then `call 0x45ed00`
- elementShroom.puffCounters 136/108/80: 0x7b170d `cmp eax,0x88 / 0x6c / 0x50` then `call 0x45eea0` (effect 0x3c)
- elementShroom.pulseDamage 16: 0x7a9088 `mov edi,0x10` (after hook 274 0x7a4ee0 `mov edi,0x14`)
- elementShroom.wideDamage 12: 0x7a9093 `mov edi,0xc` (state 3)
- elementShroom.fireDamage 56: 0x7a90a6 `mov edi,0x38` (state 1)
- elementShroom.wideRowReach 2: 0x7a929d / 0x7a922a `cmp eax,-2; jl; cmp eax,2; jle`
- elementShroom.wideRectHalf 160 / wideRectSize 400: 0x7a91b4 `sub edx,0xa0`, 0x7a91ba `mov esi,0x190`
- elementShroom.fireStripRoll 5: 0xc05601 `mov eax,5; call Rand; test eax,eax` -> 0xc05613 DropHelm 0x530e30 / 0x530a00
- elementShroom.iceRoll 18: 0x7a90eb `mov eax,0x12; call Rand; cmp eax,1; jg; je`
- elementShroom.iceDamageFlags 6: 0x7a90e3 `mov [esp+0x54],6`
- elementShroom.iceFreezeCs 150: 0x7a9110 `mov [ebx+0xb4],0x96` after `call 0x5323c0`, `mov edi,0`
- elementShroom.icePushPx 20 / icePushMaxX 800: 0x7a9137 `cmp eax,0x320; jge; add eax,0x14`; types 0x14/0x19 excluded
- elementShroom.healPerPulse 30 / healMaxCap 3000: 0x7b17a2 `add eax,0x1e; cmp eax,0xbb8`, 0x7b17b7 `add ecx,0x1e`
- elementShroom.noPlanternBoost 1: cave 0x651717 `cmp [esi+0x24],0x7a; je 0x6516ed` (reload = launch rate, not halved)
- prismShroom.clickToFire: hook 339 0x7a6000 -> 0x7a8f15 `cmp [esi+0x24],0x5d` -> 0x7a6014; hover hook 54 0x7a6127
- prismShroom.shotCost 50: 0x7a6032 `push 0x32; call 0x41bab0` (CanTakeSunMoney), 0x7a60d1 `sub [ecx+0x5560],0x32`
- prismShroom.shootingCounter 25: 0x7a60c4 `mov [esi+0x90],0x19`
- prismShroom.outOfSunFlashCs 70: 0x7a606f `mov [ecx+0x5578],0x46`
- prismShroom.projectileType 22: 0x7a5274 `cmp eax,0x5d; jne; mov [esp+0x10],0x16`
- prismShroom.damageBase 300 / damageSunCap 1000 / damageSunDivisor 4: 0x7978f0 `mov edx,[board+0x5560]; cmp edx,0x3e8; jl; mov edx,0x3e8; sar edx,2; add edx,0x12c; mov [proj+0x80],edx`; 0x7b08fb type 0x16 damage = `[eax+0x80]`
- dreamStarfruit.colours 5 / colourRerollMask 12: 0x959df9 `test ecx,0xc; jne; mov eax,5; call Rand; mov [esi+0xcd],eax`
- dreamStarfruit.palette: 0x959ccc.. `mov ecx,0x33a1c9 / 0xff0000 / 0xc000ff / 0x778899 / 0xff00`
- dreamStarfruit.damageBonus 15/20/15/25/15: 0x959cfc.. `mov ecx,0xf / 0x14 / 0xf / 0x19 / 0xf`; 0x959fe6 `add [esp],ecx`
- dreamStarfruit.shadowReturnCs 30: 0xc00e8d `cmp byte [esi+0xcc],1; jne; mov [edi+0x64],0x1e`; homing 0xc00ec0 `cmp al,1 ... mov [esi+0x58],9`
- dreamStarfruit.shadowAlwaysTargets 1: hook 284 0xc00e40 `cmp [ecx+0x24],0x6d; cmp byte [ecx+0xcc],1; je 0x45f6d1 (mov al,1)`
- dreamStarfruit.redPierceHits 5 / greyPierceHits 3: 0x959f4c `cmp [esi+0x80],2; cmp [esi+0x18],5; jge die; inc`, 0x959f89 `cmp ..,4; cmp [esi+0x18],3`.
  The values are the exe's constants; its counter starts at 1 (mVisible), so a red star lives through 4 hits and a grey
  one through 2 (Plan 9 R1 fixed a one-too-many). Blue (kind 1) and kinds > 5 take the ordinary 254-hit path. Like
  ordinary stars, every Die inside CheckForCollision counts (field edges too), and a homing kind star goes back to
  motion 7 with no target when it lives (0xc00f10).
- dreamStarfruit.blueFreezeRoll 7: 0x959ff3 `call 0x531a10 (CanBeFrozen)`, 0x95a002 `mov eax,7; call Rand; test; jne` -> 0xc059d0 HitIceTrap / ApplyChill
- dreamStarfruit.redHelmRoll 7 / redHelmMaxHp 120000: 0x95a028 `mov eax,7; call Rand` -> 0xc02d50 `test; jne; cmp [esi+0xcc],0x1d4c0; jg` -> 0x95a03a `call 0x530e30`
- dreamStarfruit.purpleHypnoRoll 10 / IZombie 20: 0xc100c0 `call 0x4537d0; je; mov eax,0x14 | mov eax,0xa` -> 0x95a06a Rand -> 0x52fa60
- dreamStarfruit.greenBlowRoll 7 / IZombie 21: 0xc10100 `mov eax,0x15 | mov eax,7` -> 0x95a0c1 Rand -> `mov byte [esi+0xb9],1`
- dreamStarfruit.effectMaxHp 15000: 0x95a8b5 / 0x95a8e5 `cmp [esi+0xcc],0x3a98; jge skip` (and `fld [esi+0x11c]; fld1; fcompp` scale <= 1)
- dreamStarfruit.greyWeakenCs 400: 0x95a095 `add word [esi+0x1a],0x190`
- dreamStarfruit.weakenDamageMult 2: 0x95a12b `jle; shl ebp,1` (reached from TakeDamage 0x818063 after `cmp word [esi+0x1a],0` 0xc05aae)
- dreamStarfruit.weakenFootballRoll 2: 0xc05a87 `cmp word [esi+0x1a],0; jle; mov eax,2; call Rand; test al,al; je normal; sar ebp,2`
- dreamStarfruit.weakenTintGrey 48: 0x95a365 `call 0x52ae40` (mFromWave not -2 / -3) -> 0x95a370 `cmp word [esi+0x1a],0;
  jle` -> 0x95a377 `mov edx,0x30; mov ecx,0x30; mov eax,0x30; jmp 0x52d2d9` (colour and additive, 0x52d382 additive on).
  It sits in the colour chain after 0xc10d30 (Repeater poison green wins) and before mind control / chill. The
  0x95a160 block (`cmp word [eax+0x1a]` -> 0x45 grey) is not reached: no jump or call leads to it.
- spiritTail.roll 36 / projectileTypes: 0xc106ba `mov eax,0x24; call Rand; cmp eax,0x21; jge ok; cmp eax,0x16; je ok; cmp eax,9; je again; cmp eax,6; je again; cmp eax,0xd; jl ok; jmp again`
- spiritTail.bigCabbageRoll 2 / starKindRoll 6 / prismDamage 475: 0xc10609 `cmp [ecx+0x5c],2; Rand(2); sete [ecx+0x80]`; `cmp ..,7; Rand(6); mov [ebx+0x80],eax`; `cmp ..,0x16; mov [ecx+0x80],0x1db`
- spiritTail.motion 9: 0x467393 `mov [ecx+0x58],9` (Cattail branch, after 0xc10668 `jmp 0x467386`)
- mysticIce.shotOffsetX 69 / shotOffsetY 10 / shotType 1: 0xc04761 `push 1; push row; push 0; push y; add [esp],0xa; push x; add [esp],0x45; call 0x40d620`
- mysticIce.shotMotion 7 / shotVelX 3.33 / shotRangeFlags 1: 0xc0477e `mov [eax+0x58],7; mov [eax+0x3c],0x40551eb8; mov [eax+0x74],1`
- mysticIce.velYRoll 2000 / velYDivisor 650 / velYOffset 1.53846: 0xc04799 `mov eax,0x7d0; call Rand; fild; fidiv [0xc0486c]=650; fsub [0xc04870]=0x3fc4ec42; fstp [esi+0x40]`
- mysticIce.convertPeas / convertTo 1: 0xc04d90 `cmp [esi+0x78],-1; jne; cmp byte [esi+0x50],1; je` -> 0xc047d4 `cmp [esi+0x5c],0; jne; mov [esi+0x5c],1`
- mysticIce.lifeIsLaunchRate / deathParticle 71: 0xc047e7 `dec [edi+0x5c]; cmp ..,0; jg; mov byte [edi+0x141],1; push 0x47; ... call 0x518a70`
- mysticIce.upgradeFrom 0 / upgradeTo 5: 0xc04843 `cmp [esi+0x24],0; jne; mov byte [esi+0x141],1; push -1; push 5; ... call 0x40d120`
- zomboniImmune.elementAndMysticIce: 0x7b1812 `cmp eax,0x7a; je skip` / 0xc04e70 `cmp eax,0x55; je skip` (Zomboni freeze loop 0x795665)

## Sniper, Primal Repeater, Shrapnel Cherry, Loaded Cannon, Butter-pult, Bowling Wall-nut (group C)

- sniper.periodCs 500: 0x7b131a `mov dword [edi+0x54],0x1f4` when `[edi+0x54] <= 0` (countdown decremented at 0x46324c)
- sniper.warnAtCs 120: 0x7b1395 `cmp ebx,0x78` -> sound `mov esi,0x52; call 0x453630`
- sniper.fireAtCs 5 / damage 500: 0x7b13aa `cmp ebx,5`; 0x7b13b3 `push 0x1f4; xor eax,eax; call 0x5317c0` (TakeDamage)
- sniper.warnFoley 82 / fireFoley 55: 0x7b139e `mov eax,[esi]; mov esi,0x52; call 0x453630` (LawnApp::PlayFoley, at the
  warning) and 0x7b13c0 `mov eax,[esi]; mov esi,0x37; call 0x453630` (with the damage). No projectile, particle or
  reanim in 0x7b1300: the shot is these two sounds plus the target mark and head aim (rules-mod-visuals.json). The
  port's pea splat on the target is a port addition (a visible hit mark); its old FOLEY_SPLAT is replaced by 0x37.
- sniper.bossMaxHp 120000: 0x7aa320 `cmp dword [eax+0xcc],0x1d4c0; jg boss` (+ type 0x19, + 0x7aa130 Newspaper 0x7f)
- primalRepeater.shotRoll 10: 0xc10bad `mov eax,0xa; call 0x5af400; cmp eax,1; jg; add eax,0x22; mov [edi+0x5c],eax`
- primalRepeater.secondPea 1: hook 290 0x7a887f `cmp eax,0x57; je 0x45f96d` (Repeater's launch-counter-25 shot)
- primalRepeater.knockbackDamage 40 / poisonDamage 15: 0xc10db0 `cmp ebx,0x22 -> mov edx,0x28`; `cmp ebx,0x23 -> mov edx,0xf`
- primalRepeater.knockbackPx 30: 0xc10bfb `mov [0xc10ca7],0x1e; fld [esi+0x2c]; fiadd [0xc10ca7]; fstp [esi+0x2c]`
- primalRepeater.poisonAddCs 500: 0xc10c7e `call 0xc10e10; add dword [eax+8],0x1f4` (Board+0x5888 side table)
- primalRepeater shot art (engine, no key; Plan 9 L2, the research notes (l2-shot-art)): hook 405 0xc10b50
  `cmp eax,0x22; mov ecx,[0xc10f4b]` / `cmp eax,0x23; mov ecx,[0xc10f47]`; slots filled by the loader extension
  0xc10e50 `push "IMAGE_PROJECTILEPOISONPEA" ... mov [0xc10f47],eax`, `push "IMAGE_PROJECTILEPRIMITIVEPEA" ... mov
  [0xc10f4b],eax` = `assets/images/ProjectilePoisonPea.png` / `projectileprimitivepea.png` (mod resources.xml
  237-238), scale 1.0; colour hook 0x959e90 tints only stars of kind 1..5, so these and the dusk shard 0x21 (hook
  407: plain `IMAGE_REANIM_CABBAGEPULT_CABBAGE`) and the prism beam 0x16 (`IMAGE_POOLSPARKLY`) draw white
- shrapnelCherry.shards / straightSpeed 4 / diagonalSpeed 2.8: 0x794017..0x7941e8, 7x `call 0x40d620` type 7,
  `+0x58 = 7`, `+0x74 = 1`, vel words 0xc0800000 / 0x40800000 / 0x40333333 / 0xc0333333, `+0x84 = 2` (first) / 1
- shrapnelCherry.shardHitDamage 250: 0x79efa3 `mov eax,0; push 0xfa; call 0x5317c0` (kind 2 0x79ef88, kind 1 0x95a0da)
- shrapnelCherry.coreReplantAgeCs 1400 / replantColumnPx 80: 0x79f067 `cmp [esi+0x60],0x578`, `cmp [esi+0x84],2`,
  `mov bx,0x50; div bx`, `push -1; push 2; ... call 0x40d120` (AddPlant Cherry Bomb)
- shrapnelCherry.squishExplodes 1: hook 303 0x79436a `cmp eax,0x52; je 0x462bfd` (DoSpecial on squish)
- loadedCannon.selfArms 0: hook 309 0xc04b30 `cmp ecx,0x7f; call 0xc04b53` -> `mov eax,[edi+0x3c]; jmp 0x461069`
  (past the ARMING->LOADING block 0x461031)
- loadedCannon.loadable 1: hook 52 0xc04980 `cmp [ebx+0x24],0x7f; cmp [ebx+0x3c],0x23` -> 0xc11840 `cmp esi,0xf / 0x22`
  -> `mov eax,0xf`; mouse-down 0xc049c0 `cmp eax,0xf` -> 0xc11870 / 0xc11810 (`+0x138 = seed; +0x3c = 0x24`)
- loadedCannon.packetPenaltyCs 6000: 0xc04a71 `mov dword [eax+0x24],0xffffe890` before `call 0x488ec0`
- loadedCannon.kernelBurnCap 3000: hook 395 0xc1179f `cmp [ebp+0x88],0x22; mov [0xc117c0],0xbb8`; used by hook 794
  0xc11770 `cmp ebx,[0xc117c0]` (ApplyBurn), reset 0xc118c0
- loadedCannon.doomBurnCap 3600: 0xc11883 `mov [eax+0x24],0xf; mov [eax+0x138],0xf; mov [0xc117c0],0xe10; call 0x4666a0`
- loadedCannon.doomClearsGraves 1: hook 345 0xc118f5 `cmp [ebx+0x138],0xf; jne crater` -> IterateGridItems, type 1 -> 0x44d000
- butterPult.alwaysButter 1: hook 349 0x7a529b `cmp eax,0x72; mov [esp+0x10],0xc`; pose hook 283 0x7a53c0 -> 0x45f1ee
- butterPult.damageRangeFlags 13: hook 271 0x7a6233 `cmp eax,0x72; je 0x45ebb5` (Melon's return path, triage: 0xD)
- bowlingWallnut.rollsAnywhere 1: hook 307 0x7a4730 `cmp [edi+0x24],0x53; je 0x46325d` (call 0x462ce0 UpdateBowling);
  hook 370 0x7a47b7 (bowling attack rect)
- bowlingWallnut.notEaten 1: hook 676 chain 0x959423 `cmp ecx,0x53; je 0x52f693` (skip as eat target)
- bowlingWallnut.fixedAnimRate 1: hook 265 0x7a4770 `cmp [esi+0x24],0x53; je 0x45ddbe`; RandF 12..18 only for seeds 3/0x31
- (no key) UpdateBowling geometry, re-read 2026-11-23: the exe's 0x462ce0 is the vanilla one: row test
  `GridToPixelY(0, row)` (0x462d75 `mov eax,ebp; xor ecx,ecx; call 0x41c740`), bounce rows 0 / 4 (0x462dab `cmp ebp,4`,
  0x4630d9 `cmp ecx,4`), only the x limit is patched (0x462d48 `cmp eax,0x44c`). So in the exe a nut planted on roof
  columns 1..4 never reaches its hit test, a 6-row nut rolls into row 6, and hook 41 (0x7a5049) keeps it in its first
  square's flying slot. **Port fix (not exe)**: on the roof the nut follows the slope ((440 - x) / 4, = GridToPixelY's
  (5 - col) * 20 at each column), rows end at the board's last row, a nut whose middle left its square holds no square
  (floats 0x679388 = 12.0, 0x6795c4 = 18.0)

## Shared init / layers / boss class, Rewind Grass, Charmed Tall-nut, Hallucination-shroom, Magic Devourer, Holy-fire Pumpkin (group D)

- initAsBase: 0x7a3e06..0x7a3e1d `cmp eax,0x50; jl; cmp eax,0xff; jg; sub eax,0x50; jmp 0x45df58`
- bossClassMinMaxHp 120000: 0x7aa320 `cmp dword [eax+0xcc],0x1d4c0; jg` (+ type 0x19, + 0x7aa130)
- rewindGrass.blowDelayCs 50: 0x7b0a47 `mov dword [edi+0x50],0x32`
- rewindGrass.blowAnimRate 20.0: 0x7b0a5a `fld dword [0x679508]` (= 20.0f), `fstp [esi+8]`
- rewindGrass.maxX 800: 0x7b0afe `cmp dword [ebx+8],0x320; jge`
- rewindGrass.backX 800.0: 0xc054f1 `push 0x44480000` -> 0x7b0b3a `pop dword [ebx+0x2c]`
- rewindGrass.untouchable: 0x7c06dd (Squish), 0x7c06a1 (eat), 0x95007a (bite damage), 0x7c05e9 + 0x7c079f
  (projectiles), 0x7c0753 (Gargantuar), 0x7c0630 (Catapult target), 0x7c0800 (lobs)
- charmedTallnut.firstSummonHp 1500: 0x9500d0 `mov ebp,0x5dc; cdq; idiv ebp`
- charmedTallnut.summonStepHp 1200: 0x9500e1 `imul edi,eax,0x4b0; sub [esi+0x114],edi`
- charmedTallnut.summonTypes [5,7,23]: 0x9500f0 `mov eax,3; call Rand`; 0x9500fa `movzx eax,byte [eax+0x950103]`,
  bytes at 0x950103 = 05 07 17
- charmedTallnut.summonBodyHpMul 1.35: 0x950127 `push 0x3faccccd; fmul dword [esp]` on `fild [eax+0xc8]`
- charmedTallnut.riseCounterCs 50: 0x950147 `mov dword [esi+0x68],0x32`; 0xc00fe9 same
- charmedTallnut.shadowBiteMul 1.5: 0xc0105e `fmul dword [0xc010a0]` (= 0x3fc00000)
- charmedTallnut.shadowThreshold 2: 0xc11474 `cmp [edi+0x24],0x67; jne; mov eax,2`
- charmedTallnut.gargMinHpFrac 0.75: 0xc00f9f `fmul dword [0xc0101e]` (0x3f400000), `cmp [edi+0x40],eax; jl`
- charmedTallnut.gargPlantCostFrac 0.4: 0xc00ffe `fmul dword [0xc01022]` (0x3ecccccd), `sub [edi+0x40],eax`;
  Gargantuar = `push 0x17` 0xc00fb5, HP = `sar ebx,1` 0xc00fcc into +0xc8/+0xcc
- charmedTallnut.regenDelayCs 100 / regenHp 75: cave 0x651e00 `cmp [esi+0x58],0x64; jl`, 0x651e06
  `add [esi+0x40],0x4b`, cap 0x651e0e; entered for 0x67 at 0xc0223d `cmp byte [esi+0xcc],1; je 0x651dd8`
- charmedTallnut.biteBackDamage 8: 0xc021da `push 8; mov eax,0; call 0x5317c0` (Zombie::TakeDamage)
- charmedTallnut.biteBackCharmRoll 200: 0xc021e9 `mov eax,0xc8; call Rand; test eax,eax; jne` -> 0xc021fb
  `mov byte [edi+0xb8],1`
- charmedTallnut.instantCharmVariant 49: 0xc021ae..0xc021d2 phase 0x1f, `[edi+0xbc]==1`, `[edi+0x134]==0x31`
- charmedTallnut.actsAsTallnut: 0x959b60 (Pogo), 0x7b191a (squash), 0x9588f2 (CanTargetPlant), 0x957600 (cracked
  frames), 0x95756b (chew), 0x95763b / 0x95766b (replant), 0x95b259 (flying-eater list)
- hallucination.impMaxHp 270: 0x7a668a `mov [ebp+0xcc],0x10e`, 0x7a6694 cap of +0xc8; type 0x7a660b
  `mov [ebp+0x24],0x18`; armour zeroed 0x7a6612..0x7a6658; rects 0x7a6662..0x7a6680; reanim 0x7a66ac `push 0x39`;
  particle 0x7a66ee `mov eax,0x47; call 0x453c80`
- magicDevourer.fastCountdownFrom 10: 0x7b07de `cmp eax,0xa; jl; sub eax,1`
- magicDevourer.swallowAtCountdown 5: 0x7b07e9 `cmp eax,5; jne`
- magicDevourer.maxCol 8 / maxRow 5: 0x7b07f5 `cmp esi,8; ja`, 0x7b0804 `cmp ebx,5; ja`; bowling 0x7b0813 `call 0x453840`
- magicDevourer.cardCoinType 16 / cardCoinMotion 2: 0x7b0839 `push 2; push 0x10; push [esi+0xc]; push [esi+8];
  call 0x40cb10` (Board::AddCoin), 0x7b084e `mov [eax+0x68],edx` (= eaten mSeedType), 0x7b0852 `call 0x4679b0`
  (Plant::Die)
- holyFirePumpkin.actsAsPumpkin: hooks 39 0x95bed0, 41 0x7a505b, 50 0x95bf50, 51 0x95bf70, 63 0x95bf90, 64 0x95bfb0,
  74 0x95bf10, 269 0x95bf30 (`mov eax,0x1e`), 333 0x95beb0, 337 0x95bef0
- holyFirePumpkin.freezeGuard: 0x95bfd0 (any plant seed 0x6e with that row/col), used by 0x7b1806 in the freeze
  filter 0x7b1800 (called at 0x795665); blasts not shared: cave 0x6513b6 / 0x6519fd compare 0x1e only

## Fire-dragon Grass, Golden Sun-shroom, Strong Coffee Bean (+ Coffee heal), Leaf Shield, projectile damage, Boss Flower (group E)

- fireDragon.rowReach 1: 0x7b050b `cmp ecx,-1; jl` / 0x7b0514 `cmp ecx,1; jg` on zombieRow - plantRow
- fireDragon.rangeBackPx 40 / rangeFrontPx 240: 0x7b0532 `add ecx,0x28` + 0x7b0535 `cmp ecx,0x118; ja` (unsigned 0..280)
- fireDragon.bossMinCol 7: 0xc026c0 `cmp [esi+0x24],0x19` + 0xc026cd `cmp [edi+0x28],7; jl`
- fireDragon.damageFlags 9: 0x7b051d `push 9; call 0x531a80` (Zombie::EffectedByDamage)
- fireDragon.attackCs 70: 0x7b05a8 `mov [edi+0x54],0x46` (state -> 0xa at 0x7b05a1)
- fireDragon.hitAtCountdown 12: 0x7b0434 `cmp [edi+0x54],0xc; je`
- fireDragon.damageBase 100 / damageMaxHpDivisor 15 / damageCap 600: 0xc055b0 `push 0x64`, 0xc055b8 `fdiv [0xc055e1]`=15.0, 0xc055c4 `mov eax,0x258`
- fireDragon.flameBudget 1800: 0xc060fb `mov [0xc06112],0x708`; spend 0xc060b3..0xc060d1
- fireDragon.shadowPoison 400: 0xc060dc `cmp byte [edi+0xcc],1` + 0xc060e9 `add word [esi+0x1a],0x190`
- fireDragon.clearsChill 1: 0x7b054c..0x7b056f (`call 0x532350` RemoveIceTrap; `mov [esi+0xac],0; call 0x52f050`)
- fireDragon.zomboniFreezeImmune 1: 0x7b1817 `cmp eax,0x56; je 0x7b1844` (returns 0 = not frozen), caller 0x795665
- goldenSunShroom.burstCs 150: 0x7b0d0e `mov [edi+0x4c],0x96`, 0x7b0d15 `mov [edi+0xbc],0x96` (state 0x17 -> 2)
- goldenSunShroom.dropAtCs 125/75/25: 0x7b0d2d/0x7b0d32/0x7b0d37 `cmp ecx,0x7d/0x4b/0x19`
- goldenSunShroom.coinType 6, coinMotion 2, coinMotionAlt 3 at 75: 0x7b0d3c `push 2`, 0x7b0d43 `mov [esp],3` when 0x4b, 0x7b0d4a `push 6`, `call 0x40cb10`
- goldenSunShroom.offMode 31: 0x7b0ce4 `cmp [ebx+0x7f8],0x1f; je skip`
- goldenSunShroom.packetStartCounter 3500: hook 472 0x7a6505/0x7a650a `cmp ...,0x59; je 0x7a6514 -> 0x489c0e` -> 0x489c11 `mov [esi+0x28],0xdac`
- (zombie shots fly over 0x59: hook 374 0xc02c5e `cmp eax,0x59; je 0x46cad0` is one entry of the single list
  0xc02c55..0xc02c6a, keyed as dodgeZombieShots.on; the separate goldenSunShroom.zombieShotsSkip key was never read
  and is gone, review 2026-11-23)
- strongCoffee.triggerCountdown 1: 0x7b0b9b `cmp [edi+0x50],1; jne`
- strongCoffee.wakeRadius 1: 0x7b0bd2..0x7b0bf0 `sub; add ecx,1; cmp ecx,2; ja` on row and column
- strongCoffee.wakeCs 100: 0x7b0c05 `mov [esi+0x130],0x64`
- strongCoffee.anyPlantOk 1: 0x40e137 `cmp byte [eax+0x143],0; jo` (vanilla `je` = needs asleep); hook 47 0x7a4f40 routes 0x5b/0x73 here
- coffeeHeal.tenths 3 / cap 300: 0xc05db8 `mov ecx,0xa; idiv`, 0xc05dbf `imul eax,eax,3`, 0xc05dc2 `cmp eax,0x12c`; gate 0xc11ce0 (seed 0x23/0x73, state 2)
- leafShield.rowReach 1: 0x7b0df1..0x7b0dfd `sub; add ecx,1; cmp ecx,2; ja`
- leafShield.bandInsidePx 30 / bandPx 40: 0x7b0e03..0x7b0e12 `sub [edi+8]; sub [edi+0x10]; add ecx,0x1e; cmp ecx,0x28; ja`
- leafShield.hpCostShift 3 / hpCostBase 2: 0x7b0e27 `sar eax,3; add eax,2; sub [edi+0x40],eax`
  (death at 0 HP, re-read 2026-11-23: the reflect 0x7b0da0 has no HP test; Plant::Update's death test is the cave
  0xc13150 `cmp [ebx+0x40],0; jl 0xc13055` -> Die, i.e. < 0 as vanilla; so a Leaf Shield at exactly 0 HP stays
  until the next hit, in the exe and in the port)
- leafShield.reflectedFlags 1: 0x7b0e18 `mov [eax+0x74],1` (gate 0x7b0de7 `cmp [eax+0x74],0`)
- leafShield.flashCs 25: 0x7b0e30 `mov [edi+0xb8],0x19`
- projectileDamage.starDouble 1: 0xc10007 `cmp ebx,7` + 0xc10017 `call 0x4537d0` (IsIZombieLevel) + 0xc10025 `shl edx,1`
- projectileDamage.byType: 0x7b08a6..0x7b0910 (0xe 40, 0xf 50, 0x10 40, 0x11 25, 0x12 300, 0x13 40, 0x14 20, 0x15 30, 0x16 [+0x80], 0x17 20, 0x20 100), 0xc10db0..0xc10dd5 (0x22 40, 0x23 15, 0x21 40); else 0 (`xor edx,edx` 0x7b0891)
- bossFlower.rollRange 128 / seedTable: 0xc000d6 `mov eax,0x80; call 0x5af400`, 0xc000e0 `cmp byte [eax+0xc000fd],1; jne` (128 bytes dumped)
- bossFlower.coinType 16 / coinMotion 2: 0xc000bc `push 2`, 0xc000c1 `push 0x10`, `call 0x40cb10`; 0xc000e9 `mov [ebx+0x68],eax`
