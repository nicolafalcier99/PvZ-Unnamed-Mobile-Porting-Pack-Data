# Sources: Pool zombies and elite forms (`data/rules-pool-zombies.json`)

Plan 4 Task 2. Evidence: the research notes (w3-pool) sections Z1-Z5, "Per-object state",
"rules.json keys" and "Elite art and other art" (read-only reads of Unnamed 1.3beta2 `PlantsVsZombies.exe`; the exe
was never run), plus the research notes (zombies) for helper 0x794800. Code wins over the Almanac and the video. App code:
`app/src/Mod/Unnamed/PoolZombies.*` (rules), `app/src/Mod/Engine/PoolEliteZombies.*` (engine sites), feature
`poolZombies` in `mod.json`. A missing key plays that rule like vanilla (value in the "vanilla" column).

Zombie fields: +0x134 = `ZombieState.variant` (Snorkel lotus 0xB, Dolphin football head 0xC), Zomboni +0x148 =
`ZombieState.extra` (0 normal, 1 orange elite, 2 red). Plant "frozen by a Zomboni" (exe Plant+0x144 = 0 plus the reanim
edits) = new `PlantState.frozen`, saved in the per-object TLV (12-byte blob; older 8-byte blobs load as not frozen).

| key | Unnamed | vanilla | study | exe evidence |
|---|---|---|---|---|
| poolZombies.snorkel.eliteRoll / eliteHit | 4 / 1 | no roll | Z1 | hook 499, site 0x522FAE, .NewSec 0x796959 `Rand(4) == 1` -> +0x134 = 0xB |
| poolZombies.snorkel.lotusIgnoresPlants | 1 | 0 | Z1 | hook 675 chain 0x795F8B: variant 0xB skips FindPlantTarget (never bites plants) |
| poolZombies.dolphin.hp | 870 | 500 | Z2 | in-place `0x522D5E mov dword [edi+0xc8], 0x366` (every Dolphin Rider) |
| poolZombies.dolphin.eliteRoll / eliteHit | 3 / 1 | no roll | Z2 | hook 494, site 0x522DB3, .NewSec 0x79699B `Rand(3) == 1` -> +0x134 = 0xC |
| poolZombies.dolphin.eliteJumpVx | 2.0 | 0.5 | Z2 | hook 559, 0x796A10: float 0x6793CC (2.0) for 0xC at the start of PHASE_DOLPHIN_IN_JUMP |
| poolZombies.zamboni.freezePlants | 1 | 0 | Z3a | hook 620, site 0x52AFC7, .NewSec 0x79561E chain (helpers 0x7B1800, 0x794320, 0x95BFD0, 0xC04E70) |
| poolZombies.zamboni.freezeRows / freezeHalfWidthPx | 1 / 120 | - | Z3a | 0x794320: `abs(plant.row - z.row) <= 1`, `z.x - 120 <= plant.x <= z.x + 120` |
| poolZombies.zamboni.freezeTintRed / freezeTintGreen | 0 / 160 | - | Z3a | 0x795706..0x795714: reanim colour red 0, green 160, blue kept; anim rate 0 |
| poolZombies.zamboni.iceShroomFreezes | 1 | 0 | Z3b | hook 712, site 0x531A1A in CanBeFrozen, 0x818031 -> 0xC02C00 -> 0x7CD050 (CanBeChilled test replaced); hook 713 0xC10AE0 (Zomboss at 1 HP refused) |
| poolZombies.zamboni.iceMaxX | 933 | 800 | Z3c "vanilla untouched" | UpdateZamboni ice timer bound `< 800` became 933 for the wide lawn |
| poolZombies.zamboni.eliteRoll / eliteHit | 9 / 0 | no roll | Z3c | hook 496, site 0x522E74, 0x95A400 -> 0x95B750: `Rand(9) == 0` -> +0x148 = 1 (not mode 0x89, not adventure level 65) |
| poolZombies.zamboni.eliteVx / redVx | 0.2 / 0.45 | curve 0.25 -> 0.05 | Z3c | hook 598, 0x95A600 |
| poolZombies.zamboni.redVxAtBodyHp | 600 | - | Z3c (U4) | hook 598: any Zomboni at exactly 600 body HP also drives at 0.45 (ported as read) |
| poolZombies.zamboni.eliteArmorFlat / eliteArmorMul | 5 / 0.8 | - | Z3c | 0xC019ED -> 0x95A476: `d' = round((d - 5) x 0.8)`, d <= 5 -> 0 |
| poolZombies.zamboni.eliteBreakHp / eliteRedHp | 200 / 350 | - | Z3c | 0x95A499 (`d' + 200 >= HP`: hit dropped, state 2); hook 613, 0x95A440 / 0x95A453 (state 1 at HP <= 350 -> 2) |
| poolZombies.zamboni.tintEliteR/G/B, tintRedR/G/B | 255,172,0 / 192,16,16 | - | Z3c | hook 647, 0x95A300 |

Fixed in code (not rules): the Zomboni freeze gate (not hypnotised, not bungee-dropped height 9, not the orange state);
the immune list (Snow Pea, Ice-shroom, Winter Melon, Torchwood, Jalapeno, Spikeweed, Tangle Kelp, Split Pea, Spikerock,
the mod's own plant codes 0x7A, 0x56, 0x55, and any plant in the square of a 0x6E plant); the CanBeFrozen gate's
refusals (variant 0x100, hypnotised, no head, body HP with low byte 0: 256, 512, 768, 1024, 1280).

Art: lotus Snorkel = `anim_head1` -> IMAGE_BLANK, `anim_hair` / `anim_head2` hidden, REANIM_LILYPAD playing `anim_idle`
at 15 attached to `anim_head1` with the umbrella leaf's transform (65, -5, 0.2 rad, -1, 1) from helper 0x794800 (the w3
study's "anim_head_idle" is the helper's `anim_idle` string 0x6580D4; LilyPad has no other loop). Football-head Dolphin
= `anim_head1` -> IMAGE_ZOMBIEFOOTBALLHEAD (`particles/ZombieFootballHead.png`, vanilla file), `anim_head2` shown.
Zomboni states = tint only. Bobsled / ice: no rule; Unnamed's `images/ice.png`, `ice_cap.png`, `ice_sparkles.png`
(dark red ice) come through the asset overlay; the four `Zombie_bobsled*.png` stay in `overlay-en-skip.txt` (only the
BRAINS OR BUST lettering differs, see `data/overlay-en-skip.md`), so the "brown sled" of the study is not shown in English.
Ducky Tube: no change (Day Normal roll applies to it as before).

Not ported (open): hook 660 (an orange Zomboni clears `mMindControlled` of overlapped zombies of types 5, 7, 0xC, 0x16,
0x17, 0x20 and steps its own state) and hook 793 (a separate damage path for state 1): not fully read (study U4). The
global elite switch `[0x800258]` is fixed at 0, as for Day and Night. Almanac text: no correction; Unnamed's Zomboni
entry says "No elite form" and the orange elite is the study's "hidden elite", left hidden.
