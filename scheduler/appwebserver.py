import zerorpc
from aiohttp import web, log

client = zerorpc.Client()
client.connect('tcp://127.0.0.1:9000')


async def handle(request:web.Request):
    txt = client.get_agents()
    return web.json_response(txt)

async  def add_taskhandler(request:web.Request):
    date = await request.json()
    return web.json_response(client.add_task(date),status=201)

app = web.Application()
app.add_routes([web.get('/task/agents', handle),
                web.post('/task',add_taskhandler)])

web.run_app(app, host='0.0.0.0', port=9527)