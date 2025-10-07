import os
import sys
import csv
import tools
import requests
import fontstyle
from wallet import Wallet
from tabulate import tabulate
from pydub import AudioSegment

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


bank = Wallet()
checkout = Wallet()
STATUS = False         #checks if sample_pack is available or not. False if not and True otherwise


#///////////////////////////////////////////////////////////////////MAIN//////////////////////////////////////////////////////////////////////////////////////////////
""""
main function provides a menu for user to guide through program
function prints on screen a main menu with given prompts to navigate

:param: function accepts different user inputs aligning with given prompts
:input type: char 
"""
def main_menu():
    global STATUS
    tools.loading_screen(fontstyle.apply("Loading", "bold/blue"))
    menu = {fontstyle.apply("Main menu", "bold/green"):
             ["1.CHECK BALANCE",
             "2.SEARCH SONG",
             "3.PLAY PREVIEW",
             "4.CHECKOUT"],
             fontstyle.apply("Enter", "bold/green"):
             ["B", 
              "S",
              "P",
              "Q"
              ]
              }
    
    print(tabulate(menu, headers="keys", tablefmt="fancy_grid"))
    prompt = input("Select: ").capitalize()

    match prompt:
        case "B":
            check_balance()
        case "S":
            get_artist()
            generate_preview()
            print(fontstyle.apply("Seach Complete!", "bold/green"))
            main_menu()
        case "P":
            if STATUS == True:
                play_preview()
            else:
                input(fontstyle.apply("No previews to play. Press enter to return to main menu and search for a song ", "bold/red"))
            main_menu()
        case "Q":
            try:
                amount_due = checkout.balance()
                tools.read_receipt("reciept.txt")
                input(fontstyle.apply(f"amount spent: R{amount_due:.02f} After reading receipt press enter to checkout", "bold/blue"))
                os.remove("reciept.txt")
            except (FileNotFoundError, PermissionError):
                pass
            if STATUS == True:
                STATUS = tools.delete_files()

            tools.random_cowsay_char()
            sys.exit()
                
        case _:
            input(fontstyle.apply("Invalid input. Press enter to return to main menu and choose from given prompts ", "bold/red"))
            main_menu()







"""
when selected, function prints a menu guide that indicates user's current balance
using the Wallet class, user can deposit a certain amount of money to use and buy 

:param: function accepts user input
:type: str and float
:exception ValueError: function handles invalid value errors by asking for user input again by reprompting menu
"""
def check_balance():

    tools.loading_screen(fontstyle.apply("Loading", "bold/blue"))
    balance_table = {fontstyle.apply("Current balance", "bold/green"): ["Deposit money", "Withdraw money", "Return to main menu"],
                     fontstyle.apply(f"R{bank.balance():.02f}", "bold/green"): ["Enter D", "Enter W", "Enter Q"]
                     }
    print(tabulate(balance_table, headers="keys", tablefmt="double_grid"))

    prompt = input("Select: ").capitalize()
    match prompt:
        case "D":
            try:
                amount = float(input("Enter amount to deposit:R"))
                bank.deposit(amount)
            except ValueError:
                input(fontstyle.apply("Invalid input. Press enter and deposit a valid amount ", "bold/red"))
            check_balance()
        case "W":
            try:
                amount = float(input("Enter amount to withdraw:R"))
                bank.withdraw(amount)
            except ValueError:
                input(fontstyle.apply("Invalid input or Insufficient funds to complete transaction. Press enter to try again ", "bold/red"))
            check_balance()
        case "Q":
            main_menu()
        case _:
            input(fontstyle.apply("Invalid input. Press enter and please choose from given prompts ", "bold/red"))
            check_balance()







""""
function simply prints a list of all song previews available on the screen 
provides information about the song and pricing

:exception FileNotFoundError: program exits if a sample_pack is not found
"""
def display_preview():
    tools.loading_screen(fontstyle.apply("Loading", "bold/blue"))
    try:
        with open("sample_pack.csv", "r") as file:
            reader = csv.DictReader(file)
            table = [[fontstyle.apply("artist", "bold/green"), fontstyle.apply("song", "bold/green"), fontstyle.apply("price", "bold/green")]]
            
            i = 0
            for row in reader:
                i += 1
                table.append([f"{i}. " + row["artist name"], row["song"], f"R{row["song price"]}"])
            
            table_chart = tabulate(table, headers="firstrow", tablefmt="grid")
            print(table_chart)      
    except FileNotFoundError:
        sys.exit("sample_pack.csv not found")







#////////////////////////////////////////////////////////////////////RETRIEVE SEARCH RESULTS////////////////////////////////////////////////////////////////////////////

