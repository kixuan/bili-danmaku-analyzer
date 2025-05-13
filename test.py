import requests

def check_cookie(sessdata: str):
    url = "https://api.bilibili.com/x/web-interface/nav"
    cookies = {"SESSDATA": sessdata}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    response = requests.get(url, cookies=cookies, headers=headers)
    print("HTTP状态码:", response.status_code)
    print("响应内容:", response.json())

if __name__ == "__main__":
    sessdata = input("请输入SESSDATA: ").strip()
    check_cookie(sessdata)