#!/usr/bin/env python

import asyncio
import secrets

import websockets
import json
 

async def handler(websocket):
    async for message in websocket:
        print(message)



async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())