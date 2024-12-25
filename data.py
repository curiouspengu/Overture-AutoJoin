import json
import requests
from collections import deque
from tkinter import messagebox
import random
from time import sleep
import webbrowser
import datetime
import re
import os
import sys

config = {}

def read_config():
    config_name = 'config.json'

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(application_path, config_name)
    global config
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

def main():
    read_config()
    global config
    if config["extremely fast autojoin (dangerous)"] == "1":
        messagebox.showwarning(title="Warning!", message="You have enabled Extremely Fast Autojoin!\nThis option may lock or even ban your discord account!\nExit the program if you do not wish to continue!")
    elif config["faster autojoin (may be dangerous)"] == "1":
        messagebox.showwarning(title="Warning!", message="You have enabled Faster Autojoin!\nThis option may lock your discord account!\nExit the program if you do not wish to continue!")

    
    messages = deque()
    if not config["authorization_key"]:
        messagebox.showerror(title="Error!", message="Authorization Key Empty!\nGo to the Github README for instructions to get one.")
        exit(1)

    try:
        channel_id = re.search("[0-9]+/?$", config["discord_channel_link"]).group(0)
    except:
        messagebox.showerror(title="Error!", message="Discord Channel Link Empty!")
        exit(1)

    print("""Just to let you know that you can donate here:
https://www.roblox.com/games/5080477735/Donations-to-Curious-Pengu#!/store
I'm not forcing you to donate, but at the end of the day most of Radiant Team's products will be completely free, so donations of any size and shape are greatly appreciated.
""")
    sleep(5)
    print("RUNNING | CLOSE THIS WINDOW TO EXIT")
    sp()
    while True:
        response = requests.request("GET",
            url=f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=1",
            headers={
                'Accept': 'application/json',
                'Authorization': config["authorization_key"]
            }
        )

        try:
            response = response.json()
            if response == None:
                messagebox.showerror("ERROR!", "This is usually caused by the authentication key timing out. Try refreshing the authentication key.")
            if not type(response) == list and response["message"] == "401: Unauthorized":
                messagebox.showerror("ERROR!", "This is usually caused by the authentication key timing out. Try refreshing the authentication key.")
            
            message = response[0]
            
            if message["id"] in messages:
                sleep_function()
                continue
            else:
                messages.append(message["id"])
            link = re.findall(r'(https?://[^\s]+)', message["content"])[0]
            
            timestamp = datetime.datetime.fromisoformat(message["timestamp"])
            duration = datetime.datetime.now(datetime.timezone.utc) - timestamp
            duration_in_s = duration.total_seconds()
            if divmod(duration_in_s, 3600)[0] < 1:
                if divmod(duration_in_s, 60)[0] < 4:
                    if "https://www.roblox.com/games/15532962292/Sols-RNG-Eon1-1?privateServerLinkCode=" in link:
                        join_ps_link(link)
                    else:
                        print("In regards to the current crosswood situation, we have disabled all links that aren't sols rng links.")

            while len(messages) > 10:
                messages.popleft()
        except Exception as e:
            if config["debug_mode"] == 1:
                print(f"Error! Discord API Responded with: [{response}]")
                print("Exception: ", e)
            else:
                print("Error!")
        sleep_function()
        
def sleep_function():
    if config["extremely fast autojoin (dangerous)"] == "1":
        pass
    elif config["faster autojoin (may be dangerous)"] == "1":
        sleep(1)
    elif config["slower_autojoin (may be safer)"] == "1":
        sleep(10)
    else:
        sleep(5)

def sp():
    if random.randint(1, 10) == 10:
        webbrowser.open("https://www.roblox.com/games/5080477735/Donations-to-Curious-Pengu#!/store")

def join_ps_link(link):
    webbrowser.open(link)

if __name__ == "__main__":
    main()
