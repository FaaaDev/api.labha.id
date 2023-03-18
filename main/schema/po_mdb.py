from main.shared.shared import ma


class PoSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "po_code",
            "po_date",
            "preq_id",
            "sup_id",
            "ref_sup",
            "top",
            "due_date",
            "split_inv",
            "prod_disc",
            "jasa_disc",
            "total_disc",
            "total_bayar",
            "ns",
            "same_sup",
            "status",
            "apprv",
            "print",
        )


po_schema = PoSchema()
pos_schema = PoSchema(many=True)
