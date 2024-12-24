# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Container(Base):
    """description: Represents a shipping container"""
    __tablename__ = 'container'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_code = Column(String)
    description = Column(String)
    status_id = Column(Integer, ForeignKey('status.id'))
    location_id = Column(Integer, ForeignKey('location.id'))
    type_id = Column(Integer, ForeignKey('container_type.id'))


class Status(Base):
    """description: Represents the various statuses a container can have (e.g., in transit, delivered, etc.)"""
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)


class Location(Base):
    """description: Represents different geographical locations relevant to the container logistics"""
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)


class ContainerType(Base):
    """description: Represents different types of containers such as refrigerated, dry storage etc."""
    __tablename__ = 'container_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)


class Journey(Base):
    """description: Represents the journey or trip a container undergoes from origin to destination"""
    __tablename__ = 'journey'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'))
    origin_id = Column(Integer, ForeignKey('location.id'))
    destination_id = Column(Integer, ForeignKey('location.id'))
    departure_date = Column(Date)
    arrival_date = Column(Date)


class TransitEvent(Base):
    """description: Represents events or updates during the transit of a container"""
    __tablename__ = 'transit_event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    journey_id = Column(Integer, ForeignKey('journey.id'))
    event_date = Column(Date)
    description = Column(String)


class Operator(Base):
    """description: Represents an operator who handles or manages the containers"""
    __tablename__ = 'operator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_info = Column(String)


class ContainerMaintenance(Base):
    """description: Represents maintenance or repairs executed on containers"""
    __tablename__ = 'container_maintenance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'))
    date = Column(Date)
    description = Column(String)
    cost = Column(Float)


class Inspection(Base):
    """description: Represents inspections carried out on containers"""
    __tablename__ = 'inspection'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'))
    date = Column(Date)
    result = Column(String)


class ContainerPosition(Base):
    """description: Represents GPS tracking information for containers at a given timestamp"""
    __tablename__ = 'container_position'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'))
    timestamp = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)


class Route(Base):
    """description: Represents predefined routes for container transport"""
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_location_id = Column(Integer, ForeignKey('location.id'))
    end_location_id = Column(Integer, ForeignKey('location.id'))
    distance = Column(Float)
    estimated_time = Column(Float)


