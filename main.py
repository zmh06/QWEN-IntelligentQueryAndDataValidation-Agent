from agents.plan_agent import PlanAgent
from agents.data_query_agent import DataQueryAgent
from agents.rule_config_agent import RuleConfigAgent
from agents.rule_executor_agent import RuleExecutorAgent
from utils.context_manager import ContextManager
from utils.logger import logger  # 导入日志模块
import traceback  # 用于错误追踪
import yaml
import os
import logging  # 缺失的logging模块已补全

def load_test_cases():
    """加载测试用例文件"""
    test_cases_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'test_cases.yaml')
    with open(test_cases_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def select_test_cases(test_cases):
    """
    让用户选择要执行的测试用例
    返回值: 选定的测试用例列表
    """
    print("共有 {} 个测试用例可用:".format(len(test_cases)))
    for i, test_case in enumerate(test_cases):
        print("{}. {} ({})".format(i+1, test_case['input'], test_case['purpose']))

    while True:
        choice = input("请输入您想执行的测试用例(输入数字n执行第n个，输入0执行全部，输入m,n执行第m到n个): ")
        try:
            # 如果输入包含逗号，则作为范围处理
            if ',' in choice:
                start, end = map(int, choice.split(','))
                if 1 <= start <= end <= len(test_cases):
                    return test_cases[start-1:end], start, end
            # 否则作为单个数字处理
            else:
                num = int(choice)
                if num == 0:
                    # 执行所有测试用例
                    return test_cases, 1, len(test_cases)
                elif 1 <= num <= len(test_cases):
                    # 只执行指定的测试用例
                    return [test_cases[num-1]], num, num

            print("输入无效，请输入有效的测试用例编号")
        except ValueError:
            print("输入格式错误，请输入数字")

def run_tests(data_query_agent, plan_agent, rule_executor_agent, rule_config_agent, context_manager, test_logger):
    """
    执行测试用例函数
    读取测试用例文件，执行每个测试用例，并记录结果
    """
    # 获取测试用例文件路径
    test_cases = load_test_cases()
    
    # 选择要执行的测试用例
    selected_test_cases, start, end = select_test_cases(test_cases)
    
    # 输出测试摘要
    passed = 0
    failed = 0
    
    # 执行每个测试用例
    for idx in range(start, end+1):
        test_case = test_cases[idx-1]  # 转换为0-based索引
        print(f"执行测试用例: {test_case['input']} (第{idx}项)")
        
        # 使用上下文扩展用户输入
        expanded_input = context_manager.expand_query_with_context(test_case['input'])
        
        # 记录改写后的输入
        logger.info(f"改写后的输入: {expanded_input}")
        test_logger.info(f"改写后的输入: {expanded_input}")
        test_logger.debug(f"改写后的输入详细记录: {expanded_input}")
        
        # 确定代理类型
        agent_type = plan_agent.determine_agent(expanded_input)
        logger.info(f"识别到的代理类型: {agent_type}")
        test_logger.info(f"识别到的代理类型: {agent_type}")
        test_logger.debug(f"代理类型识别详情：输入内容: {expanded_input}, 识别结果: {agent_type}")
        
        # 执行查询
        if agent_type == "data_query":
            result = data_query_agent.handle_query(expanded_input)
        elif agent_type == "rule_executor":
            rule_id = test_case['input'].replace("执行规则", "").strip()
            result = rule_executor_agent.execute_rule(rule_id)
        elif agent_type == "rule_config":
            result = rule_config_agent.handle_rule_config(expanded_input)
        else:
            result = "无法识别您的需求类型，请重新描述。"
            
        # 更新上下文
        context_manager.update_context(expanded_input, result)
        
        # 记录输出结果
        logger.info(f"给用户的输出: {result}")
        test_logger.info(f"测试结果: {result}")
        test_logger.debug(f"完整输出结果: {result}")
        
        # 更新测试用例实际输出
        test_case['actual_output'] = str(result)  # 确保输出是字符串格式
        
        # 检查输出是否符合预期
        expected_format = test_case.get('expected_output_format', '')
        actual_output = test_case['actual_output']
        
        # 使用LLM判断输出是否符合期望格式
        prompt = f"你是一个格式验证专家。请严格按以下步骤验证实际输出是否符合期望格式要求：\n\n1. 期望输出格式: {expected_format}\n2. 实际输出: {actual_output}\n\n请回答'通过'或'失败'，然后给出验证理由。\n\n注意：只返回验证结果和理由，不要包含其他内容。\n\n示例回答：\n通过: 输出符合期望的自然语言描述格式，正确报告了表数量。\n或者\n失败: 输出不符合表格格式要求，缺少psql风格的表格边框。\n\n"
        
        logger.info(f"使用大模型验证输出格式，提示词内容：{prompt}")
        result = data_query_agent.llm.verify_output_format(expected_format, actual_output)
        logger.info(f"大模型验证结果：{result}")
        
        # 解析结果
        if result.startswith("通过"):
            test_case['status'] = "通过"
            passed += 1
            print("测试结果: 通过")
            test_logger.info(f"测试用例 {test_case['input']} 执行成功。")
        else:
            # 检查大模型返回的结果是否包含'通过'关键词（可能在理由部分）
            if "通过" in result:
                test_case['status'] = "通过"
                passed += 1
                print("测试结果: 通过")
                test_logger.info(f"测试用例 {test_case['input']} 执行成功。")
            else:
                test_case['status'] = "失败"
                failed += 1
                print("测试结果: 失败")
                print(f"期望输出格式: {expected_format}")
                print(f"实际输出: {actual_output}")
                test_logger.info(f"测试用例 {test_case['input']} 执行失败。")
                test_logger.info(f"  期望输出格式: {expected_format}")
                test_logger.info(f"  实际输出: {actual_output}")
        print("-----------------------------")
        test_logger.info(f"测试用例 {test_case['input']} 原始数据：")
        test_logger.info(f"  输入: {test_case['input']}")
        test_logger.info(f"  测试目的: {test_case['purpose']}")
        test_logger.info(f"  期望输出格式: {test_case['expected_output_format']}")
        test_logger.info(f"  实际输出: {test_case['actual_output']}")
        test_logger.info(f"  测试状态: {test_case['status']}")
        test_logger.info("----------------------------------------")
    
    # 写回所有测试结果（不仅仅是选中的）
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'test_cases.yaml'), 'w', encoding='utf-8') as file:
        yaml.dump(test_cases, file, allow_unicode=True, sort_keys=False)
    
    # 输出测试摘要
    summary = f"\n测试完成: 通过={passed}, 失败={failed}"
    print(summary)
    test_logger.info(summary)

