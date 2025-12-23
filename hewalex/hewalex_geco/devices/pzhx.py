
from .base import BaseDevice

# Based on work by krzysztof1111111111
# https://www.elektroda.pl/rtvforum/topic3499254.html

class PZHX(BaseDevice):

    # PZ HX sterowany jest za pomocą kontrolera g922p02
    
    REG_MAX_ADR = 302
    REG_MAX_NUM = 60
    REG_CONFIG_START = 242

    registers = {

        # Rejestry statusów
        120: { 'type': 'te10', 'name': 'R_120', 'desc': '120' },
        122: { 'type': 'te10', 'name': 'R_122', 'desc': '122' },
        124: { 'type': 'te10', 'name': 'R_124', 'desc': '124' },
        126: { 'type': 'te10', 'name': 'R_126', 'desc': '126' },
        128: { 'type': 'te10', 'name': 'R_128', 'desc': '128' },
        130: { 'type': 'te10', 'name': 'R_130', 'desc': '130' },
        132: { 'type': 'te10', 'name': 'R_132', 'desc': '132' },
        134: { 'type': 'te10', 'name': 'R_134', 'desc': '134' },
        136: { 'type': 'te10', 'name': 'R_136', 'desc': '136' },
        138: { 'type': 'te10', 'name': 'I1', 'desc': 'I1 - natężenie prądu [A]' },  
        140: { 'type': 't100', 'name': 'U1', 'desc': 'U1 - napięcie zasilania [V]' },
        142: { 'type': 'te10', 'name': 'R_142', 'desc': '142' },                         
        144: { 'type': 't100', 'name': 'U2', 'desc': 'U2 - napięcie zasilania - pomiar dodatkowy [V]' },
        146: { 'type': 'te10', 'name': 'R_146', 'desc': '146' },
        148: { 'type': 'te10', 'name': 'R_148', 'desc': '148' },
        150: { 'type': 'te10', 'name': 'R_150', 'desc': '150' },
        152: { 'type': 'te10', 'name': 'Q2', 'desc': 'Q - natężenie przepływu [l/min]' },
        154: { 'type': 'te10', 'name': 'R_154', 'desc': '154' },
        156: { 'type': 'te10', 'name': 'R_156', 'desc': '156' },
        158: { 'type': 'te10', 'name': 'R_158', 'desc': '158' },
        160: { 'type': 'te10', 'name': 'R_160', 'desc': '160' },
        162: { 'type': 'te10', 'name': 'R_162', 'desc': '162' },
        164: { 'type': 'te10', 'name': 'R_164', 'desc': '164' },
        166: { 'type': 'te10', 'name': 'R_166', 'desc': '166' },
        168: { 'type': 'te10', 'name': 'R_168', 'desc': '168' },
        170: { 'type': 'te10', 'name': 'R_170', 'desc': '170' },
        172: { 'type': 'te10', 'name': 'R_172', 'desc': '172' },
        174: { 'type': 'te10', 'name': 'R_174', 'desc': '174' },
        176: { 'type': 'te10', 'name': 'R_176', 'desc': '176' },
        178: { 'type': 'te10', 'name': 'R_178', 'desc': '178' },
        180: { 'type': 'te10', 'name': 'R_180', 'desc': '180' },
        182: { 'type': 'te10', 'name': 'R_182', 'desc': '182' },
        184: { 'type': 'te10', 'name': 'PT1', 'desc': 'PT1 - temp. cieczy na wylocie [°C]' },
        186: { 'type': 'te10', 'name': 'PT2', 'desc': 'PT2 - temp. cieczy na wylocie [°C]' },
        188: { 'type': 'te10', 'name': 'R_188', 'desc': '188' },
        190: { 'type': 'te10', 'name': 'R_190', 'desc': '190' },
        192: { 'type': 'te10', 'name': 'R_192', 'desc': '192' },
        194: { 'type': 'te10', 'name': 'R_194', 'desc': '194' },
        196: { 'type': 'te10', 'name': 'R_196', 'desc': '196' },
        198: { 'type': 'te10', 'name': 'R_198', 'desc': '198' },
        200: { 'type': 'te10', 'name': 'R_200', 'desc': '200' },
        202: { 'type': 'te10', 'name': 'R_202', 'desc': '202' },
        204: { 'type': 'te10', 'name': 'R_204', 'desc': '204' },
        206: { 'type': 'te10', 'name': 'R_206', 'desc': '206' },
        208: { 'type': 'te10', 'name': 'R_208', 'desc': '208' },
        210: { 'type': 'te10', 'name': 'R_210', 'desc': '210' },
        212: { 'type': 'te10', 'name': 'R_212', 'desc': '212' },
        214: { 'type': 'te10', 'name': 'R_214', 'desc': '214' },
        216: { 'type': 'te10', 'name': 'R_216', 'desc': '216' },
        218: { 'type': 'te10', 'name': 'R_218', 'desc': '218' },
        220: { 'type': 'te10', 'name': 'R_220', 'desc': '220' },
        222: { 'type': 'te10', 'name': 'R_222', 'desc': '222' },
        224: { 'type': 'te10', 'name': 'R_224', 'desc': '224' },
        226: { 'type': 'te10', 'name': 'Q', 'desc': 'Q - natężenie przepływu [l/min]' },
        228: { 'type': 'te10', 'name': 'R_228', 'desc': '228' },
        230: { 'type': 'te10', 'name': 'R_230', 'desc': '230' },
        232: { 'type': 'te10', 'name': 'R_232', 'desc': '232' },
        234: { 'type': 'te10', 'name': 'R_234', 'desc': '234' },
        236: { 'type': 'te10', 'name': 'R_236', 'desc': '236' },
        238: { 'type': 'te10', 'name': 'R_238', 'desc': '238' },
        240: { 'type': 'te10', 'name': 'R_240', 'desc': '240' },
        242: { 'type': 'te10', 'name': 'R_242', 'desc': '242' },
        244: { 'type': 'te10', 'name': 'R_244', 'desc': '244' },
        246: { 'type': 'te10', 'name': 'R_246', 'desc': '246' },
        248: { 'type': 'te10', 'name': 'R_248', 'desc': '248' },
        250: { 'type': 'te10', 'name': 'R_250', 'desc': '250' },
        252: { 'type': 'te10', 'name': 'R_252', 'desc': '252' },
        254: { 'type': 'te10', 'name': 'R_254', 'desc': '254' },
        256: { 'type': 'te10', 'name': 'R_256', 'desc': '256' },
        258: { 'type': 'te10', 'name': 'R_258', 'desc': '258' },
        260: { 'type': 'te10', 'name': 'Ua', 'desc': 'Ua - napięcie akumulatora [V]' },
        262: { 'type': 'te10', 'name': 'R_262', 'desc': '262' },
        264: { 'type': 'te10', 'name': 'R_264', 'desc': '264' },
        266: { 'type': 'te10', 'name': 'R_266', 'desc': '266' },
        268: { 'type': 'te10', 'name': 'R_268', 'desc': '268' },
        270: { 'type': 'te10', 'name': 'R_270', 'desc': '270' },
        272: { 'type': 'te10', 'name': 'R_272', 'desc': '272' },
        274: { 'type': 'te10', 'name': 'R_274', 'desc': '274' },
        276: { 'type': 'te10', 'name': 'R_276', 'desc': '276' },
        278: { 'type': 'te10', 'name': 'R_278', 'desc': '278' },
        280: { 'type': 'te10', 'name': 'R_280', 'desc': '280' },
        282: { 'type': 'te10', 'name': 'R_282', 'desc': '282' },
        #284: { 'type': 'te10', 'name': 'PT1_2', 'desc': 'PT1 - temp. cieczy na wylocie [°C]' },    #to samo co 184
        #286: { 'type': 'te10', 'name': 'PT2_2', 'desc': 'PT2 - temp. cieczy na wylocie [°C]' },    #to samo co 185
          # Rejestry konfiguracji
        288: { 'type': 'te10', 'name': 'R_288', 'desc': '288' },
        290: { 'type': 'te10', 'name': 'R_290', 'desc': '290' },
        292: { 'type': 'te10', 'name': 'R_292', 'desc': '292' },
        294: { 'type': 'te10', 'name': 'R_294', 'desc': '294' },
        296: { 'type': 'te10', 'name': 'R_296', 'desc': '296' },                            
    }

