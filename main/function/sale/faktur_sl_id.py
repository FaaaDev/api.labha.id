from ...function.update_faktur_pj import UpdateFakturPj
from ...function.update_stock import UpdateStock
from ...model.ccost_mdb import CcostMdb
from ...model.jjasa_ddb import JjasaDdb
from ...model.jprod_ddb import JprodDdb
from ...model.fkpj_hdb import FkpjHdb
from ...model.fkpj_det_ddb import FkpjDetDdb
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
from ...schema.fkpj_hdb import FkpjSchema, fkpj_schema
from ...schema.jprod_ddb import jprod_schema
from ...schema.jjasa_ddb import jjasa_schema
from ...schema.lokasi_mdb import loct_schema


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
