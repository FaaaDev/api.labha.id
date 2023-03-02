from main.model.custom_mdb import CustomerMdb
from main.model.sord_hdb import SordHdb
from main.schema.sord_hdb import SordSchema, sord_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError


class SalesOrderClose:
    def __new__(self, id, request):
        so = SordHdb.query.filter(SordHdb.id == id).first()
        if request.method == "PUT":
            try:
                so_code = request.json["so_code"]
                so_date = request.json["so_date"]
                pel_id = request.json["pel_id"]
                ppn_type = request.json["ppn_type"]
                sub_addr = request.json["sub_addr"]
                sub_id = request.json["sub_id"]
                req_date = request.json["req_date"]
                top = request.json["top"]
                due_date = request.json["due_date"]
                split_inv = request.json["split_inv"]
                prod_disc = request.json["prod_disc"]
                jasa_disc = request.json["jasa_disc"]
                total_disc = request.json["total_disc"]
                status = request.json["status"]
                sprod = request.json["sprod"]
                sjasa = request.json["sjasa"]

                so.so_code = so_code
                so.so_date = so_date
                so.pel_id = pel_id
                so.ppn_type = ppn_type
                so.sub_addr = sub_addr
                so.sub_id = sub_id
                so.req_date = req_date
                so.top = top
                so.due_date = due_date
                so.split_inv = split_inv
                so.prod_disc = prod_disc
                so.jasa_disc = jasa_disc
                so.total_disc = total_disc
                so.status = 2

               

                db.session.commit()

                result = response(200, "Berhasil", True, sord_schema.dump(so))

            finally:
                self.response = result

        return self.response
