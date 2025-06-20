import unittest
import urllib.parse
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from classes.carro import Carro
from classes.matricula import Matricula
import datetime

load_dotenv()

class TestModelo1a1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.uri = f"mongodb+srv://fcardonabanegas:" + urllib.parse.quote("Creeper@5") +  "@cluster0.cqmsaac.mongodb.net/"
        cls.client = MongoClient(cls.uri)
        cls.db = cls.client["vehiculos_test_db"]
    
    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database("vehiculos_test_db")
        cls.client.close()
    
    def test_relacion_matricula_carro(self):
        # Crear carro
        carro = Carro(marca="Tesla", modelo="Model 3", año=2023)
        carro_id = carro.save(self.db)
        
        # Crear matrícula asignada a este carro
        matricula = Matricula(
            numero="TES-001",
            fecha_expedicion=datetime.datetime.now().strftime("%Y-%m-%d"),
            carro_id=ObjectId(carro_id)
        )
        matricula_id = matricula.save(self.db)
        
        # Actualizar carro con referencia a matrícula
        carro.matricula_id = ObjectId(matricula_id)
        carro.save(self.db)
        
        # Verificar relaciones
        carro_recuperado = self.db.carros.find_one({"_id": ObjectId(carro_id)})
        matricula_recuperada = self.db.matriculas.find_one({"_id": ObjectId(matricula_id)})
        
        # Comprobaciones 1:1
        self.assertEqual(str(matricula_recuperada["carro_id"]), carro_id)
        self.assertEqual(str(carro_recuperado["matricula_id"]), matricula_id)
        
        # Verificar unicidad
        misma_matricula = self.db.matriculas.find_one({"carro_id": ObjectId(carro_id)})
        self.assertEqual(str(misma_matricula["_id"]), matricula_id)
        
        mismo_carro = self.db.carros.find_one({"matricula_id": ObjectId(matricula_id)})
        self.assertEqual(str(mismo_carro["_id"]), carro_id)

if __name__ == "__main__":
    unittest.main()