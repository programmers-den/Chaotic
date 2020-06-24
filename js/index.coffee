Discord = require 'discord.js'
fs = require 'fs'

wss = new (require('ws').Server)(port: 9010, host: '127.0.0.1')
client = new Discord.Client()
client.commands = new Discord.Collection()
prefix = process.env.PREFIX
token = process.env.TOKEN
commandFiles = fs.readdirSync('./commands').filter((file) ->
  file.endsWith '.js' or '.coffee'
)

wss.on 'listening', () ->
  console.log "WSS: Ready!"

wss.on 'connection', (ws) ->
  ws.on 'message', (data) ->
    wss.clients.forEach (client) ->
      if client.readyState == WebSocket.OPEN
        client.send data

for file in commandFiles
  command = require "./commands/#{file}"
  client.commands.set(command.name, command)

client.once 'ready', ->
  console.log 'JS: Ready!'

client.on 'message', (message) ->
  if !message.content.startsWith(prefix) or message.author.bot
    return

  args = message.content.slice(prefix.length).split(RegExp(' +'))
  command = args.shift().toLowerCase()

  if command == 'test'
    client.commands.get('test').execute(message, args)

client.login token
