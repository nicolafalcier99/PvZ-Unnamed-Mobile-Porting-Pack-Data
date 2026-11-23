# Sources: Plan 9 V1 zombie rules (`data/rules-zombie-gaps-v1.json`; glove leap keys in `data/rules-day-zombies.json`)

Plan 9 topic V1: the contradictions the Chinese community listed (the research notes (community-zombies) section 3),
each re-read in the Unnamed 1.3beta2 exe (static radare2 / python; never run). Code wins. App code:
`app/src/Mod/Unnamed/ZombieGapsV1.*`, `app/src/Mod/Engine/ZombieGapsV1.*`, glove leap in `Mod/Unnamed/DayZombies.*` +
`Mod/Engine/EliteZombies.*`; feature `zombieGapsV1` (glove: `dayZombies`). The full write-up (per item: community
claim, exe evidence, decision) follows the key table; it is the same text as
the research notes (v1-zombie-contradictions).

| Key | Value | Exe |
|---|---|---|
| dayZombies.glove.leapOnPlantDeath | 1 | hook 361 0x95adf0 |
| dayZombies.glove.leapOffsetPx | 96 | 0x95ae7e `add eax,0x60` |
| dayZombies.glove.leapBite | 800 | 0x95af21 `push 0x320` |
| dayZombies.glove.leapVelX | 0.5 | 0x95aed4 (0x3f000000) |
| zombieGapsV1.newspaper.gaspInvincible | 1 | 0x651d22 |
| zombieGapsV1.newspaper.burnIsHit | 1 | 0x6514d5 |
| zombieGapsV1.redEye.readingClearsFlags | 1 | 0xc05900 |
| zombieGapsV1.redEye.garlicRipsPaper | 1 | 0xc05ad0 |
| zombieGapsV1.knife.biteConditions | 1 | 0x651210, 0xc02730 |
| zombieGapsV1.moonwalker.refusesFreeze | 1 | 0xc053c0 |
| zombieGapsV1.moonwalker.lethalMarginHp | 200 | 0xc05432 `lea ecx,[ebp+0xc8]` |
| zombieGapsV1.moonwalker.biteRestartsSummon | 1 | 0xc05510 |
| zombieGapsV1.moonwalker.burnIsHit | 1 | 0xc05490 |
| zombieGapsV1.roadSign.vaultKeepsSpeed | 1 | hook 555 0x9589f1 |
| zombieGapsV1.staff.summonsWithoutThrow | 1 | hook 565 0xc11500, 0xc114bc |
| zombieGapsV1.garlicPogo.crushesPlants | 1 | hook 614 0x95b010 |
| zombieGapsV1.garlicPogo.firstLandNoYucky | 1 | hook 531 0x95991c |
| zombieGapsV1.green.biteTypeMul | 7 | 0xc12f78 `fimul [ebp+0x24]` |
| zombieGapsV1.green.largeSunAt | 75 | 0xc12f81 `cmp ..,0x4b` |
| zombieGapsV1.pile.biteCadence | 1 | hook 672 0x79c300 |
| zombieGapsV1.pile.targetOnlyWhileCarrying | 1 | 0x52e61d -> 0xc02c90 |
| zombieGapsV1.zamboni.plainVelX | 0.25 | 0x52a81e (operand 0x679748) |

---


Plan 9 topic V1, written 2026-11-23. Input: `community-zombies.md` section 3 ("Contradictions with the port"). Items
already owned by R2 (vase pole 0x103), R4 (black Football damage, green Football Gatling head and 8 s event) and R7
(Tall-nut Zombie 0x101) are skipped. Every read is static (radare2 / python on a read-only copy of the 1.3beta2 exe;
nothing was run). Order of evidence: exe code > community text (which may describe older versions).

