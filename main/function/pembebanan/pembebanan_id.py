from main.function.update_pembebanan import updatePembebanan
from main.function.write_activity import WriteActivity
from main.model.direct_batch_mdb import DirectBatchMdb
from main.model.pbb_hdb import PbbHdb
from main.model.upah_ddb import UpahDdb
from main.model.overhead_ddb import OverhDdb
from main.model.pbprod_ddb import PbprodDdb
from main.model.pbpanen_ddb import PbpanenDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.pbb_hdb import pbb_schema, PbbSchema
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.upah_ddb import upah_schema
from main.schema.overhead_ddb import overh_schema
from main.schema.pbprod_ddb import pbprod_schema


class PembebananId:
    def __new__(self, user, id, user_product, user_company, request):
        pbb = PbbHdb.query.filter(PbbHdb.id == id).first()
        if request.method == "PUT":
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

                pbb.pbb_code = pbb_code
                pbb.pbb_date = pbb_date
                pbb.pbb_name = pbb_name
                pbb.type_pb = type_pb
                pbb.prod_id = ",".join([str(x) for x in prod_id]) if prod_id else None
                pbb.batch_id = batch_id
                pbb.acc_cred = acc_cred
                pbb.period = period
                pbb.panen_prod = panen_prod
                pbb.panen_loc = panen_loc
                pbb.proj_id = proj_id
                pbb.desc = desc

                uph = UpahDdb.query.filter(UpahDdb.pbb_id == id).all()
                ovr = OverhDdb.query.filter(OverhDdb.pbb_id == id).all()
                prd = PbprodDdb.query.filter(PbprodDdb.pbb_id == id).all()
                pnn = PbpanenDdb.query.filter(PbpanenDdb.pbb_id == id).all()

                old_upah = []
                new_upah = []
                for x in upah:
                    if x["acc_id"] and x["nom_uph"]:
                        if x["id"] != 0:
                            old_upah.append(x["id"])
                        else:
                            new_upah.append(
                                UpahDdb(
                                    pbb.id,
                                    x["acc_id"],
                                    x["nom_uph"],
                                    x["desc"],
                                )
                            )

                if len(old_upah) > 0:
                    for x in old_upah:
                        for y in uph:
                            if y.id not in old_upah:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in upah:
                                        if z["id"] == x:
                                            y.acc_id = z["acc_id"]
                                            y.nom_uph = z["nom_uph"]
                                            y.desc = z["desc"]

                old_overh = []
                new_overh = []
                for x in overhead:
                    if x["acc_id"] and x["nom_ovr"]:
                        if x["id"] != 0:
                            old_overh.append(x["id"])
                        else:
                            new_overh.append(
                                OverhDdb(
                                    pbb.id,
                                    x["acc_id"],
                                    x["nom_ovr"],
                                    x["desc"],
                                )
                            )

                if len(old_overh) > 0:
                    for x in old_overh:
                        for y in ovr:
                            if y.id not in old_overh:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in overhead:
                                        if z["id"] == x:
                                            y.acc_id = z["acc_id"]
                                            y.nom_ovr = z["nom_ovr"]
                                            y.desc = z["desc"]

                old_prd = []
                new_prd = []
                for x in product:
                    if x["trn_id"] and x["prd_id"]:
                        if x["id"] != 0:
                            old_prd.append(x["id"])
                        else:
                            new_prd.append(
                                PbprodDdb(
                                    pbb.id,
                                    x["trn_id"],
                                    x["prd_id"],
                                    x["qty"],
                                    x["aloc"],
                                    x["aloc_qty"],
                                )
                            )

                if len(old_prd) > 0:
                    for x in old_prd:
                        for y in prd:
                            if y.id not in old_prd:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in product:
                                        if z["id"] == x:
                                            y.trn_id = z["trn_id"]
                                            y.prd_id = z["prd_id"]
                                            y.qty = z["qty"]
                                            y.aloc = z["aloc"]
                                            y.aloc_qty = z["aloc_qty"]

                old_pnn = []
                new_pnn = []
                for x in panen:
                    if x["trn_id"] and x["prd_id"]:
                        if x["id"] != 0:
                            old_pnn.append(x["id"])
                        else:
                            new_pnn.append(
                                PbpanenDdb(
                                    pbb.id,
                                    x["trn_id"],
                                    x["prd_id"],
                                    x["qty"],
                                    x["aloc"],
                                )
                            )

                if len(old_pnn) > 0:
                    for x in old_pnn:
                        for y in pnn:
                            if y.id not in old_pnn:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in panen:
                                        if z["id"] == x:
                                            y.trn_id = z["trn_id"]
                                            y.prd_id = z["prd_id"]
                                            y.qty = z["qty"]
                                            y.aloc = z["aloc"]

                if len(new_upah) > 0:
                    db.session.add_all(new_upah)

                if len(new_overh) > 0:
                    db.session.add_all(new_overh)

                if len(new_prd) > 0:
                    db.session.add_all(new_prd)

                if len(new_pnn) > 0:
                    db.session.add_all(new_pnn)

                updatePembebanan(id, user_product, user_company, False)

                WriteActivity(user, pbb_code, "TRANSACTION", "EDITED")

                db.session.commit()
                result = response(200, "Berhasil", True, pbb_schema.dump(pbb))

            except IntegrityError:
                db.session.rollback()
                result = response(
                    400, "Tidak dapat mengedit data karena status", False, None
                )
            finally:
                self.response = result

        elif request.method == "DELETE":
            pbb_code = pbb.pbb_code
            updatePembebanan(pbb.id, user_product, user_company, True)
            WriteActivity(user, pbb_code, "TRANSACTION", "DELETED")
            
            upah = UpahDdb.query.filter(UpahDdb.pbb_id == pbb.id)
            overhead = OverhDdb.query.filter(OverhDdb.pbb_id == pbb.id)
            prd = PbprodDdb.query.filter(PbprodDdb.pbb_id == pbb.id)
            pnn = PbpanenDdb.query.filter(PbpanenDdb.pbb_id == pbb.id)
            btc = DirectBatchMdb.query.filter(DirectBatchMdb.id == pbb.batch_id).first()

            # btc.pb = False
            # db.session.commit()

            for x in upah:
                db.session.delete(x)

            for x in overhead:
                db.session.delete(x)

            if prd:
                for x in prd:
                    db.session.delete(x)

            if pnn:
                for x in prd:
                    db.session.delete(x)

            db.session.delete(pbb)
            db.session.commit()


            self.response = response(200, "Berhasil", True, None)
        else:
            pbb = (
                db.session.query(PbbHdb, DirectBatchMdb)
                .outerjoin(DirectBatchMdb, DirectBatchMdb.id == PbbHdb.batch_id)
                .order_by(PbbHdb.id.desc())
                .all()
            )

            upah = db.session.query(UpahDdb).all()

            overhead = db.session.query(OverhDdb).all()

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

                final.append(
                    {
                        "id": x[0].id,
                        "pbb_code": x[0].pbb_code,
                        "pbb_name": x[0].pbb_name,
                        "pbb_date": PbbSchema(only=["pbb_date"]).dump(x[0])["pbb_date"],
                        "batch_id": dbatch_schema.dump(x[1]),
                        "acc_cred": x[0].acc_cred,
                        "desc": x[0].desc,
                        "user_id": x[0].user_id,
                        "upah": uph,
                        "overhead": ovr,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
