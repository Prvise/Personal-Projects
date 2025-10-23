# THE LOUD HOUSE!
#### Video Demo: [Watch on YouTube](https://youtu.be/1BEgn0sNPg0)
#### Description:

---

## Project Overview

For my CS50 Python final project, I decide to implement **THE LOUD HOUSE!**, a program that imitates a digital music store. In the store, users can search for their favorite songs and artists, preview tracks, purchase them, and keep track of their bank balance through a simulated wallet system.  

The project relies on the iTunes API and the `requests` module to fetch music data. By sending pull requests to `https://itunes.apple.com/search?entity=song&limit={limit}&term={artist}`, the program retrieves JSON-formatted search results, including song details such as track name, artist, price, and preview links.  

---

## How It Works

When the program runs, users are greeted with a menu offering several options:
- Deposit money 
- Search for music by artist or song name  
- Preview and purchase tracks 
- Checkout and receive a generated receipt  

The program uses a wallet class, a few functions, and external libraries to help store and interprete data and simulate the experience of browsing and purchasing music online.  

---

## Files and Key Functions

### `project.py` (Main Program File)
This file contains the core logic of the program and handles all API requests, data storing and manipulating, and the main menu system.  

- **Functions for Data Retrieval & Audio Previews**  
  - `get_artist` - Prompts for user input and retrieves song data from iTunes API using specified parameters 
  - `capture_catalog` – Converts retrieved json file from pull request and stores necessary file information about song and artist into a 'metadata.csv' file.  
  - `generate_preview` – Reads information from 'metadata.csv' file. Then collects url links to retrieve samples passing links to `requests.Session` module. calls `convert_audio` to convert retrieved previews and generates a 'sample_pack.csv' file that stores path directions to converted previews.
  - `convert_audio` – Converts downloaded FLAC previews into MP3 format using `pydub.AudioSegment` module.  
  - `play_preview` – Plays the audio preview using `pygame` module.  

Together, these functions along with the `main_menu` function, allows users to browse, preview, and buy songs. 
At checkout, the program generates and displays a receipt summarizing the user’s purchases and amount spent.  

---

### `tools.py` (Utility Functions)
This file contains helper functions that extend the program’s functionality:  

- **`generate_fact`**  
  Uses the `randfacts` module to display random fun facts while users wait for their search results.  

- **`convert_currency`**  
  Converts song prices from USD (as provided by iTunes) into ZAR (South African Rand).  

- **`loading_screen`**  
  Clears the console using `os.system` module method between menu displays for a smoother and cleaner user experience.  

- **`delete_files`**  
  Cleans up temporary files using `os.remove` method (e.g., downloaded audio previews) when the program ends.

- **`random_cowsay_char`**
  Randomly generates ascii art with goodbye message using `cowsay` module and `random.choice` method.

---

### `wallet.py` (Additional Utility Function)

- **Class: `Wallet`**  
  The Wallet class contains methods to deposit funds, withdraw money, and check balance. This ensures users can manage their spendings while making purchases and also deposit more money if they run out of funds. Currrencies handled are in dollars and rands, and error handling systems are implemented to handle invalid or malicious user inputs. 

---

## Design Choices and Challenges

While building this project, I had to make several important design decisions:  

1. **Audio Playback Format**  
   The iTunes preview links by default returns audio files in FLAC format. Since Python does not natively support FLAC playback, I initially struggled to play previews. After testing multiple approaches, I learnt it was best to convert FLAC files to MP3 using the `pydub` module and `pydub.AudioSegment` method, then play them with another third-party package `pygame`. Its important I point out that in order for the pydub functionality to work, I had to take an extra step and `sudo apt install ffmpeg` and install `pip.install audioop`. This ensured reliable audio playback while keeping dependencies lightweight. Taking this approach was quite challenging and it came with many trials and errors but I eventually found a way to make it all work out, as I sigh.

2. **Currency Conversion**  
   Because I live in South Africa and our currency is ZAR, I felt it was more practical for local users to see prices in Rands rather than USD. This required writing a helper conversion function in `tools.py`.  

These choices and steps made the project more robust, user-friendly, and realistic.  

---

## Conclusion

By combining API requests, file handling, audio processing, and user interaction, **THE LOUD HOUSE** demonstrates how Python can be used to create an interactive program that simulates a real-world application. The project balances technical functionality with user experience, offering features like currency conversion, wallet management, fun facts, and receipt generation. 

My name is Praise, and this was THE LOUD HOUSE.