Code: app branch `plan9-v1` (`src/Mod/Unnamed/ZombieGapsV1.*`, `src/Mod/Engine/ZombieGapsV1.*`, glove leap in
`Mod/Unnamed/DayZombies.*` + `Mod/Engine/EliteZombies.*`); pack branch `plan9-v1` (`data/rules-zombie-gaps-v1.json`,
feature `zombieGapsV1`; glove keys in `data/rules-day-zombies.json`; evidence `SOURCES-zombie-gaps-v1.md`).

Offsets used below: Zombie +0x24 type, +0x28 phase, +0x2c mPosX, +0x34 mVelX, +0x51 mIsEating, +0x68 mPhaseCounter,
+0xbb mHasArm, +0xbc mHasObject, +0xc4 helm type, +0xc8/+0xcc body/max, +0xd0/+0xd4 helm/max, +0x134 elite
variant, +0x14c sub-variant. Phases: 11/12/13 pole pre/in/post vault, 29/30/31 Newspaper reading/gasp/mad, 40 Dancer
dancing in, 76/77 ladder carrying/placing. In 1051 the Newspaper is type 5, Dancer 8, Football 7.

## Summary

| # | Topic | Verdict | Port now |
|---|---|---|---|
| 1 | Glove Pole leaps to a dead plant | CONFIRMED | implemented (dayZombies keys) |
| 2 | Backup dancer becomes the Dancer | code exists, unreachable | unchanged (no promotion) |
| 3 | Newspaper invincible while gasping; paper survives a lethal hit | CONFIRMED | implemented |
| 4 | Road-sign Pole 0x29 vaults further, can't be blocked | CONFIRMED (the bonk skip was already ported) | speed part implemented |
| 5 | Staff Gargantuar summons appear at the right | CONFIRMED | implemented |
| 6 | Red-eye Newspaper rules | mostly already ported; 2 new rules found | 2 implemented |
| 7 | Potato-head Jack +7.5 s | NOT IN EXE | unchanged |
| 8 | White summoner Dancer 0x104 | 3 of 5 sub-claims CONFIRMED, follower list already right | 3 implemented |
| 9 | Garlic Pogo crushes plants / invisible 1/3 | crush CONFIRMED, 1/3 wrong (1/4) | crush implemented |
| 10 | Green Football bite grows as it is hurt | CONFIRMED (formula) | implemented |
| 11 | Ladder pile bites 3x / 4x | CONFIRMED | implemented |
| 12 | Knife Newspaper vs frozen / one-use plants | frozen CONFIRMED, one-use NOT IN EXE | frozen implemented |
| 13 | Low-confidence numbers | one port error (plain Zomboni speed) | fixed; rest match |

## 1. Glove Pole Vaulter (0x32) jumps to a dead plant (hook 361)

**Community:** when a plant in front dies, the glove Pole jumps to that spot and vaults at once, killing a plant it
was eating. Shovel and Jack blasts trigger it; Bungee theft, Gargantuar smash, the shovel Ladder and ash plants do
not (S6, tester comments on BV1Yf6nYsEZP).

**Exe:** `Plant::Die` 0x4679fe sets mDead, then 0x467a05 `jmp 0x7a8961 -> 0x95adf0`:
- 0x95adf0 runs the displaced call 0x4629f0, then `cmp ebx,0x1000000; jg skip`. EBX is whatever the caller of
  `Plant::Die` holds. Then a UI guard: board present and `[[[[board+0x8c]+0x320]+0x94]+0xc] != 1` (true in play).
- Loop over zombies (0x41c8f0): skip if 0x52eef0 (dead or dying); need type 3, +0x134 0x32, phase != 12, same row,
  `zombie.mX > plant.mX` (`jle` skips). No hypnosis test.
- 0x95ae7e: `mPosX = plant.mX + 96`. 0x95af00: if mIsEating, FindZombieTarget (0x52e840); if none,
  FindPlantTarget(CHEW) (0x52e780) takes `0x950000(plant, 800, 1)`; then StopEating (0x52f440). mX is still the old
  spot, so the bite finds the plant it was eating.
