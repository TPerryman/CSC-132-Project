###########################################################################################
# Name: Tyler Perryman, Ammar Essajee, Cade Gautreaux, Caleb Snook
# Date: 5/11/2017
# Description: This code was suppose to be a modified version of the room adventure
#              that implemented one of the puzzles that was meant to be in the final
#              version of the project. Once it proved to be working, it was intended
#              intended to be adjusted for the final version.
###########################################################################################

from Tkinter import *

# the room class
# note that this class is fully implemented with dictionaries as illustrated in the lesson "More on Data Structures"
class Room(object):
    # the constructor
    def __init__(self, name, image):
        # rooms have a name, an image (the name of a file), exits (e.g., south), exit locations
        # (e.g., to the south is room n), items (e.g., table), item descriptions (for each item),
        # and grabbables (things that can be taken into inventory)
        self.name = name
        self.image = image
        self.exits ={}
        self.items = {}
        self.grabbables = []

    # getters and setters for the instance variables
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def grabbables(self):
        return self._grabbables

    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value

    # adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    def addExit(self, exit, room):
        # append the exit and room to the appropriate dictionary
        self._exits[exit] = room

    # adds an item to the room
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made of wood)
    def addItem(self, item, desc):
        # append the item and description to the appropriate dictionary
        self._items[item] = desc

    # adds a grabbable item to the room
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)

    # removes a grabbable item from the room
    # the item is a string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)

    # returns a string description of the room
    def __str__(self):
        # first, the room name
        s = "You are in {}.\n".format(self.name)

        # next, the items in the room
        s += "You see: "
        for item in self.items.keys():
            s += item + " "
        s += "\n"

        # next, the exits from the room
        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "

        return s

# the game class
# inherits from the Frame class of Tkinter
class Game(Frame):
        # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)

    # creates the rooms
    def createRooms(self):
                # r1 through r4 are the four rooms in the mansion
                # currentRoom is the room the player is currently in (which
                # can be one of r1 through r4)

                # create the rooms and give them meaningful names and an
                # image in the current directory


#This creates the 27 rooms that make up the mansion game. Each room has a unique image to help add to the
#diversity of the game.
                r1 = Room("", "")                        
                
#The following code adds exits, grabbables, and collectible items to the rooms
                r1.addExit("", )
                r1.addGrabbable("green_pin")
                r1.addGrabbable("yellow_pin")
                r1.addGrabbable("blue_pin")
                r1.addGrabbable("red_pin")
                r1.addItem("clown_painting", "A typical portrait of a sad clown, but this one is missing his nose. Upon closer inspection, you notice that there is a small pin-sized hole where his nose should be.")
                r1.addItem("park_painting", "A group of people seem to be enjoying themselves in what would be a sunny park. There is a small pin-sized hole where the sun should be.")
                r1.additem("flower_painting", "It is a protrait of a flower. There is a section of the stem that has been replaced by a pin-sized hole.")
                r1.addItem("sailboat_painting", "It is a medium-sized painting of a small sailboat with a little amn on it, there is a pin-sized hole where is shirt should be.")




                
