"""Builds pack data/modes.json for the 48 Unnamed mod modes 0x65..0x94 from the read-only spec tables
(scratchpad specs E.md sections 1-3, B.md, D.md, A.md, C.md: hooks 12, 20, 25, 29-31, 35/36, 94, 130, 140-145, 160,
162, 176-180, 425). Per-mode status/notes are set in STATUS below. usage: gen_modes.py out.json"""
import json, sys

NAMES = {  # hook 12 table 0x850000 + (mode-0x65)*0x10 (E.md 1.5)
    0x65: ("艺术就是爆炸", "Art Is an Explosion"), 0x66: ("阳光风暴", "Sun Storm"), 0x67: ("请勿戏水", "No Playing in the Water"),
    0x68: ("持久战", "War of Attrition"), 0x69: ("视觉失调", "Visual Disorder"), 0x6a: ("顺流", "Downstream"),
    0x6b: ("手套之战", "Glove War"), 0x6c: ("僵尸快快快跑", "Zombies, Run Run Run"), 0x6d: ("黑夜惊魂", "Night Terror"),
    0x6e: ("小僵尸巨麻烦", "Little Zombie, Big Trouble"), 0x6f: ("八级大狂风", "Force-8 Gale"), 0x70: ("神兵天降", "Troops from the Sky"),
    0x71: ("The Counter", "The Counter"), 0x72: ("单枪匹马", "Lone Wolf"), 0x73: ("卡槽危机", "Seed Slot Crisis"),
    0x74: ("阴雨天", "Rainy Day"), 0x75: ("海森堡的僵尸", "Heisenberg's Zombie"), 0x76: ("薛定谔的僵尸", "Schrödinger's Zombie"),
    0x77: ("逆流", "Upstream"), 0x78: ("向日葵指挥官", "Sunflower Commander"), 0x79: ("巨人危机", "Giant Crisis"),
    0x7a: ("大僵尸小麻烦", "Big Zombie, Little Trouble"), 0x7b: ("频率切换", "Frequency Switch"), 0x7c: ("光明与雾霭", "Light and Mist"),
    0x7d: ("随机砸罐", "Random Vasebreaker"), 0x7e: ("两面包夹", "Pincer Attack"), 0x7f: ("套路的套路", "Trick of Tricks"),
    0x80: ("限量供应", "Limited Supply"), 0x81: ("Luck：欧非鉴定", "Luck: Lucky or Unlucky?"), 0x82: ("种豆得瓜", "Sow Beans, Reap Melons"),
    0x83: ("二爷博士的复仇", "Dr. Second-Master's Revenge"), 0x84: ("以牙还牙", "An Eye for an Eye"),
    0x85: ("僵尸反间计", "Zombie Counter-Espionage"), 0x86: ("左倾", "Leaning Left"), 0x87: ("手套之战 2", "Glove War 2"),
    0x88: ("领地意识", "Territorial"), 0x89: ("贪吃星", "Glutton Star"), 0x8a: ("隐形守护者", "Invisible Guardian"),
    0x8b: ("子弹狂欢", "Bullet Carnival"), 0x8c: ("我是Luck", "I Am Luck"), 0x8d: ("手套之战3", "Glove War 3"),
    0x8e: ("曾哥与WASD", "Brother Zeng and WASD"), 0x8f: ("高坚果的试探", "Tall-nut's Probe"), 0x90: ("套路的套路2", "Trick of Tricks 2"),
    0x91: ("全是一个", "All the Same One"), 0x92: ("精英僵尸的挑战", "Elite Zombies' Challenge"),
    0x93: ("未命名关卡", "Unnamed Level"), 0x94: ("未命名关卡", "Unnamed Level"),
}
BG = {0: [0x66, 0x68, 0x69, 0x6b, 0x6e, 0x73, 0x75, 0x77, 0x79, 0x7a, 0x7e, 0x80, 0x83, 0x89, 0x8a, 0x8d, 0x8e, 0x90, 0x92, 0x93, 0x94],
      1: [0x65, 0x6d, 0x72, 0x7d, 0x81, 0x87, 0x8b, 0x8c, 0x8f, 0x91], 2: [0x67, 0x6a, 0x74, 0x78], 3: [0x6f, 0x7b, 0x7c, 0x84],
      4: [0x70, 0x76, 0x85, 0x86], 6: [0x71, 0x82, 0x88], 7: [0x7f], 8: [0x6c]}  # hook 25
