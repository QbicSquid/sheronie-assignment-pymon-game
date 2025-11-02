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


#you may use, extend and modify the following random generator
def generate_random_number(max_number = 1):
    r = random.randint(0,max_number)
    return r 


class Pymon:
    def __init__(self, name = "The player"):
        self.name = name
        self.current_location = None
    
    def move(self, direction = None):
        if self.current_location != None:
            if self.current_location.doors[direction] != None:
                self.current_location.doors[direction].add_creature(self)  
                self.current_location.creatures.remove(self)
            else:
                print("no access to " + direction)
                
    def spawn(self, loc):
        if loc != None:
            loc.add_creature(self)
            self.current_location = loc
            
    def get_location(self):
        return self.current_location
            
class Location:
    def __init__(self, name = "New room", w = None, n = None , e = None, s = None):
        self.name = name
        self.doors = {}
        self.doors["west"] = w
        self.doors["north"] = n
        self.doors["east"] = e
        self.doors["south"] = s
        self.creatures = []
        self.items = []
        
    def add_creature(self, creature):
        pass
        #please implement this method to by simply appending a creature to self.creatures list.
        
    def add_item(self, item):
        pass
        #please implement this method to by simply appending an item to self.items list.
        
    def connect_east(self, another_room):
        self.doors["east"] = another_room 
        another_room.doors["west"]  = self;
        
    def connect_west(self, another_room):
        self.doors["west"] = another_room 
        another_room.doors["east"]  = self;
    
    def connect_north(self, another_room):
        self.doors["north"] = another_room 
        another_room.doors["south"]  = self;
        
    def connect_south(self, another_room):
        self.doors["south"] = another_room 
        another_room.doors["north"]  = self;
        
    def get_name(self):
        return self.name
        
class Record:
    def __init__(self):
        self.locations = []
        #please implement constructor

    def import_location(self):
        #please import data from locations.csv
        #here are sample data to start with
        school = Location("school")
        car_park = Location("car park")
        self.locations.append(school)
        self.locations.append(car_park)
        
        school.connect_west(car_park)
        
    def get_locations(self):
        return self.locations
        
    def import_creatures(self):
        pass #please import data from creatures.csv

    def import_items(self):
        pass #please import data from items.csv
    
class Operation:
    
    def handle_menu(self):
        print("Please issue a command to your Pymon:")
        print("1) Inspect Pymon")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Exit the program")
        
    
    def __init__(self):
        self.locations = []
        self.current_pymon = Pymon("Kimimon")
      
    def setup(self):
        record = Record()

        record.import_location()
        for location in record.get_locations():
            self.locations.append(location)

        a_random_number = generate_random_number(len(self.locations)-1)
        
        spawned_loc = self.locations[a_random_number]

        self.current_pymon.spawn(spawned_loc)

    def display_setup(self):
        for location in self.locations:
            print(location.name + " has the following creatures:")
            for creature in location.creatures:
                print(creature.name)

    #you may use this test run to help test methods during development
    def test_run(self):
        print(self.current_pymon.get_location().get_name())
        self.current_pymon.move("west")
        print(self.current_pymon.get_location().get_name())
        
    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.current_pymon.get_location().get_name())
        self.handle_menu()

if __name__ == '__main__':
    ops = Operation()
    ops.setup()
    #ops.display_setup()
    ops.start_game()