from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from aidrp.utils import now_iso, slugify, write_json, write_text


def _normalize_hex(value: str) -> str:
    cleaned = value.strip().lstrip("#")
    if len(cleaned) == 3:
        cleaned = "".join(char * 2 for char in cleaned)
    if len(cleaned) != 6:
        raise ValueError(f"Invalid hex color: {value}")
    return f"#{cleaned.upper()}"


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    color = _normalize_hex(value).lstrip("#")
    return tuple(int(color[index : index + 2], 16) for index in range(0, 6, 2))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _mix(color_a: str, color_b: str, ratio: float) -> str:
    left = _hex_to_rgb(color_a)
    right = _hex_to_rgb(color_b)
    blended = tuple(
        round(left[index] * (1 - ratio) + right[index] * ratio)
        for index in range(3)
    )
    return _rgb_to_hex(blended)


def _scale(base: str) -> dict[str, str]:
    normalized = _normalize_hex(base)
    return {
        "50": _mix(normalized, "#FFFFFF", 0.90),
        "100": _mix(normalized, "#FFFFFF", 0.78),
        "200": _mix(normalized, "#FFFFFF", 0.62),
        "300": _mix(normalized, "#FFFFFF", 0.42),
        "400": _mix(normalized, "#FFFFFF", 0.18),
        "500": normalized,
        "600": _mix(normalized, "#000000", 0.12),
        "700": _mix(normalized, "#000000", 0.24),
        "800": _mix(normalized, "#000000", 0.38),
        "900": _mix(normalized, "#000000", 0.54),
    }


