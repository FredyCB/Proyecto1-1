import urllib.parse
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from classes.carro import Carro
from classes.matricula import Matricula
import datetime

# Cargar variables de entorno
load_dotenv()


URI = "mongodb+srv://fcardonabanegas:" + urllib.parse.quote("Creeper@5") +  "@cluster0.cqmsaac.mongodb.net/"

def get_database():
    client = MongoClient(URI)
    return client["vehiculos_db"]

def main():
    db = get_database()
    
    # Crear carros primero
    carro1 = Carro(marca="Toyota", modelo="Corolla", año=2020)
    carro1_id = carro1.save(db)
    
    carro2 = Carro(marca="Honda", modelo="Civic", año=2022)
    carro2_id = carro2.save(db)
    
    carro3 = Carro(marca="Ford", modelo="Mustang", año=2023)
    carro3_id = carro3.save(db)
    
    # Crear matrículas y asignar a carros
    matricula1 = Matricula(
        numero="ABC-123",
        fecha_expedicion=datetime.datetime.now().strftime("%Y-%m-%d"),
        carro_id=ObjectId(carro1_id)
    )
    matricula1_id = matricula1.save(db)
    
    # Actualizar carro con referencia a matrícula
    carro1.matricula_id = ObjectId(matricula1_id)
    carro1.save(db)
    
    # Repetir para otros vehículos
    matricula2 = Matricula(
        numero="XYZ-789",
        fecha_expedicion=datetime.datetime.now().strftime("%Y-%m-%d"),
        carro_id=ObjectId(carro2_id)
    )
    matricula2_id = matricula2.save(db)
    carro2.matricula_id = ObjectId(matricula2_id)
    carro2.save(db)
    
    matricula3 = Matricula(
        numero="MUS-001",
        fecha_expedicion=datetime.datetime.now().strftime("%Y-%m-%d"),
        carro_id=ObjectId(carro3_id)
    )
    matricula3_id = matricula3.save(db)
    carro3.matricula_id = ObjectId(matricula3_id)
    carro3.save(db)
    
    # Resultados
    print("\nSISTEMA DE MATRÍCULAS DE VEHÍCULOS")
    print("==================================")
    print(f"Carro 1: {carro1.marca} {carro1.modelo} - Matrícula: {matricula1.numero}")
    print(f"Carro 2: {carro2.marca} {carro2.modelo} - Matrícula: {matricula2.numero}")
    print(f"Carro 3: {carro3.marca} {carro3.modelo} - Matrícula: {matricula3.numero}")
    print("==================================")

if __name__ == "__main__":
    main()
