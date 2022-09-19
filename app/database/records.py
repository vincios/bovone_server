from datetime import datetime

from sqlalchemy.orm import Session

from .. import schemas
from app.database import model


def get_record(db: Session, record_id: int):
    return db.query(model.Record).filter_by(id=record_id).first()


def get_record_by_period(db: Session, start: datetime, end: datetime):
    return db.query(model.Record).filter(model.Record.time >= start, model.Record.time <= end).all()


def save_record(db: Session, record: schemas.RecordSchema):
    db_record = model.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record
