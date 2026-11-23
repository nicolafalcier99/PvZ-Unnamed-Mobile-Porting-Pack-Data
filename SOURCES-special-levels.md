# Special levels 6-5, 6-10, 7-5 and the hidden 71-73 (feature `specialLevels`, Plan 7 Task 3a)

Rules: `data/rules-special-levels.json` (keys `specialLevels.*`, a missing key plays vanilla), message text
`strings/en-corrections-special-levels.txt`. App: pure rules `src/Mod/Unnamed/SpecialLevels.*`, engine
`src/Mod/Engine/SpecialLevelHooks.*` (one-line sites), `Level55Shooter.*`, `Level65Snake.*`, `HiddenLevels.*`, dispatch in
`SpecialLevels.cpp`. 7-10 (70, the giant Newspaper boss) is a separate task.

Study: the research notes (w6-w7-and-new-content) 2.3. Every address below was re-read for this task in the mod exe
(the Unnamed 1.3beta2 `PlantsVsZombies.exe`, radare2 + the research notes (hooks2), never run). Where the
re-read changes the study, it says so (**correction**). Confidence: H high, M medium, L low.

Offsets (1051): Plant +0x1c mRow, +0x24 seed, +0x28 column, +0x40 health, +0x5c mLaunchRate, +0xc8 mMagnetItems[0],
+0x141 mDead. Projectile +0x3c/+0x40 velocity, +0x5c type (7 = star), +0x60 age, +0x84 mCobTargetRow, +0x88
mTargetZombieID. Board +0x90 zombies array (+0xa0 count), +0xac plants array (+0xbc count), +0xc8 projectile block,
+0x140 advice widget, +0x559c mZombieCountDown. Zombie +0xc8..+0xe0 body / helmet / shield HP and max.

## 6-5 (55): Mushroom-garden shooter

| Rule | Exe | Port | |
|---|---|---|---|
| 4 seed slots in the chooser | hook 142 (Board::GetNumSeedsInBank 0x41bee0) -> 0x799717 returns 4 | `SpecialBankSlots` | H |
| After the chooser: sun 0, bank 0 packets, one Cabbage-pult (0x20) at **row 0**, column 0, mLaunchRate 50 | hook 462 (OnStartButton) -> 0x79842f: `mov [board+0x5560],0; mov [bank+0x24],0; push -1; push 0x20; mov eax,0; push 0; call AddPlant` (AddPlant takes the row in EAX, see 0x798614); `+0x5c = 0x32` | `ShooterStart` from Board::StartLevel | H (row: **correction**, study said medium) |
| The "100 HP" | `mov [plant+0xc8], 0x64` | not ported: +0xc8 is mMagnetItems[0].mPosX (a float) in the 1051 Plant; health is +0x40 (offsets confirmed by +0x5c, +0x141, +0x130 uses) | H (**correction**) |
| First wave after 250 cs, message 0xa20100 "[quote not included]" style 12 (BIG_MIDDLE) for 250 cs | hook 160 (Board::StartLevel 0x41f6e0) -> 0x79a000 | `ShooterStart` | H |
| Up / Down move the plant one row (rows 0..4), Plant+0x1c +-1, +0xc +-100 | hook 138 (Board::KeyDown) -> 0x79b0a0 top, keys 0x26 / 0x28 | `ShooterKey`; render order follows the row too | H |
| Sun ZombieValue x 5 (x10 with the SUN cheat) when a zombie loses its head; then Cabbage -> Melon-pult (0x27) at >= 500, Melon -> Winter Melon (0x2c) at >= 2000, one step per kill, in place, launch rate 50 | hook 596 in **Zombie::DropHead** (0x529a30: `anim_head`, `mHasHead = 0`) -> 0x7984c1 | `ShooterHeadDropped` after `mHasHead = false` | H (site: **correction**, triage named it "after UpdateZombiePool") |
| Zombie types < 26 spawn with half body / helmet / shield HP; every max HP stays | hook 517 chain at the max-HP stores of ZombieInitialize (0x523fa3..0x523fca): 0x797e04 stores the body max first, 0x799787 halves current and helmet / shield max, then 0x523fc4 / 0x523fca store the full EDX / EAX over those max values | `ShooterZombieSpawned` right after the max-HP stores | H (max: **correction**, study said "half HP") |
| Hook 142's "unknown return" | it is GetNumSeedsInBank (4 for 55, 3 for 65 via 0xc030b0) | | H |

SUN cheat (x10) is not ported (no cheat codes in the port yet).

## 6-10 (60)

