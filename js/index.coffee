Discord = require 'discord.js'
fs = require 'fs'
path = require 'path'

wss = new (require('ws').Server)(port: 9010, host: '127.0.0.1')
client = new Discord.Client()
client.commands = new Discord.Collection()
prefix = process.env.PREFIX
token = process.env.TOKEN
commandFiles = fs.readdirSync('./commands').filter((file) ->
  ['.coffee', '.js'].includes(path.extname(file))
)

wss.on 'listening', -> console.log "WSS: Ready!"

wss.on 'connection', (ws) ->
  ws.on 'message', (data) ->
    wss.clients.forEach (client) ->
      client.send(data) if client.readyState == WebSocket.OPEN

for file in commandFiles
  command = require "./commands/#{file}"
  client.commands.set(command.name, command)

console.log client.commands

client.once 'ready', -> console.log 'JS: Ready!'

client.on 'message', (message) ->
  return if !message.content.startsWith(prefix) or message.author.bot

  args = message.content.slice(prefix.length).split(RegExp(' +')) # todo: migrate to modern slash-based syntax later
  command = args.shift().toLowerCase()

  client.commands.get('test').execute(message, args) if command == 'test' # todo: automate with for loop

client.login(token)
