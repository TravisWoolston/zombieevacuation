import random
from playsound import playsound
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def ZombieTrigger(room):
    room.zombies += 1
    print(bcolors.FAIL + f"A zombie enters {room.name}" + bcolors.ENDC)
class Room:
    def __init__(self, name, item, choices):
        self.name = name
        self.item = item
        self.choices = choices
        self.zombies = 0
        self.trigger = ZombieTrigger

Attic = Room("Attic", "Gun", {"S": "Bedroom"})
Bedroom = Room("Bedroom", "Baseball Bat", {"N": "Attic", "E": "Bathroom", "S": "Living Room"})
Bathroom = Room("Bathroom", "First Aid", {"W": "Bedroom", "S": "Kitchen"})
Basement = Room("Basement", "BasementAmmo", {"E": "Living Room"})
LivingRoom = Room("Living Room", "Dog", {"N": "Bedroom", "E": "Kitchen", "W": "Basement", "S": "Driveway"})
Kitchen = Room("Kitchen", "Car Keys", {"W": "Living Room", "N": "Bathroom"})
Driveway = Room("Driveway", "Car",{"N": "Living Room", "S": "Library"})
Library = Room("Library", "Evacuate", {})
Library.zombies = 30
CarAccident = Room("CarAccident", "InjuredPassenger", {"E": "SavePassenger"})
gameManager = {
    "health": 100,
    "ammo": 0,
    "actions": 5,
    "currentRoom": Bedroom,
    "dogInjured": False,
    "hasDog": False,
    "rescueCalled": False,
    "rescueTimer": 10,
    "gameOver": True,
    "win": True,
    "dogDied": False,
    "items": ["Cell", "Baseball Bat"],
    "rooms": {"Attic": Attic, "Bedroom": Bedroom, "Bathroom": Bathroom, "Basement": Basement, "LivingRoom": LivingRoom,
              "Kitchen": Kitchen, "Driveway": Driveway, "CarAccident": CarAccident, "Library": Library}
}
def RandomZombie(gameManager):
    spawn_chance = gameManager["actions"] * 2
    if spawn_chance > 50:
        spawn_chance = 50
    i = 0
    for room in gameManager["rooms"]:
        random_num = random.random() * 100
        i += 1
        if i > 6:
            break
        if random_num < spawn_chance:
            gameManager["rooms"][room].trigger(gameManager["rooms"][room])
def Combat(gameManager):
    hitChance = 90 if gameManager["ammo"] > 0 else 55
    injuryChance = 5 if gameManager["ammo"] > 0 else 40
    injuryNum = random.random() * 100
    hit = False
    injured = False
    if gameManager["ammo"] > 0 and "Gun" in gameManager["items"]:
        print("You fire at the zombie!")
        PlaySound("shoot")
    else:
        print(bcolors.WARNING + "You strike with your bat!" + bcolors.ENDC)
        playsound('./Sounds/baseballhit.wav')
    if (random.random() * 100) < hitChance:
        print(bcolors.OKGREEN + "Zombie down!" + bcolors.ENDC)
        gameManager["currentRoom"].zombies -= 1
        if gameManager["ammo"] > 0:
            gameManager["ammo"] -= 1
        hit = True
    else:
        print(bcolors.FAIL + "You missed!" + bcolors.ENDC)
        if gameManager["ammo"] > 0:
            gameManager["ammo"] -= 1
        injuryChance += 50
        print("+%50 injury chance")
    if injuryNum < injuryChance and gameManager["currentRoom"].zombies > 0:
        gameManager["health"] -= 15
        print("The zombie bit you! That hurt!")
        PlaySound("hit")
    elif gameManager["currentRoom"].zombies > 0:
        print(bcolors.OKGREEN + "You dodged a zombie Attack!" + bcolors.ENDC)
    return hit




