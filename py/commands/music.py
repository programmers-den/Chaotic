import re

import discord
import lavalink
from discord.ext import commands, menus

global url_rx 
url_rx = re.compile(r'https?://(?:www\.)?.+')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('lavalink.wollycraft.ml', 4524, 'PRIVATELAVALINKPY1', 'eu', 'default-node', 0)  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play', 'search')

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # guild_id = int(event.player.guild_id) # Deactivated as it is unused at the moment.
            pass # This line was suppost to be a auto diconnect, passed for certain issue.

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `bot.shards[shard_id].ws` but that assumes
        # the bot instance is an AutoShardedBot.

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})\n'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        if not player.is_playing:
            await player.play()
            await player.set_volume(100)
            
    @commands.command(aliases=["find"])
    async def search(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = f'ytsearch:{query}'
        result = await player.node.get_tracks(query)
        tracks = result['tracks'][0:10]
        i = 0
        query_result = ''
        
        for track in tracks:
            i = i + 1
            query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
        
        embed1 = discord.Embed()
        embed1.description = query_result
        await ctx.send(embed=embed1)
            
        def check(message):
            return ctx.author == message.author

        response = await self.bot.wait_for('message', check=check, timeout=20)
        track = tracks[int(response.content)-1]
        
        embed = discord.Embed(color=discord.Color.blurple())
        embed.title = 'Track Enqueued'
        embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})\n'
        await ctx.send(embed=embed)

        track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
        player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()
            await player.set_volume(100)

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voice channel!')

        player.queue.clear()

        await player.stop()

        await self.connect_to(ctx.guild.id, None)
        await ctx.send(':outbox_tray: | Disconnected.')
    
    @commands.command()
    async def queue(self, ctx):
        class SongQueue(menus.ListPageSource):
            def __init__(self, queue):
                super().__init__(queue, per_page=10)

            async def format_page(self, menu, entries):
                offset = menu.current_page * self.per_page
                e = discord.Embed(colour=discord.Color.blurple())
                e.title = "Track Queue"
                e.description = '\n'.join(f'{i + 1}) [{v["title"]}](https://youtube.com/watch?v={v["identifier"]})' for i, v in enumerate(entries, start=offset))
                return e
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        
        if player.queue == 0:
            await ctx.send("Queue Is Empty!")
        else:
            pages = menus.MenuPages(source=SongQueue(player.queue), clear_reactions_after=True)
            await pages.start(ctx)

    @commands.command(name="pause")
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing and player.paused == False:
            await ctx.send("Paused.")
            await player.set_pause(True)
    
    @commands.command(name="resume")
    async def resume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.paused == True:
            await ctx.send("Resuming Music.")
            await player.set_pause(False)
        else:
            await ctx.send("Can't Resume The Music. It is not paused")

    @commands.command(name="skip")
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if len(player.queue) > 0 and player.is_connected:
            await ctx.send("Skipped")
            await player.skip()
        else:
            await ctx.send("There is no any other song in the queue!")

    @commands.command(name="remove")
    async def remove(self, ctx, rc: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if len(player.queue) > 0:
            dc = int(rc - 1)
            del player.queue[dc]
            await ctx.send(f"Cleared track {rc}) in queue")
        else:
            await ctx.send("Queue has 0 tracks to play!")

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing:
            pl = player.current
            plc = f"https://youtube.com/watch?v={pl['identifier']}"
            embed = discord.Embed()
            embed.title = "Now playing:"
            embed.add_field(name="Name: ", value=f'[{pl["title"]}]({plc})')
            await ctx.send(embed=embed)

    @commands.command(aliases=["v"])
    async def volume(self, ctx, vol: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.is_playing and vol == vol < 101 and vol == vol > -1:
            await ctx.send(f"Player Volume Has Been Configured To {vol}")
            await player.set_volume(vol)
        else:
            await ctx.send("Volume Is Out Of Range")

    @commands.command(aliases=["loop"])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.repeat:
            player.repeat = False
            await ctx.send("Track Repeat Disabled")
        else:
            player.repeat = True
            await ctx.send("Track Repeat Enabled")

    @commands.command(aliases=["s"])
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.is_playing and player.shuffle:
            player.shuffle = False
            await ctx.send("Queue shuffle disabled")
        else:
            player.shuffle = True
            await ctx.send("Queue shuffle enabled")


bot.add_cog(Music(bot))