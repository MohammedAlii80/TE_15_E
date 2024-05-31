# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Mandatory fields
VAT_MANDATORY_FIELDS = [
    '012', '013', '014', '018', '021', '022', '037',
    '046', '051', '056', '065', '076', '102', '103',
    '104', '105', '152', '233', '234', '235', '236',
    '361', '362', '407', '409', '410', '419', '423',
    '436', '462', '463', '464', '765', '766', '767',
    '768',
    # Simplified-only
    '450', '801', '802',
    # Monthly-only
    '093', '097', '457',
    # 033 and 042 are mandatory when 403 is specified (always true for us, with 0% tax)
    '033', '042', '403', '414', '415', '418', '416',
    '417', '453', '452', '451',
]

# Mapping dictionary: monthly fields as keys, list of corresponding annual fields as values
YEARLY_MONTHLY_FIELDS_TO_DELETE = [
    '472', '455', '456', '457', '458', '459', '460', '461', '454'
]

# Computation of new total fields in the annual report
YEARLY_NEW_TOTALS = {
    '080': {'add': ['077', '078', '079', '404']},
    '084': {'add': ['081', '082', '083', '405']},
    '088': {'add': ['085', '086', '087', '406']},
    '179': {'add': ['090', '092', '228']},
    '093': {'add': ['080', '084', '088', '179']},
    '101': {'add': ['098', '099', '100']},
    '102': {'add': ['093', '101'], 'subtract': ['097']},
    '104': {'add': ['102']},
    '105': {'add': ['103'], 'subtract': ['104']},
}

# Fields of the annual simplified declaration
# List drawn from : https://ecdf-developer.b2g.etat.lu/ecdf/formdocs/2020/TVA_DECAS/2020M1V002/TVA_DECAS_LINK_10_DOC_FR_2020M1V002.fieldlist
# PLUS the date fields
YEARLY_SIMPLIFIED_FIELDS = [
    '233', '234', '235', '236',
    '012', '471', '481', '450', '423', '424', '801', '802', '805', '806',
    '807', '808', '819', '820', '817', '818', '051', '056', '711', '712',
    '713', '714', '715', '716', '049', '054', '194', '065', '407', '721',
    '722', '723', '724', '725', '726', '059', '068', '195', '731', '732',
    '733', '734', '735', '736', '063', '073', '196', '409', '410', '436',
    '462', '741', '742', '743', '744', '745', '746', '431', '432', '435',
    '463', '464', '751', '752', '753', '754', '755', '756', '441', '442',
    '445', '765', '766', '761', '762', '767', '768', '763', '764', '076',
    '911', '912', '913', '914', '915', '916', '921', '922', '923', '924',
    '925', '926', '931', '932', '933', '934', '935', '936', '941', '942',
    '943', '944', '945', '946', '951', '952', '953', '954', '955', '956',
    '961', '962', '963', '964', '769', '770',
]

# New total fields in the simplified declaration
YEARLY_SIMPLIFIED_NEW_TOTALS = {
    '450': ['423', '424'],
    '481': ['472', '455', '456'],
    '076': ['802', '056', '407', '410', '768']
}

# Annex A mapping: account code borders (start included, stop excluded) -> category
YEARLY_ANNEX_MAPPING = {
    ('600000', '603130'): 'A43',
    ('603130', '603200'): 'A14',
    ('603200', '603500'): 'A43',
    ('603500', '603600'): 'A30',
    ('603600', '603610'): 'A44',
    ('603610', '603620'): 'A43',
    ('603620', '603700'): 'A44',
    ('603700', '604000'): 'A43',
    ('604000', '606000'): 'A38',
    ('606000', '608111'): 'A43',
    ('608111', '608112'): 'A15',
    ('608112', '608113'): 'A13',
    ('608113', '608120'): 'A14',
    ('608120', '608160'): 'A43',
    ('608160', '608180'): 'A36',
    ('608180', '608200'): 'A41',
    ('608200', '610000'): 'A43',
    ('611000', '611100'): 'A43',
    ('611100', '611120'): 'A43',
    ('611120', '611210'): 'A18b',
    ('611210', '611220'): 'A18a',
    ('611220', '611300'): 'A18c',
    ('611300', '611530'): 'A43',
    ('611530', '611600'): 'A44',
    ('611600', '612200'): 'A43',
    ('612200', '612221'): 'A40',
    ('612221', '612224'): 'A39',
    ('612224', '612230'): 'A43',
    ('612230', '612300'): 'A44',
    ('612300', '613300'): 'A43',
    ('613300', '613400'): 'A27',
    ('613400', '613420'): 'A43',
    ('613420', '613421'): 'A9',
    ('613421', '613430'): 'A43',
    ('613430', '613480'): 'A9',
    ('613480', '614000'): 'A43',
    ('614000', '614120'): 'A20',
    ('614120', '614130'): 'A44',
    ('614130', '614600'): 'A20',
    ('614600', '614800'): 'A29',
    ('614800', '615000'): 'A28',
    ('615000', '615110'): 'A43',
    ('615110', '615120'): 'A37',
    ('615120', '615140'): 'A43',
    ('615140', '615150'): 'A30',
    ('615150', '615160'): 'A33',
    ('615170', '615211'): 'A43',
    ('615211', '615212'): 'A12',
    ('615212', '615220'): 'A7',
    ('615220', '615240'): 'A43',
    ('615240', '615300'): 'A12',
    ('615300', '615310'): 'A17',
    ('615310', '615320'): 'A30',
    ('615320', '616000'): 'A17',
    ('616000', '617000'): 'A35',
    ('617000', '618000'): 'A34b',
    ('618000', '618120'): 'A43',
    ('618120', '618200'): 'A33',
    ('618200', '618700'): 'A43',
    ('618700', '618800'): 'A32',
    ('618800', '618840'): 'A43',
    ('618840', '619000'): 'A44',
    ('619000', '620000'): 'A43',
    ('620000', '621900'): 'A1',
    ('621900', '621910'): 'A2',
    ('621910', '621920'): 'A1',
    ('621920', '622000'): 'A2',
    ('622000', '623000'): 'A3',
    ('623000', '623200'): 'A4',
    ('623200', '623300'): 'A5',
    ('623300', '623810'): 'A4',
    ('623810', '623900'): 'A43',
    ('623900', '624000'): 'A4',
    ('624000', '630000'): 'A43',
    ('646600', '646700'): 'A44',
    ('646800', '646900'): 'A42',
    ('655000', '655210'): 'A25',
    ('655210', '655220'): 'A26',
    ('655220', '655300'): 'A25',
    ('655300', '655400'): 'A26',
    ('655400', '655500'): 'A25',
    ('655500', '655800'): 'A27',
    ('655800', '656000'): 'A25',
    ('658000', '660000'): 'A27',
    ('672000', '672100'): 'A23'
}

