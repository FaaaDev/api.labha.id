from sqlalchemy import and_
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
                                    x.id, inc.inc_date, penjualan.bkt_id, inc.inc_date, None, "K", penjualan.trx_type, "J4",
                                    penjualan.trx_amnh, None, x.payment, None, None, None, None, inc.giro_num, inc.giro_date, None, None, None )

                    db.session.add(ar_card)
                    db.session.commit()


        if delete:
            old_trans_cus = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code))).first()
            old_trans_inc = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code))).first()
            if old_trans_cus:
                db.session.delete(old_trans_cus)
            if old_trans_cus:
                db.session.delete(old_trans_inc)

        else:
            if inc.inc_type == 1:
                old_trans_cus = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code))).first()
                old_trans_inc = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code))).first()
                if old_trans_cus:
                    db.session.delete(old_trans_cus)
                if old_trans_cus:
                    db.session.delete(old_trans_inc)
                
                db.session.commit()

                if inc.bank_id:
                    bank = BankMdb.query.filter(BankMdb.id == inc.bank_id).first()
                    
                cus = (
                        db.session.query(CustomerMdb, PajakMdb)
                        .outerjoin(PajakMdb, PajakMdb.id == CustomerMdb.cus_pjk)
                        .filter(CustomerMdb.id == inc.acq_cus)
                        .first()
                    )
                # insert jurnal ap
                trans_cus = TransDdb(inc.inc_code, inc.inc_date, cus[0].cus_gl, None, None,
                                    None, None, None, None, total, "D", "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code), None, None)

                trans_inc = TransDdb(inc.inc_code, inc.inc_date, inc.acc_kas if inc.acq_pay == 1 else bank.acc_id, None, None,
                                    None, None, None, None, total, "K", "JURNAL PELUNASAN PENJUALAN %s"%(inc.inc_code), None, None)

                db.session.add(trans_cus)
                db.session.add(trans_inc)
                db.session.commit()
            else:
                old_trans_cus = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "D", TransDdb.trx_desc == "JURNAL PEMASUKAN %s"%(inc.inc_code))).first()
                old_trans_inc = TransDdb.query.filter(and_(TransDdb.trx_code == inc.inc_code, TransDdb.trx_dbcr == "K", TransDdb.trx_desc == "JURNAL PEMASUKAN %s"%(inc.inc_code))).all()
                if old_trans_cus:
                    db.session.delete(old_trans_cus)
                if old_trans_cus:
                    for x in old_trans_cus:
                        db.session.delete(x)
                
                db.session.commit()


                total = 0;
                trans_inc = []
                for x in incs:
                    total += x.value
                    trans_inc.append(TransDdb(inc.inc_code, inc.inc_date, x.acc_code, None, None,
                                    None, None, None, None, x.value, "D", "JURNAL PEMASUKAN %s"%(inc.inc_code), None, None))
                    
                # insert jurnal ap
                trans_cus = TransDdb(inc.inc_code, inc.inc_date, inc.inc_acc, None, None,
                                    None, None, None, None, total, "K", "JURNAL PEMASUKAN %s"%(inc.inc_code), None, None)

                

                db.session.add(trans_cus)
                db.session.add_all(trans_inc)
                db.session.commit()