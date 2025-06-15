"""
Data QA Agent - 基于大模型的数据查询助手

本项目提供自然语言转 SQL、规则配置、数据质量检查等功能。
支持多代理架构，可扩展性强，适用于学习和实践大模型应用开发。
"""

__version__ = "0.1.0"  # 项目版本号
__author__ = "your-name-here"  # 作者名称
__license__ = "MIT"  # 开源协议

# 导入核心模块
from agents.plan_agent import PlanAgent
from agents.data_query_agent import DataQueryAgent
from agents.rule_config_agent import RuleConfigAgent
from agents.rule_executor_agent import RuleExecutorAgent
from utils.context_manager import ContextManager
from utils.logger import logger
from utils.database import Database
from utils.llm_utils import LLMClient

# 主程序入口
from main import main