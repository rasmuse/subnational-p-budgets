NUTS_YEAR = 2016
DATA_YEAR = 2016
DEFAULT_NUTS_LEVEL = 2
EXCEPTIONS = {
    "DE": 1, # Most agricultural statistics available only on NUTS1 level
    "EL": 0, # Data quality concerns below NUTS0
    "SI": 0, # Data quality concerns below NUTS0
    'CY': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'EE': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'LU': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'LV': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
    'MT': 0, # Has only one NUTS2 region, so NUTS0 resolution is also NUTS2
}

CROP_PARTITIONS = {
    'UAA': ('ARA', 'J0000', 'PECR', 'K0000'),
    'PECR': ('H0000', 'L0000', 'PECR9'),
    'PECR9_H9000': ('PECR9', 'H9000'),
    'ARA': ('C0000', 'P0000', 'R0000', 'I0000', 'G0000', 'V0000_S0000', 'ARA9', 'Q0000'),
    'C0000': ('C1000', 'C2000'),
    'C1000': ('C1000X1500', 'C1500'),
    'C1000X1500': ('C1100', 'C1200', 'C1300', 'C1400', 'C1600_1700_1900'),
    'C1600_1700_1900': ('C1600', 'C1700', 'C1900'),
    'C2000': ('C2100', 'C2200'),
    'C1100': ('C1110', 'C1120'),
    'C1110': ('C1111', 'C1112'),
    'C1200': ('C1210', 'C1220'),
    'C1300': ('C1310', 'C1320'),
    'C1400': ('C1410', 'C1420'),
    'I0000': ('I1100','I2000','I3000','I4000','I5000','I6000_9000'),
    'I1100': ('I1110-1140', 'I1150', 'I1190'),
    'I1110-1140': ('I1110-1130', 'I1140'),
    'I1110-1130': ('I1110', 'I1120', 'I1130'),
    'P0000': ('P1000', 'P9000'),
    'P1000': ('P1100', 'P1200', 'P1300'),
    'R0000': ('R1000', 'R2000', 'R9000'),
    'G0000_J0000': ('G1000_J0000X3000', 'G0000X1000', 'J2000', 'J3000'),
    'G1000_J0000X3000': ('G1000_J1000', 'J2000'),
    'G1000_J1000': ('G1000', 'J1000'),
    'J3000': ('J3000ES',),
    'G0000X1000': ('G2000', 'G3000', 'G9000'),
    'G0000': ('G1000', 'G2000', 'G3000', 'G9000'),
    'G2000': ('G2100','G2900'),
    'G9000': ('G9100','G9900'),
    'H0000': ('F0000', 'T0000', 'W1000', 'O1000', 'H9000'),
    'W1000': ('W1100', 'W1200', 'W1300', 'W1900'),
    'W1100': ('W1110_1120', 'W1190'),
    'W1110_1120': ('W1110', 'W1120'),
    'O1000': ('O1100', 'O1900'),
    'O1900': ('O1910', 'O1990'),
    'T0000': ('T1000', 'T2000', 'T3000', 'T4000', 'T9000'),
}