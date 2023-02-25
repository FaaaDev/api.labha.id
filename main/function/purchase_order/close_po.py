from main.model.pjasa_ddb import PjasaDdb
from main.model.po_mdb import PoMdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.po_mdb import PoSchema, po_schema


class PurchaseOrderClose:
    def __new__(self, id, request):
        po = PoMdb.query.filter(PoMdb.id == id).first()
        if request.method == "PUT":
            if po.print == 0 and po.status != 2:
                try:
                    po_code = request.json["po_code"]
                    po_date = request.json["po_date"]
                    preq_id = request.json["preq_id"]
                    sup_id = request.json["sup_id"]
                    ref_sup = request.json["ref_sup"]
                    ppn_type = request.json["ppn_type"]
                    top = request.json["top"]
                    due_date = request.json["due_date"]
                    split_inv = request.json["split_inv"]
                    prod_disc = request.json["prod_disc"]
                    jasa_disc = request.json["jasa_disc"]
                    total_disc = request.json["total_disc"]
                    total_bayar = request.json["total_bayar"]
                    pprod = request.json["pprod"]
                    pjasa = request.json["pjasa"]

                    po.po_code = po_code
                    po.po_date = po_date
                    po.preq_id = preq_id
                    po.sup_id = sup_id
                    po.ref_sup = ref_sup
                    po.ppn_type = ppn_type
                    po.top = top
                    po.due_date = due_date
                    po.split_inv = split_inv
                    po.prod_disc = prod_disc
                    po.jasa_disc = jasa_disc
                    po.total_disc = total_disc
                    po.total_bayar = total_bayar
                    po.status = 2

                    db.session.commit()

                    result = response(200, "Berhasil", True, po_schema.dump(po))
                
                finally:
                    self.response = result

        return self.response
