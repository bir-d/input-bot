# input-bot
Quick discord bot written with discord.py, made for Uncharity Vigil 2023.

Uses [shelve](https://docs.python.org/3/library/shelve.html) for persistent storage and [pynput](https://pypi.org/project/pynput/) for pressing keys on the host :)

## Install
Install requirements (check requirements file)

Edit .env with your bot token and authentication role, invite the bot to your server

Run main.py

## Usage
FIRST TIME: Server owner should run $sync to push slash commands to discord

$setcredits ($scr) <USER> <NUMBER>: sets a given users credit count to the number given

$addcredits ($acr) <USER> <NUMBER>: adds a given amount of credits to the given user

$credits ($cr) <USER>: prints the current amount of credits held by the given user

$sendinput ($si) <INPUT>: Sends the given input to the computer, uses 1 credit. An input is a character, or a string consisting of a [Key](https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key), or a [KeyCode](https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#KeyCode)

$sendinputstring ($sis) <INPUTSTRING> <DELAY>: Iterates through the characters in INPUTSTRING and sends each to the computer with a delay of DELAY ms between each one.