WAVES = {0: [0x8b], 10: [0x7d], 20: [0x65, 0x67, 0x68, 0x6e, 0x70, 0x77, 0x84], 25: [0x92],
         30: [0x66, 0x69, 0x6a, 0x6b, 0x6c, 0x6f, 0x71, 0x73, 0x74, 0x75, 0x76, 0x7a, 0x7b, 0x7c, 0x7e, 0x80, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x8e],
         40: [0x6d, 0x72, 0x78, 0x79, 0x7f, 0x81, 0x82, 0x83, 0x85, 0x8c, 0x8d, 0x8f, 0x90, 0x93, 0x94], 60: [0x91]}  # hook 20
SUN = {0x73: 1000, 0x7f: 200, 0x80: 2000, 0x83: 500000, 0x8a: 200, 0x8c: 6750, 0x92: 500}  # hooks 30/31
SLOTS = {0x72: 1, 0x73: 1, 0x91: 1, 0x7d: 1, 0x8f: 1, 0x89: 3, 0x87: 7, 0x76: 9}  # hooks 141/142
NO_CHOOSER = [0x8b, 0x76, 0x79, 0x8d, 0x8e]  # hooks 35/36 in ChooseSeedsOnCurrentLevel
CONVEYOR = [0x71, 0x81, 0x84]  # hook 140
NO_SKY_SUN = [0x72, 0x74]  # hook 94
NO_GRAVES = [0x6d, 0x91]  # hooks 143, 144
FIRST_WAVE = {0x92: 7500, 0x68: 5500, 0x74: 5500, 0x72: 250}  # hook 29 (0x92), hook 160 at level start
BANNED = {  # hook 425 (E.md 1.4); mod seeds 0x51/0x59 left out until Plan 8 names them
    0x66: ["SUNFLOWER", "SUNSHROOM", "TWINSUNFLOWER", "SEASHROOM", "PUFFSHROOM"],
    0x78: ["SUNFLOWER", "SUNSHROOM", "TWINSUNFLOWER", "SEASHROOM", "PUFFSHROOM"],
    0x67: ["LILYPAD", "TANGLEKELP", "SEASHROOM", "CATTAIL"], 0x70: ["UMBRELLA"], 0x90: ["SQUASH"]}
COLOR = {"red": [0x66, 0x6c, 0x6e, 0x70, 0x79, 0x7c, 0x88, 0x8a, 0x90, 0x92],
         "purple": [0x65, 0x72, 0x75, 0x76, 0x7b, 0x7f, 0x86, 0x89],
         "blue": [0x67, 0x6d, 0x73, 0x7a, 0x7d, 0x80, 0x82, 0x84, 0x8e, 0x91],
         "green": [0x69, 0x78, 0x81, 0x85, 0x8c],
         "pulse": [0x68, 0x6a, 0x6b, 0x6f, 0x71, 0x74, 0x77, 0x7e, 0x87, 0x8b, 0x8d]}  # hook 130; others vanilla gold
