from sqlalchemy import and_
from main.model.acq_ddb import AcqDdb
from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
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
    def __init__(self, exp_id):

        exp = ExpHdb.query.filter(ExpHdb.id == exp_id).first()

        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp.id).all()

        # insert kartu ap
        total = 0
        for x in acq:
            total += x.payment
            fk = (
                db.session.query(FkpbHdb, OrdpbHdb)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
                .filter(FkpbHdb.id == x.fk_id)
                .first()
            )

            pembelian = ApCard.query.filter(and_(ApCard.ord_id == fk[1].id, ApCard.trx_type == "LP", ApCard.pay_type == "P1")).first()
            old_ap = ApCard.query.filter(
                and_(ApCard.acq_id == x.id, ApCard.pay_type == "H4")).first()
            if old_ap:
                db.session.delete(old_ap)
                db.session.commit()

            ap_card = ApCard(pembelian.sup_id, pembelian.ord_id, pembelian.ord_date, pembelian.due_date, pembelian.po_id,
                             x.id, exp.exp_date, None, "k", pembelian.trx_type, "H4", pembelian.trx_amnh, None, x.payment, None, exp.giro_num, exp.giro_date)

            db.session.add(ap_card)
            db.session.commit()

        sup = (
                db.session.query(SupplierMdb, PajakMdb)
                .outerjoin(PajakMdb, PajakMdb.id == SupplierMdb.sup_ppn)
                .filter(SupplierMdb.id == exp[1].sup_id)
                .first()
            )
        # insert jurnal ap
        trans_sup = TransDdb(exp[0].exp_code, exp[0].exp_date, sup[0].sup_hutang, None, None,
                            None, None, None, None, total, "D", "JURNAL PELUNASAN %s"%(exp[0].exp_code), None, None)

        trans_exp = TransDdb(exp[0].exp_code, exp[0].exp_date, exp[0].kas_acc if exp[0].acq_pay else exp[0].bank_acc, None, None,
                            None, None, None, None, total, "K", "JURNAL PELUNASAN %s"%(exp[0].exp_code), None, None)

        db.session.add(trans_sup)
        db.session.add(trans_exp)
        db.session.commit()