import configparser
import sys
import pyodbc as odbc


DRIVER = 'SQL Server'
SERVER_NAME = 'DESKTOP-0AV09UH'
DATABASE_NAME = 'StoreSalesPrediction'
cursor = ''

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    conn = odbc.connect(conn_string)
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()
else:
    cursor = conn.cursor()



