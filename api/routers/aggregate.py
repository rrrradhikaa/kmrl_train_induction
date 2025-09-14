from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, Dict, Any, List
from datetime import date
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models

router = APIRouter(prefix="/trains", tags=["Aggregate Variables"])

@router.get("/{train_id}/variables")
def variables_view(
    train_id: str,
    coach_id: Optional[str] = None,
    latest: bool = True,     # true => latest per (train,coach)
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    result: Dict[str, Any] = {"train_id": train_id}

    # Filter helper
    def filt(cls):
        q = db.query(cls).filter(cls.train_id == train_id)
        if coach_id:
            q = q.filter(cls.coach_id == coach_id)
        return q

    # 1) Fitness certificates (optionally latest per coach)
    if latest:
        sub = (
            db.query(
                models.FitnessCertificate.train_id,
                models.FitnessCertificate.coach_id,
                func.max(models.FitnessCertificate.fitness_check_date).label("max_dt"),
            )
            .filter(models.FitnessCertificate.train_id == train_id)
            .group_by(models.FitnessCertificate.train_id, models.FitnessCertificate.coach_id)
            .subquery()
        )
        fc = (
            db.query(models.FitnessCertificate)
            .join(
                sub,
                and_(
                    models.FitnessCertificate.train_id == sub.c.train_id,
                    models.FitnessCertificate.coach_id == sub.c.coach_id,
                    models.FitnessCertificate.fitness_check_date == sub.c.max_dt,
                ),
            )
        )
        if coach_id:
            fc = fc.filter(models.FitnessCertificate.coach_id == coach_id)
        result["fitness_certificates"] = [x.__dict__ for x in fc.all()]
    else:
        result["fitness_certificates"] = [x.__dict__ for x in filt(models.FitnessCertificate).all()]

    # 2) Open job-cards (simple heuristic)
    open_vals = {"open", "opened", "pending", "in-progress"}
    jobs = [
        x.__dict__
        for x in filt(models.JobCard).all()
        if (x.status or "").strip().lower() in open_vals or (not x.status)
    ]
    result["job_cards_open"] = jobs

    # 3) Active branding (deadline >= today, sorted by priority)
    today = date.today()
    branding_q = filt(models.BrandingPriority)
    branding = branding_q.filter(
        (models.BrandingPriority.deadline.is_(None)) | (models.BrandingPriority.deadline >= today)
    ).order_by(models.BrandingPriority.priority.asc().nulls_last()).all()
    result["branding_active"] = [x.__dict__ for x in branding]

    # 4) Mileage latest per coach
    sub_m = (
        db.query(
            models.MileageBalancing.train_id,
            models.MileageBalancing.coach_id,
            func.max(models.MileageBalancing.id).label("max_id"),
        )
        .filter(models.MileageBalancing.train_id == train_id)
        .group_by(models.MileageBalancing.train_id, models.MileageBalancing.coach_id)
        .subquery()
    )
    mil_q = db.query(models.MileageBalancing).join(
        sub_m,
        and_(
            models.MileageBalancing.train_id == sub_m.c.train_id,
            models.MileageBalancing.coach_id == sub_m.c.coach_id,
            models.MileageBalancing.id == sub_m.c.max_id,
        ),
    )
    if coach_id:
        mil_q = mil_q.filter(models.MileageBalancing.coach_id == coach_id)
    result["mileage_latest"] = [x.__dict__ for x in mil_q.all()]

    # 5) Cleaning slots (just list for that train/coach)
    result["cleaning_slots"] = [x.__dict__ for x in filt(models.CleaningSlot).all()]

    # 6) Stabling geometry (latest per coach by id)
    sub_s = (
        db.query(
            models.StablingGeometry.train_id,
            models.StablingGeometry.coach_id,
            func.max(models.StablingGeometry.stable_id).label("max_id"),
        )
        .filter(models.StablingGeometry.train_id == train_id)
        .group_by(models.StablingGeometry.train_id, models.StablingGeometry.coach_id)
        .subquery()
    )
    stab_q = db.query(models.StablingGeometry).join(
        sub_s,
        and_(
            models.StablingGeometry.train_id == sub_s.c.train_id,
            models.StablingGeometry.coach_id == sub_s.c.coach_id,
            models.StablingGeometry.stable_id == sub_s.c.max_id,
        ),
    )
    if coach_id:
        stab_q = stab_q.filter(models.StablingGeometry.coach_id == coach_id)
    result["stabling_latest"] = [x.__dict__ for x in stab_q.all()]

    # Python object me SQLAlchemy state aata hai; clean kar do:
    def clean(d):
        d.pop("_sa_instance_state", None)
        return d

    for k in ["fitness_certificates", "job_cards_open", "branding_active", "mileage_latest", "cleaning_slots", "stabling_latest"]:
        result[k] = [clean(x) for x in result.get(k, [])]

    return result
