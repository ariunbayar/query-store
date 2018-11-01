from django.db import models


class Query(models.Model):

    query = models.TextField()
    columns_pickle = models.BinaryField(null=True)
    rows_pickle = models.BinaryField(null=True)
    num_columns = models.IntegerField()
    num_rows = models.IntegerField()
    duration_ms = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ref(models.Model):

    table_name = models.CharField(max_length=250)
    table_description = models.CharField(max_length=250)
    table_description2 = models.CharField(max_length=250)

    column_name = models.CharField(max_length=250)
    column_description = models.CharField(max_length=250)
    column_description2 = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class P(models.Model):
    psp_num = models.CharField(max_length=250, null=True)
    abb_nam = models.CharField(max_length=250, null=True)
    all_nam = models.CharField(max_length=250, null=True)
    aln_idn = models.CharField(max_length=250, null=True)
    bir_day = models.CharField(max_length=250, null=True)
    ccl_yon_cde = models.CharField(max_length=250, null=True)
    crw_idn = models.CharField(max_length=250, null=True)
    dbl_reg_rsn = models.CharField(max_length=250, null=True)
    del_cde = models.CharField(max_length=250, null=True)
    edt_day = models.CharField(max_length=250, null=True)
    edt_dtm = models.CharField(max_length=250, null=True)
    edt_ocp_cde = models.CharField(max_length=250, null=True)
    edt_prt_cde = models.CharField(max_length=250, null=True)
    epr_day = models.CharField(max_length=250, null=True)
    etr_uyn_cde = models.CharField(max_length=250, null=True)
    fnm_gnr = models.CharField(max_length=250, null=True)
    fnm_nam = models.CharField(max_length=250, null=True)
    fnm_trb = models.CharField(max_length=250, null=True)
    gen_cde = models.CharField(max_length=250, null=True)
    isc_iss_cpn = models.CharField(max_length=250, null=True)
    isc_ntl_cde = models.CharField(max_length=250, null=True)
    isc_rsd_num = models.CharField(max_length=250, null=True)
    iss_day = models.CharField(max_length=250, null=True)
    ivd_cde = models.CharField(max_length=250, null=True)
    ivd_day = models.CharField(max_length=250, null=True)
    ivd_ocp_cde = models.CharField(max_length=250, null=True)
    ivd_prt_cde = models.CharField(max_length=250, null=True)
    lev_uyn_cde = models.CharField(max_length=250, null=True)
    ntl_cde = models.CharField(max_length=250, null=True)
    psp_clf_cde = models.CharField(max_length=250, null=True)
    psp_knd_cde = models.CharField(max_length=250, null=True)
    psp_typ_cde = models.CharField(max_length=250, null=True)
    psp_use_cut = models.CharField(max_length=250, null=True)
    reg_day = models.CharField(max_length=250, null=True)
    reg_ocp_cde = models.CharField(max_length=250, null=True)
    reg_prt_cde = models.CharField(max_length=250, null=True)
    rsd_num_eng = models.CharField(max_length=250, null=True)
    rsd_num_mga = models.CharField(max_length=250, null=True)
    sgl_yon_cde = models.CharField(max_length=250, null=True)
