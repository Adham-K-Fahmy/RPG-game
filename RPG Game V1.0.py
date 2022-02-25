# Made by: Adham Khaled
# Version: 1.0
# This is a text based RPG game the goal is to complete all of the stages
# The input has to be a number
# The progress is auto saved
# There is a problem with the stats equations (gold, enemy stats, user stats) which will be fixed in the next version


import math
import random
import sys
import shelve
import time


# Takes input from the user and makes sure it's a number within a valid range
def user(user_input, limit):

    # Removes all the spaces in the input
    user_input = user_input.replace(" ", "")

    # Checks if the input is a number if yes it saves it as an integer else it returns False
    if user_input.isdigit():

        user_input = int(user_input)

        # Checks if the number is within a valid range if yes it returns that number else it returns False
        if user_input in range(1, limit):

            return user_input

        else:

            return False

    else:

        return False


# Creates the enemy's stats using an equation (the equation is not balanced and will be edited)
def stage_enemy(num):

    return num*16+math.floor(math.sqrt(num*20)), num*3+math.floor(math.sqrt(num*10))


# A function for printing valid adventures(stages) and entering a stage depending on the input
def adventure():

    print("\nChoose stage number\n")
    # Counts the cleared stages and prints valid stages based on it (if you cleared stage 1 you can fight in stage 2)
    count = len(cleared_stages)

    # Makes sure that it doesn't print stages that don't exist(last stage is 12 makes sure it doesn't print 13)
    if count > 11:

        count = 11

    # Prints stages until the stage after the last stage cleared
    # ex: if you cleared stage 5 it'll print stages until stage 6
    for i in range(1, count+2):

        print(f"Stage {i}")
        # Sleep for dynamic typing
        time.sleep(0.25)

    print("\nPress enter to return\n")
    stage = input()

    # Checks if the user wants to return to the main menu else it checks if the input is a valid number
    if stage == "":

        return 0

    stage = user(stage, count+2)

    # While the input isn't a valid number or the user doesn't want to return it'll keep asking for input
    while not stage:

        print("\nInvalid number\n"
              "Please, try again\n")
        stage = input()

        # Checks if the user wants to return to the main menu else it checks if the input is a valid number
        if stage == "":

            return 0

        stage = user(stage, count+2)

    # Takes the enemy's stats from stage_enemy function the stats get higher with each higher stage
    enemy_hp, enemy_atk = stage_enemy(stage)
    # Return the fight function which takes the stats of the user and enemy and the stage number
    return fight(_hp + _armor_hp + _boot_hp, _atk + _sword_atk, enemy_hp, enemy_atk, stage)


# Fight function for the battle which takes the user's total health and attack and enemy's health and attack and stage
# and reduces the health of each by the damage of the other for each round until one of them dies (hp less than 0)
def fight(hp, base_atk, enemy_hp, base_enemy_atk, _stage):

    # Round counter (starts from 0)
    _round = 1
    print("")

    # Battle loop while health of the player or the enemy isn't 0 or less it'll continue
    # Note: the user always starts first
    while hp > 0 and enemy_hp > 0:

        # Generates random attack within the range of (atk - square root of the atk) to atk
        # for each of the enemy and the player
        enemy_atk = random.randint(math.floor(base_enemy_atk - math.sqrt(base_enemy_atk)), base_enemy_atk)
        atk = random.randint(math.floor(base_atk - math.sqrt(base_atk)), base_atk)
        print(f"\tRound{_round}\n")
        # Sleep for dynamic typing and so the user gets enough time to read the output before the screen scrolls down
        time.sleep(0.75)
        print(f"Enemy HP {enemy_hp} (-{atk})")
        enemy_hp -= atk
        time.sleep(1)

        # Checks if the enemy's hp is higher than 0 before the enemy attacks the user if yes then it breaks the loop
        if enemy_hp <= 0:

            break

        print(f"HP {hp} (-{enemy_atk})\n")
        hp -= enemy_atk
        _round += 1
        time.sleep(1)

    # Checks if the enemy's hp is lower than or equal to 0 if yes then the user won if not he lost
    if enemy_hp <= 0:

        print("\n\t\tVICTORY")
        # The stage is added to the cleared stages
        cleared_stages.add(_stage)
        # A formula for generating a random number of gold based on the cleared stage (Will be edited)
        gold = random.randint(math.floor((5 * _stage) / 2), 6 * _stage - math.floor(math.sqrt(_stage * 2)))

        if _stage == 12:

            # If the user finished the last stage it congratulates him
            print("\nCONGRATS YOU'VE FINISHED THE LAST LEVEL\n")

        print(f"\t\tGold (+{gold})")

    else:

        print("\n\t\tDEFEAT\n"
              "Try buying items from shop")
        gold = 0

    # An input for waiting so the user gets enough time to read the messages
    _wait = input("\nPress enter to return ")
    del _wait
    # returns the amount of gold acquired (0 if the user lost)
    return gold


