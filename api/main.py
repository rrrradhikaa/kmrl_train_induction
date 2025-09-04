from fastapi import FastAPI
from kmrl_train_induction.api.deps import add_cors
from kmrl_train_induction.api.routers import (
    fitness_certificates, job_cards, branding_priorities,
    mileage_balancing, cleaning_slots, stabling_geometry, aggregate
)

def create_app():
    app = FastAPI(
        title="KMRL Train Induction – Mock API",
        version="0.1.0",
        description="CRUD for six variables + aggregated variables view",
    )

    add_cors(app)

    # Routers
    app.include_router(fitness_certificates.router)
    app.include_router(job_cards.router)
    app.include_router(branding_priorities.router)
    app.include_router(mileage_balancing.router)
    app.include_router(cleaning_slots.router)
    app.include_router(stabling_geometry.router)
    app.include_router(aggregate.router)

    @app.get("/")
    def root():
        return {"ok": True, "msg": "KMRL Mock API up. See /docs"}

    return app

app = create_app()
