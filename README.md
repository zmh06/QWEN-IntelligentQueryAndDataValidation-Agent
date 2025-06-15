# QWEN_SmartQuery

> 一个智能的数据查询与校验系统

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 目录

- [项目背景与目标](#项目背景与目标)
- [系统架构](#系统架构)
- [核心特性](#核心特性)
- [创新点](#创新点)
- [技术栈](#技术栈)
- [安装指南](#安装指南)
- [使用说明](#使用说明)
- [需要修改的关键配置](#需要修改的关键配置)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 快速上手

### 安装步骤

1. 克隆本项目到本地：
   ```bash
   git clone https://github.com/zmh06/QWEN-IntelligentQueryAndDataValidation-Agent.git
   cd QWEN_SmartQuery
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动服务：
   ```bash
   python app.py
   ```

## 项目背景与目标

随着数据量的爆炸式增长，如何让非技术人员也能轻松查询和理解数据库中的数据成为一个重要课题。本项目旨在构建一个智能查询与校验系统，使用户可以通过自然语言与数据库交互，无需了解复杂的SQL语法。

本项目作者仅提供思路和配置信息，所有表结构、测试数据、代码、文档等均由通义灵码自动生成完成。

### 💡 主要目标

- 构建自然语言到 SQL 的转换系统
- 实现上下文感知的查询处理
- 提供简洁易懂的自然语言结果反馈
- 构建完整的数据查询系统
- 提供灵活的数据校验规则定义和管理功能

### 🧠 技术价值

该项目展示了如何通过智能编码工具快速构建具备基础功能的应用原型，适合用于探索和练习以下技术领域：

- **大模型应用开发**：结合 DashScope 的 Qwen 模型，实现自然语言到 SQL 的智能转换及结果格式化输出
- **多代理架构设计**：通过多个专业代理（PlanAgent、DataQueryAgent、RuleConfigAgent 等）协同工作，模拟复杂系统交互
- **测试驱动开发（TDD）**：使用 YAML 预设测试用例验证模型输出是否符合预期
- **提示词工程（Prompt Engineering）**：优化大模型输入提示词，提升意图识别与输出准确性
- **数据质量校验**：通过RuleConfigAgent实现灵活的数据校验规则配置和管理

## 项目结构
QWEN_SmartQuery/
├── data/                  # 数据存储目录，包含测试数据和示例数据
├── agents/                # 多代理模块，包含PlanAgent、DataQueryAgent等
│   ├── PlanAgent.py       # 负责生成查询计划
│   ├── DataQueryAgent.py  # 负责执行SQL查询并返回结果
│   └── RuleConfigAgent.py # 负责数据校验规则的配置和管理
├── utils/                 # 工具函数和辅助模块
│   ├── ContextManager.py  # 上下文管理器，支持上下文感知的查询处理
│   └── PromptEngineer.py  # 提示词工程模块，优化大模型输入提示词
├── tests/                 # 测试用例目录，包含YAML预设测试用例
├── config/                # 配置文件目录，存放关键配置信息
├── app.py                 # 主程序入口
└── README.md              # 项目说明文档

## 创新点

### 🚀 主要创新

- **多代理协作**：采用多个专业代理（PlanAgent、DataQueryAgent、RuleConfigAgent等）协同工作的架构，提高了系统的灵活性和扩展性
- **上下文感知**：通过ContextManager实现上下文感知的查询处理，使得交互更加自然流畅
- **测试驱动开发（TDD）**：利用YAML预设测试用例来验证模型输出是否符合预期，确保了输出的一致性和准确性
- **提示词工程（Prompt Engineering）**：对大模型输入提示词进行了优化，提升了意图识别与输出的准确性
- **数据质量校验**：通过RuleConfigAgent实现了灵活的数据校验规则配置和管理，增强了数据质量控制能力
- **大模型校验输出结果**：在测试过程中，通过大模型自动校验输出结果是否符合预期，进一步提升了测试的准确性和效率
