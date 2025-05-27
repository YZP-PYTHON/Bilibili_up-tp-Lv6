import requests
import json
import time
import qrcode
class login:
    def generate_bilibili_qrcode():
        """
        请求Bilibili二维码生成接口
        返回: 包含二维码URL和token的字典
        """
        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/generate"
        
        # 添加必要的headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Origin": "https://www.bilibili.com"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            
            data = response.json()
            if data.get("code") == 0:
                return {
                    "qrcode_url": data["data"]["url"],
                    "qrcode_key": data["data"]["qrcode_key"]
                }
            else:
                print(f"请求失败: {data.get('message', '未知错误')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求发生错误: {e}")
            return None
        except json.JSONDecodeError:
            print("解析响应数据失败")
            return None

    def poll_login_status(qrcode_key):
        """
        轮询扫码登录状态
        :param qrcode_key: 二维码key
        :return: 登录成功返回cookies，失败返回None
        """
        url = "https://passport.bilibili.com/x/passport-login/web/qrcode/poll"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
        }
        
        params = {
            "qrcode_key": qrcode_key
        }
        
        print("\n请使用B站APP扫描二维码...")
        print("等待扫码确认...")
        
        while True:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data["code"] == 0:
                    if data["data"]["code"] == 0:
                        print("\n登录成功！")
                        # 返回cookies和登录信息
                        return {
                            "cookies": response.cookies.get_dict(),
                            "login_info": data["data"]
                        }
                    elif data["data"]["code"] == 86038:
                        print("二维码已失效，请重新获取")
                        return None
                    elif data["data"]["code"] == 86090:
                        print("已扫码，请在APP上确认登录...")
                    elif data["data"]["code"] == 86101:
                        print("等待扫码...")
                    else:
                        print(f"未知状态: {data['data']['message']}")
                else:
                    print(f"请求失败: {data.get('message', '未知错误')}")
                    return None
                
                # 每2秒轮询一次
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                print(f"请求发生错误: {e}")
                return None
            except json.JSONDecodeError:
                print("解析响应数据失败")
                return None

    

    def login():
        # 1. 生成二维码
        result = login.generate_bilibili_qrcode()
        if not result:
            exit()
        
        print("\n二维码生成成功:")
        print(f"二维码URL: {result['qrcode_url']}")
        print(f"二维码Key: {result['qrcode_key']}")
        img=qrcode.make(result["qrcode_url"])
        print(f"登录链接: https://www.bilibili.com/login?qrcode_key={result['qrcode_key']}")
        img.save("login.jpg")
        # 2. 轮询登录状态
        login_result = login.poll_login_status(result["qrcode_key"])
        if login_result:
            return login_result
        else:
            return -1
def get_buvid():
    id=requests.get('https://api.bilibili.com/x/frontend/finger/spi')
    id.raise_for_status()
    id_dit=id.json()
    print(id_dit)
    code=id_dit['code']
    if code != 0 :
        return -1
    else:
        return id_dit['data']
    