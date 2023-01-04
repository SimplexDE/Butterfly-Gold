import os

import nextcord
from loguru import logger as log
from nextcord import Interaction, SlashOption
from nextcord.ext.commands import Cog, ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, \
	ExtensionNotLoaded, NoEntryPointError

from ..checks import DEV_GUILDS, is_developer




class Dev(Cog):

	def __init__(self, bot):
		self.bot = bot


	COGS = []

	for file in os.listdir("./lib/cogs"):
		if file.endswith(".py"):
			if not file.startswith("-"):
				COGS += [file[:-3]]


	@nextcord.slash_command(name="reload-commands",
	                        name_localizations={},
	                        description="Reload all Slash-Commands",
	                        description_localizations={},
	                        guild_ids=DEV_GUILDS,
	                        force_global=False,
	                        dm_permission=False,
	                        )
	@is_developer()
	async def reload_slash_commands(self, interaction: Interaction):
		await interaction.response.send_message("Discovering commands, this might take a while...", ephemeral=True)
		await self.bot.discover_application_commands()
		await self.bot.sync_application_commands()
		await interaction.followup.send("Done!", ephemeral=True)


	@nextcord.slash_command(name="modulemanager",
	                        name_localizations={"de": "modulverwaltung"},
	                        description="Manage Modules",
	                        description_localizations={"de": "Module verwalten"},
	                        guild_ids=DEV_GUILDS,
	                        force_global=False,
	                        dm_permission=False,
	                        )
	@is_developer()
	async def module_manager(self, interaction: Interaction,
	                         action: str = SlashOption(name="action",
	                                                   name_localizations={"de": "aktion"},
	                                                   description="Select Path",
	                                                   description_localizations={"de": "Aktion auswählen"},
	                                                   required=True,
	                                                   choices=["load", "unload", "reload"]
	                                                   ),
	                         module: str = SlashOption(name="module",
	                                                   name_localizations={"de": "modul"},
	                                                   description="Select Module",
	                                                   description_localizations={"de": "Modul auswählen"},
	                                                   choices=COGS,
	                                                   required=True)):

		path = "lib.cogs"

		emb_preload = nextcord.Embed(
			title="`{}/{} | {}` Result".format(path.upper().replace(".", "/"), module.upper(), action.upper()),
			description="The action your trying to perform is currently loading...",
			colour=nextcord.Colour.blurple()
		)

		emb_afterload = nextcord.Embed(
			title="`{}/{} | {}` Result".format(path.upper().replace(".", "/"), module.upper(), action.upper()),
			description="The Action was performed, results are down below",
			colour=nextcord.Colour.blurple()
		)

		msg = await interaction.response.send_message(embed=emb_preload, ephemeral=True)
		result = None
		error = None

		if action == "load":
			try:
				self.bot.load_extension(path + "." + module)
			except ExtensionNotFound as e:
				result = "The Module \"{}\" wasn't found!"
				error = e
			except ExtensionAlreadyLoaded as e:
				result = "The Module \"{}\" is already loaded!"
				error = e
			except ExtensionNotLoaded as e:
				result = "The Module \"{}\" is not loaded!"
				error = e
			except NoEntryPointError as e:
				result = "The Module \"{}\" has no setup function!"
				error = e
			except ExtensionFailed as e:
				result = "The Module \"{}\" had an error!"
				error = e
			finally:
				if result is None:
					result = "Complete."
				if error is not None:
					log.exception(error)
				if error is None:
					error = "No errors occurred."

		elif action == "unload":
			try:
				self.bot.unload_extension(path + "." + module)
			except ExtensionNotFound as e:
				result = "The Module \"{}\" wasn't found!"
				error = e
			except ExtensionAlreadyLoaded as e:
				result = "The Module \"{}\" is already loaded!"
				error = e
			except ExtensionNotLoaded as e:
				result = "The Module \"{}\" is not loaded!"
				error = e
			except NoEntryPointError as e:
				result = "The Module \"{}\" has no setup function!"
				error = e
			except ExtensionFailed as e:
				result = "The Module \"{}\" had an error!"
				error = e
			finally:
				if result is None:
					result = "Complete."
				if error is not None:
					log.exception(error)
				if error is None:
					error = "No errors occurred."

		elif action == "reload":
			try:
				self.bot.reload_extension(path + "." + module)
			except ExtensionNotFound as e:
				result = "The Module \"{}\" wasn't found!"
				error = e
			except ExtensionAlreadyLoaded as e:
				result = "The Module \"{}\" is already loaded!"
				error = e
			except ExtensionNotLoaded as e:
				result = "The Module \"{}\" is not loaded!"
				error = e
			except NoEntryPointError as e:
				result = "The Module \"{}\" has no setup function!"
				error = e
			except ExtensionFailed as e:
				result = "The Module \"{}\" had an error!"
				error = e
			finally:
				if result is None:
					result = "Action completed."
				if error is not None:
					log.exception(error)
				if error is None:
					error = "No errors occurred."

		fields = [("Result", result.format(module.upper()).replace("\"", "`"), False),
		          ("Error", error, False)]

		for field in fields:
			emb_afterload.add_field(name=field[0], value=field[1], inline=field[2])

		await msg.edit(embed=emb_afterload)


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("module-manager")




def setup(bot):
	bot.add_cog(Dev(bot))
