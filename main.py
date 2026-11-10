from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Application
from schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello Maga"}


@app.post("/applications", response_model=ApplicationOut, status_code=201)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db)):
    application = Application(**data.model_dump(exclude_none=True))
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@app.get("/applications", response_model=list[ApplicationOut])
def list_applications(
    status: str | None = None,
    company: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Application)
    if status is not None:
        query = query.filter(Application.status == status)
    if company is not None:
        query = query.filter(Application.company.ilike(f"%{company}%"))
    return query.order_by(Application.applied_date.desc(), Application.id.desc()).all()

@app.get("/applications/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()



@app.patch("/applications/{application_id}", response_model=ApplicationOut)
def update_application(application_id: int, data: ApplicationUpdate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


@app.get("/analytics/status-counts")
def status_counts(db: Session = Depends(get_db)):
    rows = (
        db.query(Application.status, func.count(Application.id))
        .group_by(Application.status)
        .all()
    )
    return {status: count for status, count in rows}


@app.get("/analytics/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Application.id)).scalar()
    waiting = (
        db.query(func.count(Application.id))
        .filter(Application.status == "applied")
        .scalar()
    )
    responded = total - waiting
    rate = round(responded / total * 100, 1) if total > 0 else 0
    return {
        "total": total,
        "waiting": waiting,
        "responded": responded,
        "response_rate_percent": rate,
    }


@app.get("/analytics/monthly")
def monthly_counts(db: Session = Depends(get_db)):
    month = func.to_char(Application.applied_date, "YYYY-MM")
    rows = (
        db.query(month, func.count(Application.id))
        .group_by(month)
        .order_by(month)
        .all()
    )
    return {m: count for m, count in rows}