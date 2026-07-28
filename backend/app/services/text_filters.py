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

    Checked per "|"-separated segment, not just over the whole string: a
    translated clause padded with the same Latin model names/numbers as the
    English half (e.g. "... GB300 NVL72 | ... 开源持续推理基准研究平台 ...
    GB300 NVL72") can dilute the non-Latin ratio below threshold when
    measured globally, while the clause itself is clearly non-English.
    """
    if not text:
        return False
    for segment in text.split("|"):
        stripped = re.sub(r"\s+", "", segment)
        if not stripped:
            continue
        non_latin_count = len(_NON_LATIN_SCRIPT_PATTERN.findall(stripped))
        if (non_latin_count / len(stripped)) >= threshold:
            return True
    return False
