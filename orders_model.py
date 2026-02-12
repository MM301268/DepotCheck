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

@dataclass
class etfdetails:
    id: int
    name: str
    isin: str
    yahoo_symbol: str

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

def qOrders(etfID) -> list:
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    if etfID == "":
        # Ausführung DB-Abfrage
        mycursor.execute(f"Select etfs_id, price, buy_date, amount FROM orders;")
    else:
        mycursor.execute(f"Select etfs_id, price, buy_date, amount FROM orders WHERE etfs_id = {etfID};")
    # Einlesen in Data-Struktur
    my_orders = [orders(*row) for row in mycursor.fetchall()]
    # Schließen DB
    close_db_connection(cnx)
    # Return Data
    return my_orders

def qETFID_byYahooSymbol(yahooSymbol) -> int:
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    # Initialisierung der Rückgabe-Variable
    etfID = 0
    # Ausführung DB-Abfrage
    mycursor.execute(f"Select id FROM etfs WHERE yahoo_symbol = '{yahooSymbol}';")
    if mycursor.rowcount == 0:
        print(f"Kein ETF mit Yahoo-Symbol '{yahooSymbol}' gefunden.")
        etfID = -1
    elif mycursor.rowcount == 1:
        etfID = mycursor.fetchone()[0]  # Einlesen der ID
    else:
        print(f"Mehrere ETFs mit Yahoo-Symbol '{yahooSymbol}' gefunden. Bitte überprüfen Sie die Datenbank.")
        etfID = -1
    # Schließen DB
    cnx.close()
    # Return Data
    return etfID

def getYahooSymbols() -> list:
     # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    # Ausführung DB-Abfrage
    mycursor.execute(f"SELECT yahoo_symbol FROM `etfs` group by yahoo_symbol;")
    # Einlesen in Data-Struktur
    yahoo_symbols = [row[0] for row in mycursor.fetchall()]
    # Return Data
    return yahoo_symbols
    # Schließen DB
    cnx.close()

def getETFID_byYahooSymbol(yahooSymbol) -> int: 
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    # Initialisierung der Rückgabe-Variable
    etfID = 0
    # Ausführung DB-Abfrage
    mycursor.execute(f"Select id FROM etfs WHERE yahoo_symbol = '{yahooSymbol}';")
    if mycursor.rowcount == 0:
        print(f"Kein ETF mit Yahoo-Symbol '{yahooSymbol}' gefunden.")
        etfID = -1
    elif mycursor.rowcount == 1:
        etfID = mycursor.fetchone()[0]  # Einlesen der ID
    else:
        print(f"Mehrere ETFs mit Yahoo-Symbol '{yahooSymbol}' gefunden. Bitte überprüfen Sie die Datenbank.")
        etfID = -1
    # Schließen DB
    cnx.close()
    # Return Data
    return etfID

def getETF_Details_byID(etfID) -> etfdetails:
    # Open DB Connection
    cnx = open_db_connection()
    # Aufbau Cursor
    mycursor = cnx.cursor(buffered=True)
    # Initialisierung der Rückgabe-Variable
    etfDetails = None
    # Ausführung DB-Abfrage
    mycursor.execute(f"Select id, name, isin, yahoo_symbol FROM etfs WHERE id = {etfID};")
    if mycursor.rowcount == 0:
        print(f"Kein ETF mit ID '{etfID}' gefunden.")
        etfDetails = None
    elif mycursor.rowcount == 1:
        etfDetails = etfdetails(*mycursor.fetchone())  # Einlesen der Details
    else:
        print(f"Mehrere ETFs mit ID '{etfID}' gefunden. Bitte überprüfen Sie die Datenbank.")
        etfDetails = None
    # Schließen DB
    cnx.close()
    # Return Data
    return etfDetails

def dspYahooSymbols(yahoo_symbols):
    print("Verfügbare Yahoo-Symbole:")
    for symbol in yahoo_symbols:
        print(f"- {symbol}")

def dspOrders(orders):
    # Ausgabe der Orders    
    for order in orders:
        print(f"ETFS_ID: {order.etfs_id:>2} |" 
              f" Preis: {order.price:>6.2f} € |"    
              f" Gekauft am: {order.buy_date.strftime('%d.%m.%Y')} |" 
              f" Anzahl: {order.amount:>5.0f}")
    
def getTotInvest(orders) -> float:
    # Berechnung des Gesamtinvestments
    totInvest = 0
    # Iteration über alle Orders und Berechnung des Investments
    for order in orders:
        totInvest += order.price * order.amount 
    # Rückgabe des Gesamtinvestments
    return totInvest

def dspTotInvest(investment):
    # Ausgabe des Gesamtinvestments
    print(f"Total Investiert: {investment:>6.2f} €")


if __name__ == "__main__":

    
    # myYahooSymbols = getYahooSymbols()
    #dspYahooSymbols(myYahooSymbols)

    
    myOrders = qOrders("")
    dspOrders(myOrders)
    dspTotInvest(getTotInvest(myOrders))
 

    """
    myYahooSymbol = "CSCA.MI"
    myETFID = qETFID_byYahooSymbol(myYahooSymbol)
    MyOrders = qOrders(myETFID)
    dspOrders(MyOrders)
    dspTotInvest(getTotInvest(MyOrders))

    myYahooSymbol = "SAUS.MI"
    myETFID = qETFID_byYahooSymbol(myYahooSymbol)
    MyOrders = qOrders(myETFID)
    dspOrders(MyOrders)
    dspTotInvest(getTotInvest(MyOrders))

    myYahooSymbol = "VEUR.AS"
    myETFID = qETFID_byYahooSymbol(myYahooSymbol)
    MyOrders = qOrders(myETFID)
    dspOrders(MyOrders)
    dspTotInvest(getTotInvest(MyOrders))

    myYahooSymbol = "XDN0.DE"
    myETFID = qETFID_byYahooSymbol(myYahooSymbol)
    MyOrders = qOrders(myETFID)
    dspOrders(MyOrders)
    dspTotInvest(getTotInvest(MyOrders))
    """