#############################################################################################################################################################################################
                
                # set room 1 as the current room at the beginning of the game
                Game.currentRoom = r1

                # initialize the player's inventory
                Game.inventory = []


    # sets up the GUI
    def setupGUI(self):
                # organize the GUI
                self.pack(fill=BOTH, expand=1)

                # setup the player input at the bottom of the GUI
                # the widget is a Tkinter Entry
                # set its background to white and bind the return key to the
                # function process in the class
                # push it to the bottom of the GUI and let it fill
                # horizontally
                # give it focus so the player doesn't have to click on it
                Game.player_input = Entry(self, bg="white")
                Game.player_input.bind("<Return>", self.process)
                Game.player_input.pack(side=BOTTOM, fill=X)
                Game.player_input.focus()

                # setup the image to the left of the GUI
                # the widget is a Tkinter Label
                # don't let the image control the widget's size
                img = None
                Game.image = Label(self, width=WIDTH / 2, image=img)
                Game.image.image = img
                Game.image.pack(side=LEFT, fill=Y)
                Game.image.pack_propagate(False)

                # setup the text to the right of the GUI
                # first, the frame in which the text will be placed
                text_frame = Frame(self, width=WIDTH / 2)
                # the widget is a Tkinter Text
                # disable it by default
                # don't let the widget control the frame's size
                Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
                Game.text.pack(fill=Y, expand=1)
                text_frame.pack(side=RIGHT, fill=Y)
                text_frame.pack_propagate(False)

                
    # sets the current room image
    def setRoomImage(self):
                if (Game.currentRoom == None):
                        # if dead, set the skull image
                        Game.img = PhotoImage(file="skull.gif")
                else:
                        # otherwise grab the image for the current room
                        Game.img = PhotoImage(file=Game.currentRoom.image)

                # display the image on the left of the GUI
                Game.image.config(image=Game.img)
                Game.image.image = Game.img
  

    # sets the status displayed on the right of the GUI
    def setStatus(self, status):
                # enable the text widget, clear it, set it, and disabled it
                Game.text.config(state=NORMAL)
                Game.text.delete("1.0", END)
                if (Game.currentRoom == None):
                        # if dead, let the player know
                        Game.text.insert(END, "You are dead. The only thing you can do now is   quit.\n")
                else:
                        # otherwise, display the appropriate status
                        Game.text.insert(END, str(Game.currentRoom) +\
                                         "\nYou are carrying: " + str(Game.inventory) +\
                                         "\n\n" + status)
                Game.text.config(state=DISABLED)                

    # plays the game
    def play(self):
                # add the rooms to the game
        self.createRooms()
        # configure the GUI
        self.setupGUI()
        # set the current room
        self.setRoomImage()
        # set the current status
        self.setStatus("")

    # processes the player's input
    def process(self, event):
                # grab the player's input from the input at the bottom of
                # the GUI
                action = Game.player_input.get()
                # set the user's input to lowercase to make it easier to
                # compare the verb and noun to known values
                action = action.lower()
                # set a default response
                response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"

                # exit the game if the player wants to leave (supports quit,
                # exit, and bye)
                if (action == "quit" or action == "exit" or action == "bye" or action == "sionara!"):
                        exit(0)

                # if the player is dead if goes/went south from room 4
                if (Game.currentRoom == None):
                        # clear the player's input
                        Game.player_input.delete(0, END)
                        return

                # split the user input into words (words are separated by
                # spaces) and store the words in a list
                words = action.split()

                # the game only understands two word inputs
                if (len(words) == 3):
                        # isolate the verb and noun
                        verb = words[0];
                        noun = words[1]
                        verb1 =  words[2];

                        # the verb is: go
                        if (verb == "go"):
                                # set a default response
                                response = "Invalid exit."

                                # check for valid exits in the current room
                                if (noun in Game.currentRoom.exits):
                                        # if one is found, change the current room to
                                        # the one that is associated with the
                                        # specified exit
                                        Game.currentRoom = Game.currentRoom.exits[noun]
                                # set the response (success)
                                response = "Room changed."
                        # the verb is: look
                        elif (verb == "look"):
                                # set a default response
                                response = "I don't see that item."

                                # check for valid items in the current room
                                if (noun in Game.currentRoom.items):
                                        # if one is found, set the response to the
                                        # item's description
                                        response = Game.currentRoom.items[noun]
                        # the verb is: take
                        elif (verb == "take"):
                                # set a default response
                                response = "I don't see that item."

                                # check for valid grabbable items in the current
                                # room
                                for grabbable in Game.currentRoom.grabbables:
                                        # a valid grabbable item is found
                                        if (noun == grabbable):
                                                # add the grabbable item to the player's
                                                # inventory
                                                Game.inventory.append(grabbable)
                                                # remove the grabbable item from the
                                                # room
                                                Game.currentRoom.delGrabbable(grabbable)
                                                # set the response (success)
                                                response = "Item grabbed."
                                                # no need to check any more grabbable
                                                # items
                                        elif (verb1 == "use"):
                                            delGrabbable(item)
                                            break

                # display the response on the right of the GUI
                # display the room's image on the left of the GUI
                # clear the player's input
                self.setStatus(response)
                self.setRoomImage()
                Game.player_input.delete(0, END)
##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Room Adventure")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()

