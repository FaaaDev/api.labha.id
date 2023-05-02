from ...function.update_pembelian import UpdatePembelian
from ...function.update_stock import UpdateStock
from ...model.ccost_mdb import CcostMdb
from ...model.jjasa_ddb import JjasaDdb
from ...model.jprod_ddb import JprodDdb
from ...model.inv_pj_hdb import InvoicePjHdb
from ...model.lokasi_mdb import LocationMdb
from ...model.ordpj_hdb import OrdpjHdb
from ...model.prod_mdb import ProdMdb
from ...model.jasa_mdb import JasaMdb
from ...model.unit_mdb import UnitMdb
from ...schema.ordpj_hdb import OrdpjSchema, ordpj_schema
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import IntegrityError
from ...schema.prod_mdb import prod_schema
from ...schema.jasa_mdb import jasa_schema
from ...schema.unit_mdb import unit_schema
from ...schema.inv_pj_hdb import InvoicePjSchema, invpj_schema
from ...schema.jprod_ddb import jprod_schema
from ...schema.jjasa_ddb import jjasa_schema
from ...schema.lokasi_mdb import loct_schema


class InvoicePjId:
    def __new__(self, id, request):
        inv = InvoicePjHdb.query.filter(InvoicePjHdb.id == id).first()
        if request.method == "PUT":
            inv_date = request.json["inv_date"]
            sale_id = request.json["sale_id"]
            inv_tax = request.json["inv_tax"]
            inv_ppn = request.json["inv_ppn"]
            inv_desc = request.json["inv_desc"]
            total_bayar = request.json["total_bayar"]

            inv.inv_date = inv_date
            inv.sale_id = sale_id
            inv.inv_tax = inv_tax
            inv.inv_ppn = inv_ppn
            inv.inv_desc = inv_desc
            inv.total_bayar = total_bayar
            inv.faktur = False

            db.session.commit()

            self.response = response(200, "success", True, invpj_schema.dump(inv))
        elif request.method == "DELETE":
            # UpdatePembelian(fk.id, id, True, user_product, user_company, glUrl, request)
            # prod = JprodDdb.query.filter(JprodDdb.pj_id == fk.sale_id).all()

            # for x in prod:
            #     x.location = None

            db.session.delete(inv)
            db.session.commit()

            self.response = response(200, "success", True, None)
        else:
            x = (
                db.session.query(InvoicePjHdb, OrdpbHdb)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == InvoicePjHdb.sale_id)
                .filter(InvoicePjHdb.id == id)
                .first()
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
                            if y[0].ord_id == x[1].id:
                                y[0].prod_id = prod_schema.dump(y[1])
                                y[0].unit_id = unit_schema.dump(y[2])
                                y[0].location = (
                                    loct_schema.dump(y[3]) if y[0].location else None
                                )
                                product.append(jprod_schema.dump(y[0]))

                jasa = []
                if x[1]:
                    for z in jjasa:
                        if x[1]:
                            if z[0].ord_id == x[1].id:
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
                        "post": x[0].post,
                        "closing": x[0].closing,
                        "product": product,
                        "jasa": jasa,
                    }
                )
                
            self.response = response(200, "success", True, final)

        return self.response
