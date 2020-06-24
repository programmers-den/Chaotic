wss = new (require('ws').Server)(port: 9010, host: '127.0.0.1')

wss.on 'listening', () ->
  console.log "Ready!"

wss.on 'connection', (ws) ->
  ws.on 'message', (data) ->
    wss.clients.forEach (client) ->
      if client.readyState == WebSocket.OPEN
        client.send data
