# Sources for data/rules-mod-plants-shadow.json (Plan 8 part 3c: shadow state, statuses, placement)

Keys are written without the `modPlants.` prefix; feature `modPlants` (no new feature). Read statically from Unnamed
1.3beta2 `PlantsVsZombies.exe` (radare2 `pd`, the Ghidra export the research notes (hooks2); nothing run), on top of
the research notes (mod-plants-behaviour) 1.2 / 1.3 and the keys already in `data/rules-mod-plants.json`
(`shadow.*`, `toxicShadowShroom.*`, `repeaterPoison.*`, `charmedTallnut.*`, `moonflower.*`, `modSun.*`). App code:
`app/src/Mod/Unnamed/ModPlantShadow.*` (pure), `app/src/Mod/Engine/ModPlantsShadow.*` and `ModZombieStatus.*` (wiring).

- shadow.dreamStarfruitFlicker 6: 0xc00e0d `mov eax,6; call 0x5af400` (Rand(6)) in the colour hook 313 chain
  0x7a3cb1 -> 0xc00e00; non-zero = no shadow colour this draw. The port does not draw from the game RNG for it (a hash of
  the board clock and the square), so replays do not depend on the frame rate.
- modSun.skipModes [43, 50, 71, 72]: the Moonflower / Primal Sunflower helper 0x7b0200 returns in modes 0x2b, 0x32, 0x47
  and 0x48 (mod-plants-behaviour.md 0x51, read for group A); the vanilla UpdateProductionPlant gates (I, Zombie, upsell,
  intro, level award, Last Stand before the onslaught) are kept as they are.
- modSun.firstTimerFullRange 1: PlantInitialize hook 265 (0x7a4770): the 300 + Rand(rate/2 - 299) start is only for
  seeds 1 / 0x29 / 9; a mod seed gets `Rand(launchRate + 1)`.
- repeaterPoison.tintR 0 / tintG 255 / tintB 64: 0xc10d30 (draw, record +8 > 0) -> 0xc10d5a `mov edx,0`, `mov ecx,0xff`,
  `mov eax,0x40` -> 0x52d2d9, the vanilla chill colour store (edx red, ecx green, eax blue; colour and additive).
- loadedCannon.twoSquares 1: **port ruling, not in the exe.** The exe plants 0x7f on one free square (no 0x7f test in
  CanPlantAt; hooks 47-52 and 0x410964 compare 0x2f only) and its Cob covers the next column too (hook 40 0xc04920), so it
  can overlap a plant there or hang past column 8. The port asks for both squares.

Rules wired without a new key (constants already in rules-mod-plants.json or read from the exe's control flow):

- Weakened doubling sits at the TakeDamage entry, after the Catapult HP lock: 0x5317c4 hook 705 -> 0xc05900 -> 0x818063
  `jmp 0x95a120` (`mov ebp,[esp+0x10]` = the damage) -> 0x95a12b `jle; shl ebp,1`. The weakened word is 16 bits (`add
  word [esi+0x1a]`, `dec word`), so the port wraps it like the exe.
- Weakened colour: Zombie::DrawReanim's colour chain (0x52d2bf -> 0xc10d30 poison -> 0x95a300 mod zombie colours ->
  0x95a365): for a zombie with the side record (0x52ae40: mFromWave not -2 / -3) and word +0x1a > 0, RGB(48, 48, 48) as
  colour and additive (key dreamStarfruit.weakenTintGrey 48, SOURCES-mod-plants.md). Repeater poison green is tested
  first, so a poisoned weakened zombie is green; both come before mind control and chill. (0x95a16b's RGB(69, 69, 69)
  block is dead code.) The exe also prints the counter over the zombie (0x95a1b0, "%d"): not ported.
- Repeater poison tick: hook 618 0x52ae6b -> 0x7971e0 -> 0xc10cd0 (`cmp [esi+4],0` board; record +8 > 0: `dec`, then
  TakeDamage(1, 0)); Toxic poison tick at the end of the same chain (0x797412 -> 0x7a6740).
- Gargantuar smash (hooks 563 0x526d64 -> 0x7a82a1 and 569 0x527242 -> 0x7a8261): FindZombieTarget (0x52e840) first,
  TakeDamage(500, 0) or 1000 for type 0x20; a hypnotised Gargantuar (`cmp byte [ebx+0xb8],0`) never looks for a plant.
  Generic in the exe; wired under modPlants because Charmed Tall-nut's summoned Gargantuars need it.
- Placement: hook 47 0x7a4f40 (0x5b / 0x73 / 0x23 -> the Coffee branch 0x40e11d, asleep test patched to `jo`), 0x957620
  (first aid list 3 / 0x31 / 0x32 / 0x67 -> 0x40e404, which compares `mSeedType == theSeedType`), hook 41 0x7a5040 (0x5b,
  0x53, 0x6b -> flying slot 0x40d355; 0x6e -> pumpkin slot, automatic in the port: its engine seed is the Pumpkin),
  hooks 39 / 50 / 51 / 63 / 64 (0x6e treated as 0x1e: automatic for the same reason, a Pumpkin and a Holy-fire Pumpkin may
  replace each other as in the exe). Hook 52 (0xc04980: Kernel / Doom on an unloaded Loaded Cannon = reason 0xf) and
  hook 61 belong to the Loaded Cannon's loading, not wired here.
