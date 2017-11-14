import os
import random
import json

class pin_login(object):
    """docstring for pin_login"""
    def __init__(self, arg):
        self.msg_path = self._get_msg_path()

    def encode(self, pin, msg):
        random.seed(pin)
        encode_map = [i for i in range(127)]
        random.shuffle(encode_map)
        ascii_code = [encode_map[ord(c)] for c in msg]
        return ascii_code

    def decode(self, pin, enc_msg):
        random.seed(pin)
        rev_map = [i for i in range(127)]
        random.shuffle(rev_map)
        decoded_ascii = [rev_map.index(c) for c in enc_code]
        decoded_msg = "".join([chr(n) for n in decoded_ascii]) 
        return decoded_msg

    def save_login_info(self):
        enc_password, self.encode()

    def load_login_info(self):
        pass

    def _get_msg_path():
        home = os.path.expanduser('~')
        if not os.path.exists(home+"/.config/"):
            os.mkdir(home+'/.config/')
        if not os.path.exists(home+"/.config/save-login/"):
            os.mkdir(home+'/.config/save-login/')
        if not os.path.exists(home+"/.config/save-login/login_msg.json"):
            os.mknod(home+"/.config/save-login/login_msg.json", 0600)
        return home+"/.config/save-login/login_msg.json"

if __name__ == '__main__':
    enc = encode('0213', 'h39rhvi2')
    print enc

    print decode('0213', enc)
