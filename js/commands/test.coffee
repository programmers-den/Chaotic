module.exports =
  name: 'test'
  description: 'A test command'
  execute: (message, args) ->
    message.channel.send 'JS: Test successful'
