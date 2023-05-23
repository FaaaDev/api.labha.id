from main.shared.shared import ma


class ProdSupSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "prod_id",
            "sup_id",
        )


prodsup_schema = ProdSupSchema()
prodsups_schema = ProdSupSchema(many=True)
