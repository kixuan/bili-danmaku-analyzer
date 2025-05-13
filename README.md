# BiliDanmakuAnalyzer 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Blog](https://img.shields.io/badge/技术博客-已上线-ff69b4)

> 🔍 B站弹幕数据挖掘工具：从协议逆向解析到情感分析的完整解决方案

---

## 📚 相关技术博客
**《B站弹幕爬虫实战指南》系列文章**  
👉 [（上篇）Protobuf协议解析与海量数据抓取](https://zhuanlan.zhihu.com/p/1905612606087099606)  
👉 下篇：SnowNLP情感计算与Pyecharts可视化（即将发布）  
👉 终篇：数据挖掘视角下的技术解析（即将发布） 

---

## 🚀 核心功能
### 协议逆向工程
- 逆向解析B站Protobuf二进制协议
- 模拟浏览器请求头（含Cookie验证）
- 支持历史弹幕按日期抓取

### 文本数据挖掘
- 正则清洗弹幕噪声（表情符号/特殊字符）
- 中文分词与停用词过滤
- 基于SnowNLP的情感极性分析

### 可视化呈现
- 动态词云生成（Pyecharts）
- 情感分布柱状图
- 数据清洗前后对比分析

---

## ⚡ 快速开始
### 环境安装
```bash
# 克隆项目
git clone https://github.com/SunSpace0/bili-danmaku-analyzer.git

# 安装依赖
pip install -r requirements.txt


### 基础使用
```bash
# 抓取指定视频弹幕（需要替换SESSDATA）
python main.py \
    --bvid BV1xx411x7xx \ 
    --date 2023-01-01 \
    --cookie "SESSDATA=your_cookie_value"
```

### 参数说明
| 参数      | 必选 | 说明                     |
|-----------|------|--------------------------|
| `--bvid`  | 是   | B站视频BV号              |
| `--date`  | 是   | 日期（格式YYYY-MM-DD）   |
| `--cookie`| 是   | 登录Cookie（含SESSDATA） |

---

## 🏗️ 项目结构
```
bili-danmaku-analyzer/
├── src/                  # 核心源码
│   ├── bilibili_api.py   # API请求模块
│   ├── danmaku_parser.py # Protobuf解析器
│   └── text_analyzer.py   # 文本分析引擎
├── docs/                 # 技术文档
├── requirements.txt      # 依赖清单
└── main.py                # 主程序入口
```

---

## 🔗 技术生态
本项目与我的技术博客构成完整知识体系：
1. **逆向工程**：详解Protobuf协议破解过程
2. **数据清洗**：分享正则表达式优化技巧
3. **算法调优**：探讨SnowNLP的领域适配方案
4. **可视化设计**：展示Pyecharts高级配置方法

---

## ⚠️ 免责声明
1. 本项目仅用于**技术研究**，请勿用于侵犯用户隐私
2. 请遵守[B站Robots协议](https://www.bilibili.com/robots.txt)
3. 使用者需自行承担法律风险

---

## 🤝 参与贡献
欢迎通过以下方式参与：
1. 提交Issue反馈问题
2. Fork后提交PR改进功能
3. 撰写技术文档或测试用例

---

License: [MIT](https://opensource.org/licenses/MIT)
