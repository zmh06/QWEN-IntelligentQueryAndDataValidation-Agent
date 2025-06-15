# 常见问题解答（FAQ）

## 🤔 项目运行相关

### Q1: 运行程序时报错 `DASHSCOPE_API_KEY environment variable not set`，怎么办？

A: 你需要设置 DashScope 的 API Key 环境变量。在命令行中执行以下命令：

```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

如果你使用 Windows 系统，可以使用以下命令设置环境变量：

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your_api_key_here", [EnvironmentVariableTarget]::User)
```

> ⚠️ 请将 `your_api_key_here` 替换为你自己的 DashScope API Key。

### Q2: 测试用例执行后状态一直是失败，但输出看起来是正确的？

A: 当前测试逻辑依赖大模型判断输出是否符合预期格式。确保你的 LLM 返回了明确的 `通过` 或 `失败` 判断。如果持续出现问题，可尝试优化提示词或调整期望输出格式。

### Q3: 如何添加新的测试用例？

A: 所有测试用例都定义在 `tests/test_cases.yaml` 文件中。你可以按照已有结构新增测试条目，包括：
- `input`: 用户输入的自然语言
- `expected_output_format`: 期望的输出格式描述
- `purpose`: 测试目的

### Q4: 为什么测试完成后会自动进入交互模式？

A: 此行为已在最新版本中修复。选择测试模式后，程序将在测试完成后自动退出交互模式。

### Q5: 如何为项目贡献代码？

A: 请参考 [CONTRIBUTING.md](docs/contributing.md) 文档中的详细说明，了解如何 Fork、提交 PR 和遵循编码规范。

### Q6: 是否支持其他大模型服务？

A: 当前实现基于 DashScope 的 Qwen 模型。如果你想集成其他 LLM 服务（如 OpenAI、HuggingFace），欢迎提交 PR 实现多模型适配器设计！