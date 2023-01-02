import nextcord.ui
from nextcord import Interaction, slash_command
from nextcord.ext.commands import Cog

from lib.checks import GUILDS




class VerifyButton(nextcord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.verified = False


	@nextcord.ui.button(
		label="Verify",
		style=nextcord.ButtonStyle.green,
		emoji="\N{WHITE HEAVY CHECK MARK}",
		custom_id="verificationButton",
	)
	async def verify(self, button: nextcord.ui.Button, interaction: Interaction):
		if not self.verified:
			self.verified = True

		self.stop()




class Verify(Cog):
	def __init__(self, bot):
		self.bot = bot


	@slash_command(
		name="verify-me",
		name_localizations={},
		description="Verify yourself.",
		description_localizations={},
		guild_ids=GUILDS
	)
	async def verification(self, interaction: Interaction):
		view = VerifyButton()
		await self.bot.setup_hook(view)
		await interaction.response.send_message("Verify yourself", view=view, ephemeral=True)
		await view.wait()
		if view.verified:
			await interaction.edit("Verified", ephemeral=True)
		else:
			await interaction.edit("Not verified")


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("verify")




def setup(bot):
	bot.add_cog(Verify(bot))
