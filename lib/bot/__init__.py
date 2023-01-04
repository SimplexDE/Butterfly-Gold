import asyncio
import os
from random import choice

import dotenv
import nextcord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger as log
from nextcord import Colour, Embed, Intents, Interaction
from nextcord.ext.application_checks import errors
from nextcord.ext.commands import Bot as BotBase, Context

# TODO Refactor & Cleanup Code! also Comment

log.info("Loading...")

# Load the .env file
dotenv.load_dotenv()
token = os.environ['GOLD']

PREFIX = "!"
COGS = []

for file in os.listdir("./lib/cogs"):
	if file.endswith(".py"):
		if not file.startswith("-"):
			COGS += [file[:-3]]




class Ready(object):
	"""A callback class that can be used to mark a function as ready."""


	def __init__(self):
		"""Create an instance of Ready."""
		for cog in COGS:
			setattr(self, cog, False)


	def ready_up(self, cog):
		"""A callback that is called when a cog is ready."""
		setattr(self, cog, True)
		# log.info("{} changed READY Status to: {}".format(cog.capitalize(), True))
		log.success("Ready [{}]".format(cog.upper()))


	def all_ready(self):
		"""A callback that is called when all cogs are ready."""
		return all([getattr(self, cog) for cog in COGS])




LOGGING_CHANNEL = 1058255931374305300




class Bot(BotBase):

	def __init__(self):
		self.PREFIX = PREFIX
		self.VERSION = ""
		self.TOKEN = token
		self.ready = False
		self.cogs_ready = Ready()
		self.scheduler = AsyncIOScheduler()
		self.blocked = {}
		super().__init__(intents=Intents.all())


	async def setup_hook(self, view: nextcord.ui.View) -> None:
		log.info("setup hook called :: {}".format(view))
		self.add_view(view)


	def setup(self):
		for cog in COGS:
			try:
				log.info("Loading {}".format(cog.upper()))
				self.load_extension("lib.cogs.{}".format(cog))
			except Exception as e:
				log.warning("Error occurred during loading of {}".format(cog))
				log.exception(e)


	def run(self, version):
		"""
		A helper function that is used to run the bot.
		"""
		self.VERSION = version

		self.setup()

		log.info("Initializing.")
		super().run(self.TOKEN, reconnect=True)


	async def presence_change(self):
		"""
		A helper function that is used to change the presence of the bot.
		"""
		choices = [("Simplex", nextcord.ActivityType.watching),
		           ("PyCharm", nextcord.ActivityType.playing),
		           ("Nextcord", nextcord.ActivityType.watching),
		           ("GitHub", nextcord.ActivityType.streaming),
		           ("Grandfather MyNexus", nextcord.ActivityType.listening)]

		sel = choice(choices)

		await bot.change_presence(status=nextcord.Status.online,
		                          activity=nextcord.Activity(
			                          type=sel[1],
			                          name="{} | {}".format(sel[0], self.VERSION)))


	async def process_commands(self, message):
		"""
		A helper function that is used to process commands.
		"""
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)


	@staticmethod
	async def add_slash_commands():
		bot.add_all_application_commands()
		await bot.sync_application_commands()


	async def on_connect(self):
		"""
		A helper function that is used to run the bot when the bot connects.
		"""
		await bot.change_presence(status=nextcord.Status.dnd)
		await self.add_slash_commands()
		self.scheduler.add_job(self.add_slash_commands, CronTrigger(minute='*/5'))
		log.success("Connected.")


	async def on_application_command_error(self, interaction: Interaction, error):
		if isinstance(error, errors.ApplicationCheckFailure):
			pass
		else:
			raise error


	async def on_ready(self):
		if not self.ready:
			self.scheduler.start()

			embed_done = Embed(title="Something went wrong, but its online!",
			                   description="{} is up.".format(bot.user.name),
			                   colour=Colour.brand_green())

			embed_done.set_footer(text="{} | {}".format(bot.user.name, self.VERSION), icon_url=bot.user.avatar)

			counter = 15
			half_counter = round(counter / 2)

			errors_during_load = False

			while not self.cogs_ready.all_ready():
				await asyncio.sleep(0.5)
				counter -= 1
				if counter == half_counter:
					log.warning("It already took {} seconds to load.".format(half_counter))
				if counter <= -1:
					log.error("Errors encountered during startup, not all cogs are available.")
					errors_during_load = True
					break

			if errors_during_load:
				embed_done.add_field(name=":warning: Completed with errors",
				                     value="The bot started with errors,"
				                           " check console for more information",
				                     inline=False)
				channel = self.get_channel(LOGGING_CHANNEL)
				await channel.send(embed=embed_done)

			self.scheduler.add_job(self.presence_change, CronTrigger(hour='*',
			                                                         jitter=269))
			await self.presence_change()

			log.success("Ready [{}@{}]".format(bot.user.name, self.VERSION))
			self.ready = True

		else:
			log.success("Reconnected.")


	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)




bot = Bot()
