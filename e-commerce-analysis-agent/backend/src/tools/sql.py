import pandas as pd
import sqlalchemy
from langchain_community.utilities import SQLDatabase
import contextlib
from tempfile import TemporaryFile
from tabulate import tabulate
import logging
import os
from sqlalchemy import inspect
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from config.app_config import AppConfig
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
load_dotenv() 
app_config = AppConfig()

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'ERROR'))
logger = logging.getLogger(__name__)

class SQL:



    def create_or_load_sqlite_db(self) -> SQLDatabase:

        
        db_path= "db/ecommerce.db"
        sales_csv = "data/sales_data.csv"
        inventory_csv = "data/product_inventory.csv"
        customer_csv = "data/customer_purchase_history.csv"

        # Create SQLAlchemy engine
        engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
        inspector = inspect(engine)

        # Map of table names and their corresponding CSVs
        table_csv_map = {
            "sales_data": sales_csv,
            "product_inventory": inventory_csv,
            "customer_purchase_history": customer_csv
        }

        # Load each table only if it doesn't already exist
        for table_name, csv_path in table_csv_map.items():
            if not inspector.has_table(table_name):
                df = pd.read_csv(csv_path)
                df.to_sql(table_name, con=engine, index=False, if_exists="replace")
                print(f"Loaded table: {table_name}")
            else:
                print(f"Table already exists: {table_name}, skipping load.")

        # Return a LangChain-compatible SQLDatabase object
        return SQLDatabase(engine=engine)


    def get_tool(self):
        #Get DB
        db=self.create_or_load_sqlite_db()

        #Get llm
        WX_ENDPOINT = app_config.WX_ENDPOINT
        IBM_CLOUD_API_KEY = app_config.IBM_CLOUD_API_KEY
        WX_PROJECT_ID = app_config.WX_PROJECT_ID
        MODEL_ID = app_config.MODEL.LLAMA_3_70_B_INSTRUCT
        PARAMETERS = app_config.PARAMETERS
        llm = WatsonxLLM(
                url=os.getenv('WX_ENDPOINT'),
                apikey=os.getenv('IBM_CLOUD_API_KEY'),
                project_id=os.getenv('WX_PROJECT_ID'),
                model_id='meta-llama/llama-3-3-70b-instruct',
                params=os.getenv('PARAMETERS')
            )
        
        #Get tool

        sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        return sql_toolkit



    

