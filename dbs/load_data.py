from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pandas as pd
from src.constants import FOLDER_WITH_DATA
from src.models.base import Base
from src.models.product import Product

import os

def load_data():
    
    for file in os.listdir(FOLDER_WITH_DATA):
        full_path = os.path.join(FOLDER_WITH_DATA, file)
        
        if os.path.isfile(full_path):
            
            store_name_from_file = file.split(".")[0]
            
            engine = create_engine(f'sqlite:///dbs/{store_name_from_file}.db')
            Session = sessionmaker(bind=engine)
            session = Session()
            
            Base.metadata.create_all(engine)
            
            count_product = session.query(Product).count()

            if count_product == 0:
                df = pd.read_csv(full_path)

                products = []

                for index, row in df.iterrows():
                    product = Product(
                        ean=row['ean'],
                        name=row['nombre'],
                        description=row['descripcion'],
                        img=row['imagen'],
                        price=row['precio'],
                        price_with_discount=row['precio_con_descuento'],
                        department=row['departamento'],
                        category=row['categoria'],
                        subcategy=row['subcategoria'],
                    )
                    products.append(product)
                    
                session.bulk_save_objects(products)

                session.commit()