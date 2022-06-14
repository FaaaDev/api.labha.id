import datetime
from sqlalchemy import and_
from main.model.acq_ddb import AcqDdb
from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.giro_hdb import GiroHdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class UpdateApGiro():
    def __init__(self, giro_id):

        giro = GiroHdb.query.filter(GiroHdb.id == giro_id).first()

        exp = ExpHdb.query.filter(ExpHdb.id == giro.pay_code).first()

        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp.id).all()

        for x in acq:
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
                             x.id, datetime.now(), None, "k", pembelian.trx_type, "H4", pembelian.trx_amnh, None, x.payment, None, giro.giro_num, giro.giro_date)

            db.session.add(ap_card)
            db.session.commit()

        trans_giro = TransDdb(giro.giro_num, datetime.now(), exp.bank_acc, None, None,
                            None, None, None, None, giro.value, "D", "JURNAL PENCAIRAN GIRO %s"%(giro.giro_num), None, None)

        trans_ap = TransDdb(giro.giro_num, datetime.now(), exp.bank_acc, None, None,
                            None, None, None, None, giro.value, "K", "JURNAL PENCAIRAN GIRO %s"%(giro.giro_num), None, None)

        db.session.add(trans_ap)
        db.session.add(trans_giro)
        db.session.commit()
