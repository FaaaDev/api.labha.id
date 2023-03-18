from main.function.update_table import UpdateTable
from main.model.preq_mdb import PreqMdb
from main.model.rprod_mdb import RprodMdb
from main.model.rjasa_mdb import RjasaMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.ccost_mdb import CcostMdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.preq_mdb import PreqSchema, preq_schema
from main.schema.rprod_mdb import rprod_schema
from main.schema.rjasa_mdb import rjasa_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.ccost_mdb import ccost_schema
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema


class RequestPurchase:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                req_code = request.json["req_code"]
                req_date = request.json["req_date"]
                req_dep = request.json["req_dep"]
                req_ket = request.json["req_ket"]
                refrence = request.json["refrence"]
                ref_sup = request.json["ref_sup"]
                ref_ket = request.json["ref_ket"]
                ns = request.json["ns"]

                rp = PreqMdb(
                    req_code,
                    req_date,
                    req_dep,
                    req_ket,
                    refrence,
                    ref_sup,
                    ref_ket,
                    ns,
                    0,
                )
                db.session.add(rp)
                db.session.commit()

                rprod = request.json["rprod"]
                all_prod = []
                for x in rprod:
                    if x["prod_id"] and x["unit_id"] and x["request"]:
                        all_prod.append(
                            RprodMdb(
                                rp.id,
                                x["prod_id"],
                                x["unit_id"],
                                x["request"],
                                x["request"],
                            )
                        )

                if len(all_prod) > 0:
                    db.session.add_all(all_prod)

                rjasa = request.json["rjasa"]
                all_jasa = []
                for x in rjasa:
                    if x["jasa_id"] and x["request"]:
                        all_jasa.append(
                            RjasaMdb(
                                rp.id,
                                x["jasa_id"],
                                x["unit_id"],
                                x["request"],
                                x["request"],
                            )
                        )

                if len(all_jasa) > 0:
                    db.session.add_all(all_jasa)

                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, preq_schema.dump(rp))
        else:
            try:
                preq = (
                    db.session.query(PreqMdb, CcostMdb, SupplierMdb)
                    .outerjoin(CcostMdb, CcostMdb.id == PreqMdb.req_dep)
                    .outerjoin(SupplierMdb, SupplierMdb.id == PreqMdb.ref_sup)
                    .order_by(PreqMdb.id.desc())
                    .all()
                )
                rprod = (
                    db.session.query(RprodMdb, ProdMdb, UnitMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == RprodMdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == RprodMdb.unit_id)
                    .all()
                )
                rjasa = (
                    db.session.query(RjasaMdb, JasaMdb, UnitMdb)
                    .outerjoin(JasaMdb, JasaMdb.id == RjasaMdb.jasa_id)
                    .outerjoin(UnitMdb, UnitMdb.id == RjasaMdb.unit_id)
                    .all()
                )

                final = []

                for x in preq:
                    product = []
                    for y in rprod:
                        if y[0].preq_id == x[0].id:
                            y[0].prod_id = prod_schema.dump(y[1])
                            y[0].unit_id = unit_schema.dump(y[2])
                            product.append(rprod_schema.dump(y[0]))

                    jasa = []
                    for z in rjasa:
                        if z[0].preq_id == x[0].id:
                            z[0].jasa_id = jasa_schema.dump(z[1])
                            z[0].unit_id = unit_schema.dump(z[2])
                            jasa.append(rjasa_schema.dump(z[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "req_code": x[0].req_code,
                            "req_date": PreqSchema(only=["req_date"]).dump(x[0])[
                                "req_date"
                            ],
                            "req_dep": ccost_schema.dump(x[1]) if x[1] else None,
                            "req_ket": x[0].req_ket,
                            "refrence": x[0].refrence,
                            "ref_sup": supplier_schema.dump(x[2]) if x[2] else None,
                            "ref_ket": x[0].ref_ket,
                            "ns": x[0].ns,
                            "status": x[0].status,
                            "rprod": product,
                            "rjasa": jasa,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        PreqMdb,
                        CcostMdb,
                        SupplierMdb,
                        RprodMdb,
                        ProdMdb,
                        UnitMdb,
                        RjasaMdb,
                    ],
                    request,
                )