class Booking(Base):
    """description: Represents the bookings made for shipping containers from one location to another"""
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('container.id'))
    operator_id = Column(Integer, ForeignKey('operator.id'))
    booking_date = Column(Date)
    pickup_date = Column(Date)
    delivery_date = Column(Date)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    container1 = Container(container_code="ABC123", description="Standard container", status_id=1, location_id=1, type_id=1)
    container2 = Container(container_code="XYZ456", description="Refrigerated container", status_id=2, location_id=2, type_id=2)
    container3 = Container(container_code="LMN789", description="Hazardous goods container", status_id=3, location_id=3, type_id=3)
    container4 = Container(container_code="QWE123", description="Open-top container", status_id=4, location_id=4, type_id=4)
    status1 = Status(name="In Transit", description="Container is currently being transported")
    status2 = Status(name="Delivered", description="Container has been delivered to destination")
    status3 = Status(name="Awaiting Pickup", description="Container is waiting to be picked up")
    status4 = Status(name="Under Maintenance", description="Container is currently under maintenance")
    location1 = Location(name="Port of Shanghai", longitude=31.2304, latitude=121.4737)
    location2 = Location(name="Port of Los Angeles", longitude=33.7405, latitude=-118.2662)
    location3 = Location(name="Port of Rotterdam", longitude=51.9494, latitude=4.1421)
    location4 = Location(name="Port of Singapore", longitude=1.2644, latitude=103.8228)
    container_type1 = ContainerType(name="Standard", description="Standard dry storage container")
    container_type2 = ContainerType(name="Refrigerated", description="Refrigerated container for perishables")
    container_type3 = ContainerType(name="Hazardous", description="Container for hazardous goods")
    container_type4 = ContainerType(name="Open-Top", description="Open-top container for bulky cargo")
    journey1 = Journey(container_id=1, origin_id=1, destination_id=2, departure_date=date(2023, 1, 15), arrival_date=date(2023, 2, 25))
    journey2 = Journey(container_id=2, origin_id=2, destination_id=3, departure_date=date(2023, 3, 5), arrival_date=date(2023, 4, 20))
    journey3 = Journey(container_id=3, origin_id=3, destination_id=4, departure_date=date(2023, 5, 10), arrival_date=date(2023, 6, 15))
    journey4 = Journey(container_id=4, origin_id=4, destination_id=1, departure_date=date(2023, 7, 20), arrival_date=date(2023, 9, 5))
    transit_event1 = TransitEvent(journey_id=1, event_date=date(2023, 1, 20), description="Loaded at Shanghai port")
    transit_event2 = TransitEvent(journey_id=2, event_date=date(2023, 3, 10), description="Departed from Los Angeles port")
    transit_event3 = TransitEvent(journey_id=3, event_date=date(2023, 5, 20), description="Delayed due to weather conditions")
    transit_event4 = TransitEvent(journey_id=4, event_date=date(2023, 7, 25), description="Inspected at Singapore port")
    operator1 = Operator(name="Global Shipping Ltd.", contact_info="global@shipping.com")
    operator2 = Operator(name="TransOcean Carriers", contact_info="info@transocean.com")
    operator3 = Operator(name="CargoExpress", contact_info="contact@cargoexpress.net")
    operator4 = Operator(name="FastTrack Logistics", contact_info="support@fasttracklogistics.com")
    container_maintenance1 = ContainerMaintenance(container_id=1, date=date(2023, 8, 1), description="Routine inspection and cleaning", cost=200.0)
    container_maintenance2 = ContainerMaintenance(container_id=2, date=date(2023, 9, 12), description="Refrigeration system repair", cost=750.0)
    container_maintenance3 = ContainerMaintenance(container_id=3, date=date(2023, 10, 5), description="Structura integrity check", cost=500.0)
    container_maintenance4 = ContainerMaintenance(container_id=4, date=date(2023, 11, 15), description="Roof tarpaulin replacement", cost=320.0)
    inspection1 = Inspection(container_id=1, date=date(2023, 6, 30), result="Passed")
    inspection2 = Inspection(container_id=2, date=date(2023, 7, 15), result="Passed with minor issues")
    inspection3 = Inspection(container_id=3, date=date(2023, 8, 20), result="Failed due to structural damage")
    inspection4 = Inspection(container_id=4, date=date(2023, 9, 25), result="Passed")
    container_position1 = ContainerPosition(container_id=1, timestamp=datetime(2023, 2, 1, 12, 30), longitude=131.0, latitude=13.5)
    container_position2 = ContainerPosition(container_id=2, timestamp=datetime(2023, 4, 8, 14, 45), longitude=140.0, latitude=36.5)
    container_position3 = ContainerPosition(container_id=3, timestamp=datetime(2023, 6, 17, 10, 15), longitude=120.0, latitude=28.0)
    container_position4 = ContainerPosition(container_id=4, timestamp=datetime(2023, 8, 20, 16, 22), longitude=110.0, latitude=55.6)
    route1 = Route(start_location_id=1, end_location_id=2, distance=13250.0, estimated_time=20.5)
    route2 = Route(start_location_id=2, end_location_id=3, distance=8450.0, estimated_time=15.0)
    route3 = Route(start_location_id=3, end_location_id=4, distance=9400.0, estimated_time=17.7)
    route4 = Route(start_location_id=4, end_location_id=1, distance=7700.0, estimated_time=14.2)
    booking1 = Booking(container_id=1, operator_id=1, booking_date=date(2023, 1, 10), pickup_date=date(2023, 1, 20), delivery_date=date(2023, 2, 25))
    booking2 = Booking(container_id=2, operator_id=2, booking_date=date(2023, 3, 2), pickup_date=date(2023, 3, 8), delivery_date=date(2023, 4, 25))
    booking3 = Booking(container_id=3, operator_id=3, booking_date=date(2023, 5, 1), pickup_date=date(2023, 5, 15), delivery_date=date(2023, 6, 20))
    booking4 = Booking(container_id=4, operator_id=4, booking_date=date(2023, 7, 10), pickup_date=date(2023, 7, 20), delivery_date=date(2023, 9, 15))
    
    
    
    session.add_all([container1, container2, container3, container4, status1, status2, status3, status4, location1, location2, location3, location4, container_type1, container_type2, container_type3, container_type4, journey1, journey2, journey3, journey4, transit_event1, transit_event2, transit_event3, transit_event4, operator1, operator2, operator3, operator4, container_maintenance1, container_maintenance2, container_maintenance3, container_maintenance4, inspection1, inspection2, inspection3, inspection4, container_position1, container_position2, container_position3, container_position4, route1, route2, route3, route4, booking1, booking2, booking3, booking4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
