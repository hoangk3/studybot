import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.command(name="remind")
    async def remind(self, ctx, time: str, *, message: str):
        delay = self.parse_time(time)
        if delay is None:
            await ctx.send("⚠️ Định dạng thời gian không hợp lệ. Ví dụ: 10s, 5m, 1h.")
            return

        reminder_time = datetime.now() + timedelta(seconds=delay)
        self.reminders.append((ctx.author.id, reminder_time, message))
        await ctx.send(f"⏰ Đã đặt nhắc nhở: {message} sau {time}")

        await asyncio.sleep(delay)
        await ctx.author.send(f"🔔 Nhắc nhở: {message}")

    def parse_time(self, time_str):
        units = {"s": 1, "m": 60, "h": 3600}
        try:
            return int(time_str[:-1]) * units[time_str[-1]]
        except (ValueError, KeyError):
            return None
def setup(bot):
    bot.add_cog(Reminder(bot))