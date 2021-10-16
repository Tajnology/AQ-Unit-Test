#### EXTERNAL MODULE IMPORTS ####
import time # time.sleep()
import os # os.fsync()
try:
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
bme280 = BME280()
from enviroplus import gas
from enviroplus.noise import Noise
import sys
import sounddevice as sd

#### LOCAL IMPORTS ####
import ipc

#### GLOBAL CONSTANTS ####
LCD_PORT = 10000
TRANSMISSION_PORT = 10001
SOUND_DEVICE = 0
SAMPLE_INTERVAL = 1 # seconds
TRANSMIT_AQ_DATA_EVENT = 'air-data'
TRANSMIT_AQ_STATUS_EVENT = 'air-status'
LOG_GAS_DATA = False
LOG_FILE_SUFFIX = '2'
LOG_TEMP_DATA = True
LOG_TEMP_SUFFIX = '1'



def main(argv):
    # Establish IPC
    ipc.init()

    heating = True
    heating_start = time.time()
    ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': heating})

    log_gas_file = None
    log_temp_file = None
    start_time = None

    

    if(LOG_GAS_DATA):
        log_gas_file = open('log_gas'+LOG_FILE_SUFFIX+'.txt','w')
        log_gas_file.write('time,oxidising,reducing,ammonia\n')
        log_gas_file.flush()
        os.fsync(log_gas_file.fileno())

        start_time = time.time()

    if(LOG_TEMP_DATA):
        log_temp_file = open('log_temp' + LOG_TEMP_SUFFIX + '.txt','w')
        log_temp_file.write('time,enviro,cpu\n')
        log_temp_file.flush()
        os.fsync(log_temp_file.fileno())

        start_time = time.time()

    while(True):
         
        gas_data = gas.read_all()
        temp = bme280.get_temperature()
        with open(r"/sys/class/thermal/thermal_zone0/temp") as File:
            cpu_temp = int(File.readline())/1000

        """ data = {'temperature':temp,'pressure':bme280.get_pressure(), # May need to add 
        'humidity':bme280.get_humidity(),'light':ltr559.get_lux(),
        'ox_gas':gas_data.oxidising/1000,'red_gas':gas_data.reducing/1000,
        'amm_gas':gas_data.nh3/1000,'noise_low':amp_low,
        'noise_mid':amp_mid,'noise_high':amp_high} """
        data = {'temperature':temp,'cpu':cpu_temp,'pressure':bme280.get_pressure(), # May need to add 
        'humidity':bme280.get_humidity(),'light':ltr559.get_lux(),
        'ox_gas':gas_data.oxidising/1000,'red_gas':gas_data.reducing/1000,
        'amm_gas':gas_data.nh3/1000}
        # GCS needs  
        if(LOG_GAS_DATA):
            log_gas_file.write(str(time.time()-start_time) + ',' + str(gas_data.oxidising) + ',' + str(gas_data.reducing) + ',' + str(gas_data.nh3) + '\n')
            log_gas_file.flush()
            os.fsync(log_gas_file.fileno())

        if(LOG_TEMP_DATA):
            log_temp_file.write(str(time.time()-start_time) + ',' + str(temp) + ',' + str(cpu_temp) + '\n')
            log_temp_file.flush()
            os.fsync(log_temp_file.fileno())

        if time.time() - heating_start > 90:
            heating=False

        ipc.msg_transmission(TRANSMIT_AQ_DATA_EVENT,data)
        ipc.msg_transmission(TRANSMIT_AQ_STATUS_EVENT,{'heating': heating})
        ipc.msg_lcd(TRANSMIT_AQ_DATA_EVENT,{'temperature':temp,'cpu':cpu_temp})

        time.sleep(SAMPLE_INTERVAL)

#### ENTRY POINT ####
if __name__ == "__main__":
    main(sys.argv[1:])