Hook 220 sits in CutScene::StartLevelIntro (0x43a900, the "after PlaceStreetZombies" name in the triage is wrong):
level 60 jumps to 0x43afec = `mov [cutscene+0x1c], 4000`, the vanilla `IsFinalBossLevel` branch that sets **mBossTime**.
CutScene::Update then calls Challenge::PlayBossEnter (0x426f60) when `mBossTime > 0` (0x43bfa4). So **6-10 is a second
Dr. Zomboss fight**, on the roof with 5000 sun, a seed chooser (no conveyor) and 10 waves of Normal Zombies (study U2
answered, **correction** of "intro timer"). Port: `SpecialIntroBossTime` returns the table's `introTimer`. H.

## 7-5 (65) and mode 0x89 Glutton Star: star snake

One code in the exe: every site tests 0x7aaee0 = "mode 0x89, or Board+0x5550 == 65" (any mode). Study with every address:
the research notes (glutton-star) (Glutton Star task, 2026-11-23, answers U3). Engine: `Mod/Engine/Level65Snake.*`; on in
7-5 with feature `specialLevels`, in mode 0x89 with feature `modModes`.

| Rule | Exe | Port | |
|---|---|---|---|
| 3 seed slots | 0xc030b0 returns 3 for 0x7aaee0 | `SpecialBankSlots` / modes.json `seedSlots` | H |
| After "Let's Rock": the turn table is cleared (0x5000 bytes = `maxTurns` 2560); three stars (type 7, motion 7, flags 1, vx 3.0, row 2, order 0x4ec80) at x 120 / 102 / 84, y 280, ages +12 / +6 / 0 (`startStars`); the head (made first = item 0 of the array) keeps the tail's id in +0x84; packets 0-2 become Starfruit, Sunflower, Wall-nut (type only: a picked seed's start recharge stays) | hook 462 chain -> 0x7a2230..0x7a2331 | `SnakeStart` from SeedChooserScreen::CloseSeedChooser (`SpecialChooserClosed`) | H |
| A click on the Starfruit packet (after the vanilla active / sun / requirement tests) pays its cost (175) and, if item 0 is a star with a tail, adds a star `growGapTicks` 6 behind the tail along its velocity (x87 rounding), 6 ticks younger, same velocity and turn count, order 0x53bd8, mShadowY = y + 82; item 0's +0x84 = the new id. No pick-up, no recharge | hook 467 -> 0x7a20f9..0x7a21e3 | `SnakePacketClick` in SeedPacket::MouseDown's last branch (`SpecialPacketClicked`) | H |
| W / A / S / D while playing (scene 3): item 0 (any type, alive or not) turns; level (vy == 0) only W / S, else only A / D; new velocity +-3 on one axis; (age, key) written at index <its turns> (+0x88), +1 | hook 138 -> 0x79b3d2.. | `SnakeKey` / `SnakeSteer` (+ swipe) | H |
| Every star: visible; a body star (+0x84 == 0) replays entry <its turns> when its age equals it; the head (+0x84 != 0) with mX < 0, mX >= 900, mY < 40 or mY >= 600 loses (scene 4). The vanilla test calls Die at y < 40 / y > 600, but that Die is one the star lives through (0x46d047 with EBP = the star, cave 0x6511e3, counter reset each tick), so the head is never removed and every edge loses at the next tick (Plan 9 R1; web 「[quote not included]」) | hook 401 -> 0x7a1fc1, after age++ | `SnakeProjectileTick` | H |
| Snake stars never die from a hit: they fly through zombies, hitting each one they overlap every tick | Projectile::Die cave 0x6511e3 (counter < 255, reset to 1 by hook 401 each tick) | `SnakeShotSurvivesHit` at the end of DoImpact (`SpecialShotSurvivesHit`) | H |
| A dead slot keeps its memory, read by index (the dead head still steers and still adds stars behind the dead tail) | stale DataArray memory | `SnakeProjectileDied`: copy in BoardState::starSlots (saved) | H (exe), M (copy) |
| Hook 496: the Zomboni's 1-in-9 orange elite roll is skipped in 0x89 and Adventure 65 (not a Gargantuar change: **correction**) | 0x95b750 -> 0x523e4e | `ZamboniRollAllowed` (Pool zombies) | H |
| The mod Starfruit's curve code (stars with +0x88 276 reverse, +0x88 0..4 spiral) is skipped in 0x89, 0x8b and Adventure 65 | 0x95b700 | nothing: the port has no curve code yet | H |

