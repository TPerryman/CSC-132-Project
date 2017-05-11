###########################################################################################
# Name: Ammar Essajee, John Do, Jalen Senones
# Date: 3/31/2017
# Description: This program implements a GUI for the room adventure program.
###########################################################################################
from Tkinter import *
import RPi.GPIO as GPIO
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
switches = [23, 22, 17, 12]

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
                self._menu = ["Go", "Look", "Take", "Use"]

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
        def menu(self):
                return self._menu

        @menu.setter
        def menu(self, value):
                for i in range(len(value)):
                        self.menu[i] = value[i]

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

                s += "\n\n"

                for i in range(len(self.menu)):
                        s += self.menu[i] + "\n"

                return s

# the game class
# inherits from the Frame class of Tkinter
class Game(Frame):
        # the constructor
        def __init__(self, parent):
                # call the constructor in the superclass
                Frame.__init__(self, parent)
                self.parent = parent
                self.key = False

        # creates the rooms
        def createRooms(self):
                # r1 through r4 are the four rooms in the mansion
                # currentRoom is the room the player is currently on (which can be one of r1 through r4)
                
                # create the rooms and give them meaningful names and an image in the current directory
                r1 = Room("Room 1", "r1.gif")
                r2 = Room("Room 2", "r2.gif")
                r3 = Room("Room 3", "r3.gif")
                r4 = Room("Room 4", "r4.gif")
                
                # add exits to Room 1
                r1.addExit("east", r2)  # to the east of room 1 is room 2
                r1.addExit("south", r3)
                # add grabbables to room 1
                r1.addGrabbable("teddy_bear")
                r1.addGrabbable("easel")
                r1.addGrabbable("pillow")
                r1.addGrabbable("blanket")
                # add items to room 1 
                r1.addItem("bed", "It is really soft and no one is sleeping in it.\
Maybe you can take the blanket and pillow.")
                r1.addItem("couch", "Looks comfy and no one's sitting in it! Look at the teddy bear next to it!")
                r1.addItem("flower_pot", "There's so many colorful flowers!")
                        
                
                # add exits to room 2 
                r2.addExit("west", r1)
                r2.addExit("south", r4)
                # add items to room 2
                r2.addItem("chair", "Uh - Oh! Somebody is currently using the chair.")
                r2.addItem("chest of drawers", "Look! There's a soft-toy on the chest of drawers.")
                r2.addItem("table", "There's some coffee on the table!")
                r2.addGrabbable("coffee")
                
                # add exits to room 3
                r3.addExit("north", r1)
                r3.addExit("east", r4)
                # add grabbables to room 3
                r3.addGrabbable("book")
                r3.addGrabbable("video game")
                # add items to room 3
                r3.addItem("bookshelves", "They are full of books! Take one.")
                r3.addItem("computer", "Looks like nobody is using it")
                r3.addItem("desk", "There's a video game on the desk.")
                
                # add exits to room 4
                r4.addExit("north", r2)
                r4.addExit("west", r3)
                r4.addExit("south", None)        # DEATH!
                # add grabbables to room 4
                r4.addGrabbable("remote")
                # add items to room 4
                r4.addItem("television", "Its a T.V.! There seems to be a remote near by.")
                r4.addItem("rug", "The rug is really colorful!")
                
                # set room 1 as the current room at the beginning of the game
                Game.currentRoom = r1
                
                # initialize the player's inventory
                Game.inventory = []

        # sets up the GUI
        def setupGUI(self):
                print "Point 1"
                # organize the GUI
                self.pack(fill=BOTH, expand=1)
                
                # setup the player input at the bottom of the GUI
                # the widget is a Tkinter Entry
                # set its background to white and bind the return key to the 
                # function process in the class
                # push it to the bottom of the GUI and let it fill
                # horizontally
                # give it focus so the player doesn't have to click on it
                #Game.player_input = Entry(self, bg="white")
                #self.bind("<Return>", process)
                #Game.player_input.pack(side=BOTTOM, fill=X)
                #Game.player_input.focus()
                
                # setup the image to the left of the GUI
                # the widget is a Tkinter Label
                # don't let the image control the widget's size 
                img = None
                Game.image = Label(self, width=WIDTH / 2, image=img)
                Game.image.image = img
                Game.image.pack(side=LEFT, fill=Y)
                Game.image.pack_propagate(False)
                
                #setup the text to the right of the GUI
                # first, the frame in which the text will be placed
                text_frame = Frame(self, width=WIDTH / 2)
                # the widget is a Tkinter Text
                # disable it by default
                # don't let the widget control the frame's size
                Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
                Game.text.pack(fill=Y, expand=1)
                text_frame.pack(side=RIGHT, fill=Y)
                text_frame.pack_propagate(FALSE)
                print"point 2"

        # sets the current room image
        def setRoomImage(self):
                if (Game.currentRoom == None):
                        # if dead, set the skull image
                        Game.img = PhotoImage(file="skull2.gif")
                else:
                        # otherwise grab the image for the current Room
                        Game.img = PhotoImage(file=Game.currentRoom.image)
                        
                # display the image on the left of the GUI
                Game.image.config(image=Game.img)
                Game.image.image = Game.img
                print "point 3"

        # sets the status displayed on the right of the GUI
        def setStatus(self, status):
                # enable the text widget, clear it, set it, and disabled it 
                Game.text.config(state=NORMAL)
                Game.text.delete("1.0", END)
                if (Game.currentRoom == None):
                        #if dead, let the player know 
                        Game.text.insert(END, "You are dead. The only thing you can do now \
                        is quit.\n")
                else:
                        # otherwise, display the appropriate status
                        Game.text.insert(END, str(Game.currentRoom) +\
                                         "\nYou are carrying: " + str(Game.inventory) +\
                                         "\n\n" + status)
                Game.text.config(state = DISABLED)
                

        # plays the game

        def play(self):
                # add the rooms to the game
                self.createRooms()
                # configure the GUI
                self.setupGUI()
                # set the current room
                self.setRoomImage()
                # set the current status
                self.setStatus(" ")
                
                print "point 5"
                
        # processes the player's input
        def process(self):
                
                print "point 4"
                # grab the player's input from the input at the bottom of 
                # the GUI
                #action = Game.player_input.get()
                # set the user's input to lowercase to make it easier to 
                # compare the verb and noun to known values
                #action = action.lower()
                # set a default response
                response = "I don't understand. Try verb noun. Valid verbs \
                #are go, look, take, inspect, and play."

                ###
                print "Start of Process"
                ###
                
                # exit the game if the player wants to leave (supports quit,
                # exit, and bye)
               # if (action == "quit" or action == "exit" or action == "bye"\
              #          or action == "sionara!"):
               #         exit(0)
                        
                # if the player is dead if goes/went south from room 4
