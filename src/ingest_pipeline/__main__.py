from __future__ import annotations

from .config import get_settings
from .logging import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(settings)
    print("ingest_pipeline image is ready. CLI will be added in a later module.")


if __name__ == "__main__":
    main()