- +0x148 = 1 if the phase was 11 (it still had its pole) else 2; phase 12; `anim_jump` (play once, blend 20,
  rate [0x679638] = 24.0); mVelX = 0.5 for mode 2, 0 for mode 1.
- Hook 557 (0x526114 -> 0x95ad80): at landing, variant 0x32 with +0x148 == 1 clears it, sets phase 11 and jumps to
  0x526147 (StartWalkAnim(0)), skipping the attack-rect reset and the phase-13 write: it keeps its pole and its
  112 px glove reach and can vault again.
- **Which deaths pass the EBX test** (callers of 0x4679b0 read one by one):

  | Caller | EBX at the call | Leap? |
  |---|---|---|
  | Zombie::EatPlant 0x52fd55 | 1 (`add [board+0x5798],ebx`, mPlantsEaten) | yes |
  | Board shovel 0x4111df | 1 (`add [board+0x579c],ebx`, mPlantsShoveled) | yes |
  | Board::KillAllPlantsInRadius 0x41cbf0 (Jack blast) | an int argument (`mov edx,ebx` into the overlap test) | yes |
  | Board::MouseDownWithPlant 0x4108fe..0x410ba5 (upgrade / first aid / Cob / Cattail replacement) | the seed (`cmp ebx,0x2a`) or `lea ebx,[esp+..]` (stack, below 0x1000000) | yes |
  | Plant::UpdateSquash 0x460d06 (Squash lands in water) | 0x20 (`mov ebx,0x20` at 0x460cd9) | yes |
  | 0x950000 (mod plant damage, incl. the 800 bite) | the damage (`sub [esi+0x40],ebx`) | yes |
  | Plant::Squish 0x462d53 / 0x462ed2 (Gargantuar, Zomboni) | the plant pointer (`add ebx,[edx]`) | no |
  | Plant::DoSpecial 0x466990.. (ash plants after use) | the plant (`push ebx`) | no |
  | Bungee 0x52b9d2 | `[app+0x784]`, a pointer | no |
  | Silver coin kill (hook 686 0xc11285) | PlayerInfo pointer | no |

  This matches the community's list item for item.

**Decision:** implemented. `PlantDeathCause` names the cause (scope set around the vanilla `Die()` calls in the
table; every other death, mod paths included, is "other" = no leap). Ruling: register-dependent callers that were not
traced (other Plant self-deaths, Challenge / mod-mode removals) do not wake the glove. Ruling: the exe's skip list of
0x950000 (state 1, 3..7 and seeds 2/0xe/0xf/0x14/0x1b/0x52/0x6b outside one app test) is not applied to the 800 bite;
the port uses its EatPlant damage path (`ModPlantBitten`). A nested leap (the 800 bite kills, which wakes the gloves
again) runs in the same order as the exe, so the glove ends at the eaten plant's x + 96 with mode 2.

Mac: `-pvzu-level 4 -pvzu-dev-plant WALLNUT:6,SUNFLOWER:1 -pvzu-dev-shovel 1@1500 -pvzu-force-variant
POLEVAULTER:0x32 ...`: five gloves walking without poles leapt from x 311..327 to 216 (= 120 + 96), mode 2. With
`SUNFLOWER:2 ... -pvzu-dev-shovel 2@600` five running gloves leapt from x 599..727 to 296 with mode 1 and landed at
146 back in phase 11 ("keeps pole"). A glove eating its own plant does not leap (zombie mX == plant mX, `jle`).
New dev flag `-pvzu-dev-shovel col@tick` (real shovel click path).

## 2. Backup dancer becomes the new Dancer (and its option)

**Community:** when an uncharmed Dancer dies, the backup behind it becomes the Dancer (not in I, Zombie); 1.2.5beta13
added an option to turn it off (S6, S1). The mod's Almanac `[BACKUP_DANCER_DESCRIPTION]` still says so.

