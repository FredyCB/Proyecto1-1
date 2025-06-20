from dataclasses import dataclass
from typing import Optional
from bson import ObjectId

@dataclass
class Matricula:
    _id: Optional[ObjectId] = None
    numero: str = ""
    fecha_expedicion: str = ""
    vigente: bool = True
    carro_id: Optional[ObjectId] = None  # Referencia ÚNICA al carro

    def save(self, db):
        matricula_data = {
            "numero": self.numero,
            "fecha_expedicion": self.fecha_expedicion,
            "vigente": self.vigente,
            "carro_id": self.carro_id
        }
        
        if self._id is None:
            result = db.matriculas.insert_one(matricula_data)
            self._id = result.inserted_id
        else:
            db.matriculas.update_one(
                {"_id": self._id},
                {"$set": matricula_data}
            )
        
        return str(self._id)