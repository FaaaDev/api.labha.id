from main.shared.shared import ma


class PlanSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", 'pcode', 'pname', 'form_id', 'desc', 'date_planing', 'total', 'unit')


plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)