"""
with user input this function retrieves song information about an artist from the itunes API
function passes retrieved data to the 'capture_catalog' function to store data

:param: prompt for user input
:type: str and int
:raise ValueError: If user inputs an invalid integer
:exception requests.HTTPError: takes exception if request to api fails
:exception requests.ConnectionError: takes exception if connection to api fails due to max requests exceeded
:return: json file
"""
def get_artist():

    try:
        artist = input(fontstyle.apply("Search artist or song: ", "bold/green"))
        limit = int(input(fontstyle.apply("How many search results would you like to get ( max = 20 ): ", "bold/green")))
        if limit > 20:
            raise ValueError
    except ValueError:
        input(fontstyle.apply("Invalid input or Exceeded search limit. Press enter to return to main menu ", "bold/red"))
        #if exception return to main menu
        main_menu()                                                               

    try:
        response = requests.get(
            f"https://itunes.apple.com/search?entity=song&limit={limit}&term={artist}"
        )
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError):
        input(fontstyle.apply("Failed to connect to itunes API server. Press enter to return to main menu. ", "bold/red"))
        #if exception return to main menu
        main_menu()

    capture_catalog(response.json())







"""
function collects data retrieved by get_artist() and stores the info inside a csv file for temporal use

:param artist_data: json file retrieved from the get_artist() function
:type artist_data: json format file
"""
def capture_catalog(artist_data):

    with open("metadata.csv", "w") as file:
        writer = csv.DictWriter(
            file, fieldnames=["artist name", "song", "song price", "Preview URL"]
        )
        writer.writeheader()

        for info in artist_data["results"]:
            writer.writerow(
                {
                    "artist name": info.get("artistName", "Unknown"),
                    "song": info.get("trackName", "Unknown"),
                    "song price": info.get("trackPrice", "Unknown"),
                    "Preview URL": info.get("previewUrl", "Unknown"),
                }
            )


"""
function collects url links for song previews using generated metadata csv file by capture_catalog()
stores sample pathes to sample pack csv file

:param: None
:return: None
"""
def generate_preview():
    global STATUS
    with open("metadata.csv", "r") as file, open("sample_pack.csv", "w") as sample_pack:
        pack_writer = csv.DictWriter(
            sample_pack, fieldnames=["artist name", "song", "song price", "Preview URL"]
        )
        pack_writer.writeheader()
        reader = csv.DictReader(file)

        #generate a random fact while user waits for search to finish
        print()
        print(fontstyle.apply("Here is a random fun fact while you wait for your search results!", "bold/green"))
        tools.generate_fact()

        i = 0
        for link in reader:
            i += 1
            with open(f"preview{i}.m4a", "wb") as sound:
                session = requests.Session()
                url = link.get("Preview URL", "Unknown")
                audio = session.get(url).content
                sound.write(audio)
                m4a = f"preview{i}.m4a"
                mp3 = f"preview{i}.mp3"
                convert_audio(m4a, mp3)

                if "Unknown" == link["song price"]:
                    price = 0
                else:
                    price = tools.convert_currency(link["song price"])

                pack_writer.writerow(
                    {
                        "artist name": link["artist name"],
                        "song": link["song"],
                        "song price": f"{price:.2f}",
                        "Preview URL": mp3,
                    }
                )
            os.remove(m4a)
    os.remove("metadata.csv")
    STATUS = True





"""
converts audio downloaded from itunes format m4p to mp3

:param m4a, mp3: \path directory for flaac sample and mp3 sample respectively
:type m4a: str
:type mp3: str
:exceptions FileNotFoundError: program exits if files not found
:return: None 
"""
def convert_audio(m4a, mp3):
    try:
        audio = AudioSegment.from_file(m4a, format="m4a")
        audio.export(mp3, format="mp3")
    except FileNotFoundError:
        sys.exit("Failed to convert audio to new format")

   


#////////////////////////////////////////////////////////////////////////////AUDIO PLAYER/////////////////////////////////////////////////////////////////////////////////

"""
function plays previews from sample_pack.csv using pygame module

:param: function takes user input to navigate through each song preview
:exception ValueError: function handles value error if a certain song does not have a defined pricing

"""
def play_preview():

    global STATUS
    pygame.mixer.init()
    display_preview()
   

    with open("sample_pack.csv", "r") as file, open("reciept.txt", "a") as reciept:
        sample_reader = csv.DictReader(file)
        i = 0
        for sample in sample_reader:
            i +=1
            try:
                song_price = float(sample["song price"])
            except ValueError:
                song_price = 0
                pass

            song = sample["Preview URL"]
            song_name = sample["song"]
            artist = sample["artist name"]
            
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=-1, fade_ms=1000)

            prompt_guide = fontstyle.apply("Press Enter to add to cart. Press x + Enter to skip. ", "bold/green")
            prompt = input((f"Playing {fontstyle.apply(artist, "bold/cyan")} ~ {fontstyle.apply(song_name, "bold/cyan")}. {prompt_guide} ")).lower()
            match prompt:
                case "":
                        pygame.mixer.music.fadeout(800)
                        try:
                            bank.withdraw(song_price)
                            checkout.deposit(song_price)
                            print(fontstyle.apply("Song added to cart!☆彡", "bold/green"))
                            print(f"current balance: R{bank.balance():.02f}")
                            reciept.write(f"{i}. {artist} ~ {song_name} \n")
                        except ValueError:
                            input(fontstyle.apply("Failed transaction due to insufficient funds. Press enter to return to main menu and check your balance ", "bold/red"))
                            break
                case "x":
                    pygame.mixer.music.fadeout(800)
                case "_":
                    pygame.mixer.music.unload()
        pygame.mixer.music.unload()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    main_menu()
