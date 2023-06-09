from ..shared.shared import ma


class CustomerMdb(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "cus_code",
            "cus_name",
            "cus_jpel",
            "cus_sub_area",
            "cus_npwp",
            "cus_pkp",
            "cus_country",
            "cus_address",
            "cus_kota",
            "cus_kpos",
            "cus_telp1",
            "cus_telp2",
            "cus_email",
            "cus_fax",
            "cus_cp",
            "cus_curren",
            "cus_pjk",
            "cus_ket",
            "cus_gl",
            "cus_uang_muka",
            "cus_limit",
            "sub_cus",
            "cus_id",
        )


customer_schema = CustomerMdb()
customers_schema = CustomerMdb(many=True)
