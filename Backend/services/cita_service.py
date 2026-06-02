from sqlalchemy.orm import Session
from Backend.models import Cita
from Backend.schemas import CitaSchema

HORAS_DISPONIBLES = ["7:00", "9:00", "11:00", "13:00"]

def obtener_horas_ocupadas(db: Session, fecha: str, servicio: str):
    citas = db.query(Cita).filter(
        Cita.fecha == fecha,
        Cita.servicio == servicio
    ).all()
    return [cita.hora for cita in citas]

def obtener_horas_libres(db: Session, fecha: str, servicio: str):
    ocupadas = obtener_horas_ocupadas(db, fecha, servicio)
    return [h for h in HORAS_DISPONIBLES if h not in ocupadas]

def crear_cita(db: Session, cita: CitaSchema):
    libres = obtener_horas_libres(db, cita.fecha, cita.servicio)
    if cita.hora not in libres:
        return None
    nueva = Cita(**cita.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva