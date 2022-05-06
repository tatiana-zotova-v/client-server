import asyncio

class ClientServerProtocol(asyncio.Protocol):
    data = {}
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    @classmethod
    def process_data(cls, string_data):
        answer = 'ok\n'
        try:
            command, data = string_data.split(' ', 1)
            if command == 'get':
                data = data.rstrip()
                print(data)
                if ' ' in data or not data:
                    raise Exception
                if data == "*":
                    for metric in cls.data:
                        for timestamp, value in cls.data[metric].items():
                            answer += '{} {} {}\n'.format(metric, value, timestamp)
                else:
                    dict_data = cls.data.get(data, {})
                    print("dict_data    ", dict_data)
                    for timestamp, value in dict_data.items():
                        answer += '{} {} {}\n'.format(data, value, timestamp)
                        print(answer)
            elif command == 'put':
                metric, value, timestamp = data.split()
                print('{} {} {}\n'.format(metric, value, timestamp))
                if not metric in cls.data:
                    cls.data[metric] = {}
                cls.data[metric].update([(int(timestamp), float(value))])
            else:
                raise Exception
        except:
            return "error\nwrong command\n\n"
        else:
            answer += '\n'
            return answer


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server('127.0.0.1', 10001)