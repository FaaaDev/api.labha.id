from datetime import datetime
from sqlalchemy import and_
from ..model.acq_ddb import AcqDdb
from ..model.apcard_mdb import ApCard
from ..model.dprod_ddb import DprodDdb
from ..model.exp_hdb import ExpHdb
from ..model.fkpb_hdb import FkpbHdb
from ..model.fkpb_det_ddb import FkpbDetDdb
from ..model.giro_hdb import GiroHdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.lokasi_mdb import LocationMdb
from ..model.ordpb_hdb import OrdpbHdb
from ..model.prod_mdb import ProdMdb
from ..model.stcard_mdb import StCard
from ..model.transddb import TransDdb
from ..model.unit_mdb import UnitMdb
from ..shared.shared import db


class UpdateApGiro:
    def __init__(self, giro_id):

        giro = GiroHdb.query.filter(GiroHdb.id == giro_id).first()

        exp = ExpHdb.query.filter(ExpHdb.id == giro.pay_code).first()

        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp.id).all()

        for x in acq:
            fk = (
                db.session.query(FkpbDetDdb, OrdpbHdb)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
                .filter(FkpbDetDdb.ord_id == x.fk_id)
                .first()
            )

            pembelian = ApCard.query.filter(
                and_(
                    ApCard.ord_id == fk[1].id,
                    ApCard.trx_type == "LP",
                    ApCard.pay_type == "P1",
                )
            ).first()

            old_ap = ApCard.query.filter(
                and_(ApCard.acq_id == x.id, ApCard.pay_type == "H4")
            ).first()

            if old_ap:
                db.session.delete(old_ap)
                db.session.commit()

            ap_card = ApCard(
                fk[1].ord_code,
                pembelian.sup_id,
                pembelian.fk_id,
                pembelian.ord_id,
                pembelian.ord_date,
                pembelian.ord_due,
                pembelian.po_id,
                x.id,
                datetime.now(),
                None,
                "k",
                pembelian.trx_type,
                "H4",
                pembelian.trx_amnh,
                None,
                x.payment,
                None,
                giro.id,
                giro.giro_date,
                None,
                False,
            )

            db.session.add(ap_card)
            db.session.commit()

        trans_giro = TransDdb(
            giro.giro_num,
            datetime.now(),
            exp.bank_id,
            None,
            None,
            None,
            None,
            None,
            None,
            giro.value,
            "D",
            "JURNAL PENCAIRAN GIRO %s" % (giro.giro_num),
            None,
            None,
        )

        trans_ap = TransDdb(
            giro.giro_num,
            datetime.now(),
            exp.bank_id,
            None,
            None,
            None,
            None,
            None,
            None,
            giro.value,
            "K",
            "JURNAL PENCAIRAN GIRO %s" % (giro.giro_num),
            None,
            None,
        )

        db.session.add(trans_ap)
        db.session.add(trans_giro)
        db.session.commit()
