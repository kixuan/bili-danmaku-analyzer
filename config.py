# config.py (修正版)

# Bilibili API Endpoints
# --- 确保这里的 bvid= 后面没有空格 ---
CID_API_URL = "https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp"
# ---------------------------------------
DANMAKU_API_URL = "https://api.bilibili.com/x/v2/dm/web/history/seg.so" # ?type=1&oid={oid}&date={date}

# Base Headers (Cookie will be added dynamically)
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.bilibili.com", # Important for some API calls
}

# Protobuf definition (This is just for reference here, actual .proto file is separate)
# We will use the compiled bilibili_danmaku_pb2.py
PROTO_DEFINITION_INFO = """
syntax = "proto3";

message DanmakuElem {
    int64 id = 1;
    int32 progress = 2;
    int32 mode = 3;
    int32 fontsize = 4;
    uint32 color = 5;
    string midHash = 6;
    string content = 7;
    int64 ctime = 8;
    int32 weight = 9;
    // ... other fields
}

message DmSegMobileReply {
    repeated DanmakuElem elems = 1;
    int32 state = 2;
    // ... other fields
}
"""

# Sentiment Analysis Thresholds
SENTIMENT_POSITIVE_THRESHOLD = 0.6 # 大于等于此值为积极
SENTIMENT_NEUTRAL_LOWER_THRESHOLD = 0.4 # 大于等于此值且小于积极阈值为中性
# 低于 SENTIMENT_NEUTRAL_LOWER_THRESHOLD 为消极