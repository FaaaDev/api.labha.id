from sqlalchemy import and_
from main.model.custom_mdb import CustomerMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.jasa_mdb import JasaMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.prod_mdb import ProdMdb
from main.model.setup_mdb import SetupMdb
from main.model.sord_hdb import SordHdb
from main.model.stcard_mdb import StCard
from main.model.arcard_mdb import ArCard
from main.model.ordpb_hdb import OrdpbHdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.user import User
from main.shared.shared import db


class UpdateAr:
    total = 0
    total_product = 0
    total_jasa = 0
    ppn = 11
    ppn_total = 0

    def __init__(self, delete, order_id, user_id):
        order = OrdpjHdb.query.filter(OrdpjHdb.id == order_id).first()
        krtar = ArCard.query.filter(ArCard.trx_code == order.ord_code).all()
        transddb = TransDdb.query.filter(TransDdb.trx_code == order.ord_code).all()
        krtst = StCard.query.filter(StCard.trx_code == order.ord_code).all()
        if order.so_id:
            so = SordHdb.query.filter(SordHdb.id == order.so_id).first()
            if so:
                if delete:
                    so.status = 0
                    db.session.commit()
                else:
                    so.status = 1
                    db.session.commit()

        if delete:
            if krtar:
                for x in krtar:
                    db.session.delete(x)
            if transddb:
                for x in transddb:
                    db.session.delete(x)
            if krtst:
                for x in krtst:
                    db.session.delete(x)

            db.session.commit()
        else:
            old_ar = ArCard.query.filter(
                and_(ArCard.trx_code == order.ord_code, ArCard.pay_type == "P1")
            ).first()
            if old_ar:
                db.session.delete(old_ar)
            if transddb:
                for x in transddb:
                    db.session.delete(x)
            if krtst:
                for x in krtst:
                    db.session.delete(x)

            db.session.commit()

            product = (
                db.session.query(JprodDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(JprodDdb.pj_id == order.id)
                .all()
            )
            jasa = (
                db.session.query(JjasaDdb, JasaMdb)
                .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                .filter(JjasaDdb.pj_id == order.id)
                .all()
            )

            unit = UnitMdb.query.all()

            customer = CustomerMdb.query.filter(
                CustomerMdb.id == (order.sub_id if order.sub_addr else order.pel_id)
            ).first()

            prod_trans = []
            new_krtst = []
            for x in product:
                self.total_product += (
                    x[0].nett_price if x[0].nett_price and int(x[0].nett_price) > 0 else x[0].total
                )
                prod_trans.append(
                    TransDdb(
                        order.ord_code,
                        order.ord_date,
                        x[2].acc_sto,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        x[0].nett_price if x[0].nett_price and int(x[0].nett_price) > 0 else x[0].total,
                        "K",
                        "SALES GL PRODUCT %s" % (x[2].code),
                        None,
                        None,
                    )
                )
                qty = 0
                if x[0].unit_id != x[1].unit:
                    for y in unit:
                        if x[0].unit_id == y.id:
                            qty = x[0].order * y.qty
                else:
                    qty = x[0].order

                new_krtst.append(
                    StCard(
                        order.ord_code,
                        order.ord_date,
                        "k",
                        "JL",
                        None,
                        qty,
                        None,
                        None,
                        x[0].nett_price if x[0].nett_price and int(x[0].nett_price) > 0 else x[0].total,
                        x[0].price,
                        x[0].disc,
                        x[0].prod_id,
                        x[0].location,
                        None,
                        0,
                        None
                    )
                )

            jasa_trans = []
            for x in jasa:
                self.total_jasa += x.total
                jasa_trans.append(
                    TransDdb(
                        order.ord_code,
                        order.ord_date,
                        x[1].acc_id,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        x[0].total,
                        "K",
                        "SALES GL JASA %s" % (x[1].code),
                        None,
                        None,
                    )
                )

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

            ar_trans = TransDdb(
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
                None,
            )

            setup = (
                db.session.query(User, SetupMdb)
                .outerjoin(SetupMdb, SetupMdb.cp_id == User.company)
                .filter(User.id == user_id)
                .first()
            )

            ppn_trans = TransDdb(
                order.ord_code,
                order.ord_date,
                setup[1].sls_tax,
                None,
                None,
                None,
                None,
                None,
                None,
                self.ppn_total,
                "K",
                "VAT - OUT %s" % (order.ord_code),
                None,
                None,
            )

            db.session.add(ppn_trans)
            db.session.add(ar_trans)
            if len(prod_trans) > 0:
                db.session.add_all(prod_trans)
            if len(jasa_trans) > 0:
                db.session.add_all(jasa_trans)
            if len(new_krtst) > 0:
                db.session.add_all(new_krtst)

            db.session.commit()
