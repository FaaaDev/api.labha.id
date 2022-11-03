from sqlalchemy import and_
from main.model.acq_ddb import AcqDdb
from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
from ..model.exp_ddb import ExpDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class UpdateApPayment():
    def __init__(self, exp_id, delete):

        exp = ExpHdb.query.filter(ExpHdb.id == exp_id).first()

        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp.id).all()

        exps = ExpDdb.query.filter(ExpDdb.exp_id == exp.id).all()

        # insert kartu ap
        total = 0
        if exp.exp_type == 1:
            for x in acq:
                if delete:
                    old_ap = ApCard.query.filter(
                        and_(ApCard.acq_id == x.id, ApCard.pay_type == "H4")).first()
                    if old_ap:
                        db.session.delete(old_ap)
                        db.session.commit()
                else:
                    total += x.payment
                    fk = (
                        db.session.query(FkpbHdb, OrdpbHdb)
                        .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
                        .filter(FkpbHdb.id == x.fk_id)
                        .first()
                    )

                    pembelian = ApCard.query.filter(and_(
                        ApCard.ord_id == fk[1].id, ApCard.trx_type == "LP", ApCard.pay_type == "P1")).first()
                    old_ap = ApCard.query.filter(
                        and_(ApCard.acq_id == x.id, ApCard.pay_type == "H4")).first()
                    if old_ap:
                        db.session.delete(old_ap)
                        db.session.commit()

                    ap_card = ApCard(pembelian.sup_id, pembelian.ord_id, pembelian.ord_date, pembelian.ord_due, pembelian.po_id,
                                     x.id, exp.exp_date, None, "k", pembelian.trx_type, "H4", pembelian.trx_amnh, None, x.payment, None, exp.giro_num, exp.giro_date)

                    db.session.add(ap_card)
                    db.session.commit()

        if delete:
            old_trans_sup = TransDdb.query.filter(and_(
                TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code))).first()
            old_trans_exp = TransDdb.query.filter(and_(
                TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code))).first()
            if old_trans_sup:
                db.session.delete(old_trans_sup)
            if old_trans_sup:
                db.session.delete(old_trans_exp)

        else:
            if exp.exp_type == 1:
                old_trans_sup = TransDdb.query.filter(and_(
                    TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code))).first()
                old_trans_exp = TransDdb.query.filter(and_(
                    TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PELUNASAN %s" % (exp.exp_code))).first()
                if old_trans_sup:
                    db.session.delete(old_trans_sup)
                if old_trans_sup:
                    db.session.delete(old_trans_exp)

                db.session.commit()

                sup = (
                    db.session.query(SupplierMdb, PajakMdb)
                    .outerjoin(PajakMdb, PajakMdb.id == SupplierMdb.sup_ppn)
                    .filter(SupplierMdb.id == exp.acq_sup)
                    .first()
                )
                # insert jurnal ap
                trans_sup = TransDdb(exp.exp_code, exp.exp_date, sup[0].sup_hutang, None, None,
                                     None, None, None, None, total, "D", "JURNAL PELUNASAN %s" % (exp.exp_code), None, None)

                trans_exp = TransDdb(exp.exp_code, exp.exp_date, exp.kas_acc if exp.acq_pay else exp.bank_acc, None, None,
                                     None, None, None, None, total, "K", "JURNAL PELUNASAN %s" % (exp.exp_code), None, None)

                db.session.add(trans_sup)
                db.session.add(trans_exp)
                db.session.commit()
            else:
                old_trans_sup = TransDdb.query.filter(and_(
                    TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code))).first()
                old_trans_exp = TransDdb.query.filter(and_(
                    TransDdb.trx_code == exp.exp_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PENGELUARAN %s" % (exp.exp_code))).all()
                if old_trans_sup:
                    db.session.delete(old_trans_sup)
                if old_trans_sup:
                    for x in old_trans_sup:
                        db.session.delete(x)

                db.session.commit()

                total = 0
                trans_exp = []
                for x in exps:
                    total += x.value
                    trans_exp.append(TransDdb(exp.exp_code, exp.exp_date, x.acc_code, None, None,
                                              None, None, None, None, x.value, "D", "JURNAL PENGELUARAN %s" % (exp.exp_code), None, None))

                # insert jurnal ap
                trans_sup = TransDdb(exp.exp_code, exp.exp_date, exp.exp_acc, None, None,
                                     None, None, None, None, total, "K", "JURNAL PENGELUARAN %s" % (exp.exp_code), None, None)

                db.session.add(trans_sup)
                db.session.add_all(trans_exp)
                db.session.commit()
