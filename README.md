# Typing Assistant

Here is a cross-platform Python script for auto keyboard-typing. It uses a SQLite database (`data.db`) to retrive key-value pairs. You can save these key-value pairs in the table named `snippet` in `data.db` file and automatically write the values anywhere using `key=` or `key+F8` shortcuts.

**Example:** If you save `hw` as key and `Hello World!` as value in snippet table and type `hw=`, it will write `Hello World!` in whatever text input you focus on any program.

# Installation

After cloning the repo:

`pip install -r requirements.txt`
<br> or <br>
`python -m pip install -r requirements.txt`

You need python and pip pre-installed obviously.

# Run

`python main.py`

# Save

Open `data.db` file with any SQLite viewer or driver and add new rows to `snippet` table.
Remember, key must be alphanumeric `a-z, A-Z, 0-9`.

# Exit

To stop the program gracefully, you have to press in sequence: `Ctrl`+`Shift`+`C`.