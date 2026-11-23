# Sources for data/rules-night-plants.json

Every key below comes from Unnamed 1.3beta2 `PlantsVsZombies.exe` code, read in
the research notes (w2-night) (section in brackets; addresses are the exe's), except the chill rule,
read in the research notes (w4-fog) (X2). The app's fallback for each key is the vanilla behaviour, and every rule is off
while the `nightPlants` feature is off (vanilla mode). Booleans are 0/1, lists are bit masks (rules are numbers only).
App code: `app/src/Mod/Unnamed/NightPlants.*`, sites marked `// PVZU:` in `Plant.cpp`, `Zombie.cpp`, `Board.cpp`.

- `nightPlants.puff.freezeRollRange` = 100: hook 688, 0x79B030 `Rand(0x64)` [1.1]
- `nightPlants.puff.freezeChanceOffset` = 15: hook 688, `ecx = [esi+0x24] + 0xF; cmp eax,ecx; jge skip` (freeze when
  Rand(100) < seed + 15: Puff-shroom 8 → 23 %, Sea-shroom 24 → 39 %); only when `[esi+0x143]` (asleep) is 0; site
  0x52FD38 in `Zombie::EatPlant` right after the plant's HP reached 0 [1.1]
- `nightPlants.puff.freezeChillCs` = 750: hook 688, `call 0x5323C0 (HitIceTrap); mov [ebp+0xAC],0x2EE` [1.1]
- `nightPlants.iceTrap.damage` = 200: hook 718, 0x95B270: Catapult `TakeBodyDamage(200, 1)`, others
  `TakeDamage(200, 1)` (vanilla `TakeDamage(20, 1)`); every HitIceTrap (Ice-shroom, Puff/Sea freeze) [1.7]
- `nightPlants.chill.armBodyDamage` = 10, `nightPlants.chill.armDamageFlags` = 10: hook 692 `0x95b8f0`, site 0x5309e4 in
  `Zombie::ApplyChill` after `mChilledCounter = max(1000/2000, ...)`: `TakeBodyDamage(10, 0x0A)` when `+0xBB` (mHasArm)
  is set. Every chill source (Snow Pea, Winter Melon, Ice-shroom, Puff/Sea freeze, ...). Not part of the Day fireball
  chill (hook 721 sets the counter itself and has its own +10, `dayPlants.fireTier.armBodyDamage`) [w4-fog X2]
- `nightPlants.sunshroom.growCs` = 9000: hook 267, 0x7A3E00 `if IsInPlay: ... state 0x17; countdown 9000` (vanilla
  12000; out of play it stays 12000) [1.2]
- `nightPlants.sunshroom.bonusRollRange` = 100, `nightPlants.sunshroom.bonusMaxRoll` = 11: hook 293, 0x795E5D
  `cmp [edi+0x3c],0x17; je skip; Rand(0x64); cmp eax,0xb; jg skip; push 2; push 5; call AddCoin` (grown only, 12 %,
  COIN_SMALLSUN 15) [1.2]
- `nightPlants.fume.attackWidthPx` = 800: in place in `Plant::GetPlantAttackRect` 0x4680DE `cmp edx,0xa; ... add edx,0x3c;
  mov edi,0x320` (vanilla 340) [1.3]
- `nightPlants.graveBuster.refundCoin` = 6 (COIN_LARGESUN, 50): hook 152, site 0x41D2A6 (DropLootPiece's last
  `AddCoin`), 0x797AC3 `push 2; push 6; AddCoin` (motion FROM_PLANT) [1.4]
- `nightPlants.graveBuster.bonusRollRange` = 3, `nightPlants.graveBuster.bonusRoll` = 1,
  `nightPlants.graveBuster.bonusCoin` = 4 (COIN_SUN, 25): 0x797ADC `Rand(3); cmp eax,1; jne; push 3; push 4; AddCoin`
  (motion COIN). Only when DropLootPiece reached that last AddCoin (no refund on its early returns) [1.4]
- `nightPlants.hypno.bucketHp` = 1200: hook 636, 0x7A0000 `mov [edi+0xc4],2; mov [edi+0xd0],0x4b0; mov [edi+0xd4],0x4b0;
  AssignRenderGroupToPrefix("anim_bucket", 0)` after `TakeDamage([edi+0xd0], 1)`, then StartMindControlled [1.5]
- `nightPlants.hypno.bucketTypesMask` = 603979861: same hook, `cmp [edi+0x24],0/2/4/0x1a/0x1d/6` = bits 0 (Normal),
  2 (Cone), 4 (Bucket), 6 (Screen Door), 26 (Peashooter zombie), 29 (Gatling zombie) [1.5]
- `nightPlants.scaredy.hp` = 1500: `.text` cave 0x65198A from PlantInitialize hook 263: `cmp [ebx+0x24],0xd;
  mov [ebx+0x40],0x5dc` (vanilla 300) [1.6]
- `nightPlants.scaredy.secondShotAtCounter` = 25: hook 290, 0x7A8850 `cmp eax,0xd; jz 0x45F96D` (the vanilla Repeater
  "second shot at launch counter 25" branch, `FindTargetAndFire(row, PRIMARY)`) [1.6]
- `nightPlants.doom.radiusPx` = 990, `nightPlants.doom.rowRange` = 6: in place in `Plant::DoSpecial` 0x466838
  `push 0x3de`, 0x466836 `push 6` (vanilla 250, 3) [1.8]
- `nightPlants.doom.craterCs` = 24000: 0x466884 `mov [eax+0x18],0x5dc0` (vanilla 18000) [1.8]

Not ported: the Imitater Doom-shroom grave clear (hook 345, 0xC118F0 `cmp [ebx+0x138],0xf`). `+0x138` is
mImitaterType, which on a morphed Imitater is SEED_IMITATER, not Doom; the read needs a second look, and Imitater is
not reachable in world 2.

English corrections (`strings/en-corrections-night-plants.txt`, code wins over the Almanac):
- Hypno-shroom: the Almanac says "a zombie built on the basic zombie"; the code's list is Normal, Cone, Bucket, Screen
  Door, Peashooter and Gatling zombie (no Flag, no Newspaper).
- Scaredy-shroom: the Almanac says "fires two spores at a time" / "raises its attack speed while attacking"; the code
  only adds the Repeater's second shot at launch counter 25 (launch rate stays 150, table 0x69F4A0; no speed code found).
