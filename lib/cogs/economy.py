import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext.commands import Cog

from ..checks import DEV_GUILDS
from ..db.sqlite3 import SQLite3

db_path = "db/economy.db"
table_name = "accounting"
db = SQLite3(db_path)




class Buttons(nextcord.ui.View):

	def __init__(self):
		super().__init__(timeout=None)




class Economy(Cog):

	def __init__(self, bot):
		self.bot = bot


	@staticmethod
	def check_for_account(interaction: Interaction):
		if db.select_from_table(db_path, table_name, ["user_id"], interaction.user.id, "user_id"):
			return True
		else:
			db.insert_into_table(db_path, table_name, ["user_id", "balance"], [interaction.user.id, 200])


	@nextcord.slash_command(name="account",
	                        description="Manage your Account",
	                        guild_ids=DEV_GUILDS,
	                        name_localizations={},
	                        description_localizations={},
	                        force_global=False,
	                        dm_permission=False)
	async def account(self, interaction: Interaction,
	                  action: str = SlashOption(
		                  name="action",
		                  description="action",
		                  required=True,
		                  choices=["Delete Account", "View Balance"]
	                  )):

		db.create_table(db_path, table_name, ["user_id", "balance"])

		emb = Embed(title="Accounting", description="", color=nextcord.Color.brand_green())
		if action == "Delete Account":
			if db.select_from_table(db_path, table_name, ["user_id"], interaction.user.id, "user_id"):
				db.delete_from_table(db_path, table_name, "user_id", interaction.user.id)
				emb.add_field(name="Delete Account", value="Your Account has been deleted...")
			else:
				emb.add_field(name="Delete Account", value="You have no account.")
			await interaction.response.send_message(embed=emb, ephemeral=True)
		elif action == "View Balance":
			await self.show_balance(interaction)


	@nextcord.slash_command(name="balance",
	                        description="balance",
	                        guild_ids=DEV_GUILDS,
	                        name_localizations={},
	                        description_localizations={},
	                        force_global=False,
	                        dm_permission=False)
	async def show_balance(self, interaction: Interaction):
		self.check_for_account(interaction)
		balance = db.select_from_table(db_path, table_name, ["balance"], interaction.user.id, "user_id")
		emb = Embed(title="Balance: ${}".format(balance[0][0]), description="",
		            color=nextcord.Color.blurple())
		await interaction.response.send_message(embed=emb, ephemeral=True)


	@nextcord.slash_command(name="bet",
	                        description="bet",
	                        guild_ids=DEV_GUILDS,
	                        name_localizations={},
	                        description_localizations={},
	                        force_global=False,
	                        dm_permission=False)
	async def bet(self, interaction: Interaction,
	              bet: int = SlashOption(
		              name="bet",
		              description="Amount to bet",
		              required=True,
		              min_value=10,
		              max_value=500
	              ),
	              line: int = SlashOption(
		              name="line",
		              description="On which line do you bet?",
		              required=True,
		              choices=[1, 2, 3]
	              )):
		self.check_for_account(interaction)
		await interaction.response.send_message("{}, {}".format(bet, line), ephemeral=True)


	# TODO: CODE HERE
	# NOTICE: USE THE MINIGAME I CREATED AS HELP

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("economy")




def setup(bot):
	bot.add_cog(Economy(bot))
