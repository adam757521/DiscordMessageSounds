import discord
import selfbotUtils

from .utils import mentioned_in
from .customization import Sounds, Notifications, Account
from .sounds import async_play_sound

__all__ = ("SoundClient", "SOUND_PATH", "SOUND_VOLUME", "SOUND_FADE")

SOUND_PATH = Sounds.SOUND_PATH
SOUND_VOLUME = Sounds.VOLUME
SOUND_FADE = Sounds.FADE


class SoundClient(discord.Client):
    """
    Represents a SoundClient that plays notification sounds.
    """

    __slots__ = ("token", "client")

    def __init__(self, token: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.client = selfbotUtils.Client(
            token, self.loop
        )  # To get notifications level (http).

    def play_sound(self, path: str, *args, **kwargs) -> None:
        """
        A shortcut function for async_play_sound.
        Runs the function in a task.

        :param str path: The path.
        :return: None
        :rtype: None
        """

        self.loop.create_task(async_play_sound(self.loop, path, *args, **kwargs))

    def play_sound_if_notifications_match(
        self, notifications: discord.NotificationLevel, mentioned: bool
    ) -> None:
        """
        Plays the sound that is needed.
        Based on the notification level and if the user was mentioned.

        :param discord.NotificationLevel notifications: The notification level.
        :param bool mentioned: A bool representing if the user is mentioned.
        :return: None
        :rtype: None
        """

        if (
            notifications == discord.NotificationLevel.all_messages
            or notifications == discord.NotificationLevel.only_mentions
            and mentioned
        ):
            sound = f"{SOUND_PATH}/ping.mp3" if mentioned else f"{SOUND_PATH}/guild.mp3"
            self.play_sound(sound, SOUND_VOLUME, SOUND_FADE)

    async def on_ready(self):
        print(f"Listening for messages on {self.user}.")
        await self.client.http._initialize()  # Initializes the client to speedup the requests.

    async def get_notification_settings(self, channel: discord.TextChannel) -> dict:
        """
        |coro|

        Returns a dict of the notification settings for a channel.

        :param discord.TextChannel channel: The channel.
        :return: The notification settings.
        :rtype: dict
        """

        guild = channel.guild
        settings = await self.client.http.request(
            "PATCH",
            f"/users/@me/guilds/{guild.id}/settings",
            auth=True,
            json={},
        )

        for channel_override in settings["channel_overrides"]:
            id_ = int(channel_override["channel_id"])

            if id_ == channel.id or channel.category and id_ == channel.category.id:
                settings["muted"] = channel_override["muted"]
                settings["message_notifications"] = channel_override[
                    "message_notifications"
                ]
                break

        return settings

    async def handle_guild_message(self, message: discord.Message) -> None:
        """
        |coro|

        Handles a guild message and plays the proper notification.

        :param discord.Message message: The message.
        :return: None
        :rtype: None
        """

        me = message.guild.me

        suppress_roles = False
        suppress_everyone = False

        if Notifications.GET_GUILD_NOTIFICATION_CONFIG:
            settings = await self.get_notification_settings(message.channel)
            notifications_level = settings["message_notifications"]

            if settings["muted"] or notifications_level == 2:
                return

            suppress_roles = settings["suppress_roles"]
            suppress_everyone = settings["suppress_everyone"]

            notifications = discord.NotificationLevel(notifications_level)
        else:
            notifications = message.guild.default_notifications

        self.play_sound_if_notifications_match(
            notifications,
            mentioned_in(me, message, suppress_roles, suppress_everyone),
        )

    async def on_message(self, message):
        if self.user == message.author and not Notifications.DEBUG:
            return

        user_status = [s for s in self.guilds][0].get_member(self.user.id).status

        if (
            not Notifications.PLAY_NOTIFICATION_IN_DND
            and user_status == discord.Status.do_not_disturb
        ):
            return

        if message.guild:
            await self.handle_guild_message(message)
        else:
            self.play_sound(f"{SOUND_PATH}/dm.mp3", SOUND_VOLUME, SOUND_FADE)

    async def on_connect(self):
        await self.change_presence(status=Account.AUTOMATIC_STATUS, afk=Account.AFK)

    def run(self):
        super().run(self.token)
