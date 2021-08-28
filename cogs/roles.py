from discord import RawReactionActionEvent
from discord.ext import commands
from discord.utils import get

import logging

logger = logging.getLogger(__name__)

message_id = 881117551344615434
role_massage_link = "https://discord.com/channels/729318120304672778/881117323321278484/881117551344615434"
reaction_roles = {
    message_id: [
        ("bonfire", 881130721295622154),  # bonfire
        ("📚", 845598058389700608),  # book
        ("obelisk", 845956928185565184),  # sac
        ("⚔️", 881137457561751583),  # 1vs1
        ("family_mmbb", 881122111324827679),  # 2vs2
        ("barrel", 881122111324827679),  # divinity
    ]
}


class ReactionRoles(commands.Cog):
    """
    This instance handles all reaction role events.
    """
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def process_reaction(self, payload: RawReactionActionEvent, r_type=None) -> None:
        if payload.message_id in reaction_roles.keys():
            for obj in reaction_roles[payload.message_id]:
                if obj[0] == payload.emoji.name:
                    guild = self.bot.get_guild(payload.guild_id)
                    user = await guild.fetch_member(payload.user_id)
                    role = guild.get_role(obj[1])
                    if role is None:
                        self.bot.ph.warn(f"An invalid role ID ({obj[0]}, {obj[1]}) was provided in `reaction_roles` for"
                                         f" message with ID: {payload.message_id}")
                        self.bot.ph.warn("Not performing any action as result.")
                    elif r_type == "add":
                        await user.add_roles(role)
                    elif r_type == "remove":
                        await user.remove_roles(role)
                    else:
                        self.bot.ph.warn("Invalid reaction type was provided in `process_reaction`.")
                        self.bot.ph.warn("Not performing any action as result.")
                    break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        logger.info(f"add {payload.emoji} {payload.member}")
        await self.process_reaction(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        logger.info(f"remove {payload.emoji} {payload.member}")
        await self.process_reaction(payload, "remove")

    @commands.command()
    # @commands.is_owner()
    # @commands.has_permissions(administrator=True)
    async def role(self, ctx, name: str = None):
        for role in ctx.guild.roles:
            print(role.id, role.name)

        member = ctx.message.author

        if name:
            role = get(ctx.guild.roles, name=name)
            if role not in member.roles:
                await ctx.send(f"add role {role.name} to {member.name}")
                await member.add_roles(role)

            elif role in member.roles:
                await ctx.send(f"remove role {role.name} from {member.name}")
                await member.remove_roles(role)

        else:
            yr = set(member.roles)
            ar = list(set(ctx.guild.roles) - yr)

            yr = "\n".join(list(map(lambda x: x.name, member.roles)))
            ar = "\n".join(list(map(lambda x: x.name, ar)))
            await ctx.send(f"Allowed roles:\n`{ar}`\n\nYour roles:\n`{yr}`\nmanage roles here {role_massage_link}")


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
