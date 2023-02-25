from main.function.update_pembelian import UpdatePembelian
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


class FakturPb:
    def __new__(self, user, request):
        if request.method == "POST":
            fk_code = request.json["fk_code"]
            fk_date = request.json["fk_date"]
            sup_id = request.json["sup_id"]
            fk_tax = request.json["fk_tax"]
            fk_ppn = request.json["fk_ppn"]
            fk_desc = request.json["fk_desc"]
            detail = request.json["detail"]

            faktur = FkpbHdb(fk_code, fk_date, sup_id, fk_tax, fk_ppn, fk_desc)

            db.session.add(faktur)

            inv = InvpbHdb.query.all()

            ord = OrdpbHdb.query.all()

            new_detail = []
            for x in detail:
                if x["inv_id"] and x["total_pay"]:
                    new_detail.append(
                        FkpbDetDdb(
                            faktur.id,
                            x["inv_id"],
                            x["ord_id"],
                            x["inv_date"],
                            x["total"],
                            x["total_pay"],
                        )
                    )

                for i in inv:
                    if x["inv_id"] == i.id:
                        i.faktur = True

                for o in ord:
                    if x["ord_id"] == o.id:
                        o.faktur = True

            if len(new_detail) > 0:
                db.session.add_all(new_detail)

            UpdateFakturPB(faktur.id, user.id, False)
            db.session.commit()

            self.response = response(200, "success", True, fkpb_schema.dump(faktur))
        else:
            fk = (
                db.session.query(FkpbHdb, SupplierMdb)
                .outerjoin(SupplierMdb, SupplierMdb.id == FkpbHdb.sup_id)
                .order_by(FkpbHdb.id.desc())
                .all()
            )
            det = (
                db.session.query(FkpbDetDdb, InvpbHdb, OrdpbHdb)
                .outerjoin(InvpbHdb, InvpbHdb.id == FkpbDetDdb.inv_id)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
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
            for x in fk:
                detail = []
                if x[0]:
                    for y in det:
                        if x[0]:
                            if y[0].fk_id == x[0].id:
                                prod = []
                                for p in dprod:
                                    if y[0]:
                                        if p[0].ord_id == y[2].id:
                                            p[0].prod_id = prod_schema.dump(p[1])
                                            p[0].unit_id = unit_schema.dump(p[2])
                                            p[0].location = (
                                                loct_schema.dump(p[3])
                                                if p[0].location
                                                else None
                                            )
                                            prod.append(dprod_schema.dump(p[0]))

                                jasa = []
                                for z in djasa:
                                    if y[0]:
                                        if z[0].ord_id == y[2].id:
                                            z[0].jasa_id = jasa_schema.dump(z[1])
                                            z[0].unit_id = unit_schema.dump(z[2])
                                            jasa.append(djasa_schema.dump(z[0]))

                                y[0].inv_id = invpb_schema.dump(y[1])
                                # y[0].ord_id = dord_schema.dump(y[2])
                                y[0].ord_id = {
                                    "id": y[2].id,
                                    "ord_code": y[2].ord_code,
                                    "ord_date": y[2].ord_date.isoformat(),
                                    "invoice": y[2].invoice,
                                    "faktur": y[2].faktur,
                                    "po_id": y[2].po_id,
                                    "dep_id": y[2].dep_id,
                                    "sup_id": y[2].sup_id,
                                    "due_date": y[2].due_date.isoformat(),
                                    "product": prod,
                                    "jasa": jasa,
                                }
                                detail.append(fkpbd_schema.dump(y[0]))

                        # if y[0].fk_id == x[0].id:

                final.append(
                    {
                        "id": x[0].id,
                        "fk_code": x[0].fk_code,
                        "fk_date": x[0].fk_date.isoformat(),
                        "sup_id": supplier_schema.dump(x[1]),
                        "fk_tax": x[0].fk_tax,
                        "fk_ppn": x[0].fk_ppn,
                        "fk_lunas": x[0].fk_lunas,
                        "fk_desc": x[0].fk_desc,
                        "post": x[0].post,
                        "closing": x[0].closing,
                        "detail": detail,
                        # "product": prod,
                        # "jasa": jasa,
                    }
                )

            self.response = response(200, "success", True, final)

        return self.response
