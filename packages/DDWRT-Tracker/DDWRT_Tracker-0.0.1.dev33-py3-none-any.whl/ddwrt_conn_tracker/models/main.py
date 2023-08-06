from __future__ import annotations

import datetime
import re

from sqlalchemy import Column, Integer, String, create_engine, BigInteger, MetaData, ForeignKey, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import ScopedSession, scoped_session

from ddwrt_conn_tracker.ddwrt import ConnectionInfo
from ddwrt_conn_tracker.definitions import DATA_FILE
from ddwrt_conn_tracker.models.constants import CONNECTED, DISCONNECTED

my_meta_data = MetaData()
engine = create_engine(f'sqlite:///' + DATA_FILE.as_posix())

Session: ScopedSession = scoped_session(sessionmaker(bind=engine))


class InvalidMacAddressError(Exception):
    pass


class InvalidIpAddressError(Exception):
    pass


class BaseModel:
    query = Session.query_property()

    pk = Column('pk', BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)

    def save_to_db(self):
        Session.add(self)
        Session.commit()

    @classmethod
    def find_by_pk(cls, pk: int):
        return cls.query.get(pk)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_list_of_pk(cls, pks: [int]):
        return cls.query.filter(cls.pk.in_(pks)).all()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pk})'


Model = declarative_base(cls=BaseModel, metadata=my_meta_data)


class MacAddressModel(Model):
    __tablename__ = 'mac_address'
    _mac_address = Column('str_mac_address', String(50), nullable=False, unique=True)

    @hybrid_property
    def mac_address(self):
        return self._mac_address

    @mac_address.setter
    def mac_address(self, value: str):
        mac_address_pattern = re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_address_pattern.match(value):
            raise InvalidMacAddressError(f'{value} is not a valid MAC-address')
        self._mac_address = value

    def __init__(self, mac_address):
        self.mac_address = mac_address

    @classmethod
    def prompt_init(cls):
        return cls(**{
                'mac_address': input('MAC-address:')
                })

    @classmethod
    def find_or_create(cls, mac_address: str) -> MacAddressModel:
        found = cls.query.filter_by(mac_address=mac_address).first()
        if found:
            return found
        new_mac_address = cls(mac_address)
        new_mac_address.save_to_db()
        return new_mac_address


class EventTypeModel(Model):
    __tablename__ = 'event_type'

    name = Column('str_name', String(50), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def find_by_name(cls, name: str) -> EventTypeModel:
        return cls.query.filter_by(name=name).first()


class EventModel(Model):
    __tablename__ = 'event'

    mac_id = Column('fk_mac_address', Integer, ForeignKey('mac_address.pk'), nullable=False)
    event_type_id = Column('fk_event_type', Integer, ForeignKey('event_type.pk'), nullable=False)
    _ip = Column('str_ip_address', String(50))
    device_name = Column('str_device_name', String(50))
    dt_created = Column('dt_created', DateTime)

    mac = relationship('MacAddressModel', foreign_keys=[mac_id], uselist=False, lazy='joined')

    def __init__(self, *, mac_address: str, event_type: str, dt_created: datetime.datetime = datetime.datetime.now(),
                 ip: str = None, device_name: str = None):
        found_mac_address = MacAddressModel.find_or_create(mac_address)
        found_event_type = EventTypeModel.find_by_name(event_type)
        self.mac_id = found_mac_address.pk
        self.event_type_id = found_event_type.pk
        self.dt_created = dt_created
        self.ip = ip
        self.device_name = device_name

    @hybrid_property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        pattern = re.compile('\d+.\d+.\d+.\d+')
        if value and not pattern.match(value):
            raise InvalidIpAddressError(f'{value} is not a valid IP address')
        self._ip = value

    @classmethod
    def record_connection(cls, mac_address: str, dt_created: datetime, ip: str = None, device_name: str = None) -> EventModel:
        new_event = cls(mac_address=mac_address, event_type=CONNECTED, dt_created=dt_created, ip=ip, device_name=device_name)
        new_event.save_to_db()
        return new_event

    def record_disconnection(self) -> EventModel:
        new_record = EventModel(mac_address=self.mac.mac_address, event_type=DISCONNECTED,
                                dt_created=datetime.datetime.utcnow(), ip=self.ip, device_name=self.device_name)
        new_record.save_to_db()
        return new_record

    @classmethod
    def find_last_event_for_address(cls, mac_address: str) -> EventModel:
        mac_address_pk = MacAddressModel.find_or_create(mac_address).pk
        return cls.query.filter_by(mac_id=mac_address_pk).order_by(desc('dt_created')).limit(1).first()

    @classmethod
    def find_all_connected(cls):
        query = f'''select pk from event where 
                    pk in (
                            select max(pk) from event
                            group by fk_mac_address
                            )
                    and fk_event_type = 1
                    '''
        res = engine.execute(query).fetchall()
        if not res:
            return []

        pks = [i[0] for i in res]
        return cls.find_by_list_of_pk(pks)

    @classmethod
    def _find_new_connections(cls, active_connections: [ConnectionInfo], saved_connections: [EventModel] = None) -> [
            ConnectionInfo]:
        if not saved_connections:
            saved_connections = cls.find_all_connected()
        saved_mac_addresses = [i.mac.mac_address for i in saved_connections]
        return filter(lambda x: x.mac not in saved_mac_addresses, active_connections)

    @classmethod
    def _find_disconnected(cls, active_connections: [ConnectionInfo], saved_connections: [EventModel] = None) -> [
            ConnectionInfo]:
        if not saved_connections:
            saved_connections = cls.find_all_connected()
        active_mac_addresses = [i.mac for i in active_connections]
        return filter(lambda x: x.mac.mac_address not in active_mac_addresses, saved_connections)

    @classmethod
    def update(cls, active_connections: [ConnectionInfo]) -> True:
        saved_connections = cls.find_all_connected()
        new_connections = cls._find_new_connections(active_connections, saved_connections=saved_connections)
        disconnected = cls._find_disconnected(active_connections, saved_connections=saved_connections)
        for con in new_connections:
            cls.record_connection(con.mac, con.dt, ip=con.ip, device_name=con.device)
        for dis in disconnected:
            dis.record_disconnection()
        return True
