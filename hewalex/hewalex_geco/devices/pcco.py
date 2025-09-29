from .base import BaseDevice

# Based on work by krzysztof1111111111
# https://www.elektroda.pl/rtvforum/topic3499254.html


class PCCO(BaseDevice):

    # PCCO is driven by PG-426-P04 (controller) and MG-426-P04 (executive module)
    # Below are the registers for the executive module, so no controller settings
    REG_MAX_ADR = 536
    REG_MAX_NUM = 226
    REG_CONFIG_START = 400

    # Interaction between status register 202 and config register 304:
    #
    # When talking to the executive module directly the heat pump can be (manually)
    # disabled and enabled through config register 304 and the result of this is visible
    # in status register 202. With the controller on this works as expected, the heat
    # pump can be put into a waiting mode where it will not turn on until enabled again
    # through register 304. With the controller off however this doesn't work. Maybe
    # the executive module is hardcoded to not turn the heat pump on when the controller
    # is off? See eavesDrop function in base device to learn how the executive module
    # knows that the controller is off. What makes this especially weird is that register
    # 202 changes its value to 0 when the controller is off even if register 304 says
    # otherwise. It would be great if we could detect the 'controller is off' situation
    # through one of the registers, but I haven't found a way yet.

    registers = {

        # Status registers
        120: { 'type': 'date', 'name': 'date', 'desc': 'Date' },                      
        124: { 'type': 'time', 'name': 'time', 'desc': 'Time' },                                         
        130: { 'type': 'te10', 'name': 'T1', 'desc': 'T1 - temp. CWU [°C]' },                         
        132: { 'type': 'te10', 'name': 'T2', 'desc': 'T2 - temp. bufora CO [°C]' },                        
        134: { 'type': 'te10', 'name': 'T3', 'desc': 'T3 - temp. wody na wlocie do skraplacza [°C]' },                         
        136: { 'type': 'te10', 'name': 'T4', 'desc': 'T4 - temp. czynnika za skraplaczem [°C]' },                         
        138: { 'type': 'te10', 'name': 'T5', 'desc': 'T5 - temp. czynnika za skraplaczem2 [°C]' },                          
        140: { 'type': 'te10', 'name': 'T6', 'desc': 'T6 - temp. wody na wylocie ze skraplacza [°C]' },                          
        142: { 'type': 'te10', 'name': 'T7', 'desc': 'T7 - temp. powrotu z instalacji CO [°C]' },                         
        144: { 'type': 'te10', 'name': 'T8', 'desc': 'T8 - temp. wody na wylocie z pompy ciepła [°C]' },
        146: { 'type': 'te10', 'name': 'T9', 'desc': 'T9 - temp. powrotu cyrkulacji [°C]' },
        148: { 'type': 'te10', 'name': 'T10', 'desc': 'T10 - temp ??? [°C]' },
        150: { 'type': 'te10', 'name': 'T11', 'desc': 'T11 - temp. za mieszaczem CO / na wylocie z bufora [°C]' },
        152: { 'type': 'te10', 'name': 'T12', 'desc': 'T12 - temp. pokojowa obiegu CO1 [°C]' },
        154: { 'type': 'te10', 'name': 'T13', 'desc': 'T13 - temp. pokojowa obiegu CO2 [°C]' },
        156: { 'type': 'te10', 'name': 'T14', 'desc': 'T14 - temp. zewnętrzna [°C]' },
        
     #   194: { 'type': 'bool', 'name': 'IsManual' },
        196: { 'type': 'mask', 'name': [
            'Grzanie CO',                                             
            'Grzanie CWU',
            'Niska temp. dla CO',                                   
            'Niska temp. dla CWU',
            'Pompa ciepła wyłączona',
            '[C01] Ochrona skraplacza przed zamarznięciem w trybie chłodzenia - poziom 1',                     
            '[C01] Ochrona skraplacza przed zamarznięciem w trybie chłodzenia - poziom 2',
            '[C02] Blokada chłodzenia',
            'Za wysoka temperatura na wyjściu',
            'Za niska temperatura na wyjściu',
            'Brak przepływu',
            'Ochrona PC - zbyt niska temperatura wody',                                 
            'Wysoka taryfa',                                            
          ]},
     #   198: { 'type': 'word', 'name': 'EV1', 'desc': 'Expansion valve' },
    #  202: { 'type': 'word', 'name': 'WaitingStatus', 'desc': ' 0 when available for operation, 2 when disabled through register 304' },               #
       
        316: { 'type': 'temp', 'name': 'Zawor_rozprezny', 'desc': 'Stopień otwarcia zaworu rozprężnego' },
        318: { 'type': 'te10', 'name': 'I', 'desc': 'I - natezenie prądu [A]' },
        320: { 'type': 'te10', 'name': 'U', 'desc': 'U - napięcie zasilania [V]' },
        322: { 'type': 'temp', 'name': 'Hz', 'desc': 'Hz - częstotliwość pracy sprężarki [Hz]' },
        326: { 'type': 'te10', 'name': 'LP', 'desc': 'LP - ciśnienie czynnika w parowniku [bar]' },
        350: { 'type': 'te10', 'name': 'Ta', 'desc': 'Ta - temp. powietrza na wlocie do pomy ciepła [°C]' },
        352: { 'type': 'te10', 'name': 'Tp', 'desc': 'Tp - temp. czynnika w parowniku [°C]' },
        354: { 'type': 'te10', 'name': 'Td', 'desc': 'Td - temp. czynnika za sprężarką [°C]' },
        356: { 'type': 'te10', 'name': 'Ts', 'desc': 'Ts - temp. czynnika przed sprężarką [°C]' },
        380: { 'type': 'te10', 'name': 'HP', 'desc': 'Ts - temp. czynnika w skraplaczu [bar]' },
        384: { 'type': 'mask', 'name': [
            'Przełącznik HP',                                             
            'Przełącznik LP',
            'Grzałka tacy kondensatu',                                   
            'Niska temp. dla CWU',
            'Podgrzewanie sprężarki',
            'Grzałka karteru sprężarki',                     
            'Niska praca wentylatora AC',
            'Wysoka praca wentylatora AC',                    
            'Zawór 4-drożny',                                            
          ]},

        # Config registers
   
        408: { 'type': 'te10', 'name': 'cwu', 'desc': 'Temp. ustawiona CWU [°C]' },
        410: { 'type': 'te10', 'name': 'co1', 'desc': 'Temp. ustawiona CO1 [°C]' },
        412: { 'type': 'te10', 'name': 'co2', 'desc': 'Temp. ustawiona CO2 [°C]' }                                                       
    }

    def disable(self, ser):
        return self.writeRegister(ser, 304, 0)

    def enable(self, ser):
        return self.writeRegister(ser, 304, 1)