**Exe:** DieNoLoot hook 691 (0x530609 -> 0x797930 -> 0xC12C20 -> 0x797935) always reaches `0x7979A9 jmp 0xC03990`;
0xC03990 `cmp [edi+0x24],8` then **0xC03994 `jmp 0x797A1C` (e9 83 40 b9 ff 90)**: an unconditional jump over the
whole block (a hand-overwritten `jne`). The dead block: option 0x8001A4 != 1, variant != 0x104, not I, Zombie,
follower slot 2 present, then backup slot 3 (+0x100) with head, type 9, phase != 50 gets `type = 8` only. A rel32 scan
of .text and .NewSec finds no other way in; no absolute pointer to it; no run-time patch restores the `jne`. The
option is 0x8001A4 "[quote not included]" (Shutdoor, default 0).

**Decision:** keep the port (re-summons only). The exe of 1.3beta2 never promotes; the text and the option are stale.

## 3. Newspaper invincible while gasping; the paper survives one lethal hit

**Community:** "[quote not included]" (S6), "[quote not included]" (tester 2026-03).

**Exe:**
- TakeBodyDamage 0x5312d0: after `sub edi,[dmg]` at 0x53130f, `jmp 0x651d22`: `cmp [ebp+0x28],0x1e; je 0x651d55`
  jumps over the only body write `mov [ebp+0xc8],edi` (0x651d4f). Flash (25) and the FREEZE chill still run. No
  type test (only Newspapers reach phase 30).
- ApplyBurn 0x532b70 -> 0x6514b0 -> 0xc01abe -> 0x95a500 -> 0xc05490 -> 0x6514d5: `cmp [esi+0x24],5; je 0x6514f1`
  -> TakeDamage(1800, 0x12) at 0x532fdb for every Newspaper, before the Loaded Cannon cap.
- Vanilla DropShield sets the gasp phase before TakeDamage passes on the overflow, so the 1800 overflow is lost.
- This explains w2's "Potato Mine fails on a mad Newspaper": a mine on a reading or gasping Newspaper only rips
  the paper.

**Decision:** implemented (`GaspIgnoresBodyDamage`, `BurnBecomesHit`). Mac: five Newspapers (two knife, one red-eye,
two plain) each met a Cherry Bomb at col 6: all five lived, papers gone, gasping.

## 4. Road-sign Pole Vaulter 0x29 vaults 2 tiles, cannot be blocked

**Community / Almanac:** vaults 2 tiles and cannot be blocked (S6).

**Exe:** only three sites test 0x29: 0x95af60 (the roll), hook 555 0x9589f1 and the bonk cave 0x651a97.
- Hook 555 (0x525ef7 -> 0x9589e0): computes the vanilla jump velocity, then for 0x29 `fstp st0`: mVelX is not
  written and keeps the running speed (0.66..0.68) through the vault (IN_VAULT moves by mVelX, no chill factor).
  Landing ~ plant.mX - 191 instead of plant.mX - 70: about 270 px instead of 150.
- 0x651a97 `cmp [esi+0x134],0x29; je 0x651ab8` skips the blocker test 0x7b1910: never bonked; still makes the grave.

**Decision:** the bonk skip was already in the port (`dayLevels` `alwaysVariant 41`); the speed part is added
(`VaultKeepsSpeed`). It vaults once (hook 557 is for 0x32 only).

## 5. Staff Gargantuar summons: where they appear (hook 565)

**Community:** "after its Imp it keeps summoning zombies from the right" (S2); a video titled "the staff Gargantuar
stuck at the screen edge".

**Exe:** the vanilla `mHasObject = false` before the throw is NOPed (0x526f3c..42). The add is the inlined
AddZombieInRow with row PickRowForNewZombie(ZOMBIE_IMP) (0x40dc50). Hook 565 (0x527001 -> 0xc11500): only when
variant 0x106 and mHasObject == 0 does it roll `Rand(33)` (re-rolled; Giga with 0x800258 = 2 around the call),
else it pushes the Imp. After init (0xc1149e -> 0xc11740 -> 0xc114bc): mHasObject != 0 -> clear it and do the
vanilla throw; mHasObject == 0 -> straight to the epilogue 0x5272d5: no x, row or phase write. Hook 568 keeps it in
THROWING while <= 50 zombies and not charmed (it never walks: "stuck").

