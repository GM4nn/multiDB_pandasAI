from pandasai import Agent
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, text as sql_text
from sqlalchemy.orm import sessionmaker
from pandasai.responses.response_parser import ResponseParser
import os
from pandasai import SmartDatalake, SmartDataframe

from src.constants import FOLDER_WITH_DATA
from src.models.product import Product

class Chat:
    
    all_df = pd.DataFrame()
    
    def encode_dataframe_columns(self, encoding='utf-8'):
        """Encodes all string columns in a DataFrame to the specified encoding.

        Args:
            df: The pandas DataFrame to encode.
            encoding: The desired encoding (default: 'utf-8').

        Returns:
            A new DataFrame with encoded columns.
        """
        
        df_encoded = self.all_df.copy()
        columns = [
            ("id",int),
            ("ean",str),
            ("name",str),
            ("description",str),
            ("img",str),
            ("price", str),
            ("price_with_discount", str),
            ("department", str),
            ("category", str),
            ("subcategy", str)
        ]
        for column, d_type in columns:
            df_encoded[column] = df_encoded[column].astype(d_type)
        return df_encoded
    
    def __init__(self) -> None:

        for file in os.listdir(FOLDER_WITH_DATA):
            full_path = os.path.join(FOLDER_WITH_DATA, file)
            
            if os.path.isfile(full_path):
                
                store_name_from_file = file.split(".")[0]
                
                engine = create_engine(f'sqlite:///dbs/{store_name_from_file}.db')
                Session = sessionmaker(bind=engine)
                session = Session()
                
                #query_statement = session.query(Product).filter_by(price = '$00').statement
                
                query_statement = """
                SELECT product.id, product.ean, product.name, product.description, product.img, product.price, product.price_with_discount, product.department, product.category, product.subcategy 
                FROM product
                WHERE product.price != '$00'
                """

                df = pd.read_sql_query(con=engine.connect(), 
                                  sql=sql_text(query_statement),)
                
                df['store'] = store_name_from_file.split("_")[1]
                self.all_df = pd.concat([self.all_df, df], axis=0)
    
    def generate_message(self):
        self.all_df = self.encode_dataframe_columns()
        os.environ["PANDASAI_API_KEY"] = '$2a$10$znpFyrNbjbJ89lmzYEOfju.NBNusdEQ0BT6bQhsqfQrNUuye9CcSK'
        df = SmartDataframe(self.all_df)
        response: pd.DataFrame = df.chat('Give me the cheapest product but the price it is not zero')
        response_to_dict = response.to_dict('records')
        
        return response_to_dict