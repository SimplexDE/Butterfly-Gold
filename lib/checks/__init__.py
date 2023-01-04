from nextcord import Interaction
from nextcord.ext import application_checks

OWNER = [579111799794958377]
STAFF = []
DEVELOPERS = []
BOT = 1025533293636112404
GUILDS = [876844147812728892, 1024369854192554084]
DEV_GUILDS = [876844147812728892]




def is_developer():
	def predicate(interaction: Interaction):
		return (
				interaction.user.id in DEVELOPERS or OWNER
		)


	return application_checks.check(predicate)




def is_staff():
	def predicate(interaction: Interaction):
		return (
				interaction.user.id in STAFF or DEVELOPERS or OWNER
		)


	return application_checks.check(predicate)
