AI Bot for the game "FOOTSIES" by HiFight

This program seeks to implement a bot that can play against an opponent (CPU or Human) in the game FOOTSIES. The goal is to use the minimax with alpha-beta pruning in order to accomplish this while making the most rational decisions. 
In order to make sure the bot behaves rational we are using the framedata available to us as well as the x-distances for the bot and opponent to eliminate certain game states.

Note: This bot is omnipotent, and can make non optimal decisions, nor does this bot guarantee a win by any means. This project was created for educational purposes and not meant to promote cheating in anyway shape or form.

What is FOOTSIES?

FOOTSIES is a fighting game developed by Hifight, its free to download, and will need to be downloaded and installed prior to the execution of this program. There are also paid versions of this game, but only the free version was using during this program's development.
The idea of "footsies" appears also every fighting game including some recent ones like "Street Fighter", "Tekken" and many others. Footsies is the tense back-and-forth between two player who are standing and trying to control the space in front of them (known as neutral as well).
This concept is very important in fighting games in terms of gaining the advantage over your opponent, breaking through their defense, and then winning a round. 

How to download and install FOOTSIES:
1. Go to this link: https://github.com/hifight/Footsies/releases/tag/1.5.0  
- NOTE: There are other versions of the game for Mac and Linus respectively so be sure to get the correct version for your machine
2. Once the download has been completed go ahead and [extract all] from the .zip file
3. To run: run "FOOTSIES.exe"

For this program, the game should run once upon the execution of this program


Required libraries:

1. pynput:
* Used for keyboard input simulation and listening for key presses.
* Provides access to Windows-specific features like focusing the game window.
2. pywin32
* Gives access to Windows features

These can be installed by a pip install in your machine's command prompt using: 
pip install [library]

IMPORTANT: Make sure the game "FOOTSIES" is available on your computer, and the file path is accurate on the launch_game() function.

DISCLAIMER: This program is intended for Windows machines

