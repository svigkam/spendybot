import logging

API_TOKEN = "5609404514:AAGLI0_U1L3zugDkg085PtB8DADCh9wzito"
STATS_PERIOD = 31  # day

def logging_config():
    file_log = logging.FileHandler('../Log.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='[%(asctime)s | %(levelname)s]: %(message)s',
                        datefmt='%m.%d.%Y %H:%M:%S',
                        level=logging.INFO)