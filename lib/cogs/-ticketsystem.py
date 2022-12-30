import random
from datetime import datetime

import nextcord

from ..checks import is_staff
from ..db.sqlite3 import SQLite3

from loguru import logger as log

from nextcord.ext.commands import Cog, command, cooldown, BucketType

# TODO: Document this file.
# TODO: Implement new database functions

# generate_name is used for generation of ticket-channel names
def generate_name(length):
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"

    use = lower_case + numbers
    length = length

    # Randomize the Letters and join them together
    out = "".join(random.sample(use, length))

    # Return the output.
    return out

db = SQLite3()

class TicketSystem(Cog):

    def __init__(self, bot):
        self.bot = bot

    async def create(self, guild: nextcord.Guild, owner: nextcord.Member, reason: str):
        db.connect("database")
        db.cursor()

        db.execute("CREATE TABLE IF NOT EXISTS tickets (CHN_ID INTEGER PRIMARY KEY, chn_name TEXT, OWNER_ID INTEGER, owner_name TEXT, state BOOLEAN, reason TEXT)")
        db.commit()

        db.execute("SELECT CHN_ID FROM tickets WHERE OWNER_ID=%s" % owner.id)
        result = db.cur.fetchone()

        if result:
            db.execute("SELECT state FROM tickets WHERE OWNER_ID=%s" % owner.id)
            curr_state = db.cur.fetchone()
            if curr_state:
                await owner.send("Bitte schließe dein Offenes Ticket, bevor du ein neues öffnest.")
                return


        # Generate the name for the ticket-channel.
        name = generate_name(6)

        # Convert the name to a string named ticket
        ticket = str(owner.name + "-" + name)

        # Create the Channel as a variable in a pre-defined category
        chn = await guild.create_text_channel(name=ticket,
                                                      category=nextcord.utils.get(self.bot.guild.categories,
                                                                                  id=1031320994205409301),
                                                      reason="{} opened a ticket".format(owner))

        # Define the overwrite-permissions for the ticket-creator.
        overwrite = chn.overwrites_for(owner)
        overwrite.read_messages = True

        # Set the overwrite-permissions
        await chn.set_permissions(owner, overwrite=overwrite)

        # Send a predefined message(also, define a msg variable) to the ticket channel
        msg = await chn.send("> Ticket eröffnet von {}.\n> Grund: `{}`".format(owner.mention, reason))

        # Pin the message
        await msg.pin()

        # Purge the pin message
        await chn.purge(limit=1)

        try:
            db.execute("INSERT INTO tickets (CHN_ID, chn_name, OWNER_ID, owner_name, state, reason) VALUES (%s, '%s', %s, '%s', %s, '%s')" % (chn.id, chn.name, owner.id, owner.name, True, reason))
        except Exception as e:
            log.error("Something went wrong during ticket creation:")
            log.error(e)

        db.commit()
        db.close()

    async def open(self, chn):

        await chn.send(
            "Halt. Du kannst aktuell keine Tickets wiedereröffnen, bitte ein neues öffnen."
            "\nDas Ticket kann mit `!delete` gelöscht werden.")
        return

        # TODO Find a way to only allow ONE open ticket per user.

        # db.connect("database")
        # db.cursor()
        #
        # db.execute("CREATE TABLE IF NOT EXISTS tickets (CHN_ID INTEGER PRIMARY KEY, chn_name TEXT, OWNER_ID INTEGER, owner_name TEXT, state BOOLEAN, reason TEXT)")
        # db.commit()
        #
        # db.execute("SELECT state FROM tickets WHERE CHN_ID=%s" % chn.id)
        # result = db.cur.fetchone()
        #
        # if result:
        #     await chn.send("Ticket ist bereits offen.")
        #     db.commit()
        #     db.close()
        #     return
        #
        # overwrite = chn.overwrites_for(owner)
        # overwrite.send_messages = True
        #
        # await chn.set_permissions(owner, overwrite=overwrite)
        # await chn.send("Ticket geöffnet")
        #
        # try:
        #     db.execute("UPDATE tickets SET state=%s WHERE CHN_ID=%s" % (True, chn.id))
        # except Exception as e:
        #     log.error("Something went wrong during ticket update:")
        #     log.error(e)
        #
        # db.commit()
        # db.close()

    async def close(self, chn, owner: nextcord.Member):
        db.connect("database")
        db.cursor()

        db.execute(
            "CREATE TABLE IF NOT EXISTS tickets (CHN_ID INTEGER PRIMARY KEY, chn_name TEXT, OWNER_ID INTEGER, owner_name TEXT, state BOOLEAN, reason TEXT)")
        db.commit()

        db.execute("SELECT state FROM tickets WHERE CHN_ID=%s" % chn.id)
        result = db.cur.fetchone()

        if not result:
            await chn.send("Ticket ist bereits geschlossen.")
            db.commit()
            db.close()
            return

        overwrite = chn.overwrites_for(owner)
        overwrite.send_messages = False

        await chn.set_permissions(owner, overwrite=overwrite)
        await chn.send("Ticket geschlossen")

        try:
            db.execute("UPDATE tickets SET state=%s WHERE CHN_ID=%s" % (False, chn.id))
        except Exception as e:
            log.error("Something went wrong during ticket update:")
            log.error(e)

        db.commit()
        db.close()

    async def delete(self, chn):
        db.connect("database")
        db.cursor()

        db.execute(
            "CREATE TABLE IF NOT EXISTS tickets (CHN_ID INTEGER PRIMARY KEY, chn_name TEXT, OWNER_ID INTEGER, owner_name TEXT, state BOOLEAN, reason TEXT)")
        db.commit()

        db.execute("SELECT * FROM tickets WHERE CHN_ID=%s" % chn.id)
        result = db.cur.fetchall()

        chn = self.bot.get_channel(result[0][0])
        await chn.delete()

        owner = self.bot.get_user(result[0][2])
        embed = nextcord.Embed(title="Ticket `{}` wurde geschlossen".format(result[0][1]),
                               colour=nextcord.Colour.brand_green(),
                               timestamp=datetime.now()
                               )
        embed.set_footer(text="Plutocore Support-System")

        await owner.send(embed=embed)

        try:
            db.execute("DELETE FROM tickets WHERE CHN_ID=%s" % chn.id)
        except Exception as e:
            log.error("Something went wrong during ticket update:")
            log.error(e)

        db.commit()
        db.close()

    @command(
        name="ticket",
        brief="Open a ticket",
        aliases=["createticket"]
    )
    @cooldown(1, 3, BucketType.guild)
    async def create_ticket(self, ctx, reason="Kein Grund angegeben"):
        await ctx.message.delete()
        await TicketSystem.create(self, ctx.guild, ctx.author, reason)

        return

    @command(
        name="close",
        brief="Closes a ticket",
        aliases=["closeticket"]
    )
    @cooldown(1, 1, BucketType.user)
    async def close_ticket(self, ctx):
        await ctx.message.delete()
        await TicketSystem.close(self, ctx.channel, ctx.author)

        return

    @command(
        name="open",
        brief="Opens a ticket",
        aliases=["openticket"]
    )
    @cooldown(1, 1, BucketType.user)
    async def open_ticket(self, ctx):
        await ctx.message.delete()
        await TicketSystem.open(self, ctx.channel)

        return

    @command(
        name="delete",
        brief="Delete a ticket[Nur Ticket-Ersteller oder Claimer]",
        # aliases=["createticket", "openticket"]
    )
    @is_staff()
    @cooldown(1, 1, BucketType.user)
    async def delete_ticket(self, ctx):
        await ctx.message.delete()
        await TicketSystem.delete(self, ctx.channel)

        return

    @Cog.listener()
    async def on_ready(self):
       if not self.bot.ready:
            self.bot.cogs_ready.ready_up("ticketsystem")

def setup(bot):
    bot.add_cog(TicketSystem(bot))
