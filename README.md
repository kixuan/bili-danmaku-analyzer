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
