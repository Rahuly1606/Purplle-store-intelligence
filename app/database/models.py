from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import Text

from app.database.database import Base


class EventDB(Base):

    __tablename__ = "events"

    event_id = Column(String, primary_key=True)

    store_id = Column(String, nullable=False)

    camera_id = Column(String, nullable=False)

    visitor_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    timestamp = Column(String, nullable=False)

    zone_id = Column(String)

    dwell_ms = Column(Integer, default=0)

    is_staff = Column(Boolean, default=False)

    confidence = Column(Float)

    metadata_json = Column(Text)