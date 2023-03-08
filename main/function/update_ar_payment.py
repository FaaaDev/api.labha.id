from sqlalchemy import and_, or_
from main.model.bank_mdb import BankMdb
from main.model.custom_mdb import CustomerMdb
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
from main.model.currency_mdb import CurrencyMdb
from main.model.setup_mdb import SetupMdb
from main.model.comp_mdb import CompMdb
from main.shared.shared import db


class UpdateArPayment:
    def __init__(self, inc_id, delete):

        inc = IncHdb.query.filter(IncHdb.id == inc_id).first()

        acq = (
            db.session.query(IAcqDdb, OrdpjHdb)
            .outerjoin(OrdpjHdb, OrdpjHdb.id == IAcqDdb.sale_id)
            .filter(IAcqDdb.inc_id == inc.id)
            .all()
        )

        incs = IncDdb.query.filter(IncDdb.inc_id == inc.id).all()

        curr = CurrencyMdb.query.all()

        bank = BankMdb.query.all()

        setup = SetupMdb.query.filter(SetupMdb.cp_id == CompMdb.id).first()

        old_trans = TransDdb.query.filter(TransDdb.trx_code == inc.inc_code).all()

        # insert kartu ar

        if inc.type_trx == 1 and inc.acq_pay != 3:
            if delete:
                for x in acq:
                    jl = ArCard.query.filter(
                        or_(
                            and_(
                                ArCard.bkt_id == x[0].sale_id,
                                ArCard.trx_dbcr == "D",
                                ArCard.pay_type == "P1",
                            ),
                            # and_(
                            #     ArCard.sa_id == x[0].sa_id,
                            #     ArCard.trx_type == "SA",
                            #     ArCard.trx_dbcr == "D",
                            #     ArCard.pay_type == "P1",
                            # ),
                        )
                    ).first()

                    old_ar = ArCard.query.filter(
                        and_(ArCard.acq_id == x[0].id, ArCard.pay_type == "J4")
                    ).first()
                    if old_ar:
                        db.session.delete(old_ar)

                    if jl.bkt_id or jl.sa_id:
                        jl.lunas = False
                        db.session.commit()
            else:
                total = 0
                total_fc = 0
                amnt = 0

                for x in acq:
                    total += x[0].payment
                    cus = (
                        db.session.query(CustomerMdb, OrdpjHdb)
                        .outerjoin(OrdpjHdb, OrdpjHdb.pel_id == CustomerMdb.id)
                        # .outerjoin(SaldoARMdb, SaldoARMdb.cus_id == CustomerMdb.id)
                        .filter(CustomerMdb.id == inc.acq_cus)
                        .first()
                    )

                    cur_rate = None
                    for y in curr:
                        if y.id == cus[0].cus_curren:
                            cur_rate = y.rate

                    if cus[0].cus_curren:
                        total_fc = total * cur_rate

                    # amnt = x.payment * cur_rate

                    sl = OrdpjHdb.query.filter(OrdpjHdb.id == x[0].sale_id).first()

                    penjualan = ArCard.query.filter(
                        or_(
                            and_(
                                ArCard.bkt_id == x[0].sale_id,
                                ArCard.trx_dbcr == "D",
                                ArCard.pay_type == "P1",
                            ),
                            # and_(
                            #     ArCard.sa_id == x[0].sa_id,
                            #     ArCard.trx_type == "SA",
                            #     ArCard.trx_dbcr == "D",
                            #     ArCard.pay_type == "P1",
                            # ),
                        )
                    ).first()

                    # sa = ArCard.query.filter()

                    old_ar = ArCard.query.filter(
                        and_(ArCard.acq_id == x[0].id, ArCard.pay_type == "J4")
                    ).first()

                    if old_ar:
                        db.session.delete(old_ar)

                    ar_card = ArCard(
                        inc.acq_cus,
                        inc.inc_code,
                        x[1].ord_date,
                        x[1].due_date,
                        x[0].id,
                        inc.inc_date,
                        x[1].id,
                        inc.inc_date,
                        cus[0].cus_curren,
                        "K",
                        penjualan.trx_type,
                        "J4",
                        penjualan.trx_amnh,
                        penjualan.trx_amnv if cus[0].cus_curren != None else None,
                        x[0].payment * cur_rate
                        if cus[0].cus_curren != None
                        else x[0].payment,
                        x[0].payment if cus[0].cus_curren != None else None,
                        None,
                        None,
                        None,
                        inc.giro_num,
                        inc.giro_date,
                        None,
                        x[1].so_id,
                        None,
                    )

                    db.session.add(ar_card)

                    if penjualan.bkt_id or penjualan.sa_id:
                        if (
                            x[0].payment + x[0].dp >= penjualan.trx_amnh
                            or x[0].payment + x[0].dp >= penjualan.trx_amnv
                        ):
                            penjualan.lunas = True

                    bank_acc = None
                    if inc.bank_acc:
                        for y in bank:
                            if y.id == inc.bank_acc:
                                bank_acc = y.acc_id

                    if old_trans:
                        for d in old_trans:
                            db.session.delete(d)

                    # insert jurnal ap
                    trans_cus = TransDdb(
                        inc.inc_code,
                        inc.inc_date,
                        cus[0].cus_gl,
                        None,
                        None,
                        None,
                        penjualan.cur_conv,
                        None,
                        penjualan.trx_amnv if cus[0].cus_curren != None else 0,
                        penjualan.trx_amnh,
                        "K",
                        "JURNAL PELUNASAN PIUTANG %s" % (inc.inc_code),
                        None,
                        None,
                    )

                    if x[0].dp > 0:
                        trans_dp = TransDdb(
                            inc.inc_code,
                            inc.inc_date,
                            cus[0].cus_uang_muka,
                            None,
                            None,
                            None,
                            cus[0].cus_curren,
                            cur_rate,
                            x[0].dp / cur_rate if cus[0].cus_curren != None else 0,
                            x[0].dp,
                            "D",
                            "JURNAL UANG MUKA ATAS PELUNASAN %s" % (inc.inc_code),
                            None,
                            None,
                        )
                        db.session.add(trans_dp)

                    if cus[0].cus_curren != None:
                        trans_kurs = TransDdb(
                            inc.inc_code,
                            inc.inc_date,
                            setup.selisih_kurs,
                            None,
                            None,
                            None,
                            cus[0].cus_curren,
                            cur_rate,
                            abs((penjualan.trx_amnh - total_fc) / cur_rate),
                            abs(penjualan.trx_amnh - total_fc),
                            "D" if total_fc - penjualan.trx_amnh < 0 else "K",
                            "JURNAL PELUNASAN SELISIH KURS %s" % (inc.inc_code),
                            None,
                            None,
                        )

                        db.session.add(trans_kurs)

                    db.session.add(trans_cus)

                trans_inc = TransDdb(
                    inc.inc_code,
                    inc.inc_date,
                    inc.acq_kas if inc.acq_pay == 1 else bank_acc,
                    None,
                    None,
                    None,
                    cus[0].cus_curren,
                    cur_rate,
                    total if cus[0].cus_curren != None else 0,
                    total_fc if cus[0].cus_curren != None else total,
                    "D",
                    "JURNAL PELUNASAN PENJUALAN %s" % (inc.inc_code),
                    None,
                    None,
                )

                db.session.add(trans_inc)

        else:
            inc_bnk = None
            if inc.inc_bnk:
                for z in bank:
                    if z.id == inc.inc_bnk:
                        inc_bnk = z.acc_id

            if old_trans:
                for d in old_trans:
                    db.session.delete(d)

            #     old_transbank = TransBank.query.filter(
            #         and_(
            #             TransBank.trx_code == inc.inc_code,
            #             TransBank.bank_id == inc.inc_bnk,
            #         )
            #     ).first()

            #     if old_transbank:
            #         db.session.delete(old_transbank)
            #         db.session.commit()
            #         db.session.close()

            total = 0
            for y in incs:
                bnk_code = None
                if y.bnk_code:
                    for z in bank:
                        if z.id == y.bnk_code:
                            bnk_code = z.acc_id

                total += y.fc

                trans_cus = TransDdb(
                    inc.inc_code,
                    inc.inc_date,
                    y.acc_code
                    if inc.inc_type == 1
                    else y.acc_bnk
                    if inc.acc_type == 1
                    else bnk_code,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    y.fc,
                    "K",
                    "JURNAL PEMASUKAN %s" % (inc.inc_code),
                    None,
                    None,
                )

                db.session.add(trans_cus)

            trans_inc = TransDdb(
                inc.inc_code,
                inc.inc_date,
                inc.inc_kas if inc.inc_type == 1 else inc_bnk,
                None,
                None,
                None,
                None,
                None,
                None,
                total,
                "D",
                "JURNAL PEMASUKAN %s" % (inc.inc_code),
                None,
                None,
            )

            db.session.add(trans_inc)

            # transbank = []

            # if inc.inc_type == 2 and inc.acc_type == 1:
            #     transbank.append(
            #         {
            #             "trx_code": inc.inc_code,
            #             "trx_date": inc.inc_date.isoformat(),
            #             "bank_id": inc.inc_bnk,
            #             "trx_amnt": total,
            #             "trx_dbcr": "D",
            #             "trx_desc": "TRX %s %s" % ("D", inc.inc_code),
            #         }
            #     )

            # if inc.inc_type == 2 and inc.acc_type == 2:
            #     transbank.append(
            #         {
            #             "trx_code": inc.inc_code,
            #             "trx_date": inc.inc_date.isoformat(),
            #             "bank_id": inc.inc_bnk,
            #             "trx_amnt": total,
            #             "trx_dbcr": "D",
            #             "trx_desc": "TRX %s %s" % ("D", inc.inc_code),
            #         }
            #     )
            #     for x in incs:
            #         transbank.append(
            #             {
            #                 "trx_code": inc.inc_code,
            #                 "trx_date": inc.inc_date.isoformat(),
            #                 "bank_id": x.bnk_code,
            #                 "trx_amnt": x.fc,
            #                 "trx_dbcr": "K",
            #                 "trx_desc": "TRX %s %s" % ("K", inc.inc_code),
            #             }
            #         )

        db.session.commit()
