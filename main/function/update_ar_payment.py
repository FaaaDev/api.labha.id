from sqlalchemy import and_
from main.model.iacq_ddb import IAcqDdb
from main.model.arcard_mdb import ArCard
from main.model.dprod_ddb import DprodDdb
from ..model.dinc_ddb import IncDdb
from main.model.inc_hdb import IncHdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.sord_hdb import SordHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class UpdateArPayment():
    def __init__(self, inc_id, delete):

        inc = IncHdb.query.filter(IncHdb.id == inc_id).first()

        acq = IAcqDdb.query.filter(IAcqDdb.inc_id == inc.id).all()

        incs = IncDdb.query.filter(IncDdb.inc_id == inc.id).all()

        # insert kartu ar
        total = 0
        if inc.inc_type == 1:
            for x in acq:
                if delete:
                    old_ar = ArCard.query.filter(
                    and_(ArCard.acq_id == x.id, ArCard.pay_type == "J4")).first()
                    if old_ar:
                        db.session.delete(old_ar)
                        db.session.commit()
                else:
                    total += x.payment
                    sl = OrdpjHdb.query.filter(OrdpjHdb.id == x.sale_id).first()

                    penjualan = ArCard.query.filter(and_(ArCard.bkt_id == sl.id, ArCard.trx_type == "JL", ArCard.pay_type == "P1")).first()

                    old_ar = ArCard.query.filter(
                        and_(ArCard.acq_id == x.id, ArCard.pay_type == "J4")).first()
                    if old_ar:
                        db.session.delete(old_ar)
                        db.session.commit()

                    ar_card = ArCard(penjualan.cus_id, inc.inc_code, penjualan.trx_date, penjualan.trx_due,
                                    x.id, inc.inc_date, penjualan.bkt_id, inc.inc_date, None, "D", penjualan.trx_type, "J4",
                                    penjualan.trx_amnh, None, x.payment, None, None, None, None, inc.giro_num, inc.giro_date, None, None, None )

                    db.session.add(ar_card)
                    db.session.commit()