##                if (Game.currentRoom == None):
##                        # clear the player's input
##                        Game.player_input.delete(0, END)
##                        return
##                        
                # split the user input into words (words are separated by 
                # spaces) and store the words in a list
                #words = action.split()

                Game.menu = ["go", "look", "take"]
                pressed = False
                while(pressed == False):
                        for i in range(len(Game.menu)):
                                if(GPIO.input(switches[i]) == True):
                                        val = i
                                        print val
                                        if (val == 0):
                                                self.menu = ["north", "south", "east", "west"]
                                                self.setStatus(" ")
                                                self.setRoomImage()
                                                sleep(1)
                                                print "Go selected"
                                                for i in range(len(Game.menu)):
                                                        if (GPIO.input(switches[i]) == True):
                                                                print "Button recognized"
                                                                val = i
                                                                if (val == 0):
                                                                        if ("north" in Game.currentRoom.exits):
                                                                                Game.currentRoom = Game.currentRoom.exits["north"]
                                                                                response = "Room Changed"
                                                                        else:
                                                                                response = "invalid exit"
                                                                elif (val == 1):
                                                                        if ("south" in Game.currentRoom.exits):
                                                                                Game.currentRoom = Game.currentRoom.exits["south"]
                                                                                response = "Room changed"
                                                                                
                                                                        else:
                                                                                response = "invalid exit"
                                                                elif (val == 2):        
                                                                        if ("east" in Game.currentRoom.exits):
                                                                                Game.currentRoom = Game.currentRoom.exits["east"]
                                                                                response = "Room Changed"
                                                                        else:
                                                                                response = "invalid exit"
                                                                elif (val == 3):
                                                                        if ("west" in Game.currentRoom.exits):
                                                                                Game.currentRoom = Game.currentRoom.exits["west"]
                                                                        else:
                                                                                response = "invalid exit"

                                                                                        
                                                                         
                                                

##                # the game only understands two word inputs
##                if (len(words) == 2):
##                        # isolate the verb and noun
##                        verb = words[0]
##                        noun = words[1]
##
##                        # the verb is: go
##                        if (verb == "go"):
##                                # set a default response
##                                response = "Invalid exit."
##                                
##                                # check for valid exits in the current room
##                                if (noun in Game.currentRoom.exits):
##                                        # if one is found, change the current room to
##                                        # the one that is associated with the 
##                                        # specified exit
##                                        Game.currentRoom =\
##                                                Game.currentRoom.exits[noun]
##                                        # set the response (success)
##                                        response = "Room changed."
##
##                        # the verb is: look
##                        elif (verb == "look"):
##                                # set a default response
##                                response = "I don't see that item."
##
##                                # check for valid items in the current room
##                                if (noun in Game.currentRoom.items):
##                                        # if one is found, set the response to the item's description
##                                        response = Game.currentRoom.items[noun]
##
##                        elif (verb == "inspect"):
##                                # set a default response
##                                response = "I can't inspect this."
##
##                                #check for valid grabbable items in the current room
##                                for grabbable in Game.currentRoom.grabbables:
##                                        # a valid grabbable item is found
##                                        if (noun == grabbable):
##                                                response = "*inspects item*"
##
##                        elif (verb == "play"):
##                                # set a default response
##                                response = "I can't play with this."
##
##                                #check for valid grabbable items in the current room
##                                for grabbable in Game.currentRoom.grabbables:
##                                        # a valid grabbable item is found
##                                        if (noun == grabbable):
##                                                Game.inventory.append(grabbable)
##                                                Game.currentRoom.delGrabbable(grabbable)
##                                                response = "*begins to play with item.*"
##
##                        
##                        # the verb is: take
##                        elif (verb == "take"):
##                                # set a default response
##                                response = "I don't see that item."
##
##                                #check for valid grabbable items in the current room
##                                for grabbable in Game.currentRoom.grabbables:
##                                        # a valid grabbable item is found
##                                        if (noun == grabbable):
##                                                Game.inventory.append(grabbable)
##                                                Game.currentRoom.delGrabbable(grabbable)
##                                                response = "item grabbed."
##                                                break
##                        
##                                                        
##                        
                # display the reponse on the right of the GUI
                # display the room's image on the left of the GUI
                # clear the player's input
                self.setStatus(response)
                self.setRoomImage()
                print "End of Process"
                #Game.player_input.delete(0, END)                        
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

thread = threading.Thread(target = g.process)
thread.start()


print "here1"
# wait for the window to close
g.mainloop()

print "here2"



