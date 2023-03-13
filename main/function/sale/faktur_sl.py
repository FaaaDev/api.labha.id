from main.function.update_table import UpdateTable
from main.function.update_faktur_pj import UpdateFakturPj
from main.model.ccost_mdb import CcostMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.fkpj_hdb import FkpjHdb
from main.model.fkpj_det_ddb import FkpjDetDdb
from main.model.inv_pj_hdb import InvoicePjHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.custom_mdb import CustomerMdb
from main.model.jasa_mdb import JasaMdb
from main.model.prod_mdb import ProdMdb
from main.model.unit_mdb import UnitMdb
from main.schema.ordpj_hdb import OrdpjSchema, ordpj_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.custom_mdb import customer_schema
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.fkpj_hdb import FkpjSchema, fkpj_schema
from main.schema.fkpj_det_ddb import fkpjd_schema
from main.schema.inv_pj_hdb import invpj_schema
from main.schema.jprod_ddb import jprod_schema
from main.schema.jjasa_ddb import jjasa_schema
from main.schema.lokasi_mdb import loct_schema


class FakturPj:
    def __new__(self, user, request):
        if request.method == "POST":
            fk_code = request.json["fk_code"]
            fk_date = request.json["fk_date"]
            pel_id = request.json["pel_id"]
            fk_tax = request.json["fk_tax"]
            fk_ppn = request.json["fk_ppn"]
            fk_desc = request.json["fk_desc"]
            detail = request.json["detail"]

            faktur = FkpjHdb(fk_code, fk_date, pel_id, fk_tax, fk_ppn, fk_desc)

            db.session.add(faktur)

            inv = InvoicePjHdb.query.all()
            ord = OrdpjHdb.query.all()

            new_detail = []
            for x in detail:
                if x["inv_id"] and x["total_pay"]:
                    new_detail.append(
                        FkpjDetDdb(
                            faktur.id,
                            x["inv_id"],
                            x["sale_id"],
                            x["inv_date"],
                            x["total"],
                            x["total_pay"],
                        )
                    )

                for i in inv:
                    if x["inv_id"] == i.id:
                        i.faktur = True

                for o in ord:
                    if x["sale_id"] == o.id:
                        o.surat_jalan = 2

            if len(new_detail) > 0:
                db.session.add_all(new_detail)

            db.session.commit()

            UpdateFakturPj(
                faktur.id,
                False,
                None,
                user.id,
            )

            return response(200, "success", True, fkpj_schema.dump(faktur))
        else:
            try:
                fk = (
                    db.session.query(FkpjHdb, CustomerMdb)
                    .outerjoin(CustomerMdb, CustomerMdb.id == FkpjHdb.pel_id)
                    .order_by(FkpjHdb.id.desc())
                    .all()
                )
                det = (
                    db.session.query(FkpjDetDdb, InvoicePjHdb, OrdpjHdb)
                    .outerjoin(InvoicePjHdb, InvoicePjHdb.id == FkpjDetDdb.inv_id)
                    .outerjoin(OrdpjHdb, OrdpjHdb.id == FkpjDetDdb.sale_id)
                    .all()
                )

                jprod = (
                    db.session.query(JprodDdb, ProdMdb, UnitMdb, LocationMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                    .outerjoin(UnitMdb, UnitMdb.id == JprodDdb.unit_id)
                    .outerjoin(LocationMdb, LocationMdb.id == JprodDdb.location)
                    .all()
                )

                jjasa = (
                    db.session.query(JjasaDdb, JasaMdb, UnitMdb)
                    .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                    .outerjoin(UnitMdb, UnitMdb.id == JjasaDdb.unit_id)
                    .all()
                )

                final = []
                for x in fk:
                    detail = []
                    if x[0]:
                        for y in det:
                            if x[0]:
                                if y[0].fk_id == x[0].id:
                                    prod = []
                                    for p in jprod:
                                        if p[0]:
                                            if p[0].pj_id == y[2].id:
                                                p[0].prod_id = prod_schema.dump(p[1])
                                                p[0].unit_id = unit_schema.dump(p[2])
                                                p[0].location = (
                                                    loct_schema.dump(p[3])
                                                    if p[0].location
                                                    else None
                                                )
                                                prod.append(jprod_schema.dump(p[0]))

                                    jasa = []
                                    for z in jjasa:
                                        if z[0]:
                                            if z[0].pj_id == y[2].id:
                                                z[0].jasa_id = jasa_schema.dump(z[1])
                                                z[0].unit_id = unit_schema.dump(z[2])
                                                jasa.append(jjasa_schema.dump(z[0]))

                                    y[0].inv_id = invpj_schema.dump(y[1])
                                    y[0].sale_id = {
                                        "id": y[2].id,
                                        "ord_code": y[2].ord_code,
                                        "ord_date": y[2].ord_date.isoformat(),
                                        "invoice": y[2].invoice,
                                        "so_id": y[2].so_id,
                                        "sub_addr": y[2].sub_addr,
                                        "sub_id": y[2].sub_id,
                                        "pel_id": y[2].pel_id,
                                        "due_date": y[2].due_date.isoformat(),
                                        "product": prod,
                                        "jasa": jasa,
                                    }
                                    detail.append(fkpjd_schema.dump(y[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "fk_code": x[0].fk_code,
                            "fk_date": x[0].fk_date.isoformat(),
                            "pel_id": customer_schema.dump(x[1]),
                            "fk_tax": x[0].fk_tax,
                            "fk_ppn": x[0].fk_ppn,
                            "fk_lunas": x[0].fk_lunas,
                            "fk_desc": x[0].fk_desc,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "detail": detail,
                            "product": prod,
                            "jasa": jasa,
                        }
                    )

                return response(200, "success", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
                        FkpjHdb,
                        CustomerMdb,
                        FkpjDetDdb,
                        InvoicePjHdb,
                        OrdpjHdb,
                        JprodDdb,
                        ProdMdb,
                        UnitMdb,
                        LocationMdb,
                        JjasaDdb,
                        JasaMdb,
                    ],
                    request,
                )
