# Sources for every Unnamed value in this pack

Tables: read from Unnamed 1.3beta2 `PlantsVsZombies.exe` (sha256 d39b3429...e89f66) by the research notes (tools) (hook-triage study),
the research notes (unnamed-tables); built by `tools/make_tables.py` against the app vanilla dump `tools/fixtures/vanilla-tables.json`.
Plant row = 0x69F2B0 + 0x24*i (+0x10 cost, +0x14 refresh, +0x1C launch); zombie row = 0x69DA80 + 0x1C*i; projectile row = 0x69F1C0 + 0xC*i (+8 damage).

| table | name | field | vanilla | Unnamed | exe row |
|---|---|---|---|---|---|
| plants | WALLNUT | refreshTime | 3000 | 2400 | 0x69f31c |
| plants | POTATOMINE | seedCost | 25 | 50 | 0x69f340 |
| plants | FUMESHROOM | seedCost | 75 | 100 | 0x69f418 |
| plants | GRAVEBUSTER | seedCost | 75 | 50 | 0x69f43c |
| plants | HYPNOSHROOM | seedCost | 75 | 100 | 0x69f460 |
| plants | SCAREDYSHROOM | seedCost | 25 | 75 | 0x69f484 |
| plants | DOOMSHROOM | seedCost | 125 | 150 | 0x69f4cc |
| plants | LILYPAD | refreshTime | 750 | 500 | 0x69f4f0 |
| plants | THREEPEATER | seedCost | 325 | 350 | 0x69f538 |
| plants | TANGLEKELP | seedCost | 25 | 50 | 0x69f55c |
| plants | SPIKEWEED | seedCost | 100 | 125 | 0x69f5a4 |
| plants | TALLNUT | seedCost | 125 | 150 | 0x69f5ec |
| plants | TALLNUT | refreshTime | 3000 | 2400 | 0x69f5ec |
| plants | PLANTERN | seedCost | 25 | 150 | 0x69f634 |
| plants | PLANTERN | refreshTime | 3000 | 3600 | 0x69f634 |
| plants | CACTUS | seedCost | 125 | 175 | 0x69f658 |
| plants | BLOVER | seedCost | 100 | 150 | 0x69f67c |
| plants | BLOVER | refreshTime | 750 | 1000 | 0x69f67c |
| plants | SPLITPEA | seedCost | 125 | 175 | 0x69f6a0 |
| plants | STARFRUIT | seedCost | 125 | 175 | 0x69f6c4 |
| plants | STARFRUIT | refreshTime | 750 | 2500 | 0x69f6c4 |
| plants | STARFRUIT | launchRate | 150 | 250 | 0x69f6c4 |
| plants | PUMPKINSHELL | seedCost | 125 | 200 | 0x69f6e8 |
| plants | PUMPKINSHELL | refreshTime | 3000 | 2400 | 0x69f6e8 |
| plants | MAGNETSHROOM | seedCost | 100 | 125 | 0x69f70c |
| plants | FLOWERPOT | refreshTime | 750 | 500 | 0x69f754 |
| plants | GARLIC | seedCost | 50 | 100 | 0x69f7c0 |
| plants | GARLIC | refreshTime | 750 | 1200 | 0x69f7c0 |
| plants | MARIGOLD | seedCost | 50 | 150 | 0x69f808 |
| plants | MARIGOLD | refreshTime | 3000 | 6000 | 0x69f808 |
| plants | MELONPULT | launchRate | 300 | 225 | 0x69f82c |
| plants | GLOOMSHROOM | seedCost | 150 | 125 | 0x69f898 |
| plants | CATTAIL | seedCost | 225 | 200 | 0x69f8bc |
| plants | WINTERMELON | launchRate | 300 | 225 | 0x69f8e0 |
| plants | GOLD_MAGNET | seedCost | 50 | 100 | 0x69f904 |
| plants | GOLD_MAGNET | refreshTime | 5000 | 1800 | 0x69f904 |
| plants | SPIKEROCK | seedCost | 125 | 150 | 0x69f928 |
| plants | EXPLODE_O_NUT | seedCost | 0 | 50 | 0x69f994 |
| plants | GIANT_WALLNUT | seedCost | 0 | 50 | 0x69f9b8 |
| plants | SPROUT | seedCost | 0 | 75 | 0x69f9dc |
| plants | SPROUT | refreshTime | 3000 | 900 | 0x69f9dc |
| plants | LEFTPEATER | seedCost | 200 | 75 | 0x69fa00 |
| zombies | POLEVAULTER | zombieValue | 2 | 3 | 0x69dad4 |
| zombies | POLEVAULTER | pickWeight | 2000 | 3000 | 0x69dad4 |
| zombies | NEWSPAPER | pickWeight | 1000 | 3000 | 0x69db0c |
| zombies | FOOTBALL | zombieValue | 7 | 5 | 0x69db44 |
| zombies | DANCER | zombieValue | 5 | 3 | 0x69db60 |
| zombies | DANCER | pickWeight | 1000 | 2000 | 0x69db60 |
| zombies | ZAMBONI | zombieValue | 7 | 5 | 0x69dbd0 |
| zombies | ZAMBONI | pickWeight | 2000 | 1000 | 0x69dbd0 |
| zombies | JACK_IN_THE_BOX | zombieValue | 3 | 2 | 0x69dc24 |
| zombies | JACK_IN_THE_BOX | pickWeight | 1000 | 1500 | 0x69dc24 |
| zombies | POGO | zombieValue | 4 | 2 | 0x69dc78 |
| zombies | BUNGEE | zombieValue | 3 | 2 | 0x69dcb0 |
| zombies | LADDER | zombieValue | 4 | 3 | 0x69dccc |
| zombies | LADDER | pickWeight | 1000 | 2000 | 0x69dccc |
| zombies | CATAPULT | zombieValue | 5 | 3 | 0x69dce8 |
| zombies | GARGANTUAR | zombieValue | 10 | 6 | 0x69dd04 |
| zombies | GATLING_HEAD | zombieValue | 3 | 5 | 0x69ddac |
| projectiles | STAR | damage | 20 | 1 | 0x69f214 |
| projectiles | SPIKE | damage | 20 | 1 | 0x69f220 |
| projectiles | COBBIG | damage | 300 | 400 | 0x69f244 |

Mod-only plants (seed types 0x50+, table 0x860000): not in this pack yet (Plan 3).

Text: `strings/en.txt` translated from the mod's LawnStrings.txt (keys listed in `strings/en-report.md`).
