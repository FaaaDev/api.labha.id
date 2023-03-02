from sqlalchemy import and_, or_
from main.model.acq_ddb import AcqDdb
from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
from ..model.exp_ddb import ExpDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.fkpb_det_ddb import FkpbDetDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.bank_mdb import BankMdb
from main.shared.shared import db


class UpdateApPayment:
    def __init__(self, exp_id, delete):

        exp = ExpHdb.query.filter(ExpHdb.id == exp_id).first()

        acq = (
            db.session.query(AcqDdb, OrdpbHdb)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == AcqDdb.fk_id)
            .filter(AcqDdb.exp_id == exp.id)
            .all()
        )

        exps = ExpDdb.query.filter(ExpDdb.exp_id == exp.id).all()

        bank = BankMdb.query.all()

        old_trans = TransDdb.query.filter(TransDdb.trx_code == exp.exp_code).all()

        # insert kartu ap
        if exp.type_trx == 1 and exp.acq_pay != 3:
            if delete:
                for x in acq:
                    old_ap = ApCard.query.filter(
                        and_(ApCard.acq_id == x[0].id, ApCard.pay_type == "H4")
                    ).first()

                    if old_ap:
                        db.session.delete(old_ap)
                        db.session.commit()

            else:
                total = 0
                for x in acq:
                    total += x[0].payment

                    fk = (
                        db.session.query(
                            FkpbHdb,
                            OrdpbHdb,
                            SupplierMdb,
                            CurrencyMdb,
                            FkpbDetDdb,
                        )
                        .outerjoin(FkpbDetDdb, FkpbDetDdb.fk_id == FkpbHdb.id)
                        .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
                        .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                        .outerjoin(
                            CurrencyMdb, CurrencyMdb.id == SupplierMdb.sup_curren
                        )
                        .filter(
                            or_(FkpbHdb.id == x[0].fk_id, SupplierMdb.id == exp.acq_sup)
                        )
                        .first()
                    )

                    pembelian = ApCard.query.filter(
                        and_(
                            ApCard.ord_id == x[1].id,
                            ApCard.trx_type == "LP",
                            ApCard.pay_type == "P1",
                        )
                    ).first()

                    old_ap = ApCard.query.filter(
                        and_(ApCard.acq_id == x[0].id, ApCard.pay_type == "H4")
                    ).first()

                    if old_ap:
                        db.session.delete(old_ap)

                    ap_card = ApCard(
                        pembelian.sup_id,
                        pembelian.ord_id,
                        pembelian.ord_date,
                        pembelian.ord_due,
                        pembelian.po_id,
                        x[0].id,
                        exp.exp_date,
                        fk[2].sup_curren,
                        "d",
                        pembelian.trx_type,
                        "H4",
                        pembelian.trx_amnh,
                        pembelian.trx_amnv if fk[2].sup_curren != None else None,
                        x[0].payment * fk[3].rate
                        if fk[2].sup_curren != None
                        else x[0].payment,
                        x[0].payment if fk[2].sup_curren != None else 0,
                        exp.giro_num,
                        exp.giro_date,
                    )

                    db.session.add(ap_card)

                    # insert jurnal ap
                    bank_acc = None
                    if exp.bank_acc:
                        for y in bank:
                            if y.id == exp.bank_acc:
                                bank_acc = y.acc_id

                    total_fc = 0
                    total_fc = total * fk[3].rate if fk[2].sup_curren != None else total

                    if old_trans:
                        for d in old_trans:
                            db.session.delete(d)

                    if exp.type_trx == 1:
                        if exp.acq_pay != 3:
                            trans_sup = TransDdb(
                                exp.exp_code,
                                exp.exp_date,
                                fk[2].sup_hutang,
                                None,
                                None,
                                None,
                                pembelian.cur_conv,
                                None,
                                pembelian.trx_amnv if fk[2].sup_curren != None else 0,
                                pembelian.trx_amnh,
                                "D",
                                "JURNAL PELUNASAN HUTANG %s" % (exp.exp_code),
                                None,
                                None,
                            )

                            if x[0].dp > 0:
                                trans_dp = TransDdb(
                                    exp.exp_code,
                                    exp.exp_date,
                                    fk[2].sup_uang_muka,
                                    None,
                                    None,
                                    None,
                                    fk[2].sup_curren,
                                    fk[3].rate if fk[2].sup_curren != None else 0,
                                    x[0].dp / fk[3].rate
                                    if fk[2].sup_curren != None
                                    else 0,
                                    x[0].dp,
                                    "K",
                                    "JURNAL UANG MUKA ATAS PELUNASAN %s"
                                    % (exp.exp_code),
                                    None,
                                    None,
                                )

                                db.session.add(trans_dp)

                            if fk[2].sup_curren != None:
                                trans_kurs = TransDdb(
                                    exp.exp_code,
                                    exp.exp_date,
                                    setup.selisih_kurs,
                                    None,
                                    None,
                                    None,
                                    fk[2].sup_curren,
                                    fk[3].rate if fk[2].sup_curren != None else 0,
                                    abs(pembelian.trx_amnh - total_fc) / fk[3].rate,
                                    abs(pembelian.trx_amnh - total_fc),
                                    "K" if total_fc - pembelian.trx_amnh < 0 else "D",
                                    "JURNAL PELUNASAN SELISIH KURS %s" % (exp.exp_code),
                                    None,
                                    None,
                                )

                                db.session.add(trans_kurs)

                            db.session.add(trans_sup)

                if exp.type_trx == 1:
                    if exp.acq_pay != 3:
                        trans_exp = TransDdb(
                            exp.exp_code,
                            exp.exp_date,
                            exp.acq_kas if exp.acq_pay == 1 else bank_acc,
                            None,
                            None,
                            None,
                            fk[2].sup_curren,
                            fk[3].rate if fk[2].sup_curren != None else 0,
                            total if fk[2].sup_curren != None else 0,
                            total_fc if fk[2].sup_curren != None else total,
                            "K",
                            "JURNAL PELUNASAN %s" % (exp.exp_code),
                            None,
                            None,
                        )

                        db.session.add(trans_exp)

        # if delete:
        #     old_trans_sup = TransDdb.query.filter(
        #         and_(
        #             TransDdb.trx_code == exp.exp_code,
        #             TransDdb.trx_dbcr == "D",
        #             TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code),
        #         )
        #     ).first()
        #     old_trans_exp = TransDdb.query.filter(
        #         and_(
        #             TransDdb.trx_code == exp.exp_code,
        #             TransDdb.trx_dbcr == "K",
        #             TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code),
        #         )
        #     ).first()
        #     if old_trans_sup:
        #         db.session.delete(old_trans_sup)
        #     if old_trans_sup:
        #         db.session.delete(old_trans_exp)

        else:

            old_trans_sup = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == exp.exp_code,
                    TransDdb.trx_dbcr == "D",
                    TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code),
                )
            ).first()

            old_trans_exp = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == exp.exp_code,
                    TransDdb.trx_dbcr == "K",
                    TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code),
                )
            ).all()

            if old_trans_sup:
                db.session.delete(old_trans_sup)
            if old_trans_sup:
                for x in old_trans_sup:
                    db.session.delete(x)

            exp_bnk = None
            if exp.exp_bnk:
                for z in bank:
                    if z.id == exp.exp_bnk:
                        exp_bnk = z.acc_id

            total = 0
            trans_exp = []
            for x in exps:
                total += x.value
                trans_exp.append(
                    TransDdb(
                        exp.exp_code,
                        exp.exp_date,
                        x.acc_code
                        if exp.exp_type == 1
                        else x.acc_bnk
                        if exp.acc_type == 1
                        else bnk_code,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        x.value,
                        "D",
                        "JURNAL PENGELUARAN %s" % (exp.exp_code),
                        None,
                        None,
                    )
                )

                if len(trans_exp) > 0:
                    db.session.add_all(trans_exp)

            # insert jurnal ap
            trans_sup = TransDdb(
                exp.exp_code,
                exp.exp_date,
                exp.kas_acc if exp.exp_type == 1 else exp_bnk,
                None,
                None,
                None,
                None,
                None,
                None,
                total,
                "K",
                "JURNAL PENGELUARAN %s" % (exp.exp_code),
                None,
                None,
            )

            db.session.add(trans_sup)

            # transbank = []
            # if exp.exp_type == 2 and exp.type_acc == 1:
            #     transbank.append(
            #         {
            #             "trx_code": exp.exp_code,
            #             "trx_date": exp.exp_date.isoformat(),
            #             "bank_id": exp.exp_bnk,
            #             "trx_amnt": total,
            #             "trx_dbcr": "K",
            #             "trx_desc": "TRX %s %s" % ("K", exp.exp_code),
            #         }
            #     )

            # if exp.exp_type == 2 and exp.type_acc == 2:
            #     transbank.append(
            #         {
            #             "trx_code": exp.exp_code,
            #             "trx_date": exp.exp_date.isoformat(),
            #             "bank_id": exp.exp_bnk,
            #             "trx_amnt": total,
            #             "trx_dbcr": "K",
            #             "trx_desc": "TRX %s %s" % ("K", exp.exp_code),
            #         }
            #     )
            #     for x in exps:
            #         transbank.append(
            #             {
            #                 "trx_code": exp.exp_code,
            #                 "trx_date": exp.exp_date.isoformat(),
            #                 "bank_id": x.bnk_code,
            #                 "trx_amnt": x.fc,
            #                 "trx_dbcr": "D",
            #                 "trx_desc": "TRX %s %s" % ("D", exp.exp_code),
            #             }
            #         )

        db.session.commit()
