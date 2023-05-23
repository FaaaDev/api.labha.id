from ...model.group_prod_mdb import GroupProMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.group_prod_mdb import groupPro_schema
from ...schema.divisi_mdb import division_schema
from ...model.divisi_mdb import DivisionMdb


class GroupProductId:
    def __new__(self, id, request):
        groupPro = GroupProMdb.query.filter(GroupProMdb.id == id).first()
        if request.method == "PUT":
            groupPro.code = request.json["code"]
            groupPro.name = request.json["name"]
            groupPro.div_code = request.json["div_code"]
            groupPro.stok = request.json["stok"]
            groupPro.wip = request.json["wip"]
            groupPro.acc_sto = request.json["acc_sto"]
            groupPro.acc_send = request.json["acc_send"]
            groupPro.acc_terima = request.json["acc_terima"]
            groupPro.hrg_pokok = request.json["hrg_pokok"]
            groupPro.acc_penj = request.json["acc_penj"]
            groupPro.acc_wip = request.json["acc_wip"]
            groupPro.potongan = request.json["potongan"]
            groupPro.pengembalian = request.json["pengembalian"]
            groupPro.selisih = request.json["selisih"]
            groupPro.biaya = request.json["biaya"]
            db.session.commit()

            self.response = response(200, "Berhasil", True, groupPro_schema.dump(groupPro))
        elif request.method == "DELETE":
            db.session.delete(groupPro)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            result = (
                db.session.query(GroupProMdb, DivisionMdb)
                .join(DivisionMdb, DivisionMdb.id == GroupProMdb.div_code)
                .order_by(GroupProMdb.div_code.asc())
                .filter(GroupProMdb.id == id)
                .first()
            )

            data = {
                "groupPro": groupPro_schema.dump(result[0]),
                "divisi": division_schema.dump(result[1]),
            }

            self.response = response(200, "Berhasil", True, data)

        return self.response