# Mapping annex code -> declaration fields
YEARLY_ANNEX_FIELDS = {
    'A1': {'total': '239', '%': '240', 'base_amount': '114'},
    'A1b': {'total': '241', '%': '242', 'base_amount': '243'},
    'A2': {'total': '244', '%': '245', 'base_amount': '246'},
    'A3': {'total': '247', '%': '248', 'base_amount': '249'},
    'A4': {'total': '250', '%': '251', 'base_amount': '252'},
    'A5': {'total': '253', '%': '254', 'base_amount': '255'},
    'A6': {'total': '256', '%': '257', 'base_amount': '258', 'tot_VAT': '259'},
    'A7': {'total': '260', '%': '261', 'base_amount': '262', 'tot_VAT': '263'},
    'A8': {'total': '265', '%': '266', 'base_amount': '267', 'tot_VAT': '268'},
    'A9': {'total': '269', '%': '270', 'base_amount': '271', 'tot_VAT': '272'},
    'A10': {'total': '274', '%': '275', 'base_amount': '276', 'tot_VAT': '277'},
    'A11': {'total': '279', '%': '280', 'base_amount': '281', 'tot_VAT': '282'},
    'A12': {'total': '283', '%': '284', 'base_amount': '183', 'tot_VAT': '184'},
    'A13': {'total': '285', '%': '286', 'base_amount': '287', 'tot_VAT': '288'},
    'A14': {'total': '289', '%': '290', 'base_amount': '291', 'tot_VAT': '292'},
    'A15': {'total': '293', '%': '294', 'base_amount': '295', 'tot_VAT': '296'},
    'A16': {'total': '297', '%': '298', 'base_amount': '299', 'tot_VAT': '300'},
    'A17': {'total': '301', '%': '302', 'base_amount': '303', 'tot_VAT': '304'},
    'A18a': {'total': '305', '%': '306', 'base_amount': '185', 'tot_VAT': '186'},
    'A18b': {'total': '307', '%': '308', 'base_amount': '309'},
    'A18c': {'total': '310', '%': '311', 'base_amount': '312', 'tot_VAT': '313'},
    'A19': {'%': '314', 'base_amount': '315'},
    'A20': {'%': '316', 'base_amount': '317'},
    'A21': {'base_amount': '319', 'tot_VAT': '320'},
    'A22': {'base_amount': '322', 'tot_VAT': '323'},
    'A23': {'base_amount': '324'},
    'A24': {'base_amount': '325'},
    'A25': {'base_amount': '326'},
    'A26': {'base_amount': '327'},
    'A27': {'base_amount': '328', 'tot_VAT': '329'},
    'A28': {'base_amount': '330'},
    'A29': {'base_amount': '331'},
    'A30': {'base_amount': '332', 'tot_VAT': '333'},
    'A31': {'base_amount': '334', 'tot_VAT': '335'},
    'A32': {'base_amount': '336'},
    'A33': {'base_amount': '337', 'tot_VAT': '338'},
    'A34a': {'base_amount': '115', 'tot_VAT': '187'},
    'A34b': {'base_amount': '188', 'tot_VAT': '189'},
    'A35': {'base_amount': '343', 'tot_VAT': '344'},
    'A36': {'base_amount': '345', 'tot_VAT': '346'},
    'A37': {'base_amount': '347', 'tot_VAT': '348'},
    'A38': {'base_amount': '349', 'tot_VAT': '350'},
    'A39': {'base_amount': '351', 'tot_VAT': '352'},
    'A40': {'base_amount': '353', 'tot_VAT': '354'},
    'A41': {'base_amount': '355', 'tot_VAT': '356'},
    'A42': {'base_amount': '358', 'tot_VAT': '359'},
    'A43': {'base_amount': '361', 'tot_VAT': '362'},
    'A44': {'base_amount': '190', 'tot_VAT': '191'}
}
