# Adapter | 适配器: React + Node Monorepo

适用于：

- 前端一个 app
- 后端一个 app
- 共享包若干

## 推荐的 `.aidrp/config.json` 调整

- 把 `apps/web/src/main.tsx` 和 `apps/api/src/index.ts` 放进 `preferred_entry_files`
- 为 `quick / precommit / ship` 配好命令
- 把 `packages/shared/` 视为高信号区域

## 常见阅读顺序

1. `README.md`
2. `AGENTS.md`
3. `package.json`
4. `apps/web/package.json`
5. `apps/api/package.json`
6. `packages/shared/*`
7. 当前任务包里的候选文件

## 常见风险点

- 前后端类型漂移
- 生成代码过期
- 环境变量读法不一致
- API 改了但前端缓存没失效