So: the first throw is always the thrown Imp it carried; every later summon is a plain spawn in a weighted spawn row
at the type's own start x (e.g. 780 + Rand(40)); a rolled Imp is not thrown either.

**Decision:** implemented (`StaffSummonsWithoutThrow`; `RoofGargAddThrown` / `RoofThrownLandsAtOnce` take
"held the Imp"). The earlier ruling (non-Imps set down where an Imp would land) is replaced.
Mac (level 4, one staff Gargantuar, 4 columns of Repeaters): first throw the Imp (t=1658), then summons every
205 ticks (t=1847 Jack row 4, 2052 Giga row 2, 2257 Conehead row 3, 2462 staff Gargantuar row 1), all at x 805..983,
in rows other than the thrower's.

## 6. Red-eye Newspaper (port "football head", subVariant 1)

**Community (1.2.5preview2):** P 1/2; garlic breaks its paper at once but it eats garlic without changing lane;
ignores the weakened debuff and 1/2 chance to ignore 3/4 of a hit; ignores Starfruit effects except charm,
weakness and slow.

**Exe:**
- P: 0xc05770 `Rand(5)` (default) / `Rand(4)` (all elites), sub 1 below 2: 2/5, 1/2 with all elites. Port matches.
- Eats garlic without changing lane: hook 637 0xc05b20. Port matches (`SkipsGarlic`).
- Weakened: 0xc05a70 `Rand(2)`: 0 full (no x2), 1 damage >> 2. Port matches (`ZombieWeakenedDamage`).
- Dream Starfruit kinds: 0xc05a20 / 0xc059d0. Port matches (`StarKindImpact`).
- **New:** TakeDamage entry 0x5317c4 -> 0xc05900: phase 29, type 5, sub 1 -> flags = 0 (no bypass, no
  shield-and-body, no freeze). Not ported before.
- **New:** Garlic aura (hook 618 -> 0x7953c3, 0x7954af -> 0xc05ad0): phase 29, type 5, sub 1 -> DropShield(z, 0)
  instead of TakeDamage(1, 1). Not ported before.

**Decision:** the two new rules implemented (`ClearsHitFlags`, `GarlicRipsPaper`); the rest already matched.

## 7. Potato-head Jack: +7.5 s on cooling packets

**Community:** packets already cooling get +7.5 s (S6; Almanac).

**Exe:** Jack outcome 0x796aa6 -> 0x7a6571 -> 0x796ac1: slots 0..8 of the seed bank: mRefreshTime = GetRefreshTime
(0x7a8530 -> 0x467e30), mActive = 0, mRefreshing = 1; mRefreshCounter (+0x24) is never touched. None of the ten
0x2ee (750) sites in .NewSec touches seed packets.

**Decision:** keep the port. A cooling packet keeps its counter and gets its full refresh time again; there is no
+750 cs.

## 8. White random summoner Dancer (0x104)

**Community:** list includes Jalapeno and Gatling heads; ignores butter and freeze while moonwalking; with its arm a
lethal hit only halves its HP; summons at once after a Blover-type blow or a bite (S1, S3).

**Exe:**
- Follower list: hook 587 0xC03A6F `Rand(0x21)`, rejects 1, 10..20 except 15, 18, 21, 25, **29 (Gatling)**; 28
  Jalapeno only above profile level 70. Port matches; the community's Gatling claim is wrong.
- Freeze / butter: CanBeFrozen 0x531A10 -> ... -> 0xC053C0: phase 40 and variant 0x104 -> return false (ApplyButter
  0x5326E0 and HitIceTrap 0x5323E4 both ask CanBeFrozen; chill is not blocked).
