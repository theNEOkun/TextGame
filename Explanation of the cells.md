# Explanation of how the world cells work

## Different types of cells:

There are a couple of different types of cells.

RIM - is used to border the area.\
GROUND - Used for normal ground\
TUNNEL - Used for pathways from once map to another\
WALL - Used to represent the houses walls\
ROAD - As described

They are represented by their first letter and once can see under "mapping" what each cell is.

## Different types of information:

In every cell, there are different types of information attached to them. Not all cells have all information
and one can add information to one celltype without adding it to another.

### "Description":

Is used when standing in that cell.

### "Directions":

When standing in the cell describes what you see in each direction when typing "look [direction]" in the 
examples below map or key is switched to an item name, which has to be unique.

### "items":

Describes what items are in the cell you are standing in and information attached to it.

#### "desc":

Description of the item, comes up when typing "look at [item]", though that is yet to be implemented.

#### "pickup":

Can either be yes or no, and is used for if a person can pick up an item.

#### "hidden_info":

Hidden info is used for if the item is a key to something. So if the item is a key, then hidden info needs 
to match the key in the door.

#### "action":

Is at the moment not used, and might change in the future.

### "interactions":

Is where things like doors and chests are added and are used with "interact [interactable]", "open [interactable]" etc.
in the example below interactx is changed to something to interact with, ex door or chest.

#### "desc":

Is used for when typing "look at [interactable] and describes it.

####  "key":

Here is where a key might be needed. If "no" then no key is needed, else the "hidden_info" has to match this.

####  "action":

Here you specify what action needs to be done. Example if it's a door then open.

#### "happening"

This is slightly harder to explain. I am working on implementing an easier to use version, though at the moment you have to specify a couple of things.

If it's a door, you first describe the coordinates to where the door is, and then you write the direction to where that door is in that square. At
the moment it is better to use words for what you want to happen.


## Below here is a cell of RIM type:

    "(0, 3)": {
        "description": {
            "place": "How did you get here?"
        },
        "directions": {
            "north": "placeholder",
            "south": "You see open ground",
            "west": "You see a wall",
            "east": "You see open ground"
        },
        "interactions": {
            "interact1": "placeholder"
        },
        "neighbours": {
            "north": {
                "coord": [
                    -1,
                    3
                ],
                "walk": "no",
                "why": "there's nothing there",
                "tunnel": "no"
            },
            "south": {
                "coord": [
                    1,
                    3
                ],
                "walk": "yes",
                "why": "It's open ground",
                "tunnel": "no"
            },
            "west": {
                "coord": [
                    0,
                    2
                ],
                "walk": "no",
                "why": "it's a wall",
                "tunnel": "no"
            },
            "east": {
                "coord": [
                    0,
                    4
                ],
                "walk": "yes",
                "why": "It's open ground",
                "tunnel": "no"
            }
        },
        "mapping": "M"
    },
	
## Below here is a cell of "GROUND" type

    "(0, 4)": {
        "description": {
            "place": "You are in a cave"
        },
        "directions": {
            "north": "You see a wall",
            "south": "You see open ground",
            "west": "You see a wall",
            "east": "You see a wall"
        },
        "items": {
            "map": {
                "desc": "map",
                "pickup": "yes",
                "hidden_info": "placeholder",
                "action": "placeholder"
            },
            "key": {
                "desc": "key with a blue band around it",
                "pickup": "yes",
                "hidden_info": "blue_key",
                "action": "placeholder"
            },
            "item3": {
                "desc": "placeholder",
                "pickup": "no",
                "hidden_info": "placeholder",
                "action": "placeholder"
            }
        },
        "interactions": {
            "interact1": {
                "desc": "placeholder",
                "key": "no",
                "action": "placeholder",
                "happening": "placeholder"
            },
            "interact2": {
                "desc": "placeholder",
                "key": "no",
                "action": "placeholder",
                "happening": "placeholder"
            },
            "interact3": {
                "desc": "placeholder",
                "key": "no",
                "action": "placeholder",
                "happening": "placeholder"
            }
        },
        "neighbours": {
            "north": {
                "coord": [
                    -1,
                    4
                ],
                "walk": "no",
                "why": "there's nothing there",
                "tunnel": "no"
            },
            "south": {
                "coord": [
                    1,
                    4
                ],
                "walk": "yes",
                "why": "It's open ground",
                "tunnel": "no"
            },
            "west": {
                "coord": [
                    0,
                    3
                ],
                "walk": "no",
                "why": "it's a wall",
                "tunnel": "no"
            },
            "east": {
                "coord": [
                    0,
                    5
                ],
                "walk": "no",
                "why": "it's a wall",
                "tunnel": "no"
            }
        },
        "key_needed": "no",
        "mapping": "R"
    },
	
