# OneClick

This is a Python project I made while learning Python.

## What it does

OneClick is a simple desktop setup opener. You save a list of website URLs once, and with one click it opens all of them in your browser at the same time — perfect for quickly loading everything you need for studying, working, or any other routine. Your URLs are saved to a file, so they're still there the next time you open the app.

## Features

- Add website URLs to a saved list (just type the name, `https://` is added automatically)
- See all your saved URLs in a scrollable list, each with an X button to remove it
- Launch every saved URL in new browser tabs with a single click
- URLs are saved to a JSON file (`urls.json`) so they survive closing and reopening the app
- Press Enter to add a URL instead of clicking the button
- Dark mode, clean layout

## What I learned

- How to save and load data with JSON (`json.dump`, `json.load`, and handling `FileNotFoundError` on first run)
- How to read user input from a `CTkEntry` and update a `CTkScrollableFrame` dynamically
- How to rebuild a widget list from data with a `refresh` function (clearing old widgets first)
- How to use `lambda` with a default argument (`lambda idx=i: ...`) so each button remembers which row it belongs to
- How to open URLs in the browser with `webbrowser.open_new_tab()`
- Why checking for `.com` isn't a reliable way to validate a URL, and how `.startswith(("http://", "https://"))` works instead

## How to run

1. Install Python 3.8 or newer.
2. Install CustomTkinter:
   ```bash
   pip install customtkinter
   ```
3. Run the file:
   ```bash
   python oneclick.py
   ```

**Made with:** Python

## Future improvements

- Support multiple named setups (Study, Work, Chill) instead of one list
- Reorder URLs by dragging or with up/down buttons
- Add a confirmation dialog before launching many tabs at once
- Import/export the URL list as JSON for easy backup
