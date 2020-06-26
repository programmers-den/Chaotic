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

usedIDs = {}
wss.on 'connection', (ws) ->
  ws.on 'message', (data) ->
    if 'js' in JSON.parse(ws.data).recipients.indexOf("recipients")
      if JSON.parse(ws.data).data == "registerid"
        usedIDs[JSON.parse(ws.data).id.toString()] = JSON.parse(ws.data).sender
        data = {"recipients":[JSON.parse(ws.data).sender], "sender":"js", "data":"id registered", "id":JSON.parse(ws.data).id}
        ws.send(JSON.stringify(data))
      else if JSON.parse(ws.data).data == "unregisterid"
        delete usedIDs[JSON.parse(ws.data).id.toString()]
        data = {"recipients":[JSON.parse(ws.data).sender], "sender":"js", "data":"unregistered id", "id":JSON.parse(ws.data).id}
        ws.send(JSON.stringify(data))
      else if JSON.parse(ws.data).data == "listids"
        data = {"recipients":[JSON.parse(ws.data).sender], "sender":"js", "data":JSON.stringify(Object.keys(usedIDs)), "id":JSON.parse(ws.data).id}
        ws.send(JSON.stringify(data))
    wss.clients.forEach (client) ->
    if client.readyState == WebSocket.OPEN
      client.send data

for file in commandFiles
  command = require "./commands/#{file}"
  client.commands.set(command.name, command)

console.log client.commands

client.once 'ready', -> console.log 'JS: Ready!'

client.on 'message', (message) ->
  return if !message.content.startsWith(prefix) or message.author.bot

  args = message.content.slice(prefix.length).split(RegExp(' +')) # todo: migrate to modern slash-based syntax later
  command = args.shift().toLowerCase()

  if command == "help"
    

  client.commands.get('test').execute(message, args) if command == 'test' # todo: automate with for loop

client.login(token)
