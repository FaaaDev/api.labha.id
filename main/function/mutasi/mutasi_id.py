from main.function.update_mutasi import UpdateMutasi
from main.model.ccost_mdb import CcostMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.mtsi_hdb import MtsiHdb
from main.model.prod_mdb import ProdMdb
from main.model.proj_mdb import ProjMdb
from main.model.unit_mdb import UnitMdb
from main.model.mtsi_ddb import MtsiDdb
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError
from main.schema.mtsi_hdb import MtsiSchema, mtsi_schema
from main.schema.mtsi_ddb import mtsiddb_schema
from main.schema.prod_mdb import prod_schema
from main.schema.unit_mdb import unit_schema
from main.schema.proj_mdb import proj_schema
from main.schema.lokasi_mdb import loct_schema
from main.schema.ccost_mdb import ccost_schema


class MutasiId:
    def __new__(self, id, request):
        mut = MtsiHdb.query.filter(MtsiHdb.id == id).first()
        if request.method == "PUT":
            try:
                mtsi_code = request.json["mtsi_code"]
                mtsi_date = request.json["mtsi_date"]
                loc_from = request.json["loc_from"]
                loc_to = request.json["loc_to"]
                dep_id = request.json["dep_id"]
                prj_id = request.json["prj_id"]
                doc = request.json["doc"]
                doc_date = request.json["doc_date"]
                desc = request.json["desc"]
                approve = request.json["approve"]
                mt = request.json["mutasi"]

                mut.mtsi_code = mtsi_code
                mut.mtsi_date = mtsi_date
                mut.loc_from = loc_from
                mut.loc_to = loc_to
                mut.dep_id = dep_id
                mut.prj_id = prj_id
                mut.doc = doc
                mut.doc_date = doc_date
                mut.desc = desc
                mut.approve = approve

                db.session.commit()

                o_mutasi = MtsiDdb.query.filter(MtsiDdb.mtsi_id == id).all()

                old_mut = []
                new_mutasi = []
                for m in mt:
                    if m["id"]:
                        if m["prod_id"] and m["qty"] and m["unit_id"]:
                            old_mut.append(m["id"])
                    else:
                        if m["prod_id"] and m["qty"] and m["unit_id"]:
                            new_mutasi.append(
                                MtsiDdb(
                                    x.id,
                                    m["prod_id"],
                                    m["unit_id"],
                                    m["qty"],
                                    m["qty_terima"],
                                )
                            )

                if len(old_mut) > 0:
                    for x in old_mut:
                        for y in o_mutasi:
                            if y.id not in old_mut:
                                db.session.delete(y)
                            else:
                                if y.id == x:
                                    for z in mt:
                                        if z["id"] == x:
                                            y.prod_id = z["prod_id"]
                                            y.unit_id = z["unit_id"]
                                            y.qty = z["qty"]
                                            y.qty_terima = z["qty_terima"]

                if len(new_mutasi) > 0:
                    db.session.add_all(new_mutasi)

                if mut.approve:
                    UpdateMutasi(id, False)

                db.session.commit()
                result = response(200, "Berhasil", True, mtsi_schema.dump(mut))
            except IntegrityError:
                db.session.rollback()
                result = response(
                    400, "Tidak dapat mengedit data karena status", False, None
                )
            finally:
                self.response = result
        else:
            
            if mut.approve:
                UpdateMutasi(mut.id, True)

            old_mutasi = MtsiDdb.query.filter(MtsiDdb.mtsi_id == id).all()
            if old_mutasi:
                for y in old_mutasi:
                    db.session.delete(y)

            db.session.delete(mut)
            db.session.commit()

            self.response = response(200, "Berhasil", True, None)

        return self.response
