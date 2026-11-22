# ==========================================================================
# PURPOSE: CONFIG LOGGING
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================

import logging
import sys

# ==========================================================================
# CONFIG LOGGING
# ==========================================================================


def setup_logging(level: str = "INFO") -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    if not any(
        isinstance(h, logging.StreamHandler) and getattr(h, "_template_managed", False)
        for h in root_logger.handlers
    ):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)
        handler.setFormatter(formatter)
        handler._template_managed = True  # type: ignore[attr-defined]
        root_logger.addHandler(handler)

    if numeric_level > logging.DEBUG:
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = True
    return logger
