import requests
import os
import sys
# 将项目根目录添加到Python路径中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from utils.logger import logger

logger.debug("Initializing llm_utils module")

class LLMClient:
    """
    大模型客户端，用于与 DashScope 的 Qwen 模型进行交互。

    属性:
        api_key (str): DashScope API 密钥。
        base_url (str): DashScope API 基础 URL。

    方法:
        __init__: 初始化 LLM 客户端
        generate_sql: 将自然语言转换为 SQL 查询语句
        generate_natural_language: 将 SQL 查询结果转换为自然语言描述
        verify_output_format: 验证输出是否符合期望格式
    """

    def __init__(self):
        """
        初始化 LLM 客户端，设置 API 密钥和基础 URL。
        
        如果环境变量 DASHSCOPE_API_KEY 未设置，抛出 ValueError。
        """
        # API密钥必须通过环境变量 DASHSCOPE_API_KEY 设置
        # 没有提供默认值，请务必在运行前设置该环境变量
        # 设置方法：
        # 在命令行中临时设置（当前会话有效）：
        #   set DASHSCOPE_API_KEY=your_api_key_here
        # 在Windows系统中永久设置（需要管理员权限）：
        #   [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your_api_key_here", [EnvironmentVariableTarget]::Machine)
        # 在Windows系统中设置当前用户环境变量（推荐）：
        #   [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your_api_key_here", [EnvironmentVariableTarget]::User)
        self.api_key = os.getenv("DASHSCOPE_API_KEY")  # 从环境变量获取API密钥
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def verify_output_format(self, expected_format, actual_output):
        """
        验证输出格式是否符合要求。

        参数:
            expected_format (str): 期望输出格式描述。
            actual_output (str): 实际输出内容。

        返回:
            str: 格式验证结果（通过/失败）和理由。
        """
        prompt_text = f"你是一个格式验证专家。请严格按以下步骤验证实际输出是否符合期望格式要求：\\n\\n1. 期望输出格式: {expected_format}\\n2. 实际输出: {actual_output}\\n\\n请回答'通过'或'失败'，然后给出验证理由。\\n\\n注意：只返回验证结果和理由，不要包含其他内容。\\n\\n示例回答：\\n通过: 输出符合期望的自然语言描述格式，正确报告了表数量。\\n或者\\n失败: 输出不符合表格格式要求，缺少psql风格的表格边框。\\n"
        
        payload = {
            "model": "qwen-max",
            "input": {
                "prompt": prompt_text.replace("\\", "\\\\")
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['output']['text'].strip()
        else:
            logger.error(f"API调用失败，状态码: {response.status_code}")
            return "失败: API调用失败，无法验证输出格式。"
            
    def generate_sql(self, natural_language, table_schema=None):
        """
        将自然语言转换为 SQL 查询语句。

        参数:
            natural_language (str): 用户输入的自然语言描述。
            table_schema (dict, optional): 数据库表结构信息，默认为 None。

        返回:
            str: 生成的 SQL 查询语句，如果失败则返回 None。
        """
        logger.info("生成SQL请求开始")
        logger.debug(f"natural_language: {natural_language}")
        if table_schema:
            logger.debug(f"table_schema: {table_schema}")
        
        # 如果提供了表结构信息，则将其加入提示词
        schema_info = ""
        if table_schema:
            schema_info = "\n".join([f"Table: {table}, Columns: {', '.join(columns)}" for table, columns in table_schema.items()])
        
        payload = {
            "model": "qwen-max",
            "input": {
                "prompt": f"""
                根据以下自然语言描述和数据库表结构生成MySQL查询语句：
                自然语言描述：{natural_language}
                表结构信息：
                {schema_info}
                注意：请直接返回SQL语句，无论如何都不要包含任何解释性文本，不要包含注释，结尾不要带有分号。
                如果无法生成有效的SQL，请返回:SELECT '未查询到相关数据'
                """
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        if response.status_code == 200:
            generated_sql = response.json()['output']['text'].strip()
            logger.info(f"LLM原始响应: {generated_sql}")
            
            # 检查生成的SQL是否符合基本格式
            if not generated_sql.lower().startswith(("select", "update", "delete", "insert")):
                logger.warning("生成的SQL格式不正确")
                return None  # 返回None表示生成失败
            
            # 验证SQL是否包含非法字符或语法错误
            try:
                # 简单的语法检查（实际可使用更复杂的解析器）
                if ";" in generated_sql or "--" in generated_sql:
                    logger.warning("生成的SQL包含非法字符")
                    return None
                
                # 检查是否有潜在的注入攻击风险
                if "' OR '1'='1" in generated_sql:
                    logger.warning("检测到潜在的SQL注入尝试")
                    return None
                
                return generated_sql
            except Exception as e:
                logger.error(f"SQL验证过程中出错: {str(e)}")
                return None
        else:
            logger.error(f"API调用失败，状态码: {response.status_code}")
            return None

    def generate_intent(self, prompt):
        """
        分析用户输入并判断其意图类型。
        
        参数:
            prompt (str): 用户输入的文本。
        
        返回:
            str: 判断出的意图类型名称（如"data_query"、"rule_executor"、"rule_config"），如果失败则返回None。
        """
        payload = {
            "model": "qwen-max",
            "input": {
                "prompt": f"分析以下用户输入并判断其意图类型：{prompt}\n可能的意图类型包括：data_query、rule_executor、rule_config。请只返回一个意图类型名称。"
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['output']['text'].strip()
        else:
            return None

    def generate_natural_language(self, prompt):
        """
        使用大模型生成自然语言回答。

        参数:
            prompt (str): 包含用户输入和 SQL 查询结果的提示词。

        返回:
            str: 生成的自然语言回答。
        """
        logger.info("生成自然语言请求开始")
        logger.debug(f"prompt: {prompt}")
        
        payload = {
            "model": "qwen-max",
            "input": {
                "prompt": f"""
                根据以下信息生成自然语言的回答：
                {prompt}
                
                请确保回答通顺、易于理解，并符合中文表达习惯。
                不要使用代码块或特殊格式，只返回自然语言描述。
                """
            }
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        if response.status_code == 200:
            generated_text = response.json()['output']['text'].strip()
            logger.info(f"LLM原始响应: {generated_text}")
            return generated_text
        else:
            logger.error(f"API调用失败，状态码: {response.status_code}")
            return "无法生成自然语言回答。"
