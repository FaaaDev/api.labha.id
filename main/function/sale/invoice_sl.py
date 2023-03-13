from main.function.update_table import UpdateTable
from main.function.update_faktur_pj import UpdateFakturPj
from main.model.ccost_mdb import CcostMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.inv_pj_hdb import InvoicePjHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.schema.ordpj_hdb import OrdpjSchema, ordpj_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.inv_pj_hdb import InvoicePjSchema, invpj_schema
from main.schema.jprod_ddb import jprod_schema
from main.schema.jjasa_ddb import jjasa_schema
from main.schema.lokasi_mdb import loct_schema


class InvoicePj:
    def __new__(self, user, request):
        if request.method == "POST":
            inv_code = request.json["inv_code"]
            inv_date = request.json["inv_date"]
            sale_id = request.json["sale_id"]
            inv_tax = request.json["inv_tax"]
            inv_ppn = request.json["inv_ppn"]
            inv_desc = request.json["inv_desc"]
            total_bayar = request.json["total_bayar"]

            invoice = InvoicePjHdb(
                inv_code,
                inv_date,
                sale_id,
                inv_tax,
                inv_ppn,
                inv_desc,
                total_bayar,
                False,
            )

            db.session.add(faktur)

            db.session.commit()

            # UpdateFakturPj(faktur.id, False, faktur.sale_id, user.id, user.product, user.company, glUrl, request)

            return response(200, "success", True, invpj_schema.dump(invoice))
        else:
            try:
                inv = (
                    db.session.query(InvoicePjHdb, OrdpjHdb)
                    .outerjoin(OrdpjHdb, OrdpjHdb.id == InvoicePjHdb.sale_id)
                    .order_by(InvoicePjHdb.id.desc())
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
                for x in inv:
                    product = []
                    if x[1]:
                        for y in jprod:
                            if x[1]:
                                if y[0].pj_id == x[1].id:
                                    y[0].prod_id = prod_schema.dump(y[1])
                                    y[0].unit_id = unit_schema.dump(y[2])
                                    y[0].location = (
                                        loct_schema.dump(y[3])
                                        if y[0].location
                                        else None
                                    )
                                    product.append(jprod_schema.dump(y[0]))

                    jasa = []
                    if x[1]:
                        for z in jjasa:
                            if x[1]:
                                if z[0].pj_id == x[1].id:
                                    z[0].jasa_id = jasa_schema.dump(z[1])
                                    z[0].unit_id = unit_schema.dump(z[2])
                                    jasa.append(jjasa_schema.dump(z[0]))

                    final.append(
                        {
                            "id": x[0].id,
                            "inv_code": x[0].inv_code,
                            "inv_date": x[0].inv_date.isoformat(),
                            "inv_tax": x[0].inv_tax,
                            "inv_ppn": x[0].inv_ppn,
                            "inv_lunas": x[0].inv_lunas,
                            "inv_desc": x[0].inv_desc,
                            "sale_id": ordpj_schema.dump(x[1]),
                            "total_bayar": x[0].total_bayar,
                            "faktur": x[0].faktur,
                            "post": x[0].post,
                            "closing": x[0].closing,
                            "product": product,
                            "jasa": jasa,
                        }
                    )

                return response(200, "success", True, final)
            except ProgrammingError as e:
                return UpdateTable(
                    [
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
