from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
from main.model.exp_hdb import ExpHdb
from main.model.mukap_ddb import MukapDdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.po_mdb import PoMdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
# from main.model.trans_bank import TransBank
from main.model.unit_mdb import UnitMdb
from main.model.bank_mdb import BankMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.user import User
from main.model.setup_mdb import SetupMdb
# from main.model.sa_ap_mdb import SaldoAPMdb
from main.model.prod_mdb import ProdMdb
from main.shared.shared import db
import requests
import json
from sqlalchemy import and_, extract, func, or_, cast, case, literal_column


class UpdateApDP:
    def __init__(self, exp_id, delete):

        exp = (
            db.session.query(ExpHdb, SupplierMdb, CurrencyMdb)
            .outerjoin(SupplierMdb, SupplierMdb.id == ExpHdb.dp_sup)
            .outerjoin(CurrencyMdb, CurrencyMdb.id == SupplierMdb.sup_curren)
            .filter(ExpHdb.id == exp_id)
            .first()
        )

        dp = (
            db.session.query(MukapDdb, PoMdb)
            .outerjoin(PoMdb, PoMdb.id == MukapDdb.po_id)
            .filter(MukapDdb.exp_id == exp[0].id)
            .all()
        )

        bank = BankMdb.query.all()

        # insert kartu ap

        if delete:
            for x in dp:
                old_ap = ApCard.query.filter(
                    and_(
                        ApCard.po_id == x[0].po_id,
                        ApCard.trx_type == "DP",
                        ApCard.pay_type == "H4",
                    )
                ).first()
                if old_ap:
                    db.session.delete(old_ap)

                old_trans = TransDdb.query.filter(
                    and_(
                        TransDdb.trx_code == exp[0].exp_code,
                        TransDdb.trx_desc
                        == "JURNAL UANG MUKA ATAS %s" % (x[1].po_code),
                    ),
                ).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

        else:
            total = 0
            for x in dp:
                total += x[0].value

                old_ap = ApCard.query.filter(
                    and_(
                        ApCard.po_id == x[1].id,
                        ApCard.trx_type == "DP",
                        ApCard.pay_type == "H4",
                    )
                ).first()

                if old_ap:
                    db.session.delete(old_ap)

                ap_card = []
                ap_card.append(
                    ApCard(
                        exp[0].dp_sup,
                        None,
                        exp[0].exp_date,
                        x[1].due_date,
                        x[0].po_id,
                        None,
                        None,
                        exp[1].sup_curren,
                        "d",
                        "DP",
                        "H4",
                        x[0].value,
                        x[0].value / exp[2].rate if exp[1].sup_curren != None else None,
                        None,
                        None,
                        None,
                        None,
                    )
                )

                if len(ap_card) > 0:
                    db.session.add_all(ap_card)

            dp_bnk = None
            if exp[0].dp_bnk:
                for y in bank:
                    if y.id == exp[0].dp_bnk:
                        dp_bnk = y.acc_id

            # insert jurnal ap

            old_trn = TransDdb.query.filter(
                TransDdb.trx_code == exp[0].exp_code
            ).first()

            if old_trn:
                db.session.delete(old_trn)

            print("===================")
            print(total)
            print("===================")

            trans_dp_d = []
            trans_dp_d.append(
                TransDdb(
                    exp[0].exp_code,
                    exp[0].exp_date,
                    exp[1].sup_uang_muka,
                    None,
                    None,
                    None,
                    exp[1].sup_curren,
                    exp[2].rate if exp[1].sup_curren != None else None,
                    total / exp[2].rate if exp[1].sup_curren != None else 0,
                    total,
                    "D",
                    "JURNAL UANG MUKA ATAS %s" % (exp[1].sup_name),
                    None,
                    None,
                )
            )

            if len(trans_dp_d) > 0:
                db.session.add_all(trans_dp_d)

            trans_dp_k = []
            trans_dp_k.append(
                TransDdb(
                    exp[0].exp_code,
                    exp[0].exp_date,
                    exp[0].dp_kas if exp[0].dp_type == 1 else dp_bnk,
                    None,
                    None,
                    None,
                    exp[1].sup_curren,
                    exp[2].rate if exp[1].sup_curren != None else None,
                    total / exp[2].rate if exp[1].sup_curren != None else 0,
                    total,
                    "K",
                    "JURNAL UANG MUKA ATAS %s" % (exp[1].sup_name),
                    None,
                    None,
                )
            )

            if len(trans_dp_k) > 0:
                db.session.add_all(trans_dp_k)

        db.session.commit()
