# Sources: Wall-nut Zombie self-copy (Plan 9 R6)

Feature `wallnutZombieCopy`, rules `data/rules-wallnut-zombie.json`. Study: the research notes (r6-wallnut-zombie)
(full disassembly and readings). Almanac: 神谕心法, "[quote not included]"
(the research notes (almanac) 3.3). Exe read statically (radare2), never run.

Entry: Zombie::Update 0x52ae6b `jmp 0x7971e0` (hook 618) -> 0xc10cd0 (board null -> vanilla; poison tick) ->
`jmp 0x7971ea` (0xc10d16). Every mode, no world / level / elite-option gate.

| Key | Value | Exe | Meaning |
|---|---|---|---|
| `wallnutZombie.copy.on` | 1 | 0x7971eb `cmp [esi+0x24], 0x1b` | the skill exists (type 27, ZOMBIE_WALLNUT_HEAD); missing = vanilla |
| `wallnutZombie.copy.quietTicks` | 3600 | 0x79722f `cmp [esi+0x114], 0xe10` | ticks without the helm HP going down before a copy (36 s) |
| `wallnutZombie.copy.maxX` | 800 | 0x797d3c `cmp [esi+8], 0x320; jg` | only while mX <= 800 (on screen) |

Fixed in code (not keys): helm type must be 8 (0x7971f5); mFromWave >= 0 (0x797d32), alive (0x797d49), has head
(0x797d56), not hypnotised (0x797d63); the counter resets when the helm HP is lower than on the last eligible tick
(0x797208 `jle`, last HP in +0x12c = mBossMode, counter in +0x114 = mSummonCounter); the copy is
IZombiePlaceZombie(0x1b, mX / 80, mRow) (0x797265 -> AddZombieInRow(27, row, 0)), its mPosX = the original's
(0x797278), then TakeDamage(copy helm - own helm, flags 1) (0x79727e..0x797292).

Mac check (port, 2026-11-23): `-pvzu-mode unnamed -pvzu-level 4 -pvzu-dev-spawn WALLNUT_HEAD -pvzu-dev-spawn-x 760
-pvzu-dev-spawn-count 2 -pvzu-log-zombies <f>`: both zombies (spawned t=50, t=100) made a copy at t=3649 / t=3699 at
their own x with helm 1600; vanilla mode made none; two zombies chewing a Tall-nut (Unnamed chips their helms) made
none in 4200 ticks.
