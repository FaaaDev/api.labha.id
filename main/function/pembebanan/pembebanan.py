from main.function.update_pembebanan import updatePembebanan
from main.function.update_table import UpdateTable
from main.function.write_activity import WriteActivity
from main.model.direct_batch_mdb import DirectBatchMdb
from main.model.pbb_hdb import PbbHdb
from main.model.upah_ddb import UpahDdb
from main.model.overhead_ddb import OverhDdb
from main.model.pbprod_ddb import PbprodDdb
from main.model.pbpanen_ddb import PbpanenDdb
from main.model.proj_mdb import ProjMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.pbb_hdb import pbb_schema, PbbSchema
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.upah_ddb import upah_schema
from main.schema.overhead_ddb import overh_schema
from main.schema.pbprod_ddb import pbprod_schema
from main.schema.pbpanen_ddb import pbpanen_schema
from main.schema.proj_mdb import proj_schema


class Pembebanan:
    # response = response(400, "Gagal", True, None)

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                pbb_code = request.json["pbb_code"]
                pbb_date = request.json["pbb_date"]
                pbb_name = request.json["pbb_name"]
                type_pb = request.json["type_pb"]
                prod_id = request.json["prod_id"]
                batch_id = request.json["batch_id"]
                acc_cred = request.json["acc_cred"]
                period = request.json["period"]
                panen_prod = request.json["panen_prod"]
                panen_loc = request.json["panen_loc"]
                proj_id = request.json["proj_id"]
                desc = request.json["desc"]
                upah = request.json["upah"]
                overhead = request.json["overhead"]
                product = request.json["product"]
                panen = request.json["panen"]

                pbb = PbbHdb(
                    pbb_code,
                    pbb_name,
                    pbb_date,
                    type_pb,
                    ",".join([str(x) for x in prod_id]) if prod_id else None,
                    batch_id,
                    acc_cred,
                    period,
                    panen_prod,
                    panen_loc,
                    proj_id,
                    desc,
                    user.id,
                )

                db.session.add(pbb)
                db.session.commit()

                btc = DirectBatchMdb.query.filter(DirectBatchMdb.id == batch_id).first()

                new_upah = []
                for x in upah:
                    if x["acc_id"] and x["nom_uph"]:
                        new_upah.append(
                            UpahDdb(
                                pbb.id,
                                x["acc_id"],
                                x["nom_uph"],
                                x["desc"],
                            )
                        )


                    if len(new_upah) > 0:
                        db.session.add_all(new_upah)

                new_overhead = []
                for x in overhead:
                    if x["acc_id"] and x["nom_ovr"]:
                        new_overhead.append(
                            OverhDdb(
                                pbb.id,
                                x["acc_id"],
                                x["nom_ovr"],
                                x["desc"],
                            )
                        )


                    if len(new_overhead) > 0:
                        db.session.add_all(new_overhead)

                new_product = []
                if pbb.type_pb != 3:
                    for x in product:
                        if x["qty"]:
                            new_product.append(
                                PbprodDdb(
                                    pbb.id,
                                    x["trn_id"],
                                    x["prd_id"],
                                    x["qty"],
                                    x["aloc_qty"],
                                    x["aloc"],
                                )
                            )


                        if len(new_product) > 0:
                            db.session.add_all(new_product)

                else:
                    new_panen = []
                    for x in panen:
                        if x["qty"]:
                            new_panen.append(
                                PbpanenDdb(
                                    pbb.id,
                                    x["trn_id"],
                                    x["prd_id"],
                                    x["qty"],
                                    x["aloc"],
                                )
                            )

                        if len(new_panen) > 0:
                            db.session.add_all(new_panen)



                # btc.pb = True
                # db.session.commit()

                updatePembebanan(pbb.id, user.product, user.company, False)

                WriteActivity(user, pbb_code, "TRANSACTION", "ADDED")

                db.session.commit()
            except IntegrityError as e:
                print(e)
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, pbb_schema.dump(pbb))
        else:
            try:
                pbb = (
                    db.session.query(PbbHdb, DirectBatchMdb, ProjMdb)
                    .outerjoin(DirectBatchMdb, DirectBatchMdb.id == PbbHdb.batch_id)
                    .outerjoin(ProjMdb, ProjMdb.id == PbbHdb.proj_id)
                    .order_by(PbbHdb.id.desc())
                    .all()
                )

                upah = db.session.query(UpahDdb).all()

                overhead = db.session.query(OverhDdb).all()

                product = db.session.query(PbprodDdb).all()

                panen = db.session.query(PbpanenDdb).all()

                final = []
                for x in pbb:
                    uph = []
                    for y in upah:
                        if x[0].id == y.pbb_id:
                            uph.append(upah_schema.dump(y))

                    ovr = []
                    for y in overhead:
                        if x[0].id == y.pbb_id:
                            ovr.append(overh_schema.dump(y))

                    prd = []
                    for y in product:
                        if x[0].id == y.pbb_id:
                            prd.append(pbprod_schema.dump(y))

                    pnn = []
                    for y in panen:
                        if x[0].id == y.pbb_id:
                            pnn.append(pbpanen_schema.dump(y))

                    final.append(
                        {
                            "id": x[0].id,
                            "pbb_code": x[0].pbb_code,
                            "pbb_name": x[0].pbb_name,
                            "pbb_date": PbbSchema(only=["pbb_date"]).dump(x[0])[
                                "pbb_date"
                            ],
                            "type_pb": x[0].type_pb,
                            "prod_id": [int(y) for y in x[0].prod_id.split(",")]
                            if x[0].prod_id
                            else None,
                            "batch_id": dbatch_schema.dump(x[1]) if x[1] else None,
                            "acc_cred": x[0].acc_cred,
                            "period": PbbSchema(only=["period"]).dump(x[0])["period"],
                            "panen_prod": x[0].panen_prod,
                            "panen_loc": x[0].panen_loc,
                            "proj_id": proj_schema.dump(x[2]) if x[2] else None,
                            "desc": x[0].desc,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "user_id": x[0].user_id,
                            "upah": uph,
                            "overhead": ovr,
                            "product": prd,
                            "panen": pnn,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                print(e)
                return UpdateTable(
                    [PbbHdb, DirectBatchMdb, UpahDdb, OverhDdb, PbprodDdb, PbpanenDdb],
                    request,
                )
