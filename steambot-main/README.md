# CatBot

This is a Discord bot to summon cat images from [The Cat API](https://thecatapi.com) into a Discord channel. Channel participants can rate cat images with emoji reactions, with ratings sent back to The Cat API.


# Setup

First, install [Python](https://www.python.org/downloads/) if you don't already have it installed.

Next, set up the virtual environment. This is one-time setup: you only need to run it again if you delete the `venv` folder that it creates, or if the contents of that folder become corrupted somehow.

- In a Unix-like terminal (including macOS and Windows Subsystem for Linux): `./configure`
- In Windows PowerShell: `./configure.bat`

Now, enter the virtual environment. This will only modify your currently running terminal session: you will have to re-do this step every time you open a new terminal session to work on this project.

- In a Unix-like terminal: `source venv/bin/activate`
- In Windows Powershell: `venv\bin\Activate.ps1`

You should see the text `(venv)` in your terminal prompt, indicating that this current terminal session has entered the virtual environment for this project. When you're finished with your development session in this terminal, run `deactivate` to exit the virtual environment, which will also remove the `(venv)` text. (You can also just exit the whole terminal session.)

Now, acquire an [API key for TheCatAPI](https://thecatapi.com/signup) and a [Discord Token](https://discordpy.readthedocs.io/en/stable/discord.html). Be careful not to share these keys with anyone you don't know and trust, since they can allow someone else to use your bot's account with these services.

Create a file named `catbot.json` in the root of this project folder and enter your API key and token in the following format (replacing the example key and token below with your actual key and token).

```
{
  "thecatapi": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "discord": "XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

For security, the `.gitignore` file for this project is configured to avoid checking in the `catbot.json` file.


# Installation

To install the project into the virtual environment, run `pip install .` from within the project folder while you're in the virtual environment. This makes the program accessible while you're in the virtual environment, but not outside it, which is good for while the program is in development. To uninstall, run `pip uninstall catbot` while in the virtual environment.

To install the program to your user account, run `pip install .` from within the project folder while you're **not** in the virtual environment. This makes the program accessible whenever you're logged into your account, regardless of whether you're in the virtual environment, which is good when you have a program that works. To uninstall, run `pip uninstall catbot` while outside the virtual environment.

You can have the program installed in both of these environments at once, and the version installed in the virtual environment can be different than the version installed in your user account, which is good when you have a stable version that works and a new in-progress development version that doesn't work yet.


# Execution

To run the installed program, run `python -m catbot`.

Note that this does not directly run the source code in the `src` folder, it runs the version of the program installed in the current environment (either the virtual environment or your user account). This means you should re-run `pip install .` after making changes to the code.
