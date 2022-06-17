from sqlalchemy import and_
from main import product
from main.model.custom_mdb import CustomerMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.stcard_mdb import StCard
from main.model.arcard_mdb import ArCard
from main.model.ordpb_hdb import OrdpbHdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.transddb import TransDdb
from main.shared.shared import db


class UpdateAr:
    total = 0
    total_product = 0
    total_jasa = 0
    ppn = 11
    ppn_total = 0

    def __init__(self, delete, order_id):
        order = OrdpjHdb.query.filter(OrdpbHdb.id == order_id).first()
        krtar = ArCard.query.filter(ArCard.trx_code == order.ord_code).first()
        transddb = TransDdb.query.filter(TransDdb.trx_code == order.ord_code).first()
        krtst = StCard.query.filter(StCard.trx_code == order.ord_code).first()

        if delete:
            if krtar:
                db.session.delete(krtar)
            if transddb:
                db.session.delete(transddb)
            if krtst:
                db.session.delete(krtst)

            db.session.commit()
        else:
            old_ar = ArCard.query.filter(
                and_(ArCard.trx_code == order.ord_code, ArCard.pay_type == "P1")
            ).first()
            if old_ar:
                db.session.delete(old_ar)
            if transddb:
                db.session.delete(transddb)
            if krtst:
                db.session.delete(krtst)

            db.session.commit()

            product = DprodDdb.query.filter(DprodDdb.ord_id == order.id).all()
            jasa = DjasaDdb.query.filter(DjasaDdb.ord_id == order.id).all()
            customer = CustomerMdb.filter(
                CustomerMdb.id == order.sub_id if order.sub_addr else order.pel_id
            ).first()

            for x in product:
                self.total_product += x.nett_price if int(x.net_price) > 0 else x.total

            for x in jasa:
                self.total_jasa += x.total

            if order.split_inv:
                self.total = (self.total_product * ((100 + self.ppn) / 100)) + (
                    self.total_jasa * ((100 + 2) / 100)
                )
            else:
                self.total = (self.total_product + self.total_jasa) * (
                    (100 + self.ppn) / 100
                )

            new_ar = ArCard(
                order.sub_id if order.sub_addr else order.pel_id,
                order.ord_code,
                order.ord_date,
                order.due_date,
                None,
                None,
                None,
                None,
                None,
                "D",
                "JL",
                "P1",
                self.total,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )

            db.session.add(new_ar)
            db.session.commit()

            self.ppn_total = self.total_product * self.ppn / 100

            ar_trans = (
                TransDdb(
                    order.ord_code,
                    order.ord_date,
                    customer.cus_gl,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    self.total,
                    "D",
                    "AR TRADE %s" % (order.ord_code),
                    None,
                    None
                ),
            )
