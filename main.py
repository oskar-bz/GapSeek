import os
import json

import requests
from urllib.parse import urlparse

API_URL = "https://arxiv.org/api"
CONFIG_PATH = os.path.abspath(os.path.dirname(__file__)) + "/.gapseek"
config = {};

def query_arxiv(queries: list[str]):
    params = "all:"+queries.join("+AND+all:")
    print(params)

def get_config():
    if os.path.isfile(CONFIG_PATH):
        return json.load(open(CONFIG_PATH))
    else:
        return {}

def save_config():
    with open(CONFIG_PATH, "w") as f:
        f.write(json.dumps(config)); 

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False

def change_endpoint():
    url = ""
    while not validate_url(url):
        url = input("API endpoint: ")
    config["endpoint"] = url

def change_provider():
    answer = "";
    while answer != "o" and answer != "j":
        answer = input("Choose your Provider, Ollama (o) or Jan (j): ")
        
    config["provider"] = "ollama" if answer == "o" else "jan"

def change_model():
    models = []
    # get available models
    if config["provider"] == "ollama":
        pass
    elif config["provider"] == "jan":
        trying = True
        while trying:
            req = requests.get(config["endpoint"]+"/v1/models")
            if req.status_code == 200: 
                json = req.json()
                for key in json["data"]:
                    if key.get("status") != None and key["status"] == "downloaded":
                        models.append(key["id"])
                break
            else:
                print("Connection failed!");
                ac = input("Change endpoint (y), try again (n) or quit(q): ")
                if ac == "y":
                    change_endpoint()
                elif ac == "q":
                    exit(-1)
        
    # let user choose a model
    print("Choose an available model:")
    for i, m in enumerate(models):
        print(str(i) + ":", m)
    num = -1
    while num < 0 or num > len(models)-1:
        num = int(input("(0-"+ str(len(models)-1) +")> "))

    config["model"] = models[num]

def main():
    global config
    config = get_config()
    print("# GapSeek\n---------------")
    if config.get("provider") == None:
        print("Setup:")

        change_provider()
        change_endpoint()
        change_model()

    else:
        while True:
            print("Provider: " + config["provider"])
            print("API endpoint: " + config["endpoint"])
            print("Model: " + config["model"])
            actions = ["a", "cm", "ce", "cp", ""]
            print("---------------")
            action = "."
            while not (action in actions):
                action = input("You can now accept (a), Change the model (cm), change the endpoint (ce) or change the provider (cp): ")
            
            if action == "cm":
                change_model()
            elif action == "ce":
                change_endpoint()
            elif action == "cp":
                change_provider()
            else:
                break
        
    print("servus")
    save_config()

if __name__ == "__main__":
    main()
