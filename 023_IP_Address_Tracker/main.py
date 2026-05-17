# =========================================
# 023_IP_Address_Tracker
# =========================================

import requests
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.CYAN + """
==================================
        IP ADDRESS TRACKER
==================================
""")

ip = input(Fore.YELLOW + "Enter IP Address: ")

try:
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "success":
        print(Fore.GREEN + "\n[+] IP Information Found\n")

        print(Fore.WHITE + f"IP Address   : {data.get('query')}")
        print(Fore.WHITE + f"Country      : {data.get('country')}")
        print(Fore.WHITE + f"Region       : {data.get('regionName')}")
        print(Fore.WHITE + f"City         : {data.get('city')}")
        print(Fore.WHITE + f"ZIP Code     : {data.get('zip')}")
        print(Fore.WHITE + f"Latitude     : {data.get('lat')}")
        print(Fore.WHITE + f"Longitude    : {data.get('lon')}")
        print(Fore.WHITE + f"Timezone     : {data.get('timezone')}")
        print(Fore.WHITE + f"ISP          : {data.get('isp')}")
        print(Fore.WHITE + f"Organization : {data.get('org')}")
        print(Fore.WHITE + f"AS Number    : {data.get('as')}")

    else:
        print(Fore.RED + "\n[-] Invalid IP Address or Data Not Found")

except Exception as e:
    print(Fore.RED + f"\n[ERROR] {e}")