"""One-off diagnostic: test the live quality gate against a known case, on
the server itself, to rule out any local/deployed drift."""

from app.schemas.schemas import SignalIngest
from app.services.detector_service import _passes_content_quality_gate
from app.services.text_filters import RELEVANCE_TERMS

TITLE = "Keychron announces first open-source firmware for gaming mice"


def main() -> None:
    lowered = TITLE.lower()
    matches = [t for t in RELEVANCE_TERMS if t in lowered]
    print("matched terms:", matches)

    signal = SignalIngest(
        title=TITLE,
        content=None,
        source_type="hackernews",
        source_id="diag",
        upvotes=1,
        comments=0,
    )
    print("gate result:", _passes_content_quality_gate(signal))


if __name__ == "__main__":
    main()
