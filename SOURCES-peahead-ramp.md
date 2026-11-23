# Sources: Peashooter Zombie fire-rate ramp (`data/rules-peahead-ramp.json`)

Plan 9 R5. Evidence: the research notes (r5-peashooter-zombie) (static radare2 reading of
Unnamed 1.3beta2 `PlantsVsZombies.exe`, never run). It answers the "Peashooter Zombie fire-rate ramp: no code found"
line of `SOURCES-world7-zombies.md` and item 8 of the research notes (w6-w7-and-new-content) section 8. Code wins over the
Almanac; here both agree. App code: `app/src/Mod/Unnamed/World7Zombies.*` (block "Peashooter Zombie fire-rate ramp"),
`app/src/Mod/Engine/World7EliteZombies.*` (`PeaHeadNextShot`, one `// PVZU:` site in `Zombie::UpdateZombiePeaHead`),
feature `peaHeadRamp` in `mod.json`. A missing key plays like vanilla (150 cs between peas, no roll).

| key | Unnamed | vanilla | exe evidence |
|---|---|---|---|
| peaHeadRamp.roll | 75 | - (no roll) | hook 572 (0x5275a3 -> 0x7958c1 -> pea at 0xc03ed0 -> back at 0x7958fe): `cmp [edi+0x24], 0x1a` (Peashooter Zombie only, no world or mode gate; hypnotised too); `pushal; mov eax, 0x4b; call 0x5af400` (Rand(75)); `cmp eax, [edi+0x12c]; jl +; inc [edi+0x12c]` |
| peaHeadRamp.baseInterval | 150 | 150 | 0x795925 `mov eax, 0x96; sub eax, [edi+0x12c]; mov [edi+0x68], eax; popal; jmp 0x5275b6` (skips the vanilla `mov [edi+0x68], 0x96` at 0x5275af) |

Zombie+0x12C is vanilla `mBossMode` (0 from ZombieInitialize; a Peashooter Zombie never uses it otherwise), kept in the
port's `ZombieState::stored` (the exe +0x12C slot, saved with the game). Nothing resets it. Since Rand(75) < 75, the
count stops at 75: 150 -> 75 cs, the Almanac's "at most +100%"; the chance of a raise is (75 - n) / 75, the Almanac's
"the fewer raises so far, the higher the chance" (`strings/en-corrections-world7.txt` PEASHOOTER_ZOMBIE_DESCRIPTION
already says so).

## Rulings

- The ramp runs in every Unnamed mode, as the exe's test is the zombie type alone.
- The Rand(75) is drawn on every shot, also once the count is at 75 (the exe draws it; keeps the RNG use the same).
