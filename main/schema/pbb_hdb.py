from ..shared.shared import ma


class PbbSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "pbb_code", "pbb_name", "pbb_date", "batch_id", "acc_cred")


pbb_schema = PbbSchema()
pbbs_schema = PbbSchema(many=True)
