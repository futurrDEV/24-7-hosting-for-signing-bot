import discord
from discord.ext import commands

SIGNING_EMOJI = "✅"

async def start_signing(ctx, target: discord.Member, extra):
    author = ctx.author
    guild = ctx.guild

    # Your exact role names
    manager_role = discord.utils.get(guild.roles, name="Manager")
    coach_role = discord.utils.get(guild.roles, name="Coach")
    free_agent_role = discord.utils.get(guild.roles, name="Free Agent")
    official_player_role = discord.utils.get(guild.roles, name="Official Player")

    # Determine if author is Manager or Coach
    is_manager = manager_role in author.roles
    is_coach = coach_role in author.roles

    # Manager assigning a coach
    if extra and "coach" in extra.lower():
        if not is_manager:
            return await ctx.send("Only managers can assign coaches.")
        await target.add_roles(coach_role)
        return await ctx.send(f"{target.mention} is now a coach for the club.")

    # Manager or Coach signing a player
    if is_manager or is_coach:

        # DYNAMIC CLUB DETECTION
        excluded = {manager_role, coach_role, free_agent_role, official_player_role}
        club_roles = [r for r in author.roles if r not in excluded]

        if not club_roles:
            return await ctx.send("You don't seem to have a club role.")

        club_role = club_roles[0]

        # Confirmation message
        embed = discord.Embed(
            title="Signing Confirmation",
            description=f"{author.mention} wants to sign {target.mention}.\n"
                        f"Both must react with {SIGNING_EMOJI} to confirm.",
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=embed)
        await msg.add_reaction(SIGNING_EMOJI)

        def check(reaction, user):
            return (
                reaction.message.id == msg.id
                and str(reaction.emoji) == SIGNING_EMOJI
                and user in [author, target]
            )

        confirmed = set()

        while len(confirmed) < 2:
            reaction, user = await ctx.bot.wait_for("reaction_add", check=check)
            confirmed.add(user)

        # APPLY ROLES
        await target.add_roles(official_player_role)
        await target.add_roles(club_role)

        if free_agent_role in target.roles:
            await target.remove_roles(free_agent_role)

        return await ctx.send(
            f"Signing complete! {target.mention} is now an official player for {club_role.name}."
        )

    return await ctx.send("You don't have permission to sign players.")
