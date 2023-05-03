from main.function.update_dbatch import updateDirectBatch
from main.function.update_table import UpdateTable
from main.function.write_activity import WriteActivity
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.direct_batch_mdb import DirectBatchMdb
from main.model.btcprod_ddb import BtcprodDdb
from main.model.btcmtrl_ddb import BtcmtrlDdb
from main.model.btcrejc_ddb import BtcrejcDdb
from main.model.wages_ddb import WagesDdb
from main.model.msn_mdb import MsnMdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.usage_material_hdb import UsageMatHdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.btcprod_ddb import bprod_schema
from main.schema.btcmtrl_ddb import bmtrl_schema
from main.schema.btcrejc_ddb import breject_schema
from main.schema.wages_ddb import wages_schema
from main.schema.ccost_mdb import ccost_schema, ccosts_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.msn_mdb import msn_schema
from main.schema.fprdc_hdb import fprdc_schema
from main.schema.usage_material_hdb import usage_mat_schema


class DirectBatch:
    # response = response(400, "Gagal", True, None)

    def __new__(self, user, request):
        if request.method == "POST":
            try:
                bcode = request.json["bcode"]
                batch_date = request.json["batch_date"]
                forml_id = request.json["forml_id"]
                mat_id = request.json["mat_id"]
                dep_id = request.json["dep_id"]
                loc_id = request.json["loc_id"]
                msn_id = request.json["msn_id"]
                prdc_rm = request.json["prdc_rm"]
                total = request.json["total"]
                # pb = request.json["pb"]
                product = request.json["product"]
                material = request.json["material"]
                reject = request.json["reject"]
                wages = request.json["wages"]

                batch = DirectBatchMdb(
                    bcode,
                    batch_date,
                    forml_id,
                    mat_id,
                    dep_id,
                    loc_id,
                    msn_id,
                    total,
                    False,
                    False,
                    False,
                    prdc_rm,
                    user.id,
                )

                db.session.add(batch)
                db.session.commit()

                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        new_material.append(
                            BtcmtrlDdb(
                                batch.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["qty"],
                                x["qty_f"],
                                x["price"],
                                x["t_price"],
                            )
                        )

                    if len(new_material) > 0:
                        db.session.add_all(new_material)
                        db.session.commit()

                new_product = []
                for x in product:
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        and x["qty"]
                    ):
                        new_product.append(
                            BtcprodDdb(
                                batch.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["loc_id"],
                                x["qty"],
                                x["qty_f"],
                                x["aloc"],
                            )
                        )
                    
                    if len(new_product) > 0:
                        db.session.add_all(new_product)
                        db.session.commit()



                new_reject = []
                for x in reject:
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        # and x["loc_id"]
                        and x["qty"]
                    ):
                        new_reject.append(
                            BtcrejcDdb(
                                batch.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["loc_id"],
                                x["qty"],
                                x["aloc"],
                            )
                        )
                    
                    if len(new_reject) > 0:
                        db.session.add_all(new_reject)
                        db.session.commit()


                new_wages = []
                for x in wages:
                    if x["acc_id"] and x["nom_wgs"]:
                        new_wages.append(
                            WagesDdb(
                                batch.id,
                                x["acc_id"],
                                x["nom_wgs"],
                                x["desc"],
                            )
                        )


                    if len(new_wages) > 0:
                        db.session.add_all(new_wages)
                        db.session.commit()


                WriteActivity(user, bcode, "TRANSACTION", "ADDED")    
                updateDirectBatch(batch.id, None, user.product, user.company, False)
                db.session.commit()


            except IntegrityError as e:
                print(e)
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, dbatch_schema.dump(batch))
        else:
            try:
                batch = (
                    db.session.query(
                        DirectBatchMdb, CcostMdb, LocationMdb, MsnMdb, FprdcHdb, UsageMatHdb
                    )
                    .outerjoin(CcostMdb, CcostMdb.id == DirectBatchMdb.dep_id)
                    .outerjoin(LocationMdb, LocationMdb.id == DirectBatchMdb.loc_id)
                    .outerjoin(MsnMdb, MsnMdb.id == DirectBatchMdb.msn_id)
                    .outerjoin(FprdcHdb, FprdcHdb.id == DirectBatchMdb.forml_id)
                    .outerjoin(UsageMatHdb, UsageMatHdb.id == DirectBatchMdb.mat_id)
                    .order_by(DirectBatchMdb.id.desc())
                    .all()
                )

                product = (
                    db.session.query(BtcprodDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == BtcprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == BtcprodDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == BtcprodDdb.loc_id)
                    .all()
                )

                material = (
                    db.session.query(BtcmtrlDdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == BtcmtrlDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == BtcmtrlDdb.unit_id)
                    .all()
                )

                reject = (
                    db.session.query(BtcrejcDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == BtcrejcDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == BtcrejcDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == BtcrejcDdb.loc_id)
                    .all()
                )

                wages = db.session.query(WagesDdb).all()

                final = []
                for x in batch:
                    prod = []
                    for y in product:
                        if x[0].id == y[0].btc_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].loc_id = loct_schema.dump(y[3])
                            prod.append(bprod_schema.dump(y[0]))

                    mat = []
                    for y in material:
                        if x[0].id == y[0].btc_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            mat.append(bmtrl_schema.dump(y[0]))

                    rej = []
                    for y in reject:
                        if x[0].id == y[0].btc_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            y[0].loc_id = loct_schema.dump(y[3])
                            rej.append(breject_schema.dump(y[0]))

                    wgs = []
                    for y in wages:
                        if x[0].id == y.btc_id:
                            wgs.append(wages_schema.dump(y))

                    final.append(
                        {
                            "id": x[0].id,
                            "bcode": x[0].bcode,
                            "batch_date": DirectBatchSchema(only=["batch_date"]).dump(
                                x[0]
                            )["batch_date"],
                            "forml_id": fprdc_schema.dump(x[4]) if x[4] else None,
                            "mat_id": usage_mat_schema.dump(x[5]) if x[5] else None,
                            "dep_id": ccost_schema.dump(x[1]),
                            "loc_id": loct_schema.dump(x[2]),
                            "msn_id": x[0].msn_id,
                            "total": x[0].total,
                            "pb": x[0].pb,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "prdc_rm": x[0].prdc_rm,
                            "user_id": x[0].user_id,
                            "product": prod,
                            "material": mat,
                            "reject": rej,
                            "wages": wgs,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                return UpdateTable(
                    [
                        DirectBatchMdb,
                        CcostMdb,
                        LocationMdb,
                        MsnMdb,
                        FprdcHdb,
                        BtcprodDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        BtcmtrlDdb,
                        BtcrejcDdb,
                    ],
                    request,
                )