Saved: the turn table and the slot copies are BoardState (chunk "PVZB", written only while not empty, so vanilla and
ordinary saves stay byte-identical; an older 8-byte chunk loads with an empty table); the head's tail (mCobTargetRow) and
each star's turn count (mTargetZombieID) are saved projectile fields. The exe saves neither table (its 0x810000 is lost
on load).

## Hidden 71 / 72 / 73

| Rule | Exe | Port | |
|---|---|---|---|
| 71 wave points: x28, then the x4 tail of Little Trouble (0x409960) = **x112** of the points before the level multipliers | hook 21 (PickZombieWaves) -> 0x95c0c0 `imul ecx, ecx, 0x1c; jmp 0x409960` | `SpecialWaveBudget` | H (**correction**: "own wave branch skipping part of the setup") |
| 71: a **Blover at column 7, row -1** every 1000 play ticks | hook 93 at the top of Board::UpdateSunSpawning (0x413a70; triage said "after ZombiesWon"): own counter Board+0x57cc (mod block), `% 1000 == 0` -> `push -1; push 0x1b; mov eax,-1; push 7; call AddPlant` | `HiddenUpdate`, counted with mMainCounter (incremented right before UpdateSunSpawning, saved) | H (plant: **correction**, study said "a plant") |
| 71 helmets x2 (and max) | hook 515 -> 0x95c110 | `HiddenZombieSpawned` | H |
| 71 Blover, 73 seeds 2 4 11 12 14 15 17 20 27 35 38 (and mod seeds) not allowed to pick | hook 425 replaces the call in the chooser's hover / pick test 0x482dd0 (vanilla: the Last Stand list) -> 0x95c180 / 0xc13330 | `SeedChooserScreen::SeedNotAllowedToPick` | H |
| 73 (board **and** profile level 73): a plant is planted in its whole column (Column Like You See 'Em's loop 0x410aec) while the lawn has no zombie and at most 29 plants (counted after the clicked plant); the cursor preview shows the column under the same test | hook 71 (MouseDownWithPlant) -> 0xc13490 / 0xc13660 (`cmp [ebp+0xbc],0x1d; setg; cmp [ebp+0xa0],0`), hook 217 (CursorObject draw) -> 0xc13440 / 0xc13690 | `SpecialPlantsColumn` at both Column-mode tests | H (U4 answered) |
| 73 Newspaper first allowed wave 5 (Adventure, board and profile 73) | hook 43 (PickZombieType) -> 0xc13520 | `SpecialFirstWave` | H |
| 73 first wave after 5000 cs | hook 29 | table (Task 1) | H |
| 72 (V2) wave points x80 (x20 then the x4 tail); every plant on the board takes the bite function 0x950000 with damage 1 when `mMainCounter % 6 == 1` (100 HP per 600 cs), sparing Squash states 3..7 and (outside I, Zombie) seeds 2, 14, 15, 20, 27, 0x52, 0x6b unless asleep; dies at once below 0 | hook 21 (0xc13070 `imul ecx,ecx,0x14`), hook 316 (0x463ed7 -> 0xc13150 / 0xc1301a: `div 6; cmp edx,1; push 1; push 1; push plant; call 0x950000`) | H |
| 73 (V2) wave points x60 (x15 then the x4 tail) | hook 21 (0xc13300 `imul ecx,ecx,0xf`) | H |

## Touch (port addition, not in the exe)

The phone has no arrow or W / A / S / D keys. A press that starts on the bare lawn (nothing in the cursor, no coin,
packet or shovel under it) and is released counts as a gesture: under `specialLevels.touch.swipeMin` (40 board px) a tap,
else a swipe along its longer axis. 6-5: a tap on a lawn row moves the plant to that row (the same as that many arrow
presses), a swipe up / down is one press. 7-5: a swipe is W / A / S / D. Works with the mouse too.

## Mac checks (2026-11-23, app on d6fbb60 + this task, hidden + silent, seed 7, width 1300)

- 6-5: `special shooter start plant=32 row=0 col=0 rate=50 sun=0 bank=0 countdown=250`; screenshot: empty bank, sun 0,
  Cabbage-pult top-left, the message "[mod text not included]" sliding in. Scripted keys down, down, up, a tap on
  row 3, a swipe up, a tap on row 0: rows 1, 2, 1, 3, 2, 0 (log + screenshot of the plant in row 3). Spawned zombies
  start at 135 / 270 body (Football helmet 700 of 1400). With `-pvzu-dev-sun 1999`: first kill +5 -> 2004, Cabbage ->
  Melon; next kill -> Winter Melon (rate 50 both); 24 kills, all +5 x value; screenshot of the Winter Melon in row 0.
