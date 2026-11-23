# Sources: the Tall-nut Zombie (type 31) in Unnamed (`data/rules-tallnut-zombie.json`)

Plan 9 R7. Evidence: the research notes (r7-tallnut-zombie) (read-only radare2 `pd` and a rel32
cross-reference scan of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe was never run). Code wins over the Almanac.
App code: `app/src/Mod/Unnamed/World7Zombies.*` (block "Tall-nut Zombie", rules) and
`app/src/Mod/Engine/World7EliteZombies.*` (`TallnutZombieTick`, `TallnutZombieTint`); feature `tallnutZombie` in
`mod.json`. A missing key plays that rule like vanilla. The Tall-nut Zombie's helm HP 2400 and its 1-in-12 roll stay in
`rules-world7-zombies.json` (`zombotany.tallnutHelmHp`, `zombotany.tallnutOddRoll`).

Hook 618 replaces the first lines of Zombie::Update (0x52ae6b); the code below runs once per update, before
`mZombieAge++`, after the Repeater poison tick, in every game mode, for any type-0x1f zombie on a board.

| key | Unnamed | vanilla | exe evidence |
|---|---|---|---|
| regen.periodCs | 100 | - | 0x7972b3: `inc [esi+0x114]; cmp 0x64; jl` then `+0x114 = 0`; only while `[esi+0xc4] == 9` (tall-nut helm, 0xc01316 / 0x7972ad) |
| regen.hp | 10 | - | 0x7972d6: `add [esi+0xd0], 0xa` (helm HP). No compare with the helm max: no cap |
| regen.undamagedExtraHp | 10 | - | 0x7972dd: `cmp [esi+0x12c], eax (helm HP before); [+0x12c] = before + 10; jg skip; add [esi+0xd0], 0xa; [+0x12c] += 10`: +10 more when it was not hurt since the last regeneration. Almanac 魂灵再生 "doubled if not damaged within 1 s" |
| odd.summonPeriodCs / summonAtCs | 1200 / 600 | - | 0xc033f0: variant 0x101 and `[mApp+0x7fc] == 3` (playing): `mZombieAge % 0x4b0 == 0x258` (age before ++) |
| odd.summonRoll / gargantuarBelow | 8 / 5 | - | 0xc0342b: `Rand(8)`, `<= 4` -> 0x17 Gargantuar, else 7 Football; Board::AddZombieInRow(type, own row), mMindControlled copied (`sete`) |
| odd.riseCounterCs | 50 | - | 0xc03466..0xc0347f: PixelToGridX(mX) -> RiseFromGrave(col, row), `+0x68 = 0x32`, UpdateZombieRiseFromGrave once |
| odd.alpha | 176 | - | 0xc03360 (DrawReanim colour chain 0x52d2bf, after Repeater poison / weakened): type 0x1f variant 0x101 -> `edi = 0xb0; jmp 0x52d2c8` = the mind-control colour with alpha 176, additive on |

Port rulings: the summoned zombie's fromWave is 1000 (the exe passes the Board pointer in EBX: never a wave, >= 0);
the counter lives in `mSummonCounter` (exe +0x114) and the recorded HP in `ZombieState::stored` (exe +0x12c).
Not ported here: variant 0x100 (mode 0x8f boss Tall-nut, hook 189 / 0xc01260), see the study section 4.
