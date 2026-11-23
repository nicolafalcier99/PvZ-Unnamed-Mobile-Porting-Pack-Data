# Level 70 (7-10) boss, the giant Newspaper Zombie: sources (feature `level70Boss`)

Rules: `data/rules-level70-boss.json` (keys `level70Boss.*`), text: `strings/en-corrections-level70-boss.txt`.
Engine: `app/src/Mod/Unnamed/Level70Boss.*` (pure rules), `app/src/Mod/Engine/Level70Boss.*` (sites).
Exe: the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read with radare2 and Python byte reads (never
run). Study: the research notes (w6-w7-and-new-content) section 3 (spawn, phases, bank, meter). The attack loop below
(0x7ab000 and its helpers) was not in the study; it was read for this port. Code wins over the Almanac.

Zombie offsets (1051 layout): +0x1c row, +0x24 type, +0x28 phase, +0x2c x, +0x74 fade, +0x8c..0x98 hit rect,
+0xac chill, +0xb0 butter, +0xb4 ice trap, +0xb8 hypnotised, +0xba has head, +0xc4 helm type, +0xc8/+0xcc body HP/max,
+0xd8..+0xe0 shield type/HP/max, +0xec dead, +0x118 body reanim, +0x11c scale, +0x128 attack (mod), +0x130 attack timer
(mod), +0x134 variant, +0x144 special head reanim. Board: +0xa0 zombie count, +0xbc plant count, +0x144 seed bank,
+0x160 challenge, +0x554c background, +0x5560 sun, +0x557c current wave, +0x5610 meter width.

## Spawn

