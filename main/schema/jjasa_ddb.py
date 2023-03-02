from main.shared.shared import ma


class JjasaSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "pj_id",
            "preq_id",
            "sup_id",
            "jasa_id",
            "unit_id",
            "order",
            "price",
            "disc",
            "total_fc",
            "total",
        )


jjasa_schema = JjasaSchema()
jjasas_schema = JjasaSchema(many=True)
