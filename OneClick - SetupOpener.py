# Import customtkinter for the modern-looking GUI widgets
import customtkinter as ctk
# Import webbrowser so we can open URLs in the default browser
import webbrowser
# Import json to read/write our saved URL list to disk
import json
# Import messagebox for small popup dialogs (info, warning, etc.)
from tkinter import messagebox

# ---------------- SAVE / LOAD ----------------
# Name of the JSON file where URLs are stored
JSON_FILE = "urls.json"

# Load the list of URLs from disk when the app starts.
# Returns a list of strings (or an empty list if no file exists yet).
def load_urls():
    try:
        # Open the JSON file in read mode
        with open(JSON_FILE) as f:
            # json.load reads the file and returns the Python list inside
            return json.load(f)
    except FileNotFoundError:
        # First time running: no file yet, so just return an empty list
        return []

# Save the current list of URLs to disk.
# "url_list" is the Python list we want to persist.
def save_urls(url_list):
    # Open the file in write mode ("w" overwrites the old content)
    with open(JSON_FILE, "w") as f:
        # Write the list as pretty-printed JSON (indent=2 = nicer to read)
        json.dump(url_list, f, indent=2)


# ---------------- APP ----------------
# Create the main application window
root = ctk.CTk()
# Set window size: 500 wide × 700 tall, positioned at (0,0) = top-left
root.geometry("500x700+0+0")
# Set the window title bar text
root.title("OneClick")

# Set the app to dark mode
ctk.set_appearance_mode("dark")

# Load any previously saved URLs from disk into the "urls" list
urls = load_urls()

# Layout: let the setup card expand
# Make column 0 stretch to fill the full width of the window
root.grid_columnconfigure(0, weight=1)
# Make row 2 (the setup card row) stretch vertically
root.grid_rowconfigure(2, weight=1)

# The big "OneClick" title at the top of the window
title = ctk.CTkLabel(root, text="OneClick", font=("Arial", 50, "bold"))
# Place it in row 0, centered horizontally (sticky="n" = north/top),
# with 20px side padding and (20 top, 5 bottom) vertical padding
title.grid(row=0, column=0, sticky="n", padx=20, pady=(20, 5))

# The smaller subtitle below the title
description = ctk.CTkLabel(root, text="OneClick - Setup Opener", font=("Arial", 20))
# Place it in row 1
description.grid(row=1, column=0, pady=10)

# The bordered frame ("card") that holds everything for the URL setup
setup1_frame = ctk.CTkFrame(root, border_width=2, border_color="white")
# Place it in row 2 (the stretchy row), filling its cell in all directions
setup1_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

# A small instruction label at the top of the card
inst = ctk.CTkLabel(setup1_frame, text="Enter full website urls (remember TLDS!) ⬇️")
# Pack it at the top with a bit of padding
inst.pack(pady=(15, 5))

# The text entry box where the user types a URL
entry = ctk.CTkEntry(setup1_frame, width=300, placeholder_text="Enter website url (one at a time)")
# Pack it below the instruction label
entry.pack(pady=10)

# The button that adds whatever is in the entry to the URL list
add_button = ctk.CTkButton(setup1_frame, text="Add URL", width=180,
                           hover_color="green", command=lambda: add_url())
# Pack it below the entry
add_button.pack(pady=5)

# The button that opens all saved URLs in the browser
launch_button = ctk.CTkButton(setup1_frame, text="Launch", width=180,
                              hover_color="darkblue", command=lambda: launch())
# Pack it below the add button
launch_button.pack(pady=5)

# A scrollable area that lists all the saved URLs
url_view = ctk.CTkScrollableFrame(setup1_frame, width=380, height=300)
# Pack it below the buttons, letting it stretch and fill remaining space
url_view.pack(pady=10, padx=10, fill="both", expand=True)


# Called when the user clicks "Add URL" (or presses Enter in the entry).
def add_url():
    # Get the text and remove leading/trailing whitespace
    url = entry.get().strip()
    # If the box was empty (or only spaces), do nothing
    if not url:
        return
    # Auto-add https:// if the user forgot
    # startswith accepts a tuple — checks either "http://" OR "https://"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    # Add the (now safe) URL to our list
    urls.append(url)
    # Save the updated list to disk so it survives a restart
    save_urls(urls)
    # Clear the entry box so the user can type the next URL
    entry.delete(0, "end")
    # Rebuild the on-screen list so the new URL shows up
    refresh_url_list()


# Called when the user clicks "Launch" — opens every URL in the browser.
def launch():
    # If the list is empty, warn the user instead of doing nothing
    if not urls:
        messagebox.showerror("Nothing to launch", "Add at least one URL first.")
        return
    # Open each URL in a new browser tab
    for url in urls:
        webbrowser.open_new_tab(url)


# Called when the user clicks the "X" next to a URL row.
# "index" is the position in the list (0 = first, 1 = second, etc.)
def remove_url_at(index):
    # Remove the URL at the given position from the list
    urls.pop(index)
    # Save the updated (shorter) list to disk
    save_urls(urls)
    # Rebuild the on-screen list so the removed URL disappears
    refresh_url_list()


# Rebuild the entire URL list on screen from the "urls" list.
# This is called every time urls changes (add, remove, or at startup).
def refresh_url_list():
    # Clear old rows first — destroy every existing widget in the scrollable frame
    for widget in url_view.winfo_children():
        widget.destroy()

    # If there are no URLs, show a friendly "empty" message and stop
    if not urls:
        ctk.CTkLabel(url_view, text="No URLs added yet.",
                     text_color="gray").pack(pady=20)
        return

    # Loop through the list with an index (i) so each X button remembers its row
    for i, url in enumerate(urls):
        # A horizontal frame to hold the URL text + the X button
        url_frame = ctk.CTkFrame(url_view, fg_color="transparent")
        # Pack it to fill the row width
        url_frame.pack(pady=3, fill="x")

        # The URL text label, left-aligned
        url_label = ctk.CTkLabel(url_frame, text=url, anchor="w", wraplength=300)
        # Pack it on the left, expanding to fill the remaining space
        url_label.pack(side="left", padx=8, fill="x", expand=True)

        # The small "X" button to delete this specific URL row.
        # lambda idx=i captures the CURRENT index so each button knows its own row.
        delete_url_button = ctk.CTkButton(
            url_frame, text="X", width=28, height=28,
            fg_color="transparent", hover_color="darkred",
            command=lambda idx=i: remove_url_at(idx),
        )
        # Pack it on the right side of the row
        delete_url_button.pack(side="right", padx=5)


# Press Enter in the entry to add a URL
entry.bind("<Return>", lambda e: add_url())

# Show any saved URLs (or the empty-state message) when the app first opens
refresh_url_list()

# Start the app's main event loop — keeps the window open and responsive
root.mainloop()