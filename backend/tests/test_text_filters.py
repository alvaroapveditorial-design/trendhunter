"""Tests for the shared non-English content filter."""

from app.services.text_filters import looks_non_english


def test_detects_chinese_description():
    text = "⚡需求分析效率提升 200%！全球首个为 AI 编程时代设计的团队协作 MCP 服务器"
    assert looks_non_english(text) is True


def test_detects_mixed_chinese_and_english():
    text = "Real-time token widget for Claude Code | 为 AI Tools 打造的即时Token、成本与限额监控桌面组件"
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
