from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...model.set_sld_ak_mdb import SetupSAMdb
from ...schema.set_sld_ak_mdb import setupsa_shcema
from ...schema.user import user_schema
from ...model.user import User
from ...schema.accou_mdb import accou_schema
from ...model.accou_mdb import AccouMdb

class SetupSaId:
    def __new__(self, id, request, user):
        setup = SetupSAMdb.query.filter(SetupSAMdb.id == id).first()
        if request.method == "PUT":
            setup.sto = request.json["sto"]
            setup.pur = request.json["pur"]
            setup.pur_shipping = request.json["pur_shipping"]
            setup.pur_retur = request.json["pur_retur"]
            setup.pur_discount = request.json["pur_discount"]
            setup.hpp = request.json["hpp"]
            db.session.commit()

            return response(200, "Berhasil", True, setupsa_shcema.dump(setup))
        elif request.method == "DELETE":
            db.session.delete(setup)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            setup = SetupSAMdb.query.filter(SetupSAMdb.cp_id == user.company).all()
            account = AccouMdb.query.all()

            final = []
            if setup:
                for z in setup:
                    setup_dict = dict(
                        (col, getattr(z, col)) for col in z.__table__.columns.keys()
                    )

                    for key, value in setup_dict.items():
                        if key != "id" and key != "cp_id" and key != "user_id":
                            for x in account:
                                if value:
                                    if value == x.id:
                                        setup_dict[key] = accou_schema.dump(x)
                    final.append(setup_dict)

                return response(200, "Berhasil", True, final if len(final) > 0 else None)

            return response(200, "Berhasil", True, None)