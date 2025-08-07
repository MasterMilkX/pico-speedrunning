# PPP - [P]ython [P]ICO-8 [P]ipeline TAS Interpreter
# This code is a hot mess -- don't look directly at it
# It involves python, lua, bash, and binary if you could believe it
# Written by Milk (i'm sorry lmao)


import time
from pynput.keyboard import Key, Controller
import subprocess
import random
import os
from PIL import Image
import glob

import argparse

# Global variables
LOVE_COMMAND = "[ADD YOUR EXTENSION TO LOVE HERE]"              # Path to love executable
CELIA_PATH = "[ADD YOUR EXTENSION TO CELIA HERE]"               # Path to Celia
TAS_DAT_LOCATION = "tas_out"                                    # Path to saved TAS data (tas file and png)

PICO_8_GAME = "[NAME OF THE PICO-8 GAME TO RUN (in Celia/carts folder)]"         # NAME of PICO-8 game
GAME_NAME = PICO_8_GAME.split('/')[-1].split('.')[0]

KEYBOARD = Controller()                                         # Keyboard controller for inputs to Celia


#########  HELPER FUNCTIONS ########

# press a key
def quick_key(key):
    KEYBOARD.press(key)
    KEYBOARD.release(key)

# skips the game forward this many frames
def skip_frames(n):
    [KEYBOARD.press('l') for f in range(n)]

# go back this many frames
def rewind_frames(n):
    [KEYBOARD.press('k') for f in range(n)]

# reset the run and play
def reset_run():
    quick_key('d')
    quick_key('p')

# convert binary to keys
def int2keys(i):
    b = [int(a) for a in '{:06b}'.format(i)]
    b = b[::-1]
    keys = [Key.left, Key.right, Key.up, Key.down, "z", "x"]
    return [keys[i] for i in range(6) if b[i] == 1]

# returns random key combos
def randKey():
    return random.randint(0,63)

# generate a random key with a chance of being 0
def randWeightKey(zero_weight=0.5):
    return 0 if random.random() < zero_weight else random.randint(1, 63)


# makes a tas file from a list of binary strings
def random_tas(frame_len=100):
    # generate a random TAS file
    tas = [str(random.randint(0,63)) for i in range(frame_len)]
    with open(f"{TAS_DAT_LOCATION}/{GAME_NAME}.tas", "w+") as f:
        f.write(",".join(tas))
        f.close()
    return tas

# imports the TAS file to the game
def load_tas():
    print(f"[PPP] Loading local TAS file for {PICO_8_GAME} (named {GAME_NAME}.tas)")
    with KEYBOARD.pressed(Key.shift):
        print(f"[PPP] Resetting input frames")
        KEYBOARD.press('r')
        time.sleep(0.5)
        KEYBOARD.release('r')
        print(f"[PPP] Loading TAS file")
        KEYBOARD.press('w')
        time.sleep(0.5)
        KEYBOARD.release('w')


# plays the TAS file directly into the game
def play_tas(tas_arr):
    print(f"[PPP] Playing TAS file")
    for frame in tas_arr:

        keys = int2keys(int(frame))
        for k in keys:
            KEYBOARD.press(k)
            KEYBOARD.release(k)
        KEYBOARD.press('l')             # iterate the frame


def play_thru(frames=1000):
    print(f"[PPP] Playing through the game")
    for i in range(frames):
        # iterate the frame
        KEYBOARD.press('l')
        KEYBOARD.release('l')

        # wait a bit
        time.sleep(0.03)
    

# creates a input frame of random keys
def randInputFrame():
    key_int = randWeightKey()
    keys = int2keys(key_int)
    for k in keys:
        KEYBOARD.press(k)
        KEYBOARD.release(k)
    KEYBOARD.press('l')             # iterate the frame



# retrieve screenshot data
def get_screenshot():
    # remove previous screenshots
    print(f"[PPP] Remove previous screenshots")
    [os.remove(f) for f in glob.glob(f"{TAS_DAT_LOCATION}/{GAME_NAME}*.png")]

    # make the screenshot
    print(f"[PPP] Making screenshot")
    quick_key(Key.f6)

    # retreive the screenshot
    try:
        time.sleep(1)
        first_pic = glob.glob(f"{TAS_DAT_LOCATION}/{GAME_NAME}*.png")[0]
        print(f"[PPP] Retrieving screenshot from [{first_pic}]")
        screenshot = Image.open(first_pic)
        return screenshot
    except:
        print("[PPP] No screenshot found")
        return None



# run the pipeline
def start_pipe():

    # run the command and monitor the output
    print("[PPP] Running Celia")
    celia_proc = subprocess.Popen([LOVE_COMMAND, CELIA_PATH, PICO_8_GAME])

    # wait 1 second
    time.sleep(1)

    # start up command
    # try:
    #     print("[PPP] Using start_up.tas to start the game past menu")
    #     start_up = []
    #     with open(os.path.join(f'{TAS_DAT_LOCATION}',f'{GAME_NAME}-start_up.tas'), "r") as f:
    #         start_up = f.read().split(",")
    #         f.close()
    #     play_tas(start_up)
    # except:
    #     print("[PPP] No start_up.tas found")
    #     # time.sleep(2)

    # time.sleep(1)


    # random inputs
    for i in range(500):
        randInputFrame()
        time.sleep(0.03)

    # get the screenshot
    # print(get_screenshot())


    ### TEST EXPERIMENTS ###

    # make a random TAS file
    # print("[PPP] Making a random file!")
    # rtas = random_tas(100)
    # print(f"[PPP] {rtas}")
    # time.sleep(2)


    # load the TAS file with "shift-W"
    # print("[PPP] Resetting run")
    # reset_run()

    # load the TAS file
    # print("[PPP] Loading TAS file")
    # load_tas()

    # # play the TAS file
    # play_thru(len(rtas))

    # iterate for 100 frames
    # print(f"[PPP] Forward 100 frames")
    # skip_frames(100)

    # # wait 1 seconds
    # time.sleep(1)

    # # rewind 30 frames
    # print(f"[PPP] Rewind 30 frames")
    # rewind_frames(30)

    # wait 3 seconds then kill
    time.sleep(3)
    print("[PPP] GOODBYE!")
    celia_proc.kill()





if __name__ == "__main__":
    start_pipe()


