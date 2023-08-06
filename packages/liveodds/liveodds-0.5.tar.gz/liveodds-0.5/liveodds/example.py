#!/usr/bin/env python3

import liveodds

race = liveodds.race(liveodds.list_races()[0])

for horse in race.odds().values():
    for bookie in horse.values():
        print(bookie['bookie'], bookie['price'])