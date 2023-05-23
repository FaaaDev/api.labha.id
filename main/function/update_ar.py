from sqlalchemy import and_
from ..model.custom_mdb import CustomerMdb
from ..model.supplier_mdb import SupplierMdb
from ..model.djasa_ddb import DjasaDdb
from ..model.dprod_ddb import DprodDdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.jasa_mdb import JasaMdb
from ..model.jjasa_ddb import JjasaDdb
from ..model.jprod_ddb import JprodDdb
from ..model.pajak_mdb import PajakMdb
from ..model.prod_mdb import ProdMdb
from ..model.setup_mdb import SetupMdb
from ..model.sord_hdb import SordHdb
from ..model.stcard_mdb import StCard
from ..model.arcard_mdb import ArCard
from ..model.ordpb_hdb import OrdpbHdb
from ..model.ordpj_hdb import OrdpjHdb
from ..model.transddb import TransDdb
from ..model.unit_mdb import UnitMdb
from ..model.currency_mdb import CurrencyMdb
from ..model.comp_mdb import CompMdb
from ..model.user import User
from ..shared.shared import db


class UpdateAr:
    total = 0
    total_fc = 0
    total_product = 0
    total_product_fc = 0
    total_jasa = 0
    tjasa_fc = 0
    ppn = 0
    ppn_total = 0
    ppn_total_fc = 0

    def __init__(self, delete, order_id, user_id):
        order = OrdpjHdb.query.filter(OrdpjHdb.id == order_id).first()
        krtar = ArCard.query.filter(ArCard.trx_code == order.ord_code).all()
        transddb = TransDdb.query.filter(TransDdb.trx_code == order.ord_code).all()
        krtst = StCard.query.filter(StCard.trx_code == order.ord_code).all()


        # comp = CompMdb.query.filter(CompMdb.id == user_company).first()

        curr = CurrencyMdb.query.all()

        if order.so_id:
            so = SordHdb.query.filter(SordHdb.id == order.so_id).first()
            if so:
                if delete:
                    so.status = 0
                    # db.session.commit()

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

            # db.session.commit()
        else:
            product = (
                db.session.query(JprodDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(JprodDdb.pj_id == order.id)
                .all()
            )
            jasa = (
                db.session.query(JjasaDdb, JasaMdb, SupplierMdb)
                .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == JjasaDdb.sup_id)
                .filter(JjasaDdb.pj_id == order.id)
                .all()
            )

            customer = CustomerMdb.query.filter(
                CustomerMdb.id == (order.sub_id if order.sub_addr else order.pel_id)
            ).first()


            ppn = (
                db.session.query(OrdpjHdb, CustomerMdb, PajakMdb)
                .outerjoin(CustomerMdb, CustomerMdb.id == OrdpjHdb.pel_id)
                .outerjoin(PajakMdb, PajakMdb.id == customer.cus_pjk)
                .first()
            )

            unit = UnitMdb.query.all()

            cur_rate = None
            for y in curr:
                if y.id == customer.cus_curren:
                    cur_rate = y.rate

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

            # Product
            prod_trans = []
            new_krtst = []
            for x in product:
                self.total_product += (
                    x[0].nett_price
                    if x[0].nett_price and int(x[0].nett_price) > 0
                    else x[0].total
                )

                self.total_product_fc += (
                    x[0].nett_price
                    if x[0].nett_price and int(x[0].nett_price) > 0
                    else x[0].total_fc
                    if customer.cus_curren != None
                    else 0
                )

                qty = 0
                if x[0].unit_id != x[1].unit:
                    for y in unit:
                        if x[0].unit_id == y.id:
                            qty = x[0].order * y.qty
                else:
                    qty = x[0].order

                # Insert Kartu Stock
                new_krtst.append(
                    StCard(
                        order.ord_code,
                        order.ord_date,
                        "k",
                        "JL",
                        None,
                        qty,
                        x[0].nett_price
                        if x[0].nett_price and int(x[0].nett_price) > 0
                        else x[0].total,
                        None,
                        x[0].price
                        if customer.cus_curren == None
                        else x[0].price * cur_rate,
                        x[0].price if customer.cus_curren != None else None,
                        x[0].disc,
                        x[0].prod_id,
                        x[0].location,
                        None,
                        0,
                        None,
                    )
                )

                if len(new_krtst) > 0:
                    db.session.add_all(new_krtst)

                # Insert Jurnal Stock
                acc_prod = None
                if x[2].wip:
                    acc_prod = x[2].acc_wip
                else:
                    acc_prod = x[2].acc_sto

                prod_trans.append(
                    TransDdb(
                        order.ord_code,
                        order.ord_date,
                        acc_prod,
                        None,
                        None,
                        None,
                        customer.cus_curren,
                        cur_rate,
                        x[0].nett_price
                        if x[0].nett_price and int(x[0].nett_price) > 0
                        else x[0].total_fc,
                        x[0].nett_price
                        if x[0].nett_price and int(x[0].nett_price) > 0
                        else x[0].total,
                        "K",
                        "SALES GL PRODUCT %s" % (x[2].code),
                        None,
                        None,
                    )
                )

                if len(prod_trans) > 0:
                    db.session.add_all(prod_trans)

            # Jasa
            jasa_trans = []
            cur_jasa = None
            for x in jasa:
                self.total_jasa += x[0].total
                self.tjasa_fc += x[0].total_fc

                for y in curr:
                    if y.id == x[2].sup_curren:
                        cur_jasa = y.rate

                # Insert Jurnal Jasa
                if order.surat_jalan == 2:
                    jasa_trans.append(
                        TransDdb(
                            order.ord_code,
                            order.ord_date,
                            x[1].acc_id,
                            None,
                            None,
                            None,
                            x[2].sup_curren,
                            cur_jasa,
                            x[0].total_fc,
                            x[0].total,
                            "K",
                            "SALES GL JASA %s" % (x[1].code),
                            None,
                            None,
                        )
                    )

                    if len(jasa_trans) > 0:
                        db.session.add_all(jasa_trans)

            # AR Card
            if order.split_inv:
                if customer.cus_pjk != None:
                    self.total = (self.total_product * ((100 + ppn[2].nilai) / 100)) + (
                        self.total_jasa * ((100 + 2) / 100)
                    )

                    self.total_fc = (
                        self.total_product_fc * ((100 + ppn[2].nilai) / 100)
                    ) + (self.tjasa_fc * ((100 + 2) / 100))
                else:
                    self.total = (self.total_product * ((100 + 0) / 100)) + (
                        self.total_jasa * ((100 + 2) / 100)
                    )

                    self.total_fc = (self.total_product_fc * ((100 + 0) / 100)) + (
                        self.tjasa_fc * ((100 + 2) / 100)
                    )
            else:
                if customer.cus_pjk != None:
                    self.total = (self.total_product + self.total_jasa) * (
                        (100 + ppn[2].nilai) / 100
                    )

                    self.total_fc = (self.total_product_fc + self.tjasa_fc) * (
                        (100 + ppn[2].nilai) / 100
                    )
                else:
                    self.total = (self.total_product + self.total_jasa) * (
                        (100 + 0) / 100
                    )

                    self.total_fc = (self.total_product_fc + self.tjasa_fc) * (
                        (100 + 0) / 100
                    )

            # Insert Kartu AR
            if order.surat_jalan == 2:
                new_ar = ArCard(
                    order.sub_id if order.sub_addr else order.pel_id,
                    order.ord_code,
                    order.ord_date,
                    order.due_date,
                    None,
                    None,
                    order.id,
                    None,
                    cur_rate,
                    "D",
                    "JL",
                    "P1",
                    self.total,
                    (self.total / cur_rate) if customer.cus_curren != None else 0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    order.so_id,
                    None,
                    None,
                    False,
                )

                db.session.add(new_ar)

            if customer.cus_pjk != None:
                self.ppn_total = self.total_product * ppn[2].nilai / 100

                self.ppn_total_fc = self.total_product_fc * ppn[2].nilai / 100

            setup = SetupMdb.query.filter(SetupMdb.cp_id == CompMdb.id).first()
            # Insert Jurnal AR && PPN
            ar_trans = TransDdb(
                order.ord_code,
                order.ord_date,
                setup.ar if order.surat_jalan == 2 else setup.sls,
                None,
                None,
                None,
                customer.cus_curren,
                cur_rate,
                self.total_fc,
                self.total,
                "D",
                "AR TRADE %s" % (order.ord_code),
                None,
                None,
            )

            if order.surat_jalan == 2:
                if customer.cus_pjk != None:
                    ppn_trans = TransDdb(
                        order.ord_code,
                        order.ord_date,
                        ppn[2].acc_sls_tax,
                        None,
                        None,
                        None,
                        customer.cus_curren,
                        cur_rate,
                        self.ppn_total_fc,
                        self.ppn_total
                        if self.total_jasa == 0
                        else (self.total_product + self.total_jasa)
                        * ppn[2].nilai
                        / 100,
                        "K",
                        "VAT - OUT %s" % (order.ord_code),
                        None,
                        None,
                    )

                    db.session.add(ppn_trans)
            db.session.add(ar_trans)

        db.session.commit()
