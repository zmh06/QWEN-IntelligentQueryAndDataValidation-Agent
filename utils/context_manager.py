class ContextManager:
    """管理对话上下文，用于查询优化和意图识别"""
    def __init__(self):
        self.previous_query = None
        self.previous_result = None

    def update_context(self, query, result):
        """更新上下文信息"""
        self.previous_query = query
        self.previous_result = result

    def expand_query_with_context(self, current_query):
        """使用上下文信息扩写当前查询"""
        if not current_query or not self.previous_query:
            return current_query

        # 如果检测到模糊的上下文引用，则扩展查询
        if any(phrase in current_query.lower() for phrase in ['分别是', '有哪些', '哪几个', '具体是']):
            return f"{self.previous_query} {current_query}"
            
        return current_query