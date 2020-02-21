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

def bytes_to_int(data:bytes) -> int:
    return(int.from_bytes(data, "little"))

class ClientSocket:
    def __init__(self, ip: str = config.SERVER_IP, port: int = config.SERVER_PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip = ip
        self._port = port
        self._connected = False
        self._message: str = ""
        self.connect_to_server(self._ip, self._port)
        print(f"socket: {self._socket}")

    @property
    def message(self) -> str:
        return self._message

    def connect_to_server(self, ip, port):
        if not self._connected:
            self._socket.connect((ip, port))
            self._connected = True

    def _get_command(self) -> str:
        if not self._connected:
            print("trying to connect to server")
            self.connect_to_server(self._ip, self._port)
        data = bytes()
        while len(data) < 3:
            data += self._socket.recv(3 - len(data))
        return data.decode()

    def _get_message(self, length: int) -> str:
        if not self._connected:
            print("trying to connect to server")
            self.connect_to_server(self._ip, self._port)
        data: bytes = bytes()
        while len(data) < length:
            data += self._socket.recv(1 - len(data))
        return data

    def _parse_message(self) -> Tuple[str, Any]:
        command: str = self._get_command()
        print(f"received command: {command}")
        if command == "END":
            raise EndException()
        if command == "BYE":
            raise ByeException()
        elif command not in ["SET", "HUM", "HME", "MAP", "UPD"]:
            raise ValueError("Command unknown")

        if command == "SET":
            return ("set", (bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1))))

        if command == "HUM":
            humans = []
            nb = bytes_to_int(self._get_message(1))
            print(nb)

            for i in range(nb):
                print(humans)
                humans += [bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1))]
            print(humans)
            return(["hum"]+humans)
            #return "hum", [tuple(map(bytes_to_int, self._get_message(2))) for _ in range(bytes_to_int(self._get_message(1)))]

        if command == "HME":
            return "hme", (bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)))

        if command == "MAP":
            map = []
            nb = bytes_to_int(self._get_message(1))
            print(nb)
            for i in range(nb):
                print(map)
                map += [[bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1))]]
            print(map)
            return (["map"] + [map])

        if command == "UPD":
            upd = []
            nb = bytes_to_int(self._get_message(1))
            print(nb)

            for i in range(nb):
                print(upd)
                upd += [[bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1)), bytes_to_int(self._get_message(1))]]
            print(upd)
            return (["upd"] + [upd])

    def get_message(self) -> Tuple[str, Any]:
        try:
            self._message = self._parse_message()
            print(self._message)
            return self._message
        except OSError:
            pass
        except IOError as e:
            print(e)
        except EndException:
            raise
        except ByeException:
            raise

    def send_NME(self, name:str):
        if not self._connected:
            print("trying to connect to server")
            self.connect_to_server(self._ip, self._port)

        self._socket.send("NME".encode() + bytes([len(name)]) + name.encode())

    def send_MOV(self, nb_moves:int, moves):
        message = bytes([nb_moves])
        for move in moves:
            for data in move:
                print(data)
                message += bytes([data])

        self._socket.send("MOV".encode() + message)


    def _send_command(self, command: str):
        if not self._connected:
            print("trying to connect to server")
            self.connect_to_server(self._ip, self._port)
        command = str(command)
        if command == "nme":
            command = "NME"
        elif command == "mov":
            command = "MOV"
        else:
            raise UnknownCommand(f"Command {command} unknown")
        self._socket.send(command.encode())

    def send_message(self, message: Tuple[str, Any]):
        if not self._connected:
            print("trying to connect to server")
            self.connect_to_server(self._ip, self._port)
        self._send_command(message[0])
        if message[0] == "nme":
            self._socket.send(bytes([len(message[1])]) + message[1].encode())
        elif message[0] == "mov":
            self._socket.send()

