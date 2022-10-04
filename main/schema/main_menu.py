from main.shared.shared import ma

class MainMenuSchema(ma.Schema):
    class Meta:
        ordered=True
        fields = ('id', 'name', 'visible', 'parent_id', 'route_name', 'icon_file')


main_menu_schema = MainMenuSchema()
main_menus_schema = MainMenuSchema(many=True)