# visualizer.py
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Bar
import os

def create_word_cloud(word_freq_data: list[tuple[str, int]], bvid: str, date_range_str: str, output_dir: str = "output"):
    """根据词频数据生成词云图"""
    if not word_freq_data:
        print("[!] 没有词频数据，无法生成词云图。")
        return

    # 创建输出目录 (如果不存在)
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"{bvid}_word_cloud_{date_range_str}.html")

    print(f"\n[*] 正在生成词云图: {output_filename}")
    try:
        c = (
            WordCloud()
            .add(series_name="弹幕热词", data_pair=word_freq_data, word_size_range=[15, 100], shape='diamond') # shape可选 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"视频 {bvid} 弹幕热词词云 ({date_range_str})"),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
            .render(output_filename) # 直接渲染保存为HTML文件
        )
        print(f"[*] 词云图已保存。")
    except Exception as e:
        print(f"[!] 生成词云图时发生错误: {e}")

def create_sentiment_distribution_chart(sentiment_stats: dict, bvid: str, date_range_str: str, output_dir: str = "output"):
    """根据情感统计结果生成情感分布柱状图"""
    if not sentiment_stats or sentiment_stats.get("total_analyzed", 0) == 0:
        print("[!] 没有有效的情感统计数据，无法生成情感分布图。")
        return

    # 创建输出目录 (如果不存在)
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"{bvid}_sentiment_distribution_{date_range_str}.html")

    print(f"\n[*] 正在生成情感分布图: {output_filename}")
    categories = ["积极", "中性", "消极"]
    counts = [
        sentiment_stats.get("positive", 0),
        sentiment_stats.get("neutral", 0),
        sentiment_stats.get("negative", 0)
    ]
    # 为每个柱子设置不同颜色
    colors = ["#c23531", "#61a0a8", "#91c7ae"] # 可以自定义颜色

    try:
        bar = (
            Bar()
            .add_xaxis(categories)
            .add_yaxis("弹幕数量", counts, itemstyle_opts=opts.ItemStyleOpts(color=lambda params: colors[params.data_index])) # 使用回调函数设置颜色
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"视频 {bvid} 弹幕情感分布 ({date_range_str})"),
                yaxis_opts=opts.AxisOpts(name="弹幕数量"),
                xaxis_opts=opts.AxisOpts(name="情感倾向"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"), # 添加更好的提示框
            )
            .render(output_filename)
        )
        print(f"[*] 情感分布图已保存。")
    except Exception as e:
        print(f"[!] 生成情感分布图时发生错误: {e}")
