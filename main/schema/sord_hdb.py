from ..shared.shared import ma


class SordSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "so_code",
            "so_date",
            "pel_id",
            "ppn_type",
            "sub_addr",
            "sub_id",
            "req_date",
            "top",
            "due_date",
            "split_inv",
            "prod_disc",
            "jasa_disc",
            "total_disc",
            "total_bayar",
            "status",
            "print",
        )


sord_schema = SordSchema()
sords_schema = SordSchema(many=True)
