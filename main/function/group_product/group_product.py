from main.function.update_table import UpdateTable
from main.model.group_prod_mdb import GroupProMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.group_prod_mdb import groupPro_schema
from main.schema.divisi_mdb import division_schema
from main.model.divisi_mdb import DivisionMdb


class GroupProduct:
    def __new__(self, user, request):
        if request.method == "POST":
            code = request.json["code"]
            name = request.json["name"]
            div_code = request.json["div_code"]
            stok = request.json["stok"]
            wip = request.json["wip"]
            acc_sto = request.json["acc_sto"]
            acc_send = request.json["acc_send"]
            acc_terima = request.json["acc_terima"]
            hrg_pokok = request.json["hrg_pokok"]
            acc_penj = request.json["acc_penj"]
            acc_wip = request.json["acc_wip"]
            potongan = request.json["potongan"]
            pengembalian = request.json["pengembalian"]
            selisih = request.json["selisih"]
            biaya = request.json["biaya"]
            try:
                groupPro = GroupProMdb(
                    code,
                    name,
                    div_code,
                    stok,
                    wip,
                    acc_sto,
                    acc_send,
                    acc_terima,
                    hrg_pokok,
                    acc_penj,
                    acc_wip,
                    potongan,
                    pengembalian,
                    selisih,
                    biaya,
                )
                db.session.add(groupPro)
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(
                    400, "Kode akun " + code + " sudah digunakan", False, None
                )
            finally:
                return response(200, "Berhasil", True, groupPro_schema.dump(groupPro))
        else:
            try:
                result = (
                    db.session.query(GroupProMdb, DivisionMdb)
                    .outerjoin(DivisionMdb, DivisionMdb.id == GroupProMdb.div_code)
                    .order_by(GroupProMdb.id.asc())
                    .all()
                )
                data = [
                    {
                        "groupPro": groupPro_schema.dump(x[0]),
                        "divisi": division_schema.dump(x[1]),
                    }
                    for x in result
                ]

                return response(200, "Berhasil", True, data)
            except ProgrammingError as e:
                print("=============")
                print(e)
                return UpdateTable([GroupProMdb, DivisionMdb], request)
