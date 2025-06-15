import logging
import os
from datetime import datetime

def setup_logger():
    """设置全局日志记录器"""
    # 创建logs目录（如果不存在）
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s] %(message)s')
    
    # 创建控制台处理器，并设置级别为WARNING
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)  # 仅记录WARNING及以上级别日志到控制台
    
    # 创建文件处理器
    log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)  # 文件记录INFO及以上级别日志
    
    # 获取根日志记录器并添加处理器
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    
    return logger

# 全局日志记录器
logger = setup_logger()