def build_design_token_pack(
    *,
    title: str,
    product_surface: str,
    brand_direction: str,
    brand_color: str,
    accent_color: str,
    canvas_color: str,
    text_color: str,
    font_sans: str,
    font_display: str,
    font_mono: str,
    design_principles: list[str],
    modes: list[str],
    guardrails: list[str],
) -> dict[str, Any]:
    brand = _scale(brand_color)
    accent = _scale(accent_color)
    canvas = _normalize_hex(canvas_color)
    text = _normalize_hex(text_color)
    token_pack_id = slugify(title)

    principles = design_principles or [
        "先定义语义，再写组件，不要在组件里直接写死颜色和间距。",
        "用同一套令牌同时约束 Web、App 和设计稿，减少平台漂移。",
        "优先稳定、耐看、可扩展，不为了一时的炫技破坏一致性。",
    ]
    mode_list = modes or ["light"]
    visual_guardrails = guardrails or [
        "组件代码里不要直接写十六进制颜色。",
        "新增尺寸、颜色、阴影前，先确认现有令牌是否已能表达。",
        "语义令牌命名不要绑具体颜色名，例如不要用 blue-primary 这种写法。",
    ]

    primitives = {
        "color": {
            "brand": brand,
            "accent": accent,
            "neutral": {
                "0": canvas,
                "50": "#F8FAFC",
                "100": "#F1F5F9",
                "200": "#E2E8F0",
                "300": "#CBD5E1",
                "400": "#94A3B8",
                "500": "#64748B",
                "600": "#475569",
                "700": "#334155",
                "800": "#1E293B",
                "900": text,
            },
            "success": _scale("#16A34A"),
            "warning": _scale("#D97706"),
            "danger": _scale("#DC2626"),
            "info": _scale("#2563EB"),
        },
        "spacing": {
            "0": "0px",
            "1": "4px",
            "2": "8px",
            "3": "12px",
            "4": "16px",
            "5": "20px",
            "6": "24px",
            "8": "32px",
            "10": "40px",
            "12": "48px",
            "16": "64px",
        },
        "radius": {
            "xs": "6px",
            "sm": "10px",
            "md": "14px",
            "lg": "20px",
            "xl": "28px",
            "pill": "999px",
        },
        "typography": {
            "font": {
                "sans": font_sans,
                "display": font_display,
                "mono": font_mono,
            },
            "size": {
                "xs": "12px",
                "sm": "14px",
                "md": "16px",
                "lg": "18px",
                "xl": "24px",
                "2xl": "32px",
            },
            "line_height": {
                "tight": "1.2",
                "body": "1.5",
                "relaxed": "1.7",
            },
            "weight": {
                "regular": "400",
                "medium": "500",
                "semibold": "600",
                "bold": "700",
            },
        },
        "shadow": {
            "sm": "0 1px 2px rgba(15, 23, 42, 0.08)",
            "md": "0 10px 24px rgba(15, 23, 42, 0.12)",
            "lg": "0 18px 48px rgba(15, 23, 42, 0.16)",
        },
        "motion": {
            "duration": {
                "fast": "120ms",
                "normal": "220ms",
                "slow": "320ms",
            },
            "easing": {
                "standard": "cubic-bezier(0.2, 0, 0, 1)",
                "emphasized": "cubic-bezier(0.2, 0.8, 0.2, 1)",
            },
        },
    }

    semantics = {
        "surface.canvas": "{color.neutral.0}",
        "surface.panel": "{color.neutral.50}",
        "surface.panel-elevated": "{color.neutral.0}",
        "surface.inverse": "{color.neutral.900}",
        "text.primary": "{color.neutral.900}",
        "text.secondary": "{color.neutral.600}",
        "text.tertiary": "{color.neutral.500}",
        "text.inverse": "{color.neutral.0}",
        "border.subtle": "{color.neutral.200}",
        "border.default": "{color.neutral.300}",
        "border.strong": "{color.neutral.500}",
        "accent.primary": "{color.brand.500}",
        "accent.primary-hover": "{color.brand.600}",
        "accent.secondary": "{color.accent.500}",
        "accent.on-primary": "{color.neutral.0}",
        "feedback.success": "{color.success.500}",
        "feedback.warning": "{color.warning.500}",
        "feedback.danger": "{color.danger.500}",
        "feedback.info": "{color.info.500}",
        "focus.ring": "{color.brand.300}",
    }

    component_guidance = [
        {
            "component": "page-shell",
            "tokens": ["surface.canvas", "text.primary", "spacing.6", "spacing.8"],
            "notes": "页面骨架保持透气，不要用过重阴影和过满填充。标题优先用 display 字体。",
        },
        {
            "component": "conversation-bubble",
            "tokens": ["surface.panel", "accent.primary", "text.primary", "radius.lg"],
            "notes": "AI 产品的对话气质要明确，自己发出的消息和系统回复要有清楚层级，但不要靠花哨颜色取胜。",
        },
        {
            "component": "timeline-card",
            "tokens": ["surface.panel-elevated", "border.subtle", "shadow.sm", "radius.xl"],
            "notes": "时间卡片优先解决扫描效率，状态强调用 semantic token，不直接写业务色。",
        },
        {
            "component": "primary-action",
            "tokens": ["accent.primary", "accent.on-primary", "radius.pill", "shadow.sm"],
            "notes": "主操作按钮要稳定，不要在一个页面同时出现多个视觉上等权的主按钮。",
        },
        {
            "component": "input-field",
            "tokens": ["surface.panel", "border.default", "focus.ring", "text.primary"],
            "notes": "输入框优先稳定和可读，不要靠复杂渐变制造存在感。",
        },
    ]

    export_targets = [
        "CSS variables: `:root { --color-accent-primary: ... }`",
        "Tailwind theme extension or design-tokens.js export",
        "Native app bridge map for iOS / Android style constants",
        "Design tool reference table for Figma or Sketch",
    ]

    return {
        "schema_version": "0.1.0",
        "token_pack_id": token_pack_id,
        "generated_at": now_iso(),
        "title": title,
        "product_surface": product_surface,
        "brand_direction": brand_direction,
        "design_principles": principles,
        "modes": mode_list,
        "primitives": primitives,
        "semantics": semantics,
        "component_guidance": component_guidance,
        "guardrails": visual_guardrails,
        "export_targets": export_targets,
    }