- Save / load: a 6-5 game quit with the plant in row 2 loads with one plant (no second Cabbage), and Up moves it to 1, 0.
- 6-10: `special intro level=60 bossTime=4000`; Dr. Zomboss spawns at the boss time (Unnamed 50000 HP) and summons Normal
  Zombies; screenshot of the roof with 25 pots, 5000 sun and the robot. 9000 frames with autoplay, no assert.
- 7-5: 3 seed slots, sun 0, sky sun falls (screenshot). Starfruit column + scripted W/A/S/D every 13 frames: 64 steer
  lines (head = star in slot 0, v = +-3), 200 logged replays at the recorded ages, a swipe steered the head (`by=swipe`).
- 71: wave points before x112 (wave 1 budget 112 instead of 4; total 5151), Blover at column 7, row -1 at play ticks
  1000 / 2000 / 3000, helmets doubled (cone 740, bucket 2200, Football 2800), Blover barred in the chooser.
- 73: chooser screenshot with the eleven seeds darkened; with autoplay before the first wave two Flower Pots each filled
  their column (`column plant plants=1` / `plants=6`, screenshot); first Newspaper in wave 5 (baseline: wave 2).
- Wave logs of the baseline d6fbb60 build and this one, byte-identical: vanilla 1, 10, 25, 50; Unnamed 1, 25, 50, 55,
  60, 65, 72. Different, as intended: 71 (budgets) and 73 (Newspaper waves).

## Rulings

- Ruling: 55's setup runs at Board::StartLevel, not at the chooser's start button — one hook point for chooser and dev
  runs, same result — cost if wrong: the plant appears about two seconds later than in the exe.
- Ruling: the "+0xc8 = 100" write is not ported — +0xc8 is a Magnet-shroom item slot in the 1051 Plant, the Cabbage-pult
  keeps 300 HP — cost if wrong: the 6-5 plant should die faster.
- Ruling: 55 halves current HP only, all max HP stay — the max stores after the hook overwrite its halved max values —
  cost if wrong: arm / helmet damage stages show later than in the exe.
- Ruling: 6-5 sun goes straight into mSunMoney (past 9990), as the exe adds to Board+0x5560 — cost if wrong: none (sun
  buys nothing there).
- Ruling: 55 arrows act only while playing — the exe would follow a stale pointer outside play — cost if wrong: none.
- Ruling: 6-10 is a Dr. Zomboss fight — mBossTime > 0 is what the vanilla cut-scene uses to bring him in — cost if wrong:
  6-10 should be a plain Normal-Zombie roof level with a long intro.
- Ruling: 71's Blover is counted with mMainCounter instead of the mod's Board+0x57cc — both count UpdateSunSpawning calls
  from 0, and mMainCounter is saved — cost if wrong: Blover times shift after a load.
- Ruling: 73's column planting and Newspaper wave need the profile level 73 as the exe checks it — a level picked with the
  level skip or a dev start keeps the profile on 73 anyway — cost if wrong: none.
- Ruling: touch gestures (tap a row / swipe) work on every layout and with the mouse — simpler to test, harmless on
  desktop — cost if wrong: the owner wants them on the phone only, or on-screen arrows instead (one rule each).
- Ruling: the 6-5 message names both keys and touch in one English text (exe: one Chinese line for the arrows) — cost if
  wrong: one string.

- Ruling: the head off the field calls Board::ZombiesWon(nullptr) — the exe sets scene 4 bare, which in the port would
  freeze without the game-over screen — cost if wrong: none (same result, the normal lost screen).
- Ruling: no loss once the level award has dropped — the exe would set scene 4 after a won level — cost if wrong: a
  player who steers off the edge after the last zombie would lose a won level in the exe.
- Ruling: a dead slot is a saved copy of its last state (BoardState::starSlots), standing in for the exe's stale memory
  — cost if wrong: after the head dies through the top / bottom, Starfruit clicks and keys act on that copy as the exe's
  do on its memory; any field the copy lacks reads as the next projectile's.
- Ruling: the snake's start runs at CloseSeedChooser (the port's OnStartButton end), after the mod-mode bank code, as
  hook 462's chain — cost if wrong: none.

## Open

- U3 answered (the research notes (glutton-star)). Open: the snake was not played on the phone; the 0x89 start sun (50, no rule found) not checked against a video.
- 6-10: the end of the fight (boss death -> level complete, money / award) was not played to the end on the Mac.
- 7-5 on the phone: no hint tells the player to swipe (the exe shows none for W / A / S / D either).
- In 6-5 the plant in row 0, column 0 is drawn over the sun counter in the centred 800-wide garden board (cosmetic).
