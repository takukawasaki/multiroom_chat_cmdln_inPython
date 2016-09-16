#!/usr/bin/python3

import select
import  socket
import sys
import  pdb
from util import Chat, Room, Player
import util

BUF = 4096

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = util.make_socket((host, util.PORT))

chat = Chat()
connection_list = []
connection_list.append(listen_sock)

while True:
    # Player.fileno()
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock: # new connection, player is a socket
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            chat.welcome_new(new_player)

        else: # new message
            msg = player.socket.recv(BUF)
            if msg:
                msg = msg.decode().lower()
                chat.handle_msg(player, msg)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
