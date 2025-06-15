from utils.llm_utils import LLMClient
import logging
from utils.logger import logger

logger.debug("Initializing PlanAgent module")

class PlanAgent:
    """
    负责分析用户输入并决定使用哪个代理来处理请求。

    属性:
        None

    方法:
        determine_agent: 分析输入内容，返回对应的代理类型
    """

    def determine_agent(self, user_input):
        """
        分析用户输入并返回对应的代理类型。

        参数:
            user_input (str): 用户输入的自然语言描述。

        返回:
            str: 代理类型名称（如'data_query'、'rule_executor'、'rule_config'）
        """
        # 简单的关键词匹配逻辑作为示例
        if "数据库" in user_input or "表" in user_input or "查询" in user_input:
            return "data_query"
        elif "执行规则" in user_input:
            return "rule_executor"
        elif "配置规则" in user_input or "设置规则" in user_input:
            return "rule_config"
        else:
            return "unknown"
