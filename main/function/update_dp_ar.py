from main.model.arcard_mdb import ArCard
from main.model.inc_hdb import IncHdb
from main.model.mukar_ddb import MukarDdb
from main.model.sord_hdb import SordHdb
from main.model.prod_mdb import ProdMdb
from main.model.custom_mdb import CustomerMdb
from main.model.transddb import TransDdb
from main.model.bank_mdb import BankMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.user import User
from main.model.setup_mdb import SetupMdb
from main.shared.shared import db
import requests
import json
from sqlalchemy import and_, extract, func, or_, cast, case, literal_column


class UpdateArDP:
    def __init__(self, inc_id, delete):

        inc = (
            db.session.query(IncHdb, CustomerMdb, CurrencyMdb)
            .outerjoin(CustomerMdb, CustomerMdb.id == IncHdb.dp_cus)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == CustomerMdb.cus_curren)
            .filter(IncHdb.id == inc_id)
            .first()
        )

        dp = (
            db.session.query(MukarDdb, SordHdb)
            .outerjoin(SordHdb, SordHdb.id == MukarDdb.so_id)
            .filter(MukarDdb.inc_id == inc[0].id)
            .all()
        )

        bank = BankMdb.query.all()

        # insert kartu ap
        if delete:
            for x in dp:
                old_ar = ArCard.query.filter(
                    and_(
                        ArCard.so_id == x[0].so_id,
                        ArCard.trx_type == "DP",
                        ArCard.pay_type == "J4",
                    )
                ).first()
                if old_ar:
                    db.session.delete(old_ar)

                old_trans = TransDdb.query.filter(
                    and_(
                        TransDdb.trx_code == inc[0].inc_code,
                        TransDdb.trx_desc
                        == "JURNAL UANG MUKA ATAS %s" % (x[1].so_code),
                    ),
                ).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

        else:
            total = 0

            for x in dp:
                total += x[0].value

                old_ar = ArCard.query.filter(
                    and_(
                        ArCard.so_id == x[1].id,
                        ArCard.trx_type == "DP",
                        ArCard.pay_type == "J4",
                    )
                ).first()

                if old_ar:
                    db.session.delete(old_ar)

                ar_card = []
                ar_card.append(
                    ArCard(
                        inc[0].dp_cus,
                        inc[0].inc_code,
                        inc[0].inc_date,
                        x[1].due_date,
                        None,
                        None,
                        None,
                        None,
                        inc[1].cus_curren,
                        # inc[2].rate if inc[1].cus_curren != None else None,
                        "K",
                        "DP",
                        "J4",
                        x[0].value,
                        x[0].value / inc[2].rate if inc[1].cus_curren else 0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        x[1].id,
                        None,
                    )
                )

                if len(ar_card) > 0:
                    db.session.add_all(ar_card)

            dp_bnk = None
            if inc[0].dp_bnk:
                for y in bank:
                    if y.id == inc[0].dp_bnk:
                        dp_bnk = y.acc_id

            # insert jurnal ap

            old_trn = TransDdb.query.filter(
                TransDdb.trx_code == inc[0].inc_code
            ).first()

            if old_trn:
                db.session.delete(old_trn)

            trans_dp_d = []
            trans_dp_d.append(
                TransDdb(
                    inc[0].inc_code,
                    inc[0].inc_date,
                    inc[1].cus_uang_muka,
                    None,
                    None,
                    None,
                    inc[1].cus_curren,
                    inc[2].rate if inc[1].cus_curren != None else None,
                    total / inc[2].rate if inc[1].cus_curren != None else 0,
                    total,
                    "K",
                    "JURNAL UANG MUKA ATAS %s" % (x[1].so_code),
                    None,
                    None,
                )
            )

            trans_dp_k = []
            trans_dp_k.append(
                TransDdb(
                    inc[0].inc_code,
                    inc[0].inc_date,
                    inc[0].dp_kas if inc[0].dp_type == 1 else dp_bnk,
                    None,
                    None,
                    None,
                    inc[1].cus_curren,
                    inc[2].rate if inc[1].cus_curren != None else None,
                    total / inc[2].rate if inc[1].cus_curren != None else 0,
                    total,
                    "D",
                    "JURNAL UANG MUKA ATAS %s" % (x[1].so_code),
                    None,
                    None,
                )
            )

            if len(trans_dp_d) > 0:
                db.session.add_all(trans_dp_d)

            if len(trans_dp_k) > 0:
                db.session.add_all(trans_dp_k)

        db.session.commit()
