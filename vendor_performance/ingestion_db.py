import pandas as pd
import os
import time
from sqlalchemy import create_engine
import logging
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')
def ingest_db(df,table_name,engine):
    df.to_sql(table_name,con=engine,if_exists='replace',index=False)
    
def load_raw_data():
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
             df=pd.read_csv('data/'+file)
        logging.info(f'ingesting {file} in db')
        ingest_db(df,file[:-4],engine)  
    end=time.time()
    total_time = (end-start)/60
    logging.info('ingestion compelete')
    logging.info(f'total time taken: {total_time}minutes')

    
if __name__ =="__main__":
    load_raw_data()
