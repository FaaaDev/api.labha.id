from main.model.ccost_mdb import CcostMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.inv_pb_hdb import InvpbHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.schema.dord_hdb import DordSchema, dord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.inv_pb_hdb import InvpbSchema, invpb_schema
from main.schema.dprod_ddb import dprod_schema
from main.schema.djasa_ddb import djasa_schema
from main.schema.lokasi_mdb import loct_schema


class InvoicePb:
    def __new__(self, user, request):
        if request.method == "POST":
            inv_code = request.json["inv_code"]
            inv_date = request.json["inv_date"]
            ord_id = request.json["ord_id"]
            inv_tax = request.json["inv_tax"]
            inv_ppn = request.json["inv_ppn"]
            inv_desc = request.json["inv_desc"]
            total_bayar = request.json["total_bayar"]

            invoice = InvpbHdb(
                inv_code,
                inv_date,
                ord_id,
                inv_tax,
                inv_ppn,
                inv_desc,
                total_bayar,
                False,
            )

            db.session.add(invoice)

            db.session.commit()

            # UpdateFakturPj(faktur.id, False, faktur.sale_id, user.id, user.product, user.company, glUrl, request)

            self.response = response(200, "success", True, invpb_schema.dump(invoice))
        else:
            inv = (
                db.session.query(InvpbHdb, OrdpbHdb)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == InvpbHdb.ord_id)
                .order_by(InvpbHdb.id.desc())
                .all()
            )
            dprod = (
                db.session.query(DprodDdb, ProdMdb, UnitMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == DprodDdb.unit_id)
                .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
                .all()
            )

            djasa = (
                db.session.query(DjasaDdb, JasaMdb, UnitMdb)
                .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
                .outerjoin(UnitMdb, UnitMdb.id == DjasaDdb.unit_id)
                .all()
            )

            final = []
            for x in inv:
                product = []
                if x[1]:
                    for y in dprod:
                        if x[1]:
                            if y[0].ord_id == x[1].id:
                                y[0].prod_id = prod_schema.dump(y[1])
                                y[0].unit_id = unit_schema.dump(y[2])
                                y[0].location = (
                                    loct_schema.dump(y[3]) if y[0].location else None
                                )
                                product.append(dprod_schema.dump(y[0]))

                jasa = []
                if x[1]:
                    for z in djasa:
                        if x[1]:
                            if z[0].ord_id == x[1].id:
                                z[0].jasa_id = jasa_schema.dump(z[1])
                                z[0].unit_id = unit_schema.dump(z[2])
                                jasa.append(djasa_schema.dump(z[0]))

                final.append(
                    {
                        "id": x[0].id,
                        "inv_code": x[0].inv_code,
                        "inv_date": x[0].inv_date.isoformat(),
                        "ord_id": dord_schema.dump(x[1]),
                        "inv_tax": x[0].inv_tax,
                        "inv_ppn": x[0].inv_ppn,
                        "inv_lunas": x[0].inv_lunas,
                        "inv_desc": x[0].inv_desc,
                        "total_bayar": x[0].total_bayar,
                        "faktur": x[0].faktur,
                        "post": x[0].post,
                        "closing": x[0].closing,
                        "product": product,
                        "jasa": jasa,
                    }
                )

            self.response = response(200, "success", True, final)

        return self.response