| Key | Value | Evidence |
|---|---|---|
| level | 70 | 0x7aa100: `Board+0x5550 == 0x46` (or mode 0x83); board level only, any mode |
| triggerWave | 10 | 0x7a07be `cmp [esi+0x557c], 0xa`, reached from .text 0x413fdf right after `call 0x413c00` (SpawnZombieWave) in UpdateZombieSpawning. The engine hook runs at the start of SpawnZombieWave, so it fires when wave index 9 is sent (same tick, boss placed before the wave's own zombies; both have mFromWave 0 vs 9, so TotalZombiesHealthInWave is the same) |
| row, col | 2, 8 | 0xc11030: `mov eax,2; push 8; push 5; call 0x42a0f0` (IZombiePlaceZombie), 0x800258 = 1 around it (no elite roll) |
| variant | 0x7f | 0x7a07f8 `mov [esi+0x134], 0x7f` |
| scale | 3.0 | 0x7a0802..0x7a0812 fild 3 -> +0x11c |
| hp | 150000 | 0x7a0840/0x7a084a +0xc8 = +0xcc = 0x249f0; shield +0xd8/+0xdc/+0xe0 = 0 (Almanac's 50000 + 100000 is not the code) |
| firstAttackCs | 750 | 0x7a085e +0x130 = 0x2ee; +0x128 = 0 |
| rectWidthFactor, rectHeightFactor | 3, 2 | 0x7a0869..0x7a0884: w *= 3; y -= h; h += h |
| pinX | 640.0 | hook 603 (0x52ab18 -> 0x7a0c21): boss -> `mov [esi+0x2c], 0x44200000` and skip the move |
| (no prey) | - | hook 673 (0x52f65e -> 0x7a0920): boss -> 0x52f693, StopEating if eating |
| (no damage states) | - | hook 597 (0x52a4ba -> 0x7a0951): boss -> return from UpdateDamageStates |

## Darkness (0x7aa7a0, also attack 0) and light (0x7aa8a0, attack 1)

| Key | Value | Evidence |
|---|---|---|
| (background) | 1 / 0 | 0x7aa7ae / 0x7aa8ae `+0x554c = 1 / 0`, then 0x40a160 (LoadBackgroundImages) |
| (sleep) | dark: day plants asleep, mushrooms awake; day: the reverse | 0x7aa680 with edi 0 / 1: `call 0x794ac0` (IsNocturnal: 8,9,10,12,13,14,15,24,31,42); `cmp eax, edi; sete al`; SetSleeping(al) (0x45e860, stack arg = asleep); skips Squash 5..7, squished, bungee 2, dead |
| reinforcementRoll, reinforcementExclude | 33, [11,13,14,19,25] | 0x7aa7d5..0x7aa7f8 Rand(33) re-rolled |
| reinforcementRows, reinforcementCol | 5, 8 | 0x7aa7fa Rand(5) row, push 8; count = Board+0xbc (plants) |
| bankMax | 10 | 0xc11070 `cmp eax, 0xa` on SeedBank+0x24 |
| darkBank | [51,115,27,30,14,39,23,15,29,115] | 0x7aa823..0x7aa835 pushes (first argument last pushed): Sprout, Strong Coffee (0x73), Blover, Pumpkin, Ice, Melon, Tall-nut, Doom, Starfruit, Strong Coffee |
| lightBank | [25,11,27,93,14,39,23,2,18,115] | 0x7aa8d0..0x7aa8e2: Plantern, Grave Buster, Blover, Prism-shroom (0x5d), Ice, Melon, Tall-nut, Cherry, Threepeater, Strong Coffee |
| (packet write) | refresh time 0, type | 0x7aa762: packet+0x28 = 0, packet+0x34 = type, packets from SeedBank+0x28, 0x50 apart |
| standInFrom, standInTo | [115,93,89] -> [35,13,9] | **stand-ins (not exe)**: mod plants 0x73 Strong Coffee Bean, 0x5d Prism-shroom, 0x59 Golden Sun-shroom are not in the engine yet; vanilla Coffee Bean, Scaredy-shroom, Sun-shroom (their base plants, study 5.1) take the slot. Since review 2026-11-23 the engine writes the real mod seeds whenever the modPlants feature is on (as the exe does); these keys are used only with modPlants off |
| lightRemoveMax | 4 | 0x7aa8f8..0x7aa973: count live zombies with variant 1..0x7e that are not boss class (0x7aa320), cap bank size and 4, empty that many random non-empty packets (type -1) |
| (text) | DARK_HUNT, LIGHT | 0x7aa83f string 0xa20220 "[quote not included]"; 0x7aa978 string 0xa202c0 "[quote not included]"; MessageWidget::SetLabel style 4, +0x88 = 250 |
| sproutSeed, sproutRoll | 51, 48 | 0x7a071a (bank planting path, cursor type 1): seed 0x33, or Imitater (0x30) of 0x33 -> Imitater with imitater type Rand(0x30) |

## Phases (hook 707, Zombie::TakeDamage 0x531801 -> 0x7a0a70; HP read before the hit)

The boss branch sits inside `FUN_007aa4c0` (Adventure and profile level 61..70), like the world-7 Jack rule.

| Key | Value | Evidence |
|---|---|---|
| shieldBelowThirds, shieldHp | 3, 1 | phase 0x1d and `hp * 3 < max`: +0xd8 = 2, +0xdc = 1 (the next hit breaks the paper, vanilla maddening) |
| phase2Hp, phase2Sun | 4500, 1500 | phase 0x1f, hp < 0x1194, max > 0x1194: max = 0x1194, `Board+0x5560 = 0x5dc` (a store: the 9990 cap does not apply), text 0xa202a0 "[quote not included]" |
| phase3Hp | 1500 | then hp < 0x5dc: max = 0x5dc, +0x134 = 0 (boss form ends), text 0xa20260 "[quote not included]" |
| meterWidth | 150 | hook 101 (0x414286 -> 0x7a08b0): level 70: boss found -> vanilla boss meter (lost HP x 150 / max; 150 when dying); none and wave < 10 -> 0; else the normal meter |
| (draw) | - | hook 650 (0x52d49c -> 0x7a0980): the boss always draws the shield render group; mad and no special head: 0x7aa560 blanks "Zombie_paper_paper" and attaches REANIM_GATLINGPEA (type 80) "anim_head_idle" at 15 fps, matrix (54, 36, 0.2 rad, -1, 1). Hook 651 (0x52d658 -> 0x7a0a00): hands over the paper unless phase 0x1e/0x1f |

## Attack loop (0x7ab000, every update of the boss; reached via .NewSec 0x7a6740 -> 0x7a0ca0)

Runs only with +0x74 < 0, no butter, no ice trap, not hypnotised, head on, not dead, phase not 1/2/3/0x1e.

| Key | Value | Evidence |
|---|---|---|
| (timer) | - | +0x130 - 1; while >= 0 store and return |
| columnTypes | [6,8,12,21,29] | mad only, before the pick: 0x7ab13b Rand(5) -> Door, Dancer, Zomboni, Ladder, Gatling head; 0x7aab60 places it in rows 4..0 at column 8 |
| columnScale, columnHpFactor, columnFadeCs, columnDoorBucketHp | 1.5, 4, 400, 4400 | 0x7aab80 +0x11c = 1.5; 0x7aab91 +0x74 = 400 (gone at 0); body/helm/shield x4 (shl 2); Door: helm type 2, 0x1130, `anim_bucket` shown |
| attackRollReading, attackRollMad | 4, 7 | 0x7ab196..0x7ab1ab Rand(4) / Rand(7) -> +0x128 |
| (0 dark) | - | 0x7aa7a0 again; mad: drain + heal + packets |
| drainPlantsCap, drainScale | 50, 0.080078125 | 0x7ab1d0..0x7ab200: p = min(plants, 50), f = (p/50 + 50/p) x float 0x3da40000 |
| drainFlashCs | 25 | 0x7aa9d0: each plant (not squished, not state 6/7): +0xb8 = max(.., 25), HP -= round(max HP x f) |
| drainHealShift, drainHealCap | 4, 1800 | 0x7a8821: total >> 4, cap 0x708, added to HP, capped at max |
| madPacketSeed | 89 | 0x7ab22e / 0x7ab2bc: SeedBank+0x5c and +0xac (packets 0, 1) = 0x59 if not -1 (stand-in Sun-shroom) |
| (1 light) | - | 0x7aa8a0; mad: 0x7aac50 eat, and if any eaten the freeze and packets |
| eatRows, eatReachPx | 1, 80 | 0x7aac9f..0x7aacd4: other non-boss zombies with \|row - boss row\| <= 1 and x + rect width + 80 >= boss x |
| eatHealShift, eatHealCap | 3, 150 | 0x7a87e0: (body + helm + shield + flying) >> 3, cap 0x96; then TakeDamage(sum, 0); particle 0x42 (MowerCloud); foley 0xf; particle 0x46 (PresentPickup) at the boss |
| eatFreezePerPlant | 10 | 0x7ab27e: [0x800100] = 1, [0x800104] += plants x eaten x 10 (the Fog ice-head freeze) |
| (2 laser) | - | 0x7aadf0(row): particle 0x4b (ZombieBossFireball) at (80c + 64, 100 row + 80) for c 9..0; 0x7aa000 kills every plant of the row (Board+0x5798 += 1, Plant::Die); text 0xa201c0 "[quote not included]"; foley 0x26. Mad: a second row Rand(4), Rand(5) on pool/fog, not the boss's row |
| bungeeRows, bungeeCols | 12 cells | mode 3: 0x412c30 (SpawnZombiesFromSky) twice; if zombies < plants, 0x7aaa70: Bungees (0x14) at (0,1) (0,3) (0,5) (1,3) (2,1) (2,2) (2,4) (2,5) (3,3) (4,1) (4,3) (4,5) |
| graveFirstCol, graveLastCol | 7, 8 | mad: 0x7aa1d0(7): GraveDangerSpawnGraveAt on columns 7..8 of rows 4..0 (5 on pool) without a grave, then 0x412ce0 (SpawnZombiesFromGraves) |
| rayGunPeriod, rayGunFireAt | 50, [9,18,26,34] | mode 4 (mad only): every tick while +0x128 == 4, `t % 50` in the list fires |
| rayGunAngleRate, rayGunAngleMax | 0.031415924, 1.0471976 | 0x7ab092..0x7ab0aa: sin(t x float 0x3d00adfc) x float 0x3f860a92 |
| rayGunDx, rayGunDy, rayGunProjectile | -24, 24, 3 | 0x7ab0eb..0x7ab109: AddProjectile(x - 24, y + 24, renderOrder - 1, row, 3 melon); +0x58 = 7 (star motion); fptan: +0x3c = -1, +0x40 = tan(angle) |
| rayGunSpeedX | -1.0 | as above; text 0xa20240 "[quote not included]", head "anim_shooting" |
| (shot hits plants) | - | hook 380 (0x46cfc5 -> 0x795e39): damage-range flags 0 -> the plant test (0x46cfcf), melon damage |
| (5 frenzy) | - | 0x7aa260 + 0x794707: every zombie loses chill, butter, ice trap, hypnosis, blow-away, yucky face; non-boss: body anim rate x2 |
| (6 rest) | - | nothing |
| headAnimRate | 76 | mad: +0x144 reanim rate 0x42980000, loop, frames of [0x800240] ("anim_head_idle", "anim_shooting" for 4) |
| rowRoll | 5 | 0x7ab47e: Rand(5) re-rolled until it differs, stored in +0x1c (the vanilla row drift moves y) |
| timerRoll, timerBase | 300, 1200 | 0x7ab490: Rand(300) + 1200; mad: x 0x55555556 >> 32 (/3) then add eax,eax (x2) |
| (paper image) | not ported | reading: Rand(40) picks one of 40 engine images (table 0x800300) for "Zombie_paper_paper" each cycle; cosmetic, the paper stays the newspaper |

## Boss class (0x7aa320: max HP > 120000 or type 0x19)

| Key | Value | Evidence |
|---|---|---|
| bossClassMaxHpAbove | 120000 | 0x7aa320 `cmp [eax+0xcc], 0x1d4c0; jg` |
| longButterCs | 30000 | hook 631 (0x52b464 -> 0xc01fd0): butter >= 30000: boss class -> 0; a maddening (0x1e) Newspaper -> hypnotised, 0; else the countdown |
| (mowers) | boss class passes | LawnMower::UpdatePlaying 0x458832 -> cave 0x651615 -> 0x7955f3 -> 0xc01f50 (`+0xcc > 0x1d4c0` -> skip) -> 0x795606 (0x7aa320 -> skip). The same chain lets a thrown Imp (type 0x18, phase 0x47) pass; that part is not ported here (open point) |
| (Chomper) | ported by Day plants | hook 795 (0xc011b0): `dayPlants.chomper.unswallowableMaxHpAbove` 120000 |
| (Tangle Kelp) | ported by Pool plants | hook 360 (0x95a83f -> 0xc01230) is the Tangle Kelp skip: `poolPlants.tangle.maxTargetHp` 120000 (the study's "targeted first" reading was wrong) |

## Sun cap

Board::AddSunMoney (0x41b960) is not patched: `add [eax+0x5560], ecx; if > 0x2706 then 0x2706`; its only caller is
.text 0x4532d9 (Coin collect). So 7-10 starts at 500000 (InitLevel store) and the first collected sun drops the bank to
9990; phase 2 stores 1500. The engine's AddSunMoney already caps at 9990, so nothing changes.

## Text

English in `strings/en-corrections-level70-boss.txt` (keys `PVZU_BOSS70_*`), the exe's message lines (their Chinese and Japanese text is not included in the public pack).
