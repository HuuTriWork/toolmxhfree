import os
import sys
import time
import json
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Đang cài đặt module '{package}' ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

for module in ["requests"]:
    install_and_import(module)

import requests

def get_token():
    token_file = "api_token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()
            if token:
                return token
            
    token = input("Nhập API Token (lấy tại https://like.vn/docs/api): ").strip()
    with open(token_file, "w") as f:
        f.write(token)
    return token

services = {
    "1": {
        "name": "Views TikTok",
        "url": "https://like.vn/api/mua-view-tiktok/order",
        "data": {"server_order": "4", "giftcode": "", "amount": "1000", "note": ""}
    },
    "2": {
        "name": "Like TikTok",
        "url": "https://like.vn/api/mua-like-tiktok/order",
        "data": {"server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    },
    "3": {
        "name": "Follow TikTok",
        "url": "https://like.vn/api/mua-follow-tiktok/order",
        "data": {"server_order": "5", "giftcode": "", "amount": "10", "note": ""}
    },
    "4": {
        "name": "Like Instagram",
        "url": "https://like.vn/api/mua-like-instagram/order",
        "data": {"server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    },
    "5": {
        "name": "Follow Facebook Cá Nhân",
        "url": "https://like.vn/api/mua-follow-facebook/order",
        "data": {"server_order": "7", "giftcode": "", "amount": "10", "note": ""}
    },
    "6": {
        "name": "Like & Follow Fanpage Facebook",
        "url": "https://like.vn/api/mua-like-fanpage-facebook/order",
        "data": {"server_order": "6", "giftcode": "", "amount": "10", "note": ""}
    }
}

def main():
    token = get_token()
    os.system("cls" if os.name == "nt" else "clear")
    print("\nDanh sách dịch vụ miễn phí:")
    for key, svc in services.items():
        print(f"{key}. {svc['name']}")

    choice = input("Chọn dịch vụ (1-6): ").strip()
    if choice not in services:
        print("Lựa chọn không hợp lệ!")
        return

    link = input("Nhập link: ").strip()

    svc = services[choice]
    url = svc["url"]
    data = svc["data"].copy()
    data["objectId"] = link
    amount = int(data["amount"])  

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "Origin": "https://like.vn",
        "Referer": "https://like.vn/",
        "api-token": token
    }

    print("\nBắt đầu chạy dịch vụ:", svc["name"])
    print("Nhấn Ctrl + C để dừng\n")

    success_count = 0
    total_buff = 0

    try:
        while True:
            try:
                r = requests.post(url, headers=headers, data=data)
                resp = {}
                try:
                    resp = r.json()
                except json.JSONDecodeError:
                    pass

                if resp.get("status") == "success":
                    success_count += 1
                    total_buff += amount
                    status = "Thành công"
                elif resp.get("status") == "error":
                    status = "Đang delay"

                print(f"Status: {status} | Thành công: {success_count} | Tổng: {total_buff}")

            except Exception as e:
                print("Lỗi request:", e)

            time.sleep(120)  

    except KeyboardInterrupt:
        print("\nĐã dừng.")


if __name__ == "__main__":
    main()
