# overlay-en-skip.txt: how it was made

Written 2026-11-22. `overlay-en-skip.txt` lists the imported Unnamed files that English mode must **not** serve, so
the engine falls back to the vanilla file in `main.pak` (`Startup.cpp` loads the list, `AssetOverlay.cpp` leaves those
paths out of the index). Chinese mode ignores the list.

Rule for a line: the file (a) differs from the vanilla file of the same path and (b) differs only because of
language (baked Chinese text, or art drawn to fit Chinese text). Anything that carries new game art stays served.

## Counts (2,505 files in `assets/`, `import-manifest.json` included)

| Result | Files |
|---|---|
| identical to vanilla (same path, same bytes) | 2,036 |
| only in Unnamed (no vanilla file with that path or image stem) | 94 |
| differs (same path 364, plus 11 where Unnamed has `.png` and vanilla `.jpg`, or the reverse) | 375 |
| of those, in the skip list | 82 (22 font files + 60 images) |

The 375 that differ: 248 `compiled/*.compiled`, 22 `data/` font files, 65 `images/`, 38 `reanim/`, 2 `properties/`.

## Method

1. the research notes (enskip_compare) (run with `python33 -I`, which has Pillow + numpy) reads
   `main.pak` (XOR 0xF7), matches every assets file case-insensitively by path, and
   for images with no same-path file by stem across `.png/.jpg/.gif`. Images that both decode are compared per pixel:
   share of RGB pixels changed, share of alpha changed, bounding box of the change, and sizes.
2. Every differing image was looked at side by side (vanilla | Unnamed) with the research notes (enskip_sheet),
   which composes PopCap alpha files (`<name>_.png`, `_<name>.png`). Sheets were made in the session scratchpad and
   deleted after viewing.
3. Pairs were checked: every skipped colour file's alpha partner is either skipped too (`PvZ_Logo_`,
   `ZombiesWon_`, `Credits_wearetheundead_`) or identical to vanilla (`Tombstones_`, `SelectorScreen_BG_Right_`).
   Every skipped font `.txt` has its glyph image either identical to vanilla or skipped as well.
4. All 82 lines were checked to exist in `assets/` with the exact case, and to have status "differs".

The engine tries `.png` before `.jpg` and asks the overlay first for each one. Skipping an Unnamed `.png` whose vanilla
twin is a `.jpg` therefore still ends at the vanilla `.jpg` (`SelectorScreen_BG_Right` is the one case in the list).

## Fonts

