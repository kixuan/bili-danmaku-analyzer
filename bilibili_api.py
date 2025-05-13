# bilibili_api.py (修正版)
import requests
import time
from config import CID_API_URL, DANMAKU_API_URL, BASE_HEADERS
import json # 引入json库用于更安全的解析

def get_cid(bvid: str, user_cookie: str) -> int | None:
    """
    根据BVID获取视频的CID (假设是单P视频，取第一个CID).
    包含增强的错误报告功能。
    """
    url = CID_API_URL.format(bvid=bvid)
    headers = BASE_HEADERS.copy()
    headers["cookie"] = user_cookie
    headers["referer"] = f"https://www.bilibili.com/video/{bvid}/"
    # 确保Origin请求头存在，有时是必需的
    # headers["Origin"] = "https://www.bilibili.com" # BASE_HEADERS 中已包含

    print(f"  [*] 尝试从URL获取CID: {url}") # 增加调试信息
    try:
        response = requests.get(url, headers=headers, timeout=10)

        # --- 增强的错误检查 ---
        if response.status_code != 200:
            print(f"  [!] 获取CID失败: HTTP状态码: {response.status_code}")
            # 尝试打印部分响应文本以获取线索
            try:
                print(f"  [!] 响应文本片段: {response.text[:500]}...")
            except Exception:
                 pass # 忽略打印文本时的任何错误
            return None

        # 尝试解析JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print(f"  [!] 获取CID失败: 响应不是有效的JSON格式。")
            print(f"  [!] 响应文本片段: {response.text[:500]}...")
            return None

        # --- 更详细地检查响应内容 ---
        if data is None:
             print(f"  [!] 获取CID失败: API返回了空的JSON数据。")
             return None

        api_code = data.get('code', -999) # 如果'code'键不存在，给一个默认错误码
        api_message = data.get('message', 'N/A') # 获取API返回的消息

        if api_code == 0:
            cid_data = data.get('data')
            # 检查 'data' 是否是一个非空列表
            if cid_data and isinstance(cid_data, list) and len(cid_data) > 0:
                # 检查列表的第一个元素是否包含 'cid'
                if 'cid' in cid_data[0]:
                    cid = cid_data[0]['cid']
                    print(f"  [*] 成功获取视频 {bvid} 的CID: {cid}")
                    return cid
                else:
                     print(f"  [!] 获取CID成功(code=0)，但响应数据的第一个元素中缺少 'cid' 字段。 Data[0]: {cid_data[0]}")
                     return None
            else:
                 print(f"  [!] 获取CID成功(code=0)，但响应 'data' 字段为空或格式不正确。 Data: {cid_data}")
                 return None
        else:
            # 明确打印出Bilibili返回的错误码和消息
            print(f"  [!] 获取CID失败: B站API返回错误码: {api_code}, 消息: '{api_message}'")
            # 你可以取消下面这行注释来查看完整的API响应，有助于调试复杂问题
            # print(f"  [!] 完整的API响应JSON: {data}")
            return None
        # --- 详细检查结束 ---

    except requests.exceptions.Timeout:
         print(f"  [!] 请求CID时超时。")
         return None
    except requests.exceptions.RequestException as e:
        # 网络层面的错误 (DNS错误, 连接错误等)
        print(f"  [!] 请求CID时发生网络错误: {e}")
        return None
    except Exception as e:
        # 捕获其他可能的意外错误
        print(f"  [!] 获取CID时发生未知错误: {e}")
        return None


def fetch_danmaku_segment_bytes(oid: int, date_str: str, user_cookie: str) -> bytes | None:
    """
    获取指定OID和日期的弹幕数据 (原始bytes).
    包含增强的错误处理和调整后的延时。
    """
    params = {
        "type": 1,
        "oid": oid,
        "date": date_str
    }
    headers = BASE_HEADERS.copy()
    headers["cookie"] = user_cookie
    # 弹幕API的Referer通常使用av号+oid，这是一种常见的做法
    headers["referer"] = f"https://www.bilibili.com/video/av{oid}/"

    print(f"  [*] 正在下载日期 {date_str} 的弹幕...")
    try:
        response = requests.get(DANMAKU_API_URL, params=params, headers=headers, timeout=15)

        # 检查状态码
        if response.status_code != 200:
             print(f"  [!] 下载日期 {date_str} 弹幕失败: HTTP状态码: {response.status_code}")
             # 对一些常见的错误状态码给出更具体的提示
             if response.status_code == 412: # Precondition Failed
                 print("  [!] (建议) 错误412：请求被拒绝，可能是Cookie失效或请求过于频繁。请检查Cookie或增加请求间隔。")
             elif response.status_code == 404: # Not Found
                 print(f"  [!] (信息) 错误404：未找到资源，通常表示日期 {date_str} 没有弹幕数据。")
             elif response.status_code == 403: # Forbidden
                 print(f"  [!] (建议) 错误403：禁止访问，权限不足，请确认Cookie有效且有权限访问该视频弹幕。")
             else:
                 # 对于其他错误，尝试打印响应体前200个字符
                 try:
                     print(f"  [!] 响应文本片段: {response.text[:200]}...")
                 except Exception: pass # 忽略打印错误
             return None

        # 请求成功 (status code 200)
        # 稍微增加延时，放在成功请求之后，避免对服务器造成过大压力
        time.sleep(1.5) # 等待1.5秒
        return response.content # 返回原始的二进制数据

    except requests.exceptions.Timeout:
         print(f"  [!] 下载日期 {date_str} 弹幕时超时。")
         return None
    except requests.exceptions.RequestException as e:
        print(f"  [!] 下载日期 {date_str} 弹幕时发生网络错误: {e}")
        return None
    except Exception as e:
        # 捕获其他可能的意外错误
        print(f"  [!] 下载日期 {date_str} 弹幕时发生未知错误: {e}")
        return None
