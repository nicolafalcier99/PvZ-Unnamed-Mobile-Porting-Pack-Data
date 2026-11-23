#!/usr/bin/env python3
"""Writes data/mod-plants.json from the study's decode of the exe's mod-plant table (0x860000).

Run: python3 -I tools/make_mod_plants.py <study>/out/unnamed-tables.json data/mod-plants.json
Numbers, Chinese names and tooltips come from the table bytes (the research notes (decode_tables), row
`extended_plants_0x860000`); the English text is ours (the research notes (w6-w7-and-new-content) 5.1). Empty rows (no name,
cost 0: 0x54) are left out. Evidence and field meanings: SOURCES-mod-plants.md.
"""
import json
import sys

# Engine SeedType names (app/src/Mod/Engine/EngineTables.cpp kPlantNames), index = SeedType.
ENGINE_NAMES = [
    "PEASHOOTER", "SUNFLOWER", "CHERRYBOMB", "WALLNUT", "POTATOMINE", "SNOWPEA",
    "CHOMPER", "REPEATER", "PUFFSHROOM", "SUNSHROOM", "FUMESHROOM", "GRAVEBUSTER",
    "HYPNOSHROOM", "SCAREDYSHROOM", "ICESHROOM", "DOOMSHROOM", "LILYPAD", "SQUASH",
    "THREEPEATER", "TANGLEKELP", "JALAPENO", "SPIKEWEED", "TORCHWOOD", "TALLNUT",
    "SEASHROOM", "PLANTERN", "CACTUS", "BLOVER", "SPLITPEA", "STARFRUIT",
    "PUMPKINSHELL", "MAGNETSHROOM", "CABBAGEPULT", "FLOWERPOT", "KERNELPULT", "INSTANT_COFFEE",
    "GARLIC", "UMBRELLA", "MARIGOLD", "MELONPULT", "GATLINGPEA", "TWINSUNFLOWER",
    "GLOOMSHROOM", "CATTAIL", "WINTERMELON", "GOLD_MAGNET", "SPIKEROCK", "COBCANNON",
    "IMITATER", "EXPLODE_O_NUT", "GIANT_WALLNUT", "SPROUT", "LEFTPEATER",
]

# seed: (English name, English tooltip). Translations of the table's GBK name / tooltip (study 5.1).
ENGLISH = {
    0x50: ("Shadow Peashooter", "Fires shadow peas. In shadow state it fires a shadow beam that slows zombies."),
    0x51: ("Primal Sunflower", "Steadily makes a larger amount of sun."),
    0x52: ("Shrapnel Cherry", "Blows up like a fragmentation grenade, then blows up again 12 seconds later."),
    0x53: ("Bowling Wall-nut", "Lets you bowl on any level."),
    0x55: ("Mystic-Ice Shooter", "Fires 500 ice peas in 5 seconds, then vanishes. While it stands, peas turn into ice "
                                 "peas; when it vanishes, Peashooters turn into Snow Peas."),
    0x56: ("Fire-dragon Grass", "Breathes fire on every zombie a short way ahead, but it also ends their slowing and "
                                "freezing."),
    0x57: ("Primal Repeater", "10% of its peas knock zombies back, 10% poison them."),
    0x58: ("Toxic Shadow-shroom", "A zombie that eats it is poisoned and keeps taking damage. In shadow state the "
                                  "poison ignores armour."),
    0x59: ("Golden Sun-shroom", "Makes a lot of sun at once, then vanishes."),
    0x5b: ("Magic Devourer", "Swallows a plant and turns it into a seed card."),
    0x5c: ("Hallucination-shroom", "A zombie that eats it turns into an Imp."),
    0x5d: ("Prism-shroom", "Tap it to spend sun and fire."),
    0x67: ("Charmed Tall-nut", "For every 1200 health it loses, a hypnotised Zombie, Newspaper Zombie or Gargantuar "
                               "rises from the ground to fight for you, with 1.35 times its health."),
    0x69: ("Moonflower", "Puts nearby shadow plants into shadow state. Makes small sun; normal sun in shadow state."),
    0x6b: ("Rewind Grass", "Sends every zombie back to the right edge of the lawn at full health."),
    0x6d: ("Dream Starfruit", "Fires stars of different colours that do different things to zombies."),
    0x6e: ("Holy-fire Pumpkin", "Keeps the plant inside from being frozen by a Zomboni, but cannot thaw a plant that is "
                                "already frozen."),
    0x70: ("Dusk-pult", "Lobs cabbages at zombies. In shadow state it lobs at three rows."),
    0x72: ("Butter-pult", "Lobs butter at zombies."),
    0x73: ("Strong Coffee Bean", "Wakes up every plant around it."),
    0x75: ("Leaf Shield", "Bounces back zombie shots flying at the three rows ahead. Each bounce costs it some health."),
    0x76: ("Boss Flower", "Can drop any plant card."),
    0x78: ("Sniper", "Snipes the target with the most health on the lawn ahead (never a boss)."),
    0x7a: ("Element-shroom", "Gives off smoke around itself and now and then takes on an element. Its last 3 elements "
                             "decide what it does."),
    0x7b: ("Spirit-tail", "Fires a random projectile (never a zombie's shot or a fireball)."),
    0x7f: ("Loaded Cannon", ""),  # the exe has no tooltip for it
}


def main():
    src, out = sys.argv[1], sys.argv[2]
    rows = json.load(open(src, encoding="utf-8"))["extended_plants_0x860000"]
    table = {}
    for r in rows:
        seed = r["mSeedType"]
        if not r["name_gbk"]:
            continue  # empty slot (0x54)
        base = seed - 0x50
        assert r["base_seed_guess"] == "SEED_" + ENGINE_NAMES[base], (hex(seed), r["base_seed_guess"])
        en_name, en_tip = ENGLISH[seed]
        table[str(seed)] = {
            "hex": hex(seed),
            "base": ENGINE_NAMES[base],
            "name": {"en": en_name, "zh": r["name_gbk"]},
            "tooltip": {"en": en_tip, "zh": r["tooltip_gbk"].replace("\n", " ")},
            "seedCost": r["mSeedCost"],
            "refreshTime": r["mRefreshTime"],
            "launchRate": r["mLaunchRate"],
            "subclass": "shooter" if r["mSubClass"] == 1 else "normal",
            "tint": [r["f24"], r["f28"], r["f2c"], r["f30"]],
        }
    assert len(table) == 26, len(table)
    with open(out, "w", encoding="utf-8") as f:
        f.write("{\n")
        items = list(table.items())
        for i, (k, v) in enumerate(items):
            f.write("\t" + json.dumps(k) + ": " + json.dumps(v, ensure_ascii=False) + ("," if i + 1 < len(items) else "") + "\n")
        f.write("}\n")


if __name__ == "__main__":
    main()
