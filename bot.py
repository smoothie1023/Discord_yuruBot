import discord
import discord.app_commands
from discord.ui import Button,View

#################################
client=discord.Client(intents=discord.Intents.default())
tree=discord.app_commands.CommandTree(client)
#################################
#トークン読み込み
path="token.txt"
f=open(path)
TOKEN=f.read()
f.close()

#ギルドID読み込み
path="guild_id.txt"
f=open(path)
GUILD_ID=f.read()
guild=discord.Object(GUILD_ID)
f.close()

class Panel(discord.ui.View):
    def __init__(self,game,time,host):
        super().__init__(timeout=None)
        self.game=game
        self.time=time
        self.host=host
        self.value=None
        self.userlist=[host]

    
    @discord.ui.button(label="参加する",style=discord.ButtonStyle.success)
    async def join(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(interaction.user.name in self.userlist):
            await interaction.response.edit_message(content=f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:{interaction.user.name}さんは既に参加しています。\nメンバー:"+",".join(self.userlist))
        else:
            self.userlist.append(interaction.user.name)
            await interaction.response.edit_message(content=f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:{interaction.user.name}さんが参加しました。\nメンバー:"+",".join(self.userlist))

        
    @discord.ui.button(label="キャンセル",style=discord.ButtonStyle.grey)
    async def cancel(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(interaction.user.name not in self.userlist):
            await interaction.response.edit_message(content=f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:{interaction.user.name}さんは参加していません。\nメンバー:"+",".join(self.userlist))
        else:
            self.userlist.remove(interaction.user.name)
            await interaction.response.edit_message(content=f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:{interaction.user.name}さんがキャンセルしました。\nメンバー:"+",".join(self.userlist))

    @discord.ui.button(label="募集を終える",style=discord.ButtonStyle.danger)
    async def quit(self,interaction:discord.Interaction,button:discord.ui.Button):
        if(self.host==interaction.user.name):
            self.clear_items()
            await interaction.response.edit_message(content="募集は終了されました。",view=self)
            self.stop()
        else:
            await interaction.response.edit_message(content=f"@everyone\n ゲーム名:{self.game}\n開始時刻:{self.time}\n一緒に遊ぶ人を募集します。\nホスト名:{self.host}\nステータス:募集を終わらせられるのはホストのみです。\nメンバー:"+",".join(self.userlist))

#募集ボタン作成
@tree.command(
    guild=guild,
    name="募集",
    description="誰かと何かしたいときに人を募集するために使えます。"
)
async def recruit(ctx:discord.Interaction,ゲーム名: str,時間:str):
    view=Panel(ゲーム名,時間,ctx.user.name)
    await ctx.response.send_message(f"@everyone\n ゲーム名:{ゲーム名}\n開始時刻:{時間}\n一緒に遊ぶ人を募集します。\nホスト名:{ctx.user.name}\nステータス:募集が開始されました\nメンバー:"+ctx.user.name,view=view)

#Bot起動
@client.event
async def on_ready():
    print("ready...")
    await tree.sync(guild=guild)
    print("sync commands...")

#コマンド登録
client.run(TOKEN)