from sqlalchemy import and_
from main.model.stcard_mdb import StCard
from main.model.apcard_mdb import ApCard
from main.model.reprod_ddb import ReprodDdb
from main.model.inv_pb_hdb import InvpbHdb
from main.model.lokasi_mdb import LocationMdb
from main.model.retord_hdb import RetordHdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.setup_mdb import SetupMdb
from main.model.comp_mdb import CompMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.user import User
from main.shared.shared import db, ma
import requests


class UpdateReturOrd:
    def __init__(
        self, ret_id, user_id, delete
    ):
        try:
            # update kartu ap
            ret = (
                db.session.query(RetordHdb, InvpbHdb, OrdpbHdb)
                .outerjoin(InvpbHdb, InvpbHdb.id == RetordHdb.inv_id)
                .outerjoin(OrdpbHdb, OrdpbHdb.id == InvpbHdb.ord_id)
                .filter(RetordHdb.id == ret_id)
                .first()
            )

            curr = CurrencyMdb.query.all()

            if delete:
                # if x[1]:
                old_ap = ApCard.query.filter(
                    and_(
                        ApCard.ord_id == ret[1].ord_id,
                        ApCard.trx_type == "RET",
                        ApCard.pay_type == "RB1",
                    )
                ).first()
                if old_ap:
                    db.session.delete(old_ap)

                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == ret[0].ret_code
                ).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

            else:
                prod = (
                    db.session.query(ReprodDdb, ProdMdb, GroupProMdb)
                    .outerjoin(ProdMdb, ProdMdb.id == ReprodDdb.prod_id)
                    .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                    .filter(ReprodDdb.ret_id == ret[0].id)
                    .all()

                )

                sup = SupplierMdb.query.filter(
                    SupplierMdb.id == ret[2].sup_id).first()

                # comp = CompMdb.query.filter(CompMdb.id == user_company).first()

                # setup = SetupMdb.query.filter(
                #     SetupMdb.cp_id == user_company).first()

                ppn = PajakMdb.query.filter(PajakMdb.id == sup.sup_ppn).first()

                total_product = 0
                total_product_fc = 0
                trx_amnt = 0
                trx_amnv = 0
                for y in prod:
                    if y[0].nett_price and y[0].nett_price > 0:
                        total_product += y[0].nett_price
                    else:
                        total_product += y[0].totl

                    total_product_fc += y[0].totl_fc if y[0].totl_fc != None else 0

                if sup.sup_ppn:
                    trx_amnh = total_product * ((100 + ppn.nilai) / 100)

                    trx_amnv = total_product_fc * ((100 + ppn.nilai) / 100)
                else:
                    trx_amnh = total_product * ((100 + 0) / 100)

                    trx_amnv = total_product_fc * ((100 + 0) / 100)

                all_sto = []
                old_sto = StCard.query.filter(
                    StCard.trx_code == ret[0].ret_code).all()
                if old_sto:
                    for x in old_sto:
                        db.session.delete(x)

                for x in prod:
                    all_sto.append(
                        StCard(
                            ret[0].ret_code,
                            ret[0].ret_date,
                            "k",
                            "RTB",
                            None,
                            x[0].retur,
                            None,
                            None,
                            x[0].nett_price
                            if x[0].nett_price and x[0].nett_price > 0
                            else x[0].totl,
                            None,
                            x[0].disc,
                            x[0].prod_id,
                            x[0].location,
                            0,
                            0,
                            0,
                        )
                    )

                    if len(all_sto) > 0:
                        db.session.add_all(all_sto)

                    trans_sto = []
                    acc_prod = None
                    if x[2].wip:
                        acc_prod = x[2].acc_wip
                    else:
                        acc_prod = x[2].acc_sto

                    old_trn_sto = TransDdb.query.filter(
                        and_(
                            TransDdb.trx_code == ret[0].ret_code,
                            TransDdb.trx_desc
                            == "JURNAL RETUR STOCK %s" % (x[1].code, x[2].code),
                        )
                    ).first()

                    if old_trn_sto:
                        db.session.delete(old_trn_sto)

                    trans_sto.append(
                        TransDdb(
                            ret[0].ret_code,
                            ret[0].ret_date,
                            acc_prod,
                            None,
                            None,
                            None,
                            sup.sup_curren,
                            cur_rate if sup.sup_curren else None,
                            x[0].nett_price
                            if x[0].nett_price and x[0].nett_price > 0
                            else x[0].totl_fc
                            if sup.sup_curren != None
                            else 0,
                            x[0].nett_price
                            if x[0].nett_price and x[0].nett_price > 0
                            else x[0].totl,
                            "K",
                            "JURNAL RETUR STOCK %s %s" % (
                                x[1].code, x[2].code),
                            None,
                            None,
                        )
                    )

                    if len(trans_sto) > 0:
                        db.session.add_all(trans_sto)

                # Insert APCARD
                old_ap = ApCard.query.filter(
                    and_(
                        ApCard.ord_id == ret[1].ord_id,
                        ApCard.trx_type == "RET",
                        ApCard.trx_code == ret[0].ret_code,
                    )
                ).all()
                if old_ap:
                    for x in old_ap:
                        db.session.delete(x)

                new_ap = []
                new_ap = ApCard(
                    ret[0].ret_code,
                    ret[2].sup_id,
                    ret[1].ord_id,
                    ret[0].ret_date,
                    None,
                    None,
                    None,
                    None,
                    sup.sup_curren,
                    "d",
                    "RET",
                    "P1",
                    trx_amnh,
                    trx_amnv,
                    None,
                    None,
                    None,
                    None,
                    None,
                    False,
                )

                db.session.add(new_ap)

                # insert jurnal ap
                old_trn_ap = TransDdb.query.filter(
                    and_(
                        TransDdb.trx_code == ret[0].ret_code,
                        TransDdb.trx_desc
                        == "JURNAL RETUR PEMBELIAN %s" % (ret[0].ret_code),
                    )
                ).first()

                if old_trn_ap:
                    db.session.delete(old_trn_ap)

                trans_ap = TransDdb(
                    ret[0].ret_code,
                    ret[0].ret_date,
                    sup.sup_hutang if sup.sup_hutang != None else None,
                    None,
                    None,
                    None,
                    sup.sup_curren,
                    cur_rate,
                    trx_amnv if sup.sup_curren != None else 0,
                    trx_amnh,
                    "D",
                    "JURNAL RETUR PEMBELIAN %s %s" % (ret[0].ret_code),
                    None,
                    None,
                )

                db.session.add(trans_ap)

                # insert jurnal ppn
                if ppn:
                    old_trn_ppn = TransDdb.query.filter(
                        and_(
                            TransDdb.trx_code == ret[0].ret_code,
                            TransDdb.trx_desc
                            == "JURNAL PPN MASUKAN %s" % (ret[0].ret_code),
                        )
                    ).first()

                    if old_trn_ppn:
                        db.session.delete(old_trn_ppn)

                    trans_ppn = TransDdb(
                        ret[0].ret_code,
                        ret[0].ret_date,
                        ppn.acc_pur_tax,
                        None,
                        None,
                        None,
                        sup.sup_curren,
                        cur_rate if sup.sup_curren else None,
                        total_product_fc * ppn.nilai / 100,
                        total_product * ppn.nilai / 100,
                        "K",
                        "JURNAL PPN MASUKAN %s %s" % (ret[0].ret_code),
                        None,
                        None,
                    )

                    db.session.add(trans_ppn)

            db.session.commit()

        except Exception as e:
            print("================")
            print(e)
