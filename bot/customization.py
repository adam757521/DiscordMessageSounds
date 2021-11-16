import discord

__all__ = ("Account", "Notifications", "Sounds")


class Account:
    TOKEN = "ACCOUNT_TOKEN"  # Replace 'ACCOUNT_TOKEN' with your discord account token.
    AUTOMATIC_STATUS = (
        discord.Status.do_not_disturb
    )  # To suppress the default notifications.
    AFK = True


class Notifications:
    DEBUG = False  # Messages sent by the account will not be filtered.
    GET_GUILD_NOTIFICATION_CONFIG = True
    # Represents if the bot will get the personal guild notification config or use the default one. (API call)
    PLAY_NOTIFICATION_IN_DND = (
        True  # Will play the notification sound even if the user is in do not disturb.
    )


class Sounds:
    SOUND_PATH = "./sounds/"  # The path to the sound files directory.
    VOLUME = 0.85  # 0.0 - 1.0 (can go up to 88.9)
    FADE = 0.5  # Can also be None
