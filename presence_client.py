import argparse
import os
import sys
from enum import Enum
from socket import AF_INET, SOCK_DGRAM, socket


class ClientTypes(Enum):
    PROFESSOR = "professor"
    STUDENT = "aluno"


class PresenceClient:
    def __init__(
        self,
        client: socket,
        user: ClientTypes = ClientTypes.STUDENT,
        host: str = "127.0.0.1",
        port: int = 4000,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.client = client

    def run(self):
        message: str = ""

        if self.user == ClientTypes.PROFESSOR:
            print("Iniciando client como professor\n Digite o ID da Turma")

        while message != "fechar":
            message = input(">>> ")
            self.client.sendto(
                f"{self.user.value}: {message}".encode(), (self.host, self.port)
            )
            response, addr = self.client.recvfrom(1024)
            response_message = response.decode()
            print(response_message)

        self.client.close()


def is_professor():
    args = sys.argv[1:]
    return len(args) > 0 and (args[0] == "-p" or args[0] == "--professor")


if __name__ == "__main__":
    client = socket(SOCK_DGRAM, AF_INET)
    if is_professor():
        PresenceClient(client, ClientTypes.PROFESSOR).run()
        quit()
    PresenceClient(client).run()
