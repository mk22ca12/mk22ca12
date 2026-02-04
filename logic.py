import os
import json

# 1. Φόρτωση δεδομένων παιχνιδιού
with open('connect4.json', 'r') as f:
    data = json.load(f)

grid = data['grid']
turn = data['turn']

# 2. Λήψη κίνησης από το GitHub Issue (π.χ. "Connect4: 3")
issue_title = os.getenv('ISSUE_TITLE', '')
try:
    column = int(issue_title.split(':')[-1].strip()) - 1
except:
    print("invalid move")
    exit(1)

# 3. Λογική πτώσης μάρκας
for row in reversed(range(6)):
    if grid[row][column] == 0:
        grid[row][column] = turn
        break
else:
    exit(1) # Στήλη γεμάτη

# 4. Μετατροπή του grid σε Emojis για το README
emoji_map = {0: "⚪", 1: "🔴", 2: "🟡"}
board_html = "<table>"
for row in grid:
    board_html += "<tr>"
    for cell in row:
        board_html += f"<td>{emoji_map[cell]}</td>"
    board_html += "</tr>"
board_html += "</table>"

# 5. Ενημέρωση του README.md
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

start_marker = ""
end_marker = ""

# Αντικαθιστούμε ό,τι υπάρχει ανάμεσα στα markers με το νέο board
new_readme = readme.split(start_marker)[0] + start_marker + "\n" + board_html + "\n" + end_marker + readme.split(end_marker)[1]

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)

# 6. Αποθήκευση νέας κατάστασης
data['turn'] = 2 if turn == 1 else 1
data['grid'] = grid
with open('connect4.json', 'w') as f:
    json.dump(data, f)
