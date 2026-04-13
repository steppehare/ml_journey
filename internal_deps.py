#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx==0.26.0",
#     "requests>=2.33.1"
# ]
# ///

import sys
import requests
import httpx

def main():
    print("Hello from ml-journey!")
    print("Python version:", sys.version)

    resp = requests.get(url='https://ifconfig.me/ip', verify=True)
    print(f"IP addr: {resp.text}")
    x_resp = httpx.get('https://ifconfig.me/forwarded')
    print(f'Forwarded: {x_resp.text}')

if __name__ == "__main__":
    main()
