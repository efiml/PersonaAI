import argparse
import requests
import time
import os
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm
import pyfiglet
import colorama
from colorama import Fore, Style
import re

# Constants
API_KEY_FILE = "apikey.txt"
KEY_FILE = "secret.key"
PSYCHO_PROFILE_URL = "https://irbis.espysys.com/api/developer/psycho_profile"
RESULTS_URL_TEMPLATE = "https://irbis.espysys.com/api/request-monitor/api-usage/{}?key={}"

# Function to generate a new encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, 'rb').read()

# Function to encrypt the API key
def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message

# Function to decrypt the API key
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

# Function to display the intro with ASCII art
def show_intro():
    ascii_art = pyfiglet.figlet_format("PersonaAI", font="slant")
    print(Fore.CYAN + ascii_art + Style.RESET_ALL)
    print(Style.BRIGHT + "Welcome to PersonaAI, your tool for generating AI-based psychological profiles.")
    print("To get started, please enter your IRBIS API key." + Style.RESET_ALL)

# Function to sanitize the API key for display
def sanitize_api_key(api_key):
    return f"${'*' * (len(api_key) - 5)}{api_key[-5:]}"

# Function to validate the API key
def validate_api_key(api_key, debug_mode=False):
    sanitized_key = sanitize_api_key(api_key)
    print(f"Validating API key: {sanitized_key}")
    response = requests.get(
        f"https://irbis.espysys.com/api/request-monitor/credit-stat?key={api_key}",
        headers={"Content-Type": "application/json"}
    )
    if debug_mode:
        print("Debug Mode: Response from API:")
        print(response.text)

    if response.status_code == 200:
        print("API key validated successfully.")
        return response.json()
    else:
        print(f"Error validating API key: {response.status_code} {response.text}")
        return None

# Function to validate Facebook ID
def validate_facebook_id(facebook_id):
    # Pattern for numeric ID (e.g., "100077649716158")
    numeric_pattern = re.compile(r'^\d+$')
    # Pattern for alphanumeric username with periods (e.g., "itaybar1", "eloy.simoesjr", "gwry.pwmrny.n.l.ymwz.whhzrh")
    username_pattern = re.compile(r'^[a-zA-Z0-9._-]+$')

    if numeric_pattern.match(facebook_id) or username_pattern.match(facebook_id):
        return True
    else:
        return False

# Function to get the stored API key
def get_stored_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'rb') as file:
            encrypted_key = file.read()
            try:
                return decrypt_message(encrypted_key)
            except Exception as e:
                print(f"Error decrypting API key: {e}")
                return None
    return None

# Function to store the API key
def store_api_key(api_key):
    encrypted_key = encrypt_message(api_key)
    with open(API_KEY_FILE, 'wb') as file:
        file.write(encrypted_key)
    print("API key encrypted and stored successfully.")

