# GitHub Action CI 配置

本项目使用 GitHub Actions 实现自动化测试和代码风格检查。

## 工作流说明

- **ci.yml**：在每次推送或拉取请求时运行，执行以下任务：
  - 安装依赖
  - 运行测试用例
  - 检查代码风格（flake8）
  - 构建文档（可选）

## 如何启用

1. 在项目根目录下创建 `.github/workflows/` 文件夹
2. 将 `ci.yml` 放入该文件夹
3. 提交代码到 GitHub 仓库后，GitHub Actions 会自动识别并运行工作流