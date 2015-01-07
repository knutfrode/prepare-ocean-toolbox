# MyOcean default username and password
username = 'my-userid'
password = 'my-passwd'

# Relevant MyOcean datasets
sources = [

{
        'name': 'arctic',
        'forecast': {
            'productID': 'DATASET-TOPAZ4-ARC-MYOCEANV2-BE',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#ARC-METNO-ARC-TOPAZ4_2_PHYS-FOR-TDS',
            'motuClient': 'http://myocean.met.no/miscas/cgi-bin/fiMisSubsetter',
            'datasets': ['dataset-topaz4-arc-myoceanv2-be']},
        'reanalysis': {
            'productID': 'ARCTIC_REANALYSIS_PHYS_002_003',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#ARC-NERSC-ARC-TOPAZ4_PHYS-RAN-TDS',
            'motuClient': 'http://myocean.met.no/miscas/cgi-bin/fiMisSubsetter',
            'datasets': ['dataset-ran-arc-myoceanv2-be']}},

            {
        'name': 'baltic',
        'forecast': {
            'productID': 'BALTICSEA_ANALYSIS_FORECAST_PHYS_003_006',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#BALTICSEA_ANALYSIS_FORECAST_PHYS_003_006-TDS',
            'motuClient': 'http://myocean.smhi.se/mis-gateway-servlet/Motu',
            'datasets': ['dataset-bal-analysis-forecast-phys']},
        'reanalysis': {
            'productID': 'BALTICSEA_REANALYSIS_PHYS_003_005',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#BALTICSEA_REANALYSIS_PHYS_003_005-TDS',
            'motuClient': 'http://myocean.smhi.se/mis-gateway-servlet/Motu',
            'datasets': ['dataset-reanalysis-hbmV1-bal-smhi']}},

# Black Sea products are presently unavailable
#            {
#        'name': 'blacksea',
#        'forecast': {
#            'productID': '',
#            'serviceID': '',
#            'motuClient': '',
#            'datasets': ['']},
#        'reanalysis': {
#            'productID': '',
#            'serviceID': '',
#            'motuClient': '',
#            'datasets': ['']}},

            {
        'name': 'northwestshelf',
        'forecast': {
            'productID': 'NORTHWESTSHELF_ANALYSIS_FORECAST_PHYS_004_001_b',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#NORTHWESTSHELF_ANALYSIS_FORECAST_PHYS_004_001_b',
            'motuClient': 'http://data.ncof.co.uk/mis-gateway-servlet/Motu',
            'datasets': ['MetO-NWS-PHYS-hi-Agg-all-levels']},
        'reanalysis': {
            'productID': 'NORTHWESTSHELF_REANALYSIS_PHYS_004_010',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#NWS-IMR-NWS-ROMS_GEO6-PHYS-RAN-TDS',
            'motuClient': 'http://myocean.met.no/miscas/cgi-bin/fiMisSubsetter',
            'datasets': ['dataset-nws-roms-geo6-phys-myocean-ts']}},

            {
        'name': 'southwestshelf',
        'forecast': {
            'productID': 'IBI_ANALYSIS_FORECAST_PHYS_005_001_b',
            'serviceID': 'http://purl.org/myocean/ontology/individual/myocean#IBI_ANALYSIS_FORECAST_PHYS_005_001_b-TDS',
            'motuClient': 'http://puertos.cesga.es/mis-gateway-servlet/Motu',
            'datasets': ['dataset-ibi-analysis-forecast-phys-005-001-hourly']},
        'reanalysis': {
            'productID': 'IBI_REANALYSIS_PHYS_005_002',
            'serviceID': 'http://purl.org/myocean/ontology/individual/myocean#IBI_REANALYSIS_PHYS_005_002-TDS',
            'motuClient': 'http://puertos.cesga.es/mis-gateway-servlet/Motu',
            'datasets': ['dataset-ibi-reanalysis-phys-005-002-daily-regulargrid']}},

            {
        'name': 'mediterranean',
        'forecast': {
            'productID': 'MYOV04-MED-INGV-CUR-AN-FC',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#MEDSEA_ANALYSIS_FORECAST_PHYS_006_001_a-TDS',
            'motuClient': 'http://gnoodap.bo.ingv.it/mis-gateway-servlet/Motu',
            'datasets': ['myov04-med-ingv-cur-an-fc']},
        'reanalysis': {
            'productID': 'MEDSEA_REANALYSIS_PHYS_006_004',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#MEDSEA_REANALYSIS_PHYS_006_004-TDS',
            'motuClient': 'http://gnoodap.bo.ingv.it/mis-gateway-servlet/Motu',
            'datasets': ['myov04-med-ingv-cur-rean-dm']}},

            {
        'name': 'global',
        'forecast': {
            'productID': 'GLOBAL-ANALYSIS-FORECAST-PHYS-001-002',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#GLOBAL_ANALYSIS_FORECAST_PHYS_001_002-TDS',
            'motuClient': 'http://atoll.mercator-ocean.fr/mfcglo-mercator-gateway-servlet/Motu',
            'datasets': ['global-analysis-forecast-phys-001-002']},
#        'reanalysis': {
#            'productID': 'GLOBAL_REANALYSIS_PHYS_001_010',
#            'serviceID': 'http://purl.org/myocean/ontology/service/database#GLOBAL_REANALYSIS_PHYS_001_010',
#            'motuClient': 'http://data.ncof.co.uk/mis-gateway-servlet/Motu',
#            'datasets': ['GLOBAL_REANALYSIS_PHYS_001_010_RAN-UK-ORCA025_GRIDS', 'GLOBAL_REANALYSIS_PHYS_001_010_RAN-UK-ORCA025_GRIDT',
#                         'GLOBAL_REANALYSIS_PHYS_001_010_RAN-UK-ORCA025_GRIDU', 'GLOBAL_REANALYSIS_PHYS_001_010_RAN-UK-ORCA025_GRIDV']}}
        'reanalysis': {
            'productID': 'GLOBAL_REANALYSIS_PHYS_001_009',
            'serviceID': 'http://purl.org/myocean/ontology/service/database#GLOBAL-REANALYSIS-PHYS-001-009-TDS',
            'motuClient': 'http://atoll.mercator-ocean.fr/mfcglo-mercator-gateway-servlet/Motu',
            'datasets': ['dataset-global-reanalysis-phys-001-009-ran-fr-glorys2v3-monthly-u-v',
                         'dataset-global-reanalysis-phys-001-009-ran-fr-glorys2v3-monthly-s',
                         'dataset-global-reanalysis-phys-001-009-ran-fr-glorys2v3-monthly-t',
                         'dataset-global-reanalysis-phys-001-009-ran-fr-glorys2v3-monthly-ssh',
                         'dataset-global-reanalysis-phys-001-009-ran-fr-glorys2v3-monthly-ice']}}
            ]
