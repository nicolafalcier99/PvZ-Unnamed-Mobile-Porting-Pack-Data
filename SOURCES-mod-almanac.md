# Sources for the mod-plant guide (feature `modAlmanac`, port-only)

Unnamed 1.3beta2 has no Almanac pages for its 26 mod-only plants (its Plant Almanac lists the 49 vanilla plants) and no
hints for them. This feature is a port addition, so it can be turned off (`mod.json` feature `modAlmanac`, or the rules
below) and the game is exactly like the mod again. Nothing here changes a rule of the game.

Files
- `strings/mod-almanac-en.txt`: each plant's Almanac text (`MOD_PLANT_0x.._DESCRIPTION`, `_HOW_TO_USE`), the lawn
  hints (`MOD_HINT_*`) and the page's own words. `strings/mod-almanac-zh.txt`: Chinese words for the page; missing keys
  fall back to English. Plant names and costs come from `data/mod-plants.json` (names in the game's language).
- `data/mod-plants.json` `tooltip.en`: rewritten as one line that also says how to use the plant (the seed chooser's
  tooltip). The Loaded Cannon had none (the exe has no tooltip for it); `tooltip.zh` is the exe's text, unchanged.
- `data/rules-mod-almanac.json`: `modAlmanac.pages` (0 hides the "More plants" Almanac grid), `modAlmanac.hints` (0
  turns every lawn hint off). A hint with an empty or missing text is not shown.

Where the numbers come from (the port's behaviour; exe evidence for each is in `SOURCES-mod-plants.md` /
the research notes (mod-plants-behaviour)): costs and recharges from `data/mod-plants.json` (recharge shown in seconds =
refreshTime / 100); damage, timers and areas from `data/rules-mod-plants.json` and `rules-mod-plants-shadow.json`, e.g.
Sniper `sniper.periodCs` 500 / `sniper.damage` 500; Prism `prismShroom.*` 300 + min(sun, 1000) / 4; Mystic-Ice 1 pea a
tick for its launch rate 500; Rewind Grass `rewindGrass.blowDelayCs` 50; Loaded Cannon `loadedCannon.kernelBurnCap`
3000 / `doomBurnCap` 3600 / `packetPenaltyCs` 6000; shadow thresholds `shadow.threshold*` (Moonflower, Fire-dragon,
Dream Starfruit 3, Charmed Tall-nut 2, others 1). Star damage 2 (`projectiles.json` STAR 1, doubled) + the colour bonus
15..25 gives Dream Starfruit's 17..27. Shrapnel Cherry's core becomes a Cherry Bomb at age 1400 cs (the tooltip's
"12 s" is the exe's text; code wins: 14 s). How-to lines for the Loaded Cannon, Magic Devourer, Sniper and Rewind Grass
came verified on the Mac with the task (2026-11-23).

Hints (shown on the game's message bar, `MESSAGE_STYLE_HINT_*`, never over a tutorial or level message):
- planted (once per level per plant, only when the player plants it from a packet or a dropped card): `PLANTED_*`, or
  `SHADOW_*` when a shadow plant stands without enough shadow points for its threshold;
- tap: an unloaded Loaded Cannon (cob state ARMING), a Prism-shroom that would fire but the sun is under 50;
- refused: a Magic Devourer / Strong Coffee Bean that cannot go there gets its own line instead of the Coffee Bean
  message; it keeps that message's once-per-level rule and the exe's refusal itself.
