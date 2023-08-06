# Installing
```
python3 -m pip install aiocord
```
# Simple Usage
```py
import asyncio
import aiohttp
import aiocord.engine # external

token = 'APPLICATION_TOKEN'

# get the event loop
loop = asyncio.get_event_loop()

# create a session
session = aiohttp.ClientSession(loop = loop)

# cooperative client
client = aiocord.engine.Client(session, token, loop = loop)

@client.track('ready')
async def handle_0(shard, version, initial_guild_ids):

    # caution! blocking
    print(shard, 'ready')

@client.track('message create')
async def handle_1(shard, guild, channel, message):

    signal = '.say '

    if message.content.startswith(signal):

        response = message.content[len(signal):]

        await client.create_message(channel.id, content = response)

async def initialize():

    await client.start()

async def finalize():

    await client.close()

    await session.close()

try:

    loop.run_until_complete(initialize())

    try:

        loop.run_forever()

    except KeyboardInterrupt:

        pass

finally:

    loop.run_until_complete(finalize())
```
# Advanced Usage
```py
import asyncio
import aiohttp
import aiocord
import functools

token = 'APPLICATION_TOKEN'

# get the event loop
loop = asyncio.get_event_loop()

# create a session
session = aiohttp.ClientSession(loop = loop)

# used for fetching info
rest = aiocord.rest.Client(session, loop = loop)

# authorize
rest.authorize(token)

# this is our stream handler
def handle(shard, event, data):

    # caution! blocking
    print(shard, event)

    if event == 'READY':

        session_id = data['session_id']

        # needed for resume
        shard.patch(session_id)

        return

shards = []

async def initialize():

    # sharding information
    data = await rest.get_gateway_bot()

    # shard count and gateway url
    count, url = data['shards'], data['url']

    # index is the shard id
    for index in range(count):

        # needed for identify
        info = (index, count)

        # used for listening to events
        gateway = aiocord.gateway.Client(session, token, info, loop = loop)

        # docs advice to routinely update the response of the
        # get gateway bot request, hence why this method exists
        gateway.update(url)

        # pass the current gateway to our handler
        callback = functools.partial(handle, gateway)

        # will be called with
        # every event dispatch
        gateway.track(callback)

        # connect, start event steam
        # and identify with info given
        await gateway.start()

        shards.append(gateway)

        if not index < count:

            break

        await asyncio.sleep(5.5)

async def finalize():

    for gateway in shards:

        await gateway.close()

    await session.close()

try:

    loop.run_until_complete(initialize())

    try:

        loop.run_forever()

    except KeyboardInterrupt:

        pass

finally:

    loop.run_until_complete(finalize())
```
