# This script is inspired by ippsec and his video(https://www.youtube.com/watch?v=aG_N2ZiCfxk&t=2419s&ab_channel=IppSec)
# The output be like `developer:sha256:50000:i/PjRSt4VE+L7pQA1pNtNA==:5THTmJRhN7rqcO1qaApUOF7P8TEwnAvY8iXyhEBrfLyO/F2+8wvxaCYZJjRE6llM+1Y=` and you should only need the latter [username:hash].
# Command:hashcat -m 10900 hash.txt /usr/share/wordlists/rockyou.txt

import sqlite3
import base64
import sys

def get_user_data(db_file):
    try:
        with sqlite3.connect(db_file) as con:
            cursor = con.cursor()
            cursor.execute("SELECT name, passwd_hash_algo, salt, passwd FROM user")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)

def process_user_data(row):
    if "pbkdf2" in row[1]:
        _, iterations, keylen = row[1].split("$")
        algo = "sha256"
        name = row[0]
    else:
        raise Exception("Unknown Algorithm")
    
    salt = bytes.fromhex(row[2])
    passwd = bytes.fromhex(row[3])
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    passwd_b64 = base64.b64encode(passwd).decode("utf-8")
    
    return f"{name}:{algo}:{iterations}:{salt_b64}:{passwd_b64}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gitea2hashcat.py <gitea.db>")
        sys.exit(1)

    db_file = sys.argv[1]
    
    user_data = get_user_data(db_file)

    for row in user_data:
        try:
            output = process_user_data(row)
            print(output)
        except Exception as e:
            print(f"Error processing user data: {e}")

if __name__ == "__main__":
    main()
