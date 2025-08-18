"""Emoji support for the game."""

from .download import _PNG_DIR, download


if not _PNG_DIR.exists():
    _PNG_DIR.mkdir(parents=True)
    download()
