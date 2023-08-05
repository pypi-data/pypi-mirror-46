#!/usr/bin/env python3

import argparse
import re
import sys
import requests


def getID(username):
    url = "https://www.instagram.com/{}"

    r = requests.get(url.format(username))

    html = r.text

    if r.ok:
        return re.findall('"id":"(.*?)",', html)[0]

    else:
        print("\033[91m✘ Invalid username\033[0m")
        sys.exit()


def fetchDP(userID):
    url = "https://i.instagram.com/api/v1/users/{}/info/"

    r = requests.get(url.format(userID))

    if r.ok:
        data = r.json()
        return data['user']['hd_profile_pic_url_info']['url']

    else:
        print("\033[91m✘ Cannot find user ID \033[0m")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(
        description="Download any users Instagram display picture/profile picture in full quality")

    parser.add_argument('username', action="store", help="username of the Instagram user")

    args = parser.parse_args()

    username = args.username

    user_id = getID(username)
    file_url = fetchDP(user_id)
    fname = username + ".jpg"

    r = requests.get(file_url, stream=True)
    if r.ok:
        with open(fname, 'wb') as f:
            f.write(r.content)
            print("\033[92m✔ Downloaded:\033[0m {}".format(fname))
    else:
        print("Cannot make connection to download image")


if __name__ == "__main__":
    main()
