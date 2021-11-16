from enum import Enum

from .customization import Sounds

__all__ = (
    "Sound",
    "SOUND_PATH"
)

SOUND_PATH = Sounds.SOUND_PATH


class Sound(Enum):
    DM = SOUND_PATH + "/dm.mp3"
    GUILD = SOUND_PATH + "/guild.mp3"
    PING = SOUND_PATH + "/ping.mp3"
    SENT = SOUND_PATH + "/sent.mp3"
    SYSTEM = SOUND_PATH + "/system.mp3"
