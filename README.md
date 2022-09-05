<h1 align="center">
  brew4me
</h1>

<h4 align="left">
brew4me is a tool to find popular Magic: the Gathering decks using the user's collection.
</h4>

![brew4me](https://i.imgur.com/zEaFtbM.png)

# Installation requirements
Python3 is needed to run the script.


# Installation
1. Copy the repository or [download brew4me as a zip file.](https://github.com/xmliu0512/brew4me/archive/refs/heads/main.zip)
2. Place all files in the same location on your computer.
3. Place your collection file (.csv) in the `collection` folder.

# Usage

## Downloading decks
1. Run `deck_crawler.py`

	  -Note, the first time you ever run the `deck_crawler.py`, it will download Chromium into your home directory (e.g. `~/.pyppeteer/`). This only happens once. You may also need to install a few [Linux packages](https://github.com/miyakogi/pyppeteer/issues/60) to get pyppeteer working.
	  
	  -You can manually add your own decks by placing them in the `decks` folder. (Decklists must be in arena format.)

## Find decks to build
1. Run `brew4me.py`
