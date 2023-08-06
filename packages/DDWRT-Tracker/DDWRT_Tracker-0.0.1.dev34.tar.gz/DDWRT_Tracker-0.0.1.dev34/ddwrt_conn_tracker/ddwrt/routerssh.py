import re
import socket
from collections import namedtuple
from datetime import datetime

import attr
from fabric import Connection, Result
from loguru import logger

ConnectionInfo = namedtuple('ConnectionInfo', 'ip mac dt device')


@attr.s
class RouterSSH:
    host: str = attr.ib()
    port: int = attr.ib(kw_only=True)
    user: str = attr.ib(kw_only=True)
    password: str = attr.ib(kw_only=True, repr=False)
    _conn: Connection = None

    @property
    def connection(self):
        if not self._conn:
            self._conn = Connection(self.host, port=self.port, user=self.user,
                                    connect_kwargs={'password': self.password}, connect_timeout=10)

        return self._conn

    def execute(self, command: str, hide=True) -> Result:
        try:
            return self.connection.run(command, hide=hide)
        except socket.timeout:
            logger.error(f'Failed to execute: Timeout')
            exit(1)

    def get_active_connections(self) -> [ConnectionInfo]:
        cmd = 'arp -a'
        active_connections: Result = self.execute(cmd)
        pattern = re.compile('(\S+)\s\((\d+.\d+.\d+.\d+)\) at (\S+\:\S+\:\S+\:\S+\:\S+\:\S+)')
        return [ConnectionInfo(device=i[0], ip=i[1], mac=i[2], dt=datetime.utcnow()) for i in
                pattern.findall(active_connections.stdout)]
