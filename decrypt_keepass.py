#!/usr/bin/env python3 

from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError
import sys

KDBX_FILE = 'recovery.kdbx'
WORDLIST = '/usr/share/wordlists/rockyou.txt'

try:
    with open(WORDLIST, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            password = line.strip()
            try:
                kp = PyKeePass(KDBX_FILE, password=password)
                print(f'\n[+] Password found: {password}')
                print('[+] Dumping entries:\n')
                for entry in kp.entries:
                    print(f' - {entry.title}: {entry.username} / {entry.password}')
                break
            except CredentialsError:
                continue
except FileNotFoundError:
    print(f'[!] File not found: {WORDLIST}')
    sys.exit(1)
