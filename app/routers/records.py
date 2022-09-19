import datetime

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..database import records
from ..dependencies import get_session
router = APIRouter(prefix="/records", tags=["records"])


@router.post('/', response_model=schemas.DBRecordSchema)
async def create_record(record: schemas.RecordSchema, session: Session = Depends(get_session)):
    # db_record = get_record(session, record.id)
    # if db_record:
    #     raise HTTPException(status_code=400, detail="Record already present")

    return records.save_record(db=session, record=record)


@router.get("/{record_id}", response_model=schemas.DBRecordSchema)
async def read_record(record_id: int, session: Session = Depends(get_session)):
    db_record = records.get_record(session, record_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")

    return db_record


@router.get("/", response_model=list[schemas.DBRecordSchema])
def get_records_period(start_time: datetime.datetime, end_time: datetime.datetime,
                       session: Session = Depends(get_session)):
    db_records: list[schemas.DBRecordSchema] = records.get_record_by_period(session, start_time, end_time)
    # if not db_records:
    #     raise HTTPException(status_code=404, detail="No records found")

    return db_records

