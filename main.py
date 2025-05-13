# # main.py
# import datetime
#
# from BiliBliDanmu2.config import SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEUTRAL_LOWER_THRESHOLD
# from bilibili_api import get_cid, fetch_danmaku_segment_bytes
# from danmaku_parser import parse_danmaku_from_bytes
# from text_analyzer import clean_danmaku_list, load_stopwords, calculate_word_frequency, batch_analyze_sentiments # 引入新函数
# import os # 引入os模块来创建目录
#
#
#
# def get_date_range(start_date_str: str, end_date_str: str) -> list[str]:
#     """生成日期范围内的日期字符串列表 (YYYY-MM-DD)"""
#     start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
#     end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
#
#     delta = end_date - start_date
#     dates = []
#     for i in range(delta.days + 1):
#         day = start_date + datetime.timedelta(days=i)
#         dates.append(day.strftime("%Y-%m-%d"))
#     return dates
#
#
# def main():
#     print("欢迎使用B站历史弹幕获取工具！")
#
#     # 1. 获取用户输入
#     bvid = input("请输入B站视频的BV号 (例如 BV1GJ411x7h7): ").strip()
#     # !!! 重要: Cookie涉及个人隐私，实际项目中不应硬编码或明文传输/存储 !!!
#     # 这里为了教学演示，直接输入。请确保从浏览器开发者工具获取SESSDATA的值。
#     user_sessdata = input("请输入你的B站SESSDATA Cookie值: ").strip()
#     if not user_sessdata:
#         print("错误：SESSDATA不能为空！")
#         return
#     user_cookie = f"SESSDATA={user_sessdata}"  # 构造成完整的Cookie字符串
#
#     start_date_str = input("请输入开始日期 (格式 YYYY-MM-DD, 例如 2023-01-01): ").strip()
#     end_date_str = input("请输入结束日期 (格式 YYYY-MM-DD, 例如 2023-01-03): ").strip()
#
#     try:
#         dates_to_fetch = get_date_range(start_date_str, end_date_str)
#     except ValueError:
#         print("日期格式错误，请确保输入YYYY-MM-DD格式。")
#         return
#
#     if not bvid:
#         print("BV号不能为空！")
#         return
#
#     # 2. 获取CID
#     print(f"\n正在为视频 {bvid} 获取CID...")
#     oid = get_cid(bvid, user_cookie)
#     if not oid:
#         print("无法获取CID，程序终止。请检查BV号和Cookie。")
#         return
#
#     # 3. 循环下载和解析弹幕
#     all_danmaku_texts = []
#     print(f"\n开始获取从 {start_date_str} 到 {end_date_str} 的弹幕...")
#     for date_str in dates_to_fetch:
#         danmaku_segment_bytes = fetch_danmaku_segment_bytes(oid, date_str, user_cookie)
#         if danmaku_segment_bytes:
#             parsed_texts = parse_danmaku_from_bytes(danmaku_segment_bytes)
#             if parsed_texts:
#                 print(f"日期 {date_str}: 成功解析 {len(parsed_texts)} 条弹幕。")
#                 all_danmaku_texts.extend(parsed_texts)
#             else:
#                 print(f"日期 {date_str}: 未解析到弹幕或解析失败。")
#         else:
#             print(f"日期 {date_str}: 下载弹幕数据失败。")
#
#     # 4. 初步成果展示
#     if all_danmaku_texts:
#         print(f"\n🎉 成功获取总计 {len(all_danmaku_texts)} 条弹幕！")
#         print("部分弹幕示例:")
#         for i, text in enumerate(all_danmaku_texts[:5]):  # 显示前5条
#             print(f"  {i + 1}. {text}")
#
#         # [可选] 保存所有原始弹幕到文件
#         # output_filename = f"{bvid}_raw_danmaku_{start_date_str}_to_{end_date_str}.txt"
#         # try:
#         #     with open(output_filename, 'w', encoding='utf-8') as f:
#         #         for text in all_danmaku_texts:
#         #             f.write(text + '\n')
#         #     print(f"\n所有原始弹幕已保存到文件: {output_filename}")
#         # except IOError as e:
#         #     print(f"\n保存弹幕文件失败: {e}")
#
#     else:
#         print("\n未能获取到任何弹幕。请检查日期范围、视频是否有弹幕或Cookie是否有效。")
#
#     # 4. 清洗弹幕数据 <--- 新增步骤
#     if not all_danmaku_texts:
#         print("\n[!] 未能获取到任何弹幕，无法进行后续分析。")
#         return
#
#     cleaned_danmaku = clean_danmaku_list(all_danmaku_texts)
#
#     if not cleaned_danmaku:
#         print("[!] 清洗后没有剩余有效弹幕，程序终止。")
#         return
#
#     # 打印清洗后的示例
#     print("\n[*] 清洗后弹幕示例:")
#     for i, text in enumerate(cleaned_danmaku[:5]): # 显示前5条
#         print(f"  {i+1}. {text}")
#
#     # [可选] 保存清洗后的弹幕到文件
#     # save_cleaned = input("\n是否将清洗后的弹幕保存到文件? (yes/no，默认为no): ").strip().lower()
#     # if save_cleaned == 'yes':
#     #     cleaned_filename = f"{bvid}_cleaned_danmaku_{start_date_str}_to_{end_date_str}.txt"
#     #     try:
#     #         with open(cleaned_filename, 'w', encoding='utf-8') as f:
#     #             for text in cleaned_danmaku:
#     #                 f.write(text + '\n')
#     #         print(f"[*] 清洗后的弹幕已保存到文件: {cleaned_filename}")
#     #     except IOError as e:
#     #         print(f"[!] 保存清洗后弹幕文件失败: {e}")
#
#
#     # 5. 加载停用词并进行词频统计 <--- 新增步骤
#     stopwords = load_stopwords("cn_stopwords.txt") # 确保文件存在
#     word_frequency = calculate_word_frequency(cleaned_danmaku, stopwords)
#
#     if not word_frequency:
#         print("[!] 未能统计出词频信息。")
#         # 这里可以选择是否终止，或者继续进行情感分析
#         # return
#
#     # [可选] 保存词频结果到文件
#     # save_freq = input("\n是否将词频结果保存到CSV文件? (yes/no，默认为no): ").strip().lower()
#     # if save_freq == 'yes' and word_frequency:
#     #     freq_filename = f"{bvid}_word_frequency_{start_date_str}_to_{end_date_str}.csv"
#     #     try:
#     #         import csv
#     #         with open(freq_filename, 'w', encoding='utf-8', newline='') as f:
#     #             writer = csv.writer(f)
#     #             writer.writerow(['词语', '频次']) # 写入表头
#     #             writer.writerows(word_frequency)
#     #         print(f"[*] 词频结果已保存到文件: {freq_filename}")
#     #     except Exception as e:
#     #         print(f"[!] 保存词频文件失败: {e}")
#     # --- 后续的情感分析和可视化步骤将在这里添加 ---
#
#     # 6. 进行情感分析 <--- 新增步骤
#     sentiment_scores, sentiment_stats = batch_analyze_sentiments(cleaned_danmaku)
#
#     # --- 可选保存：情感分析详情和摘要 ---
#     save_sentiment = input("\n是否将情感分析结果保存到文件? (yes/no，默认为no): ").strip().lower()
#     if save_sentiment == 'yes' and sentiment_scores:
#         # 创建输出目录 (如果不存在)
#         output_dir = "output"
#         os.makedirs(output_dir, exist_ok=True)
#
#         # 保存详细情感分数 (弹幕原文+分数，可能比较大)
#         sentiment_detail_filename = os.path.join(output_dir, f"{bvid}_sentiment_details_{start_date_str}_to_{end_date_str}.csv")
#         try:
#             import csv
#             with open(sentiment_detail_filename, 'w', encoding='utf-8', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(['Danmaku', 'SentimentScore'])
#                 # 注意：这里需要 cleaned_danmaku 和 sentiment_scores 一一对应
#                 # 但由于 analyze_sentiment 可能返回 None，直接 zip 可能不准确
#                 # 更准确的做法是在 batch_analyze_sentiments 中同时记录文本和分数
#                 # 为了简化，这里可以只保存分数列表，或保存摘要
#             # print(f"[*] 情感分析详情已尝试保存到: {sentiment_detail_filename}") # 简化处理
#         except Exception as e:
#             print(f"[!] 保存情感详情文件失败: {e}")
#
#         # 保存情感分析摘要
#         sentiment_summary_filename = os.path.join(output_dir, f"{bvid}_sentiment_summary_{start_date_str}_to_{end_date_str}.txt")
#         try:
#             with open(sentiment_summary_filename, 'w', encoding='utf-8') as f:
#                 total_valid = sentiment_stats["total_analyzed"]
#                 positive_count = sentiment_stats["positive"]
#                 neutral_count = sentiment_stats["neutral"]
#                 negative_count = sentiment_stats["negative"]
#                 f.write(f"B站视频 {bvid} ({start_date_str} to {end_date_str}) 弹幕情感分析摘要\n")
#                 f.write("="*40 + "\n")
#                 f.write(f"总计分析有效弹幕数: {total_valid}\n")
#                 if total_valid > 0:
#                     avg_score = sum(sentiment_scores) / total_valid if sentiment_scores else 0
#                     f.write(f"平均情感分数: {avg_score:.4f}\n")
#                     f.write(f"积极弹幕 (>= {SENTIMENT_POSITIVE_THRESHOLD}): {positive_count} 条 ({positive_count/total_valid:.1%})\n")
#                     f.write(f"中性弹幕 ({SENTIMENT_NEUTRAL_LOWER_THRESHOLD} ~ {SENTIMENT_POSITIVE_THRESHOLD}): {neutral_count} 条 ({neutral_count/total_valid:.1%})\n")
#                     f.write(f"消极弹幕 (< {SENTIMENT_NEUTRAL_LOWER_THRESHOLD}): {negative_count} 条 ({negative_count/total_valid:.1%})\n")
#                 else:
#                     f.write("无有效弹幕进行统计。\n")
#             print(f"[*] 情感分析摘要已保存到: {sentiment_summary_filename}")
#         except Exception as e:
#             print(f"[!] 保存情感摘要文件失败: {e}")
#
#     # --- 后续的可视化步骤将在这里添加 ---
#
#
#
# if __name__ == "__main__":
#     main()


