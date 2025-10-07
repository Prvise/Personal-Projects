import os
import sys
import time
import cowsay
import random
import fontstyle
from tabulate import tabulate
from randfacts import get_fact


def tools():
    generate_fact()
    delete_files()
    loading_screen()
    random_cowsay_char()
    convert_currency()
    read_receipt()


""""
function reads user reciept after on checkout and prints a list of all songs purchased

:param path: function takes a path directory for the generated receipt
:type path: str
:exception FileNotFoundError: function raises an error if a receipt is not found
"""
def read_receipt(directory="path"):
    try:
        with open(directory, "r") as receipt:
            read = receipt.readlines()
            table = []
            i = 0
            for row in read:
                i += 1
                table.append([fontstyle.apply(f"{row}", "bold/green")])
            
            receipt = tabulate(table, headers=[f"{fontstyle.apply("RECEIPT", "bold/cyan")}"], tablefmt="grid")
            print(receipt)
    except FileNotFoundError:
        raise FileNotFoundError






"""
function converts currency from dollars to rands ( current value as of 25 September 2025 )

:param dollar: function takes in a given value in dollars to convert to rands
:type dollar: int or float
:return : a value converted from dollars to rands
:return type: float
:raise ValueError: function raises a value error if given input is not of format int or float
"""
def convert_currency(dollar=0):
    try:
        return float(dollar) * 17.32
    except ValueError:
        raise ValueError


# simply generates a random fact and prints it on screen
def generate_fact():
    fact = get_fact()
    print(fontstyle.apply(fact, "bold/darkcyan"))
    print()






"""
after the program is finished and user has checked out , any remaining file created is deleted 

:exception FileNotFoundError: function handles error if any of the files a not found in path by passing
"""
def delete_files():
    for x in range(20):
        try:
            os.remove(f"Preview{x+1}.mp3")
        except FileNotFoundError:
            pass
    try:
        os.remove("sample_pack.csv")
        return False
    except FileNotFoundError:
        pass






"""
function simply generates a loading screen on command line

:param text: function takes a text as input and displays it on loading screen eg. 'Searching', 'Loading', 'Finding' or anything
:type text: str
""" 
def loading_screen(text="None"):
    os.system("cls")
    dot_count = 0
    max_dots = 4
    loading_speed = 1
    for _ in range(loading_speed):
        dots = ".." * (dot_count % (max_dots + 1))
        sys.stdout.write(f"\r{text}{dots}".ljust(len(f"{text}") + max_dots + 2))
        sys.stdout.flush()
        time.sleep(0.5)
        dot_count += 1

    sys.stdout.write("\r" + " " * (len(f"{text}") + max_dots + 2) + "\r")
    sys.stdout.flush()






"""
function simply generates a random cowsay ascii art and prints goodbye message
"""
def random_cowsay_char():
    os.system("cls")
    characters = [
        "beavis",
        "cheese",
        "cow",
        "daemon",
        "dragon",
        "fox",
        "ghostbusters",
        "kitty",
        "meow",
        "miki",
        "milk",
        "octopus",
        "pig",
        "stegosaurus",
        "stimpy",
        "trex",
        "turkey",
        "turtle",
        "tux",
    ]

    character = random.choice(characters)
    print(
        cowsay.get_output_string(
            character,
            fontstyle.apply("Thanks for visiting THE LOUD HOUSE!", "bold/blue"),
        )
    )


if __name__ == "__main__":
    tools()
