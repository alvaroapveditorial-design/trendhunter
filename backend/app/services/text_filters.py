"""Shared lightweight text filters used by the signal collectors.

No translation service or LLM is configured (see docs/HANDOFF_CTO.md) so a
non-English signal can't be translated -- it can only be kept as-is (which
looks broken to an English-only audience) or skipped. These filters skip.
"""

import re

# Unicode ranges for scripts that read as clearly non-English regardless of
# any Latin characters mixed in (emoji, numbers, product names). Covers the
# cases actually seen in ingested GitHub/RSS/HN content: CJK, Cyrillic, Arabic.
_NON_LATIN_SCRIPT_PATTERN = re.compile(
    "["
    "一-鿿"  # CJK unified ideographs (Chinese)
    "぀-ヿ"  # Hiragana / Katakana (Japanese)
    "가-힣"  # Hangul syllables (Korean)
    "Ѐ-ӿ"  # Cyrillic
    "؀-ۿ"  # Arabic
    "]"
)


def looks_non_english(text: str, threshold: float = 0.10) -> bool:
    """True if a meaningful share of the text's characters are non-Latin script.

    A low threshold (10% of non-whitespace characters) is enough to catch
    genuinely non-English content -- including the common case of an English
    description with a full translated clause appended after a separator
    ("... | 为 AI Tools 打造的...") -- while tolerating the occasional foreign
    proper noun inside an otherwise-English title/description.
    """
    if not text:
        return False
    stripped = re.sub(r"\s+", "", text)
    if not stripped:
        return False
    non_latin_count = len(_NON_LATIN_SCRIPT_PATTERN.findall(stripped))
    return (non_latin_count / len(stripped)) >= threshold
