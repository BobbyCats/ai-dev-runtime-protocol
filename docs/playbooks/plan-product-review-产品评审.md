# 产品评审（Product Review）

适用场景：

- 需求刚收敛，但第一版范围还没稳
- 你担心一上来就做太大
- 你怀疑这件事其实不是工程问题，而是 scope 问题

## 这一步的目标

不是设计系统，而是回答下面这几个问题：

- 第一版到底服务谁
- 第一版最小有价值场景是什么
- 哪些东西这次明确不做
- 现在应该扩 scope、保持 scope，还是缩 scope

## 标准问题

- 目标用户是谁
- 他现在最痛的动作是什么
- 什么场景最先发生，而且频率最高
- 第一版只做好一件事，应该是哪一件
- 哪些功能听起来想要，但现在不该做
- 做成什么样就算值得继续投资源

## 输出要求

至少要落下这些结论：

- 核心用户
- 核心问题
- 最小有价值切片
- 非目标
- 成功标准
- `扩 / 保持 / 缩` 的 scope 决策

推荐模板：

- [templates/plan-product-review-产品评审.md](../../templates/plan-product-review-产品评审.md)

如果你已经有 `requirement-brief`，建议直接生成结构化工件，而不是只写散文结论：

```bash
python -m aidrp product-review \
  --brief .aidrp/briefs/<brief-id>.json \
  --current-goal "把第一版压成可交付的最小切片" \
  --scope-decision 保持 \
  --scope-reason "第一版边界已经清楚，先不要扩张" \
  --output-dir .aidrp/product-reviews
```

这样后面的工程评审、教程、示例和测试都可以直接复用同一份事实来源。

## 硬规则

- 没做 scope 决策，不要进入工程评审
- 不要在这一步提前争论技术细节
- 发现需求其实还没讲清楚时，退回需求访谈或需求简报
- 如果第一版切片说不出来，通常说明做得太大