Z = {"Cone": "TRAFFIC_CONE", "Pole": "POLEVAULTER", "Football": "FOOTBALL", "Dancer": "DANCER", "Jack": "JACK_IN_THE_BOX",
     "Balloon": "BALLOON", "Garg": "GARGANTUAR", "Digger": "DIGGER", "Ladder": "LADDER", "Door": "DOOR", "Snorkel": "SNORKEL",
     "Newspaper": "NEWSPAPER", "Tallnut-h": "TALLNUT_HEAD", "Wallnut-h": "WALLNUT_HEAD", "Squash-h": "SQUASH_HEAD",
     "Pea-h": "PEA_HEAD", "Gatling-h": "GATLING_HEAD", "Jalapeno-h": "JALAPENO_HEAD", "Redeye": "REDEYE_GARGANTUAR",
     "Dolphin": "DOLPHIN_RIDER", "Zamboni": "ZAMBONI", "Pogo": "POGO", "Catapult": "CATAPULT", "Bungee": "BUNGEE", "Pail": "PAIL"}
# E.md section 3: the mode's own list (Normal is added unless noNormal); P = Pail and Yeti kept; empty list = Cone + P
ALLOW = {
    0x65: ("Cone Pole Dancer Digger Ladder", False), 0x66: ("Cone Pole Football Dancer Jack Balloon Garg", True),
    0x67: ("Cone Jack Pogo Ladder Catapult", True), 0x68: ("Cone Door Dancer Ladder Garg", True),
    0x69: ("Cone Pole Dancer Tallnut-h", False), 0x6a: ("Cone Snorkel Newspaper Garg", True),
    0x6b: ("Cone Pole Football Dancer Jack Digger Squash-h Tallnut-h", True), 0x6c: ("Door Dolphin Jack Pogo Garg", False),
    0x6d: ("Cone Door", True), 0x6e: ("Cone Football Zamboni Pogo Catapult Pea-h Wallnut-h Redeye", False),
    0x6f: ("Cone Pole Football Snorkel Zamboni", True), 0x70: ("Cone Bungee Ladder Catapult Garg Gatling-h", True),
    0x71: ("Door Zamboni Digger Ladder Catapult", False), 0x72: ("Cone Digger Jalapeno-h Jack Ladder Garg", False),
    0x73: ("Cone Pole Newspaper Garg", False), 0x74: ("Dancer Zamboni Pogo Ladder Catapult", True),
    0x75: ("Cone Pole Football Digger Bungee Squash-h Jalapeno-h", True), 0x76: ("Newspaper Dancer Ladder Garg Squash-h", True),
    0x77: ("Football Newspaper Jack Digger Catapult", True), 0x78: ("Cone Pole Snorkel Zamboni Digger Jalapeno-h Tallnut-h", True),
    0x79: ("Garg Redeye", False), 0x7a: ("Cone Door Jack Squash-h", False),
    0x7b: ("Football Snorkel Dolphin Balloon Digger Ladder Gatling-h", True), 0x7c: ("Pole Snorkel Jack Pogo Catapult Garg Jalapeno-h", True),
    0x7d: ("", True), 0x7e: ("Door Football Jack Bungee Wallnut-h Tallnut-h", False), 0x7f: ("Pole Balloon Garg", True),
    0x80: ("Cone Door Dancer Digger Pogo Catapult", True),
    0x81: ("Cone Pole Door Football Zamboni Bungee Ladder Garg Redeye Wallnut-h Tallnut-h", True),
    0x82: ("Cone Newspaper Zamboni Ladder Garg Pea-h Gatling-h Redeye", True), 0x83: ("", True),
    0x84: ("Cone Football Dancer Pea-h Gatling-h Garg", True), 0x85: ("Cone Digger", False),
    0x86: ("Pole Football Dancer Pogo Ladder Garg", False), 0x87: ("Pea-h Newspaper Balloon Catapult Garg", False),
    0x88: ("Cone Pole Pogo Catapult Ladder Garg Jalapeno-h", True),
    0x89: ("Newspaper Football Dancer Garg Squash-h Tallnut-h Redeye", True), 0x8a: ("Pole Bungee Pea-h Catapult Tallnut-h", False),
    0x8b: ("", True), 0x8c: ("", True),
    0x8d: ("Cone Pail Newspaper Door Football Jack Catapult Garg Pea-h Squash-h Tallnut-h", True),
    0x8e: ("Cone Door Football Ladder Wallnut-h Squash-h Tallnut-h", True), 0x8f: ("", True),
    0x90: ("Pole Pail Newspaper Ladder Garg", True), 0x91: ("Pail Football Zamboni Jack Garg Tallnut-h Redeye", True),
    0x92: ("Dancer", True), 0x93: ("", True), 0x94: ("", True),
}
NO_NORMAL = [0x79, 0x85]
# hook 162 (0x799e01): conveyor seeds and weights.
CONVEYOR_SEEDS = {0x84: [["HYPNOSHROOM", 80], ["LILYPAD", 16], ["BLOVER", 4]],
                  0x81: [["SPROUT", 90], ["CHERRYBOMB", 5], ["GRAVEBUSTER", 5]],
                  0x71: [["REPEATER", 20], ["0x72", 20], ["POTATOMINE", 9], ["SPIKEWEED", 21], ["ICESHROOM", 15],
                        ["MAGNETSHROOM", 15]]}  # "0x72" = mod seed Butter-pult (Kernel-pult + 80)
