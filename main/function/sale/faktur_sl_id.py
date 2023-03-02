from main.function.update_faktur_pj import UpdateFakturPj
from main.function.update_stock import UpdateStock
from main.model.ccost_mdb import CcostMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.fkpj_hdb import FkpjHdb
from main.model.fkpj_det_ddb import FkpjDetDdb
from main.model.inv_pj_hdb import InvoicePjHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.schema.ordpj_hdb import OrdpjSchema, ordpj_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.fkpj_hdb import FkpjSchema, fkpj_schema
from main.schema.jprod_ddb import jprod_schema
from main.schema.jjasa_ddb import jjasa_schema
from main.schema.lokasi_mdb import loct_schema


class FakturPjId:
    def __new__(self, id, request):
        fk = FkpjHdb.query.filter(FkpjHdb.id == id).first()
        if request.method == "PUT":
            fk_code = request.json["fk_code"]
            fk_date = request.json["fk_date"]
            pel_id = request.json["pel_id"]
            fk_tax = request.json["fk_tax"]
            fk_ppn = request.json["fk_ppn"]
            fk_desc = request.json["fk_desc"]
            detail = request.json["detail"]

            fk.fk_code = fk_code
            fk.fk_date = fk_date
            fk.pel_id = pel_id
            fk.fk_tax = fk_tax
            fk.fk_ppn = fk_ppn
            fk.fk_desc = fk_desc

            UpdateFakturPj(fk.id, False, None, id)
            db.session.commit()

            self.response = response(200, "success", True, fkpj_schema.dump(fk))

        else:
            UpdateFakturPj(fk.id, True, None, id)
            det = FkpjDetDdb.query.filter(FkpjDetDdb.fk_id == fk.id).all()
            inv = InvoicePjHdb.query.all()
            ord = OrdpjHdb.query.all()

            for x in det:
                for i in inv:
                    if x.inv_id == i.id:
                        i.faktur = False

                for o in ord:
                    if x.sale_id == o.id:
                        o.surat_jalan = 1


                db.session.delete(x)

            db.session.delete(fk)
            db.session.commit()

            self.response = response(200, "success", True, None)

        return self.response
