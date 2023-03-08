from sqlalchemy import and_
from main.model.custom_mdb import CustomerMdb
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.jasa_mdb import JasaMdb
from main.model.jjasa_ddb import JjasaDdb
from main.model.jprod_ddb import JprodDdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.setup_mdb import SetupMdb
from main.model.sord_hdb import SordHdb
from main.model.stcard_mdb import StCard
from main.model.arcard_mdb import ArCard
from main.model.ordpb_hdb import OrdpbHdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.comp_mdb import CompMdb
from main.model.fkpj_hdb import FkpjHdb
from main.model.fkpj_det_ddb import FkpjDetDdb
from main.model.inv_pj_hdb import InvoicePjHdb
from main.shared.shared import db
import requests


class UpdateFakturPj:
    total = 0
    total_fc = 0
    total_product = 0
    total_product_fc = 0
    total_jasa = 0
    tjasa_fc = 0
    ppn = 0
    ppn_total = 0
    ppn_total_fc = 0

    def __init__(
        self,
        fak_id,
        delete,
        order_id,
        user_id,
    ):
        order = (
            db.session.query(
                FkpjHdb,
                FkpjDetDdb,
                OrdpjHdb,
                InvoicePjHdb,
            )
            # .outerjoin(FkpjDetDdb, FkpjDetDdb.fk_id == FkpjHdb.id)
            .outerjoin(OrdpjHdb, OrdpjHdb.id == FkpjDetDdb.sale_id)
            .outerjoin(InvoicePjHdb, InvoicePjHdb.sale_id == FkpjDetDdb.sale_id)
            .filter(FkpjHdb.id == fak_id)
            .first()
        )

        det = (
            db.session.query(FkpjDetDdb, OrdpjHdb)
            .outerjoin(OrdpjHdb, OrdpjHdb.id == FkpjDetDdb.sale_id)
            .filter(FkpjDetDdb.fk_id == order[0].id)
            .all()
        )

        krtar = ArCard.query.all()
        transddb = TransDdb.query.filter(TransDdb.trx_code == order[0].fk_code).all()

        ppn = (
            db.session.query(OrdpjHdb, CustomerMdb, PajakMdb)
            .outerjoin(CustomerMdb, CustomerMdb.id == OrdpjHdb.pel_id)
            .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
            .first()
        )

        cur = CurrencyMdb.query.all()

        # comp = CompMdb.query.filter(CompMdb.id == user_company).first()

        # if order[1].so_id:
        #     so = SordHdb.query.filter(SordHdb.id == order[1].so_id).first()
        #     if so:
        #         if delete:
        #             so.status = 0
        #             # db.session.commit()

        if delete:
            if krtar:
                for x in krtar:
                    for d in det:
                        if x.trx_code == d[1].ord_code:
                            db.session.delete(x)

            if transddb:
                for x in transddb:
                    db.session.delete(x)

            # db.session.commit()
        else:
            product = (
                db.session.query(JprodDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == JprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                # .filter(JprodDdb.pj_id == order[2].id)
                .all()
            )
            jasa = (
                db.session.query(JjasaDdb, JasaMdb, SupplierMdb)
                .outerjoin(JasaMdb, JasaMdb.id == JjasaDdb.jasa_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == JjasaDdb.sup_id)
                # .filter(JjasaDdb.pj_id == order[2].id)
                .all()
            )

            customer = CustomerMdb.query.filter(
                CustomerMdb.id
                == (order[2].sub_id if order[2].sub_addr else order[2].pel_id)
            ).first()

            unit = UnitMdb.query.all()

            setup = SetupMdb.query.filter(SetupMdb.cp_id == CompMdb.id).first()

            cur_rate = None
            for y in cur:
                if y.id == customer.cus_curren:
                    cur_rate = y.rate

            old_ar = ArCard.query.filter(
                and_(ArCard.trx_code == order[0].fk_code, ArCard.pay_type == "P1")
            ).first()

            if old_ar:
                db.session.delete(old_ar)

            if transddb:
                for x in transddb:
                    db.session.delete(x)

            # Product
            prod_trans = []
            new_krtst = []
            for d in det:
                for x in product:
                    if d[0].sale_id == x[0].pj_id:
                        self.total_product += (
                            x[0].nett_price
                            if x[0].nett_price and int(x[0].nett_price) > 0
                            else x[0].total
                        )

                        self.total_product_fc += (
                            x[0].nett_price
                            if x[0].nett_price and int(x[0].nett_price) > 0
                            else x[0].total_fc if x[0].total_fc != None else 0
                        )

                        qty = 0
                        if x[0].unit_id != x[1].unit:
                            for y in unit:
                                if x[0].unit_id == y.id:
                                    qty = x[0].order * y.qty
                        else:
                            qty = x[0].order

                        # Insert Jurnal Stock
                        prod_trans.append(
                            TransDdb(
                                order[0].fk_code,
                                order[0].fk_date,
                                setup.sls,
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
                                "SALES GL PRODUCT %s" % (x[2].name),
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
                    if d[0].sale_id == x[0].pj_id:
                        self.total_jasa += x[0].total
                        self.tjasa_fc += x[0].total_fc

                        for y in cur:
                            if y.id == x[2].sup_curren:
                                cur_jasa = y.rate

                        # Insert Jurnal Jasa
                        jasa_trans.append(
                            TransDdb(
                                order[0].fk_code,
                                order[0].fk_date,
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
                if order[2].split_inv:
                    if customer.cus_pjk != None:
                        self.total = (
                            self.total_product * ((100 + ppn[2].nilai) / 100)
                        ) + (self.total_jasa * ((100 + 2) / 100))

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
                new_ar = []
                new_ar.append(
                    ArCard(
                        d[1].sub_id if d[1].sub_addr else order[0].pel_id,
                        d[1].ord_code,
                        d[1].ord_date,
                        d[1].due_date,
                        None,
                        None,
                        d[0].sale_id,
                        None,
                        customer.cus_curren,
                        "D",
                        "JL",
                        "P1",
                        d[0].total_pay,
                        (d[0].total_pay / cur_rate)
                        if customer.cus_curren != None
                        else 0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        d[1].so_id,
                        None,
                    )
                )

                if len(new_ar) > 0:
                    db.session.add_all(new_ar)

                if customer.cus_pjk != None:
                    self.ppn_total = self.total_product * ppn[2].nilai / 100

                    self.ppn_total_fc = self.total_product_fc * ppn[2].nilai / 100

                # Insert Jurnal AR && PPN
                ar_trans = []
                ppn_trans = []
                ar_trans.append(
                    TransDdb(
                        order[0].fk_code,
                        order[0].fk_date,
                        customer.cus_gl,
                        None,
                        None,
                        None,
                        customer.cus_curren,
                        cur_rate,
                        (d[0].total_pay / cur_rate)
                        if customer.cus_curren != None
                        else 0,
                        d[0].total_pay,
                        "D",
                        "AR TRADE %s" % (order[0].fk_code),
                        None,
                        None,
                    )
                )

                if customer.cus_pjk != None:
                    ppn_trans.append(
                        TransDdb(
                            order[0].fk_code,
                            order[0].fk_date,
                            ppn[2].acc_sls_tax,
                            None,
                            None,
                            None,
                            customer.cus_curren,
                            cur_rate,
                            (d[0].total * ppn[2].nilai / 100) / cur_rate
                            if customer.cus_curren != None
                            else 0,
                            d[0].total * ppn[2].nilai / 100,
                            "K",
                            "VAT - OUT %s" % (order[0].fk_code),
                            None,
                            None,
                        )
                    )

                    if len(ppn_trans) > 0:
                        db.session.add_all(ppn_trans)

                if len(ar_trans) > 0:
                    db.session.add_all(ar_trans)

        db.session.commit()
