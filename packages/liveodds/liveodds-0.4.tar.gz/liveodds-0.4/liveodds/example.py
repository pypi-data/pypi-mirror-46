#!/usr/bin/env python3

import liveodds


def main():

    # get list of todays meetings
    meetings = liveodds.list_courses()

    print(meetings, '\n')

    
    # list race times for each course
    for meet in meetings:
        print(meet)
        for race in liveodds.list_races(meet):
            print(race)
        print()

    
    # get Race objects for all races at Nottingham
    races = liveodds.course('nottingham')


    # liveodds.course() func return a dictionary
    print(type(races))


    # each key is a race time
    # each value is the corresponding Race object
    for key, val in races.items():
        print('Key:', key, ' Value:', val)

    print()

    
    # accessing the Race objects
    for race in races.values():
        print(race.info())

        print('Runners:')

        for horse in race.runners():
            print(f'{horse.number}. {horse.name} ({horse.jockey}) {horse.form}')

        print('\n')


    
    # accessing the odds

    race = liveodds.race(liveodds.list_races()[0])

    # returns dict where key is horse name, value is odds dict
    odds = race.odds()

    for horse in odds.values():
        for bookie in horse.values():
            print(bookie['bookie'], bookie['price'])


    
    # odds for individual horse

    race_time = liveodds.list_races()[0]
    race = liveodds.race(race_time)

    # runners() return a list of horse objects for that race
    for horse in race.runners():
        print()
        print(horse.name)

        # odds() return a dictionary of odds for the horse
        odds = horse.odds()

        # each key in the dictionary is a bookie
        # each value is a dictionary with 3 keys (bookie, price, time)
        # the name of the bookie, the price and the time the price was checked
        for bookie in odds.values():
            print(bookie['bookie'], bookie['price'], '@', bookie['time'])

    print()


    # display race odds in formatted table
    print(race.odds_table())


    # display odds for individual horse
    horse = liveodds.race(liveodds.list_races()[0]).runners()[0]

    print(horse.odds_table())


if __name__ == '__main__':
    main()
