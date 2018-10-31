# https://cx-oracle.readthedocs.io/en/latest/installation.html#quick-start-cx-oracle-installation
# install cx_Oracle $python -m pip install cx_Oracle --upgrade
# configure oracle client on PC https://oracle.github.io/odpi/doc/installation.html#linux

import cx_Oracle
import json
import os

from local_settings import (
        DB_HOST,
        DB_PORT,
        DB_SERVER_NAME,
        DB_USERNAME,
        DB_PASSWORD,
        )

os.environ["NLS_LANG"] = ".AL32UTF8"

dsn_tns = cx_Oracle.makedsn(DB_HOST, DB_PORT, DB_SERVER_NAME)
connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, dsn_tns)

curs = connection.cursor()

columns = {}

def type2str(type):
    if type == cx_Oracle.NUMBER:
        return 'number'
    if type == cx_Oracle.STRING:
        return 'string'
    if type == cx_Oracle.FIXED_CHAR:
        return 'fixed_char'
    if type == cx_Oracle.DATETIME:
        return 'datetime'
    return repr(type)


def get_columns(cursor):
    columns = []
    for field in cursor.description:
        name, type, display_size, internal_size, precision, scale, null_ok = field
        columns.append({
                'name': name,
                'type': type2str(type),
                'display_size': display_size,
                'internal_size': internal_size,
                'precision': precision,
                'scale': scale,
                'null_ok': null_ok,
            })
    return columns
# [('ALN_IDN', <class 'cx_Oracle.NUMBER'>, 127, None, 0, -127, 0),
 # ('NTL_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('FNM_TRB', <class 'cx_Oracle.STRING'>, 50, 50, None, None, 1),
 # ('FNM_GNR', <class 'cx_Oracle.STRING'>, 50, 50, None, None, 1),
 # ('FNM_NAM', <class 'cx_Oracle.STRING'>, 50, 50, None, None, 1),
 # ('BIR_DAY', <class 'cx_Oracle.FIXED_CHAR'>, 8, 8, None, None, 1),
 # ('GEN_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('MGA_NYN_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('DBL_NYN_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('IVD_DAY', <class 'cx_Oracle.FIXED_CHAR'>, 8, 8, None, None, 1),
 # ('IVD_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('REG_DAY', <class 'cx_Oracle.FIXED_CHAR'>, 8, 8, None, None, 1),
 # ('REG_OCP_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 5, 5, None, None, 1),
 # ('REG_PRT_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 4, 4, None, None, 1),
 # ('EDT_DAY', <class 'cx_Oracle.FIXED_CHAR'>, 8, 8, None, None, 1),
 # ('EDT_DTM', <class 'cx_Oracle.DATETIME'>, 23, None, None, None, 1),
 # ('EDT_OCP_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 5, 5, None, None, 1),
 # ('EDT_PRT_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 4, 4, None, None, 1),
 # ('IVD_OCP_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 5, 5, None, None, 1),
 # ('IVD_PRT_CDE', <class 'cx_Oracle.FIXED_CHAR'>, 4, 4, None, None, 1),
 # ('DEL_CDE', <class 'cx_Oracle.STRING'>, 3, 3, None, None, 1),
 # ('RSD_NUM_ENG', <class 'cx_Oracle.STRING'>, 16, 16, None, None, 1),
 # ('RSD_NUM_MGA', <class 'cx_Oracle.STRING'>, 16, 16, None, None, 1)]
#curs.execute('select * from (select * from ISM.T_ALN_M) where ROWNUM <= 20')


# query_get_columns = "SELECT column_name FROM all_tab_columns WHERE table_name='T_PSP_ALN_M'"
query_get_columns = "SELECT * FROM all_tab_columns WHERE table_name='T_PSP_ALN_M'"


query_get_row = """
    select * from (
        select
        ISM.Crypt.decrypt(PSP_NUM) as PSP_NUM,
        ABB_NAM,
        ALL_NAM,
        ALN_IDN,
        BIR_DAY,
        CCL_YON_CDE,
        CRW_IDN,
        DBL_REG_RSN,
        DEL_CDE,
        EDT_DAY,
        EDT_DTM,
        EDT_OCP_CDE,
        EDT_PRT_CDE,
        EPR_DAY,
        ETR_UYN_CDE,
        FNM_GNR,
        FNM_NAM,
        FNM_TRB,
        GEN_CDE,
        ISC_ISS_CPN,
        ISC_NTL_CDE,
        ISC_RSD_NUM,
        ISS_DAY,
        IVD_CDE,
        IVD_DAY,
        IVD_OCP_CDE,
        IVD_PRT_CDE,
        LEV_UYN_CDE,
        NTL_CDE,
        PSP_CLF_CDE,
        PSP_KND_CDE,
        PSP_TYP_CDE,
        PSP_USE_CUT,
        REG_DAY,
        REG_OCP_CDE,
        REG_PRT_CDE,
        RSD_NUM_ENG,
        RSD_NUM_MGA
        SGL_YON_CDE,
        from ISM.T_PSP_ALN_M
	WHERE PSP_NUM = ISM.Crypt.encrypt('U32433042')
    ) where ROWNUM <= 1
    """

('ALN_PSP_IDN',)
('PSP_NUM',)
('PSP_PIC',)


('ABB_NAM',)
('ALL_NAM',)
('ALN_IDN',)
('BIR_DAY',)
('CCL_YON_CDE',)
('CRW_IDN',)
('DBL_REG_RSN',)
('DEL_CDE',)
('EDT_DAY',)
('EDT_DTM',)
('EDT_OCP_CDE',)
('EDT_PRT_CDE',)
('EPR_DAY',)
('ETR_UYN_CDE',)
('FNM_GNR',)
('FNM_NAM',)
('FNM_TRB',)
('GEN_CDE',)
('ISC_ISS_CPN',)
('ISC_NTL_CDE',)
('ISC_RSD_NUM',)
('ISS_DAY',)
('IVD_CDE',)
('IVD_DAY',)
('IVD_OCP_CDE',)
('IVD_PRT_CDE',)
('LEV_UYN_CDE',)
('NTL_CDE',)
('PSP_CLF_CDE',)
('PSP_KND_CDE',)
('PSP_TYP_CDE',)
('PSP_USE_CUT',)
('REG_DAY',)
('REG_OCP_CDE',)
('REG_PRT_CDE',)
('RSD_NUM_ENG',)
('RSD_NUM_MGA',)
('SGL_YON_CDE',)

curs.execute(query_get_columns)

columns = get_columns(curs)
import pprint; pprint.pprint([(v['name'], v['type']) for v in columns])
# import pprint; pprint.pprint(columns)

row = curs.fetchone()
while row:
    import pprint; pprint.pprint(row)
    row = curs.fetchone()

connection.close()
