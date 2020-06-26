Discord = require 'discord.js'
fs = require 'fs'
path = require 'path'
pass = () -> # pass func, this is all it needs
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
dataWaitingRoom = {}
wss.on 'connection', (ws) ->
  ws.on 'message', (data) ->
    wsjsondata = JSON.parse(ws.data)
    if 'js' in wsjsondata.recipients.indexOf("recipients")
      if wsjsondata.id in dataWaitingRoom
        dataWaitingRoom[wsjsondata.id.toString()][wsjsondata.sender] = wsjsondata.data
      if wsjsondata.data == "registerid"
        if wsjsondata.id.toString() not in usedIDs
          usedIDs[wsjsondata.id.toString()] = wsjsondata.sender
          text = "id registered"
        else
          text = "id not registered"
        data = {"recipients":[wsjsondata.sender], "sender":"js", "data":text, "id":wsjsondata.id}
        ws.send(JSON.stringify(data))
      else if wsjsondata.data == "unregisterid"
        if wsjsondata in usedIDs 
          delete usedIDs[wsjsondata.id.toString()]
          text = "unregistered id"
        else
          text = "id not unregistered"
        data = {"recipients":[wsjsondata.sender], "sender":"js", "data":text, "id":wsjsondata.id}
        ws.send(JSON.stringify(data))
      else if wsjsondata.data == "listids"
        data = {"recipients":[wsjsondata.sender], "sender":"js", "data":JSON.stringify(Object.keys(usedIDs)), "id":wsjsondata.id}
        ws.send(JSON.stringify(data))
    wss.clients.forEach (client) ->
      client.send(data) if client.readyState == WebSocket.OPEN


for file in commandFiles
  command = require "./commands/#{file}"
  client.commands.set(command.name, command)

console.log(client.commands)

client.once 'ready', -> console.log 'JS: Ready!'

client.on 'message', (message) ->
  return if !message.content.startsWith(prefix) or message.author.bot

  args = message.content.slice(prefix.length).split(RegExp(' +')) # todo: migrate to modern slash-based syntax later
  command = args.shift().toLowerCase()

  if command == "help"
    while true
      id = Math.floor(Math.random() * (9999999999 - 0) + 0)
      if id not in usedIDs
        break
    wss.clients.forEach (client) ->
      if client.readyState == WebSocket.OPEN
        client.send(JSON.stringify({"recipients":["py"], "sender":"js", "data":"cmdlist", "id":id}))
    usedIDs[id.toString()] = "js"
    dataWaitingRoom[id.toString()] = {}
    pass() while "py" not in dataWaitingRoom[id.toString()] 
    pycmds = dataWaitingRoom[id.toString()].py
    delete dataWaitingRoom[id.toString()]
    cmds = ""
    for cmd in pycmds
      cmds = "#{cmds}#{cmd}: #{pycmds[cmd].description}"
    for cmd in client.commands
      console.log cmd

  client.commands.get('test').execute(message, args) if command == 'test' # todo: automate with for loop

client.login(token)