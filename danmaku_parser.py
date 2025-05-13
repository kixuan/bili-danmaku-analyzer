# danmaku_parser.py
try:
    # 关键: 导入由protoc编译生成的Python模块
    from bilibili_danmaku_pb2 import DmSegMobileReply, DanmakuElem
except ImportError:
    print("错误：无法导入 bilibili_danmaku_pb2.py。")
    print("请确保你已经使用protoc编译了bilibili_danmaku.proto文件。")
    print("编译命令: protoc --python_out=. bilibili_danmaku.proto")
    # 可以选择在这里直接退出程序或抛出更严重的异常
    DmSegMobileReply = None
    DanmakuElem = None

def parse_danmaku_from_bytes(data_bytes: bytes) -> list[str]:
    """
    从Protobuf二进制数据中解析出弹幕文本列表.
    """
    if DmSegMobileReply is None:
        print("Protobuf模块未加载，无法解析弹幕。")
        return []

    danmaku_list = []
    if not data_bytes:
        return danmaku_list

    try:
        dm_seg_reply = DmSegMobileReply()
        dm_seg_reply.ParseFromString(data_bytes) # 这是Protobuf对象的核心解析方法

        for elem in dm_seg_reply.elems:
            # elem 是一个 DanmakuElem 对象
            # 我们只关心它的 content 字段
            if elem.content: # 确保弹幕内容不为空
                danmaku_list.append(elem.content)
        return danmaku_list
    except Exception as e:
        # 捕获Protobuf解析可能发生的任何错误
        print(f"解析弹幕数据时发生错误: {e}")
        return [] # 返回空列表，而不是让整个程序崩溃