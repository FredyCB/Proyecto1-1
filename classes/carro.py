from dataclasses import dataclass
from typing import Optional
from bson import ObjectId

@dataclass
class Carro:
    _id: Optional[ObjectId] = None
    marca: str = ""
    modelo: str = ""
    año: int = 0
    matricula_id: Optional[ObjectId] = None  # Referencia ÚNICA a la matrícula

    def save(self, db):
        carro_data = {
            "marca": self.marca,
            "modelo": self.modelo,
            "año": self.año,
            "matricula_id": self.matricula_id
        }
        
        if self._id is None:
            result = db.carros.insert_one(carro_data)
            self._id = result.inserted_id
        else:
            db.carros.update_one(
                {"_id": self._id},
                {"$set": carro_data}
            )
        
        return str(self._id)
