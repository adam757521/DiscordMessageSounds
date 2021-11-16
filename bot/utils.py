from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import discord

__all__ = ("mentioned_in",)


def mentioned_in(
    member: discord.Member,
    message: discord.Message,
    suppress_roles: bool = False,
    suppress_everyone: bool = False,
) -> bool:
    """
    Returns a bool representing if the user was mentioned in the message.

    :param bool suppress_roles: A bool indicating if the roles should be suppressed.
    :param bool suppress_everyone: A bool indicating if @everyone mentions should be suppressed.
    :param discord.Member member: The member/user.
    :param discord.Message message: The message.
    :return: A bool representing if the user was mentioned in the message.
    :rtype: bool
    """

    return (
        not suppress_roles
        and any(role in member.roles for role in message.role_mentions)
        or not suppress_everyone
        and message.mention_everyone
        or member in message.mentions
    )
