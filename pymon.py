#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id :
@highest_level_attempted (P/C/D/HD):

- Reflection:
- Reference:
"""

import random


# you may use, extend and modify the following random generator
def generate_random_number(max_number=1):
    r = random.randint(0, max_number)
    return r


class Creature:
    def __init__(self, name="New Creature", description="", location=None):
        self.name = name
        self.description = description
        self.location = location

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location


class Pymon(Creature):
    def __init__(self, name="Player", description="", location=None, energy=3, speed=1):
        super().__init__(name=name, description=description, location=location)
        self.energy = energy
        self.speed = speed

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_location(self):
        return self.location

    def set_location(self, current_location):
        self.location = current_location

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = energy

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def move(self, direction=None):
        if self.location != None:
            if self.location.doors[direction] != None:
                self.location.doors[direction].add_creature(self)
                self.location.creatures.remove(self)
                self.set_location(self.location.doors[direction])
                return True
            else:
                return False
        else:
            return False

    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.set_location(loc)


class PymonCreature(Creature):
    def __init__(self, name="New Pymon", description="", location=None, speed=1):
        super().__init__(name, description, location)
        self.energy = 3
        self.speed = speed

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = energy

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def move(self, direction=None):
        if self.location != None:
            if self.location.doors[direction] != None:
                self.location.doors[direction].add_creature(self)
                self.location.creatures.remove(self)
                self.set_location(self.location.doors[direction])


class Item:
    def __init__(self, name="New Item", description="No description"):
        self.name = name
        self.description = description
        self.pickable = False
        self.consumable = False

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_pickable(self):
        return self.pickable

    def set_pickable(self, pickable):
        self.pickable = pickable

    def get_consumable(self):
        return self.consumable

    def set_consumable(self, consumable):
        self.consumable = consumable


class Location:
    def __init__(self, name="New room", w=None, n=None, e=None, s=None):
        self.name = name
        self.description = ""
        self.doors = {}
        self.doors["west"] = w
        self.doors["north"] = n
        self.doors["east"] = e
        self.doors["south"] = s
        self.creatures = []
        self.items = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.get_name() == item_name:
                self.items.remove(item)
                return True
        return False

    def connect_east(self, another_room):
        self.doors["east"] = another_room
        another_room.doors["west"] = self

    def connect_west(self, another_room):
        self.doors["west"] = another_room
        another_room.doors["east"] = self

    def connect_north(self, another_room):
        self.doors["north"] = another_room
        another_room.doors["south"] = self

    def connect_south(self, another_room):
        self.doors["south"] = another_room
        another_room.doors["north"] = self

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_doors(self):
        return self.doors

    def set_doors(self, doors):
        self.doors = doors

    def get_creatures(self):
        return self.creatures

    def set_creatures(self, creatures):
        self.creatures = creatures

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items


class Record:
    def __init__(self):
        self.locations = []
        self.creatures = []
        self.items = []

    def get_locations(self):
        return self.locations

    def set_locations(self, locations):
        self.locations = locations

    def get_creatures(self):
        return self.creatures

    def set_creatures(self, creatures):
        self.creatures = creatures

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    def import_location(self, imported_items=[]):
        # Import data from locations.csv
        import csv
        import os

        # Try to find the CSV file in data directory first, then sample_data
        csv_paths = [
            os.path.join(os.path.dirname(__file__), "data", "locations.csv"),
        ]

        locations_dict = {}  # To store locations by name for connecting

        for csv_path in csv_paths:
            if os.path.exists(csv_path):
                try:
                    with open(csv_path, "r", encoding="utf-8") as file:
                        csv_reader = csv.DictReader(file)
                        rows = list(csv_reader)  # Read all rows into memory

                        # First pass: create all locations
                        for row in rows:
                            name = row["name"].strip()
                            description = row["description"].strip()
                            location = Location(name)
                            location.set_description(description)

                            # Add items to location
                            items_names = (
                                []
                                if row["items"] == "None" or row["items"].strip() == ""
                                else row["items"].strip().split("-")
                            )
                            for item_name in items_names:
                                item_name = item_name.strip()
                                if item_name:
                                    # Find the item in the provided items list
                                    for item in imported_items:
                                        if item.get_name() == item_name:
                                            location.add_item(item)
                                            break
                            
                            # Add creatures to location
                            for creature in self.creatures:
                                if creature.get_location() is None:
                                    # Randomly assign creature to location
                                    if generate_random_number(len(rows) - 1) == rows.index(row):
                                        location.add_creature(creature)
                                        creature.set_location(location)

                            locations_dict[name] = location
                            self.locations.append(location)

                        # Second pass: connect locations
                        for row in rows:
                            name = row["name"].strip()
                            current_location = locations_dict[name]

                            # Connect directions (if not "None")
                            directions = ["west", "north", "east", "south"]
                            for direction in directions:
                                connected_name = row[direction].strip()
                                if connected_name and connected_name != "None":
                                    if connected_name in locations_dict:
                                        current_location.doors[direction] = (
                                            locations_dict[connected_name]
                                        )

                    return  # Successfully imported, exit function

                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")
                    continue

        # Fallback to original sample data if CSV import fails
        print("Could not find or read locations.csv, using fallback data")
        school = Location("school")
        car_park = Location("car park")
        self.locations.append(school)
        self.locations.append(car_park)
        school.connect_west(car_park)

    def import_creatures(self):
        # Import data from creatures.csv
        import csv
        import os

        # Try to find the CSV file in data directory first, then sample_data
        csv_paths = [
            os.path.join(os.path.dirname(__file__), "data", "creatures.csv"),
        ]

        for csv_path in csv_paths:
            if os.path.exists(csv_path):
                try:
                    with open(csv_path, "r", encoding="utf-8") as file:
                        csv_reader = csv.DictReader(file)

                        for row in csv_reader:
                            name = row["name"].strip()
                            description = row[
                                " description"
                            ].strip()  # Note the space in the CSV header
                            adoptable = row[" adoptable"].strip().lower() == "yes"
                            speed = int(row["speed"].strip())

                            # Create PymonCreature if adoptable, otherwise regular Creature
                            if adoptable:
                                creature = PymonCreature(name, description, None, speed)
                            else:
                                creature = Creature(name, description, None)

                            self.creatures.append(creature)

                            # Randomly assign creature to a location
                            if self.locations:
                                random_location = self.locations[
                                    generate_random_number(len(self.locations) - 1)
                                ]
                                random_location.add_creature(creature)
                                creature.set_location(random_location)

                    return  # Successfully imported, exit function

                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")
                    continue

        print("Could not find or read creatures.csv")

    def import_items(self):
        # Import data from items.csv
        import csv
        import os

        # Try to find the CSV file in data directory first, then sample_data
        csv_paths = [
            os.path.join(os.path.dirname(__file__), "data", "items.csv"),
        ]

        for csv_path in csv_paths:
            if os.path.exists(csv_path):
                try:
                    with open(csv_path, "r", encoding="utf-8") as file:
                        csv_reader = csv.DictReader(file)

                        for row in csv_reader:
                            name = row["name"].strip()
                            description = row["description"].strip()  # Note the space in CSV header
                            # Additional attributes that might be needed later
                            pickable = row["pickable"].strip().lower() == "yes"
                            consumable = row["consumable"].strip().lower() == "yes"

                            item = Item(name, description)
                            # Set additional attributes using setters
                            item.set_pickable(pickable)
                            item.set_consumable(consumable)

                            self.items.append(item)

                            # Randomly assign item to a location
                            if self.locations:
                                random_location = self.locations[
                                    generate_random_number(len(self.locations) - 1)
                                ]
                                random_location.add_item(item)

                    return  # Successfully imported, exit function

                except Exception as e:
                    print(f"Error reading {csv_path}: {e}")
                    continue

        print("Could not find or read items.csv")


class Operation:
    def __init__(self, locations=None, current_pymon=None):
        self.locations = locations if locations is not None else []
        self.current_pymon = (
            current_pymon if current_pymon is not None else Pymon("Kimimon")
        )
        self.inventory = []

    def handle_menu(self):
        while True:
            print("Please issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Exit the program")
            print("5) Pick up item")
            print("6) View inventory")
            input_command = input()
            if input_command == "1":
                self.inspect_pymon()
            elif input_command == "2":
                self.inspect_location()
            elif input_command == "3":
                self.move_pymon()
            elif input_command == "4":
                print("Exiting the program.")
                break
            elif input_command == "5":
                self.pick_up_item()
            elif input_command == "6":
                self.view_inventory()
            else:
                print("Invalid command. Please try again.")
            print()

    def get_locations(self):
        return self.locations

    def set_locations(self, locations):
        self.locations = locations

    def get_current_pymon(self):
        return self.current_pymon

    def set_current_pymon(self, current_pymon):
        self.current_pymon = current_pymon

    def setup(self):
        record = Record()

        # Import all data from CSV files
        record.import_items()
        record.import_creatures()
        record.import_location(record.get_items())

        # Add locations to the operation
        for location in record.get_locations():
            self.locations.append(location)

        # Spawn the player's Pymon at a random location
        if self.locations:
            a_random_number = generate_random_number(len(self.locations) - 1)
            spawned_loc = self.locations[a_random_number]
            self.current_pymon.spawn(spawned_loc)

    def display_setup(self):
        for location in self.locations:
            print(location.get_name() + " has the following creatures:")
            for creature in location.creatures:
                print(creature.get_name())

    # you may use this test run to help test methods during development
    def test_run(self):
        print(self.current_pymon.get_location().get_name())
        self.current_pymon.move("west")
        print(self.current_pymon.get_location().get_name())

    def start_game(self):
        print("Welcome to Pymon World\n")
        print(
            "It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n"
        )
        print("You started at ", self.current_pymon.get_location().get_name())
        self.handle_menu()

    def inspect_pymon(self):
        pymon = self.current_pymon
        print(
            f"Hi player, my name is {pymon.get_name()}, I am {pymon.get_description() if pymon.get_description() else 'just a regular Pymon'}."
        )
        print(f"My energy is {pymon.get_energy()}. What can I do to help you?")

    def inspect_location(self):
        location = self.current_pymon.get_location()
        if location:
            print(f"You are at {location.get_name()}, {location.get_description()}")
        else:
            print("Current Location: None")

    def move_pymon(self):
        direction = (
            input("Moving to which direction? (west/north/east/south):").strip().lower()
        )
        isSuccessful = self.current_pymon.move(direction)
        if not isSuccessful:
            print("You can't move in that direction.")

    def pick_up_item(self):
        location = self.current_pymon.get_location()
        if location:
            items = location.get_items()
            if items and len(items) > 0:
                print(
                    f"Items available to pick up: {', '.join(item.get_name() for item in items)}"
                )
            else:
                print("There are no items to pick up here.")
                return
            print("Picking what?")
            input_item_name = input().strip()
            for item in location.get_items():
                if item.get_name().lower() == input_item_name.lower():
                    if item.get_pickable():
                        self.inventory.append(item)
                        location.remove_item(item.get_name())
                        print(f"You picked up the {item.get_name()}.")
                    else:
                        print(f"The {item.get_name()} cannot be picked up.")
                    return

    def view_inventory(self):
        if self.inventory and len(self.inventory) > 0:
            print("You are carrying:")
            for item in self.inventory:
                print(f"- {item.get_name()}: {item.get_description()}")
        else:
            print("Your inventory is empty.")


if __name__ == "__main__":
    ops = Operation()
    ops.setup()
    # ops.display_setup()  # Uncomment to see the loaded data
    ops.start_game()
