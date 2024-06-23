#!/usr/bin/env python

import asyncio
import secrets

import websockets
import json
from datetime import datetime
 

connected = []

def addToConnected(websocket):
    """
    Function to add the websocket of people
    """ 
    if websocket not in connected:
        connected.append(websocket)
    return connected

async def handler(websocket): 
    connected = addToConnected(websocket)
    async for message in websocket:
        #ajout de la date, l'heure au message.
        event = json.loads(message)
        now = datetime.now()
        event["date"] = now.strftime("%m-%d")
        event["hour"] = now.strftime("%H:%M")
 
        #envoi à tous les membres
        websockets.broadcast(connected, json.dumps(event)) 


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())