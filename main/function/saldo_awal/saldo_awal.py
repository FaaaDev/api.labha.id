# from ...function.posting.posting_year import GetYearPosting
from ...function.update_table import UpdateTable
from ...model.akhir_mdb import AkhirMdb
from ...model.comp_mdb import CompMdb
from ...model.inv_ddb import InvDdb
from ...model.lokasi_mdb import LocationMdb
from ...model.group_prod_mdb import GroupProMdb
from ...model.prod_mdb import ProdMdb
from ...model.sa_inv import SaldoInvMdb
from ...model.stcard_mdb import StCard
from ...model.user import User
from ...schema.sa_inv import sainv_schema
from ...schema.lokasi_mdb import loct_schema
from ...schema.prod_mdb import prod_schema
from ...schema.group_prod_mdb import groupPro_schema
from ...shared.shared import db
from ...utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import *


class SaldoInv:
    def __new__(self, user, request):
        if request.method == "POST":
            try:
                loc_id = request.json["loc_id"]
                prod_id = request.json["prod_id"]
                qty = request.json["qty"]
                nilai = request.json["nilai"]
                total = request.json["total"]

                sa = SaldoInvMdb(loc_id, prod_id, qty, nilai, total, user.id)

                cp = CompMdb.query.filter(CompMdb.id == user.company).first()

                today = date.today()

                inv_ddb = InvDdb(
                    cp.year_co,
                    cp.cutoff,
                    prod_id,
                    loc_id,
                    total,
                    0,
                    0,
                    total,
                    qty,
                    0,
                    0,
                    qty,
                    nilai,
                    True,
                    False,
                    user.id,
                )

                krtst = StCard(
                    "SA-%s %s" % (prod_id, loc_id),
                    today,
                    "d",
                    "SA",
                    None,
                    qty,
                    None,
                    None,
                    total,
                    None,
                    None,
                    prod_id,
                    loc_id,
                    None,
                    0,
                    None,
                )

                db.session.add(sa)
                db.session.add(inv_ddb)
                db.session.add(krtst)
                db.session.commit()

            except Exception as e:
                print(e)
                db.session.rollback()
                db.session.close()
                return response(400, "Kode sudah digunakan", False, None)
            finally:
                return response(200, "Berhasil", True, sainv_schema.dump(sa))
        else:
            try:
                sld = (
                    db.session.query(SaldoInvMdb, LocationMdb, ProdMdb, GroupProMdb)
                    .outerjoin(LocationMdb, LocationMdb.id == SaldoInvMdb.loc_id)
                    .outerjoin(ProdMdb, ProdMdb.id == SaldoInvMdb.prod_id)
                    .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                    .order_by(SaldoInvMdb.id.desc())
                    .all()
                )

                # sa = []
                # for x in sld:
                #     sa.append(
                #         InvDdb(
                #             2022,
                #             10,
                #             x[2].id,
                #             x[1].id,
                #             x[0].total,
                #             0,
                #             0,
                #             x[0].total,
                #             x[0].qty,
                #             0,
                #             0,
                #             x[0].qty,
                #             x[0].nilai,
                #             True,
                #             False,
                #             user.id,
                #         )
                #     )

                # db.session.add_all(sa)
                # db.session.commit()

                final = []
                for x in sld:
                    final.append(
                        {
                            "id": x[0].id,
                            "loc_id": loct_schema.dump(x[1]),
                            "prod_id": prod_schema.dump(x[2]),
                            "qty": x[0].qty,
                            "nilai": x[0].nilai,
                            "total": x[0].total,
                            "user_id": x[0].user_id,
                        }
                    )

                return response(200, "Berhasil", True, final)
            except ProgrammingError as e:
                print(e)
                return UpdateTable(
                    [
                        SaldoInvMdb,
                        LocationMdb,
                        ProdMdb,
                        GroupProMdb,
                        StCard,
                        InvDdb,
                        CompMdb,
                    ],
                    request,
                )
