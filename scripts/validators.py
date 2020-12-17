import urllib.request
import sys
import ipaddress
from colors import bcolors

# check if the ipadress is valid


def ip_validator(ip_adress):
    try:
        ip_adress = ipaddress.ip_address(ip_adress)
        return str(ip_adress)
    except ValueError:
        print(f"{bcolors.WARNING}ERROR: Invalid IP4 adress.{bcolors.ENDC}")
        sys.exit()

# check if the url is returning something


def url_validator(ip_adress, port):

    if port.isnumeric() == True:
        pass
    else:
        print(f'{bcolors.WARNING}ERROR: Port should be a number.{bcolors.ENDC}')
        sys.exit()

    url = ("http://" + ip_adress + ":" + port)
    try:
        urllib.request.urlopen(url, timeout=2)
        return url
    except urllib.error.URLError:
        print(
            f"{bcolors.WARNING}ERROR: The IP adress/port are wrong or the device is not connected, try again.{bcolors.ENDC}")
        sys.exit()
