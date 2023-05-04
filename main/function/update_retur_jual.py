from sqlalchemy import and_
from main.model.custom_mdb import CustomerMdb
from main.model.rsprod_ddb import RsprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.setup_mdb import SetupMdb
from main.model.sord_hdb import SordHdb
from main.model.stcard_mdb import StCard
from main.model.arcard_mdb import ArCard
from main.model.retsale_hdb import RetSaleHdb
from main.model.ordpj_hdb import OrdpjHdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.currency_model import CurrencyModel
from main.model.comp_mdb import CompMdb
from main.model.inv_pj_hdb import InvoicePjHdb
from main.shared.shared import db
import requests


class UpdateRetSale:
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
        ret_id,
        delete,
        user_id,
        user_product,
        user_company,
        glUrl,
        request,
    ):
        try:
            order = (
                db.session.query(
                    RetSaleHdb,
                    OrdpjHdb,
                )
                .outerjoin(OrdpjHdb, OrdpjHdb.id == RetSaleHdb.sale_id)
                .filter(RetSaleHdb.id == ret_id)
                .first()
            )
            krtar = ArCard.query.all()
            transddb = TransDdb.query.filter(TransDdb.trx_code == order[0].ret_code).all()

            ppn = (
                db.session.query(OrdpjHdb, CustomerMdb, PajakMdb)
                .outerjoin(CustomerMdb, CustomerMdb.id == OrdpjHdb.pel_id)
                .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
                .first()
            )

            comp = CompMdb.query.filter(CompMdb.id == user_company).first()

            header = {"Authorization": "Bearer {}".format(request.headers["Authorization"])}
            result = requests.get(url=glUrl + "/v1/api/currency", headers=header).json()

            curr = []
            if result["code"] == 200:
                for z in result["data"]:
                    curr.append(CurrencyModel(z))

            # if order[1].so_id:
            #     so = SordHdb.query.filter(SordHdb.id == order[1].so_id).first()
            #     if so:
            #         if delete:
            #             so.status = 0
            #             # db.session.commit()

            if delete:
                if krtar:
                    for x in krtar:
                        if x.trx_code == order[0].ret_code:
                            db.session.delete(x)

                if transddb:
                    for x in transddb:
                        db.session.delete(x)

                # db.session.commit()
            else:
                product = (
                    db.session.query(RsprodDdb, ProdMdb, GroupProMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == RsprodDdb.prod_id)
                    .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                    .filter(RsprodDdb.ret_id == order[0].id)
                    .all()
                )

                customer = CustomerMdb.query.filter(
                    CustomerMdb.id
                    == (order[1].sub_id if order[1].sub_addr else order[1].pel_id)
                ).first()

                unit = UnitMdb.query.all()

                setup = SetupMdb.query.filter(SetupMdb.cp_id == user_company).first()

                cur_rate = None
                for y in curr:
                    if y.id == customer.cus_curren:
                        cur_rate = y.rate

                old_ar = ArCard.query.filter(
                    and_(ArCard.trx_code == order[0].ret_code, ArCard.trx_type == "RET")
                ).first()

                if old_ar:
                    db.session.delete(old_ar)

                if transddb:
                    for x in transddb:
                        db.session.delete(x)

                # Product
                prod_trans = []
                new_krtst = []
                for x in product:
                    self.total_product += (
                        x[0].nett_price
                        if x[0].nett_price and int(x[0].nett_price) > 0
                        else x[0].totl
                    )

                    self.total_product_fc += (
                        x[0].nett_price
                        if x[0].nett_price and int(x[0].nett_price) > 0
                        else x[0].totl_fc
                    )

                    # Insert Jurnal Stock
                    acc_prod = None
                    if comp.gl_detail:
                        if x[2].wip:
                            acc_prod = x[1].acc_wip
                        else:
                            acc_prod = x[1].acc_sto

                    else:
                        if x[2].wip:
                            acc_prod = x[2].acc_wip
                        else:
                            acc_prod = x[2].acc_sto

                    if user_product == "inv+gl":
                        prod_trans.append(
                            TransDdb(
                                order[0].ret_code,
                                order[0].ret_date,
                                acc_prod,
                                None,
                                None,
                                None,
                                customer.cus_curren,
                                cur_rate,
                                x[0].nett_price
                                if x[0].nett_price and int(x[0].nett_price) > 0
                                else x[0].totl_fc,
                                x[0].nett_price
                                if x[0].nett_price and int(x[0].nett_price) > 0
                                else x[0].totl,
                                "D",
                                "JURNAL RETUR STOCK %s" % (x[2].name),
                                None,
                                None,
                            )
                        )

                        if len(prod_trans) > 0:
                            db.session.add_all(prod_trans)

                # AR Card
                if customer.cus_pjk != None:
                    self.total = self.total_product * ((100 + ppn[2].nilai) / 100)

                    self.total_fc = self.total_product_fc * ((100 + ppn[2].nilai) / 100)
                else:
                    self.total = self.total_product * ((100 + 0) / 100)

                    self.total_fc = self.total_product_fc * ((100 + 0) / 100)

                # Insert Kartu AR
                new_ar = []
                new_ar.append(
                    ArCard(
                        order[1].sub_id if order[1].sub_addr else order[1].pel_id,
                        order[0].ret_code,
                        order[0].ret_date,
                        order[1].due_date,
                        None,
                        None,
                        order[1].id,
                        None,
                        customer.cus_curren,
                        cur_rate,
                        "K",
                        "RET",
                        "RT1",
                        self.total,
                        self.total_fc,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        order[1].so_id,
                        None,
                        None,
                        False,
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
                if user_product == "inv+gl":
                    ar_trans.append(
                        TransDdb(
                            order[0].ret_code,
                            order[0].ret_date,
                            customer.cus_gl,
                            None,
                            None,
                            None,
                            customer.cus_curren,
                            cur_rate,
                            self.total_fc,
                            self.total,
                            "K",
                            "JURNAL RETUR AR %s" % (order[0].ret_code),
                            None,
                            None,
                        )
                    )

                    if customer.cus_pjk != None:
                        ppn_trans.append(
                            TransDdb(
                                order[0].ret_code,
                                order[0].ret_date,
                                ppn[2].acc_sls_tax,
                                None,
                                None,
                                None,
                                customer.cus_curren,
                                cur_rate,
                                self.ppn_total_fc,
                                self.ppn_total,
                                "D",
                                "RETUR VAT - OUT %s" % (order[0].ret_code),
                                None,
                                None,
                            )
                        )

                        if len(ppn_trans) > 0:
                            db.session.add_all(ppn_trans)

                    if len(ar_trans) > 0:
                        db.session.add_all(ar_trans)

            db.session.commit()

        except Exception as e:
            print("=========")
            print(e)