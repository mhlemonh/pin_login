import pin_login

def check_login(username, password):
    if username == "admin" and password == "admin":
        return True
    else:
        return False

if __name__ == '__main__':
    pl = pin_login.pin_login(check_login)
    pl.get_login("FTP")

