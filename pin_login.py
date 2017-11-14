import os
import json
import random
import getpass

class pin_login(object):
    """docstring for pin_login"""
    def __init__(self, arg):
        self.store_path = self._get_store_path()
        self.login_verify_method = None

    def get_login(self, destination):
        # try to read encoded login info
        with open(self.store_path) as stored_info:
            login_info = json.loads(stored_info.read())

        if destination in login_info:
            username, password = self.load_login_info(destination, login_info)
        else:
            # first time to login / no saved information
            username = raw_input("User name: ")
            password = getpass.getpass("Password:  ")
            if self.try_login(username, password):
                self.save_login_info()

    def save_login_info(self):
        choice = raw_input("Do you want to save login information with 4 digit pin code? [Y/N]")
        enc_password, self.encode()

    def load_login_info(self, destination, login_info):
        pin = raw_input("Please enter 4 digit pin code:")
        username = login_info[destination]["Username"]
        password = decode(pin, login_info[destination]["Password"])
        return username, password
        
    def _try_login(self, username, password):
        if self.login_verify_method
            login_result = self.login_verify_method(username, password)
            if isinstance(type(login_result), bool):
                raise TypeError("The login verify method does not return boolean.")
            else:
                return login_result
        else:
            return True

    def _get_store_path():
        home = os.path.expanduser('~')
        if not os.path.exists(home+"/.config/"):
            os.mkdir(home+'/.config/')
        if not os.path.exists(home+"/.config/save-login/"):
            os.mkdir(home+'/.config/save-login/')
        if not os.path.exists(home+"/.config/save-login/login_msg.json"):
            os.mknod(home+"/.config/save-login/login_msg.json", 0600)
        return home+"/.config/save-login/login_msg.json"

# --------------------------

def encode(pin, msg):
    random.seed(pin)
    encode_map = [i for i in range(127)]
    random.shuffle(encode_map)
    ascii_code = [encode_map[ord(c)] for c in msg]
    return ascii_code

def decode(pin, enc_msg):
    random.seed(pin)
    rev_map = [i for i in range(127)]
    random.shuffle(rev_map)
    decoded_ascii = [rev_map.index(c) for c in enc_code]
    decoded_msg = "".join([chr(n) for n in decoded_ascii]) 
    return decoded_msg

if __name__ == '__main__':
    pass