Vanilla has all 42 `data/` font files, and Unnamed has the same 42 names. 22 of them differ: every font `.txt`
descriptor (Unnamed re-ordered or re-mapped the character lists and widths), plus `HouseofTerror28.png` (4295x200
against vanilla's 4295x54) and `_HouseofTerror16.png` (2495x80 against 2495x32). The other 20 are byte-identical
(for example every `DwarvenTodcraft*.png`, `_BrianneTod*.png`).

**Recommendation: English mode uses the vanilla fonts. All 22 differing `data/` files are in the skip list.** No
vanilla font is missing, and `strings/en.txt` uses only ASCII in its values (the only non-ASCII bytes are 13 Chinese
key names), so vanilla glyphs cover every English string.

Font files with no vanilla counterpart are left alone (not in the list): `font/font1-6.bin/.dds` and `fonts/*.ttf`
(`fzcq`, `fzjz`, `fzkt`, `FZKTK`, `fzyh`, `ark-pixel-12px-proportional-zh_cn`, `NotoColorEmoji-Regular`). The GOTY
engine never asks for them, so they cost nothing in English mode; keep them for a future Chinese TTF renderer.

The 22 skipped font files:
`BrianneTod12.txt`, `BrianneTod16.txt`, `BrianneTod32.txt`, `BrianneTod32Black.txt`, `ContinuumBold14.txt`,
`ContinuumBold14outback.txt`, `DwarvenTodcraft12.txt`, `DwarvenTodcraft15.txt`, `DwarvenTodcraft18.txt`,
`DwarvenTodcraft18BrightGreenInset.txt`, `DwarvenTodcraft18GreenInset.txt`, `DwarvenTodcraft18Yellow.txt`,
`DwarvenTodcraft24.txt`, `DwarvenTodcraft36BrightGreenInset.txt`, `DwarvenTodcraft36GreenInset.txt`,
`HouseofTerror16.txt`, `HouseofTerror20.txt`, `HouseofTerror28.png`, `HouseofTerror28.txt`, `_HouseofTerror16.png`,
`Pico129.txt`, `Pix118Bold.txt` (all under `data/`).

## What is skipped (images, 60)

- Main-menu tombstones (开始冒险吧 / 冒险模式 / 玩玩小游戏 / 解谜模式 / 生存模式), with their highlights.
- Wooden sign (its welcome and not-your-save lines), vases (帮助 / 选项 / 退出), almanac book (图鉴), shop key (商店), Zen
  Garden can (禅境花园), and the menu's right-hand tombstone carved 汉化第二版.
- Title logo (植物大战僵尸 无名版), the shop sign and its NEXT/PREV buttons, the Zen Garden shop button.
- Ready / Set / Plant!, Final Wave, The Zombies Ate Your Brains, the level-progress bar label, the seed-chooser
  almanac icon, the gravestone epitaphs on the top row of `Tombstones.jpg`.
- All seven zombie notes and the three credits text images.
- The bobsled lettering (see the borderline cases).

## What differs but is kept (not language)

- Gameplay art: `ice.png`, `ice_cap.png`, `ice_sparkles.png` (dark red ice), the pool set and `background3/4`
  (water), `seeds.png` (650 wide: new packets), `packet_plants.png` (one icon replaced), `Zombie_ladder_*` (wooden
  ladder), `Zombie_head.png`, all 94 new files (elite football, cones, hurrikale, poison pea, knife, target, ...).
- Widened screens with no text in them (1068x600 or wider, vanilla 800x600): `titlescreen.jpg`, the three almanac
  backs, `Challenge_Background.jpg`, `AwardScreen_Back.png`, `Background_Greenhouse.jpg`,
  `Background_MushroomGarden.jpg`, `aquarium1.jpg`, `Store_Background*.png`, the `Store_Car*` set,
  `reanim/tree_bg.jpg`, `SelectorScreen_BG.jpg`, `SelectorScreen_BG_Center.jpg` + `_`.
- `compiled/*.compiled` (248): differ even after decompression. Not language, and the engine never reads them through
  the overlay anyway (`Definition.cpp` opens compiled files with `std::ifstream` from the app-data cache or a loose
  path, not through `PakInterface`). With no `.reanim` XML in Unnamed, the menu layout stays vanilla's.
- `properties/*`: `AssetOverlay.cpp` never serves them; Chinese text goes through StringOverlay.

## Borderline cases and the decision taken

| File(s) | What the pixels show | Decision |
|---|---|---|
| `images/Zombie_bobsled1-4.png` | Frame 1: only the BRAINS OR BUST lettering differs (3.7% of pixels, all inside the lettering box). Frames 2-3: the same lettering change, with the whole sled moved up 6 px (and 3 px left on frame 3). Frame 4: also moved 4 px left and 12 px up. No new painting. | **Skip all four**, so the lettering stays the same through every damage frame and English mode matches GOTY. This goes against the brief's "keep bobsled": the evidence shows a language change plus a re-alignment, not new art. To keep Unnamed's alignment, delete these 4 lines (the sled then reads in Chinese). |
| `reanim/SelectorScreen_BG_Right.png` | Carved 汉化第二版 on the tombstone base, and also redrawn 1066 wide (vanilla .jpg 730) with an extra wall and grass on the right. | **Skip**: it is the 汉化第二版 label seen on the phone, and the menu layout is vanilla's anyway. The cost is that the main menu's right edge goes back to vanilla. |
| `images/PvZ_Logo.jpg` + `PvZ_Logo_.png` | Chinese title logo with the 无名版 badge. | **Skip**: language. English mode loses the "Unnamed" mark on the title; if you want one, it should be an English badge of our own. |
| `reanim/Zombie_questionmark.png` | Vanilla "?" (24 px wide); Unnamed's is 272 px wide, the "?" plus a Chinese joke line, not a translation. | **Skip**: only Chinese readers get the joke. An English rewrite would be our own art. |
| `reanim/SelectorScreen_Shadow_Adventure.png` | No text; the shadow is drawn to the Chinese button's shape (337x126, vanilla 350x150). | **Skip**, together with the button it belongs to. |
| `reanim/SelectorScreen_Adventure_button/_highlight.png` | 冒险模式, with the LEVEL plate moved to the bottom right (vanilla: top). | **Skip**: the code draws the level number where vanilla's plate is. |
| `reanim/SelectorScreen_WoodSign3.png` | No text in Unnamed: a broken plank (92x40) where GOTY has the ZOMBATAR! sign (279x83). Unnamed is built on the pre-GOTY game, which has no Zombatar. | **Keep** (not language). Whether English mode should offer Zombatar is a feature question, not an art one. |
| Font `.txt` files whose glyph image is identical (`DwarvenTodcraft*`, `Pico129`, `Pix118Bold`, ...) | Descriptor rewritten, picture unchanged. | **Skip** the descriptor: vanilla metrics belong to the vanilla picture. |
| Widened menu backgrounds (`titlescreen`, almanac/challenge/award/store backs, `SelectorScreen_BG_Center`) | Redrawn wider, with no text in them. | **Keep** (not language). Separate issue: menus are 800x600 in this engine, so these may be cropped or misplaced in both languages. |
| `images/Tombstones.jpg` | Only the top row's epitaphs changed (已辞世, 与世长辞, ...), 1.1% of pixels; alpha identical. | **Skip**. |

## Update 2026-11-22: overlay-skip-always.txt

A phone test showed two of the "kept" groups above only fit Unnamed's own exe: `seeds.png` (13 cells, Unnamed's
resources.xml `cols="13"`, GOTY says 9, so packets drew 72 px wide) and the widened menu backs (vanilla layout at
x 134 inside, so boxes moved right of their text). They are now in `overlay-skip-always.txt`, which every language
skips. `SelectorScreen_BG*` and `AwardScreen_Back.png` stay served (they line up at x 0).
