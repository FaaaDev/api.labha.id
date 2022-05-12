from main.shared.shared import ma


class SetupSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "cp_id",
            "ar",
            "ap",
            "pnl",
            "pnl_year",
            "rtn_income",
            "sls_rev",
            "sls_disc",
            "sls_retur",
            "sls_shipping",
            "sls_prepaid",
            "sls_unbill",
            "sls_unbill_recv",
            "sls_tax",
            "pur_cogs",
            "pur_discount",
            "pur_shipping",
            "pur_retur",
            "pur_advance",
            "pur_unbill",
            "pur_tax",
            "sto",
            "sto_broken",
            "sto_general",
            "sto_production",
            "sto_hpp_diff",
            "sto_wip",
            "fixed_assets",
        )


setup_shcema = SetupSchema()
setups_schema = SetupSchema(many=True)
