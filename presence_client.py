import argparse
import sys
from enum import Enum
from socket import AF_INET, SOCK_DGRAM, socket


class ClientTypes(Enum):
    PROFESSOR = "professor"
    STUDENT = "aluno"


class PresenceClient:
    def __init__(
        self,
        user: ClientTypes = ClientTypes.STUDENT,
        host: str = "127.0.0.1",
        port: int = 4000,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.client = socket(SOCK_DGRAM, AF_INET)

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


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0 and (args[0] == "-p" or args[0] == "--professor"):
        PresenceClient(user=ClientTypes.PROFESSOR).run()
    else:
        PresenceClient().run()
