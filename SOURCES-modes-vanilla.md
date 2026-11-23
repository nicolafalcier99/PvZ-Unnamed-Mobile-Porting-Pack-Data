# Sources: Unnamed changes to the vanilla modes (feature `modesVanilla`)

Rules file: `data/rules-modes-vanilla.json`. Study: the research notes (modes-ui-shop) 2.1, 2.2, 9 and Final table A.
Every row below was re-read in the Unnamed 1.3beta2 `PlantsVsZombies.exe` with radare2 (read only)
on 2026-11-23; where the study's reading was wrong the corrected reading is given and marked **(corrects study)**.
Numbers are the 1051 GameMode / SeedType / ZombieType values (PvZ-Portable's enums are the same; tests assert it).
The 48 mod-only modes (0x65-0x94) are not in this file.

## Challenge screen (study 2.1)

| Key | Value | Evidence |
|---|---|---|
| modesVanilla.challenge.11 / .12 / .14 / .15 | [page, row, col, icon] = [0,2,0,5] [0,2,1,6] [0,2,3,8] [0,2,4,9] | gChallengeDefs 0x6a2ba0 (in-place .data edit), the research notes (modes_challenge_defs) EXE 6a2ba0 72`: Endless Day/Night/Fog/Roof on the Survival page beside Pool Endless (13 stays page 0 row 2 col 2 icon 10) |
| modesVanilla.challenge.49 | [2,3,0,10] | same table: Squirrel moves Limbo row 2 col 3 -> row 3 col 0 |
| (no key) Tree of Wisdom name | kept "Tree of Wisdom" | the exe's entry is "        智慧树" (Chinese text for the Chinese build); the English port keeps the English name |

Unlock rules are vanilla .text (ChallengeScreen::MoreTrophiesNeeded): the four moved Endless modes need 10 Survival
trophies after the adventure, as Pool Endless does.

## Zombie allow lists (Challenge::InitZombieWaves)

| Key | Value | Evidence |
|---|---|---|
| allow.29.add (Zombies on Speed) | FOOTBALL, DANCER, JACK_IN_THE_BOX, BALLOON, LADDER | hook 177: 0x4258a8 -> 0x7a03c3 writes BL (= 1) to +0x54db/dc/e3/e4/e9 and re-does the stolen Pole write. The triage's "clears" is wrong |
| allow.34.add (Pogo Party) | POLEVAULTER, DANCER | hook 178: 0x4258bb -> 0x7a0416 (+0x54d7, +0x54dc, stolen Pogo +0x54e6) |
| allow.41.add (Air Raid) | POLEVAULTER, DOLPHIN_RIDER, BUNGEE, CATAPULT | hook 179: 0x425aae -> 0x7a0457 (+0x54d7, e2, e8, ea, stolen Balloon e4) |
| allow.22 (Seeing Stars) | add POLEVAULTER, GATLING_HEAD; remove TRAFFIC_CONE | hook 180: 0x425cad (the default branch, after its Normal write at 0x425ca7) jumps to 0x79ac00 over 9 bytes (`mov edx,[esi+4]` + the Cone write); mode 0x16 writes +0x54d4, f1, d7 and returns to 0x79af0d -> 0x425cb6 (Pail). Cone is never written |
| allow.36.add (Art Wall-nut) | BUNGEE, LADDER, GARGANTUAR, JACK_IN_THE_BOX | 0x79ac20: +0x54d6 (Cone, re-written), e8, e9, eb, e3 |
| allow.38.add (Resodded) | FOOTBALL, JACK_IN_THE_BOX, GATLING_HEAD | 0x79ac4c..: +0x54d6 (Cone), db, e3, f1 |
| allow.40 (Art Sunflower) | add PEA_HEAD, DANCER, CATAPULT; remove PAIL, YETI | mode 0x28 writes +0x54ee, d6 (Cone), dc, ea and returns through 0x79af0b `xor ebx, ebx`, so the Pail write at 0x425cb9 and the Yeti write at 0x425d8b (`mov [ecx+0x54e7], bl`) store 0. Normal was already set at 0x425ca7. **(corrects study: the extras are set, Normal is set, Pail and Yeti are cleared)** |
| allow.45 (Grave Danger) | add POLEVAULTER, DOOR, DANCER, ZAMBONI, SQUASH_HEAD; remove TRAFFIC_CONE | mode 0x2d: +0x54d7, da, dc, e0, f2 -> 0x79af0d |
| (no key) every other default-branch mode | vanilla Normal, Cone, Pail | the chain 0x79ac00 -> 0xc00900 -> 0xc00d20 -> 0xc02e10 -> 0xc05260 -> 0xc03110 -> 0xc00958 -> 0x7a5a3e ends at 0x7a5e96 `mov [ecx+0x54d6], bl` (Cone) -> 0x425cb6 (Pail) **(resolves study U2)** |

The edits are applied after the vanilla list and its Yeti line, which gives the exe's result in every case above.

## Art challenges (Challenge::CanPlantAt)

| Key | Value | Evidence |
|---|---|---|
| art.ignorePictureSeeds | [11] (Grave Buster) | hook 175: 0x425642 replaced `cmp ebp, 0x1e; je 0x425651` (Pumpkin) with 0xc113f0: seeds 0xb, 0x1e, 0x5b, 0x6e jump to 0x425651 (the "fits the art" path, then the Art Wall-nut eye-cell check), the rest return 6 (PLANTING_NOT_ON_ART). Applies to all three art modes (0x16, 0x24, 0x28: 0x42561c). **(corrects study: Grave Buster may go on any art cell like Lily Pad and Pumpkin; it is not "only on marked cells")** 0x5b / 0x6e are the mod's +80 forms (no such seeds in the port) |

## Grave Danger

| Key | Value | Evidence |
|---|---|---|
| graveDanger.gravesPerWave | 5 | Challenge::SpawnZombieWave 0x426850: non-flag wave > 5 -> hook 184 0x426928 -> 0xc11350 calls GraveDangerSpawnRandomGrave (0x4266c0) five times (vanilla once) |
| bannedSeeds.45 | [11] | the seed chooser filter 0x7b0f00 (replaces the inlined SeedNotAllowedToPick at 0x482e17, 0x482f60, 0x4830f2, 0x4832a7, 0x484a3b, 0x485101, 0x486376, 0x486b8a) chains to 0x7b0f6e: `cmp edx, 0x2d; jne; cmp ebx, 0xb; je 0x7b0fd2` (not allowed). **(new: not in the study)** |
| (no key) hook 181 | plants under a new grave die through the mod's damage call (0x950000, health + 1) instead of Plant::Die | same result for every plant in the port (no shielded mod plants); vanilla Die kept |
| (no key) hook 183 | 0x412ce0(0) = SpawnZombiesFromGraves on the flag wave | same as vanilla |

## V2 (2026-11-23): mini-games changed in place in `.text` (community S2 1.2.5beta5 list, checked in the exe)

| Key | Value | Evidence |
|---|---|---|
| numWaves.17 / .45 | 30 (Bowling, Grave Danger; vanilla 20) | `Board::PickZombieWaves` 0x4093fe / 0x409408 -> 0x40946c `mov [edi+0x5564], 0x1e` |
| numWaves.27 / .33 | 40 (Column, Bowling 2; vanilla 30) | 0x409444 / 0x409459 -> 0x409460 `mov [edi+0x5564], 0x28` |
| numWaves.48 | 40 (Bungee Blitz; vanilla 30) | hook 0x4093c0 -> 0x79a207 `cmp edx,0x30; je 0x409460` |
| numWaves.30 | 16 (Whack a Zombie mini-game; vanilla 12; 2-5 keeps 8) | 0x4093ec `mov [edi+0x5564], 0x10` |
| conveyor.21 | Repeater 25, Wall-nut 15, Doom 5, Jalapeño 15, Lily Pad 30, Ice 10 (vanilla Peashooter, Wall-nut, Kernel, Squash, Lily, Ice) | `Challenge::UpdateConveyorBelt` 0x423250 (mode 0x15), registers from 0x422e1b (edx 10, ebx 5, esi 20) |
| whack.bank | Cherry x3, Jalapeño x3, Doom x3, Ice (10 packets) | `Board::InitLevel` 0x40b84d..0x40b888 (mode != 0) then hook 34 0x959340; `GetNumSeedsInBank` 0x41bf32 returns 10. Adventure 2-5 keeps Potato Mine, Grave Buster, Cherry (0x40b7fb); the exe also gives 2-5 a 10-slot bank (7 empty), the port keeps 3 there |
| whack.groupSize | 4 (vanilla 1) | `WhackAZombieSpawning` 0x42618f `mov [esp+0x1c], 4`; no mode test, so 2-5 too. Pail still needs a group < 3 (0x42620c), so Pails come only in pairs |
| whack.graveTarget | 30 (vanilla 5) | 0x426043 `mov ecx, 0x1e; sub ecx, GetGraveStonesCount(); max 1` at countdown 100; graves go to columns 3..8 (0x425da0) |
| (no key) Pogo Party + Bungee, Dig It / Squirrel with Tall-nuts | not in 1.3beta2 | hook 178 0x7a0416 sets only Pole, Dancer, Pogo; `ShovelAddWallnuts` 0x428510 still plants seed 3 |

## Wall-nut Bowling (Plant::UpdateBowling 0x462ce0, plain Wall-nut only)

| Key | Value | Evidence |
|---|---|---|
| bowling.zombie.3 / .4 | 27 (Wall-nut head), 31 (Tall-nut head) | hook 304: 0x46300e (the vanilla `cmp eax, 3` after the count-2 silver coin) -> 0xc110d0: count 3 or 4 -> AddZombieInRow((count == 4) * 4 + 0x1b, row), mPosX = the nut's mX, +0xb8 (mMindControlled) = 1, then 0x4630d0 (no coins, no foley) |
| bowling.packetFrom / packetSeeds | 5 / [3, 49, 50] | count >= 5 -> 0xc10a80: count clamped to 7, BL = [0xc10ac3 + count - 5] = 03 31 32, AddCoin(mX, mY, 16 = usable seed packet, 3 = coin motion), coin+0x68 = seed. No gold coin, no RollSomeHeads achievement |
| (no key) count 2 | vanilla silver coin | 0x462ff6 runs before the hook **(resolves study U9: the count-2 coin stays; counts 3 and 4 give no coins)**. The "bounce rules rewritten" in the study is the decompiler following the vanilla code at 0x4630d0 |

## Last Stand: no change

Hook 291 (0xc00080) only adds mod plant 0x76 to the Marigold path; the "no production before the onslaught" test at
0x45fa2f is vanilla .text (PvZ-Portable Plant::UpdateProductionPlant has it). The seed filter's Last Stand row (seeds
1, 9, 0x29, 0x18, 8 and +80 forms) is vanilla SeedNotAllowedToPick plus mod seeds. **(corrects study)**

## Vasebreaker

| Key | Value | Evidence |
|---|---|---|
| scaryPot.directSunFrom / sunValue | 16 / 25 | hook 188 (0xc01f10): pot+0x50 (mSunCount) >= 0x10 -> sun += count * [0x4309f0] (= 0x19), EBP = 0 (no drops). Vanilla pots hold Rand(3)+1, so this only shows in mod modes |
| (no key) hooks 189, 558 and the vase pole's vault (0xc036e0) | ported in `SOURCES-vase-pole.md` (Plan 9 R2) | they belong to the Pole Vaulter elite 0x103 (Day zombies): at its vault (0xc036e0, sets +0x12c = 1) it puts a vase at column ±1 with a Rand(33) zombie (11-14, 16, 19, 20, 25 re-rolled) and turns zombies in that cell into vases (pot+0x54 = hypnotised); on landing (558, 0x52613a) it opens vases at PixelToGridX(mX, mY) ± 1; 189 gives a pot's zombie mMindControlled = pot+0x54. None of it is mode-specific. Correction: the zombies caught are those whose rect overlaps the pole's attack rect (any column), and their vases hold `mMindControlled != 1`, so they come out on the pole's side |

## I, Zombie

| Key | Value | Evidence |
|---|---|---|
| iz.cost.62 | 125 (Pole Vaulter card) | Plant::GetCost jump table 0x467bac (index seed - 0x38): index 6 points at the 125 block 0x467b71; Cone (index 5) at the 75 block 0x467b65. PvZ-Portable (and the PC game) price it 75, so the table entry is an in-place edit (M: no clean 1051 exe to compare) |
| (no key) Bungee 125 | vanilla | hook 363 returns `mov eax, 0x7d` for index 10, the same as the table; the immediate at 0x8f007e is rewritten at run time (below) |
| iz.footballToggleZombie | 5 (Newspaper) | hook 79 (0x412228, Board::MouseDown on a packet with click count <= 0): Football card (0x43) -> `xor [0xc05bdb], 1`; hook 190 (IZombieSeedTypeToZombieType 0x42a08f -> 0xc05b85): 0x43 -> 5 while the toggle is 1, else 7. The toggle is never reset |
| iz.dancerCompanions | [61, 62, 63, 67, 72, 73] | hook 78 (0x412204, Board::MouseDown with a card held, before MouseDownWithPlant): clicking the Dancer card (0x48) with Cone/Pole/Pail/Football/Dancer/Gargantuar held (0xc04533..) stores the held card's zombie type (table 0x8f01a8) at packet+0x40 and sets the Dancer price 0xc045f5 = card price (table 0x8f01b7 -> GetCost jump table) + 0x15e |
| iz.bungeeCompanions | [60..65, 67..74] | 0x8f0140: clicking the Bungee card (0x42) with any zombie card 0x3c..0x4a but 0x42 held does the same with price 0x8f007e = card price + 0x7d. (A held seed < 0x21, a plant, takes a plant-cost path; plants cannot be held in I, Zombie, not ported) |
| (no key) right click on Dancer / Bungee | companion -1, price back to 350 / 125 | 0xc045d0, 0x8f037b |
| (no key) placing | Bungee: AddZombieInRow(companion, 0) before the Bungee, then BungeeDropZombie(companion, target col, row); Dancer: 0x7968eb = 1 during the placement -> the elite roll 0x79682f is skipped and the Dancer becomes 0x104 with +0x12c = 0xc046c4 (the companion) | hook 193 (0xc0462b, 0x8f04d8), 0x79682f, 0xc04610 |
| iz.longPressTicks | 50 | port only: the phone has no right click; a press of 0.5 s on one of these cards counts as one |

The port keeps the companion where the exe does (SeedPacket+0x40 = mSlotMachiningNextSeed, saved with the packet) and
works the price out from it; the exe's global price would show a combo price on a new level after the companion was
reset with the new packet (not kept).

## I, Zombie Endless

| Key | Value | Evidence |
|---|---|---|
| starfruit.noExtraStarsMode | 70 | hook 287 -> 0x95b790: mode 0x46 jumps to 0x95b0e7, past the Rand(3) at 0x95b0e2, with EAX = the App pointer (non-zero), so `test eax,eax; jne` skips the four stars: in I, Zombie Endless a Starfruit **never** adds them and draws no roll (Plan 9 R1 corrected the earlier "always" reading) |

Hooks 172 (mode 0x46 draws one more image), 157 / 194 / 195 (formation helpers): mode 0x46 runs the vanilla code
(0x42a71d, 0x42af46); they matter only for mod mode 0x8c.

## Zen Garden

| Key | Value | Evidence |
|---|---|---|
| zen.gloveSkipsBusySquash | 1 | hook 478 (0x51f65d, ZenGarden::MouseDownWithTool): glove (cursor 0xe) on a Squash (0x11) with mState != 0 returns without picking it up |

## Not in this feature

It's Raining Seeds / Dark Stormy Night rain (hooks 117, 163, 164, 185), Tree of Wisdom power and fast-forward
(268, 167): these follow the settings dialog (study 3) and come with it. Column Like You See 'Em plays the vanilla
Conveyer tune (.text 0x45b82a). Pogo Party has no graves in vanilla already (PvZ-Portable StageHasGraveStones).

## Mac evidence (2026-11-23, hidden silent runs, seed 7, both modes)

- Challenge screen page 0 (screenshot viewed): Unnamed shows 15 Survival buttons (Endless Day/Night/Fog/Roof on row 3
  with the Hard icons); vanilla shows Pool Endless alone. Page 2: Squirrel at row 3 col 0 (vanilla row 2 col 3).
- `modesAllowed` lines equal the table above for modes 22, 29, 34, 36, 38, 40, 41, 45; vanilla mode prints the
  vanilla lists. The picked waves use the new types (e.g. Air Raid: Pole 13, Balloon 9, Catapult 7, Dolphin 6, Bungee 2;
  Art Sunflower: no Pail; Seeing Stars: no Cone).
- Grave Danger (waves sped up by the dev flag): graves 7 -> 22 between waves 6 and 9 (vanilla 7 -> 10), capped at the
  25 cells of columns 4-8; `graveBusterBanned=1` (vanilla 0).
- Wall-nut Bowling: ricochet 1-2 vanilla, 3 -> hypnotised Wall-nut head (25x), 4 -> Tall-nut head (15x), 5 -> Wall-nut
  packet (4x), 6 -> Explode-o-nut packet (1x); no crash.
- I, Zombie Endless: Football toggled -> a Newspaper is placed; Dancer + Cone costs 425 and becomes 0x104 whose four
  followers are Cones; Bungee + Pail costs 250, the Pail is dropped (height 9 -> 0 at the target) and the Bungee
  leaves; Pole card 125 (vanilla 75 / 350 / 125 and a Football). Starfruit: no extra stars, no roll (Plan 9 R1).
- Art challenges 36, 40, 22: Grave Buster passes the art check on all 12 / 15 / 14 art cells (vanilla 0).
- Vasebreaker 1 and Survival Day Endless played without errors (rules inert there).
