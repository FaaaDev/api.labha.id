from datetime import date, datetime
from main.model.comp_mdb import CompMdb
from main.model.accou_ddb import AccouDdb
from main.model.accou_mdb import AccouMdb
from main.model.kateg_mdb import KategMdb
from main.model.setup_mdb import SetupMdb
from main.model.pnl_mdb import PnlMdb
from main.model.transddb import TransDdb
from main.model.user import User
from main.schema.accou_ddb import AccddbSchema, accddb_schema, accddbs_schema
from main.schema.accou_mdb import AccouSchema, accou_schema
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import IntegrityError


class TransferGL:
    def __new__(self, user, request):
        try:
            trans = request.json["trans"]

            old_trans = TransDdb.query.filter(TransDdb.tf_inv == True).all()

            for x in trans:
                dt = datetime.fromisoformat(x["trx_date"])
                for y in old_trans:
                    dt_old = y.trx_date
                    if dt.month == dt_old.month and dt.year == dt_old.year:
                        db.session.delete(y)

            db.session.commit()

            ddb = []
            for x in trans:
                trx_code = x["trx_code"]
                trx_date = x["trx_date"]
                acc_id = x["acc_id"]
                ccost_id = x["ccost_id"]
                proj_id = x["proj_id"]
                acq_date = x["acq_date"]
                cur_id = x["cur_id"]
                cur_rate = x["cur_rate"]
                trx_vala = x["trx_vala"]
                trx_amnt = x["trx_amnt"]
                trx_dbcr = x["trx_dbcr"]
                trx_desc = x["trx_desc"]
                gen_post = x["gen_post"]
                post_date = x["post_date"]

                ddb.append(
                    TransDdb(
                        trx_code,
                        trx_date,
                        acc_id,
                        ccost_id,
                        proj_id,
                        acq_date,
                        cur_id,
                        cur_rate,
                        trx_vala,
                        trx_amnt,
                        trx_dbcr,
                        trx_desc,
                        gen_post,
                        post_date,
                        True,
                        user.id,
                    )
                )

            if len(ddb) > 0:
                db.session.add_all(ddb)

            db.session.commit()

            return response(200, "Berhasil", True, None)
        except Exception as e:
            db.session.rollback()
            db.session.close()
            print(e)

            return response(400, "Gagal", True, None)
