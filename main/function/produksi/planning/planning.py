
from main.function.update_table import UpdateTable
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
from main.schema.fprdc_hdb import fprdc_schema
from main.schema.fmtrl_ddb import fmtrl_schema
from main.schema.fprod_ddb import fprod_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.msn_mdb import msn_schema
from main.schema.plmch_ddb import plmch_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.lokasi_mdb import loct_schema


class Planning:
    def __new__(self, user, request):
        if request.method == "POST":
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

                plan = PlanHdb(
                    pcode, pname, form_id, dep_id, loc_id, desc, date_planing, total, unit
                )

                db.session.add(plan)
                db.session.commit()

                new_mesin = []
                for x in mesin:
                    if x["mch_id"]:
                        new_mesin.append(PlmchDdb(plan.id, x["mch_id"]))

                if len(new_mesin) > 0:
                    db.session.add_all(new_mesin)

                db.session.commit()

                UpdateRpbb(plan.id, False)

                result = response(200, "Berhasil", True,
                                  plan_schema.dump(plan))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        else:
            try:
                plan = (
                    db.session.query(PlanHdb, FprdcHdb,
                                     UnitMdb, CcostMdb, LocationMdb)
                    .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
                    .outerjoin(UnitMdb, UnitMdb.id == PlanHdb.unit)
                    .outerjoin(CcostMdb, CcostMdb.id == PlanHdb.dep_id)
                    .outerjoin(LocationMdb, LocationMdb.id == PlanHdb.loc_id)
                    .order_by(PlanHdb.id.desc())
                    .all()
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

                final = []
                for x in plan:
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

                    final.append(
                        {
                            "id": x[0].id,
                            "pcode": x[0].pcode,
                            "pname": x[0].pname,
                            "form_id": fprdc_schema.dump(x[1]),
                            "dep_id": ccost_schema.dump(x[3]),
                            "loc_id": loct_schema.dump(x[4]),
                            "desc": x[0].desc,
                            "date_created": PlanSchema(only=["date_created"]).dump(x[0])[
                                "date_created"
                            ],
                            "date_planing": PlanSchema(only=["date_planing"]).dump(x[0])[
                                "date_planing"
                            ],
                            "total": x[0].total,
                            "unit": unit_schema.dump(x[2]),
                            "material": mat,
                            "product": prod,
                            "mesin": msn,
                        }
                    )

                return response(200, "Berhasil", True, final)

            except ProgrammingError as e:
                return UpdateTable(
                    [PlanHdb, FprdcHdb, UnitMdb, CcostMdb, LocationMdb,
                        FprodDdb, ProdMdb, UnitMdb, FmtrlDdb, PlmchDdb, MsnMdb], request
                )
