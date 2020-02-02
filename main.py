#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'zork.json'
item_file = 'items.json'
inventory = [""]
points = 0
moves = 0

# Load the contents of the files into the game and items dictionaries. You can largely ignore this
# Sorry it's messy, I'm trying to account for any potential craziness with the file location
def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)




def check_inventory(item):
    for i in inventory:
        if i == item:
            return True
        return False


def render (game,items,current,moves,points):
    c = game [current]
    print ("\n\n{} Moves\t{} Points".format(moves,points))
    print("\n\nYou are at the " + c["name"])
    print(c["desc"])

    #display any items
    for i in c ["items"]:
        if not check_inventory(i("item")):
            print(i["desc"])


def get_input():
    response = input ("What would you like to do?")
    response = response.upper().strip()
    return response




def update(game,items,current,response):
    if response == "INVENTORY":
        print ("You are carrying:")
        if not len(inventory) == 0:
            print ("Nothing")
        else:
            for i in inventory:
                print(i.lower())
        return current
    
    c = game [current]
    for e in c["exits"]:
        if response == e["exit"]:
            moves += 1
            return e["target"]
    
    for i in c ["items"]:
        if response == "GET" + i["item"] and not check_inventory (i["item"]):
            print (i["take"])
            inventory.append(i["item"])
            return current
     
    return current




# The main function for the game
def main():
    current = 'WHOUS'  # The starting location
    end_game = ['END']  # Any of the end-game locations

    (game,items) = load_files()

    
    
    while True:
        render(game,items,current)
        response = get_input()
        
        if response == "QUIT":
            break

        current = update (game,items,current,response)
        
    print("Thanks for playing!")
    print ("You scored {} points in {} moves".format(points,moves))
# run the main function
if __name__ == '__main__':
	main()