from sqlalchemy import and_, or_
from ..model.acq_ddb import AcqDdb
from ..model.apcard_mdb import ApCard
from ..model.dprod_ddb import DprodDdb
from ..model.exp_ddb import ExpDdb
from ..model.exp_hdb import ExpHdb
from ..model.fkpb_hdb import FkpbHdb
from ..model.fkpb_det_ddb import FkpbDetDdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.lokasi_mdb import LocationMdb
from ..model.ordpb_hdb import OrdpbHdb
from ..model.pajak_mdb import PajakMdb
from ..model.currency_mdb import CurrencyMdb
from ..model.prod_mdb import ProdMdb
from ..model.stcard_mdb import StCard
from ..model.supplier_mdb import SupplierMdb
from ..model.transddb import TransDdb
from ..model.trans_bank import TransBank
from ..model.unit_mdb import UnitMdb
from ..model.bank_mdb import BankMdb
from ..shared.shared import db


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
                    bl = ApCard.query.filter(
                        or_(
                            and_(
                                ApCard.ord_id == x[0].fk_id,
                                ApCard.trx_dbcr == "k",
                                ApCard.pay_type == "P1",
                            ),
                            # and_(
                            #     ApCard.sa_id == x[0].sa_id,
                            #     ApCard.trx_type == "SA",
                            #     ApCard.trx_dbcr == "k",
                            #     ApCard.pay_type == "P1",
                            # ),
                        )
                    ).first()

                    if bl:
                        bl.lunas = False
                        db.session.commit()

                    old_ap = ApCard.query.filter(
                        and_(ApCard.acq_id == x[0].id, ApCard.pay_type == "H4")
                    ).first()

                    if old_ap:
                        db.session.delete(old_ap)

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
                        x[1].ord_code,
                        pembelian.sup_id,
                        pembelian.fk_id,
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
                        None,
                        False,
                    )

                    db.session.add(ap_card)

                    cek_ap = ApCard.query.filter(
                        or_(
                            and_(ApCard.pay_type == "H4", ApCard.ord_id == x[1].id),
                            # and_(ApCard.pay_type == "H4", ApCard.sa_id == x[0].sa_id),
                        )
                    ).all()

                    cek_dp = ApCard.query.filter(
                        and_(
                            ApCard.po_id == x[1].po_id,
                            ApCard.pay_type == "H4",
                            ApCard.trx_type == "DP",
                        ),
                    ).all()

                    t_bayar = 0
                    t_acq = 0
                    t_acq_fc = 0
                    t_bayar_fc = 0
                    t_dp = 0
                    t_dp_fc = 0
                    t_val = 0
                    for dp in cek_dp:
                        t_dp = dp.trx_amnh if dp.trx_amnh != None else 0
                        t_dp_fc = dp.trx_amnv if dp.trx_amnv != None else 0

                    for b in cek_ap:
                        t_acq += b.acq_amnh if b.acq_amnh != None else 0
                        t_acq_fc += b.acq_amnv if b.acq_amnv != None else 0

                    t_bayar = x[0].value
                    t_bayar_fc = pembelian.trx_amnv
                    t_val = t_acq + t_dp

                    if pembelian.ord_id or pembelian.sa_id:
                        if fk[2].sup_curren == None:
                            if x[0].payment + x[0].dp >= x[0].value or t_val >= t_bayar:
                                pembelian.lunas = True
                        else:
                            if (
                                x[0].payment + x[0].dp >= pembelian.trx_amnv
                                or t_acq_fc + t_dp_fc >= t_bayar_fc
                            ):
                                pembelian.lunas = True

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

        else:

            old_trans_sup = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == exp.exp_code,
                    TransDdb.trx_dbcr == "D",
                    TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code),
                )
            ).first()

            if old_trans_sup:
                db.session.delete(old_trans_sup)

            old_trans_exp = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == exp.exp_code,
                    TransDdb.trx_dbcr == "K",
                    TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code),
                )
            ).all()

            if old_trans_exp:
                for x in old_trans_exp:
                    db.session.delete(x)

            exp_bnk = None
            if exp.exp_bnk:
                for z in bank:
                    if z.id == exp.exp_bnk:
                        exp_bnk = z.acc_id

            total = 0
            trans_exp = []
            for x in exps:
                bnk_code = None
                if x.bnk_code:
                    for z in bank:
                        if z.id == x.bnk_code:
                            bnk_code = z.acc_id

                total += x.fc
                trans_exp.append(
                    TransDdb(
                        exp.exp_code,
                        exp.exp_date,
                        x.acc_code
                        if exp.exp_type == 1
                        else x.acc_bnk
                        if exp.type_acc == 1
                        else bnk_code,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        x.fc,
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

            transbank = []

            old_trans_bank = TransBank.query.filter(
                TransBank.trx_code == exp.exp_code
            ).all()

            if old_trans_bank:
                for x in old_trans_bank:
                    db.session.delete(x)

            if exp.exp_type == 2 and exp.type_acc == 1:
                transbank.append(
                    TransBank(
                        exp.exp_code,
                        exp.exp_date,
                        exp.exp_bnk,
                        total,
                        "K",
                        "TRX %s %s" % ("K", exp.exp_code),
                        exp.user_id,
                    )
                )

            if exp.exp_type == 2 and exp.type_acc == 2:
                transbank.append(
                    TransBank(
                        exp.exp_code,
                        exp.exp_date,
                        exp.exp_bnk,
                        total,
                        "K",
                        "TRX %s %s" % ("K", exp.exp_code),
                        exp.user_id,
                    )
                )
                for x in exps:
                    transbank.append(
                        TransBank(
                            exp.exp_code,
                            exp.exp_date,
                            x.bnk_code,
                            x.fc,
                            "D",
                            "TRX %s %s" % ("D", exp.exp_code),
                            exp.user_id,
                        )
                    )

            if len(transbank) > 0:
                db.session.add_all(transbank)

        db.session.commit()
