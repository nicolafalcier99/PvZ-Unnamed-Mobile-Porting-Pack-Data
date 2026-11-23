# pvz-unnamed-pack

The data pack for the **Unnamed** mode of
[PvZ-Unnamed-Mobile-Porting-Pack](https://github.com/nicolafalcier99/PvZ-Unnamed-Mobile-Porting-Pack) (the game code), a port of the Chinese *Plants vs. Zombies*
mod "Unnamed" (植物大战僵尸无名版) 1.3beta2 to PvZ-Portable. It holds the mod's rules as numbers: plant, zombie and
projectile stats, elite zombies, levels 51-73, the 26 mod-only plants and the 48 mod-only game modes, each value with
the place in the mod's game where it was read (`SOURCES-*.md`).

Clone it next to the code as `pvz-unnamed-pack`, where the build scripts look for it:

```sh
git clone https://github.com/nicolafalcier99/PvZ-Unnamed-Mobile-Porting-Pack.git pvz-unnamed
git clone https://github.com/nicolafalcier99/PvZ-Unnamed-Mobile-Porting-Pack-Data.git pvz-unnamed-pack
```

## Credits

The Unnamed mod is the work of its authors; its official channel is the Tencent Channel "植物大战僵尸无名版" by JFY,
and its in-game credits name HwequentBrony as mod author and 伴久九技高一筹 as an Almanac contributor. This pack is not
affiliated with or endorsed by them, by PopCap Games or by Electronic Arts. *Plants vs. Zombies* belongs to PopCap
Games / Electronic Arts.

## What is not here

- **No game files**: no images, music, sounds or text files from the game or the mod. For the mod's art and music,
  import your own copy of the Unnamed 1.3beta2 zip (see the code repository's README); it lands in `assets/`, which git
  ignores.
- **None of the mod's own text**: its Almanac descriptions, tooltips, messages and our English translations of them
  are left out until the mod's authors agree. In Chinese Text mode the game reads the mod's text from your imported
  zip; in English mode it shows the vanilla text, short code fallbacks for a few messages, and the names kept here.

## Layout

- `mod.json`: the pack id and its features (each one switches a group of rules on; `testCheats` is off).
- `data/plants.json`, `data/zombies.json`, `data/projectiles.json`: stat changes keyed by the engine's enum names.
- `data/rules-*.json`: the mod's constants, one file per area (a missing key = vanilla behaviour).
- `data/levels-51-73.json`, `data/modes.json`, `data/mod-plants.json`: the mod's extra levels, modes and plants.
- `strings/`: the port's own words only (`mod-almanac-en.txt`: Almanac pages and hints for the mod plants;
  `en-corrections-*.txt`: UI labels and Almanac names in the game's LawnStrings format).
- `SOURCES*.md`: where each number comes from.
- `tools/`: table builders and their tests.

## License

MIT (see `LICENSE`), for this port's own work: the tables as arranged here, the source notes, the tools and the
port's own text. It grants no rights to *Plants vs. Zombies* (PopCap Games / Electronic Arts) or to the Unnamed mod,
which belong to their owners.
