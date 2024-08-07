from io import StringIO
from pandasai import Agent
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, text as sql_text
from sqlalchemy.orm import sessionmaker
from pandasai.responses.response_parser import ResponseParser
import os
from pandasai import SmartDatalake, SmartDataframe
from pandasai import Agent
from src.constants import FOLDER_WITH_DATA
from src.models.product import Product
from pandasai.responses.response_parser import ResponseParser
from pandasai import SmartDatalake
from pandasai.llm import OpenAI

class PandasDataFrame(ResponseParser):

    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        print(f"result {result}")
        # Returns Pandas Dataframe instead of SmartDataFrame
        return result["value"]


class Chat:
    
    all_df = pd.DataFrame()
    
    def encode_dataframe_columns(self, encoding='unicode-escape'):
        """Encodes all string columns in a DataFrame to the specified encoding.

        Args:
            self: The object instance.
            encoding: The desired encoding (default: 'utf-8').

        Returns:
            A new DataFrame with encoded columns.
        """
        columns = [
            ("id",int),
            ("ean",str),
            ("name",str),
            ("description",str),
            ("img",str),
            ("price", int),
            ("price_with_discount", int),
            ("department", str),
            ("category", str),
            ("subcategy", str)
        ]
        df_encoded = self.all_df.copy()

        for column,dtype in columns:
            if dtype == str:
                df_encoded[column] = df_encoded[column].astype(str).str.encode(encoding).str.decode(encoding).str.encode('utf-8').str.decode('utf-8')
            elif dtype == int:
                df_encoded[column] = df_encoded[column].astype(str).str.replace(r'\D+', '', regex=True).astype(int)
        print(df_encoded)
        
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

    def dataframe_to_dict(self,df):
        """Converts a DataFrame with product, price, and store information into a dictionary.

        Args:
            df: The pandas DataFrame.

        Returns:
            A dictionary where the product name is the key and the value is a dictionary containing price and store.
        """

        data_dict = {}
        for index, row in df.iterrows():
            product_name = row['name']
            price = row['price']
            store = row['store']
            data_dict[product_name] = {'price': price, 'store': store}
        return data_dict
    
    def generate_message(self, msg):
        self.all_df = self.encode_dataframe_columns()
        os.environ["PANDASAI_API_KEY"] = '$2a$10$YilTZTWRAz.sz4LnTetyp.TtpHe2S5dxKlZjk6xxlGrmMUXdxLQxq'
        df = SmartDataframe(self.all_df , config={"response_parser": PandasDataFrame})
        response = df.chat(msg)
        response_to_dict = response.to_dict('records')
        return response_to_dict