# Inventory function for showing items that the user has bought and equipping them
# Takes the parameters of the equipped items' stats
def inventory(armor_hp, boot_hp, sword_atk):

    # Unless the user want's to return to the main menu the loop will keep going
    while True:

        # Checks for each item if the user has bought them it prints them else it doesn't
        if len(_items) == 0:

            print("\nYou have no items you can buy items from shop")

        if 1 in _items and sword_atk != 10:

            print("\n1-Starter Sword")
            time.sleep(0.3)

        if 2 in _items and sword_atk != 20:

            print("\n2-Apprentice Sword")
            time.sleep(0.3)

        if 3 in _items and armor_hp != 50:

            print("\n3-Starter Armor")
            time.sleep(0.3)

        if 4 in _items and armor_hp != 100:

            print("\n4-Apprentice Armor")
            time.sleep(0.3)

        if 5 in _items and boot_hp != 20:

            print("\n5-Starter Boots")
            time.sleep(0.3)

        if 6 in _items and boot_hp != 50:

            print("\n6-Apprentice Boots")
            time.sleep(0.3)

        print("\nPress enter to return")

        equip = input("\n")

        # Checks if the user wants to return to the main menu if yes it returns the equipped items
        # if not it checks if the input is a valid input
        if equip == "":

            return armor_hp, boot_hp, sword_atk

        equip = user(equip, 7)

        # While the input is not valid the user enters another input
        # either he returns to the main menu or enters a valid number
        while not equip:

            print("\nInvalid number\n"
                  "Please, try again\n")
            equip = input("\n")

            if equip == "":

                return armor_hp, boot_hp, sword_atk

            equip = user(equip, 7)

        # Checks each item for the user's input and equips the one that the user chose
        # unless the user doesn't own that item
        if equip == 1:

            if 1 not in _items:

                print("\nYou don't have that item")

            else:
                sword_atk = 10
                print("\n\tItem equipped")
            time.sleep(1.5)

        if equip == 2:

            if 2 not in _items:

                print("\nYou don't have that item")

            else:
                sword_atk = 20
                print("\n\tItem equipped")
            time.sleep(1.5)

        if equip == 3:

            if 3 not in _items:

                print("\nYou don't have that item")

            else:
                armor_hp = 50
                print("\n\tItem equipped")
            time.sleep(1.5)

        if equip == 4:

            if 4 not in _items:

                print("\nYou don't have that item")

            else:
                armor_hp = 100
                print("\n\tItem equipped")
            time.sleep(1.5)

        if equip == 5:

            if 5 not in _items:

                print("\nYou don't have that item")

            else:
                boot_hp = 20
                print("\n\tItem equipped")
            time.sleep(1.5)

        if equip == 6:

            if 6 not in _items:

                print("\nYou don't have that item")

            else:
                boot_hp = 50
                print("\n\tItem equipped")
            time.sleep(1.5)


