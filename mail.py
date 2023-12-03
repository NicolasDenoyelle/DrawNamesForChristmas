import smtplib


class Email:
    def __init__(self, send_address: str, recv_address: str, message: str):
        self.sender_address = send_address
        self.receiver_address = recv_address
        self.message = message

    def __str__(self):
        ret = f"from: {self.sender_address}\n"
        ret += f"to: {self.receiver_address}\n\n"
        ret += f"{self.message}\n"
        return ret


class Server:
    def __init__(
        self,
        smtp_password,
        smtp_id="denoyelle.nicolas@gmail.com",
        smtp_server_address="smtp.gmail.com",
    ):
        self.smtp_server_address = smtp_server_address
        self.sender_address = smtp_id
        self.smtp_server = smtplib.SMTP_SSL(smtp_server_address)
        self.smtp_server.login(smtp_id, smtp_password)

    def __del__(self):
        self.smtp_server.quit()

    def __str__(self):
        ret = f"smtp_server: {self.smtp_server_address}\n"
        ret += f"sender_address: {self.sender_address}\n"
        return ret

    def Send(self, email: Email):
        self.server.sendmail(
            email.sender_address, email.receiver_address, email.message
        )
