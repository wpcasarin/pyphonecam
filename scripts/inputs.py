import subprocess
import sys
import os.path
from colors import bcolors

valid_inputs = ("y", "Y", "n", "N", "q", "Q")
quit_inputs = ("q", "Q")
yes_inputs = ("y", "Y")
no_inputs = ("n", "N")

v4l2_cmd = (
    "sudo modprobe v4l2loopback exclusive_caps=1 video_nr=1  card_label='PhoneCam'")

# simple exit function
def simple_exit():
    print(f"{bcolors.BOLD}Script finished.{bcolors.ENDC}")
    sys.exit()

# setup v4l2loopback and return the device index
def inputs():
    while True:
        resp = input(
            f"Do you have already setup v4l2loopback? {bcolors.BOLD}[Y/N]{bcolors.ENDC} -> ")
        if resp in quit_inputs:
            simple_exit()
        elif resp not in valid_inputs:
            print(
                f"{bcolors.WARNING}ERROR: Invalid input try again or press 'Q' to exit{bcolors.ENDC}")
        elif resp in yes_inputs:
            while True:
                resp = input("Enter the device index number: ")
                if resp in quit_inputs:
                    simple_exit()
                elif resp.isnumeric() == False:
                    print(
                        f"{bcolors.WARNING}ERROR: The index should be a number.{bcolors.ENDC}")
                else:
                    v_index = str(resp)
                    if os.path.exists(f'/dev/video{v_index}') == True:
                        return v_index
                    print(
                        f"{bcolors.WARNING}ERROR: Device not found, try again or press 'Q' to exit.{bcolors.ENDC}")
        elif resp in no_inputs:
            v_index = ('1')
            subprocess.check_output(v4l2_cmd, shell=True)
            if os.path.exists(f'/dev/video{v_index}') == True:
                return v_index
            print(f"{bcolors.WARNING}ERROR: Device not found.{bcolors.ENDC}")
            sys.exit()