# Shop function for buying items takes the parameter of the gold that the user has
# It shows all the items unless the ones that the user has already bought
def shop(_gold):

    # Unless the user want's to return to the main menu the loop will keep going
    while True:

        print(f"\n\tGold: {_gold}")
        # Sleep for dynamic typing and to give the user enough time to read the output
        time.sleep(0.4)

        # Checks for each item if it's in the items that the user has it skips it if not it prints it with it's cost
        if 1 not in _items:

            print("\n1-Starter Sword")
            time.sleep(0.25)
            print("\n\t10 Gold")
            time.sleep(0.6)

        if 2 not in _items:

            print("\n2-Apprentice Sword")
            time.sleep(0.25)
            print("\n\t25 Gold")
            time.sleep(0.6)

        if 3 not in _items:

            print("\n3-Starter Armor")
            time.sleep(0.25)
            print("\n\t15 Gold")
            time.sleep(0.6)

        if 4 not in _items:

            print("\n4-Apprentice Armor")
            time.sleep(0.25)
            print("\n\t35 Gold")
            time.sleep(0.6)

        if 5 not in _items:

            print("\n5-Starter Boots")
            time.sleep(0.25)
            print("\n\t5 Gold")
            time.sleep(0.6)

        if 6 not in _items:

            print("\n6-Apprentice Boots")
            time.sleep(0.25)
            print("\n\t15 Gold")
            time.sleep(0.6)

        print("\nPress enter to return")

        buy = input("\n")

        # Checks if the user wants to return to main menu if yes it returns the current gold
        # if not it checks if the user's input is valid
        if buy == "":

            return _gold

        buy = user(buy, 7)

        # While the user's input is invalid and the user doesn't want to return to main menu
        # it'll keep asking for new input
        while not buy:

            print("\nInvalid number\n"
                  "Please, try again\n")
            buy = input("\n")

            if buy == "":

                return

            buy = user(buy, 7)

        # Checks the user's input and compares it with the items that the user has already bought
        # if it's not already bought by the user it checks if the user has enough money to buy it
        # if yes it's added to the items that the user has and it's cost is subtracted from the money that the user has
        # and prints "Bought" else it prints "Not enough Gold" then returns to the shop function
        # in either case it sleeps so the user gets time to read the message
        if buy == 1 and 1 not in _items:

            if _gold >= 10:

                _gold -= 10
                _items.append(1)
                print("\n\tBought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        if buy == 2 and 2 not in _items:

            if _gold >= 25:

                _gold -= 25
                _items.append(2)
                print("\n\tbought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        if buy == 3 and 3 not in _items:

            if _gold >= 15:

                _gold -= 15
                _items.append(3)
                print("\n\tbought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        if buy == 4 and 4 not in _items:

            if _gold >= 35:

                _gold -= 35
                _items.append(4)
                print("\n\tbought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        if buy == 5 and 5 not in _items:

            if _gold >= 5:

                _gold -= 5
                _items.append(5)
                print("\n\tbought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        if buy == 6 and 6 not in _items:

            if _gold >= 15:

                _gold -= 15
                _items.append(6)
                print("\n\tbought")
                time.sleep(1.5)
                continue

            else:

                print("\nNot enough gold")
                time.sleep(1.5)
                return shop(_gold)

        else:

            print("Item's already bought")


# Save function for storing the user's data
# it works using shelve library
def save():

    # Opens the save file
    save_file = shelve.open("User_Data")
    # Saves each variable in the file with their keyword
    save_file["stage"] = cleared_stages
    save_file["hp"] = _hp
    save_file["atk"] = _atk
    save_file["gold"] = _gold
    save_file["items"] = _items
    save_file["armor_hp"] = _armor_hp
    save_file["boot_hp"] = _boot_hp
    save_file["sword_atk"] = _sword_atk
    # Closes the file
    save_file.close()


# A function for loading the data which were save if there was no data saved it creates a file to save the data in
# and returns the default (starting) values to each variable
def load_files():

    # Opens the file (creates a file if there is none)
    save_file = shelve.open("User_Data")

    try:

        # Checks if there is a save variable in this keyword if there is one it loads the data from each keyword
        # to it's variable and prints "welcome back to FAR"
        # If there's no data it'll give an error which will make the except case run
        # which prints "Welcome to FAR" then prints the tutorials then waits for user to press enter
        # then returns the defaults of each variable
        check_save_file = save_file["stage"]
        del check_save_file
        print("\nWelcome Back to FAR\n"
              "We missed you\n")
        time.sleep(0.6)
        return save_file["stage"], save_file["hp"], save_file["atk"], save_file["gold"], save_file["items"]\
            , save_file["armor_hp"], save_file["boot_hp"], save_file["sword_atk"]

    except:

        print("\nWelcome to FAR (Fun Addictive RPG)\n"
              "Made by FCAI student: Adham Khaled\n"
              "\t\tVersion 1.0\n")
        time.sleep(0.6)
        print("How to play: Your goal is to finish all the stages.")
        time.sleep(1)
        print("You get gold for each stage you win.")
        time.sleep(1)
        print("You can use this gold to buy items in shop.")
        time.sleep(1)
        print("You can equip bought items from inventory.")
        time.sleep(1)
        print("You can play by typing the number of your selection.\n"
              "ex: if you want to choose stage 1 you have to type 1")
        time.sleep(1)
        print("note: your progress is auto saved so don't worry if your game shuts down for any reason")
        time.sleep(1)
        _wait = input("\npress enter to continue")
        del _wait
        return set(), 50, 10, 0, [], 0, 0, 0


# sets each variable to it's value using the load function
cleared_stages, _hp, _atk, _gold, _items, _armor_hp, _boot_hp, _sword_atk = load_files()
# Game loop (Main menu)
while True:

    # prints each valid option then sleeps for dynamic typing
    print("\n1-Adventure")
    time.sleep(0.25)
    print("2-Inventory")
    time.sleep(0.25)
    print("3-Stats")
    time.sleep(0.25)
    print("4-Shop")
    time.sleep(0.25)
    print("5-Save and Quit\n")
    _input = user(input(), 6)

    # While the input isn't valid it will keep asking the user for another input
    while not _input:

        print("\nInvalid input.\n"
              "Please, try again\n")
        _input = user(input(), 6)

    if _input == 1:

        # Goes to the adventure function which calls the fight function which returns gold if you won and 0 if you lost
        # then saves the progress
        _gold += adventure()
        save()

    elif _input == 2:

        # Assigns each of these variables to the value that returns from the inventory function
        # based on what the user equips then saves the progress
        _armor_hp, _boot_hp, _sword_atk = inventory(_armor_hp, _boot_hp, _sword_atk)
        save()

    elif _input == 3:

        # Prints the stats of the user (Attack, Health and, Gold) then waits for the user to return to main menu
        print(f"\nAttack: {_atk + _sword_atk}\n"
              f"HP: {_hp + _armor_hp + _boot_hp}\n"
              f"Gold: {_gold}\n")
        wait = input("press enter to return ")
        del wait

    elif _input == 4:

        # Assigns the gold to the value that returns from the shop function based on what the user buys
        # then saves the progress
        _gold = shop(_gold)
        save()

    elif _input == 5:

        # Saves the progress then prints a goodbye message then quits the game
        save()
        print("\n\t\t\tSaved\n\n")
        time.sleep(0.6)
        print("Hope you enjoyed the game\n"
              "Give me your feedback on noorcool116@gmail.com\n")
        sys.exit()
