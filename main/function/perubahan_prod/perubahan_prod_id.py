from main.function.update_pproduct import UpdatePerubahanProd
from main.function.write_activity import WriteActivity
from main.model.lokasi_mdb import LocationMdb
from main.model.pproduct_hdb import PproductHdb
from main.model.prod_asal_ddb import PAsalDdb
from main.model.prod_jadi_ddb import PJadiDdb
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.pproduct_hdb import pproduct_schema, PproductSchema
from main.schema.direct_batch_mdb import dbatch_schema, DirectBatchSchema
from main.schema.prod_asal_ddb import prod_asal_schema
from main.schema.prod_jadi_ddb import prod_jadi_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema


class PerubahanProdId:
    def __new__(self, user, id, user_product, user_company, request):
        pproduct = PproductHdb.query.filter(PproductHdb.id == id).first()
        if request.method == "PUT":
            try:
                pp_code = request.json["pp_code"]
                pp_date = request.json["pp_date"]
                pasal = request.json["pasal"]
                pjadi = request.json["pjadi"]

                pproduct.pp_code = pp_code
                pproduct.pp_date = pp_date

                prodA = PAsalDdb.query.filter(PAsalDdb.pp_id == id).all()
                prodJ = PJadiDdb.query.filter(PJadiDdb.pp_id == id).all()

                old_prodA = []
                new_product_asal = []
                for x in pasal:
                    if x["prod_id"] and x["unit_id"] and x["loc_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_prodA.append(x["id"])
                        else:
                            new_product_asal.append(
                                PAsalDdb(
                                    pproduct.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["loc_id"],
                                    x["qty"],
                                )
                            )

                if len(old_prodA) > 0:
                    for x in old_prodA:
                        for y in prodA:
                            if y.id not in old_prodA:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in pasal:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.loc_id = z["loc_id"]
                                            y.qty = z["qty"]

                old_prodJ = []
                new_product_jadi = []
                for x in pjadi:
                    if x["prod_id"] and x["unit_id"] and x["qty"]:
                        if x["id"] != 0:
                            old_prodJ.append(x["id"])
                        else:
                            new_product_jadi.append(
                                PJadiDdb(
                                    pproduct.id,
                                    x["prod_id"],
                                    x["unit_id"],
                                    x["loc_id"],
                                    x["qty"],
                                )
                            )

                if len(old_prodJ) > 0:
                    for x in old_prodJ:
                        for y in prodJ:
                            if y.id not in old_prodJ:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in pjadi:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.loc_id = z["loc_id"]
                                            y.qty = z["qty"]

                if len(new_product_asal) > 0:
                    db.session.add_all(new_product_asal)

                if len(new_product_jadi) > 0:
                    db.session.add_all(new_product_jadi)

                UpdatePerubahanProd(id, False, user_product, user_company)

                WriteActivity(user, pp_code, "TRANSACTION", "EDITED")

                db.session.commit()
                
                result = response(200, "Berhasil", True, pproduct_schema.dump(pproduct))

            except IntegrityError:
                db.session.rollback()
                result = response(
                    400, "Tidak dapat mengedit data karena status", False, None
                )
            finally:
                self.response = result

        elif request.method == "DELETE":
            pp_code = pproduct.pp_code
            UpdatePerubahanProd(pproduct.id, True, user_product, user_company)

            WriteActivity(user, pp_code, "TRANSACTION", "DELETED")

            productA = PAsalDdb.query.filter(PAsalDdb.pp_id == pproduct.id)
            productJ = PJadiDdb.query.filter(PJadiDdb.pp_id == pproduct.id)

            for x in productA:
                db.session.delete(x)

            for x in productJ:
                db.session.delete(x)

            db.session.delete(pproduct)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)
        else:
            pp = db.session.query.order_by(PproductHdb.id.desc()).all()

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
                pasal = []
                for y in pasal:
                    if x.id == y.pp_id:
                        y[0].prod_id = prod_schema.dump(y[1])
                        y[0].unit_id = unit_schema.dump(y[2])
                        y[0].loc_id = loct_schema.dump(y[3])
                        pasal.append(prod_asal_schema.dump(y[0]))

                pjadi = []
                for y in pjadi:
                    if x.id == y.pp_id:
                        y[0].prod_id = prod_schema.dump(y[1])
                        y[0].unit_id = unit_schema.dump(y[2])
                        y[0].loc_id = loct_schema.dump(y[3])
                        pjadi.append(prod_jadi_schema.dump(y[0]))

                final.append(
                    {
                        "id": x.id,
                        "pp_code": x.pp_code,
                        "pp_date": PproductSchema(only=["pp_date"]).dump(x)["pp_date"],
                        "user_id": x.user_id,
                        "pasal": pasal,
                        "pjadi": pjadi,
                    }
                )

            self.response = response(200, "Berhasil", True, final)

        return self.response
