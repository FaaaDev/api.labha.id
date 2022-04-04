from main.shared.shared import ma

class AdmUserMenuSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id_adm_user', 'id_adm_menu', 'view', 'edit', 'delete')


adm_user_menu_schema = AdmUserMenuSchema()
adm_user_menus_schema = AdmUserMenuSchema(many=True)