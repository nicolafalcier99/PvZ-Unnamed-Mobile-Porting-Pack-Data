# Sources: Unnamed visual details (Plan 9 L3)

Feature `modVisuals` (info tooltip, Peashooter layer number); the Sniper and Element-shroom looks also need `modPlants`.
Rules: `data/rules-mod-visuals.json`; English labels: `strings/en-corrections-visuals.txt`. Full study with addresses:
the research notes (l3-visual-details). Exe = 1.3beta2 PlantsVsZombies.exe, read statically.

| Key | Value | Evidence |
|---|---|---|
| modVisuals.infoTooltip | 1 | hook 57 (`Board::UpdateToolTip` 0x40f351 -> 0x955281): zombie title `[name]`, label body/max, 一类 helm, 二类 shield, 气球 balloon, HP total, 黄油 butter, 减速 chill, 冰冻 ice, 易伤 weakened (0x95a1b0), two fields per line (0x9558c0); plant title + 生命 hp/max (0xc05f30..0xc05fea) |
| modVisuals.infoButtons | 2 | `cmp [WidgetManager+0xe8], 2` (0x9552b9): right button only |
| modVisuals.infoSkipMode | 21 | `cmp [LawnApp+0x7f8], 0x15` (0x9552a6): not in Invisighoul |
| modVisuals.infoHoldTicks | 40 | port addition: the phone has no right button; a finger held still 0.4 s with an empty cursor |
| modVisuals.peashooterLayers | 1 | 0xc05e7c: raw seed 0 draws `"%d"` of Plant+0x80 at (2, 70), FONT_DWARVENTODCRAFT18, (255, 0, 255) |
| modVisuals.sniperAim | 1 | hook 13 (`Attachment::SetMatrix` 0x404c8a -> 0x7a7e60 -> 0x7aa500): head overlay = rotation about (40, 40) by atan2(py - zy, abs(zx - px)) while aiming |
| modVisuals.sniperMark | 1 | hook 121 (0xc10f70 sets the side-record flag) + 0xc10fd0: IMAGE_TARGET (`images/target.png`) at zombie (20, 0), scale 1 |
| modVisuals.elementIcons | 1 | 0x7a8e21 -> 0x7b1536 digit (IMAGE_SELECTORSCREEN_LEVELNUMBERS cel countdown/100+1 <= 9 at (w/2 - 6, 25)) and 0x7b158f icons (bit 4, 2, 1 left to right at (3 + 20 i, h - 25); ice = IMAGE_PROJECTILESNOWPEA, fire = REANIM_FIRE_PEA anim_idle frame 20 left 25 up, made by 0x7b3000) |
| modVisuals.packetPlantCels | 0 | phone report 2026-11-23 (Rewind Grass "2 different images"): `DrawSeedPacket`'s plant helper 0x487380 jumps over every static packet_plants.png cel: 0x4873e0 `e9 6e 02 00 00` = `jmp 0x487653` (the reanim draw, then hook 464 0x48767f -> 0x95bda0 / 0x7a39ea tints mod seeds with table +0x24..+0x30) where vanilla has `cmp edi,4; jne` (the next test 0x48740e is still `83 ff 06 75 29`). So every packet (chooser, bank, HUD) draws its plant from the reanim, like the lawn; the pack's own cel 4 (a blue Blover, unused by the exe) never shows. 1 or missing = vanilla cels |

Engine-only fix (no key): the Reanimation and ReanimatorTrackInstance constructors copy the mod's own white 0x800134
(0x4718e9, 0x47198c, 0x4719ab, 0x4719cd), not `Color::White`, so Visual Disorder (0x69) fades only plain image draws,
text and particles, never the reanimations.

Day-plants fix: `PeashooterLayersGuard` maps <= 0 to 1 (the exe's +0x80 starts at -1, PlantInitialize 0x45dc0a, and its
guard 0xc05d10 makes it 1).
