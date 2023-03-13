from ...shared.shared import db
from ...function.update_table import UpdateTable
from ...utils.response import response
from sqlalchemy.exc import *
from ...model.set_sld_ak_mdb import SetupSAMdb
from ...schema.set_sld_ak_mdb import setupsa_shcema
from ...schema.user import user_schema
from ...model.user import User
from ...schema.accou_mdb import accou_schema
from ...model.accou_mdb import AccouMdb


class SetupSldAkhir:
    result = None

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                cp_id = user.company
                sto = request.json["sto"]
                pur = request.json["pur"]
                pur_shipping = request.json["pur_shipping"]
                pur_retur = request.json["pur_retur"]
                pur_discount = request.json["pur_discount"]
                hpp = request.json["hpp"]

                setup = SetupSAMdb(
                    cp_id, sto, pur, pur_shipping, pur_retur, pur_discount, hpp, user.id
                )
                db.session.add(setup)
                db.session.commit()

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

                    self.result = response(200, "Berhasil", True, final)

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                self.result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return self.result
        else:
            try:
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

                    return response(
                        200, "Berhasil", True, final if len(final) > 0 else None
                    )

                return response(200, "Berhasil", True, None)
            except ProgrammingError as e:
                return UpdateTable([SetupSAMdb, AccouMdb], request)
