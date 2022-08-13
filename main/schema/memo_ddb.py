from main.shared.shared import ma


class MddbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "mcode",
            "acc_id",
            "dep_id",
            "currency",
            "dbcr",
            "amnt",
            "amnh",
            "desc",
        )


mddb_schema = MddbSchema()
mddbs_schema = MddbSchema(many=True)
