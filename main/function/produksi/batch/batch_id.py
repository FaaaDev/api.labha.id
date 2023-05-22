from main.function.update_batch import updateBatch
# from main.function.write_activity import WriteActivity
from main.model.batch_mdb import BatchMdb
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
from main.schema.batch_mdb import batch_schema, BatchSchema
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


class BatchId:
    def __new__(self, id, request):
        x = BatchMdb.query.filter(BatchMdb.id == id).first()
        if request.method == "PUT":
            try:
                x.bcode = request.json["bcode"]
                x.batch_date = request.json["batch_date"]
                x.plan_id = request.json["plan_id"]
                x.dep_id = request.json["dep_id"]

                db.session.commit()

                result = response(200, "Berhasil", True, batch_schema.dump(x))
            except IntegrityError:
                db.session.rollback()
                result = response(400, "Kode sudah digunakan", False, None)
            finally:
                return result
        elif request.method == "DELETE":
            updateBatch(x.id, True)
            db.session.delete(x)
            db.session.commit()

            return response(200, "Berhasil", True, None)
        else:
            batch = (
                db.session.query(
                    BatchMdb, PlanHdb, FprdcHdb, UnitMdb, CcostMdb, LocationMdb
                )
                .outerjoin(PlanHdb, PlanHdb.id == BatchMdb.plan_id)
                .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
                .outerjoin(UnitMdb, UnitMdb.id == PlanHdb.unit)
                .outerjoin(CcostMdb, CcostMdb.id == BatchMdb.dep_id)
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

            for x in batch:
                if x[0].id == id:
                    prod = []
                    for y in product:
                        if x[2].id == y[0].form_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            prod.append(fprod_schema.dump(y[0]))

                    mat = []
                    for y in material:
                        if x[2].id == y[0].form_id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            mat.append(fmtrl_schema.dump(y[0]))

                    msn = []
                    for y in mesin:
                        if x[1].id == y[0].pl_id:
                            y[0].mch_id = msn_schema.dump(y[1])
                            msn.append(plmch_schema.dump(y[0]))

                    final = {
                        "id": x[0].id,
                        "bcode": x[0].bcode,
                        "batch_date": BatchSchema(only=["batch_date"]).dump(x[0])[
                            "batch_date"
                        ],
                        "dep_id": ccost_schema.dump(x[4]),
                        "plan_id": {
                            "id": x[1].id,
                            "pcode": x[1].pcode,
                            "pname": x[1].pname,
                            "form_id": fprdc_schema.dump(x[1]),
                            "loc_id": loct_schema.dump(x[1]),
                            "desc": x[1].desc,
                            "date_created": PlanSchema(only=["date_created"]).dump(x[1])[
                                "date_created"
                            ],
                            "date_planing": PlanSchema(only=["date_planing"]).dump(x[1])[
                                "date_planing"
                            ],
                            "total": x[1].total,
                            "unit": unit_schema.dump(x[3]),
                            "material": mat,
                            "product": prod,
                            "mesin": msn,
                        },
                    }

            return response(200, "Berhasil", True, final)

        return self.response
