import logging
from utils.logger import logger
from utils.database import Database

logger.debug("Initializing RuleExecutorAgent module")

class RuleExecutorAgent:
    """
    负责执行预定义的数据质量规则。

    属性:
        db (Database): 数据库连接实例

    方法:
        execute_rule: 执行指定的规则并返回结果
    """

    def __init__(self):
        """
        初始化 RuleExecutorAgent 实例，建立数据库连接。
        """
        self.db = Database()

    def execute_rule(self, rule_id):
        """
        执行指定的规则。

        参数:
            rule_id (str): 规则标识符。

        返回:
            str: 执行结果。
        """
        logger.info(f"执行规则 {rule_id}")
        
        try:
            # 从dq_rules表获取规则详情
            rule_query = f"SELECT * FROM dq_rules WHERE rule_id = '{rule_id}'"
            rule_result = self.db.query(rule_query)
            
            if not rule_result:
                return f"未找到规则 {rule_id} 的定义。"
            
            rule = rule_result[0]
            table_name = rule['table_name']
            column_name = rule['column_name']
            condition_type = rule['condition_type']
            description = rule['description']
            
            # 根据不同的条件类型构建查询
            if condition_type == 'not_null':
                query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL OR {column_name} = ''"
            elif condition_type == 'not_empty':
                query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} = '' OR {column_name} IS NULL"
            elif condition_type == 'in_list':
                # 这里需要从规则描述中提取允许的值列表
                # 例如，描述应该是类似"地区必须为 East/West/North/South"的形式
                allowed_values = description.split('必须为 ')[1].split(' ')[0].split('/')
                values_str = "','".join(allowed_values)
                query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} NOT IN ('{values_str}')"
            else:
                return f"不支持的条件类型: {condition_type}"
            
            # 执行规则查询
            result = self.db.query(query)
            count = result[0]['COUNT(*)'] if isinstance(result[0], dict) else result[0]
            
            # 生成结果信息
            if count == 0:
                return f"校验通过，不存在异常数据。{description} 的检查已通过，没有发现违规数据。"
            else:
                return f"校验不通过，发现了{count}条异常数据。{description} 的检查未通过，发现了{count}条违反规则的数据。"
                
        except Exception as e:
            return f"执行规则时出错：{str(e)}"