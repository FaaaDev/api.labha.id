from main.function.update_pembelian import UpdatePembelian
from main.function.update_stock import UpdateStock
from main.model.ccost_mdb import CcostMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.po_mdb import PoMdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.unit_mdb import UnitMdb
from main.model.syarat_bayar_mdb import RulesPayMdb
from main.schema.dord_hdb import DordSchema, dord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.syarat_bayar_mdb import rpay_schema
from main.schema.dprod_ddb import dprod_schema
from main.schema.djasa_ddb import djasa_schema
from main.schema.supplier_mdb import supplier_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.po_mdb import po_schema
from main.schema.ccost_mdb import ccost_schema


class OrderDate:
    def __new__(self, user, request):
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]

        do = (
            db.session.query(OrdpbHdb, CcostMdb, SupplierMdb, RulesPayMdb, PoMdb)
            .outerjoin(CcostMdb, CcostMdb.id == OrdpbHdb.dep_id)
            .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
            .outerjoin(RulesPayMdb, RulesPayMdb.id == OrdpbHdb.top)
            .outerjoin(PoMdb, PoMdb.id == OrdpbHdb.po_id)
            .filter(OrdpbHdb.ord_date >= start_date, OrdpbHdb.ord_date <= end_date)
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
        for x in do:
            product = []
            for y in dprod:
                if y[0].ord_id == x[0].id:
                    y[0].prod_id = prod_schema.dump(y[1])
                    y[0].unit_id = unit_schema.dump(y[2])
                    y[0].location = loct_schema.dump(y[3]) if y[0].location else None
                    product.append(dprod_schema.dump(y[0]))

            jasa = []
            for z in djasa:
                if z[0].ord_id == x[0].id:
                    z[0].jasa_id = jasa_schema.dump(z[1])
                    z[0].unit_id = unit_schema.dump(z[2])
                    jasa.append(djasa_schema.dump(z[0]))

            final.append(
                {
                    "id": x[0].id,
                    "ord_code": x[0].ord_code,
                    "ord_date": DordSchema(only=["ord_date"]).dump(x[0])["ord_date"],
                    "faktur": x[0].faktur,
                    "po_id": po_schema.dump(x[4]),
                    "dep_id": ccost_schema.dump(x[1]),
                    "sup_id": supplier_schema.dump(x[2]),
                    "top": rpay_schema.dump(x[3]),
                    "due_date": DordSchema(only=["due_date"]).dump(x[0])["due_date"],
                    "split_inv": x[0].split_inv,
                    "prod_disc": x[0].prod_disc,
                    "jasa_disc": x[0].jasa_disc,
                    "total_disc": x[0].total_disc,
                    "status": x[0].status,
                    "print": x[0].print,
                    "dprod": product,
                    "djasa": jasa,
                }
            )

        self.response = response(200, "Berhasil", True, final)

        return self.response
