import argparse
from webdriver_work import GosUslugi


if __name__ == '__main__':
    gosuslugi = argparse.ArgumentParser(description='some description')
    gosuslugi.add_argument('-login', '--login')
    gosuslugi.add_argument('-password', '--password')
    args = gosuslugi.parse_args()

    login = args.login
    password = args.password
    if login and password:
        gos = GosUslugi(login, password)
        gos.run()