import discord
import discord.app_commands
from discord.ui import Button,View
import os

#################################
client=discord.Client(intents=discord.Intents.default())
tree=discord.app_commands.CommandTree(client)
#################################
#トークン読み込み
DiscordIDs="DiscordKeys/"
with open(os.path.join(DiscordIDs,"token.txt")) as t, \
     open(os.path.join(DiscordIDs,"guild_id.txt")) as g:
     TOKEN=t.read()
     GUILD_ID=g.read()
     guild=discord.Object(GUILD_ID)
   
class Panel(discord.ui.View):
    def __init__(self,game,time,host,timeout=10800):
        super().__init__(timeout=timeout)
        self.game=game
        self.time=time
        self.host=host
        self.value=None
        self.userlist=[host]
    
    def setMessage(self,status):
        return f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:**{status}**\nメンバー:"+",".join(self.userlist)

    @discord.ui.button(label="参加する",style=discord.ButtonStyle.success,custom_id="join")
    async def join(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(interaction.user.name in self.userlist):
            await interaction.response.edit_message(content=self.setMessage(f"{interaction.user.name}さんは既に参加しています。"))
        else:
            self.userlist.append(interaction.user.name)
            await interaction.response.edit_message(content=self.setMessage(f"{interaction.user.name}さんが参加しました。"))
        
    @discord.ui.button(label="参加をキャンセル",style=discord.ButtonStyle.grey,custom_id="cancel")
    async def cancel(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(interaction.user.name == self.host):
            await interaction.response.edit_message(content=self.setMessage(f"ホストは参加をキャンセルできません。募集を終了する場合は募集を終えるを押してください。"))
            return
        if(interaction.user.name not in self.userlist):
            await interaction.response.edit_message(content=self.setMessage(f"{interaction.user.name}さんは参加していません。"))
        else:
            self.userlist.remove(interaction.user.name)
            await interaction.response.edit_message(content=self.setMessage(f"{interaction.user.name}さんがキャンセルしました。"))

    @discord.ui.button(label="募集を終える",style=discord.ButtonStyle.danger,custom_id="quit")
    async def quit(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(self.host==interaction.user.name):
            self.clear_items()
            await interaction.response.edit_message(content="募集は終了されました。",view=self)
            self.stop()
        else:
            await interaction.response.edit_message(content=self.setMessage(f"募集を終わらせられるのはホストのみです。"))
    
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(content="募集はタイムアウトしました。",view=self)
        return await super().on_timeout()
        
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.channel.send("error"+str(error))
        return await super().on_error(interaction, error)

#募集ボタン作成
@tree.command(
    guild=guild,
    name="募集",
    description="誰かと何かしたいときに人を募集するために使えます。"
)
@discord.app_commands.describe(
    ゲーム名="募集するゲーム名",
    時間="何時から開始するか"
)
async def recruit(ctx:discord.Interaction,ゲーム名: str,時間:str):
    view=Panel(ゲーム名,時間,ctx.user.name)
    await ctx.response.send_message(f"@everyone\n ゲーム名:{ゲーム名}\n開始時刻:{時間}\n一緒に遊ぶ人を募集します。\nホスト名:{ctx.user.name}\nステータス:**募集が開始されました**\nメンバー:"+ctx.user.name,view=view)
    view.message=await ctx.original_response()
#Bot起動
@client.event
async def on_ready():
    print("ready...")
    await tree.sync(guild=guild)
    print("sync commands...")

#コマンド登録
client.run(TOKEN)