def EnterRoom(gameManager, room_name):
    room_name = room_name.replace(" ", "")
    combatSuccess = True
    if room_name == "Driveway":
        room_name = "Library"
    if gameManager["currentRoom"].zombies > 0:
        damage = 15 * gameManager["currentRoom"].zombies
        print(bcolors.FAIL + f"A zombie strikes you for {damage} damage!" + bcolors.ENDC)
        PlaySound("hit")
        gameManager["health"] -= damage
    if combatSuccess:
        if gameManager["rooms"][room_name].name == "Driveway" and "Car Keys" not in gameManager["items"]:
            print(bcolors.FAIL + "I need my Car Keys." + bcolors.ENDC)
            EnterRoom(gameManager, LivingRoom)
            return
        if gameManager["rooms"][room_name] == "SavePassenger":
            gameManager["currentRoom"] = Library
            print(gameManager["currentRoom"].name)
        else:
            gameManager["currentRoom"] = gameManager["rooms"][room_name]
            print(f"{gameManager['currentRoom'].name} ({gameManager['currentRoom'].item})")
    if gameManager["currentRoom"].name == "Basement" and "BasementAmmo" not in gameManager["items"]:
        gameManager["items"].append("BasementAmmo")
        gameManager["ammo"] += 10
        print(bcolors.OKGREEN + "You found 10 bullets!" + bcolors.ENDC)
        playsound('./Sounds/reload.mp3')
    if gameManager["currentRoom"].name == "Attic" and "AtticAmmo" not in gameManager["items"]:
        gameManager["ammo"] += 5
        print(bcolors.OKGREEN + "You found 5 bullets!" + bcolors.ENDC)
        playsound('./Sounds/reload.mp3')

    AddToInventory(gameManager)

def PrintChoices(gameManager):
    hitChance = 90 if "Gun" in gameManager["items"] and gameManager["ammo"] > 0 else 55
    injuryChance = 5 if "Gun" in gameManager["items"] and gameManager["ammo"] > 0 else 40
    itemBlacklist = ["Library", "Driveway"]
    current_room = gameManager["currentRoom"]
    if current_room.zombies > 0:
        print(f"F - Attack Zombie(Use gun or melee weapon). Chance to hit: %{hitChance} Injury: %{injuryChance}")
    for direction, room_name in current_room.choices.items():
        room_str = ""
        if gameManager['rooms'][room_name.replace(' ', '')].name in itemBlacklist:
            if gameManager['rooms'][room_name.replace(' ', '')].name == "Driveway":
                room_str = f"{direction} - {room_name} (Drive to Library)"
        elif gameManager['rooms'][room_name.replace(' ', '')].item in gameManager["items"]:
            room_str = f"{direction} - {room_name}"
        else:
            room_str = f"{direction} - {room_name} (Item: {gameManager['rooms'][room_name.replace(' ', '')].item})"
        if current_room.zombies > 0:
            room_str += bcolors.FAIL + "(You will be attacked)" + bcolors.ENDC
        print(room_str)

def AddToInventory(gameManager, ammo = False):
    item = gameManager["currentRoom"].item
    if item not in gameManager["items"]:
        gameManager["items"].append(item)
        if gameManager["currentRoom"].name != "Library":
          print(bcolors.OKGREEN + f"{item} added to inventory!" + bcolors.ENDC)
def InjureDog():
    if "Dog" not in gameManager["items"]:
        LivingRoom.trigger(LivingRoom)
        gameManager["dogInjured"] = True
        print(bcolors.FAIL + "Your dog yelps from the living room! It was injured!" + bcolors.ENDC)
        playsound("./Sounds/dogyelp.wav")

def PlaySound(sound):
    if sound == "zombie":
        random_int = random.randint(1, 3)
        sound_str = f'./ZombieSounds/say{random_int}.wav'
        playsound(sound_str)
    if sound == "shoot":
        playsound('./GunSounds/gunshot.wav')
    if sound == "hit":
        random_int = random.randint(1, 3)
        sound_str = f'./HitSounds/hit{random_int}.wav'
        playsound(sound_str)
def UponEntry(gameManager):
    if not gameManager["rescueCalled"] and gameManager["currentRoom"].name == "Library":
        gameManager["rescueCalled"] = True
        playsound('./Sounds/ignition.mp3')
        print(
            "You enter the Library. There are remains of unfortunate people who didn't make it, and shattered windows. \nYou call 911 with %1 battery remaining on your phone. \nA voice pierces through the line. 'What's your location?' \nRelieved, you give them your location. \n'Hold tight! We are on our way!' \nYour relief is short lived as another window breaks behind you! The horde has arrived!")
    if gameManager["currentRoom"].zombies > 0:
        print(bcolors.FAIL + f"There are {gameManager['currentRoom'].zombies} zombies in this room!" + bcolors.ENDC)
        PlaySound("zombie")
    gameManager["actions"] += 1
    if gameManager["actions"] == 8 and gameManager["hasDog"] == False:
        InjureDog()
    elif gameManager["rescueCalled"]:
        Library.zombies += 3
        gameManager["rescueTimer"] -= 1
    status_str = f"Health: {gameManager['health']} Ammo: {gameManager['ammo']} Horde Aggression: %{gameManager['actions'] * 2}"
    if gameManager["rescueCalled"]:
        turnsRemaining = bcolors.OKBLUE + f" Turns remaining: {gameManager['rescueTimer']}" + bcolors.ENDC
        status_str += turnsRemaining
    print(status_str)
    PrintChoices(gameManager)
