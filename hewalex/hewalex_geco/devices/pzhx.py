
from .base import BaseDevice

# Based on work by krzysztof1111111111
# https://www.elektroda.pl/rtvforum/topic3499254.html

class PZHX(BaseDevice):

    REG_MAX_ADR = 279
    REG_MAX_NUM = 60
    REG_CONFIG_START = 220

    registers = {

        # Rejestry statusów
        120: { 'type': 'date', 'name': 'date', 'desc': 'Date' },                      
        124: { 'type': 'time', 'name': 'time', 'desc': 'Time' },                                         
        130: { 'type': 'te10', 'name': 'T1', 'desc': 'T1 - temp. CWU [°C]' },                         
        132: { 'type': 'te10', 'name': 'T2', 'desc': 'T2 - temp. bufora CO [°C]' },                        
        134: { 'type': 'te10', 'name': 'T3', 'desc': 'T3 - temp. wody na wlocie do skraplacza [°C]' },                         
        136: { 'type': 'te10', 'name': 'T4', 'desc': 'T4 - temp. czynnika za skraplaczem [°C]' },                                                 
        140: { 'type': 'fl100', 'name': 'U1', 'desc': 'U1 - napięcie zasilania [V]' },                          
        142: { 'type': 'te10', 'name': 'T7', 'desc': 'T7 - temp. powrotu z instalacji CO [°C]' },                         
        144: { 'type': 'te10', 'name': 'U2', 'desc': 'U2 - napięcie zasilania - pomiar dodatkowy [V]' },
        146: { 'type': 'te10', 'name': 'T9', 'desc': 'T9 - temp. powrotu z cyrkulacji [°C]' },
        150: { 'type': 'te10', 'name': 'T11', 'desc': 'T11 - temp. za mieszaczem CO / na wylocie z bufora [°C]' },
        152: { 'type': 'te10', 'name': 'T12', 'desc': 'T12 - temp. pokojowa obiegu CO1 [°C]' },
        154: { 'type': 'te10', 'name': 'T13', 'desc': 'T13 - temp. pokojowa obiegu CO2 [°C]' },
        156: { 'type': 'te10', 'name': 'T14', 'desc': 'T14 - temp. zewnętrzna [°C]' },
        158: { 'type': 'te10', 'name': 'T15', 'desc': 'T15 - czyjnik przepływu' },
        160: { 'type': 'te10', 'name': 'PV', 'desc': 'PV - współpraca z PV' },
        
  
        # Rejestry konfiguracji
        240: { 'type': 'te10', 'name': 'Ta', 'desc': 'Ta - temp. powietrza na wlocie do pomy ciepła [°C]' },
        250: { 'type': 'te10', 'name': 'Tp', 'desc': 'Tp - temp. czynnika w parowniku [°C]' },
        260: { 'type': 'te10', 'name': 'CO2', 'desc': 'Temp. ustawiona CO2 [°C]' },                                                     
    }

