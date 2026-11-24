import random
from statistics import median
from sync.lww import LWWStore

def make_phone(name, max_skew, rng, truth, editors):
    skew = rng.uniform(-max_skew, max_skew)
    store = LWWStore()
    for i in range(30):
        key = f"record{rng.randrange(20)}"
        real_time = rng.uniform(0, 3600)
        value = f"{name}-edit{i}"
        store.write(key, value, real_time + skew, name)
        if key not in truth or real_time > truth[key][0]:
            truth[key] = (real_time, value)
        if key not in editors:
            editors[key] = set()
        editors[key].add(name)
    return store

def run_once(max_skew, seed):
    rng = random.Random(seed)
    truth = {}
    editors = {}
    phones = []
    for i in range(5):
        phones.append(make_phone(f"phone{i}", max_skew, rng, truth, editors))

    server = LWWStore()
    for phone in phones:
        server.merge(phone)

    contested = 0
    wrong = 0
    for key in truth:
        if len(editors[key]) >= 2:
            contested = contested + 1
            if truth[key][1] != server.entries[key].value:
                wrong = wrong + 1
    if contested == 0:
        return 0.0
    return wrong / contested

for skew in [0, 1, 10, 60, 300, 900, 3600]:
    rates = []
    for seed in range(30):
        rates.append(run_once(skew, seed))
    print("max clock error", skew, "s -> median wrong rate", median(rates))