# hook 32 (Board::InitLevel fixed banks); mod seeds are written "0x59".
BANK = {0x76: ["FLOWERPOT", "SUNFLOWER", "0x59", "POTATOMINE", "CHERRYBOMB", "JALAPENO", "TALLNUT", "MELONPULT", "BLOVER"],  # 0x7a6e00
        0x79: ["SUNFLOWER", "SNOWPEA", "MARIGOLD", "INSTANT_COFFEE", "ICESHROOM", "DOOMSHROOM", "DOOMSHROOM", "CHERRYBOMB",
               "SQUASH", "POTATOMINE"]}


def inv(d):
    return {m: k for k, ms in d.items() for m in ms}


def build(status):
    bg, waves, color = inv(BG), inv(WAVES), inv(COLOR)
    out = {}
    for m in range(0x65, 0x95):
        zh, en = NAMES[m]
        r = {"name": en, "nameZh": zh, "background": bg[m], "waves": waves[m]}
        lst, pail = ALLOW[m]
        if lst:
            r["allowed"] = [Z[x] for x in lst.split()]
        r["pail"] = pail
        if m in NO_NORMAL:
            r["normal"] = False
        if m in SUN: r["startSun"] = SUN[m]
        if m in SLOTS: r["seedSlots"] = SLOTS[m]
        if m in NO_CHOOSER: r["chooser"] = False
        if m in CONVEYOR: r["conveyor"] = True
        if m in NO_SKY_SUN: r["skySun"] = False
        if m in NO_GRAVES: r["graves"] = 0
        if m in FIRST_WAVE: r["firstWaveCountdown"] = FIRST_WAVE[m]
        if m in BANNED: r["bannedSeeds"] = BANNED[m]
        if m in CONVEYOR_SEEDS: r["conveyorSeeds"] = CONVEYOR_SEEDS[m]
        if m in BANK: r["bank"] = BANK[m]
        r["nameColor"] = color.get(m, "gold")
        st = status.get(m, ("unknown", "Rules not read yet", None, None))
        r["status"] = "placeholder" if m >= 0x93 else st[0]
        if m >= 0x93:
            r["note"] = "An empty slot in the mod itself"
        elif st[1]:
            r["note"] = st[1]
        if st[2]:
            r["key"] = st[2]
        if st[3]:
            r["rules"] = st[3]
        out[f"0x{m:02x}"] = r
    return out


STATUS = json.load(open(sys.argv[2], encoding='utf-8')) if len(sys.argv) > 2 else {}
STATUS = {int(k, 16): tuple(v) for k, v in STATUS.items()}
with open(sys.argv[1], 'w', encoding='utf-8') as f:
    json.dump(build(STATUS), f, ensure_ascii=False, indent='\t')
    f.write('\n')
print('ok')
