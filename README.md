# Prerequisites
1. Python 3.8+ (See: https://youtu.be/i-MuSAwgwCU)
2. pip (Update pip to latest version if not updated)
3. Microsoft Build Tools (Download from: https://www.microsoft.com/en-us/download/details.aspx?id=48159)
4. Create virtual environment.

# Create Virtual Environment
To install requried packages, it is better to create virtual environment first:
1. Navigate to repo's folder.
2. Type `cmd` in window's path field.
3. In cmd, type `python -m venv <name_of_virtualenv>`.
4. Now, we need to activate our created virtual environment. In the same cmd window, type `<name_of_virtualenv>\Scripts\activate`.
5. Keep cmd window open.

<img src=".github\images\create_venv.gif">


# Install Requirements
After activating the created virtual environement, we need to install required packages found in `requirements.txt`:
1. In the same cmd window, type `pip install -r requirements.txt --no-cache-dir`
2. Wait untill all requried packages are installed.
3. Close cmd window.

<img src=".github\images\install_req.gif">

# Run App
Every time you need to run Saqer app, the created virtual environment needs to be activated first. (Apply step 1, 2 and 4 from `Create Virtual Environment` section):
1. After activating the virtual environment, type `python main.py` in cmd window.
2. Happy testing ༼ つ ◕_◕ ༽つ!

<img src=".github\images\run_app.gif">