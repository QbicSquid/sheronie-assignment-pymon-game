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


# Custom Exceptions
class InvalidDirectionException(Exception):
    """Exception thrown when selected direction does not contain any location"""
    pass

class InvalidInputFileFormat(Exception):
    """Exception thrown when CSV file has invalid content or incorrect format"""
    pass


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
        self.move_count = 0
        self.has_pogo_boost = False

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

    def get_move_count(self):
        return self.move_count

    def set_move_count(self, move_count):
        self.move_count = move_count

    def get_has_pogo_boost(self):
        return self.has_pogo_boost

    def set_has_pogo_boost(self, has_pogo_boost):
        self.has_pogo_boost = has_pogo_boost

    def move(self, direction=None):
        if self.location != None:
            if self.location.doors[direction] != None:
                self.location.doors[direction].add_creature(self)
                self.location.creatures.remove(self)
                self.set_location(self.location.doors[direction])
                
                # Increment move count and check energy depletion
                self.move_count += 1
                if self.move_count >= 2:
                    self.move_count = 0
                    current_energy = self.get_energy()
                    if current_energy > 0:
                        self.set_energy(current_energy - 1)
                        print(f"{self.get_name()}'s energy decreased to {self.get_energy()}")
                        
                        # Check if energy is depleted
                        if self.get_energy() <= 0:
                            print(f"{self.get_name()} has run out of energy and escaped into the wild!")
                            return "energy_depleted"
                
                return True
            else:
                return False
        else:
            return False

    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.set_location(loc)

    def use_item(self, item, inventory):
        """Use an item from inventory"""
        if item not in inventory:
            return "Item not in inventory"
            
        item_name = item.get_name().lower()
        
        # Handle edible items (like apple)
        if item.get_consumable():
            current_energy = self.get_energy()
            if current_energy < 3:
                self.set_energy(min(current_energy + 1, 3))
                inventory.remove(item)
                return f"{self.get_name()} ate the {item.get_name()} and gained energy! Energy: {self.get_energy()}"
            else:
                return f"{self.get_name()} is already at maximum energy (3)"
        
        # Handle pogo stick
        elif "pogo" in item_name:
            self.set_has_pogo_boost(True)
            return f"{self.get_name()} is now ready to use the pogo stick in the next race!"
        
        # Handle binocular  
        elif "binocular" in item_name:
            return "binocular_ready"  # Special return to indicate binocular usage
        
        else:
            return f"The {item.get_name()} cannot be used"


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
                        
                        # Validate CSV format
                        required_columns = ["name", "description", "west", "north", "east", "south"]
                        if not all(col in csv_reader.fieldnames for col in required_columns):
                            raise InvalidInputFileFormat(f"Missing required columns in {csv_path}")

                        # First pass: create all locations
                        for row in rows:
                            try:
                                name = row["name"].strip()
                                description = row["description"].strip()
                                
                                if not name:
                                    raise InvalidInputFileFormat("Location name cannot be empty")
                                    
                                location = Location(name)
                                location.set_description(description)

                                # Add items to location
                                items_names = (
                                    []
                                    if "items" not in row or row["items"] == "None" or row["items"].strip() == ""
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
                                
                            except KeyError as e:
                                raise InvalidInputFileFormat(f"Missing column {e} in CSV file")
                            except Exception as e:
                                raise InvalidInputFileFormat(f"Error processing location data: {e}")

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
                        
                        # Validate CSV format
                        required_columns = ["name", " description", " adoptable", "speed"]
                        if not all(col in csv_reader.fieldnames for col in required_columns):
                            raise InvalidInputFileFormat(f"Missing required columns in creatures.csv")

                        for row in csv_reader:
                            try:
                                name = row["name"].strip()
                                description = row[" description"].strip()  # Note the space in the CSV header
                                
                                if not name:
                                    raise InvalidInputFileFormat("Creature name cannot be empty")
                                
                                adoptable_str = row[" adoptable"].strip().lower()
                                if adoptable_str not in ["yes", "no"]:
                                    raise InvalidInputFileFormat("Adoptable field must be 'yes' or 'no'")
                                adoptable = adoptable_str == "yes"
                                
                                try:
                                    speed = int(row["speed"].strip())
                                    if speed < 0:
                                        raise InvalidInputFileFormat("Speed cannot be negative")
                                except ValueError:
                                    raise InvalidInputFileFormat("Speed must be a valid integer")

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
                                    
                            except KeyError as e:
                                raise InvalidInputFileFormat(f"Missing column {e} in creatures.csv")
                            except InvalidInputFileFormat:
                                raise  # Re-raise our custom exceptions
                            except Exception as e:
                                raise InvalidInputFileFormat(f"Error processing creature data: {e}")

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
            print("4) Pick an item")
            print("5) View inventory")
            print("6) Challenge a creature")
            print("7) Generate stats")
            print("8) Exit the program")
            input_command = input()
            if input_command == "1":
                self.inspect_pymon()
            elif input_command == "2":
                self.inspect_location()
            elif input_command == "3":
                result = self.move_pymon()
                if result == "game_over":
                    break
            elif input_command == "4":
                self.pick_up_item()
            elif input_command == "5":
                self.view_inventory()
            elif input_command == "6":
                self.challenge_creature()
            elif input_command == "7":
                self.generate_stats()
            elif input_command == "8":
                print("Exiting the program.")
                break
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
            
            # Show creatures in the location
            creatures = location.get_creatures()
            other_creatures = [c for c in creatures if c != self.current_pymon]
            if other_creatures:
                print("Other creatures here:")
                for creature in other_creatures:
                    creature_type = "Pymon" if isinstance(creature, PymonCreature) else "Creature"
                    print(f"- {creature.get_name()} ({creature_type})")
            else:
                print("No other creatures are here.")
                
            # Show items in the location
            items = location.get_items()
            if items:
                print("Items here:")
                for item in items:
                    print(f"- {item.get_name()}: {item.get_description()}")
            else:
                print("No items are here.")
        else:
            print("Current Location: None")

    def move_pymon(self):
        try:
            direction = (
                input("Moving to which direction? (west/north/east/south):").strip().lower()
            )
            
            # Check if direction is valid
            location = self.current_pymon.get_location()
            if direction not in ["west", "north", "east", "south"]:
                raise InvalidDirectionException("Invalid direction specified")
            
            if not location or location.doors[direction] is None:
                raise InvalidDirectionException(f"No location exists in the {direction} direction")
            
            result = self.current_pymon.move(direction)
            
            if result == "energy_depleted":
                # Move Pymon to random location
                if self.locations:
                    random_location = self.locations[generate_random_number(len(self.locations) - 1)]
                    self.current_pymon.spawn(random_location)
                    print(f"{self.current_pymon.get_name()} has been moved to {random_location.get_name()}")
                    
                    # Check if this is game over (only one Pymon)
                    print("GAME OVER - Your Pymon has escaped!")
                    return "game_over"
            elif not result:
                print("You can't move in that direction.")
            else:
                print(f"Moved to {self.current_pymon.get_location().get_name()}")
                
        except InvalidDirectionException as e:
            print(f"Error: {e}")
        
        return "continue"

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
            for i, item in enumerate(self.inventory, 1):
                print(f"{i}) {item.get_name()}: {item.get_description()}")
            
            print("\nWould you like to use an item? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                self.use_item_menu()
        else:
            print("Your inventory is empty.")

    def use_item_menu(self):
        if not self.inventory:
            print("No items to use.")
            return
            
        print("Select item to use:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}) {item.get_name()}")
        
        try:
            choice = int(input("Enter item number: ")) - 1
            if 0 <= choice < len(self.inventory):
                item = self.inventory[choice]
                result = self.current_pymon.use_item(item, self.inventory)
                
                if result == "binocular_ready":
                    self.use_binocular()
                else:
                    print(result)
                    
                    # Remove pogo stick after use (it breaks)
                    if "pogo" in item.get_name().lower() and self.current_pymon.get_has_pogo_boost():
                        # Don't remove yet - it will be removed after the next race
                        pass
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid number.")

    def use_binocular(self):
        print("Using binocular! Enter direction to inspect:")
        print("Options: current, west, north, east, south")
        direction = input().strip().lower()
        
        location = self.current_pymon.get_location()
        if not location:
            print("You are not in any location.")
            return
            
        if direction == "current":
            creatures = [c.get_name() for c in location.get_creatures() if c != self.current_pymon]
            items = [i.get_name() for i in location.get_items()]
            
            output = []
            if creatures:
                output.append(", ".join(creatures))
            if items:
                output.append(", ".join(items))
                
            # Check connected directions
            connections = []
            for dir_name, connected_loc in location.get_doors().items():
                if connected_loc:
                    connections.append(f"in the {dir_name} is {connected_loc.get_name()}")
            
            if connections:
                output.extend(connections)
            
            if output:
                print(f"Current location: {', '.join(output)}")
            else:
                print("Current location appears empty with no connections.")
                
        elif direction in ["west", "north", "east", "south"]:
            connected_location = location.doors.get(direction)
            if connected_location:
                creatures = [c.get_name() for c in connected_location.get_creatures()]
                items = [i.get_name() for i in connected_location.get_items()]
                
                output_parts = []
                if items:
                    output_parts.append(f"an edible {items[0]}" if items[0].lower() in ["apple"] else items[0])
                if creatures:
                    if len(creatures) == 1:
                        output_parts.append(f"another {creatures[0]}")
                    else:
                        output_parts.append(f"{len(creatures)} creatures")
                
                if output_parts:
                    print(f"In the {direction}, there seems to be {connected_location.get_name()} with {' and '.join(output_parts)} nearby")
                else:
                    print(f"In the {direction}, there seems to be {connected_location.get_name()} but it appears empty")
            else:
                print(f"This direction leads nowhere")
        else:
            print("Invalid direction. Use: current, west, north, east, south")

    def generate_stats(self):
        print("=== Game Statistics ===")
        print(f"Player Pymon: {self.current_pymon.get_name()}")
        print(f"Energy: {self.current_pymon.get_energy()}/3")
        print(f"Speed: {self.current_pymon.get_speed()}")
        print(f"Current Location: {self.current_pymon.get_location().get_name() if self.current_pymon.get_location() else 'None'}")
        print(f"Moves made: {self.current_pymon.get_move_count()}")
        print(f"Items in inventory: {len(self.inventory)}")
        
        if self.inventory:
            print("Inventory items:")
            for item in self.inventory:
                print(f"  - {item.get_name()}")
        
        print(f"Total locations discovered: {len(self.locations)}")
        
        # Count creatures and Pymons
        total_creatures = 0
        total_pymons = 0
        for location in self.locations:
            for creature in location.get_creatures():
                if creature != self.current_pymon:
                    total_creatures += 1
                    if isinstance(creature, PymonCreature):
                        total_pymons += 1
        
        print(f"Total creatures in world: {total_creatures}")
        print(f"Total Pymons in world: {total_pymons}")

    def challenge_creature(self):
        location = self.current_pymon.get_location()
        if not location:
            print("You are not in any location.")
            return
            
        creatures = location.get_creatures()
        if not creatures or len(creatures) <= 1:  # Only player's Pymon is present
            print("There are no other creatures here to challenge.")
            return
            
        # Display available creatures to challenge
        other_creatures = [c for c in creatures if c != self.current_pymon]
        print("Creatures available to challenge:")
        for i, creature in enumerate(other_creatures, 1):
            print(f"{i}) {creature.get_name()}")
            
        try:
            choice = input("Choose a creature to challenge (enter number): ").strip()
            creature_index = int(choice) - 1
            
            if creature_index < 0 or creature_index >= len(other_creatures):
                print("Invalid choice.")
                return
                
            target_creature = other_creatures[creature_index]
            
            # Check if it's a PymonCreature (adoptable Pymon)
            if isinstance(target_creature, PymonCreature):
                self.race_against_pymon(target_creature)
            else:
                # Humorous responses for non-Pymon creatures
                self.humorous_challenge_response(target_creature)
                
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    def race_against_pymon(self, opponent):
        print(f"\n{self.current_pymon.get_name()} challenges {opponent.get_name()} to a race!")
        print("The race begins!")
        
        # Get speeds
        player_speed = self.current_pymon.get_speed()
        opponent_speed = opponent.get_speed()
        
        print(f"{self.current_pymon.get_name()}'s speed: {player_speed}")
        print(f"{opponent.get_name()}'s speed: {opponent_speed}")
        
        # Add some randomness to make it more interesting
        player_roll = generate_random_number(10) + player_speed
        opponent_roll = generate_random_number(10) + opponent_speed
        
        # Apply pogo stick boost if available
        if self.current_pymon.get_has_pogo_boost():
            player_roll = player_roll * 2
            print(f"🚀 Pogo stick boost activated! {self.current_pymon.get_name()}'s performance doubled!")
            
            # Remove pogo stick from inventory (it breaks after use)
            for item in self.inventory:
                if "pogo" in item.get_name().lower():
                    self.inventory.remove(item)
                    print(f"💥 The pogo stick breaks and disappears from inventory!")
                    break
            
            self.current_pymon.set_has_pogo_boost(False)
        
        print(f"\n{self.current_pymon.get_name()} races with total performance: {player_roll}")
        print(f"{opponent.get_name()} races with total performance: {opponent_roll}")
        
        if player_roll > opponent_roll:
            print(f"\n🏆 {self.current_pymon.get_name()} wins the race!")
            print("Your Pymon gains confidence and energy!")
            # Boost player's energy as a reward
            current_energy = self.current_pymon.get_energy()
            self.current_pymon.set_energy(min(current_energy + 1, 3))  # Cap at 3
        elif player_roll < opponent_roll:
            print(f"\n😞 {opponent.get_name()} wins the race!")
            print("Your Pymon is tired from the effort.")
            # Reduce player's energy as consequence
            current_energy = self.current_pymon.get_energy()
            self.current_pymon.set_energy(max(current_energy - 1, 0))  # Don't go below 0
        else:
            print(f"\n🤝 It's a tie! Both Pymons performed equally well!")
            print("Both Pymons respect each other's abilities.")

    def humorous_challenge_response(self, creature):
        creature_name = creature.get_name().lower()
        
        # Predefined humorous responses based on creature types
        responses = {
            'sheep': f"The {creature.get_name()} just ignored you and continued grazing peacefully.",
            'chicken': f"The {creature.get_name()} just laughed at you with a loud 'cluck cluck!'",
            'tree': f"The {creature.get_name()} stands still, completely unimpressed by your challenge.",
            'rock': f"The {creature.get_name()} remains motionless, as rocks tend to do.",
            'cat': f"The {creature.get_name()} gives you a dismissive look and walks away with attitude.",
            'dog': f"The {creature.get_name()} wags its tail, thinking you want to play fetch instead.",
            'fish': f"The {creature.get_name()} just blows bubbles at you, clearly confused.",
        }
        
        # Check for specific creature names or use a generic response
        response_given = False
        for key, response in responses.items():
            if key in creature_name:
                print(f"\n{response}")
                response_given = True
                break
                
        if not response_given:
            # Generic humorous response for unknown creatures
            print(f"\nThe {creature.get_name()} looks at you with confusion and tilts its head.")
            print("It seems like it doesn't understand what a 'race' is!")


if __name__ == "__main__":
    ops = Operation()
    ops.setup()
    # ops.display_setup()  # Uncomment to see the loaded data
    ops.start_game()
