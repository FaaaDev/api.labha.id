from datetime import datetime
from sqlalchemy import and_
from ..model.bank_mdb import BankMdb
from ..model.iacq_ddb import IAcqDdb
from ..model.arcard_mdb import ArCard
from ..model.dprod_ddb import DprodDdb
from ..model.inc_hdb import IncHdb
from ..model.ordpj_hdb import OrdpjHdb
from ..model.giro_inc_hdb import GiroIncHdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.lokasi_mdb import LocationMdb
from ..model.sord_hdb import SordHdb
from ..model.prod_mdb import ProdMdb
from ..model.stcard_mdb import StCard
from ..model.transddb import TransDdb
from ..model.unit_mdb import UnitMdb
from ..shared.shared import db


class UpdateArGiro:
    def __init__(self, giro_inc_id):

        giro = GiroIncHdb.query.filter(GiroIncHdb.id == giro_inc_id).first()

        inc = IncHdb.query.filter(IncHdb.id == giro.pay_code).first()

        acq = IAcqDdb.query.filter(IAcqDdb.inc_id == inc.id).all()

        if giro.bank_id:
            bank = BankMdb.query.filter(BankMdb.id == giro.bank_id).first()

        for x in acq:
            sl = (
                db.session.query(OrdpjHdb, SordHdb)
                .outerjoin(SordHdb, SordHdb.id == OrdpjHdb.so_id)
                .filter(OrdpjHdb.id == x.sale_id)
                .first()
            )

            penjualan = ArCard.query.filter(
                and_(
                    ArCard.bkt_id == sl[0].id,
                    ArCard.trx_type == "JL",
                    ArCard.pay_type == "P1",
                )
            ).first()
            old_ar = ArCard.query.filter(
                and_(ArCard.acq_id == x.id, ArCard.pay_type == "J4")
            ).first()
            if old_ar:
                db.session.delete(old_ar)
                db.session.commit()

            ar_card = ArCard(
                penjualan.cus_id,
                inc.inc_code,
                penjualan.trx_date,
                penjualan.trx_due,
                x.id,
                inc.inc_date,
                penjualan.bkt_id,
                inc.inc_date,
                None,
                "K",
                penjualan.trx_type,
                "J4",
                penjualan.trx_amnh,
                None,
                x.payment,
                None,
                None,
                None,
                None,
                giro.id,
                inc.giro_date,
                None,
                None,
                None,
                None,
                False,
            )

            db.session.add(ar_card)
            db.session.commit()

        # trans_giro = TransDdb(giro.giro_num, datetime.now(), inc.giro_bnk, None, None, None, None, None, None,
        #                     giro.value, "D", "JURNAL PELUNASAN DENGAN GIRO %s"%(giro.giro_num), None, None)

        trans_ar = TransDdb(
            giro.giro_num,
            datetime.now(),
            bank.acc_id,
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

        db.session.add(trans_ar)
        # db.session.add(trans_giro)
        db.session.commit()
