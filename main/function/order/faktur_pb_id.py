from main.function.update_faktur_pb import UpdateFakturPB
from main.model.ccost_mdb import CcostMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.inv_pb_hdb import InvpbHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.jasa_mdb import JasaMdb
from main.model.unit_mdb import UnitMdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.fkpb_det_ddb import FkpbDetDdb
from main.model.supplier_mdb import SupplierMdb
from main.schema.dord_hdb import DordSchema, dord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.prod_mdb import prod_schema
from main.schema.jasa_mdb import jasa_schema
from main.schema.unit_mdb import unit_schema
from main.schema.inv_pb_hdb import InvpbSchema, invpb_schema
from main.schema.fkpb_hdb import FkpbSchema, fkpb_schema
from main.schema.fkpb_det_ddb import fkpbd_schema
from main.schema.dprod_ddb import dprod_schema
from main.schema.djasa_ddb import djasa_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.supplier_mdb import supplier_schema


class FakturPbId:
    def __new__(self, id, request):
        fk = FkpbHdb.query.filter(FkpbHdb.id == id).first()
        if request.method == "PUT":
            fk_code = request.json["fk_code"]
            fk_date = request.json["fk_date"]
            sup_id = request.json["sup_id"]
            fk_tax = request.json["fk_tax"]
            fk_ppn = request.json["fk_ppn"]
            fk_desc = request.json["fk_desc"]
            detail = request.json["detail"]

            fk.fk_code = fk_code
            fk.fk_date = fk_date
            fk.sup_id = sup_id
            fk.fk_tax = fk_tax
            fk.fk_ppn = fk_ppn
            fk.fk_desc = fk_desc

            db.session.commit()

            UpdateFakturPB(fk.id, id, False)

            self.response = response(200, "success", True, fkpb_hdb.dump(fk))

        else:
            UpdateFakturPB(fk.id, id, True)
            det = FkpbDetDdb.query.filter(FkpbDetDdb.fk_id == fk.id).all()
            inv = InvpbHdb.query.all()
            ord = OrdpbHdb.query.all()

            for x in det:
                for i in inv:
                    if x.inv_id == i.id:
                        i.faktur = False

                for o in ord:
                    if x.ord_id == o.id:
                        o.faktur = False


                db.session.delete(x)

            db.session.delete(fk)
            db.session.commit()

            self.response = response(200, "success", True, None)

        return self.response