def main():
    # 创建日志记录器
    test_logger = None
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 创建文件处理器
    log_filename = os.path.join(logs_dir, 'test_execution.log')
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # 将处理器添加到记录器
    test_logger = logging.getLogger('test_execution')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(file_handler)
    
    try:
        plan_agent = PlanAgent()
        data_query_agent = DataQueryAgent()
        rule_config_agent = RuleConfigAgent()  # 添加这一行来创建rule_config_agent实例
        rule_executor_agent = RuleExecutorAgent()
        context_manager = ContextManager()

        logger.info("程序初始化成功")
        
        # 新增逻辑：让用户选择是从测试用例运行还是从终端输入
        while True:
            mode_choice = input("请选择运行模式：\n1. 从test_cases.yaml读取测试样例\n2. 从终端获取用户输入\n输入数字选择模式（默认使用模式2）: ").strip()
            if mode_choice == '1':
                logger.info("用户选择从测试用例运行")
                # 运行测试用例
                run_tests(data_query_agent, plan_agent, rule_executor_agent, rule_config_agent, context_manager, test_logger)
                break  # 测试完成后退出
            elif mode_choice == '' or mode_choice == '2':
                logger.info("用户选择从终端获取用户输入")
                break  # 继续进入交互式输入模式
            else:
                print("输入无效，请输入1或2")
        
        # 原来的交互式输入模式
        while True:
            # 如果是测试模式且已执行完成，则跳过交互模式
            if mode_choice == '1':
                break
            
            user_input = input("\n请输入您的需求（输入'exit'退出）：").strip()
            if not user_input:
                print("输入不能为空，请重新输入！")
                logger.warning("空输入尝试")
                continue
            if user_input.lower() == 'exit':
                logger.info("用户请求退出程序")
                break

            # 使用上下文扩展用户输入
            expanded_input = context_manager.expand_query_with_context(user_input)
            
            # 记录用户输入和改写后的输入
            logger.info(f"用户输入: {user_input}")
            logger.info(f"改写后的输入: {expanded_input}")
            
            agent_type = plan_agent.determine_agent(expanded_input)
            logger.info(f"识别到的代理类型: {agent_type}")
            
            if agent_type == "data_query":
                result = data_query_agent.handle_query(expanded_input)
            elif agent_type == "rule_executor":
                rule_id = user_input.replace("执行规则", "").strip()
                result = rule_executor_agent.execute_rule(rule_id)
            elif agent_type == "rule_config":
                result = rule_config_agent.handle_rule_config(expanded_input)
            else:
                result = "无法识别您的需求类型，请重新描述。"
                
            # 更新上下文
            context_manager.update_context(expanded_input, result)
            
            # 记录输出结果
            logger.info(f"给用户的输出: {result}")
            print(result)

    except Exception as e:
        logger.error("程序运行时发生错误: {}".format(traceback.format_exc()))

if __name__ == "__main__":
    main()
