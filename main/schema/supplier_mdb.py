from main.shared.shared import ma


class SupplierMdb(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "sup_code",
            "sup_name",
            "sup_jpem",
            "sup_ppn",
            "sup_npwp",
            "sup_pkp",
            "sup_country",
            "sup_address",
            "sup_kota",
            "sup_kpos",
            "sup_telp1",
            "sup_telp2",
            "sup_fax",
            "sup_cp",
            "sup_curren",
            "sup_ket",
            "sup_hutang",
            "sup_uang_muka",
            "sup_limit",
        )


supplier_schema = SupplierMdb()
suppliers_schema = SupplierMdb(many=True)
