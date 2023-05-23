from main.function.update_rpbb import UpdateRpbb
# from main.function.write_activity import WriteActivity
from main.model.unit_mdb import UnitMdb
from main.model.prod_mdb import ProdMdb
from main.model.plan_hdb import PlanHdb
from main.model.plmch_ddb import PlmchDdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.fprod_ddb import FprodDdb
from main.model.msn_mdb import MsnMdb
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.plan_hdb import plan_schema, PlanSchema
from main.schema.fmtrl_ddb import fmtrl_schema
from main.schema.fprod_ddb import fprod_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.plmch_ddb import plmch_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.lokasi_mdb import loct_schema


class PlanningId:
    def __new__(self, id, request):
        x = PlanHdb.query.filter(PlanHdb.id == id).first()
        if request.method == "PUT":
            try:
                pcode = request.json["pcode"]
                pname = request.json["pname"]
                form_id = request.json["form_id"]
                dep_id = request.json["dep_id"]
                loc_id = request.json["loc_id"]
                desc = request.json["desc"]
                date_planing = request.json["date_planing"]
                total = request.json["total"]
                unit = request.json["unit"]
                mesin = request.json["mesin"]

                x.pcode = pcode
                x.pname = pname
                x.form_id = form_id
                x.dep_id = dep_id
                x.loc_id = loc_id
                x.desc = desc
                x.date_planing = date_planing
                x.total = total
                x.unit = unit

                db.session.commit()

                old_mesin = PlmchDdb.query.filter(PlmchDdb.pl_id == id).all()
                new_mesin = []

                for z in mesin:
                    if z["id"]:
                        for y in old_mesin:
                            if z["id"] == y.id:
                                if z["mch_id"]:
                                    y.mch_id = z["mch_id"]
                    else:
                        if z["mch_id"]:
                            new_mesin.append(PlmchDdb(id, x["mch_id"]))

                if len(new_mesin) > 0:
                    db.session.add_all(new_mesin)

                db.session.commit()

                UpdateRpbb(x.id, False)

                result = response(200, "Berhasil", True, plan_schema.dump(x))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        elif request.method == "DELETE":
            UpdateRpbb(x.id, True)
            old_mesin = PlmchDdb.query.filter(PlmchDdb.pl_id == id).all()

            for y in old_mesin:
                db.session.delete(y)

            db.session.delete(x)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            x = (
                db.session.query(PlanHdb, FprdcHdb, UnitMdb, CcostMdb, LocationMdb)
                .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
                .outerjoin(UnitMdb, UnitMdb.id == PlanHdb.unit)
                .outerjoin(CcostMdb, CcostMdb.id == PlanHdb.dep_id)
                .outerjoin(LocationMdb, LocationMdb.id == PlanHdb.loc_id)
                .filter(PlanHdb.id == id)
                .first()
            )

            product = (
                db.session.query(FprodDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == FprodDdb.unit_id)
                .all()
            )

            material = (
                db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
                .all()
            )

            mesin = (
                db.session.query(PlmchDdb, MsnMdb)
                .outerjoin(MsnMdb, MsnMdb.id == PlmchDdb.mch_id)
                .all()
            )

            prod = []
            for y in product:
                if x[1].id == y[0].form_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    prod.append(fprod_schema.dump(y[0]))

            mat = []
            for y in material:
                if x[1].id == y[0].form_id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    mat.append(fmtrl_schema.dump(y[0]))

            msn = []
            for y in mesin:
                if x[0].id == y[0].pl_id:
                    y[0].mch_id = msn_schema.dump(y[1])
                    msn.append(plmch_schema.dump(y[0]))

            final = {
                "id": x[0].id,
                "pcode": x[0].pcode,
                "pname": x[0].pname,
                "form_id": fprdc_schema.dump(x[1]),
                "dep_id": ccost_schema.dump(x[3]),
                "loc_id": loct_schema.dump(x[4]),
                "desc": x[0].desc,
                "date_created": PlanSchema(only=["date_creaded"]).dump(x[0])[
                    "date_created"
                ],
                "date_planing": PlanSchema(only=["date_planing"]).dump(x[0])[
                    "date_planing"
                ],
                "total": x[0].total,
                "unit": units_schema.dump(x[2]),
                "material": mat,
                "product": prod,
                "mesin": msn,
            }

            return response(200, "Berhasil", True, final)

        return self.response
