# Data QA Agent 测试用例说明

本项目使用 `tests/test_cases.yaml` 文件来存储预设的测试用例，用于验证系统各模块的功能是否正常工作。

## 🧪 测试用例结构

每个测试用例包含以下字段：

- `input`: 用户输入的自然语言查询
- `expected_output_format`: 期望输出格式描述（如自然语言、表格等）
- `purpose`: 测试目的，说明该用例验证的功能点
- `actual_output`: 实际输出结果（由程序运行时自动填充）
- `status`: 测试状态（通过/失败，由程序运行时自动更新）

## ✅ 示例测试用例

```yaml
- input: 数据库中现在有多少张表？
  expected_output_format: 自然语言描述，如'数据库中现在有X张表。'
  purpose: 验证系统能够正确统计并返回数据库中的表数量
  actual_output: 数据库中目前有3张表。
  status: 通过
```

## 📝 使用方式

1. 启动程序时选择 **模式1**（从 `test_cases.yaml` 读取测试样例）。
2. 程序会加载所有测试用例，并提示你选择执行全部或部分测试。
3. 每个测试用例执行完成后，其 `actual_output` 和 `status` 字段将被更新。
4. 所有测试结果都会记录在 `logs/test_execution.log` 中。

## 🧩 添加新测试用例

你可以按照已有结构新增测试条目，例如：

```yaml
- input: 显示所有销售数据
  expected_output_format: 表格格式，包含id、region、sales、order_date字段，使用psql风格的表格
  purpose: 验证系统能够正确查询并格式化显示所有销售数据
  actual_output: 
  status: 
```

> 💡 提示：实际输出和状态会在测试运行后自动填充。

## 📌 注意事项

- 测试逻辑依赖大模型判断输出是否符合预期格式，请确保网络连接正常且 API Key 有效。
- 如果发现测试误判（如应为“通过”却被标记为“失败”），可尝试优化提示词或调整期望输出格式描述。