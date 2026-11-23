# Sources: settings/cheats panel, shop, Zen Garden, Almanac, save (feature `shopUi`, rules-shop-ui.json)

Study (source of truth): the research notes (modes-ui-shop) sections 3-7, the research notes (w6-w7-and-new-content) 1.3.
Exe = the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only through the study export
the research notes (hooks2) (the research notes (modes_show)); nothing run. Code: `app/src/Mod/Unnamed/Options.*` (rules),
`app/src/Mod/OptionsPanel.*` (touch layout, long press), `app/src/Mod/Engine/OptionsPanel.*` (engine), tests
`app/tests/test_options.cpp`.

## The panel

| What | Port | Evidence | Conf |
|---|---|---|---|
| Opening | right click on the Menu button (board) or anywhere on the seed chooser, as the exe; on touch a long press of `shopUi.panel.longPressTicks` (50 = 0.5 s) on Menu, board or seed chooser | hook 80 (0x7a8da1: `clickCount == -1` -> 0xb76c02(0x80)), hook 457 (0xc035c0) | H |
| Storage | `pvzu-settings.json` `"unnamedOptions"` (the exe: `WMInit.ini [BasicSettings]`); not in the save file | 0xb73548.. strings, GetPrivateProfileIntA | H |
| Layout | our own touch panel (two columns of 64 px buttons inside the safe insets), not the exe's 450 x 360 checkbox dialog | modes-ui-shop 3 "Engine impact" | - |

## rules-shop-ui.json

| Key | Value | Missing | Meaning |
|---|---|---|---|
| shopUi.panel.longPressTicks | 50 | 0 = no long press (right click only) | hold time on Menu, 1/100 s; the same 50 as laterLevels.skip.longPressTicks (level skip) |

## Options (Mod/Unnamed/Options.h)

| Option | Exe flag / ini key / typed code | Effect in the port | Evidence | Conf |
|---|---|---|---|---|
| eliteZombies 0/1/2 | 0x800258 / SpZombies / INFZOM (+1 mod 3) | 1: every elite roll skipped (Day, Night, Pool, Fog incl. Jack/Balloon/Digger, Roof incl. Bungee/Ladder/Catapult, World 7 Tall-nut and Imp); 2: every type is elite (table "Elite option 2" below) | 0x7b2100 (option 1) nops/jmps the roll jumps at 0x7970f8 (485), 0x796166 (486), 0x796967 (499), 0x7969a9 (494), 0x796a64 (500), 0x7a62b0 (503), 0x79747e (490), 0x796ec0 (488), 0x796d2c (487), 0x796e17/19 (498), 0x7a1f53 (571); hook 517 (0x7a3081) clears +0x134 when option == 1; direct readers 482-484, 487, 489, 491, 496, 498, 501, 502, 508, 513 | H |
| doubleSun | 0x800110 / Sun / SUN | collected sun 15 -> 25, 25 -> 50, 50 -> 75; V2: the conveyor's countdown (Challenge+0x5c) and each packet's slide step 2 instead of 1 (x2 again at the HUD's 2x, the exe's Fast 0x800118), never below 0 | hook 204 (0x797c32) at `Board+0x5560 += value`; hooks 161 (0x422d17 -> 0x7a031a) and 473 (0x489c9c -> 0x7a0375) | H |
| autoCollect | 0x800114 / AutoCollecting / AUTO | coin types 1..6 not yet collected collect themselves | hook 207 (0x7982d0) | H |
| freePlanting | LawnApp+0x814 / Free / FREE | vanilla `mEasyPlantingCheat` | hook 80 dialog fill (0xb73de0), hook 138 | H |
| closeDoor | 0x8001a4 / Shutdoor | a zombie at the house does not end the game | hook 630 (0x7a0281) | M |
| freezeZombies | 0x800250 / - / STOP | zombies do not walk | hook 603 (0x7a0c21) | M |
| treePower (default on) | 0x800254 ^ 1 / Wisdom / HARDWS | Tree of Wisdom plant HP buff (hook 268) on/off | 0xb73de0 `DAT_00800254 ^ 1`; hook 268 | H |
| Win this level (button, not stored) | WIN | `FadeOutLevel` (Board+0x5600 = 600) on a non-survival level | hook 138 0x79b0a0 | M |

### R8 rows (feature `extraOptions`; study the research notes (r8-options))

