#!/bin/sh

pkg update && pkg upgrade -y && pkg install -y termux-api python git && termux-setup-storage && git clone https://github.com/kishore07-svg/test && cd test && pip install -q -r requirements.txt && chmod +x main.py && python main.py
