from query.models import P

fields = [
    'psp_num',
    'abb_nam',
    'all_nam',
    'aln_idn',
    'bir_day',
    'ccl_yon_cde',
    'crw_idn',
    'dbl_reg_rsn',
    'del_cde',
    'edt_day',
    'edt_dtm',
    'edt_ocp_cde',
    'edt_prt_cde',
    'epr_day',
    'etr_uyn_cde',
    'fnm_gnr',
    'fnm_nam',
    'fnm_trb',
    'gen_cde',
    'isc_iss_cpn',
    'isc_ntl_cde',
    'isc_rsd_num',
    'iss_day',
    'ivd_cde',
    'ivd_day',
    'ivd_ocp_cde',
    'ivd_prt_cde',
    'lev_uyn_cde',
    'ntl_cde',
    'psp_clf_cde',
    'psp_knd_cde',
    'psp_typ_cde',
    'psp_use_cut',
    'reg_day',
    'reg_ocp_cde',
    'reg_prt_cde',
    'rsd_num_eng',
    'rsd_num_mga',
    'sgl_yon_cde',
    ]


distinct_values = {}
for field in fields:
    values = P.objects.all().values_list(field, flat=True).distinct()
    distinct_values[field] = list(values)


import random

with open('insert.sql', 'w') as f:
    tablename = 'people'
    for i in range(1000000):
        query = "INSERT INTO `%s` VALUES " % tablename
        values = [random.choice(distinct_values[f]) for f in fields]
        values[2] = values[15] + ' ' + values[16]
        values[1] = ''.join([v[0] for v in values[2].split(' ')])
        query += "(null,'" + "','".join(values) + "');\n"
        f.write(query)
