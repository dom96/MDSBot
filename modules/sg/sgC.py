#!/usr/bin/env python
"""
Created on 05/05/10 20:21:32
By Dominik Picheta
"""

# DATA
# races
OPRAN_RACE = 0
ELDERS_RACE = 1
LOK_RACE = 2

# atmosphere
OXYGEN_ATMOSPHERE = 0
CARBON_ATMOSPHERE = 1
NITROGEN_ATMOSPHERE = 2

# queue types
building_type = 0
defense_type = 1
ship_type = 2

# Buildings
TITANIUM_MINE = 0
GALLIUM_MINE = 1
HYDROGEN_SYNTHESIZER = 2
# TODO: Add more buildings..

import time, thread

class player():
    def __init__(self, nick, empire):
        self.nick = nick
        self.empire = empire

        self.running = True

class empire():
    def __init__(self, name, race):
        self.name = name
        self.race = race

        plnt = planet("Homeland", OXYGEN_ATMOSPHERE)
        self.planets = [plnt]

        self.player = None

    def start(self):
        thread.start_new(lambda x: self.work_queue(), (None,))
        thread.start_new(lambda x: self.work_resources(), (None,))

    def work_queue(self):
        # Check if any queue item finished.
        while self.player.running:
            for p in self.planets:
                for item in p.queue:
                    if item.timestamp < time.time():
                        thread.start_new(item.func, item.args)
                        p.queue.remove(item)
            time.sleep(1)     

    def work_resources(self):
        # Collect resources.
        while self.player.running:
            for p in self.planets:
                # Titanium
                # LVL * 0.5
                titaniumMine = p.get_building(TITANIUM_MINE)
                if titaniumMine != None:
                    p.titanium += titaniumMine.level * 0.5

                # Gallium mine
                # lvl * 0.4
                galliumMine = p.get_building(GALLIUM_MINE)
                if galliumMine != None:
                    p.gallium += galliumMine.level * 0.4

                # Hydrogen synthesizer
                # lvl * 0.25
                hydrogenSynth = p.get_building(HYDROGEN_SYNTHESIZER)
                if hydrogenSynth != None:
                    p.hydrogen += hydrogenSynth.level * 0.25

                time.sleep(1)


class planet():
    def __init__(self, name, atmosphere):
        self.name = name
        self.atmosphere = atmosphere

        self.ships = [] # Ships which are on the planet.
        self.buildings = [] # Buildings built on the planet.
        self.defenses = []

        self.titanium = 1000 # i.e metal
        self.gallium = 500 # gallium crystals
        self.hydrogen = 100 # Deuterium is actually hydrogen(h2 or heavy hydrogen)
        self.energy = 20

        # I think there should be a building which finds planets.
        # Telescope!!! :P

        self.queue = []

    def build_building(self, buildingID):
        if self.queue_has_building(): return "Cannot build, building queue is full."

        bldng = self.get_building(buildingID)
        if bldng != None:
            # Level up the building, instead of building another one.
            return bldng.queue_add_level()

        newBuilding = building(buildingID, self)

        titanium, gallium, hydrogen = calculate_build_resources(newBuilding)
        if self.titanium < titanium: return "Cannot build, not enough titanium. You need " + str(titanium)
        if self.gallium < gallium: return "Cannot build, not enough gallium. You need " + str(gallium)
        if self.hydrogen < hydrogen: return "Cannot build, not enough hydrogen. You need " + str(hydrogen)
        self.titanium -= titanium
        self.gallium -= gallium
        self.hydrogen -= hydrogen    

        timestamp = calculate_build_time(newBuilding)

        queue = queueItem(timestamp, self.finalise_building, (newBuilding, ), newBuilding)
        self.queue.append(queue)

        return True

    def finalise_building(self, bldng):
        fBldng = self.get_building(bldng.buildingID)
        if fBldng != None:
            fBldng.add_level()
        else:
            self.buildings.append(bldng)

    def get_building(self, buildingID):
        for i in self.buildings:
            if int(i.buildingID) == int(buildingID):
                return i

        return None

    def queue_has_building(self):
        for i in self.queue:
            if i.item.__class__ == building:
                return True
        return False

class building():
    def __init__(self, buildingID, planet):
        self.buildingID = buildingID
        self.level = 1
        self.planet = planet

    def add_level(self):
        self.level += 1

    def queue_add_level(self):
        titanium, gallium, hydrogen = calculate_build_resources(self)
        if self.planet.titanium < titanium: return "Cannot build, not enough titanium. You need " + str(titanium)
        if self.planet.gallium < gallium: return "Cannot build, not enough gallium. You need " + str(gallium)
        if self.planet.hydrogen < hydrogen: return "Cannot build, not enough hydrogen. You need " + str(hydrogen)
        self.planet.titanium -= titanium
        self.planet.gallium -= gallium
        self.planet.hydrogen -= hydrogen

        timestamp = calculate_build_time(self)
        queue = queueItem(timestamp, self.planet.finalise_building, (self, ), self)
        self.planet.queue.append(queue)
        return True

class queueItem():
    def __init__(self, timestamp, func, args, item):
        self.item = item
        self.func = func # Function to be called when this finishes.
        self.args = args # Arguments to pass to that function
        self.timestamp = timestamp # when this is suppose to complete

def calculate_build_time(item):
    timestamp = 0
    import time
    # Calculate how much time this takes to complete
    if item.buildingID == TITANIUM_MINE:
        # LVL * 600000
        # 2 * 600000 = 20 minutes
        # 16 lvl = 2 hours and 40 minutes
        # i will need to of course add some buildings which decrease build time.
        timestamp = time.time() + 12 #(item.level * 600)
    elif item.buildingID == GALLIUM_MINE:
        # LVL * 900000
        timestamp = time.time() + (item.level * 900)
    elif item.buildingID == HYDROGEN_SYNTHESIZER:
        # LVL * 1200000
        timestamp = time.time() + (item.level * 1200)

    return timestamp

def calculate_build_resources(item):

    titanium, gallium, hydrogen = 0, 0, 0
    # Calculate how much resources each building needs to be built.
    if item.buildingID == TITANIUM_MINE:
        # Titanium = lvl * 350
        # Gallium = lvl * 200
        # Hydrogen = lvl * 30
        titanium = item.level * 350
        gallium = item.level * 200
        hydrogen = item.level * 30
    if item.buildingID == GALLIUM_MINE:
        # Titanium = lvl * 360
        # gallium = lvl * 295
        # Hydrogen = lvl * 25
        titanium = item.level * 360
        gallium = item.level * 295
        hydrogen = item.level * 25
    if item.buildingID == HYDROGEN_SYNTHESIZER:
        # Titanium = lvl * 250
        # gallium = lvl * 350
        # Hydrogen = lvl * 35
        titanium = item.level * 250
        gallium = item.level * 350
        hydrogen = item.level * 35

    return [titanium, gallium, hydrogen]


def get_building_name(buildingID):
    if buildingID == TITANIUM_MINE:
        return "Titanium Mine"
    elif buildingID == GALLIUM_MINE:
        return "Gallium Mine"
    elif buildingID == HYDROGEN_SYNTHESIZER:
        return "Hydrogen Synthesizer"






