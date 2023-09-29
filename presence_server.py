import json
from socket import SOCK_DGRAM, socket, AF_INET
from presence_client import ClientTypes, Message


class PresenceServer:
    def __init__(self, server: socket, host: str = "127.0.0.1", port: int = 4000):
        self.host = host
        self.port = port
        self.server = server
        self.server.bind((self.host, self.port))
        self.presence_list: list[str] = []
        self.class_id = 0
        self.is_open = False

    def run(self):
        print("Servidor de chamadas rodando na porta", self.port)
        message: str = ""
        while message != "sair":
            data, address = self.server.recvfrom(1024)
            message_data: Message = json.loads(data.decode())
            message = self.get_message(message_data)
            if self.is_professor(message_data):
                self.handle_professor_message(message, address)
            else:
                self.handle_student_message(message, address)

    def is_professor(self, data: Message):
        return data["user"] == ClientTypes.PROFESSOR.value

    def handle_professor_message(self, message, address):
        if message == "fechar":
            self.is_open = False
            self.server.sendto(
                f"Alunos presentes na turma {self.class_id}: {self.presence_list}".encode(),
                address,
            )
            return
        if self.is_open:
            self.server.sendto(
                f"A chamada já está aberta. Feche a chamada da turma {self.class_id}".encode(),
                address,
            )
            return
        self.class_id = message
        self.is_open = True
        self.server.sendto(f"Chamada da turma {message} iniciada".encode(), address)

    def handle_student_message(self, message, address):
        if message == "fechar":
            self.server.sendto("".encode(), address)
            return
        if not self.is_open:
            self.server.sendto("A chamada está fechada".encode(), address)
            return
        self.presence_list.append(message)
        self.server.sendto(
            f"Presença do aluno registrada ({message})".encode(), address
        )

    def get_message(self, message_data: Message):
        return message_data["message"]


if __name__ == "__main__":
    server = socket(SOCK_DGRAM, AF_INET)
    PresenceServer(server).run()
    print("Servidor fechando")
    server.close()
