import socket
import struct
from typing import Any, Tuple

import config


class EndException(Exception):
    pass


class ByeException(Exception):
    pass


class UnknownCommand(Exception):
    pass


class ClientSocket:
    def __init__(self, soc: socket.socket = None, ip: str = config.SERVER_IP, port: int = config.SERVER_PORT):
        self._socket = soc
        self._ip = ip
        self._port = port
        if not self._socket:
            self._socket = self.get_server_socket()
        self._connexion = None
        self._message: str = ""

    @property
    def connexion(self) -> socket.socket:
        return self._connexion

    @property
    def message(self) -> str:
        return self._message

    def get_server_socket(self) -> socket.socket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soc:
            server_soc.bind((self._ip, self._port))
            server_soc.listen(1)
            return server_soc

    def _get_command(self) -> str:
        data = bytes()
        while len(data) < 3:
            data += self._connexion.recv(3 - len(data))
        return data.decode()

    def _get_message(self, length: int) -> str:
        data: bytes = bytes()
        while len(data) < length:
            data += self._connexion.recv(1 - len(data))
        return data.decode()

    def _parse_message(self) -> Tuple[str, Any]:
        command: str = self._get_command()
        if command == "END":
            raise EndException()
        if command == "BYE":
            raise ByeException()
        elif command not in ["SET", "HUM", "HME", "MAP", "UPD"]:
            raise ValueError("Command unknown")
        if command == "SET":
            return "set", (int(self._get_message(1)), int(self._get_message(1)))
        if command == "HUM":
            return "hum", [tuple(map(int, self._get_message(2))) for _ in range(int(self._get_message(1)))]
        if command == "HME":
            return "hme", (int(self._get_message(1)), int(self._get_message(1)))
        if command == "MAP":
            return "map", [tuple(map(int, self._get_message(5))) for _ in range(int(self._get_message(1)))]
        if command == "UPD":
            return "upd", [tuple(map(int, self._get_message(5))) for _ in range(int(self._get_message(1)))]

    def get_message(self) -> Tuple[str, Any]:
        try:
            self._connexion, client = self._socket.accept()
            self._message = self._parse_message()
            return self._message
        except OSError:
            pass
        except IOError as e:
            print(e)
        except EndException:
            raise
        except ByeException:
            raise

    def _send_command(self, command: str):
        command = str(command)
        if command == "nme":
            command = "NME"
        elif command == "mov":
            command = "MOV"
        else:
            raise UnknownCommand(f"Command {command} unknown")
        self._connexion.send(command.encode())

    def send_message(self, message: Tuple[str, Any]):
        self._send_command(message[0])
        if message[0] == "nme":
            self._connexion.send(struct.pack("d", int(message[1][0])))
            self._connexion.send(message[1][1].encode())
        elif message[0] == "mov":
            self._connexion.send(struct.pack("d", int(message[1][0])))
            self._connexion.send("".join(map(str, message[1[1]])))
