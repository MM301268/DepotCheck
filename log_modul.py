import logging
from datetime import datetime

def build_logger_string() -> str:
    # build a date string for the log filename
    date_str = datetime.now().strftime('%Y-%m-%d')

    basicConfig = {
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }
    return date_str, basicConfig

def define_logger(FileName: str, ModuleName: str)-> logging.Logger:
    date_str, basicConfig = build_logger_string()
    # use a RotatingFileHandler so the file is date-based, appended to,
    # and rotated when it exceeds ~5MB
    from logging.handlers import RotatingFileHandler
    log_filename = f'{date_str}_{FileName}.log'
    handler = RotatingFileHandler(
        log_filename,
        mode='a',
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter(basicConfig['format'], datefmt=basicConfig['datefmt'])
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.WARNING)
    root.addHandler(handler)
    # Deinen spezifischen Logger für dein Skript holen
    logger = logging.getLogger(ModuleName)
    # NUR für den eigenen Logger das Level auf DEBUG setzen
    logger.setLevel(logging.DEBUG)
    # Sicherstellen, dass dein Logger nicht doppelt loggt
    logger.propagate = True
    return logger