def design_token_pack_to_markdown(pack: dict[str, Any]) -> str:
    lines = [
        f"# Design Token Pack | 设计令牌包: {pack['title']}",
        "",
        f"- Token Pack ID | 令牌包 ID: `{pack['token_pack_id']}`",
        f"- Generated | 生成时间: `{pack['generated_at']}`",
        f"- Product Surface | 产品界面: {pack['product_surface']}",
        "",
        "## Brand Direction | 视觉方向",
        "",
        pack["brand_direction"],
        "",
        "## Design Principles | 设计原则",
        "",
    ]
    for item in pack["design_principles"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Modes | 模式", ""])
    for item in pack["modes"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Semantic Tokens | 语义令牌", ""])
    for key, value in pack["semantics"].items():
        lines.append(f"- `{key}` -> `{value}`")

    lines.extend(["", "## Component Guidance | 组件指导", ""])
    for item in pack["component_guidance"]:
        lines.append(
            f"- `{item['component']}`: {item['notes']} Tokens: {', '.join(f'`{token}`' for token in item['tokens'])}"
        )

    lines.extend(["", "## Guardrails | 护栏", ""])
    for item in pack["guardrails"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Export Targets | 导出目标", ""])
    for item in pack["export_targets"]:
        lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def design_token_pack_to_html(pack: dict[str, Any]) -> str:
    color = pack["primitives"]["color"]
    typography = pack["primitives"]["typography"]
    radius = pack["primitives"]["radius"]
    shadow = pack["primitives"]["shadow"]
    spacing = pack["primitives"]["spacing"]
    semantics = pack["semantics"]

    swatches = []
    for family in ("brand", "accent", "neutral"):
        for scale, value in color[family].items():
            swatches.append(
                f"""
                <div class="swatch">
                  <div class="swatch-chip" style="background:{html.escape(value)};"></div>
                  <div class="swatch-label">{html.escape(f"{family}.{scale}")}</div>
                  <div class="swatch-value">{html.escape(value)}</div>
                </div>
                """
            )

    semantics_rows = []
    for key, value in semantics.items():
        semantics_rows.append(
            f"""
            <tr>
              <td>{html.escape(key)}</td>
              <td><code>{html.escape(value)}</code></td>
            </tr>
            """
        )

    component_cards = []
    for item in pack["component_guidance"]:
        tokens = "".join(f"<li><code>{html.escape(token)}</code></li>" for token in item["tokens"])
        component_cards.append(
            f"""
            <article class="component-card">
              <h3>{html.escape(item['component'])}</h3>
              <p>{html.escape(item['notes'])}</p>
              <ul>{tokens}</ul>
            </article>
            """
        )

    principles = "".join(f"<li>{html.escape(item)}</li>" for item in pack["design_principles"])
    guardrails = "".join(f"<li>{html.escape(item)}</li>" for item in pack["guardrails"])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(pack['title'])} | Design Token Preview</title>
  <style>
    :root {{
      --surface-canvas: {color['neutral']['0']};
      --surface-panel: {color['neutral']['50']};
      --text-primary: {color['neutral']['900']};
      --text-secondary: {color['neutral']['600']};
      --accent-primary: {color['brand']['500']};
      --accent-secondary: {color['accent']['500']};
      --border-subtle: {color['neutral']['200']};
      --radius-lg: {radius['lg']};
      --radius-xl: {radius['xl']};
      --shadow-md: {shadow['md']};
      --spacing-4: {spacing['4']};
      --spacing-6: {spacing['6']};
      --spacing-8: {spacing['8']};
      --font-sans: {typography['font']['sans']};
      --font-display: {typography['font']['display']};
      --font-mono: {typography['font']['mono']};
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background:
        radial-gradient(circle at top left, {color['brand']['100']}, transparent 28%),
        radial-gradient(circle at top right, {color['accent']['100']}, transparent 24%),
        var(--surface-canvas);
      color: var(--text-primary);
    }}
    .page {{
      max-width: 1200px;
      margin: 0 auto;
      padding: {spacing['10']} {spacing['6']} {spacing['16']};
    }}
    .hero {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: {spacing['8']};
      align-items: stretch;
      margin-bottom: {spacing['10']};
    }}
    .hero-card, .preview-card, .section {{
      background: rgba(255, 255, 255, 0.86);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-subtle);
      border-radius: {radius['xl']};
      box-shadow: var(--shadow-md);
    }}
    .hero-card {{
      padding: {spacing['8']};
    }}
    .hero h1 {{
      margin: 0 0 {spacing['3']};
      font-family: var(--font-display);
      font-size: {typography['size']['2xl']};
      line-height: {typography['line_height']['tight']};
    }}
    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 14px;
      border-radius: {radius['pill']};
      background: {color['brand']['100']};
      color: {color['brand']['700']};
      font-weight: {typography['weight']['semibold']};
      margin-bottom: {spacing['4']};
    }}
    .muted {{
      color: var(--text-secondary);
    }}
    .hero ul, .section ul {{
      padding-left: 18px;
      margin: {spacing['4']} 0 0;
    }}
    .preview-card {{
      padding: {spacing['6']};
      display: grid;
      gap: {spacing['4']};
    }}
    .mock-page {{
      padding: {spacing['6']};
      border-radius: {radius['lg']};
      background: {color['neutral']['0']};
      border: 1px solid {color['neutral']['200']};
    }}
    .mock-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: {spacing['5']};
    }}
    .mock-badge {{
      padding: 6px 12px;
      border-radius: {radius['pill']};
      background: {color['brand']['100']};
      color: {color['brand']['700']};
      font-size: {typography['size']['sm']};
      font-weight: {typography['weight']['medium']};
    }}
    .bubble {{
      max-width: 84%;
      padding: {spacing['4']} {spacing['5']};
      border-radius: {radius['lg']};
      margin-bottom: {spacing['3']};
      line-height: {typography['line_height']['body']};
    }}
    .bubble-user {{
      margin-left: auto;
      background: {color['brand']['500']};
      color: {color['neutral']['0']};
    }}
    .bubble-agent {{
      background: {color['neutral']['50']};
      border: 1px solid {color['neutral']['200']};
    }}
    .timeline-card {{
      border: 1px solid {color['neutral']['200']};
      border-radius: {radius['xl']};
      padding: {spacing['5']};
      box-shadow: {shadow['sm']};
      display: grid;
      gap: {spacing['2']};
      background: {color['neutral']['0']};
    }}
    .button-row {{
      display: flex;
      gap: {spacing['3']};
      margin-top: {spacing['4']};
    }}
    .btn {{
      padding: 12px 18px;
      border-radius: {radius['pill']};
      border: none;
      font: inherit;
      font-weight: {typography['weight']['semibold']};
    }}
    .btn-primary {{
      background: {color['brand']['500']};
      color: {color['neutral']['0']};
      box-shadow: {shadow['sm']};
    }}
    .btn-secondary {{
      background: {color['accent']['100']};
      color: {color['accent']['700']};
    }}
    .section {{
      padding: {spacing['6']};
      margin-bottom: {spacing['6']};
    }}
    .section h2 {{
      margin: 0 0 {spacing['4']};
      font-size: {typography['size']['xl']};
    }}
    .swatch-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: {spacing['4']};
    }}
    .swatch {{
      padding: {spacing['3']};
      border: 1px solid {color['neutral']['200']};
      border-radius: {radius['lg']};
      background: {color['neutral']['0']};
    }}
    .swatch-chip {{
      height: 72px;
      border-radius: {radius['md']};
      border: 1px solid rgba(15, 23, 42, 0.08);
      margin-bottom: {spacing['3']};
    }}
    .swatch-label {{
      font-weight: {typography['weight']['semibold']};
      margin-bottom: 4px;
    }}
    .swatch-value, code {{
      font-family: var(--font-mono);
      font-size: {typography['size']['xs']};
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 12px;
      border-bottom: 1px solid {color['neutral']['200']};
      text-align: left;
      vertical-align: top;
    }}
    .component-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: {spacing['4']};
    }}
    .component-card {{
      border: 1px solid {color['neutral']['200']};
      border-radius: {radius['lg']};
      padding: {spacing['4']};
      background: {color['neutral']['0']};
    }}
    .component-card h3 {{
      margin-top: 0;
      margin-bottom: {spacing['3']};
    }}
    .component-card ul {{
      margin: {spacing['3']} 0 0;
      padding-left: 18px;
    }}
    @media (max-width: 900px) {{
      .hero {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="hero-card">
        <div class="eyebrow">Design Token Preview / 设计令牌预览</div>
        <h1>{html.escape(pack['title'])}</h1>
        <p class="muted">{html.escape(pack['product_surface'])}</p>
        <p>{html.escape(pack['brand_direction'])}</p>
        <ul>{principles}</ul>
      </div>
      <div class="preview-card">
        <div class="mock-page">
          <div class="mock-header">
            <div>
              <strong>Today / 今天</strong>
              <div class="muted">AI-native schedule assistant</div>
            </div>
            <div class="mock-badge">Live QA Ready</div>
          </div>
          <div class="bubble bubble-agent">你明天下午 3 点和产品团队有一个评审会。</div>
          <div class="bubble bubble-user">把它改到下班以后，并且给我预留 30 分钟路程。</div>
          <div class="timeline-card">
            <strong>Product Review / 产品评审</strong>
            <span class="muted">19:00 - 20:00 · 深圳</span>
            <span>Tokens: <code>surface.panel-elevated</code>, <code>border.subtle</code>, <code>radius.xl</code></span>
          </div>
          <div class="button-row">
            <button class="btn btn-primary">确认计划</button>
            <button class="btn btn-secondary">稍后再说</button>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Color Scales / 色板刻度</h2>
      <div class="swatch-grid">
        {''.join(swatches)}
      </div>
    </section>

    <section class="section">
      <h2>Semantic Tokens / 语义令牌</h2>
      <table>
        <thead>
          <tr><th>Token</th><th>Value</th></tr>
        </thead>
        <tbody>
          {''.join(semantics_rows)}
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>Component Guidance / 组件指导</h2>
      <div class="component-grid">
        {''.join(component_cards)}
      </div>
    </section>

    <section class="section">
      <h2>Guardrails / 护栏</h2>
      <ul>{guardrails}</ul>
    </section>
  </main>
</body>
</html>
"""


def write_design_token_pack(
    pack: dict[str, Any],
    output_json: Path,
    output_markdown: Path,
    output_html: Path | None = None,
) -> None:
    write_json(output_json, pack)
    write_text(output_markdown, design_token_pack_to_markdown(pack))
    if output_html is not None:
        write_text(output_html, design_token_pack_to_html(pack))
