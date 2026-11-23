"""Builds data/plants.json, zombies.json, projectiles.json from Unnamed's exe tables
(the research notes (unnamed-tables), read by the hook-triage study) against the app's vanilla dump
(-pvzu-dump-tables). Writes only fields that differ. Mod-only plants (seed type >= 0x50) are left for Plan 3.
Usage: python3 -I tools/make_tables.py [unnamed-tables.json] [vanilla-tables.json]"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_STUDY = os.path.expanduser('~/pvz-research/unnamed-tables.json')
DEFAULT_VANILLA = os.path.join(HERE, 'fixtures', 'vanilla-tables.json')

PLANT_FIELDS = {'seedCost': 'mSeedCost', 'refreshTime': 'mRefreshTime', 'launchRate': 'mLaunchRate'}
ZOMBIE_FIELDS = {'zombieValue': 'mZombieValue', 'startingLevel': 'mStartingLevel',
                 'firstAllowedWave': 'mFirstAllowedWave', 'pickWeight': 'mPickWeight'}
PROJ_FIELDS = {'damage': 'mDamage'}


def _strip(name, prefix):
    return name[len(prefix):] if name.startswith(prefix) else name


def _diff(rows, vanilla, key, prefix, fields):
    out = {}
    for row in rows:
        name = _strip(row[key], prefix)
        if name not in vanilla:
            raise KeyError(f'{name} not in vanilla dump')
        changed = {f: row[src] for f, src in fields.items() if row[src] != vanilla[name][f]}
        if changed:
            out[name] = changed
    return out


def build(study, vanilla):
    return {
        'plants': _diff([r for r in study['plants'] if r['mSeedType'] < 0x50], vanilla['plants'],
                        'seed_name', 'SEED_', PLANT_FIELDS),
        'zombies': _diff(study['zombies'], vanilla['zombies'], 'zombie_name', 'ZOMBIE_', ZOMBIE_FIELDS),
        'projectiles': _diff(study['projectiles'], vanilla['projectiles'], 'proj_name', 'PROJECTILE_', PROJ_FIELDS),
    }


def main():
    study = json.load(open(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STUDY))
    vanilla = json.load(open(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VANILLA))
    out = build(study, vanilla)
    for table, rows in out.items():
        with open(os.path.join(HERE, '..', 'data', f'{table}.json'), 'w') as f:
            json.dump(dict(sorted(rows.items())), f, indent='\t', sort_keys=True)
            f.write('\n')
        print(table, len(rows), 'changed rows')


if __name__ == '__main__':
    main()
