# Sources for data/rules-day-levels.json (Plan 2 Task 5, Day waves and level rules)

Evidence: the research notes (levels) (section numbers below), read from Unnamed 1.3beta2 `PlantsVsZombies.exe` (1051 + `.NewSec`).
Every key is read by `app/src/Mod/Unnamed/Levels.cpp` with the vanilla value as fallback (a missing key = vanilla).
Unchanged vanilla rules (wave counts 0x6a34e8, allow list 0x6a35b0, start sun, first-wave countdowns, flag-wave 2.5x and
8 plain Normals, explosion damage 1800, rewards, seed slots) need no key: the engine values are already right (levels.md 2, 4-7).

| key | value | vanilla | evidence |
|---|---|---|---|
| dayLevels.waveBudgetMultiplier | 4 | (none: x1, x3 mini-boss, x4 bowling) | hook 22 0xa878a4 -> 0x79ab09 `cmp eax,0x11; jmp 0x409960` (x4), levels.md 3.3 |
| dayLevels.forcedFlag.level | 1 | (none) | hook 23 0x7954e0 `mLevel == 1`, levels.md 3.7 |
| dayLevels.forcedFlag.wave | 3 | (none) | hook 23: flat index 0x244 - 0x1ad = 151 = mZombiesInWave[3][1] (0-based wave) |
| dayLevels.forcedFlag.slot | 1 | (none) | hook 23: same flat index (0-based slot) |
| dayLevels.allowCheckUsesStartingLevel | 0 | 1 | in-place patch 0x40d6a3 `eb 03` (GOTY `7d 03`), levels.md 4 |
| dayLevels.poleGrave.enabled | 1 | 0 | .text 0x525fa0 `jmp 0x651a97` (not in hooks.txt), levels.md 8.2 |
| dayLevels.poleGrave.colDivisor | 80 | - | 0x651ac5..0x651ad8 `div bx`, bx = 0x50 |
| dayLevels.poleGrave.colOffset | -1 | - | 0x651ac5: quotient - 1 |
| dayLevels.poleGrave.alwaysVariant | 41 (0x29) | - | 0x651a97: variant 0x29 skips the Tall-nut test |
| dayLevels.poleGrave.skipVariant | 50 (0x32) | - | 0x95add0: glove elite (0x32) makes no grave |
| dayLevels.poleGrave.vaseVariant | 259 (0x103) | - | 0xc036e0: variant 0x103 takes the Scary-Potter vase path, no grave |
| dayLevels.poleBonk.seedTallnut | 23 (0x17) | 23 | 0x7b1910 (vanilla Zombie.cpp:1757) |
| dayLevels.poleBonk.seedTallnutPlus | 103 (0x67) | (none) | 0x7b1910 (mod plant Tall-nut+80) |
| dayLevels.poleBonk.seedGiantWallnut | 50 (0x32) | (none) | 0x7b1910 |
| dayLevels.poleBonk.seedCactus | 26 (0x1a) | (none) | 0x7b1910 |
| dayLevels.poleBonk.cactusState | 32 (0x20, STATE_CACTUS_HIGH) | (none) | 0x7b1910 `+0x3c == 0x20` |
| dayLevels.graveRise.rerollRange | 25 | 0 (no re-roll) | hook 88 0x795531 `Rand(25)`, levels.md 8.3 |
| dayLevels.graveRise.rerollAcceptMask | 25199359 (bits 0-7, 9, 15, 23, 24) | 0 | hook 88 0xc0358d: r in {0..7, 9, 15, 23, 24} -> use r |
| dayLevels.graveRise.rerollAgainMask | 256 (bit 8, Dancer) | 0 | hook 88: r == 8 -> roll again |
| dayLevels.graveRise.rerollMisses | 2 | - | hook 88: r in {10..14, 16..22}: 1st -> roll again, 2nd -> vanilla pick |
| dayLevels.graveRise.phaseByType | 1 | 0 | hook 595 0x95b2e0 / 0x95b300: Pole PRE_VAULT, Newspaper READING, Jack RUNNING |
| dayLevels.graveRise.jackFuseBase | 300 | - | hook 595 0x95b41f: +0x68 = Rand(1000) + 300 |
| dayLevels.graveRise.jackFuseRange | 1000 | - | hook 595 0x95b41f |
| dayLevels.ashThreshold | 1800 | 1800 | 0xc11794 / 0x651504, levels.md 10 |
| dayLevels.ashThresholdUsesTotalHp | 1 | 0 (body only) | .text 0x532b96 -> 0x6514b0 -> 0xc01abe: body + helm (+0xd0) + shield (+0xdc) |
