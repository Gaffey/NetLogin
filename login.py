#!/bin/python

import requests, sys, json, argparse, hashlib

logout_payload = {"action":"logout"}

url = "https://net.tsinghua.edu.cn/do_login.php"

def store(data):
    with open('config.json', 'w') as json_config:
        json_config.write(json.dumps(data))

def load():
    with open('config.json') as json_config:
        data = json.load(json_config)
        return data

def md5(data):
    md5_func = hashlib.md5(data)
    return md5_func.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help="Choose login/logout", default="login")
    parser.add_argument('--username', help="Input your username. if no username specify, use last one", default="")
    parser.add_argument('--password', help="Input your password. if no password specify, use last one", default="")
    args = parser.parse_args()
    if args.action == "login":
        login_payload = load()
        rewrite = False
        if args.username:
            login_payload["username"] = args.username
            rewrite = True
        if args.password:
            login_payload["password"] = "{MD5_HEX}" + md5(args.password)
            rewrite = True
        conn = requests.post(url, data=login_payload)
        print(conn.text)
        if conn.text == "Login is successful." and rewrite:
            store(login_payload)
    elif args.action == "logout":
        conn = requests.post(url, data=logout_payload)
        print(conn.text)

if __name__ == "__main__":
    main()