# main.py (最终版)
import datetime
import os
from bilibili_api import get_cid, fetch_danmaku_segment_bytes
from danmaku_parser import parse_danmaku_from_bytes
# 确保导入所有需要的函数
from text_analyzer import (
    clean_danmaku_list, load_stopwords, calculate_word_frequency,
    batch_analyze_sentiments
)
# 引入可视化函数
from visualizer import create_word_cloud, create_sentiment_distribution_chart

def get_date_range(start_date_str: str, end_date_str: str) -> list[str]:
    """生成日期范围内的日期字符串列表 (YYYY-MM-DD)"""
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):
        day = start_date + datetime.timedelta(days=i)
        dates.append(day.strftime("%Y-%m-%d"))
    return dates

def main():
    print("欢迎使用B站历史弹幕分析工具！")

    # 1. 获取用户输入
    bvid = input("请输入B站视频的BV号 (例如 BV1GJ411x7h7): ").strip()
    user_sessdata = input("请输入你的B站SESSDATA Cookie值: ").strip()
    if not user_sessdata: print("错误：SESSDATA不能为空！"); return
    user_cookie = f"SESSDATA={user_sessdata}"
    start_date_str = input("请输入开始日期 (格式 YYYY-MM-DD): ").strip()
    end_date_str = input("请输入结束日期 (格式 YYYY-MM-DD): ").strip()

    try:
        dates_to_fetch = get_date_range(start_date_str, end_date_str)
        date_range_str_for_filename = f"{start_date_str}_to_{end_date_str}" # 用于文件名
    except ValueError: print("日期格式错误。"); return
    if not bvid: print("BV号不能为空！"); return

    # 2. 获取CID
    print(f"\n[*] 正在为视频 {bvid} 获取CID...")
    oid = get_cid(bvid, user_cookie)
    if not oid: print("[!] 无法获取CID，程序终止。"); return

    # 3. 循环下载和解析弹幕
    all_danmaku_texts = []
    print(f"\n[*] 开始获取从 {start_date_str} 到 {end_date_str} 的弹幕...")
    # --- 这部分循环下载解析的代码保持不变 ---
    for date_str in dates_to_fetch:
        danmaku_segment_bytes = fetch_danmaku_segment_bytes(oid, date_str, user_cookie)
        if danmaku_segment_bytes:
            parsed_texts = parse_danmaku_from_bytes(danmaku_segment_bytes)
            if parsed_texts:
                print(f"  [*] 日期 {date_str}: 成功解析 {len(parsed_texts)} 条弹幕。")
                all_danmaku_texts.extend(parsed_texts)
            else:
                # 即使解析为空列表，也认为是“成功”下载了文件（可能当天没弹幕或解析器问题）
                # print(f"  [!] 日期 {date_str}: 未解析到弹幕或解析失败。")
                pass # 不打印信息，减少干扰
        else:
            # 下载失败的消息已在 fetch 函数内部打印
            pass
    # --- 循环结束 ---

    if not all_danmaku_texts:
        print("\n[!] 未能获取到任何弹幕，无法进行后续分析。")
        return
    print(f"\n[*] 成功获取总计 {len(all_danmaku_texts)} 条原始弹幕。")

    # 4. 清洗弹幕数据
    cleaned_danmaku = clean_danmaku_list(all_danmaku_texts)
    if not cleaned_danmaku:
        print("[!] 清洗后没有剩余有效弹幕，程序终止。")
        return

    # 5. 加载停用词并进行词频统计
    stopwords = load_stopwords("cn_stopwords.txt")
    word_frequency = calculate_word_frequency(cleaned_danmaku, stopwords)

    # 6. 进行情感分析
    sentiment_scores, sentiment_stats = batch_analyze_sentiments(cleaned_danmaku)

    # --- 定义输出目录 ---
    output_directory = f"output_{bvid}_{date_range_str_for_filename}"
    os.makedirs(output_directory, exist_ok=True)
    print(f"\n[*] 所有输出文件将保存在目录: {output_directory}")

    # 7. 生成可视化图表 <--- 新增步骤
    # 生成词云图 (如果词频数据存在)
    if word_frequency:
        create_word_cloud(word_frequency, bvid, date_range_str_for_filename, output_dir=output_directory)

    # 生成情感分布图 (如果情感统计数据有效)
    if sentiment_stats.get("total_analyzed", 0) > 0:
        create_sentiment_distribution_chart(sentiment_stats, bvid, date_range_str_for_filename,
                                            output_dir=output_directory)

    # --- 可选保存部分 (可以根据需要取消注释) ---
    # if input("\n是否保存清洗后的弹幕? (y/n): ").lower() == 'y':
    #     # 保存代码... (使用 os.path.join(output_directory, filename))
    # if input("是否保存词频结果? (y/n): ").lower() == 'y' and word_frequency:
    #     # 保存代码... (使用 os.path.join(output_directory, filename))
    # if input("是否保存情感分析摘要? (y/n): ").lower() == 'y' and sentiment_stats['total_analyzed'] > 0:
    #     # 保存代码... (使用 os.path.join(output_directory, filename))

    print("\n--- 分析流程结束 ---")


if __name__ == "__main__":
    main()