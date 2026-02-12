import mysql.connector
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import datetime

@dataclass
class orders:
    etfs_id: int
    price: float
    buy_date: datetime
    amount: int

def open_db_connection() -> mysql.connector.connection.MySQLConnection:
    # Lade aus .env
    load_dotenv()
    # Datenbank-Definition
    cnx = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"))
    return cnx

def close_db_connection(cnx : mysql.connector.connection.MySQLConnection):
    cnx.close()

def writeData(etf_id, etfexchange_date, price, yahoo_symbol, entry_date):
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    # Ausführung DB-Abfrage
    mycursor.execute(f"INSERT INTO marketdata (etf_id, exch_date, price, yahoo_symbol, entry_date) VALUES ({etf_id}, '{etfexchange_date}', {price}, '{yahoo_symbol}', '{entry_date}');")
    cnx.commit()  # Änderungen speichern
    # Schließen DB
    close_db_connection(cnx)

def getProfitLoss(etf_id) -> float:
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    profitLoss = 0
    # Ausführung DB-Abfrage
    mycursor.execute(f"SELECT etfs_id, price,buy_date,amount FROM orders WHERE etfs_id = {etf_id};")
    myorders = [orders(*row) for row in mycursor.fetchall()]
    for order in myorders:
        mycursor.execute(f"SELECT price FROM marketdata WHERE etf_id = {order.etfs_id} ORDER BY exch_date DESC LIMIT 1;")
        current_price = mycursor.fetchone()[0]  # Aktueller Preis
        profitLoss = profitLoss + (order.amount * (current_price - order.price))  # Gewinn/Verlust pro Order
    #print(f"Order: ETF_ID={order.etfs_id}, Buy Price={order.price:>6.2f}, Current Price={current_price:>6.2f}, Profit/Loss={profitLoss:>8.2f}")
    # Schließen DB
    close_db_connection(cnx)
    return profitLoss