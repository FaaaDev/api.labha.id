from sqlalchemy.exc import IntegrityError
from main.model.main_menu import MainMenu
from main.shared.shared import db
from main.utils.response import response
from main.schema.main_menu import main_menu_schema


class MenuId:
    def __new__(self, request, id):
        menu = MainMenu.query.filter(MainMenu.id == id).first()
        if request.method == "PUT":
            menu.name = request.json["name"]
            menu.visible = request.json["visible"]
            menu.parent_id = request.json["parent_id"]
            menu.route_name = request.json["route_name"]
            menu.icon_file = request.json["icon_file"]
            menu.category = request.json["category"]

            db.session.commit()

            return response(200, "Berhasil", True, main_menu_schema.dump(menu))
        elif request.method == "DELETE":
            db.session.delete(menu)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            result = MainMenu.query.all()

            data = []

            sub_menu = []
            for y in result:
                last_menu = []
                for z in result:
                    if z.parent_id == y.id:
                        last_menu.append(
                            {
                                "id": z.id,
                                "name": z.name,
                                "route_name": z.route_name,
                                "icon_file": z.icon_file,
                                "parent_id": z.parent_id,
                                "visible": z.visible,
                                "category": z.category,
                            }
                        )
                if y.parent_id == menu.id:
                    sub_menu.append(
                        {
                            "id": y.id,
                            "name": y.name,
                            "route_name": y.route_name,
                            "icon_file": y.icon_file,
                            "visible": y.visible,
                            "parent_id": y.parent_id,
                            "category": y.category,
                            "lastmenu": last_menu,
                        }
                    )

            data = {
                "id": menu.id,
                "name": menu.name,
                "route_name": menu.route_name,
                "icon_file": menu.icon_file,
                "visible": menu.visible,
                "parent_id": menu.parent_id,
                "category": menu.category,
                "submenu": sub_menu,
            }

            return response(200, "Berhasil", True, data)
