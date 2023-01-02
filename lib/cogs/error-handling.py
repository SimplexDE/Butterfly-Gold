from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.ext.commands import Cog




class ErrorHandling(Cog):

	def __init__(self, bot):
		self.bot = bot
		self.blocked = {}


	@staticmethod
	@Cog.listener()
	async def on_error(err, *args, **kwargs):
		"""
    	A helper function that is used to run the bot when an error occurs.
    	"""
		if err == "on_application_command_error":
			await args[0].send("Etwas ist schiefgelaufen!", delete_after=3)
		raise


	@staticmethod
	@Cog.listener()
	async def on_application_command_error(interaction: Interaction, error):

		if isinstance(error, application_checks.errors.ApplicationCheckFailure):
			return await interaction.send("Command failed. [ApplicationCheckFailure]", ephemeral=True)
		else:
			return await interaction.send("Command failed. [{}]".format(error), ephemeral=True)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("error-handling")




def setup(bot):
	bot.add_cog(ErrorHandling(bot))
