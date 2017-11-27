import os
import re
import sys
import json
import random
import getpass

class pin_login(object):
    """docstring for pin_login"""
    def __init__(self, login_verify_method=None):
        self.store_path = self._get_store_path()
        self.login_verify_method = login_verify_method
        self.max_try = 3

    def get_login(self, destination):
        # try to read encoded login info
        with open(self.store_path, 'r') as psw_bin:
            login_info = json.loads(psw_bin.read())

        if destination in login_info:
            username, password = self.pin_login(destination, login_info)
        else:
            username, password = self.normal_login(destination)

        return username, password

    def normal_login(self, destination):
        # first time to login / no saved information
        error_count = 0
        while error_count < self.max_try:
            username = raw_input("User name: ")
            password = getpass.getpass("Password:  ")
            if self._try_login(username, password):
                self._ask_for_saving_psw(destination, username, password)
                return username, password
            else:
                print "User name or password incorrect."
                error_count += 1
        else:
            raise KeyError("Exceed maximum attempt.")

    def pin_login(self, destination, login_info):
        error_count = 0
        while error_count < self.max_try:
            username, password = self._load_login_info(destination, login_info)
            if self._try_login(username, password):
                return username, password
            else:
                print "Pin incorrect or password changed."
                error_count += 1
        else:
            reset_option = raw_input("Do you want to remove pin?(Y/N)")
            if reset_option.lower() == "y":
                self.reset_pin(destination)
            else:
                raise KeyError("Exceed maximum attempt.")

    def reset_pin(self, destination):
        with open(self.store_path, 'r') as psw_bin:
            login_info = json.loads(psw_bin.read())

        _ = login_info.pop(destination, None)

        with open(self.store_path, 'w') as psw_bin:
            psw_bin.write(json.dumps(login_info, indent=4))
        print "Pin has been removed."
        sys.exit()
        

    def _ask_for_saving_psw(self, destination, username, password):
        saving_option = raw_input("Do you want to save your login information by pin code?(Y/N) ")
        if saving_option.lower() == "y":
            self._save_login_info(destination, username, password)

    def _save_login_info(self, destination, username, password):
        while True:
            pin = getpass.getpass("Please enter 4 digit pin code(number only):")
            if not pin.isdigit():
                print "Please enter number."
                continue
            elif len(pin) != 4:
                print "Please enter 4 digit number."
                continue
            pin_check = getpass.getpass("Please enter pin code again:")
            if pin_check != pin:
                print "Not the same pin code, please try again."
            else:
                break

        encoded_psw = encode(pin, password)

        with open(self.store_path, 'r') as psw_bin:
            login_info = json.loads(psw_bin.read())

        with open(self.store_path, 'w') as psw_bin:
            # over write the login information if it has been exist.
            login_info[destination] = {"Username":username,"Password":encoded_psw}
            psw_bin.write(json.dumps(login_info, indent=4))
            


    def _load_login_info(self, destination, login_info):
        pin = getpass.getpass("Please enter 4 digit pin code:")
        username = login_info[destination]["Username"]
        password = decode(pin, login_info[destination]["Password"])
        return username, password
        
    def _try_login(self, username, password):
        if self.login_verify_method:
            login_result = self.login_verify_method(username, password)
            if isinstance(type(login_result), bool):
                raise TypeError("The login verify method does not return boolean.")
            else:
                return login_result
        else:
            return True

    def _get_store_path(self):
        home = os.path.expanduser('~')
        if not os.path.exists(home+"/.config/"):
            os.mkdir(home+'/.config/')
        if not os.path.exists(home+"/.config/save-login/"):
            os.mkdir(home+'/.config/save-login/')
        if not os.path.exists(home+"/.config/save-login/login_msg.json"):
            with open(home+"/.config/save-login/login_msg.json", "w") as psw_bin:
                psw_bin.write("{}")
        return home+"/.config/save-login/login_msg.json"

# --------------------------

def encode(pin, message):
    """Encode the message with pin coed.
    
    Arguments:
        pin {str} -- using this as seed to generate ascii map.
        message {str} -- the message wants to encrypt.
    
    Returns:
        [list] -- a list of swapped ascii number.
    """
    random.seed(pin)
    encode_map = [i for i in range(127)]
    random.shuffle(encode_map)
    ascii_code = [encode_map[ord(c)] for c in message]
    return ascii_code

def decode(pin, enc_msg):
    """Decode the encrypted message by pin code.
    
    Arguments:
        pin {str} -- sing this as seed to generate ascii map.
        enc_msg {str} -- the message wants to be decode.
    
    Returns:
        [str] -- decoded message
    """
    random.seed(pin)
    rev_map = [i for i in range(127)]
    random.shuffle(rev_map)
    decoded_ascii = [rev_map.index(c) for c in enc_msg]
    decoded_msg = "".join([chr(n) for n in decoded_ascii]) 
    return decoded_msg