- Lethal hit: TakeDamage entry -> 0x95A470 -> 0xC05400: type 8, phase 40, variant 0x104, mHasArm, and
  `damage + 200 >= body` -> damage 0, body = max >> 1, UpdateDamageStates(0), mHasArm = 0. Once only (the arm).
  ApplyBurn 0xC05490: same four tests -> TakeDamage(1800, 0x12), so one ash plant is survived while dancing in.
- Bite: UpdateZombieDancer's `if (mIsEating) return` -> 0xC05510: phase 40 and 0x104 -> mPhaseCounter = 0, so it
  summons as soon as the bite ends.
- "Blover blow": it is Rewind Grass 0x6B (0x7B0B35 -> 0xC054E0), any Dancer dancing in; already ported
  (`RewindGrassResetsPhaseCounter`).

**Decision:** freeze/butter refusal, the lethal-hit save (and the burn route) and the bite reset implemented.

## 9. Garlic Pogo crushes plants / invisible chance

**Community:** crushes plants; invisible 1/3 (S6, beta5; crush repeated in a 2026-07 comment).

**Exe:** invisibility hook 501 0x796c66..71 `Rand(4)`, `setne [edi+0x18]`: invisible 1/4 (port right). Crush: hook
614 replaces the vanilla Zomboni test at 0x52ad67 with 0x95b010: type 0x12 and +0x134 0x12 -> 0x52ad71, the Zomboni
path: `mFlatTires == 0` -> CheckSquish(DRIVE_OVER) (0x52edb0), every tick from UpdateZombiePosition. Also hook 531
0x95991c: its landing on a zombie makes the yucky face only from the 2nd hit (first hit 0x9598ca, 1800, no yucky).

**Decision:** crush implemented (`PogoCrushesPlants`), first-hit yucky fixed (`PogoLandMakesYucky`); 1/4 kept.
Open: CheckSquish's own entry hook 0x958fb0 skips the squish for a hypnotised squisher or height 9; not ported
(affects Zomboni, coin and gold Football too; outside V1).

## 10. Green Football bite damage

**Community (S2, 1.3beta1):** bite damage grows as its HP falls; after 8 s it drops the helmet and gains 1000.

**Exe:** EatPlant hook 686 0x52fcf0 -> 0xc11260 (coin) -> 0xc12660: type 7, sub 0x1a -> 0xc12f40:
`x = (helmMax + bodyMax) / ((helmType != 0) * helm + body) * type(7)`; `fist` -> if x >= 75 and I, Zombie
(0x4537d0): AddCoin(mX, mY, 6 large sun, motion 2); 0xc12694 `fisub/fchs/fistp`: plant HP = round(HP - x)
(round to nearest even); then the normal 4-HP bite still follows. Examples: full HP +7, no helmet body 300 +77,
body 100 +231. The 8 s helmet event is R4's (Zombie::Animate, not the chew).

**Decision:** implemented (`GreenFootballBite`) after the coin step, before the knife / normal bite. Ruling: the
exe's I, Zombie /40 Sunflower branch that leaves before this hook is not modelled.

## 11. Ladder pile bites while carrying a ladder

**Community:** 3x attack with a ladder, 4x without (S6); "his bites hurt a lot, even more once out of ladders".

**Exe:** bite clock 0x52f640: N = 4 (8 chilled), rem = age % N; hook 672 -> 0x79c300: type 0x15, variant 0x35:
shield type != 3 -> 0x79c35b bites every tick; with a ladder (shield 3) bites when 0 < rem < 6 (3 of 4, chilled
5 of 8). Damage per bite stays 4 (hook 790 changes only 0x37). The pile's target rule 0xc02c90 is reached only from
the vanilla phase block `cmp phase,0x4c/0x4d` (0x52e61d): CHEW on a ladderless cell is refused only while carrying
or placing. The port had the opposite: no bites with a ladder, and CHEW refused in every phase (a pile out of
ladders could never chew).

