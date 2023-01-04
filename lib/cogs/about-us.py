import datetime

import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Cog




class Buttons(nextcord.ui.View):

	def __init__(self):
		super().__init__(timeout=None)

#
# @nextcord.ui.button(label="Join our Discord!", style=nextcord.ButtonStyle.grey, disabled=True,
#                     emoji=)
# async def join_discord(self, interaction: Interaction):
# 	await interaction.response.send_message()
# 	Buttons().refresh()  # TODO
#



class About(Cog):

	def __init__(self, bot):
		self.bot = bot


	@nextcord.slash_command(name="about-us",
	                        description="About Butterfly",
	                        # guild_ids=GUILDS,
	                        name_localizations={"de": "über-uns"},
	                        description_localizations={"de": "Über Butterfly [ENGLISCH]"},
	                        force_global=True,
	                        dm_permission=True)
	async def about_us(self, interaction: Interaction):

		emb = nextcord.Embed(title="About Butterfly",
		                     description="**Butterfly** is currently in *semi-active development*\n\nCurrently,"
		                                 " you can only use `/about-us`, but this will change in the future when\n"
		                                 " I unlock more features.",
		                     colour=nextcord.Colour.brand_green(),
		                     timestamp=datetime.datetime.utcnow())

		fields = [("Developer", "Simplex#7008", False)]

		for field in fields:
			emb.add_field(name=field[0], value=field[1], inline=field[2])

		emb.set_thumbnail(self.bot.user.avatar)
		emb.set_footer(text="formerly MyNexus", icon_url=self.bot.user.avatar)

		view = Buttons()
		await interaction.response.send_message(embed=emb, ephemeral=True, view=view)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("about-us")




def setup(bot):
	bot.add_cog(About(bot))
