# pico-speedrunning
Source code for PICO-8 cartridge speedrunning using Celia
This code was originally written in <8 hours for [Dagstuhl 24216](https://drops.dagstuhl.de/entities/document/10.4230/DagRep.14.6.130)
*This code is incomplete*

## Setup

1. Clone this repository
2. Download the [LOVE](https://love2d.org/#download) application 
3. Download the [Celia TAS tool](https://www.lexaloffle.com/bbs/?tid=50283)
4. (Optional) Create a virtual environment in this repository
    - Example: `python -m venv ai-speedrun`
5. Install the libraries from the requirements.txt file
6. Place any pico-8 carts you would like to use (in .p8 format) in the Celia/carts folder

## Usage

1. Set the global variables in [ppp.py](ppp.py) to the appropriate paths
    - **LOVE_COMMAND**: Path to the LOVE application to call from command line
    - **CELIA_PATH**: Path to the Celia application
    - **TAS_DAT_LOCATION**: Output for screenshots and TAS files created by the program
    - **PICO_8_GAME**: The game you would like to run (in png format)
2. Run/edit [ppp.py](ppp.py) with `python3 ppp.py`
    - The TAS files are integer values corresponding to binary inputs of the Celia tool
    - Be careful not to change screens while running!
