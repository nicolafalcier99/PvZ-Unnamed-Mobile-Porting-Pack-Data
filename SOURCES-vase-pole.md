# Sources: the Vase Pole Vaulter (elite 0x103) in Unnamed (`data/rules-vase-pole.json`)

Plan 9 R2. Evidence: the research notes (r2-vase-pole) (static radare2 reads of Unnamed 1.3beta2
`PlantsVsZombies.exe`, sha256 d39b3429...e89f66; the exe was never run): cave 0x651a97 -> 0xc036e0..0xc038a6 (vault),
0xc01d87 (vase placer), hook 558 0x52613a -> 0xc038c0 (landing), hook 189 0x429b90 -> 0x9594a0 / 0xc01eb1 (vase
zombie side), 0x7aa320 / 0x7aa130 (boss class), vanilla 1051 calls named from the research notes (addr-1051-funcs).
The roll and the art of 0x103 were ported earlier (`SOURCES-day-zombies.md`, `dayZombies.pole.vaseMaxRoll`).
Code wins; the Almanac has no 0x103 entry and no video shows it. App code: `app/src/Mod/Unnamed/VasePole.*` (rules),
`app/src/Mod/Engine/VasePole.*` (engine), feature `vasePole` in `mod.json`. A missing key plays vanilla (no vase).

| Key | Value | Evidence |
|---|---|---|
| vasePole.enabled | 1 | 0xc036e0 `cmp [esi+0x134], 0x103` takes the vase path instead of the grave (0x958b10); hypnosis does not stop it; `+0x12c` (the grave flag) makes it once per zombie and is set first (0xc03711) |
| vasePole.colDivisor | 80 | 0xc03701..0xc0372b: `div bx` (bx = 0x50) on the low 16 bits of mX, `xor ah,ah`, then -1 (normal) / +1 (hypnotised): the vaulted plant's cell. Landing 0xc038de..0xc038fe: `PixelToGridX(mX, mY)` (0x41c4c0) +1 / -1: the same cell |
| vasePole.zombieRollRange / zombieRejectMask | 33 / 35223552 | 0xc0378e..0xc037be: `Rand(0x21)` re-rolled on 11, 12, 13, 14, 16, 19, 20, 25 (mask bits); only a normal pole makes this vase (a hypnotised one jumps to 0xc037c7), after `SquishAllInSquare(col, row, 0)` (0x52e920) and only if no plant is left in the cell (0xc03745..0xc03788: not dead, not squished, `+0x134 != 2`) |
| vasePole.catchFlags / catchFlagsHypnotised | 129 / 1 | 0xc0381f..0xc0383c: `EffectedByDamage(0x81 / 1)` (0x531a80) on zombies of the same row whose rect (0x5320b0) overlaps the pole's attack rect (0x532140; 0x955e40 strict overlap): a pole catches the other side only. Caught: `mDead = 1`, a vase of its type in the cell, vase+0x54 = `mMindControlled != 1` (0xc03846..0xc0389e) |
| vasePole.potState | 5 | 0xc01d87: GridItem type 7, state 5 (zombie-hand vase), pot type 2, seed 0, sun 0, render order `row * 10000 + 302000` |
| vasePole.potSetsSide | 1 | hook 189: after AddZombieInRow, `mov bl,[esi+0x54]; mov [eax+0xb8],bl` (0x9594b3): a vase zombie's mMindControlled = the vase's byte (0 on every vanilla vase) |
| vasePole.awardOutsideVasebreaker | 0 | **port ruling**: the landing (hook 558) opens vases with the vanilla ScaryPotterOpenPot (0x429ac0), whose tail awards the level when no vase and no enemy zombie is left; outside Vasebreaker that could end a Day level mid-waves (a hypnotised pole's catches all come out hypnotised). The port runs that tail only in Vasebreaker levels |

Rulings (details in the study, section 4):
- The catch loop's boss test (0xc04410: `call 0x7aa320; jne`) reads ZF, not the AL answer; the port uses the intended AL
  reading (skip max HP > 120000, Zomboss, the level-70 boss form). Cost if wrong: level-70 hypnotised Newspapers.
- No vase (and no catch) when the vault column is off the lawn; the exe writes an unreachable grid item.
- Caught zombies also free their reanims (the exe leaks them); nothing visible changes.
- Not ported: a Bungee coming out of a vase keeps its own x (hook 189, 0xc01eb2).
