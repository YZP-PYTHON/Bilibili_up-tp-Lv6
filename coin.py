import requests

def add_coin(cookie_str, aid=None, bvid=None, multiply=2, select_like=0):
    """
    给B站视频投币

    :param cookie_str: 登录Cookie字符串，需包含SESSDATA、buvid3、bili_jct
    :param aid: 视频的av号，与bvid二选一
    :param bvid: 视频的BV号，与aid二选一
    :param multiply: 投币数量，1或2，默认为2
    :param select_like: 是否同时点赞，1是0否，默认为0
    :return: API的JSON响应数据
    """
    # 解析Cookie字符串为字典
    cookies = {}
    for item in cookie_str.split(';'):
        key_value = item.strip().split('=', 1)
        if len(key_value) == 2:
            cookies[key_value[0]] = key_value[1]
    
    # 检查必要Cookie字段是否存在
    required_cookies = ['SESSDATA', 'buvid3', 'bili_jct']
    for key in required_cookies:
        if key not in cookies:
            raise ValueError(f"Cookie中缺少必要字段: {key}")
    
    # 检查必须提供aid或bvid中的一个
    if not aid and not bvid:
        raise ValueError("必须提供aid或bvid中的一个")
    if aid and bvid:
        raise ValueError("aid和bvid不能同时提供")
    
    # 检查multiply是否为1或2
    if multiply not in (1, 2):
        raise ValueError("投币数量必须为1或2")
    
    # 构造请求数据
    data = {
        'multiply': multiply,
        'select_like': select_like,
        'csrf': cookies['bili_jct']
    }
    if aid:
        data['aid'] = aid
    else:
        data['bvid'] = bvid
    
    # 发送POST请求
    response = requests.post(
        'https://api.bilibili.com/x/web-interface/coin/add',
        data=data,
        cookies=cookies
    )
    
    # 返回JSON响应
    return response.json()

# 使用示例
'''
if __name__ == '__main__':
    # 替换为你的Cookie，需包含SESSDATA、buvid3、bili_jct
    your_cookie = "SESSDATA=你的SESSDATA; buvid3=你的buvid3; bili_jct=你的bili_jct; 其他Cookie字段..."
    
    # 使用bvid投币2个并点赞
    try:
        result = add_coin(
            cookie_str=your_cookie,
            bvid='BV1N7411A7wC',  # 替换为目标视频的BV号
            multiply=2,
            select_like=1
        )
        if result['code'] == 0:
            print("投币成功！点赞状态:", result['data']['like'])
        else:
            print(f"投币失败，错误码: {result['code']}, 信息: {result['message']}")
    except Exception as e:
        print(f"发生错误: {e}")
'''