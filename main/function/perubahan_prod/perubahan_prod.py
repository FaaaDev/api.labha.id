from main.function.update_pproduct import UpdatePerubahanProd
from main.function.write_activity import WriteActivity
from main.function.update_table import UpdateTable
from main.model.lokasi_mdb import LocationMdb
from main.model.pproduct_hdb import PproductHdb
from main.model.prod_asal_ddb import PAsalDdb
from main.model.prod_jadi_ddb import PJadiDdb
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.pproduct_hdb import pproduct_schema, PproductSchema
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.prod_asal_ddb import prod_asal_schema
from main.schema.prod_jadi_ddb import prod_jadi_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class PerubahanProduct:
    # response = response(400, "Gagal", True, None)

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                pp_code = request.json["pp_code"]
                pp_date = request.json["pp_date"]
                pasal = request.json["pasal"]
                pjadi = request.json["pjadi"]

                pp = PproductHdb(pp_code, pp_date, user.id)

                db.session.add(pp)
                db.session.commit()

                new_pasal = []
                for x in pasal:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        new_pasal.append(
                            PAsalDdb(
                                pp.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["loc_id"],
                                x["qty"],
                            )
                        )

                new_pjadi = []
                for x in pjadi:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        new_pjadi.append(
                            PJadiDdb(
                                pp.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["loc_id"],
                                x["qty"],
                            )
                        )

                if len(new_pasal) > 0:
                    db.session.add_all(new_pasal)

                if len(new_pjadi) > 0:
                    db.session.add_all(new_pjadi)

                UpdatePerubahanProd(pp.id, False, user.product, user.company)

                WriteActivity(user, pp_code, "TRANSACTION", "ADDED")
                db.session.commit()


            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, pproduct_schema.dump(pp))

        else:
            try:
                pp = db.session.query(PproductHdb).order_by(PproductHdb.id.desc()).all()

                pasal = (
                    db.session.query(PAsalDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == PAsalDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == PAsalDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == PAsalDdb.loc_id)
                    .all()
                )

                pjadi = (
                    db.session.query(PJadiDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == PJadiDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == PJadiDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == PJadiDdb.loc_id)
                    .all()
                )

                final = []
                for x in pp:
                    prodA = []
                    for y in pasal:
                        if x.id == y[0].pp_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].loc_id = loct_schema.dump(y[3])
                            prodA.append(prod_asal_schema.dump(y[0]))

                    prodJ = []
                    for y in pjadi:
                        if x.id == y[0].pp_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].loc_id = loct_schema.dump(y[3])
                            prodJ.append(prod_jadi_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x.id,
                            "pp_code": x.pp_code,
                            "pp_date": PproductSchema(only=["pp_date"]).dump(x)[
                                "pp_date"
                            ],
                            "post": x.post,
                            "closing": x.closing,
                            "user_id": x.user_id,
                            "pasal": prodA,
                            "pjadi": prodJ,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [PproductHdb, PAsalDdb, ProdMdb, UnitMdb, LocationMdb, PJadiDdb],
                    request,
                )
