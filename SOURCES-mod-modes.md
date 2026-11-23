# Sources: mod-only game modes 0x65-0x94 (modes.json, strings/en-corrections-mod-modes.txt, feature `modModes`)

Study (source of truth): the research notes (modes-ui-shop) 2.3, 9 and Final table A, plus a per-mode read of the hooks done
for this pack on 2026-11-23 (exe the Unnamed 1.3beta2 `PlantsVsZombies.exe`, read only through
the research notes (hooks2), the research notes (modes_)*.py` and static radare2; nothing run). Code: `app/src/Mod/Unnamed/ModModes.*`
(table, zombie list, name colour, list layout); `tools/gen_mod_modes.py` writes `data/modes.json` from the spec tables and `tools/mod-modes-status.json`, `app/src/Mod/Unnamed/ModModeRules.*` (pure rules), `app/src/Mod/Engine/
ModModes.cpp` (generic engine sites), `ModModeRules.cpp` (per-mode sites), `ModModesScreen.cpp` (the list on the challenge
screen); tests `app/tests/test_mod_modes.cpp` (its last test compares this pack's `data/modes.json` with the exe tables,
transcribed separately in the test) and `app/tests/test_mod_mode_rules.cpp`.

In the exe a mod mode is just `LawnApp::mGameMode` = 0x65..0x94. The 1051 code treats it as a generic challenge
(`IsChallengeMode`, .text 0x453710) and the mod's hooks add each mode's rules. The port does the same: the engine keeps
its vanilla paths and asks `Mod/Engine/ModModes.h` at each site (all guarded by the feature and the mode).

## modes.json fields (one row per mode, keyed "0x65".."0x94")

| Field | Meaning | Evidence | Conf |
|---|---|---|---|
| `name`, `nameZh` | English translation / the exe's name | GBK at 0x850000 + (mode-0x65)*0x10, assigned by hook 12 (0x799120, the global `std::string(const char*)` override while mode >= 0x49) | H |
| `background` | engine `BackgroundType` = exe `Board+0x554c` | hook 25 (0x79a5fb in `Board::PickBackground`): `cmp [app+0x7f8],mode; mov [board+0x554c],bg` per mode | H |
| `waves` | `mNumWaves` | hook 20 (0x79a201 in `Board::PickZombieWaves`) jumps to the vanilla stores 0x409394 (20), 0x40946c (30), 0x409460 (40), 0x409478 (0), 0x409489 (10); 0x91 -> 0xc03160 (60), 0x92 -> 0xc05ca0 (25) | H |
| `allowed`, `normal`, `pail` | zombie list: Normal (unless `normal` false), the mode's own types, Cone when the mode has no list, Pail when `pail`; Yeti follows Pail | hook 180 (0x79ac00, from .text 0x425cad in `Challenge::InitZombieWaves`' last branch) and its continuation 0x7a5a00 -> 0xc00900 -> 0xc00d20 -> 0xc02e10 -> 0xc05260 -> 0xc03110 -> 0xc00958 -> 0x7a5a3e..0x7a5e91; fall-through 0x7a5e96 writes Cone; exits 0x79af0d keep the vanilla Pail write, 0x79af0b (`xor ebx,ebx`) writes Pail and the Yeti line false; 0x79 and 0x85 write Normal = BH = 0 | H |
| `startSun` | start sun (absent = 50) | hooks 30/31 chain 0x7981a0 -> 0x7a2385 -> 0xc00670 -> 0x95c0e0 -> 0xc12fd0 -> 0xc05cc0: 0x73 1000, 0x7f 200, 0x80 2000, 0x83 500000, 0x8a 200, 0x8c 6750, 0x92 500 | H |
| `seedSlots` | `GetNumSeedsInBank` (absent = 6 + upgrades) | hook 141 (0x7a8741: 0x7d, 0x8f -> 1), hook 142 (0x799717: 0x72 -> 1; 0x73, 0x91 -> 1 via 0xc030b0; 0x89 -> 3; 0x87 -> 7; 0x76 -> 9) | H |
| `chooser` | seed chooser shown | hooks 35 (0xa878f1) / 36 (0x7a6c30) sit in `Board::ChooseSeedsOnCurrentLevel` (.text 0x40bd30, static r2 read of the function: 0x13/0x47/0x48 tests, bowling, squirrel, scary potter, conveyor...), false for 0x8b and 0x76/0x79/0x8d/0x8e. The triage's "InitLawnMowers" label is wrong: mowers are vanilla | H |
| `conveyor`, `conveyorSeeds` | conveyor bank and its seeds/weights | hook 140 (0x799d21, `HasConveyorBeltSeedBank`): 0x71, 0x81, 0x84; hook 162 (0x799e01, `Challenge::UpdateConveyorBelt`): 0x84 Hypno-shroom 80, Lily Pad 16, Blover 4; 0x81 Sprout 90, Cherry Bomb 5, Grave Buster 5; 0x71 Repeater 20, Butter-pult (mod 0x72) 20, Potato Mine 9, Spikeweed 21, Ice-shroom 15, Magnet-shroom 15. The vanilla weight fix-ups after the list still run | H |
| `bank` | fixed packets of a no-chooser mode | hook 32 (0x7a6e94, `Board::InitLevel`): 0x79 Sunflower, Snow Pea, Marigold, Coffee Bean, Ice-shroom, Doom-shroom x2, Cherry Bomb, Squash, Potato Mine (first N packets = bank size) | H |
| `skySun` | falling sun | hook 94 (0x79a500 in `Board::UpdateSunSpawning`): none in 0x72, 0x74 | H |
| `graves` | 0 = no gravestones | hook 143 (0xc03180): 0x91; hook 144 (0x796531): background 1 except 0x6d | H |
| `firstWaveCountdown` | cs before the first wave | hook 160 (0x79a000 in `Challenge::StartLevel` after the Column block): 0x68, 0x74 5500, 0x72 250; hook 29 (0xc050ad): 0x92 7500 | H |
| `bannedSeeds` | chooser greys these (`SeedNotAllowedToPick`) | hook 425 (0x7b0f00, replaces 8 inline copies of the Last Stand filter): 0x66/0x78 Sunflower, Sun-shroom, Twin Sunflower, Sea-shroom, Puff-shroom (+ mod 0x51, 0x59 later); 0x67 Lily Pad, Tangle Kelp, Sea-shroom, Cattail; 0x70 Umbrella Leaf; 0x90 Squash | H |
| `nameColor` | level-name colour | hook 130 (0x7a3300 in `Board::DrawLevel`): red (194,19,37), purple (92,0,170), blue (20,126,220), green (10,204,20), pulse (v = mMainCounter & 0xff: v <= 127 -> (61,v,61) else (v/2+36,61,61)), else gold | H |
| `status` | `built` / `needsModPlants` (Plan 8 seeds 0x50-0x7f) / `unknown` (not built yet) / `placeholder` (0x93, 0x94 "[quote not included]") | this pack | - |
| `rules` | the mode's own constants (read with the exe value as default) | per mode below | H |

## Built modes: rules and evidence

| Mode | Rule (engine site) | Evidence | Conf |
|---|---|---|---|
| 0x65 Art Is an Explosion | a plant's first blink (instead of `DoBlink`) explodes it: zombies in its row within radius 100 of (mX + mWidth/4, mY + mHeight/2) take 300 (`TakeDamage(300, 18)`), Potato Mine particle, shake 12/3/-4, the plant dies, then `Rand(4) >= 2` drops a large sun (motion = the roll) and only then a second `Rand(4) >= 2` drops a sun (`Plant::UpdateBlink`) | hook 319 (0x7a45c0) + hook 155 (0x7a46d0: 300 damage only for the blink caller) | H |
| 0x67 No Playing in the Water | data only (bans above) | hook 425 chain 0xc02e95 | H |
| 0x68 War of Attrition | after a wave spawns with an even, non-zero `mCurrentWave`: background day <-> night (images only), every plant but Lily Pad / Flower Pot / Coffee Bean sleeps when `IsNocturnal(seed) != night` with the exe's list 8, 9, 10, 12, 13, 14, 15, 24, 31, 42 (after `SpawnZombieWave` in `UpdateZombieSpawning`); first wave 5500 | .text 0x413fdf -> 0x7995a1 -> 0xc05200 -> 0x7995a6 (not in hooks2; r2), IsNocturnal 0x794ac0; hook 160 | H |
| 0x6a Downstream | each bite (after `StartEating`) moves the plant `Rand(41)+40` px left; x <= -32 or a new cell that `CanPlantAt` refuses (column 8 excepted) destroys it; particles 0x46 / 0x42, foley 0xf / 8 | hook 679 (0x796560) | H (foley names M) |
| 0x6c Zombies Run Run Run | from wave 6 the zombie anim rate x (1 + 0.125*(wave-5)) (`ApplyAnimRate`, after the night rate); Zombiquarium lawn rows NORMAL POOL POOL POOL NORMAL DIRT (`laterLevels.rows.8`) | hook 662 chain 0x7a6b80 (float 0.125 = 0x3e000000); hook 27 | H |
| 0x6e Little Zombie, Big Trouble | V2: vanilla Little Trouble zombies (scale 0.5, body/helm/shield/flying HP / 4) and x7 zombie points before the Little Trouble x4 tail (= x28); keeps the seed chooser, loot and countdowns (`IsLittleTroubleLevel` 0x4538c0 is unpatched) | hook 516 (0x523ed2 -> 0x7a7b00: `cmp ecx,0x6e; jz 0x523eeb`), hook 21 (0x7a7836: `imul ecx,ecx,7` -> 0x409960) | H |
| 0x6f Force-8 Gale | from wave index 8: gust when the timer (Challenge+0x58) is 0: timer = `Rand(1500)+2500`, dir (Challenge+0x70) 0 -> +1, then flips; message style 4 for 250 cs. Each unblinking tick a plant rolls `Rand(36 - wave)`: 1 moves it 1 px with the wind; x outside 0..800 kills it, else `mPlantCol = PixelToGridX(mX + 40)` | hook 98 (0x7a69c1), hook 318 (0x7a6ab1); strings 0xa20140, 0xa20180, 0xa201a0 | H |
| 0x70 Troops from the Sky | every wave dropped by bungees as in Bungee Blitz (only that branch of `SpawnZombieWave`; chooser, countdown normal) | hook 89 (0x7a7a00) | H |
| 0x73 Seed Slot Crisis | 1 slot, 1000 sun; each planting re-rolls the packet `Rand(6)`: Sunflower, Potato Mine, Snow Pea, Repeater, Wall-nut, Blover, before the recharge starts (`SeedPacket::WasPlanted`) | hook 69 (0x799681) | H |
| 0x74 Rainy Day | vanilla rain (render item, `UpdateRain`, `DrawRain`) without lightning; no sky sun; first wave 5500; the exe sets `Color::White` to (100,100,100) every update | hooks 117 (0x7a064c), 164 (0x7a05aa), 185 (0x7a05fe), 94, 160, 103 (0x798c61) | H (dimming look M) |
| 0x75 Heisenberg's Zombie | a zombie at its lane's y is drawn in another row (`Rand(5)` re-rolled while equal), y = row*100+50, its hit box moved back (saved y/rect in the boss counters), `mRow` kept; then no more y steps; Pole in vault skipped; Boss and yucky-faced zombies vanilla (`UpdateZombiePosition`) | hook 615 (0x798e27) | H |
| 0x77 Upstream | every hit (also while dying) moves the zombie `min((damage>>1)+1, 160)` px toward the house (`TakeDamage` top) | hook 706 (0x7a6900, FSUBRP) | H (direction checked by two decodes; play-test once) |
| 0x79 Giant Crisis | no chooser, fixed 10-seed bank; list Gargantuar + Red-eye only; no first-wave / points test in `PickZombieType` | hooks 35/36, 32, 180 chain (BH Normal), 42 (0x7a93a1) | H |
| 0x7a Big Zombie, Little Trouble | every zombie: body, helm, shield HP x4, scale 2, not chilled (after the Little Trouble block in `ZombieInitialize`) | hook 517 -> 0x7961f9 | H |
| 0x7b Frequency Switch | from the first wave, every `Rand(201)+400` cs: plants hidden (f 1) / zombies and shadows hidden (f 2), alternating; no planting while zombies are hidden | hooks 104 (0x7a7c71), 118, 122, 124 (render switch 0x417358), 46 (0x7a7500) | H |
| 0x7c Light and Mist | fog from column 0; Planterns/Torchwood clear nothing; each visible sun coin clears radius 2 (sun) / 1 (small) / 3 (large) around (PixelToGridX(cx), (cy-90)/85) when 0 < cx < 750, 45 < cy < 600; Blover clears for 1 tick | hooks 145 (0x7a8310), 135 (0x7a8351), 342 (0x7a8450) | H |
| 0x7e Pincer Attack | V2: zombie points x((wave >> 3) + 1) then the x4 tail (hook 21, 0x7a7847). From wave index 6, 1 in 2 wave zombies spawned off the right edge (not Dancer, Bobsled, Digger, Yeti, Bungee) start at x 20 with `mHasObject`; every zombie with `mHasObject` walks backwards (Flag Zombie too, literal) | hooks 44 (0x7a8111), 642 (0x7a80b0) | H |
| 0x80 Limited Supply | V2: a planted packet stays grey (no countdown) until its plant is gone; then the first grey packet of that seed (an Imitater packet: its copy, for a plant from an Imitater) starts its full recharge. An Imitater's morph restarts nothing | hook 70 (0x7a8901) clears `mRefreshing`; hook 361 (`Plant::Die` 0x467a05 -> 0x7a8961/0x7a8966: skip when called from ImitaterMorph 0x466b89, loop packets, `mRefreshing = 1`) | H |
| 0x82 Sow Beans, Reap Melons | every tick: pea -> melon, snow pea -> winter melon, zombie pea -> melon (type only) | hook 402 (0x7a81e0) | H |
| 0x84 An Eye for an Eye | conveyor (Hypno-shroom 80, Lily Pad 16, Blover 4) | hooks 140, 162 | H |
| 0x85 Zombie Counter-Espionage | Cone + Digger only, no wave gate; a Digger that surfaces is hypnotised; hypnotised zombies also bite plants | hooks 42, 586 (0x7a85a0), 674 (0x7a8560) | H |
| 0x89 Glutton Star | the star snake of 7-5, same code (exe test 0x7aaee0 "mode 0x89 or level 65"): bank Starfruit / Sunflower / Wall-nut after the chooser, three stars from (120, 280); the Starfruit packet buys a star at the tail; W / A / S / D steer; stars fly through zombies; the head off x 0..899 loses. Day lawn, 30 waves, start sun 50 (no 0x89 sun rule), no orange Zomboni (hook 496). Engine: `Mod/Engine/Level65Snake.*`; full rules and addresses in SOURCES-special-levels.md "7-5" | hooks 462 (0x7a2230), 467 (0x7a20f9), 138 (0x79b3d2), 401 (0x7a1fc1), Die cave 0x6511e3; study the research notes (glutton-star) | H |
| 0x8a Invisible Guardian | V2: only plants start invisible (hook 2 sits in `Plant::Plant` 0x401b20, not GameObject); at chooser close the bank is shuffled (2n swaps of two different `Rand(n)` packets, Imitater resolved to its copy) and every card but Sunflower 1, Sun-shroom 9, Twin Sunflower 0x29 is hidden with `mRefreshTime = 0` (hidden cards still work); start sun 200. 0x798dc0 / 0x79abb3 / 0x798df1 have no reference (dead code) | hook 2 (0x798d91), 0x79849e -> 0x798f01 (shuffle), 0x798f90 (hide) | H |
| 0x86 Leaning Left | every zombie's attack rect x -250 at spawn | hook 518 (0x7a92e1) | H |
| 0x66 Sun Storm | sky sun: countdown `min((unsigned)t >> 1, 450)` after the vanilla roll, always a large sun; a falling large sun is "charged" (Coin+0x68 = 1, its reanim filter LESS_WASHED_OUT) and landing clears it; clicking a charged sun hides it, Doom particle, Cherry Bomb foley, and every zombie with `abs(mY - cy) <= 120` and every plant with `abs(mY - cy) <= 100`, both with `mX - 125 <= cx <= mX + 130` (cx, cy = round(pos) - 30), takes 270 (plants via HP, dying at 0); no sun is paid | hooks 95 (0x7990d0), 205 (0x798670), 206 (0x798901), 208 (0x798721) | H (look of the charge M) |
| 0x6d Night Terror | at "Let's Rock": 25 permanent craters (rows `..XXX.XXX`, `..X.X.X..`, `..X.X.XXX`, `..X.X...X`, `XXX.XXXXX`), rows 1-4 dirt (zombies and the mower only in row 0, cells still plantable); the forward walk follows the crater path (x thresholds 660/655, 495/500, 340/335, 175/170; holds while the row changes; row 2 walks right); y steps 0.1875 px when 1+ px away; zombie body/helm/shield x (mCurrentWave + 4) / 4; no elite rolls; no gravestones | hooks 462 (0x7962d5), 604 (0x7989c0), 616/617, 517 (0x7a3081), 144 | H |
| 0x72 Lone Wolf | after the chooser: sun 0, one packet that is always Ice-shroom, a Peashooter at (0, 0) with launch rate 50; Up/Down (phone: tap a row or swipe, port addition) move it one row; a dropped head pays ZombieValue x 5 sun, then one upgrade step Peashooter -> Snow Pea (100) -> Repeater (750) -> Threepeater (2000) -> Gatling (5000), launch rate 50 (Repeater 64, Gatling 96); first wave 250 cs with the "use the arrow keys" message; vanilla zombie HP halved | hooks 462 (0x7983b6), 138 (0x79b0a0), 596 (0x7984c1, 0x798629), 160, 517 (0x799787) | H |
| 0x73 Seed Slot Crisis (correction) | the one chosen packet becomes six copies after the chooser, refresh times 0 (0xc030e0 sends 0x73 through 0x91's block); each then re-rolls when planted | 0xc030e0 -> 0x798fdf | H |
| 0x78 Sunflower Commander | a Sunflower (100 HP, launch rate 400, off the grid) follows the cursor (mouse - 40) in the row under it; when it is gone the level is lost (the port calls ZombiesWon) | hook 104 (0x7a7580) | H |
| 0x7f / 0x90 Trick of Tricks (1, 2) | a Squash smash that hits no zombie with a head adds 1 (Challenge+0x24, here mChallengeScore); from 15 each miss drops a money bag (coin type 0x12 = the level award: collecting it wins, V2 check of the community's "instant win"); fewer than 15 when the final wave comes = lost; start message "Trick the Squash 15 times before flag 4" (style 4, 500 cs); HUD "Squash tricked: n/15" at x 660 (645 from 10), y 60, red; 0x90 also starts with 15 Squashes on columns 0-2 | hooks 96, 234, 243, 296, 297; 0xc02eb0 | H (HUD colour order L) |
| 0x88 Territorial | the first plant on a cell claims it (Imitater never); a claimed cell takes only that seed, Lily Pad, Grave Buster, Pumpkin (and mod 0x5b / 0x6e); the Art Challenge ghosts show claimed empty cells; no art win | hooks 38 (0x7a8a21), 168, 170, 174 | H |
| 0x8b Bullet Carnival | the player is a Kernel projectile that follows the cursor; it eats one bullet of a lower or equal tier per tick for (tier+1)^2, grows at 5/18/60/210/650/1300/2600/4200/6500/8000 (Kernel, Puff, Pea, Cabbage, Star, Spike, Basketball, Butter, Melon, Winter Melon, Cob), the Cob wins; a bigger bullet kills it (an invisible zombie at x -100 ends the level); every 8 ticks a bullet comes in from an edge, weights 800 - 80 abs(d) near the next tier; young bullets (< 300 cs) do not die off-screen; a 40 x 10 score bar under the player | hooks 159 (0xa8727e), 165 (0x7b8a66, tables 0x8f3464 / 0x8d3464), 127, 219, 229, 376, 379 | H (bar colours L) |
| 0x91 All the Same One | 1 pick, then six packets of it (the Imitater's copy), refresh 0; sun 0x70000000 every update, shown "Unlimited"; upgrade plants need no base, every requirement met; no gravestones; 60 waves | 0x798fdf, hooks 53, 153, 471, 143 | H |
| 0x92 Elite Zombies' Challenge | every wave slot spawns a Dancer as the White-light Dance King (0x104); with the "Zombie Sea" box (seed chooser) all 50 slots spawn; first wave 7500 cs | hooks 29, 90, 100, 469 | H |
| 0x71 The Counter | conveyor with the mod Butter-pult 0x72 (weight 20); at most 6 plants | hooks 140, 162, 46 chain 0x7a7532 | H |
| 0x76 Schrodinger's Zombie | fixed 9-packet bank with Golden Sun-shroom 0x59 third; a dying zombie stays hittable and a hit revives it; corpses of types >= 5 (not Zamboni, Bungee, Catapult, Boss) never fade | hooks 32 (0x7a6e00), 714, 706, 725 | H |
| 0x7d Random Vasebreaker | 35 "?" vases off columns 0-1, each `Rand(65)`: 0 sun, 1..32 (not 26) zombie r-1, else a seed `Rand(128)` re-rolled while Imitater, Sprout, 53..79 or an empty mod row; no leaf vases; one slot | hooks 158, 187 (0x7a8611, 0x7b2350), 141, 166, 53 | H |
| 0x81 Luck | Sprout belt (90/5/5); a Sprout from the belt plants an Imitater of a random plant (the existing mod-plant rule) | hooks 140, 162, 67 | H |
| 0x83 Dr. Second-Master's Revenge | the 7-10 giant Newspaper boss when wave index 10 starts (0x7aa100 counts mode 0x83 as level 70); the waves go on to 40; start sun 500000 | 0x7aa100, 0x7a07be, hook 101 | H |
| 0x8c I Am Luck | an I, Zombie level: 45 Imitaters over all nine columns, one packet (Imp card) that places a `Rand(33)` zombie, Zomboss 500 HP, start sun 6750; an Imitater with no copy picks `Rand(128)` until the exe's table 0xc003ce allows it (vanilla 0-47, 49, 50, 52 and 22 mod plants) and in 0x8c its cost is taken from the sun | 0xc002e0, hooks 191, 194, 195, 348 (table read from the file), 505/506 | H |
| 0x8d Glove War 3 | ten plants in columns 0-1, ten packets of their +80 forms; a packet click swaps its lawn plant to the other form (cost of the new form, refresh + the old HP lost, the old HP added), or plants it at (0, 0) with refresh + 3000; the glove (item mode 4); upgrade plants need no base. The click is taken only after vanilla's own packet tests: `SeedPacket::MouseDown` jumps to 0xc007d0 at 0x488dae, past mActive, `CanTakeSunMoney(GetCurrentPlantCost)` (0x48880d / 0x488816), `PlantingRequirementsMet` (0x4889bc) and the ClearAdvice block (0x488d1e..); the no-plant branch calls `AddPlant(0, 0)` with no `CanPlantAt` (0xc008bb..0xc008c5) | 0xc004c8, 0xc007d0, 0x488dae, hook 53 | H (static r2 re-read 2026-11-23) |
| 0x8e Brother Zeng and WASD | packet 0 Blover, a Gloom-shroom at (0, 0) moved by W/A/S/D onto cells where a Peashooter could go; at wave 9 it becomes the Element-shroom; its hits (and the Gloom's) go to the body; from wave 20 each hit adds a homing puff worth 80 body damage | hooks 138 (0xc00bd0), 99 (0xc010c0), 275 (0xc00a60), 396 (0xc01110) | H (hook 266 L) |
| 0x8f Tall-nut's Probe | a Vasebreaker level (IsScaryPotterLevel) with two vases: the Boss Flower 0x76 at (0, 0) and a marked Tall-nut head at (8, 4) that comes out with 150000 body, 120000 helm, a 30000 Screen Door, scale 1.95 | 0xc01cd0, 0xc01d00, hook 189 (0xc01e00) | H (0x524370 / 0x533000 read as AttachShield / anim refresh, M) |
| 0x69 Visual Disorder | every tick Color::White's alpha is 40; from wave 12 it gets a random colour every 128 ticks; reset when the board goes | hook 103 (0x798ca8), 765 | H (which draws read it may differ from 1051, M) |
| 0x6b / 0x87 / 0x90 Glove Wars and Trick of Tricks 2 | V2, 0x6b only (0x7a4c50 in the hook 462 chain, item mode 1): at chooser close each chosen packet i is planted at column i, row 0 (i < 5) or column i - 5, row 1 (Imitater = its copy, empty = Flower Pot, no CanPlantAt), then the bank is 2 packets: Blover, Cherry Bomb (types only). All: item mode: the shovel slot holds the Zen glove (drop foley), which picks up a lawn plant and puts it on a free cell (render order row*10000 + 302805 - x); the chooser greys Gatling..Cob in item modes 1, 2, 4; 0x87 7 slots; 0x90 only columns 0-3 (stripe at x 340) | 0x7aaf60, hooks 73, 76, 77, 103, 132, 133, 171, 173, 438, 452, 479 | H (cursor offsets 211/215/476 and the Cattail rule 65 not copied) |

## Not built (and why)

| Mode | What it needs |
|---|---|
| 0x93, 0x94 | empty slots in the mod |

## Port choices (rulings)

- The list: the exe reuses the 20 Mini-games buttons on challenge pages 4-6 (mode = 0x65 + (page-4)*20 + slot, hooks
  199-203; twins' icons, locks, trophies). The port shows its own scrolling list (same frames and thumbnails) from an
  "Unnamed modes" button on the Mini-games page, because 2-3 extra pages of reused buttons do not suit a phone. No locks:
  the exe's locks are the vanilla twins', not the mod's.
- Records: the exe keeps none (hook 251 skips `mChallengeRecords[mode-1]++` and the unlock flag). The port keeps a
  record per mode in `userdata-unnamed/user<id>-modes.json` to show a trophy in the list, and never sets the unlock flag.
  The exe's out-of-bounds "beaten" read (aliasing `mPurchases`) is not copied.
- Hook 12's side effect (every string built while the mode runs becomes its name, e.g. the restart dialog body) is not
  copied; only the level name and house message use the mode name.
- 0x74's dimmed `Color::White` is drawn as a black veil of alpha 155 over the board picture.
- 0x65: only the blink explosion deals 300; the exe's EBX trick that decides it is not copied.
- 0x7d: the exe extends only the vase populate, the slot count and the bank slide-in, so its vases could never be opened
  (and its 10 waves would decide the level). The port treats it as a Vasebreaker (`IsScaryPotterLevel`), as 0x8f is in
  the exe. Cost if wrong: 0x7d plays as a vase level instead of a 10-wave level with unbreakable vases.
- 0x6d: elites are skipped at the roll (the exe rolls, then writes variant -1 after its HP edits).
- 0x72: the plant is the only Peashooter-line plant on the lawn (found there each time, not a kept pointer); a tap on a row
  or a swipe moves it, as in 6-5.
- 0x78 / 0x7f / 0x90: where the exe writes `mGameScene = 4` the port calls `Board::ZombiesWon(nullptr)` (the normal loss).
- 0x8b: the player reads the mouse in board coordinates (the exe reads the cursor object, which the port only updates
  while it is drawn); the score bar is black and yellow (colours not decoded); the seed bank keeps the vanilla default.
- 0x8d: ten seed slots (the exe writes ten packets; hook 142 has no 0x8d branch); a packet still recharging or too dear
  buzzes (vanilla's tests run first, as in the exe).
- 0x8d: the no-plant branch plants on (0, 0) only if it is free, else on the first free cell down column 0, then column
  1...; a full lawn refuses the click; the sun is floored at 0. Why: the exe's `AddPlant(0, 0)` has no `CanPlantAt`, so a
  second click after the plant there moved or died would stack two plants in one cell. Cost if wrong: a revived plant
  lands one cell lower than in the exe when (0, 0) is taken.
- 0x8e: on the phone (no W/A/S/D) a swipe is one step its way and a tap on another lawn cell one step toward it (longer
  axis, the row on a tie), through the same Peashooter-cell test as the keys (port addition, as 0x72 / 6-5).
- 0x78 / 0x8b: a mouse is followed every tick (the exe); a finger or S Pen only while a press that began on a bare lawn
  cell is held, and the object stays put between presses. Why: with a finger every tap moves the pointer, so a tap on a
  sun or packet teleported the Sunflower / bullet there. Cost if wrong: touch players must drag instead of tapping.
- 0x69: the faint (and from wave 12 tinted) `Color::White` is applied only while the board is in play (playing, not
  paused, no dialog); the pause menu, options, almanac and the zombies-won screen are drawn in plain white. The exe
  leaves the global tinted until its menu hook (765) resets it. Cost if wrong: menus look plain where the exe's are faint.
- Glove Wars (item modes): a gloved lawn plant is drawn from its own seed (it has no potted-plant record) and the glove
  drops it if it is eaten while held (the exe would keep reading the dead plant).
- 0x8c: one seed slot (only packet 0 is written).
- 0x88: claims store the plant's engine seed (a mod plant claims as its base plant).
- 0x92: the options sit at (464, 100) and (464, 136) in the chooser (the English label is longer), higher with CARD on;
  the street preview keeps the vanilla mix (hook 218's Dancer-only preview is not copied).
- 0x8e: hook 266 is read as "the Gloom-shroom stays awake by day".
- Hook 348 (an Imitater with no copy picks from table 0xc003ce) runs whenever the pack's `modModes` feature is on; only I
  Am Luck makes such Imitaters. A mod seed without a row in data/mod-plants.json is re-rolled too (the exe has all 26).
