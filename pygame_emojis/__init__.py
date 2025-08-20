"""Emoji support for the game."""
import logging
from pathlib import Path
import emoji
import io

import pygame

from pygame_emojis.emojis_data.download import _EMOJIS_DIR

logger = logging.getLogger("pygame_emojis")


class EmojiNotFound(Exception):
    ...


def find_code(emoji_: str) -> list[str]:
    """Find the unicode values of the emoji.

    Return a list with all the unicodes.
    """
    # Convert the emoji to a byte str of the emoji
    logger.debug(f"{emoji_}")
    emoji_ = emoji.emojize(emoji_)
    logger.debug(f"{bytes(emoji_, 'utf-8')=}")
    # Convert the byte str to the hexadecimal code

    return [f"{ord(e):X}" for e in emoji_]

def find_emoji(emoji_: str) -> Path | None:
    """Find an emoji image file (regardless of extension) based on the emoji.

    It uses the following method:

    * Converts the emoji to Unicode codepoints.
    * Searches for files whose names start with the codepoints.
    * If none are found, shortens the code progressively and retries.
    """

    try:
        code_list = find_code(emoji_)
    except Exception as e:
        raise EmojiNotFound(emoji_) from e
    logger.debug(f"{code_list=}")

    while code_list:
        code = "-".join(code_list)

        # Check for exact filename match (any extension)
        for f in _EMOJIS_DIR.iterdir():
            if f.stem == code:
                return f

        # Check for more complex matches (e.g. with variation selectors, skin tones, etc.)
        possible_files = [f for f in _EMOJIS_DIR.glob(f"{code}*") if f.is_file()]
        if possible_files:
            return possible_files[0]

        # Reduce specificity and try again
        code_list.pop()

    return None


def load_emoji(
    emoji_: str, size: tuple[int, int] | int = None
) -> pygame.Surface:
    """Load a surface corresponding to the emoji.

    If not found, raise a FileNotFoundError.
    """

    file = find_emoji(emoji_)
    logger.debug(f"{file=}")
    if file is not None:
        return emoji_to_surface(file, size)
    else:
        raise FileNotFoundError(f"No file available for emoji {emoji_}")



def emoji_to_surface(filename, size: tuple[int, int] | int = None) -> pygame.Surface:
    if str(filename).lower().endswith('.png'): # Convert to str as filename is path object
        """Load a png image and scale it based on the input size."""
        # Load the image
        image = pygame.image.load(filename)
        
        # Check if we need to scale the image
        if size:
            # If the size is a single integer (e.g., width), scale uniformly
            if isinstance(size, int):
                width = height = size
            # If the size is a tuple (e.g., (width, height)), use those values directly
            elif isinstance(size, tuple):
                width, height = size
            # Resize the image
            image = pygame.transform.scale(image, (width, height))
            return image
    elif str(filename).lower().endswith('.svg'): # Convert to str as filename is path object
        kwargs = {}

        # Check if we need to scale the image
        if size:
            kwargs["parent_width"] = size if isinstance(size, int) else size[0]
            kwargs["parent_height"] = size if isinstance(size, int) else size[1]

        # Convert the svg to a png with the given size
        new_bites = cairosvg.svg2png(url=str(filename), **kwargs)
        byte_io = io.BytesIO(new_bites)
        return pygame.image.load(byte_io)
    else:
        raise ValueError("Image file must be a .png or .svg file")