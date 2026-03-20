# 可观测性关联（Observability Correlation）

适用场景：

- 你已经开始觉得“让 AI 读代码找 bug”越来越慢
- 一个问题要扫 8 到 10 分钟，token 和上下文一起爆
- 你明明有日志，但 Agent 还是不知道该先看哪里

## 王自如那套真正有价值的地方

不是“有日志”这么简单，而是：

- 给每一次关键动作编号
- 给每一种关键行为编号
- 让 trace、log、计划、工具调用共享同一套关联编号

这样出现 bug 时，Agent 不是从“症状”开始大范围扫，而是：

1. 先拿到关联编号
2. 先缩到对应日志段
3. 再缩到故障阶段
4. 最后才去看代码

## 推荐最小编号集合

- `trace_id`：一条任务链路
- `request_id`：一次入口请求
- `decision_id`：一次关键判断或分支切换
- `plan_id`：一份执行计划
- `tool_call_id`：一次工具执行

## 推荐排查顺序

1. 先按编号 grep 日志
2. 再看故障阶段前后是否缺日志或日志顺序异常
3. 再对照 `decision-trace`
4. 最后再扩大到代码阅读

## 产物要求

- 结构化的可观测性关联卡
- `debug-pack` 里必须优先写入关联编号和 grep 关键词
- 回归用例要保留当时的故障签名

推荐模板：

- [templates/observability-correlation-可观测性关联.md](../../templates/observability-correlation-可观测性关联.md)

## CLI 用法

```bash
python -m aidrp observability-correlation \
  --project-root . \
  --title "Delete event correlation" \
  --trace-id "trace-77" \
  --decision-id "dec-99" \
  --entrypoint "calendar.delete" \
  --failure-stage "executor" \
  --log-file "logs/runtime.log"
```

如果不显式传 `--log-file`，CLI 会尝试根据 `.aidrp/config.json` 里的 `observability.log_globs` 去找候选日志文件。
