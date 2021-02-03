import pyrebase
import json
import requests

username = "meow1@gmail.com"
password = "12345678901"

try:
    with open('../db/fbConfig.json') as file:
        config = json.load(file)
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    print(auth.sign_in_with_email_and_password(username, password))
except requests.exceptions.HTTPError as e:
    print(json.loads(e.args[1])["error"]["message"])
except Exception:
    print("Something went wrong! Could not login.")
