import subprocess
import sys

#var = subprocess.Popen('sudo pacman -Syu', shell=True)

#var = subprocess.check_output('sudo modprobe v4l2loopback exclusive_caps=1  card_label="PyPhoneCam"', shell=True)

#print('VAR ->>>>',var)

v_index = None

while True:
    resp = input("Do you have v4l2loopback already setup? [y/N] -> ")
    if resp not in ("n", "y", "q", "N", "Y", "Q"):
        print("Invalid input try again or press 'q' do exit.")
    if resp in ("q", "Q"):
        print("Exited successfully.")
        sys.exit()
    if resp in ("y", "Y"):
        while True:
            v_index = input("Enter the v4l2loopback device index: ")
            if v_index.isnumeric():
                break
            else:
                print("Invalid index, try again.")
        break

print(v_index)
