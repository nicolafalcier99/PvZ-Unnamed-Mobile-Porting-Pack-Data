# Sources: Plan 9 R9 small rules (feature `smallRules`)

Rules file: `data/rules-small-rules.json`. Study: the research notes (r9-small-rules) (full disassembly notes).
Read in the Unnamed 1.3beta2 `PlantsVsZombies.exe` with radare2 (read only) on 2026-11-23.
Engine: `Mod/Unnamed/SmallRules.*` (pure rules), `Mod/Engine/SmallRules.*` (Projectile::DoImpact, Plant::Die sites).

## Pity hypnotise (feature `smallRules`)

| Key | Value | Vanilla | Evidence |
|---|---|---|---|
| smallRules.pity.rollRange | 14370 | (none: no rule) | 0xc10050..0xc1009b: plain star (`+0x80 == 0`) on a zombie that is not boss class (0x7aa320): `cmp [0xc10033], 0x3822; jge` hit, else `mov eax, 0x3822; call 0x5af400` (Rand) `jne` skip; hit = `[0xc10033] = 0`, `byte [zombie+0xb8] = 1` (mMindControlled) before TakeDamage |
| smallRules.pity.counterAt | 14370 | (none) | same `cmp [0xc10033], 0x3822; jge`. The counter: 0xc10000 (hook 396 -> 0x7a0f31 -> 0x7b0890) `cmp ebx, 7; jne; call 0x4537d0` (I, Zombie) `jne; shl edx, 1; add [0xc10033], 1`: +1 per star damage, outside I, Zombie; global, not saved |

Only stars: 0xc05700 (the last link of hook 397) `cmp [edi+0x5c], 7; jne 0x79f01e` sends every other projectile to
TakeDamage before the pity / star-kind block (0x79ef88 -> 0x959fc0). The Shrapnel core (`+0x84 == 2`, 0x79ef88) skips it.
**(corrects study)** mod-plants-behaviour.md said any projectile with `+0x80 == 0`, and that the Roof big cabbage gets
the star-kind effects; both are wrong.

Plain-star damage x2 (same 0xc10025 `shl edx, 1`) uses the existing `modPlants.projectileDamage.starDouble`
(SOURCES-mod-plants.md): the port's vanilla DoImpact path now calls `ModProjectileDamage` for plain stars too (it did
for kind stars only, so a Starfruit star did 1 instead of 2).

## Flying zombies hit by flags 13 (V2, feature `smallRules`)

| Key | Value | Vanilla | Evidence |
|---|---|---|---|
| smallRules.flyingHitByFlags | 13 | (none: ground flags never hit a flying zombie) | hook 715: `Zombie::EffectedByDamage` 0x531c4b `call IsFlying; jmp 0xc11cb0`: flying -> `cmp bl, 0xd; je 0x531c6a` (true) else false. 13 = `GetDamageRangeFlags` of Cabbage, Kernel, Melon, Winter Melon, Squash (0x45ebb5) and the mod pults (hook 271). 1.3beta1 "[quote not included]". Hook 360 (0x95a83f) is Tangle Kelp's target filter, not this |

## Chooser: Last Stand, 0x66, 0x78 (feature `modesVanilla`)

| Key | Value | Evidence |
|---|---|---|
| modesVanilla.bannedSeeds.31 | [81, 89] | seed filter 0x7b0f00 (hook 425): `cmp edx, 0x1f / 0x66 / 0x78; je 0x7b0f85` -> seeds 1, 9, 0x29, 0x18, 8 (vanilla, engine) and **0x51 Primal Sunflower, 0x59 Golden Sun-shroom** (0x7b0fb2, 0x7b0fbb) |
| modesVanilla.bannedSeeds.102 | [81, 89] | same branch, mode 0x66 (its vanilla five are in modes.json `bannedSeeds`) |
| modesVanilla.bannedSeeds.120 | [81, 89] | same branch, mode 0x78 (same) |

## Coffee Bean heal (no new key)

Plant::Die hook 362 (0x467aa1 -> 0xc05da0 -> 0xc11ce0): dying seed 0x23 (vanilla Coffee Bean) **or** 0x73, in state 2,
heals the top plant under it by `maxHp / 10 * 3` (cap 300). No mode gate. Keys `modPlants.coffeeHeal.tenths` / `.cap`
(SOURCES-mod-plants.md); the engine now calls it for the vanilla Coffee Bean too.

## Checked and not ported (no such rule in the exe)

- Cactus "can't be hammered" (Fog U13): 0x7b1910 is called only from cave 0x651a97, entered from 0x525fa0 in
  Zombie::UpdateZombiePolevaulter after FindPlantTarget(VAULT): it is the Pole Vaulter bonk list (Tall-nut 0x17, 0x67,
  Giant Wall-nut 0x32, HIGH Cactus), already `dayLevels.poleBonk.*` (SOURCES-day-levels.md).
- Blover 60 damage / 200 px push (Almanac; Fog U4): the code is 20 freeze damage (hook 803 `push 0x14`), no lane push
  anywhere (every `0x1b` compare in the mod code checked). Code wins: `fogPlants.blover.*` unchanged.
- Imitater Doom-shroom clears graves (w2 1.8): hook 345 (0xc118f0) tests `Plant+0x138 == 0xf`; the Imitater morph
  (0x466b95 `push 0x30`) gives the new Doom-shroom mImitaterType 0x30; the only writer of 0xf is the Loaded Cannon
  Doom load (0xc1188a), already `modPlants.loadedCannon.doomClearsGraves`.
