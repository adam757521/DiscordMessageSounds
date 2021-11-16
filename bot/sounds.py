import asyncio

from pydub import AudioSegment
from pydub.playback import play

__all__ = ("play_sound", "async_play_sound")


def play_sound(path: str, volume: float = 0.5, fade_time: float = None) -> None:
    """
    Plays the sound

    :param int fade_time: The fade time of the sound.
    :param float volume: The volume to play the sound in.
    :param str path: The sound path.
    :return: None
    :rtype: None
    """

    try:
        sound = AudioSegment.from_mp3(path)

        sound = sound - (70 - (70 * volume))  # Pretty bad method to set volume.

        if fade_time:
            fade_time = int(len(sound) * fade_time)
            sound = sound.fade_in(fade_time).fade_out(fade_time)

        play(sound)
    except PermissionError:
        raise ImportWarning("simpleaudio is not installed, sounds cannot be played!")


async def async_play_sound(loop: asyncio.AbstractEventLoop, *args, **kwargs) -> None:
    """
    |coro|

    Takes the loop and calls the play_sound function in executor.

    :param asyncio.AbstractEventLoop loop: The loop.
    :param args: args for play_sound
    :param kwargs: kwargs for play_sound
    :return: None
    :rtype: None
    """

    await loop.run_in_executor(None, lambda: play_sound(*args, **kwargs))
