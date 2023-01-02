from nextcord import Interaction
from nextcord.ext import application_checks

STAFF = []
DEV = [579111799794958377]
BOT = 1025533293636112404
GUILDS = [876844147812728892]




# TODO: Cleanup & Refactor /// Come up with something similar


def is_bot_owner():
	def predicate(interaction: Interaction):
		return (
				interaction.user.id in DEV
		)


	return application_checks.check(predicate)




def is_bot_staff():
	def predicate(interaction: Interaction):
		return (
				interaction.user.id in STAFF
		)


	return application_checks.check(predicate)




def is_allowed_server():
	def predicate(interaction: Interaction):
		return (
				interaction.guild is not None
				and interaction.guild.id in GUILDS
		)


	return application_checks.check(predicate)
