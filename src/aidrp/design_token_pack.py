from __future__ import annotations

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


def write_design_token_pack(pack: dict[str, Any], output_json: Path, output_markdown: Path) -> None:
    write_json(output_json, pack)
    write_text(output_markdown, design_token_pack_to_markdown(pack))
