import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
LAST_MESSAGE_ID = None


def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        # this shows how to use the .get() method to get specifically the messages but there is more you can do (hint: sample.json)
        return response.json().get("response", {}).get("messages", [])
    return []

def get_dad_joke():
    print("here")
    joke_url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "text/plain"}
    response = requests.get(joke_url, headers=headers)
    print(response.text)

    if response.status_code == 200:
        return response.text
    else:
        return "Sorry, I couldn't fetch a dad joke at the moment."

def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    

    sender_user_id = str(message.get("user_id"))
    sender_user_name = str(message.get("name"))
    
    
    if sender_user_id == "87796592":
        text = message["text"].lower()

        #Checks if the message is "hello bot"
        if "hello bot" == text:
            send_message("sup")
        elif "good morning" in text:
            send_message(f"good morning, {sender_user_name}")
        elif "good night" in text:
            send_message(f"good night, {sender_user_name}")
        elif "tell me a joke" in text:
            dad_joke = get_dad_joke()
            print(dad_joke)
            send_message(dad_joke)
    elif sender_user_id != None and str(message.get("sender_type")) == "user":
        text = message["text"].lower()
        if sender_user_id != None:
            if "good morning" in text:
                send_message(f"good morning, {sender_user_name}")
            elif "good night" in text:
                send_message(f"good night, {sender_user_name}")
            
    print(message)
    LAST_MESSAGE_ID = message["id"]


def main():
    global LAST_MESSAGE_ID
    try:
    # this is an infinite loop that will try to read (potentially) new messages every 10 seconds, but you can change this to run only once or whatever you want
        while True:
            messages = get_group_messages(LAST_MESSAGE_ID)
            for message in (messages):
                process_message(message)
                break
            
            time.sleep(3)
    except KeyboardInterrupt:
        LAST_MESSAGE_ID = None
        print("Script interrupted. LAST_MESSAGE_ID reset to None.")


if __name__ == "__main__":
    main()
