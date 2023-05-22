
from main.function.update_table import UpdateTable
# from main.function.write_activity import WriteActivity
from main.model.accou_mdb import AccouMdb
from main.model.batch_mdb import BatchMdb
from main.model.plan_hdb import PlanHdb
from main.model.pbb_hdb import PbbHdb
from main.model.uph_ddb import UphDdb
from main.model.ovh_ddb import OvhDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.batch_mdb import batch_schema, BatchSchema
from main.schema.pbb_hdb import pbb_schema, PbbSchema
from main.schema.plan_hdb import plan_schema
from main.schema.uph_ddb import uph_schema
from main.schema.ovh_ddb import ovh_schema
from main.schema.accou_mdb import accou_schema


class Pembebanan:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                pbb_code = request.json["pbb_code"]
                pbb_name = request.json["pbb_name"]
                pbb_date = request.json["pbb_date"]
                batch_id = request.json["batch_id"]
                acc_cred = request.json["acc_cred"]
                uph = request.json["uph"]
                ovh = request.json["ovh"]

                p = PbbHdb(pbb_code, pbb_name, pbb_date, batch_id, acc_cred)

                db.session.add(p)
                db.session.commit()

                new_uph = []
                for x in uph:
                    if x["acc_id"]:
                        new_uph.append(
                            UphDdb(
                                p.id,
                                x["acc_id"],
                            )
                        )

                new_ovh = []
                for x in ovh:
                    if x["acc_id"]:
                        new_ovh.append(
                            OvhDdb(
                                p.id,
                                x["acc_id"],
                            )
                        )

                if len(new_uph) > 0:
                    db.session.add_all(new_uph)

                if len(new_ovh) > 0:
                    db.session.add_all(new_ovh)

                db.session.commit()

                result = response(200, "Berhasil", True, pbb_schema.dump(p))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            try:
                pbb = (
                    db.session.query(PbbHdb, BatchMdb, PlanHdb, AccouMdb)
                    .outerjoin(BatchMdb, BatchMdb.id == PbbHdb.batch_id)
                    .outerjoin(PlanHdb, PlanHdb.id == BatchMdb.plan_id)
                    .outerjoin(AccouMdb, AccouMdb.id == PbbHdb.acc_cred)
                    .order_by(PbbHdb.id.desc())
                    .all()
                )

                uph = (
                    db.session.query(UphDdb, AccouMdb)
                    .outerjoin(AccouMdb, AccouMdb.id == UphDdb.acc_id)
                    .all()
                )

                ovh = (
                    db.session.query(OvhDdb, AccouMdb)
                    .outerjoin(AccouMdb, AccouMdb.id == OvhDdb.acc_id)
                    .all()
                )

                final = []
                for x in pbb:
                    uph = []
                    for y in uph:
                        if y[0].pbb_id == x[0].id:
                            y[0].acc_id = accou_schema.dump(y[1])
                            uph.append(uph_schema.dump(y[0]))

                    ovh = []
                    for z in ovh:
                        if z[0].pbb_id == x[0].id:
                            z[0].acc_id = accou_schema.dump(z[1])
                            ovh.append(ovh_schema.dump(z[0]))

                    if x[1]:
                        x[1].plan_id = plan_schema.dump(x[2])

                    final.append(
                        {
                            "id": x[0].id,
                            "pbb_code": x[0].pbb_code,
                            "pbb_name": x[0].pbb_name,
                            "acc_cred": accou_schema.dump(x[3]),
                            "pbb_date": PbbSchema(only=["pbb_date"]).dump(x[0])["pbb_date"],
                            "batch_id": batch_schema.dump(x[1]),
                            "uph": uph,
                            "ovh": ovh,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                return UpdateTable(
                    [PbbHdb, BatchMdb, PlanHdb, AccouMdb, UphDdb, OvhDdb], request
                )
