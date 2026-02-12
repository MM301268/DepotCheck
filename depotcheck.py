import logging
import yfinance as yf
from log_modul import define_logger
from datetime import datetime
from orders_model import getYahooSymbols
from orders_model import getETFID_byYahooSymbol
from orders_model import getETF_Details_byID
from marketdata_model import writeData
from marketdata_model import getProfitLoss  
from typing import Final

class orders:
    etfs_id: int
    price: float
    buy_date: datetime
    amount: int

queryPeriod: Final[str] = "1d"

# Initialisierung
logger: logging.Logger
    
def get_depot_update():
    # Programm Start in Logfile schreiben
    logger.debug(f"--- DEPOT-UPDATE-START: ---")
    # Alle Yahoo-Symbole aus der Datenbank abrufen 
    tickers_Yahoo = getYahooSymbols()
    # Prfit/Loss für jedes Yahoo-Symbol initialisieren
    TotalProfitLoss = 0
    # Für jedes Yahoo-Symbol 
    for symbol in tickers_Yahoo:
        # Aktuellen Kurs von Yahoo Finance abrufen
        ticker = yf.Ticker(symbol)
        # Historische Daten abrufen, um den aktuellen Schlusskurs zu erhalten
        hist = ticker.history(period=queryPeriod)
        # Schlusskurs des letzten Tages als aktuellen Preis verwenden
        curPrice = hist['Close'].iloc[-1]
        # ETF-ID für das Yahoo-Symbol abrufen
        etfID = getETFID_byYahooSymbol(symbol)
        # Sicherheitsprüfung der ETF-ID und Marktdaten in die Datenbank schreiben          
        if etfID != -1:
            writeData(etfID,datetime.now(), curPrice, symbol, datetime.now())
        else:
            logger.warning(f"ETF-ID für Symbol '{symbol}' konnte nicht abgerufen werden.")
        # Profit/Loss für die ETF-ID berechnen und Details abrufen
        profitLoss = getProfitLoss(etfID)
        # Hole Zusatzdetails zum ETF, um sie in der Ausgabe anzuzeigen
        etfDetails = getETF_Details_byID(etfID)
        # Ausgabe des Profit/Loss mit ETF-Details, falls verfügbar
        if etfDetails is not None:
            logger.debug(f"Gewinn/Verslust für ETF-ID: {etfID} Yahoo-Symbol: '{symbol}' Name: {etfDetails.name:<17} Isin: {etfDetails.isin} Betrag: {profitLoss:.2f} €")
            TotalProfitLoss += profitLoss
        else:
            logger.warning(f"ETF-Details für ETF-ID {etfID} konnten nicht abgerufen werden.")
    # Gesamtprofit/-verlust ausgeben
    aktTime = datetime.now().strftime('%d.%m.%Y | %H:%M')
    logger.debug(f"Total Profit/Loss: {TotalProfitLoss:.2f} €")
    logger.debug(f"--- DEPOT-UPDATE-END:  ---")

if __name__ == "__main__":
    logger = define_logger("depotcheck", __name__)
    get_depot_update()
