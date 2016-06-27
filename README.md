### XPilot bot
This code implements a XPilot virtual player based on human player history. As a project of the Scientific Python for Engineers subject.

It is intended to work with the libPyAI version that is included. This version is patched in order to allow setting up and down the ship shield. The behaviour of libPyAi.shield() is to 'toggle the space bar key'. Also, the hisory.csv file contains data stored from recorded games and is needed for classifier training.

All other files are source code. The main file to be run  is pilot.py: `python3 pilot.py`. It is currently set up to play in a localhost server. The startup can take a while since the classifier needs to be trained.

This project is hosted in [GitHub](https://github.com/jordisoler/xpilot).
