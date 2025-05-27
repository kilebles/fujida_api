from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class DeviceModel(Base):
    __tablename__ = 'device_models'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    embedding = Column(Vector(1536))
    is_active = Column(Boolean, default=False)
    is_detector = Column(Boolean, default=False)

    specs = relationship('DeviceSpec', back_populates='model', cascade='all, delete')


class DeviceSpec(Base):
    __tablename__ = 'device_specs'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('device_models.id', ondelete='CASCADE'))
    name = Column(String, nullable=False)
    value = Column(String, nullable=True)

    model = relationship('DeviceModel', back_populates='specs')


class FAQEntry(Base):
    __tablename__ = 'faq_entries'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    embedding = Column(Vector(1536))