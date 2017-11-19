import os
import re
import json
import random
import getpass

class pin_login(object):
    """docstring for pin_login"""
    def __init__(self):
        self.store_path = self._get_store_path()
        self.login_verify_method = None

    def get_login(self, destination):
        # try to read encoded login info
        with open(self.store_path) as psw_bin:
            login_info = json.loads(psw_bin.read())

        if destination in login_info:
            username, password = self.load_login_info(destination, login_info)
        else:
            # first time to login / no saved information
            username = raw_input("User name: ")
            password = getpass.getpass("Password:  ")
            if self.try_login(username, password):
                self.ask_for_saving_psw(destination, username, password)
        return username, password

    def ask_for_saving(self, destination, username, password):
        while True:
            saving_option = raw_input("Do you want to save your login information by pin code? [Y/N]")
            if saving_option.lower() == "y":
                self.save_login_info(destination, username, password)
            else:
                break

    def save_login_info(self, destination, username, password):
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
            login_info[destination] = {"Username":username,"Password":encoded_psw}
            psw_bin.write(json.dumps(login_info, indent=4))
            


    def load_login_info(self, destination, login_info):
        pin = raw_input("Please enter 4 digit pin code:")
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
    decoded_ascii = [rev_map.index(c) for c in enc_code]
    decoded_msg = "".join([chr(n) for n in decoded_ascii]) 
    return decoded_msg
