const Koa = require('koa')
const Redis = require('ioredis')
const io = require('socket.io')()
const app = new Koa()
const redis = new Redis()

const sub = redis.client();
sub.subscribe('test_channel');
app.listen(3000)