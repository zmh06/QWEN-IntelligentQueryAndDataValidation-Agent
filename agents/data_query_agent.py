import logging
from utils.logger import logger
from utils.database import Database  # 添加缺失的导入
from utils.llm_utils import LLMClient  # 添加缺失的导入

logger.debug("Initializing DataQueryAgent module")

class DataQueryAgent:
    """
    负责将自然语言查询转换为 SQL 查询并返回结果。

    属性:
        db (Database): 数据库连接实例
        llm (LLMClient): 大模型客户端实例

    方法:
        handle_query: 处理用户输入的自然语言查询，生成并执行 SQL，返回格式化结果
        format_natural_language_response: 将 SQL 查询结果格式化为自然语言回答
        generate_natural_language: 使用大模型生成自然语言回答
        escape_special_characters: 转义 SQL 中的特殊字符
        extract_params_from_sql: 提取 SQL 中的参数
    """

    def __init__(self):
        """
        初始化 DataQueryAgent 实例，建立数据库连接和 LLM 客户端。
        """
        self.db = Database()
        self.llm = LLMClient()

    def handle_query(self, user_input):
        # 获取表结构信息
        table_schema = self.db.get_table_schema()
        
        # 记录表结构信息
        logger.debug(f"获取到的表结构: {table_schema}")
        
        # 调用大模型生成SQL
        logger.info("调用LLM生成SQL")
        logger.debug(f"传给LLM的提示词: {user_input}")
        
        raw_sql = self.llm.generate_sql(user_input, table_schema)
        
        if not raw_sql:
            logger.warning("无法生成有效的SQL语句")
            return "无法生成有效的SQL语句，请重新描述您的查询需求。"
        
        # 打印原始生成的SQL，便于调试
        logger.info(f"Raw SQL generated: {raw_sql}")

        # 新增：转义SQL中的特殊字符
        raw_sql = self.escape_special_characters(raw_sql)

        try:
            # 解析SQL并提取参数
            params = self.extract_params_from_sql(raw_sql)
            
            # 如果用户问的是"分别是哪几张"，则执行单独的表名查询
            if "分别" in user_input and "哪几张" in user_input:
                results = self.db.query("SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()")
            # 如果用户问的是"有多少张表"，则执行单独的表数量查询
            elif "多少张表" in user_input or "多少个表" in user_input:
                results = self.db.query("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE()")
            # 否则执行原来的查询
            else:
                results = self.db.query(raw_sql, params)
            
            # 构建自然语言输出
            prompt = f"用户输入: {user_input}\nSQL查询结果: {results}"
            
            # 使用LLM生成自然语言回答
            try:
                llm_response = self.llm.generate_natural_language(prompt)
                logger.info(f"LLM生成的自然语言回答: {llm_response}")
                return llm_response
            except Exception as e:
                logger.error(f"使用LLM生成自然语言时出错: {str(e)}")
                return "无法生成自然语言回答，请查看原始表格数据。"

        except Exception as e:
            return f"执行SQL时出错：{str(e)}"

    def format_natural_language_response(self, user_input, results):
        """将SQL执行结果格式化为自然语言回答"""
        if not results:
            logger.debug("查询结果为空")
            return "未找到匹配的数据。"
        
        # 记录完整的用户输入和结果，便于调试
        logger.debug(f"原始用户输入: {user_input}")
        logger.debug(f"查询结果: {results}")
        
        # 构建自然语言输出
        prompt = f"用户输入: {user_input}\nSQL查询结果: {results}"
        
        # 使用LLM生成自然语言回答
        try:
            llm_response = self.generate_natural_language(prompt)
            logger.info(f"LLM生成的自然语言回答: {llm_response}")
            return llm_response
        except Exception as e:
            logger.error(f"使用LLM生成自然语言时出错: {str(e)}")
            return "无法生成自然语言回答，请查看原始表格数据。"

    def generate_natural_language(self, prompt):
        """
        使用大模型生成自然语言回答。
        
        参数:
            prompt (str): 包含用户输入和SQL查询结果的提示词。
        
        返回:
            str: 生成的自然语言回答。
        """
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
            return response.json()['output']['text'].strip()
        else:
            logger.error(f"API调用失败，状态码: {response.status_code}")
            return "无法生成自然语言回答。"

    def handle_rule_config(self, user_input):
        """
        处理规则配置相关的请求。
        
        参数:
            user_input (str): 用户输入的自然语言描述。
        
        返回:
            str: 生成的自然语言回答。
        """
        logger.info("处理规则配置请求")
        logger.debug(f"用户输入: {user_input}")
        
        # 示例逻辑：返回固定的规则配置信息
        rule_config_info = "规则配置功能正在开发中，当前暂不支持实际操作。"
        logger.info(f"规则配置响应: {rule_config_info}")
        return rule_config_info

    def escape_special_characters(self, sql):
        """
        转义SQL中的特殊字符，如%，_等。
        
        参数:
            sql (str): 原始SQL语句。
        
        返回:
            str: 转义后的SQL语句。
        """
        # 修改：将SQL中的%替换为%%以避免格式字符串错误
        return sql.replace('%', '%%')

    def extract_params_from_sql(self, sql):
        """
        提取SQL中的参数。
        
        参数:
            sql (str): 原始SQL语句。
        
        返回:
            tuple: 参数元组，如果没有参数则返回空元组。
        """
