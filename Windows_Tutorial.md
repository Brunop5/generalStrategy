# How to Run the Python Project on Windows (Step‑by‑Step Guide)

This guide explains **everything from zero**. Follow the steps **in order**. Do not skip anything.

---

# 1. Preparation (Things You Must Install First)

## 1.1 Install Python

1. Open your web browser.
2. Go to: [https://www.python.org/downloads/](https://www.python.org/downloads/)
3. Click **Download Python**.
4. Run the downloaded file.

**VERY IMPORTANT:**

During installation:

* Check the box:

```
Add Python to PATH
```

Then click:

```
Install Now
```

When finished, click **Close**.

---

## 1.2 Install Visual Studio Code (VS Code)

1. Open browser.
2. Go to: [https://code.visualstudio.com/](https://code.visualstudio.com/)
3. Click **Download for Windows**.
4. Run the installer.
5. Keep clicking **Next**.

When you see additional tasks:

Enable:

```
Add "Open with Code" to Windows Explorer
Add to PATH
```

Finish installation.

---

## 1.3 Install Python Extension in VS Code

1. Open **VS Code**.
2. On the left side click the **Extensions icon** (looks like 4 squares).
3. Search:

```
Python
```

4. Install the extension made by **Microsoft**.

---

# 2. Opening the Project

## 2.1 Download or Copy the Project Folder (trading_bot)

Make sure you have the project folder on your computer.

Example:

```
C:\Users\YourName\Desktop\my_project
```

---

## 2.2 Open the Project in VS Code

1. Open **VS Code**.
2. Click:

```
File → Open Folder
```

3. Select the project folder.
4. Click **Select Folder**.

---

# 3. Opening the Terminal (Very Important)

The terminal is where you type commands.

In VS Code:

1. Top menu click:

```
Terminal → New Terminal
```

OR press:

```
CTRL + `
```

A panel will open at the bottom.

You should see something like:

```
PS C:\Users\YourName\Desktop\my_project>
```

If you see that — you did it correctly.

---

# 4. Create Virtual Environment and Install Dependencies

## 4.1 Create Virtual Environment

Copy and paste this into the terminal:

```
python -m venv venv
```

Wait until it finishes.

---

## 4.2 Activate Virtual Environment

Copy and paste:

```
venv\Scripts\activate
```

If it worked, you will see something like:

```
(venv) PS C:\Users\...
```

The `(venv)` means it is active.

---

## 4.3 Install All Dependencies

Copy and paste:

```
pip install -r requirements.txt
```

Wait. This can take several minutes.

Do **not** close VS Code during installation.

---

# 5. Editing the inputs

Find the main inputs file.

it is `FVG_projectX_bot/FVG_strategy.py`

open it, and there you can see the familiar inputs. 
ASSETS list and other main functionality inputs are on the top

The strategy inputs are below


### New additions:
```
# Partial close sizing and ATR steps
SPLIT_ORDERS_ENABLED = True        # If False, place a single order with FIXED_LOT
EACH_TRADE_SIZE = 1                # Size per child order when splitting FIXED_LOT
PARTIAL_TP_ATR_STEP = 1  # ATR step size for favorable partial closes
PARTIAL_SL_ATR_STEP = 2  # ATR step size for adverse partial closes
PARTIAL_TP_CLOSE_SIZE = 1  # Size to close per favorable step (multiple of EACH_TRADE_SIZE)
PARTIAL_SL_CLOSE_SIZE = 2  # Size to close per adverse step (multiple of EACH_TRADE_SIZE)
ENABLE_PARTIAL_TP = True
ENABLE_PARTIAL_SL = True

.
.
.

ALLOW_PYRAMIDING = True
PYR_ATR_STEP = 1.0     # after how many ATR upwards does it buy in
PYR_ADD_ON_SIZE = 1    # the amount of contracts it should buy in
PYR_MAX_ADDS = 10      # maximum amount of buy ins that can happen
```

If you dont understand any of these, dont hesitate and contact me

once you edit those, you HAVE TO press CTRL + S to save the changes, if you dont do that, the script will run with the old inputs
---


# 6. Running the main script

The main script to run is located in `FVG_projectX_bot/projectX/FVG_projectX.py`
WARNING: the script to run is not the same as the inputs script.

to run it copy and paste this into the terminal:

```
python -m FVG_projectX_bot.projectX.FVG_projectX
```
and press enter

if you want to stop the script, click on the terminal, and press CTRL + C (as if you wanted to copy something)
this will forcefully stop the script.


# 7. Every Time You Open the Project Again

You must do this **every time** before running the script.

Open terminal and run:

```
venv\Scripts\activate
```

Then run:

```
python -m FVG_projectX_bot.projectX.FVG_projectX
```

---


# 8. Some general info
- each ASSET triple will create a .json and .csv file in the root directory, 
so it is not suggested to have many running cause it will clog up the directory

- if you stopped the script, and want to restart it after a longer time (a Day for example),
it is suggested you delete the original csv and json files created before.

# 8. If Python Command Does Not Work

Try this instead when creating Virtual Enviroment:

```
py -m venv venv
```

Activate:

```
venv\Scripts\activate
```

Install:

```
py -m pip install -r requirements.txt
```

Run:

```
py main.py
```

---


# 8. Common Problems

## "python is not recognized"

Python was not added to PATH.

Fix:

* Reinstall Python
* Check **Add Python to PATH**

---

## Dependencies Fail to Install

Try upgrading pip:

```
python -m pip install --upgrade pip
```

Then again:

```
pip install -r requirements.txt
```

---

## Virtual Environment Not Activating

Make sure you are inside the project folder.

You should see the `venv` folder in the left file list.

---

# 9. What NOT To Do

Do NOT:

* Move files inside the project
* Rename folders
* Delete the `venv` folder
* Close VS Code during installation

---

# 10. Quick Checklist

If something does not work, check:

* Python installed
* VS Code installed
* Python extension installed
* Project folder opened
* Terminal open
* Virtual environment activated 
* Dependencies installed

If all are true — the project should run.
