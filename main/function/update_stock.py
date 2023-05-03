from sqlalchemy import and_
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.hrgbl_mdb import HrgBlMdb
from main.model.jasa_mdb import JasaMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.comp_mdb import CompMdb
from main.shared.shared import db
import requests
from main.utils.response import response


class UpdateStock:
    # def print_trans_biaya(
    #     self,
    #     trx_code,
    #     desc,
    #     amnt,
    #     acc,
    # ):
    # print("\nJURNAL========================")
    # print("code: %s" % (trx_code))
    # print("acc: %s" % (acc))
    # print("amnt: %s" % (amnt))
    # print("desc: %s" % (desc))
    # print("============================\n")

    # print("\nJURNAL BIAYA========================")
    # print("code: %s" % (trx_code))
    # print("acc: %s" % (acc))
    # print("amnt: %s" % (amnt))
    # print("desc: %s" % (desc))
    # print("============================\n")

    def __init__(self, order_id, delete):
        try:
            order = OrdpbHdb.query.filter(OrdpbHdb.id == order_id).first()

            supl = SupplierMdb.query.filter(
                SupplierMdb.id == order.sup_id).first()

            # comp = CompMdb.query.filter(CompMdb.id == user_company).first()          

            curr = CurrencyMdb.query.all()

            product = (
                db.session.query(DprodDdb, ProdMdb, GroupProMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
                .filter(DprodDdb.ord_id == order_id)
                .all()
            )

            djasa = (
                db.session.query(DjasaDdb, JasaMdb, SupplierMdb)
                .outerjoin(JasaMdb, JasaMdb.id == DjasaDdb.jasa_id)
                .outerjoin(SupplierMdb, SupplierMdb.id == DjasaDdb.sup_id)
                .filter(DjasaDdb.ord_id == order_id)
                .all()
            )

            jasa_trans = []
            for x in djasa:
                old_trans = TransDdb.query.filter(
                    and_(
                        TransDdb.trx_code == order.ord_code,
                        TransDdb.trx_dbcr == "D",
                        TransDdb.trx_desc == "JURNAL BL JASA %s" % (x[1].name),
                    )
                ).first()
                if old_trans:
                    db.session.delete(old_trans)

                cur_rate_js = None
                for y in curr:
                    if order.same_sup:
                        if y.id == supl.sup_curren:
                            cur_rate_js = y.rate
                    else:
                        if y.id == x[2].sup_curren:
                            cur_rate_js = y.rate

                jasa_trans.append(
                    TransDdb(
                        order.ord_code,
                        order.ord_date,
                        x[1].acc_id,
                        order.dep_id,
                        order.proj_id,
                        None,
                        x[2].sup_curren
                        if order.same_sup == False
                        else supl.sup_curren,
                        cur_rate_js,
                        x[0].total_fc,
                        x[0].total,
                        "D",
                        "JURNAL BL JASA %s" % (x[1].name),
                        None,
                        None,
                    )
                )

            unit = UnitMdb.query.all()

            trans = []
            krtst = []
            trans_biaya = []

            cur_rate = None
            for y in curr:
                if y.id == supl.sup_curren:
                    cur_rate = y.rate

            qty = 0
            qty_total = 0
            total_prod = 0
            total_jasa = 0
            h_pokok = 0

            for y in djasa:
                total_jasa += y[0].total

            for x in product:
                qty_total += x[0].order

            for x in product:
                if delete:
                    old_history = HrgBlMdb.query.filter(
                        and_(
                            HrgBlMdb.ord_id == order.id,
                            HrgBlMdb.sup_id == order.sup_id,
                            HrgBlMdb.prod_id == x[0].prod_id,
                        )
                    ).first()
                    if old_history:
                        db.session.delete(old_history)

                    old_krtst = StCard.query.filter(
                        and_(
                            StCard.trx_code == order.ord_code,
                            StCard.prod_id == x[0].prod_id,
                            StCard.loc_id == x[0].location,
                        )
                    ).first()
                    if old_krtst:
                        db.session.delete(old_krtst)

                    old_trans = TransDdb.query.filter(
                        and_(
                            TransDdb.trx_code == order.ord_code,
                            TransDdb.trx_desc.like("%JURNAL STOCK%"),
                        )
                    ).first()
                    print(old_trans)
                    if old_trans:
                        db.session.delete(old_trans)

                else:
                    if x[0].unit_id != x[1].unit:
                        for y in unit:
                            if x[0].unit_id == y.id:
                                qty = x[0].order * y.qty
                    else:
                        qty = x[0].order

                    if x[0].nett_price and x[0].nett_price > 0:
                        total_prod += x[0].nett_price
                    else:
                        total_prod += x[0].total

                    if supl.sup_curren != None:
                        h_pokok = (
                            (total_jasa / qty_total) + (x[0].price * cur_rate)
                            if total_jasa and total_jasa > 0
                            else x[0].total
                        )

                    else:
                        h_pokok = (
                            (total_jasa / qty_total) + x[0].price
                            if total_jasa and total_jasa > 0
                            else x[0].total
                        )

                    old_history = HrgBlMdb.query.filter(
                        and_(
                            HrgBlMdb.ord_id == order.id,
                            HrgBlMdb.sup_id == order.sup_id,
                            HrgBlMdb.prod_id == x[0].prod_id,
                        )
                    ).first()

                    if old_history:
                        db.session.delete(old_history)

                    sup = HrgBlMdb(order.id, order.sup_id,
                                   x[0].prod_id, x[0].price)
                    db.session.add(sup)

                    old_krtst = StCard.query.filter(
                        and_(
                            StCard.trx_code == order.ord_code,
                            StCard.prod_id == x[0].prod_id,
                            StCard.loc_id == x[0].location,
                        )
                    ).first()
                    if old_krtst:
                        db.session.delete(old_krtst)

                    if x[1].ns == False:
                        krtst.append(
                            StCard(
                                order.ord_code,
                                order.ord_date,
                                "d",
                                "BL",
                                None,
                                qty,
                                None,
                                None,
                                h_pokok,
                                None,
                                None,
                                x[0].prod_id,
                                x[0].location,
                                0,
                                0,
                                0,
                            )
                        )

                        old_trans = TransDdb.query.filter(
                            and_(
                                TransDdb.trx_code == order.ord_code,
                                # TransDdb.trx_desc
                                # == "JURNAL STOCK %s %s" % (x[1].name, x[3].name),
                            )
                        ).all()

                        if old_trans:
                            for t in old_trans:
                                db.session.delete(t)

                        # for y in djasa:
                        acc_prod = None
                        if x[2].wip:
                            acc_prod = x[2].acc_wip
                        else:
                            acc_prod = x[2].acc_sto

                        # total_prod = 0
                        # total_prod_fc = 0
                        # if x[1].ns:
                        #     if x[0].nett_price and x[0].nett_price > 0:
                        #         total_prod += x[0].nett_price
                        #     else:
                        #         total_prod += x[0].total

                        #     total_prod_fc += x[0].total_fc

                        trans.append(
                            TransDdb(
                                order.ord_code,
                                order.ord_date,
                                acc_prod,
                                order.dep_id,
                                order.proj_id,
                                None,
                                supl.sup_curren,
                                cur_rate,
                                x[0].nett_price
                                if x[0].nett_price and x[0].nett_price > 0
                                else x[0].total_fc
                                if supl.sup_curren != None
                                else 0,
                                x[0].nett_price
                                if x[0].nett_price and x[0].nett_price > 0
                                else x[0].total,
                                "D",
                                "JURNAL STOCK %s %s" % (
                                    x[1].name, x[3].name),
                                None,
                                None,
                            )
                        )

                    else:
                        # Insert Jurnal Biaya
                        if x[1].ns:
                            trans_biaya.append(
                                TransDdb(
                                    order.ord_code,
                                    order.ord_date,
                                    x[2].biaya,
                                    order.dep_id,
                                    order.proj_id,
                                    None,
                                    supl.sup_curren,
                                    cur_rate,
                                    x[0].nett_price
                                    if x[0].nett_price and x[0].nett_price > 0
                                    else x[0].total_fc
                                    if supl.sup_curren != None
                                    else 0,
                                    x[0].nett_price
                                    if x[0].nett_price and x[0].nett_price > 0
                                    else x[0].total,
                                    "D",
                                    "JURNAL BIAYA %s %s" % (
                                        x[1].name, x[3].name),
                                    None,
                                    None,
                                )
                            )

                if not delete:
                    if len(trans) > 0:
                        # for x in trans:
                        # self.print_trans(
                        #     x.trx_code,
                        #     x.trx_desc,
                        #     x.trx_amnt,
                        #     x.acc_id,
                        # )
                        db.session.add_all(trans)
                    if len(krtst) > 0:
                        db.session.add_all(krtst)

                    if len(trans_biaya) > 0:
                        # for y in trans_biaya:
                        #     self.print_trans_biaya(
                        #         y.trx_code,
                        #         y.trx_desc,
                        #         y.trx_amnt,
                        #         y.acc_id,
                        #     )
                        db.session.add_all(trans_biaya)

                if len(jasa_trans) > 0:
                    db.session.add_all(jasa_trans)
            db.session.commit()

        except Exception as e:
            print(e)
            db.session.rollback()
            return response(400, "Gagal", True, None)
