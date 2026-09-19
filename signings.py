import discord

SIGNING_ROLE_NAME = "Signings Perms"
CLUB_ROLE_NAME = "Club Manager"
COACH_ROLE_NAME = "Coach"
PLAYER_ROLE_NAME = "Official Player"
FREE_AGENT_ROLE_NAME = "Free Agent"

async def start_signing(ctx, player, extra):
    coach = ctx.author

    # Check signing perms
    signing_role = discord.utils.get(ctx.guild.roles, name=SIGNING_ROLE_NAME)
    if signing_role not in coach.roles:
        return await ctx.send("You don't have signing permissions.")

    embed = discord.Embed(
        title="Signing Confirmation",
        description=f"{coach.mention} wants to sign {player.mention}.\n"
                    f"Both must react with ✅ to confirm.",
        color=discord.Color.blue()
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")

    def check(reaction, user):
        return (
            reaction.message.id == msg.id
            and str(reaction.emoji) == "✅"
            and user in [coach, player]
        )

    confirmed = set()

    while len(confirmed) < 2:
        reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
        confirmed.add(user)

    club_role = discord.utils.get(ctx.guild.roles, name=CLUB_ROLE_NAME)
    coach_role = discord.utils.get(ctx.guild.roles, name=COACH_ROLE_NAME)
    player_role = discord.utils.get(ctx.guild.roles, name=PLAYER_ROLE_NAME)
    free_agent_role = discord.utils.get(ctx.guild.roles, name=FREE_AGENT_ROLE_NAME)

    if free_agent_role in player.roles:
        await player.remove_roles(free_agent_role)

    await player.add_roles(player_role)
    await player.add_roles(club_role)

    await ctx.send(f"Signing complete! {player.mention} is now signed to {club_role.name}.")

