# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 24, 2024 03:34:53
# Database: sqlite:////tmp/tmp.f75uapp7OE-01JFVBKW7CGY9A0QSYDS39FHDV/ContainerTrackingAPI/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class ContainerType(SAFRSBaseX, Base):
    """
    description: Represents different types of containers such as refrigerated, dry storage etc.
    """
    __tablename__ = 'container_type'
    _s_collection_name = 'ContainerType'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerList : Mapped[List["Container"]] = relationship(back_populates="type")



class Location(SAFRSBaseX, Base):
    """
    description: Represents different geographical locations relevant to the container logistics
    """
    __tablename__ = 'location'
    _s_collection_name = 'Location'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerList : Mapped[List["Container"]] = relationship(back_populates="location")
    RouteList : Mapped[List["Route"]] = relationship(foreign_keys='[Route.end_location_id]', back_populates="end_location")
    startRouteList : Mapped[List["Route"]] = relationship(foreign_keys='[Route.start_location_id]', back_populates="start_location")
    JourneyList : Mapped[List["Journey"]] = relationship(foreign_keys='[Journey.destination_id]', back_populates="destination")
    originJourneyList : Mapped[List["Journey"]] = relationship(foreign_keys='[Journey.origin_id]', back_populates="origin")



class Operator(SAFRSBaseX, Base):
    """
    description: Represents an operator who handles or manages the containers
    """
    __tablename__ = 'operator'
    _s_collection_name = 'Operator'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="operator")



class Status(SAFRSBaseX, Base):
    """
    description: Represents the various statuses a container can have (e.g., in transit, delivered, etc.)
    """
    __tablename__ = 'status'
    _s_collection_name = 'Status'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ContainerList : Mapped[List["Container"]] = relationship(back_populates="status")



class Container(SAFRSBaseX, Base):
    """
    description: Represents a shipping container
    """
    __tablename__ = 'container'
    _s_collection_name = 'Container'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_code = Column(String)
    description = Column(String)
    status_id = Column(ForeignKey('status.id'))
    location_id = Column(ForeignKey('location.id'))
    type_id = Column(ForeignKey('container_type.id'))

    # parent relationships (access parent)
    location : Mapped["Location"] = relationship(back_populates=("ContainerList"))
    status : Mapped["Status"] = relationship(back_populates=("ContainerList"))
    type : Mapped["ContainerType"] = relationship(back_populates=("ContainerList"))

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="container")
    ContainerMaintenanceList : Mapped[List["ContainerMaintenance"]] = relationship(back_populates="container")
    ContainerPositionList : Mapped[List["ContainerPosition"]] = relationship(back_populates="container")
    InspectionList : Mapped[List["Inspection"]] = relationship(back_populates="container")
    JourneyList : Mapped[List["Journey"]] = relationship(back_populates="container")



class Route(SAFRSBaseX, Base):
    """
    description: Represents predefined routes for container transport
    """
    __tablename__ = 'route'
    _s_collection_name = 'Route'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    start_location_id = Column(ForeignKey('location.id'))
    end_location_id = Column(ForeignKey('location.id'))
    distance = Column(Float)
    estimated_time = Column(Float)

    # parent relationships (access parent)
    end_location : Mapped["Location"] = relationship(foreign_keys='[Route.end_location_id]', back_populates=("RouteList"))
    start_location : Mapped["Location"] = relationship(foreign_keys='[Route.start_location_id]', back_populates=("startRouteList"))

    # child relationships (access children)



class Booking(SAFRSBaseX, Base):
    """
    description: Represents the bookings made for shipping containers from one location to another
    """
    __tablename__ = 'booking'
    _s_collection_name = 'Booking'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'))
    operator_id = Column(ForeignKey('operator.id'))
    booking_date = Column(Date)
    pickup_date = Column(Date)
    delivery_date = Column(Date)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("BookingList"))
    operator : Mapped["Operator"] = relationship(back_populates=("BookingList"))

    # child relationships (access children)



class ContainerMaintenance(SAFRSBaseX, Base):
    """
    description: Represents maintenance or repairs executed on containers
    """
    __tablename__ = 'container_maintenance'
    _s_collection_name = 'ContainerMaintenance'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'))
    date = Column(Date)
    description = Column(String)
    cost = Column(Float)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("ContainerMaintenanceList"))

    # child relationships (access children)



class ContainerPosition(SAFRSBaseX, Base):
    """
    description: Represents GPS tracking information for containers at a given timestamp
    """
    __tablename__ = 'container_position'
    _s_collection_name = 'ContainerPosition'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'))
    timestamp = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("ContainerPositionList"))

    # child relationships (access children)



class Inspection(SAFRSBaseX, Base):
    """
    description: Represents inspections carried out on containers
    """
    __tablename__ = 'inspection'
    _s_collection_name = 'Inspection'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'))
    date = Column(Date)
    result = Column(String)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("InspectionList"))

    # child relationships (access children)



class Journey(SAFRSBaseX, Base):
    """
    description: Represents the journey or trip a container undergoes from origin to destination
    """
    __tablename__ = 'journey'
    _s_collection_name = 'Journey'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    container_id = Column(ForeignKey('container.id'))
    origin_id = Column(ForeignKey('location.id'))
    destination_id = Column(ForeignKey('location.id'))
    departure_date = Column(Date)
    arrival_date = Column(Date)

    # parent relationships (access parent)
    container : Mapped["Container"] = relationship(back_populates=("JourneyList"))
    destination : Mapped["Location"] = relationship(foreign_keys='[Journey.destination_id]', back_populates=("JourneyList"))
    origin : Mapped["Location"] = relationship(foreign_keys='[Journey.origin_id]', back_populates=("originJourneyList"))

    # child relationships (access children)
    TransitEventList : Mapped[List["TransitEvent"]] = relationship(back_populates="journey")



class TransitEvent(SAFRSBaseX, Base):
    """
    description: Represents events or updates during the transit of a container
    """
    __tablename__ = 'transit_event'
    _s_collection_name = 'TransitEvent'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    journey_id = Column(ForeignKey('journey.id'))
    event_date = Column(Date)
    description = Column(String)

    # parent relationships (access parent)
    journey : Mapped["Journey"] = relationship(back_populates=("TransitEventList"))

    # child relationships (access children)