**Decision:** implemented (`PileBitesThisTick`, `PileTargetRuleOnlyWhileCarrying`; `RoofEatsPlants` no longer blocks
the pile).

## 12. Knife Newspaper vs frozen / one-use plants

**Community:** does not slash plants frozen by the ice-head Jack (bites them instead) (beta11); no effect on
one-use plants (beta5).

**Exe:** the mark (hook 639 0x901deb) skips only seed 4 (Potato Mine). The skipped bite: EatPlant 0x6513d7 ->
0x651210 requires phase 31 and mHasObject, then 0xc02730 requires variant 0x31, `[0x800100] != 1` (no ice-head Jack
freeze) and plant +0x144 == 1 (not Zomboni-frozen); otherwise the normal 4-HP bite (0x651228 -> 0x95c3b0). The kill
0xc02700 needs +0x144 == 1. One-use plants: no knife rule (Cherry, Ice, Doom, Jalapeno trigger first, hook 679).

**Decision:** implemented (`KnifeSkipsBite`: mad, knife held, no ice freeze, plant not frozen). One-use plants:
not in the exe, keep the port. Also fixes the port's "any phase" reading (a reading knife bites normally).

## 13. The low-confidence numbers (community items 16-26)

| # | Claim | Exe | Port |
|---|---|---|---|
| 16 | Zomboss half-HP rage outside Legendary | hooks 633 / 648 and 0xc02586 all need `[0x8001a8] == 1`, set only by the options checkbox (0xb73fbf) | matches (off) |
| 17 | Gatling head spread 33% | `Rand(100)`, `jg` past 0x31 (0x795cf1, 0x795d93): 50% | matches |
| 18 | Orange Zomboni red below 450 | hook 613 0x95a453: body <= 0x15e (350) | matches |
| 19 | Plain Zomboni "does not slow down" | 0x52a81e `fmul qword [0x679748]` reads 14.0f as a double (~5e-315); Steam's same instruction points at -0.2: a 1-byte patch (0x28 -> 0x48 at 0x52a820). Speed stays 0.25 | **was 0.25 -> 0.05; fixed** (`zamboni.plainVelX`) |
| 20 | Sticky-note Normal 2x speed | hook 662 0x79678b x3.0 | matches |
| 21 | Chocolate Pogo 270 HP | 500 - 200 at 0x796c29 = 300 | matches |
| 22 | Gold Football 1/12 | 0x9dd37a `Rand(13)` | matches |
| 23 | Almanac Newspaper +5 body per paper hit | hook 695 0x7a1b02 +15 | matches |
| 25 | Thrown Imp straight into the house | hook 630 0x7a0281 skips the house check only in phases 0x47 / 0x48; throws are always the minimum distance, so a Gargantuar with mX < 73 lands its Imp past the edge | matches |
| 26 | 7-10 frenzy ends at the next bite | 0x7aa260 doubles mAnimRate once, no timer; the next vanilla rate write (StartEating -> UpdateAnimSpeed) resets it | matches in effect |
| 24 | I, Zombie football helmets | R4's | skipped |

## Open points

- Mac evidence: the glove (1), Newspaper (3) and staff (5) runs above; the other rules rest on unit tests. The Pogo
  crush, pile cadence, green bite and white-summoner rules were not watched in a run.
- CheckSquish entry hook 0x958fb0 (hypnotised / height-9 squishers skip) not ported (outside V1).
- ApplyBurn's normal path 0x65150B (`cmp ebx,1800; jno 0x532FDB`) is almost always taken, so nearly every burn
  becomes TakeDamage(1800); whoever owns ApplyBurn may want to recheck `UnnamedTooToughToAsh`.
- `SOURCES-day-levels.md` line 19 called skipVariant 50 the "road-sign" elite; 0x32 is the glove (fixed in the pack).
