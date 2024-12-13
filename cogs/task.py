import discord
from discord.ext import commands
from utils.db import load_data, save_data

class TaskManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load dữ liệu từ file, mỗi người dùng sẽ có danh sách công việc riêng biệt
        self.tasks = load_data("data/tasks.json", default={})

    @commands.command(name="add")
    async def add_task(self, ctx, *, task: str):
        """Thêm công việc vào danh sách của người dùng"""
        user_id = str(ctx.author.id)
        # Kiểm tra nếu người dùng chưa có danh sách công việc thì tạo mới
        if user_id not in self.tasks:
            self.tasks[user_id] = []
        
        # Thêm công việc vào danh sách của người dùng
        self.tasks[user_id].append(task)
        save_data("data/tasks.json", self.tasks)
        
        # Gửi thông báo đơn giản khi thêm công việc mà không có Embed
        await ctx.send(f"✅ Đã thêm công việc: **{task}**")

    @commands.command(name="list")
    async def list_tasks(self, ctx):
        """Hiển thị danh sách công việc của người dùng"""
        user_id = str(ctx.author.id)
        
        # Kiểm tra xem người dùng có danh sách công việc không
        if user_id not in self.tasks or not self.tasks[user_id]:
            embed = discord.Embed(
                title="❌ Không có công việc!",
                description="Danh sách công việc hiện đang trống.",
                color=discord.Color.red()
            )
            # Thêm ảnh lớn vào Embed khi danh sách trống
            embed.set_image(url="https://i.pinimg.com/originals/f5/f2/74/f5f27448c036af645c27467c789ad759.gif")  # Thay bằng URL ảnh lớn của bạn
        else:
            task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(self.tasks[user_id])])
            embed = discord.Embed(
                title="📋 Danh sách công việc:",
                description=task_list,
                color=discord.Color.blue()
            )
            # Thêm ảnh lớn vào Embed khi có công việc
            embed.set_image(url="https://i.pinimg.com/originals/f5/f2/74/f5f27448c036af645c27467c789ad759.gif")  # Thay bằng URL ảnh lớn của bạn

        embed.set_footer(text="Task Manager Bot")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(TaskManager(bot))