Read from the **live** dialog (builder 0xb76c02, listener 0xb75c02, fill 0xb73de0, apply 0xb73f00). The exe also holds
an older copy (builder 0xb7393b) that nothing calls; it is the only writer of 0x800298. Without `extraOptions` the
panel shows the 7 rows above (+ CARD) and every R8 effect is off.

| Option | Exe flag / ini key / typed code | Effect in the port | Evidence | Conf |
|---|---|---|---|---|
| gravestones 墓碑模式 | 0xc113a8 / (FogFullScreen) | Grave Danger's wave rules on any level: a flag wave (not the last) raises zombies from the graves, after wave 5 a wave adds graves (`ModesGraveDangerGraves`) | hook 182 0xc11373 `cmp [0xc113a8],1; je 0x4268f8` (ZF set = the mode test passes); label 0xb72db3 `push 0xc1139f` "[quote not included]"; community S3 (1.3beta1: "[quote not included]") | H |
| noSpawnLimit 无限制出怪 | 0x800278 / Unlimited / HARDSP | PickZombieType skips the first-allowed-wave and points checks (the level's allowed list stays) | hook 42 0x7a93a1 (at 0x40d911, before the Pogo/Bobsled/Air Raid test, jumps to the weight code 0x40d984) | H |
| daveNoPick 戴夫不选卡 | 0x800450 / DaveChooseNot | Dave picks nothing; never at 7-5 (65) / 7-10 (73); seeds he picked are freed (hover, tap, tooltip) | hook 436 0xc13410 -> 0x95b7ba; hook 447 0xc03630 `mov byte [ecx+0x38],0` | H |
| spawnForward 刷新点前移 | 0x80027c | no +133 start; Pole 822, Zamboni 800, Catapult 825, Gargantuars 845 (= Unnamed base - 133) | hooks 480 0x959500, 492 0x95952f, 495 0x959549, 497 0x959563, 512 0x95957d | H |
| rain 下雨模式 0/1/2 | 0x80011c / Rain / RAIN | 1: the rain of It's Raining Seeds / Stormy Night (falling rain, splashes); 2: plus the stormy night's darkness and lightning. Looks only, no rain sound (InitLevel is not hooked) | hooks 117 0x7a064c, 163 0x7a06da, 164 0x7a05aa, 185 0x7a05fe, 186 0x7a069a; RAIN 0x79b797 cycles 0..2 | H |
| fullFog 全屏浓雾 (port row) | 0x800298 | fog from column 0 in fog stages (OR-ed with `fogLevels.fullFog`); the top bar / seed bank item then draws just above the fog | hook 145 0x7a8310; writers 0xb73355 / 0xb7345c only in the dead dialog copy, so unreachable in 1.3beta2 | H (reading), port addition (row) |
| Save game / Load game (buttons, in a level) | 0xb72a6b / 0xb72b06 | Save = LawnSaveGame to `<mode save>.quick`; Load (only after a save this run) = TryLoadGame without the continue dialog, board paused under the open panel | 0xb72a00 (0x408c30 TryToSaveGame), hook 769 0xb72ac1 -> 0x44f7a0 TryLoadGame with magic 0x114514, hook 244 0xb72a8b skips DoContinueDialog 0x450220 | H; own file = port ruling (PvZ-Portable saves the mode file on every pause) |

Rules added with R8 (`rules-day-zombies.json`, the start x the port had missed, hooks 495 / 497 / 512):
`dayZombies.zamboni.startX` 933 (vanilla 800), `dayZombies.catapult.startX` 958 (825), `dayZombies.gargantuar.startX`
978 (845); the type per site is matched by the vanilla constant (M), the values are H.

Mac evidence (2026-11-23, hidden runs, 1300 x 600, seed 7, app plan9-r8):

- Panel (4-1, long press on Menu, safe left 57): 13 rows + Mod plants in 3 columns, footer Win / Save game /
  Load game / Done, Rain shows "Storm" in green.
- Rain 1 on 2-5: falling rain and splash rings; rain 2 on 1-3: dark lawn, lightning flash fading (frames 2050..2700).
- 5-8 with closeDoor: default waves 1-3 Normal/Cone; noSpawnLimit: a Gargantuar in wave 1, start x 980-982
  (978 + Rand); + spawnForward: Gargantuar 846-847, Normal 805, Cone 814-819 (no +133). Vanilla mode with the
  same `-pvzu-dev-options`: Normal at 791, budget 1 (unchanged).
- 1-4 gravestones + free planting + autoplay: 0 graves to wave 5, 5 at wave 7, 15 at wave 9 (5 per wave after 5).
- 2-2 second run (`-pvzu-dev-finished 1`): Dave picks 3 seeds; with daveNoPick the bank is empty.
- 1-3 quick save at app frame 2650, load at 5150: `quick save ok=1`, `quick load ok=1`, the file
  `game1_0.v4.quick`; after the load the first wave spawns again at board time 1800 with the saved zombie ids
  (#6..#8), the game runs on after the panel closes.
- 4-1 full fog (option): `leftFogColumn=0 source=rule fullFog=1`; the top bar and seed column stay visible (an overlap
  was not reproduced at 1300 x 600, zoomed or `-pvzu-dev-zoom 1`; the HUD item now draws above the fog anyway).

Not ported (open): FAST = the HUD 1x/2x button already (hook 167, one extra update per frame); Legendary Zomboss
(0x8001a8, hooks 633, 648, 664, 733-759); "hardplus" extra elites (string only, U4).

## Elite option 2 ("all elites")

Read with radare2 from the exe (nothing run), 2026-11-23. The option reaches the rolls two ways:

- **setting** (patched code): every way of changing the option (typed INFZOM 0x79b375, the panel 0x7a8cb6, the dialog
  0xb734f0 / 0xb74050) first calls 0x7b2200 (restore), then 0x7b2100 (option 1) or 0x7b2000 (option 2), which rewrite
  the roll code bytes in .NewSec. The port: `engine::EliteOption()`.
- **value** (`[0x800258]` read when the zombie is made): equal to the setting, except while a staff Giga adds its
  thrown zombie (0xc1152c: `push [0x800258]; mov [0x800258], 2`, hook 565), where it is 2 and the patched code still
  follows the setting. The port: `engine::EliteValue()` and `EliteValueAllScope` (Mod/Engine/OptionsPanel.h), now for
  every world's direct reader (before, only the Roof rolls saw the Giga's 2). Almanac pictures (value 1, hook 415) and
  the 7-10 boss Newspaper (0xc11030) do not roll in the port.

| Type | Option 2 in the exe | How | Rule keys | Conf |
|---|---|---|---|---|
| Normal / Ducky Tube | Rand(4): 0 sticky, 1..3 coin; I, Zombie: coin 0x105, nothing drawn | value: 0xc11160 `cmp [0x800258],2` (Rand(4) not Rand(8)); 0xc111c7 | dayZombies.normal.rollRangeAllElite 4 | H |
| Conehead | Rand(2) + 2: phonograph / Dancer head | value: 0x795fbb `mov al,2` | dayZombies.cone.rollRangeAllElite 2 | H |
| Buckethead | Rand(2) + 4: pumpkin / umbrella | setting: 0x7b201c `[0x7970ec] = 2` (Rand(9) -> Rand(2)) | dayZombies.bucket.rollRangeAllElite 2 | H |
| Pole Vaulter | Rand(13) (sky drop Rand(10) + 3); 3..9 road sign 0x29 in every world | value: 0x7a1b91 `test bl,bl` (13 not 22), 0x95af49 `test bl,bl` skips the world-7 check | dayZombies.pole.rollRangeAllElite 13, skyDropRollRangeAllElite 10 | H |
| Newspaper | Rand(4): 0..1 football head, 2 Almanac paper (no level gate), 3 knife | value: 0xc05771 `cmp eax,2; setne al; add eax,4`; 0x7a1a16 `cmp eax,2; je 0x7a1a37` | nightZombies.newspaper.eliteRollRangeAllElite 4 | H |
| Screen Door | Rand(5) drawn, always the Tall-nut door | setting: 0x7b202f `[0x796166]` jne -> jo | - | H |
| Football | never plain: profile level <= 60: Rand(16) < 13 green (then gold Rand(13), extra Rand(3) unless gold), else gold; > 60: Rand(40): 0 gold, 1..13 green as before, 14..39 gold Rand(13) != 0 black, == 0 gold then Rand(3) < 1 gold + black (900 / 2200) | value: 0xc12afd .. 0xc12b5f, 0x9dd37a .. 0x9dd419, 0xc12500, 0xc12c50, 0x9dd423 | nightZombies.football.allEliteRoll 16, allEliteGreenBelow 13, allEliteRollAbove60 40, allEliteGreenMaxAbove60 13, allEliteBlackExtraBelow 1; world7Zombies.football.goldBlackBodyHp 900, goldBlackHelmHp 2200 | H (flow), M (black needs world7Zombies) |
| Dancer | Rand(15): 0..2 random summoner, 3..6 trophy, 7..14 moonwalker, also in I, Zombie | value: 0x79683c `test bl,bl` (15 not 60); 0xc043eb `cmp [0x800258],2; je 0x79686e` skips the I, Zombie check | nightZombies.dancer.eliteRollRangeAllElite 15 | H |
| Snorkel | Rand(4) drawn, always lotus | setting: 0x7b2042 `[0x796967]` jne -> jo | - | H |
| Dolphin Rider | Rand(3) drawn, always football head | setting: 0x7b204b `[0x7969a9]` jne -> jo | - | H |
| Zomboni | orange, nothing drawn (not in mode 0x89 / adventure 65) | value: 0x95a40d `cmp [0x800258],2; je 0x95a428` | - | H |
| Jack-in-the-Box | Rand(2): ice / potato (not in Vasebreaker) | setting: 0x7b2054 `[0x796a58] = 2` | fogZombies.jack.eliteRollAllElite 2 | H |
| Balloon | Rand(7) drawn, always the cloud (not in I, Zombie) | setting: 0x7b205e `[0x7a62b0]` jne -> jo | - | H |
| Digger | Rand(5) drawn, always the screwdriver, then Rand(3) surfacing (not in I, Zombie) | setting: 0x7b2067 `[0x79747e]` jg -> jo | - | H |
| Pogo | Rand(2) (was ported) | value: 0x796c08 | fogZombies.pogo.eliteRollAllElite 2 | H |
| Bungee | Rand(3): 0 / 2 wheelbarrow, 1 Jack head | setting: 0x7b207a `[0x796eb4] = 3` | roofZombies.bungee.eliteRollAllElite 3 | H |
| Ladder | shovel on Rand(4) < 2; else the second roll Rand(2): pile / ghost (>= 5 plants) | setting: 0x7b2084 `[0x796d2c]` jne -> jge; 0x7b20a4 `[0x95aa1f] = 2`; value 1 still skips the second roll (0x95aa15) | roofZombies.ladder.shovelBelowAllElite 2, secondRollAllElite 2 | H |
| Catapult | Rand(100) < 83 pole head; 83..99: vase 0x70 with profile level > 60, else pole head | setting: 0x7b208d `[0x796e16] = 0x53` (83), 0x7b2094 `[0x910002] = 100`; value: 0x91009b `cmp [0x800258],2; je pole head` | roofZombies.catapult.poleHeadBelowAllElite 83, poleHeadAllEliteBelowAllElite 100; world7Zombies.catapult.vaseRollFromAllElite 83, vaseRollBelowAllElite 100 | H |
| Gargantuar staff | always 0x106 (was ported) | value: hook 513 0xc116a2 | - | H |
| Imp (world 7) | Rand(3) drawn, always lands as a Gargantuar | setting: 0x7b209b `[0x7a1f53]` jne -> jo | - | H |
| Tall-nut head | always 0x101 (was ported; now reads the value) | value: hook 508 0xc033a8 | - | H |

Correction (2026-11-23): this file said "2: Catapult < 60" and the port modelled option 2 for the Catapult as pole head
below 60 and Rand(4) for the Ladder's second roll. That is what the *value* 2 does without the patch (a Giga's thrown
zombie); the *setting* 2 also patches 0x796e16 (83) and 0x910002 (100) and the Ladder's 0x95aa1f (Rand(2)).

Patched rolls still draw their Rand with option 1 in the exe (0x7b2100 patches the jump after the call); the port skips
the draw there (unchanged, open).

## Shop, Zen Garden, Almanac, save

| What | Port | Evidence | Conf |
|---|---|---|---|
| Prices | vanilla `GetItemCost` unchanged | .text 0x48c620 table = vanilla (modes-ui-shop 4) | H |
| Slot upgrades | sold out at 9 (15 slots), already in `Mod/SeedSlots.*` | .text 0x48a9e9 `cmp [ecx+0x214], 9` | H |
| Zen glove | does not pick up a Squash whose state != 0 | hook 478 (0xc02f10) | M |
| Almanac | ZomBotany names (Plan 7), preview zombies never roll (Tall-nut fixed here) | hooks 9/10, 415 (0xc10880 sets 0x800258 = 1) | H |
| Save | options live in the settings file, not in saves | modes-ui-shop 7 | H |
