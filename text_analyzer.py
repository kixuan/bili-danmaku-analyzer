# text_analyzer.py
import re
import unicodedata
from collections import Counter
import jieba # 后面分词用
from snownlp import SnowNLP # 后面情感分析用

from BiliBliDanmu2.config import SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEUTRAL_LOWER_THRESHOLD


# from config import SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEUTRAL_LOWER_THRESHOLD # 引入情感阈值

# 定义一个简单的清洗规则：移除特殊符号、多余空格，并将全角转半角
def clean_danmaku(text: str) -> str:
    """清洗单条弹幕文本"""
    if not text:
        return ""
    # 移除B站特定表情符号，例如 [doge]
    text = re.sub(r'\[.*?\]', '', text)
    # 移除大部分标点符号和特殊字符，保留基本中文、英文、数字
    # 你可以根据需要调整这个正则表达式
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text, flags=re.UNICODE)
    # 全角转半角 (提升一致性)
    text = unicodedata.normalize('NFKC', text)
    # 去除首尾空格
    text = text.strip()
    # 合并中间多余空格
    text = re.sub(r'\s+', ' ', text)
    return text

def clean_danmaku_list(danmaku_list: list[str]) -> list[str]:
    """批量清洗弹幕列表"""
    print("\n[*] 开始清洗弹幕数据...")
    cleaned_list = [clean_danmaku(text) for text in danmaku_list if clean_danmaku(text)] # 清洗后非空的才保留
    print(f"[*] 清洗完成，保留有效弹幕 {len(cleaned_list)} 条。")
    return cleaned_list

# --- 后续分词、词频、情感分析函数将添加在这里 ---
def load_stopwords(filepath: str) -> set[str]:
    """加载停用词表"""
    stopwords = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
        print(f"[*] 成功加载停用词表: {filepath}")
    except FileNotFoundError:
        print(f"[!] 警告：停用词文件 {filepath} 未找到，将不使用停用词过滤。")
    except Exception as e:
        print(f"[!] 加载停用词时发生错误: {e}")
    return stopwords

def segment_text(text: str, stopwords: set[str]) -> list[str]:
    """对单条文本进行分词并去除停用词"""
    # 使用jieba进行分词 (精确模式)
    words = jieba.cut(text, cut_all=False)
    # 过滤掉停用词、单个字符和纯数字/空格 (根据需要调整)
    filtered_words = [word for word in words if word not in stopwords and len(word.strip()) > 1 and not word.isdigit()]
    return filtered_words

def calculate_word_frequency(danmaku_list: list[str], stopwords: set[str]) -> list[tuple[str, int]]:
    """计算清洗后弹幕列表的词频"""
    print("\n[*] 开始进行分词和词频统计...")
    word_counter = Counter()
    total_danmaku = len(danmaku_list)
    for i, text in enumerate(danmaku_list):
        if (i + 1) % (total_danmaku // 10 + 1) == 0: # 打印进度
             print(f"  [*] 分词进度: {((i+1)/total_danmaku)*100:.1f}%")
        words = segment_text(text, stopwords)
        word_counter.update(words)

    # 获取最常见的 N 个词 (例如前100个)
    top_words = word_counter.most_common(100)
    print(f"[*] 词频统计完成，最高频词示例:")
    for word, freq in top_words[:10]: # 打印前10个
        print(f"  - {word}: {freq}")
    return top_words # 返回词频列表 [(词, 频率), ...]

# --- 后续情感分析函数将添加在这里 ---

def analyze_sentiment(text: str) -> float | None:
    """分析单条文本的情感倾向值 (0-1之间)"""
    # SnowNLP 在处理空字符串或非常短的、无意义的文本时可能会出错或给出无意义结果
    if not text or len(text.strip()) < 2: # 简单过滤掉过短的文本
         return None
    try:
        s = SnowNLP(text)
        return s.sentiments
    except Exception as e:
        # print(f"[!] 分析情感时出错: '{text[:20]}...' - {e}") # 调试时可以取消注释
        return None # 返回None表示分析失败

def batch_analyze_sentiments(danmaku_list: list[str]) -> tuple[list[float], dict]:
    """批量分析弹幕的情感，并返回分数列表和统计结果"""
    print("\n[*] 开始进行情感分析...")
    sentiment_scores = []
    valid_analyzed_count = 0
    total_danmaku = len(danmaku_list)

    for i, text in enumerate(danmaku_list):
        if (i + 1) % (total_danmaku // 10 + 1) == 0: # 打印进度
             print(f"  [*] 情感分析进度: {((i+1)/total_danmaku)*100:.1f}%")
        score = analyze_sentiment(text)
        if score is not None:
            sentiment_scores.append(score)
            valid_analyzed_count += 1

    print(f"[*] 情感分析完成，共成功分析 {valid_analyzed_count} 条有效弹幕。")

    # 计算统计数据
    stats = {"total_analyzed": valid_analyzed_count, "positive": 0, "neutral": 0, "negative": 0}
    if not sentiment_scores:
        print("[!] 未能生成任何有效的情感分数。")
        return [], stats # 返回空列表和初始统计

    positive_count = 0
    neutral_count = 0
    negative_count = 0
    for score in sentiment_scores:
        if score >= SENTIMENT_POSITIVE_THRESHOLD:
            positive_count += 1
        elif score >= SENTIMENT_NEUTRAL_LOWER_THRESHOLD:
            neutral_count += 1
        else:
            negative_count += 1

    stats["positive"] = positive_count
    stats["neutral"] = neutral_count
    stats["negative"] = negative_count

    total_valid = stats["total_analyzed"]
    if total_valid > 0:
        print(f"[*] 情感分布统计:")
        print(f"  - 积极 (>= {SENTIMENT_POSITIVE_THRESHOLD}): {positive_count} 条 ({positive_count/total_valid:.1%})")
        print(f"  - 中性 ({SENTIMENT_NEUTRAL_LOWER_THRESHOLD} ~ {SENTIMENT_POSITIVE_THRESHOLD}): {neutral_count} 条 ({neutral_count/total_valid:.1%})")
        print(f"  - 消极 (< {SENTIMENT_NEUTRAL_LOWER_THRESHOLD}): {negative_count} 条 ({negative_count/total_valid:.1%})")
    else:
        print("[!] 没有有效的弹幕进行情感统计。")

    return sentiment_scores, stats # 返回分数列表和统计字典
