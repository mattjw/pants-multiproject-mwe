"""Pointless sub-package for sake of demonstration."""

import random
from typing import Dict, List

from dataclasses import dataclass


@dataclass
class Emoji:
    name: str
    emoji: str


def emoji_compendium() -> List[Emoji]:
    return [
        Emoji("snake", "🐍"),
        Emoji("basketball", "🏀"),
        Emoji("violin", "🎻"),
    ]


def random_emoji() -> Emoji:
    return random.choice(emoji_compendium())
