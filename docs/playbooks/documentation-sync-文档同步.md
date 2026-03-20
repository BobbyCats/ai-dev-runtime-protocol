# 文档同步（Documentation Sync）

适用场景：

- 任何非 trivial 改动
- 新增命令、目录、模板、工件、阶段门
- README 看起来还在，但描述的已经不是当前系统

## 这一步为什么单独存在

文档漂移不是“顺手没改”的小问题，而是会直接误导下一次开发、下一位 Agent 和未来的你自己。

最常见的错误不是完全不改文档，而是：

- 代码和流程已经变了
- 但 README 只是底部追加了一条更新
- 结果整篇文档的主叙事还停在旧版本

## 标准顺序

1. 先生成 `文档同步包（doc-sync）`
2. 先判断这次是 `targeted-update`、`section-rewrite` 还是 `full-rewrite`
3. README 先改
4. 再改 `ONBOARDING.md`
5. 再改 `AGENTS.md`
6. 再改架构说明、playbook、模板、示例

## 什么时候该整篇重写 README

满足下面任意一种，通常就该整篇或大段重写，而不是只追加：

- 命令表面变了
- 阶段顺序变了
- 系统定位变了
- 仓库结构和主要入口变了
- 这次变更影响了多个核心文档

## CLI 用法

```bash
python -m aidrp doc-sync \
  --project-root . \
  --title "Workflow refresh 工作流升级" \
  --summary "Added new stages, commands, and closing discipline." \
  --changed-file src/aidrp/cli.py \
  --changed-file README.md
```

推荐模板：

- [templates/documentation-sync-文档同步包.md](../../templates/documentation-sync-文档同步包.md)

## 硬规则

- README 是当前系统地图，不是 changelog
- 如果主结构变了，不允许只追加一段补丁说明
- 核心文档之间的默认工作顺序必须一致
- 没过文档同步，不算正式收尾
