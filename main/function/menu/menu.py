from sqlalchemy.exc import IntegrityError
from main.model.main_menu import MainMenu
from main.shared.shared import db
from main.utils.response import response
from main.schema.main_menu import main_menu_schema


class Menu:
    def __new__(self, request):
        if request.method == "POST":
            try:
                name = request.json["name"]
                visible = request.json["visible"]
                parent_id = request.json["parent_id"]
                route_name = request.json["route_name"]
                icon_file = request.json["icon_file"]
                category = request.json["category"]

                menu = MainMenu(
                    name, visible, parent_id, route_name, icon_file, category
                )

                db.session.add(menu)
                db.session.commit()

                result = response(200, "Berhasil", True, main_menu_schema.dump(menu))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            result = MainMenu.query.order_by(MainMenu.category.asc(), MainMenu.id.asc()).all()

            data = []

            for x in result:
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
                    if y.parent_id == x.id:
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
                if not x.parent_id:
                    data.append(
                        {
                            "id": x.id,
                            "name": x.name,
                            "route_name": x.route_name,
                            "icon_file": x.icon_file,
                            "visible": x.visible,
                            "parent_id": x.parent_id,
                            "category": x.category,
                            "submenu": sub_menu,
                        }
                    )

            return response(200, "Berhasil", True, data)
