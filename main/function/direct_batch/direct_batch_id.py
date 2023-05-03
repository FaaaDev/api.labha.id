from main.function.update_dbatch import updateDirectBatch
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
from main.model.fprdc_hdb import FprdcHdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.btcprod_ddb import bprod_schema
from main.schema.btcmtrl_ddb import bmtrl_schema
from main.schema.btcrejc_ddb import breject_schema
from main.schema.wages_ddb import wages_schema
from main.schema.ccost_mdb import ccost_schema, ccosts_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.fprdc_hdb import fprdc_schema


class DirectBatchId:
    def __new__(self, user, id, user_product, user_company, request):
        batch = DirectBatchMdb.query.filter(DirectBatchMdb.id == id).first()
        if request.method == "PUT":
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
                product = request.json["product"]
                material = request.json["material"]
                reject = request.json["reject"]
                wages = request.json["wages"]

                batch.bcode = bcode
                batch.batch_date = batch_date
                batch.forml_id = forml_id
                batch.mat_id = mat_id
                batch.dep_id = dep_id
                batch.loc_id = loc_id
                batch.msn_id = msn_id
                batch.prdc_rm = prdc_rm
                batch.total = total

                prod = BtcprodDdb.query.filter(BtcprodDdb.btc_id == batch.id).all()
                mat = BtcmtrlDdb.query.filter(BtcmtrlDdb.btc_id == batch.id).all()
                rej = BtcrejcDdb.query.filter(BtcrejcDdb.btc_id == batch.id).all()
                wgs = WagesDdb.query.filter(WagesDdb.btc_id == batch.id).all()

                old_prod = []
                new_product = []
                for x in product:
                    if (
                        x["prod_id"]
                        and x["unit_id"]
                        # and x["loc_id"]
                        and x["qty"]
                        and x["aloc"]
                    ):
                        if x["id"] != 0:
                            old_prod.append(x["id"])
                        else:
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

                if len(old_prod) > 0:
                    for x in old_prod:
                        for y in prod:
                            if y.id not in old_prod:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in product:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.loc_id = z["loc_id"]
                                            y.qty = z["qty"]
                                            y.qty_f = z["qty_f"]
                                            y.aloc = z["aloc"]

                old_mat = []
                new_material = []
                for x in material:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_mat.append(x["id"])
                        else:
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

                if len(old_mat) > 0:
                    for x in old_mat:
                        for y in mat:
                            if y.id not in old_mat:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in material:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.qty = z["qty"]
                                            y.qty_f = z["qty_f"]
                                            y.price = z["price"]
                                            y.t_price = z["t_price"]

                old_rej = []
                new_reject = []
                for x in reject:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_rej.append(x["id"])
                        else:
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

                if len(old_rej) > 0:
                    for x in old_rej:
                        for y in rej:
                            if y.id not in old_rej:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in reject:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.loc_id = z["loc_id"]
                                            y.qty = z["qty"]
                                            y.aloc = z["aloc"]

                old_wgs = []
                new_wages = []
                for x in wages:
                    if x["acc_id"]:
                        if x["id"] != 0:
                            old_wgs.append(x["id"])
                        else:
                            new_wages.append(
                                WagesDdb(
                                    batch.id,
                                    x["acc_id"],
                                    x["nom_wgs"],
                                    x["desc"],
                                )
                            )

                if len(old_wgs) > 0:
                    for x in old_wgs:
                        for y in wgs:
                            if y.id not in old_wgs:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in wages:
                                        if z["id"] == x:
                                            y.acc_id = z["acc_id"]
                                            y.nom_wgs = z["nom_wgs"]
                                            y.desc = z["desc"]

                if len(new_product) > 0:
                    db.session.add_all(new_product)

                if len(new_material) > 0:
                    db.session.add_all(new_material)

                if len(new_reject) > 0:
                    db.session.add_all(new_reject)

                if len(new_wages) > 0:
                    db.session.add_all(new_wages)

                WriteActivity(user, bcode, "TRANSACTION", "EDITED")
                db.session.commit()

                updateDirectBatch(id, None, user_product, user_company, False)

                result = response(200, "Berhasil", True, dbatch_schema.dump(batch))

            except Exception as e:
                print(e)
                db.session.rollback()
                # result = response(400, "Kode sudah digunakan", False, None)
            finally:
                self.response = result

        elif request.method == "DELETE":
            bcode = batch.bcode
            WriteActivity(user, bcode, "TRANSACTION", "DELETED")
            updateDirectBatch(batch.id, None, user_product, user_company, True)

            product = BtcprodDdb.query.filter(BtcprodDdb.btc_id == batch.id)
            material = BtcmtrlDdb.query.filter(BtcmtrlDdb.btc_id == batch.id)
            reject = BtcrejcDdb.query.filter(BtcrejcDdb.btc_id == batch.id)
            wages = WagesDdb.query.filter(WagesDdb.btc_id == batch.id)

            for x in product:
                db.session.delete(x)

            for x in material:
                db.session.delete(x)

            for x in reject:
                db.session.delete(x)

            for x in wages:
                db.session.delete(x)

            db.session.delete(batch)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            batch = (
                db.session.query(
                    DirectBatchMdb, UnitMdb, CcostMdb, LocationMdb, FprdcHdb
                )
                .outerjoin(UnitMdb, UnitMdb.id == DirectBatchMdb.unit_id)
                .outerjoin(CcostMdb, CcostMdb.id == DirectBatchMdb.dep_id)
                .outerjoin(LocationMdb, LocationMdb.id == DirectBatchMdb.loc_id)
                .outerjoin(FprdcHdb, FprdcHdb.id == DirectBatchMdb.forml_id)
                .order_by(DirectBatchMdb.id.desc())
                .all()
            )

            product = (
                db.session.query(BtcprodDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == BtcprodDdb.unit_id)
                .all()
            )

            material = (
                db.session.query(BtcmtrlDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcmtrlDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == BtcmtrlDdb.unit_id)
                .all()
            )

            reject = (
                db.session.query(BtcrejcDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcrejcDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == BtcrejcDdb.unit_id)
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
                        rej.append(breject_schema.dump(y[0]))

                wgs = []
                for y in wages:
                    if x[0].id == y.btc_id:
                        wgs.append(wages_schema.dump(y))

                final.append(
                    {
                        "id": x[0].id,
                        "bcode": x[0].bcode,
                        "batch_date": DirectBatchSchema(only=["batch_date"]).dump(x[0])[
                            "batch_date"
                        ],
                        "forml_id": fprdc_schema.dump(x[4]),
                        "dep_id": ccost_schema.dump(x[2]),
                        "loc_id": loct_schema.dump(x[3]),
                        "unit_id": unit_schema.dump(x[1]),
                        "total": x[0].total,
                        "user_id": x[0].user_id,
                        "product": prod,
                        "material": mat,
                        "reject": rej,
                        "wages": wgs,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
