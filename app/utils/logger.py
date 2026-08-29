"""
One logger config shared across the app instead of print() statements.
Usage:  from app.utils.logger import logger
"""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("coursemind")
