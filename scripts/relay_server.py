#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This scripts runs a Socket.IO server that forwards all the messages from
# the neuronavigation system to the robot. That is, upon receiving a
# 'from_neuronavigation' message, it emits 'to_robot' message with the same
# data.
#
# Important:
#      :param data: The data to send to the client or clients. Data can be of
#      type ``str``, ``bytes``, ``list`` or ``dict``. To send
#      multiple arguments, use a tuple where each element is of
#      one of the types indicated above.
#

import asyncio
import sys

import nest_asyncio
import socketio
import uvicorn

import multiprocessing

class Server:
    def __init__(self, host='127.0.0.1', port=5000):
        # Configuração do servidor e eventos
        self.host = host
        self.port = port

        # Inicializando o servidor SocketIO
        self.sio = socketio.AsyncServer(async_mode='asgi')
        self.app = socketio.ASGIApp(self.sio)

        # Registrando eventos
        self._register_events()

    def _register_events(self):
        # Definindo os eventos do SocketIO
        @self.sio.event
        async def from_neuronavigation(sid, msg):
            await self._forward_to_robot(msg)

        @self.sio.event
        async def from_robot(sid, msg):
            await self._forward_to_neuronavigation(msg)

        @self.sio.event
        async def restart_robot_main_loop(sid):
            await self._restart_robot_main_loop()

    async def _forward_to_robot(self, msg):
        await self.sio.emit('to_robot', msg)
        print('Forwarding neuronavigation -> robot: %s' % str(msg))

    async def _forward_to_neuronavigation(self, msg):
        await self.sio.emit('to_neuronavigation', msg)
        print('Forwarding robot -> neuronavigation: %s' % str(msg))

    async def _restart_robot_main_loop(self):
        await self.sio.emit('restart_robot_main_loop')
        print('Restarting robot main_loop')

    def run(self):
        # Inicializa o servidor Uvicorn
        nest_asyncio.apply()
        uvicorn.run(self.app, host=self.host, port=self.port, loop='asyncio')

def run_server(host, port):
    server = Server(host, port)
    server.run()

def start_server(host, port):
    server_process = multiprocessing.Process(target=run_server, args=(host, port))
    server_process.start()

# Execução do servidor
if __name__ == '__main__':
    # Obtendo host e porta dos argumentos de linha de comando
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) == 2:
        host = '127.0.0.1'
        port = int(sys.argv[1])
    else:
        print(f'Usage: python {sys.argv[0]} [host] port')
        sys.exit(1)

    # Inicializando o servidor com os parâmetros de host e porta
    server = Server(host=host, port=port)
    server.run()

# import multiprocessing

# def start_server(self, app, host, port):
#     uvicorn.run(app, host=host, port=port, loop='asyncio')

# @sio.event
# def from_neuronavigation(sid, msg):
#     asyncio.create_task(sio.emit('to_robot', msg))
#     print('Forwarding neuronavigation -> robot: %s' % str(msg))

# @sio.event
# def from_robot(sid, msg):
#     asyncio.create_task(sio.emit('to_neuronavigation', msg))
#     print('Forwarding robot -> neuronavigation: %s' % str(msg))

# @sio.event
# def restart_robot_main_loop(sid):
#     asyncio.create_task(sio.emit('restart_robot_main_loop'))
#     print('Restarting robot main_loop')


# def startServer(host, port):

#     sio = socketio.AsyncServer(async_mode='asgi')
#     app = socketio.ASGIApp(sio)
    
#     nest_asyncio.apply()

#     default_host = '127.0.0.1'

#     server_process = multiprocessing.Process(target=start_server, args=(app, host, port))
#     server_process.start()



    # if len(sys.argv) == 3:
    #     host = sys.argv[1]
    #     port = int(sys.argv[2])
    # elif len(sys.argv) == 2:
    #     host = default_host
    #     port = int(sys.argv[1])
    # else:
    #     print(f'Usage: python {sys.argv[0]} [host] port')
    #     sys.exit(1)

    # sio = socketio.AsyncServer(async_mode='asgi')
    # app = socketio.ASGIApp(sio)

    # @sio.event
    # def from_neuronavigation(sid, msg):
    #     asyncio.create_task(sio.emit('to_robot', msg))
    #     print('Forwarding neuronavigation -> robot: %s' % str(msg))

    # @sio.event
    # def from_robot(sid, msg):
    #     asyncio.create_task(sio.emit('to_neuronavigation', msg))
    #     print('Forwarding robot -> neuronavigation: %s' % str(msg))

    # @sio.event
    # def restart_robot_main_loop(sid):
    #     asyncio.create_task(sio.emit('restart_robot_main_loop'))
    #     print('Restarting robot main_loop')


    # if __name__ == '__main__':
    #     uvicorn.run(app, host=host, port=port, loop='asyncio')
