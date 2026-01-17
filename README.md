# Scopy
Raspberry Pi based soldering microscope

# Installation

Run 'install_scopy.sh'.
It will create 'run_scopy.sh' script for running it and an autostart entry in ~/.config/autostart which calls it on startup.

# Note

The python script has memory leak which crashes it after some time.
The run_scopy.sh script exists just to restart it when it crashes.
I probably won't be fixing it. In case I ever do, it will probably be a rewrite in some other language.

## File types
.diy - electronic circuit schematics. Opened by DIY Layout Creator
