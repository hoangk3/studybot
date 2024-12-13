import discord
from discord.ext import commands
import json
from utils.db import load_data, save_data

class Gamification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scores = load_data("data/leaderboard.json", default={})

    @commands.command(name="rank")
    async def rank(self, ctx):
        """Xem cấp bậc của bạn"""
        user_id = str(ctx.author.id)
        score = self.scores.get(user_id, 0)
        await ctx.send(f"🏅 {ctx.author.name}, bạn hiện có {score} điểm.")

    @commands.command(name="top")
    async def leaderboard(self, ctx):
        """Hiển thị bảng xếp hạng"""
        leaderboard = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        formatted = "\n".join([f"{i+1}. <@{user}>: {score} điểm" for i, (user, score) in enumerate(leaderboard)])
        await ctx.send(f"📋 Bảng xếp hạng:\n{formatted}")

def setup(bot):
    bot.add_cog(Gamification(bot))