def Escape(gameManager):
    print("You enter the helicopter. You made it!")
    if "Dog" in gameManager["items"]:
        print("A soldier inspects your dog for injuries:")
        if gameManager["dogInjured"]:
            print(bcolors.FAIL + "'Your dog has a flesh wound!' one of the soldiers abruptly shouts before pushing it out of the helicopter. \nTears stream down your face as your dog is torn apart by the horde." + bcolors.ENDC)
        else:
            print("Dog is clear!")
    else:
        print("You wish your dog was here.")
    gameManager["win"] = False
def BeginGame(gameManager):
    openingPrompt = "You awaken in the middle of the night to a blaring alert on your phone. It reads; \n“Sudden unexplained pandemic. Infected humans become hostile zombies. This is NOT a joke! Your evacuation location is: 655 East 900 south. \nHead there immediately, arm yourself if possible.” \nYour hearts drops and you can’t begin to process what you’re reading when your dog starts barking at something from the living room."
    print(bcolors.OKCYAN + openingPrompt + bcolors.ENDC)
    playsound('./Sounds/alert.wav')
    playsound('./Sounds/dogbark.wav')
    print(bcolors.OKGREEN + "Baseball Bat added to inventory!" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Cell Phone added to inventory!" + bcolors.ENDC)
    while gameManager["gameOver"] and gameManager["win"]:
        if gameManager["health"] <= 0:
            if "Dog" in gameManager["items"] and not gameManager["dogDied"]:
                print(bcolors.FAIL + "Your dog sacrificed himself!" + bcolors.ENDC)
                playsound('./Sounds/dogyelp.wav')
                gameManager["dogInjured"] = True
                gameManager["health"] = 20
                gameManager["dogDied"] = True
                gameManager["items"].remove("Dog")
            else:
                gameManager["gameOver"] = False
                break

        RandomZombie(gameManager)
        UponEntry(gameManager)
        if gameManager["rescueTimer"] <= 0:
            print(
                "A helicopter with armed soldiers descends from the sky, raining down bullets on the relentless horde.")
            playsound('./Sounds/helicopter.wav')
            print(bcolors.OKGREEN + "G - Escape!" + bcolors.ENDC)
        if "First Aid" in gameManager["items"]:
            print("H - Use First Aid")

        userInput = input().upper()
        if userInput == "S" and gameManager["currentRoom"].name == "Living Room" and "Car Keys" not in gameManager["items"]:
            print("I need my car keys.")
            continue
        if userInput == "G" and gameManager["rescueTimer"] <= 0:
            Escape(gameManager)
        if userInput == "A":
                print(gameManager["actions"])
        if userInput == "F":
            Combat(gameManager)
        if userInput == "H" and "First Aid" in gameManager["items"]:
            gameManager["items"].remove("First Aid")
            gameManager["health"] = 100
        if userInput not in gameManager["currentRoom"].choices:
            continue
        EnterRoom(gameManager, gameManager["currentRoom"].choices[userInput])

BeginGame(gameManager)
if not gameManager["gameOver"]:
    print(bcolors.FAIL + "Game Over!" + bcolors.ENDC)
    playsound("./Sounds/flatline.wav")
elif not gameManager["win"]:
    print("You won!!")
print("Thanks for playing!")
print("Play again? Y/N")
response = input()
if response.upper() == "Y":
    gameManager = {
    "health": 100,
    "ammo": 0,
    "actions": 5,
    "currentRoom": Bedroom,
    "dogInjured": False,
    "hasDog": False,
    "rescueCalled": False,
    "rescueTimer": 10,
    "gameOver": True,
    "win": True,
    "dogDied": False,
    "items": ["Cell", "Baseball Bat"],
    "rooms": {"Attic": Attic, "Bedroom": Bedroom, "Bathroom": Bathroom, "Basement": Basement, "LivingRoom": LivingRoom,
              "Kitchen": Kitchen, "Driveway": Driveway, "CarAccident": CarAccident, "Library": Library}
    }
    for room in gameManager["rooms"]:
        gameManager["rooms"][room].zombies = 0
    BeginGame(gameManager)