# Function to display account information
def display_account_info(account_info):
    balance = account_info["balance"]
    currency = account_info["currency"]
    credits = account_info["credits"]
    expiration_date = datetime.strptime(account_info["expiratioDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    status = account_info["status"]

    print(f"Balance: {balance} {currency}")
    print(f"Credits: {credits}")
    print(f"Expiration Date: {expiration_date}")
    print(f"Status: {status}")

# Function to display available commands
def display_command_options():
    print("\nAvailable Commands:")
    print("  -h            Help")
    print("  -k APIKEY     Replace API key")
    print("  -id FACEBOOK  Facebook ID to analyze")
    print("  -b            Check balance")
    print("  -d            Debug mode\n")

# Function to trigger the psycho profile lookup
def trigger_psycho_profile(api_key, facebook_id, debug_mode=False):
    payload = {
        "key": api_key,
        "lookupType": "PSYCH",
        "value": facebook_id,
        "lookupId": 180
    }

    response = requests.post(
        PSYCHO_PROFILE_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if debug_mode:
        print("Debug Mode: Response from API:")
        print(response.text)

    if response.status_code == 201:
        response_data = response.json()
        print(f"Profile lookup initiated. ID: {response_data.get('id')}")
        return response_data.get('id')
    else:
        print(f"Error initiating profile lookup: {response.status_code} {response.text}")
        return None

# Function to poll for results
import textwrap
import sys

def poll_for_results(api_key, lookup_id, debug_mode=False):
    url = RESULTS_URL_TEMPLATE.format(lookup_id, api_key)
    status = "progress"
    attempt_number = 1

    while status != "FINISHED":
        # Display attempt number before the progress bar
        print(f"Attempt {attempt_number} to recheck status:")
        
        for _ in tqdm(range(10), desc="", unit="s", leave=False):
            time.sleep(1)

        response = requests.get(url, headers={"Content-Type": "application/json"})
        if debug_mode:
            print("Debug Mode: Response from API:")
            print(response.text)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                status = data['data'][0]['status']
                if status == "FINISHED":
                    print("\nProfile analysis complete!")
                    print("Waiting 20 seconds before final retrieval...\n")
                    # Wait an additional 20 seconds before retrieving the final data
                    for _ in tqdm(range(20), desc="Finalizing", unit="s"):
                        time.sleep(1)
                    
                    # Retrieve the final data after the timeout
                    final_response = requests.get(url, headers={"Content-Type": "application/json"})
                    final_data = final_response.json()
                    
                    if 'data' in final_data and len(final_data['data']) > 0:
                        profile = final_data['data'][0]['psychAnalyst']['profiles'][0]
                        danger_level = profile['levelOfDanger'].split(",", 1)
                        danger_main = danger_level[0] if len(danger_level) > 0 else ""
                        danger_details = danger_level[1] if len(danger_level) > 1 else ""

                        formatted_output = f"""
################## Psychological Profile ##################
Name: {profile['personName']}

PsychoPortrait: {textwrap.fill(profile['psychologicalPortrait'], width=141)}

Level Of Danger: {danger_main}, {textwrap.fill(danger_details, width=141)}

Predicted Characteristics: {', '.join(profile['predictedCharacteristics'])}.
##########################################################
"""
                        print(formatted_output)
                    else:
                        print("Error: No data available in final retrieval. Please try again later.")
                    break
                else:
                    if debug_mode:
                        print("Profile analysis is still in progress...")
        elif response.status_code == 404:
            print("""
    ***********************************************
    *                                             *
    *  Error: Data not found or invalid request   *
    *                                             *
    ***********************************************
    """)
            break
        else:
            print(f"Error checking status: {response.status_code} {response.text}")

        attempt_number += 1

# Main function to handle CLI mode
def main():
    colorama.init(autoreset=True)
    show_intro()

    parser = argparse.ArgumentParser(description="PersonaAI Tool")
    parser.add_argument("-k", "--apikey", type=str, help="Your IRBIS API Key")
    parser.add_argument("-id", "--facebook", type=str, help="Facebook ID to analyze")
    parser.add_argument("-s", "--showkey", action="store_true", help="Show current API key")
    parser.add_argument("-b", "--balance", action="store_true", help="Check account balance")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.apikey:
        api_key = args.apikey
        account_info = validate_api_key(api_key, debug_mode=args.debug)
        if account_info:
            store_api_key(api_key)
            display_account_info(account_info)
        else:
            print("Invalid API key. Please try again.")
            return
    else:
        api_key = get_stored_api_key()
        if not api_key:
            api_key = input("Enter your API key: ")
            account_info = validate_api_key(api_key, debug_mode=args.debug)
            if account_info:
                store_api_key(api_key)
                display_account_info(account_info)
            else:
                print("Invalid API key. Please try again.")
                return
        else:
            account_info = validate_api_key(api_key, debug_mode=args.debug)
            if not account_info:
                print("Stored API key is invalid. Please run the script with a new API key using the -k option.")
                return
            display_account_info(account_info)

    if args.facebook:
        if validate_facebook_id(args.facebook):
            lookup_id = trigger_psycho_profile(api_key, args.facebook, debug_mode=args.debug)
            if lookup_id:
                poll_for_results(api_key, lookup_id, debug_mode=args.debug)
        else:
            print("Error: Invalid Facebook ID format. Please use a numeric ID or a valid username.")
    elif args.balance:
        print("Checking balance...")
        display_account_info(account_info)
    elif args.showkey:
        print(f"Current API key: {sanitize_api_key(api_key)}")
    else:
        display_command_options()

if __name__ == "__main__":
    main()
