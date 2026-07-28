"""Tests for the shared non-English content filter."""

from app.services.text_filters import looks_non_english


def test_detects_chinese_description():
    text = "⚡需求分析效率提升 200%！全球首个为 AI 编程时代设计的团队协作 MCP 服务器"
    assert looks_non_english(text) is True


def test_detects_mixed_chinese_and_english():
    text = "Real-time token widget for Claude Code | 为 AI Tools 打造的即时Token、成本与限额监控桌面组件"
    assert looks_non_english(text) is True


def test_detects_english_description_with_translated_clause_appended():
    """Regression test: a description that's mostly English but has a full
    translated clause tacked on after a separator must still be caught, even
    though the Chinese portion alone is a minority of the total characters."""
    text = (
        "Real-time token, cost, and AI limits widget with multi-device sync for "
        "Claude Code, Codex, OpenCode, Hermes, OpenClaw, Cursor, Antigravity and "
        "more. | 为 AI Tools 打造的即时Token、成本与限额监控桌面组件，支持多设备同步"
    )
    assert looks_non_english(text) is True


def test_detects_translated_clause_diluted_by_shared_latin_jargon():
    """Regression test: a translated clause padded with the same Latin model
    names/numbers as the English half can dilute the non-Latin ratio below
    threshold when measured over the whole string, even though the clause
    itself is clearly non-English once measured on its own."""
    text = (
        "Open Source Continuous Inference Benchmark Research Platform "
        "— Kimi K2.7-Code, MiniMax M3, DeepSeekv4, GLM5 - GB200 NVL72 vs "
        "MI355X vs B200 vs GB300 NVL72 & soon™ TPUv6e/v7/Trainium2/3 | "
        "开源持续推理基准研究平台 "
        "— Kimi K2.7-Code、MiniMax M3、DeepSeekv4、GLM5 - GB200 "
        "NVL72 vs MI355X vs B200 vs GB300 NVL72，即将推出™ "
        "TPUv6e/v7/Trainium2/3"
    )
    assert looks_non_english(text) is True


def test_allows_plain_english():
    text = "A Model Context Protocol server for searching and analyzing arXiv papers"
    assert looks_non_english(text) is False


def test_allows_english_with_occasional_foreign_word():
    text = "RamaLama is an open-source developer tool, from the French word for llama"
    assert looks_non_english(text) is False


def test_allows_empty_text():
    assert looks_non_english("") is False
    assert looks_non_english(None) is False
