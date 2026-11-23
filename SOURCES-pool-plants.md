# Sources for data/rules-pool-plants.json

Every key below comes from Unnamed 1.3beta2 `PlantsVsZombies.exe` code, read in
the research notes (w3-pool) (section in brackets; addresses are the exe's). The app's fallback for each
key is the vanilla behaviour, and every rule is off while the `poolPlants` feature is off (vanilla mode). Booleans are
0/1. App code: `app/src/Mod/Unnamed/PoolPlants.*` (rules), `app/src/Mod/Engine/PoolPlantSites.*` (Jalapeño column,
barrage, Ice-shroom; dev layout), sites marked `// PVZU:` in `Plant.cpp`, `Projectile.cpp`, `Zombie.cpp`, `Board.cpp`.
The exe never checks the level in these hooks, so the rules hold on every lawn in Unnamed mode, not only in world 3.

Table changes (already in `data/plants.json`, Plan 1 tables, not repeated here): Lily Pad recharge 750 → 500 [P1],
Threepeater cost 350 [P3], Tangle Kelp 50 [P4], Spikeweed 125 [P6], Tall-nut 150 / recharge 2400 [P8].

## Squash [P2]
- `poolPlants.squash.reachPx` = 105, `poolPlants.squash.reachEatingPx` = 136: in place in `FindSquashTarget`
  `0x4608D6 mov [esp+0x1c],0x69`, `0x4608E0 mov [esp+0x1c],0x88` after `cmp byte [zombie+0x51]` (mIsEating);
  vanilla 70 / 110
- `poolPlants.squash.surviveRoll` = 100, `poolPlants.squash.surviveBelow` = 27: hook 298, site 0x460D1E (the land
  branch's `mStateCountdown = 100` in `UpdateSquash`), 0x79580A (decompile) `if (Rand(100) < 0x1b)`: the old Squash gets
  `mVisible = 0`, `mStateCountdown = 1`, then `Board::AddPlant(mX / 80, mRow, SEED_SQUASH)` and the new one takes the old
  `mX, mY`. In the pool the Squash dies before this site (vanilla), so no roll there.

## Threepeater [P3]
- `poolPlants.threepeater.roll` = 3, `snowRoll` = 1, `fireRoll` = 2: hook 352, 0x7976DA `cmp [ebp+0x24],0x12;
  Rand(3); 0 → keep; 1 → sete byte [proj+0x5c] (type 1 = snow pea); 2 → ConvertToFireball(proj)` once per `Plant::Fire`
  (= per pea: `LaunchThreepeater` fires each lane separately)

## Tangle Kelp [P4]
- `poolPlants.tangle.drags` = 3: hook 294, site 0x4602D5 (the `Die()` when the drag ends), 0x79719F
  (decompile) `++[plant+0xcc]; if (< 3) mState = 0; else Plant::Die()`; the dragged zombie still dies (vanilla code after)
- `poolPlants.tangle.anyGround` = 1: hooks 48 (0x40E273 → 0x95A828) and 49 (0x40E2CD → 0x95A800) in
  `Board::CanPlantAt`: seed 0x13 jumps past the "Lily Pad / Tangle Kelp / Sea-shroom only in water" block on every
  stage (roof included) to the shared tail 0x95BF50 = vanilla's "under plant / normal plant" rules: an Imitater under
  it or any plant in the normal layer refuses (NOT_HERE), else OK. Seed 0x2B (Cattail) shares the hook; not ported
  here (not a world-3 plant)
- `poolPlants.tangle.maxTargetHp` = 120000: hook 360, site 0x4677A8 in `FindTargetZombie` (vanilla
  `TANGLEKELP && !mInPool → skip`), 0x95A83F: skip Boss (0x19) and Bungee (0x14); `[zombie+0xbd]` (mInPool) → target
  as vanilla; on land skip Gargantuar (0x17) and Giga (0x20), then 0xC01230 `cmp [zombie+0xcc],0x1d4c1; jl target`
  (skip body max HP >= 120001)
- Range flags stay vanilla 5 (`GetDamageRangeFlags`, hook 272 returns the same value)

## Jalapeño [P5]
- `poolPlants.jalapeno.burnsColumn` = 1, `columnFireDx` = 40, `iceCutDx` = 80: hook 346, site 0x466951 (start of
  `DoSpecial` case 0x14) → 0x95B960: 5 lanes (6 when `Board+0x554c` = background 2 or 3), each
  `AddReanimation(mX + [0x67959c] = 40.0f, GridToPixelY(mPlantCol, lane), lane * 10000 + 0x4AF39, 0x22 =
  REANIM_JALAPENO_FIRE)`; every zombie with `EffectedByDamage(GetDamageRangeFlags(0))` whose rect covers the column
  (0x957680: `round(x/80) - 1 <= col <= round((x+w)/80) - 1`, FPU rounding) gets `ApplyBurn` then `RemoveColdEffects`
  (0x532B40); a Zomboss iceball (`+0x140` reanim, `+0x14c` = 0) with `round((reanim+0x2c + 0.0f) / 80.0) == col` is
  destroyed; all 6 rows `if (mIceMinX <= mX + 0x50) mIceMinX = mX + 0x50` (Board+0x60c); GridItems type 3 (ladder) with
  `mGridX == col` die; then back to vanilla 0x466957 (row burn)
- `poolPlants.jalapeno.iceRoll` = 100, `iceMax` = 17, `fullHp` = 300: `.text` cave 0x651E6C, entered from
  `UpdateAbilities` 0x46340A when `mDoSpecialCountdown` reaches 0: `cmp [edi+0x44],0x12c; cmp [edi+0x40],0x12c`
  (max HP and HP both 300, checked before the roll), `cmp [edi+0x24],0x14 → ebx = 0x11, ebp = 0xE`,
  `Rand(0x64); cmp eax,ebx; jg` (<= 17 → **18 %**), `AddPlant(mPlantCol, mRow, 0xE, -1)` and, as the new plant is type
  0xE, its `DoSpecial` (0x4666A0) at once, then the Jalapeño's own `DoSpecial`. Almanac says 13 %: code wins
- `poolPlants.jalapeno.barrage` (69 shots `[dx, dy, vx, vy, vxAdd]`), `barrageConversions` = 2, `barrageMotion` = 7,
  `barrageRangeFlags` = 1, `barrageRenderOrder` = 342525: hook 347, site 0x466995 (after `Die`) → 0x956082..0x9574C0:
  per shot `Board::AddProjectile(mX + dx, mY + 0x20, 0x539FD, mRow, 0)`, `[p+0x74] = 1` (range flags), `[p+0x58] = 7`
  (MOTION_STAR), `[p+0x3c]`/`[p+0x40]` = vx/vy, then helper 0x956030 (`vx -= 0.25f`, dx = −55, 35 shots) or 0x956059
  (`vx += 0.2f`, dx = +115, 34 shots), each calling `ConvertToFireball(0)` then `ConvertToFireball(1)` → tier 2
  (blue, 60 damage). The list was read from the exe bytes (`mov dword [eax+disp8], imm32` immediates as float32, no
  rounding) by a read-only script; it equals the research notes (w3_barrage) except that tool shows −0.0 (r2 printed
  `0x80000000` as an import name) as 0. Velocities in the file are the shortest decimals that round-trip to the
  exe's float32 values

## Spikeweed / Spikerock [P6]
- `poolPlants.spikeweed.anyGround` = 1 (V2, 2026-11-23, community "[quote not included]" = plantable on the roof):
  `Board::CanPlantAt` 0x40e230 `cmp esi,0x15` is followed by 2 NOPs at 0x40e233 (the vanilla short `je` into the
  "pool / roof / under-plant -> 12 PLANTING_NEEDS_GROUND" block is gone), so only Spikerock (0x2e, 0x40e235) keeps
  that test. Then the roof pot test 0x40e2c4 jumps to hook 49 0x95a800: seed 0x15 with the pot flag `[esp+0x17]` 0
  -> on (0x40e2e3), with a pot -> eax 5 (PLANTING_NEEDS_POT). Side effects kept from the exe: Spikeweed may go on a Lily
  Pad, and on a Flower Pot off the roof. Pure rules `SpikeweedNeedsGround`, `SpikeweedRoofPot`
- `poolPlants.spikeweed.stunRoll` = 3, `stunSkip` = 1, `stunCs` = 30: hook 276, site 0x45EE22 in `DoRowAreaDamage`
  (after `TakeDamage`), 0x797A2D (decompile): seed 0x15 or 0x2E, `[z+0xba]` (has head), `[z+0xb0] == 0` (mButteredCounter),
  `[z+0x28]` (phase) not 1..3, then `Rand(3) != 1` → `ApplyButter`, `[z+0xb0] = 0x1e` (also when ApplyButter refused
  the zombie, as the exe)

## Torchwood [P7]
- `poolPlants.torch.maxTier` = 5: hook 295, site 0x4606AB in `UpdateTorchwood` (0x7959E7: type 0 pea, or type 6
  fireball with `[p+0x80] <= 4` → ConvertToFireball(col); type 1 snow pea → ConvertToPea(col)) and the in-place
  `0x460661 jmp 0x460668` that drops the vanilla "pea or snow pea" filter
- tier steps (code, not keys): hook 411 (0x46ECB8 → 0x795B32, the start of `ConvertToFireball`): `if
  (byte [p+0x78] != -1 && [p+0x84] == 0) { [p+0x84] = 1; [p+0x80] = -1; body }` (a pea a Torchwood just thawed
  converts at that same Torchwood) else `[p+0x84] = 1; if ([p+0x78] != gridX) body`; hook 412 (0x46ED3D → 0x795A19,
  after the new fire-pea reanim): tier 1 → 2, 2 → 5, 3 → 4, 4 → 5, −1 → 3, else → 1
- `poolPlants.torch.tier2Tint*` = 40/200/240, `tier4Tint*` = 139/1/139, `tier5Tint*` = 240/60/60: hook 412 writes
  reanim `+0x48/+0x4c/+0x50` (colour override) and `+0x98 = 0` (filter effect) for tiers 2, 4, 5; tier 3 uses the Day
  key `dayPlants.fireTier.tier3Tint*` (122/230/143, same code); tier 1 keeps the vanilla look
- damage and chill are **not repeated here**: they are the Day keys `dayPlants.fireTier.damage1..5` (40/60/40/60/80,
  hook 389) and `dayPlants.fireTier.chill*` (tiers 3..5 → 750 cs + 10 arm damage, hook 721), which already cover every
  tier
- Snow Pea 34 % fire shot (Day): the exe sets `[p+0x80] = -1` and converts → 3; with the Pool tiers on the app now does
  the same (start tier −1), so a Torchwood steps it 3 → 4 → 5, never twice

## Tall-nut [P8]
- `poolPlants.tallnut.regenHp` = 75, `regenTicks` = 100: hook 807 (0x651D9D → 0xC02230, in the blink code shared with
  the Day Wall-nut heal): seed 0x17, not in game mode 0x2B (Zen Garden): `if ([p+0xd0] == hp) { if (++[p+0x58] < 100)
  done; hp = min(hp + 0x4b, max) } [p+0x58] = 0; [p+0xd0] = hp` (also seed 0x67 with a flag: a later-world plant, not
  ported)
- `poolPlants.tallnut.thorns` = 10, `thornsFlags` = 0: `Zombie::AnimateChewEffect` 0x52BC94 (after
  `mEatenFlashCountdown = max(.., 25)`) → … → 0x796747 `push 0xa; mov eax,0; call 0x5317C0` (TakeDamage(10, 0)) for a
  Tall-nut. Almanac says 15 per bite: code wins
- `poolPlants.tallnut.smashDamage` = 2400: `Zombie::SquishAllInSquare` 0x52E96B `jmp 0x651A45`: plant 0x17 and
  squisher 0x17 / 0x20 / 0x1E → `sub [plant+0x40],0x960` instead of `mPlantsEaten++; Squish()`. 8000 HP → dies on the
  4th smash (vanilla `Plant::Update` kills a plant below 0 HP)

## Not ported
- Squash missed-smash coin (hooks 296/297, `Plant+0xCC` hit counter, coin 0x12 from the 15th miss): its gate flag
  (`in_ZF`) was not resolved in the study (conf L)
- Tangle Kelp's own land attack rect (hook 371): numbers not read (study U7); the vanilla rect `(mX, mY, mWidth,
  mHeight)` stays
- Cattail on grass (same placement hook as Tangle Kelp): not a world-3 plant

English corrections (`strings/en-corrections-pool-plants.txt`, code wins over the Almanac):
- Jalapeño: the Almanac says 13 % and "freezes every zombie outside its lane"; the code is 18 % and an Ice-shroom that
  freezes every zombie on the lawn; it also burns its column, which the Almanac does not say
- Tall-nut: the Almanac says thorns 15 per bite; the code does 10 per chew
