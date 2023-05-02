from main.shared.shared import ma

class AdmMenuSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'sequence_no', 'page_name', 'note', 'visible', 'parent_id', 'route_name', 'icon_file', 'sub_content', 'open_target')


adm_menu_schema = AdmMenuSchema()
adm_menus_schema = AdmMenuSchema(many=True)