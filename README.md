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

项目的目录结构如下：

```
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
```

每个模块都有明确的功能划分，便于维护和扩展。

## 系统架构

本项目采用多代理协作架构，主要包括以下几个核心组件：

1. **PlanAgent**：负责解析用户查询请求，生成查询计划
2. **DataQueryAgent**：根据查询计划执行SQL查询，并返回结果
3. **RuleConfigAgent**：负责数据校验规则的配置和管理
4. **ContextManager**：维护查询上下文，支持上下文感知的查询处理
5. **PromptEngineer**：优化大模型输入提示词，提升意图识别与输出准确性

这种架构设计使得系统具有良好的灵活性和扩展性，可以方便地添加新的功能模块。

## 核心特性

### 自然语言查询

系统支持通过自然语言与数据库交互，用户无需了解复杂的SQL语法即可进行数据查询。

### 上下文感知

通过ContextManager实现上下文感知的查询处理，使得交互更加自然流畅。

### 数据校验规则配置

通过RuleConfigAgent实现灵活的数据校验规则配置和管理，增强了数据质量控制能力。

### 测试驱动开发

利用YAML预设测试用例来验证模型输出是否符合预期，确保了输出的一致性和准确性。

## 创新点

### 🚀 主要创新

- **多代理协作**：采用多个专业代理（PlanAgent、DataQueryAgent、RuleConfigAgent等）协同工作的架构，提高了系统的灵活性和扩展性
- **上下文感知**：通过ContextManager实现上下文感知的查询处理，使得交互更加自然流畅
- **测试驱动开发（TDD）**：利用YAML预设测试用例来验证模型输出是否符合预期，确保了输出的一致性和准确性
- **提示词工程（Prompt Engineering）**：对大模型输入提示词进行了优化，提升了意图识别与输出的准确性
- **数据质量校验**：通过RuleConfigAgent实现了灵活的数据校验规则配置和管理，增强了数据质量控制能力
- **大模型校验输出结果**：在测试过程中，通过大模型自动校验输出结果是否符合预期，进一步提升了测试的准确性和效率

## 技术栈

本项目主要使用以下技术和工具：

- **Python**：作为主要开发语言
- **Qwen**：基于阿里云的大规模语言模型，用于自然语言理解和生成
- **DashScope**：提供大模型API和服务
- **YAML**：用于测试用例和配置信息的存储
- **Git**：版本控制系统
- **GitHub**：代码托管和协作平台

## 安装指南

### 环境要求

- Python 3.x
- pip
- Git

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

## 使用说明

### 基本用法

启动服务后，用户可以通过自然语言进行数据查询。例如：

"请查询销售额超过10000的订单"

### 查询历史记录

系统会自动保存用户的查询历史，支持查看和管理历史查询记录。

### 数据校验

用户可以通过RuleConfigAgent配置数据校验规则，对查询结果进行质量检查。

## 需要修改的关键配置

### 数据库配置

在`config/db_config.yaml`中配置数据库连接信息，包括主机地址、端口、数据库名称、用户名和密码等。

### 大模型配置

在`config/model_config.yaml`中配置大模型相关参数，如模型类型、API密钥、请求超时时间等。

## 贡献指南

我们欢迎社区开发者参与本项目的改进和完善。如果您有任何想法或建议，请随时提交Issue或Pull Request。

### 提交Issue

如果您在使用过程中遇到任何问题，或者有新的需求建议，请提交Issue。

### 提交Pull Request

如果您已经修复了某个问题或实现了新功能，请提交Pull Request。

## 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。