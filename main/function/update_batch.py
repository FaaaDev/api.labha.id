from sqlalchemy import and_
from main.model.batch_mdb import BatchMdb
from main.model.plan_hdb import PlanHdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fprod_ddb import FprodDdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.ccost_mdb import CcostMdb
from main.model.transddb import TransDdb
from main.model.stcard_mdb import StCard
from main.model.group_prod_mdb import GroupProMdb
from main.model.prod_mdb import ProdMdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class updateBatch:
    def __init__(self, batch_id, delete):


        btc = (db.session.query(BatchMdb, PlanHdb, FprdcHdb, CcostMdb)
            .outerjoin(PlanHdb, PlanHdb.id == BatchMdb.plan_id)
            .outerjoin(FprdcHdb, FprdcHdb.id == PlanHdb.form_id)
            .outerjoin(CcostMdb, CcostMdb.id == BatchMdb.dep_id)
            .filter(BatchMdb.id == batch_id)
            .first())

        product = (db.session.query(FprodDdb, ProdMdb, GroupProMdb)
                  .outerjoin(ProdMdb, ProdMdb.id == FprodDdb.prod_id)
                  .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                  .filter(FprodDdb.form_id == btc[2].id)
                  .all())

        material = (db.session.query(FmtrlDdb, ProdMdb, GroupProMdb)
                  .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
                  .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                  .filter(FmtrlDdb.form_id == btc[2].id)
                  .all())

        sto = StCard.query.filter(and_(StCard.trx_dbcr == "d", StCard.trx_type == "BL")).all()

        if delete:
            old_trans_prod = TransDdb.query.filter(TransDdb.trx_code == btc[0].bcode).all()

            if old_trans_prod:
                for x in old_trans_prod:
                    db.session.delete(x)
                    db.session.commit()


        else:
            for x in product:
                hrg_pokok = 0
                total_sto = 0

                for y in sto:
                    if x[0].prod_id == y.prod_id:
                        total_sto += y.trx_qty 
                        hrg_pokok += y.trx_hpok


                trans_btc_prod = TransDdb(
                    btc[0].bcode,
                    btc[0].batch_date,
                    x[2].acc_wip if x[2].wip else x[2].acc_sto,
                    btc[3].id,
                    None,
                    None,
                    None,
                    None,
                    None,
                    hrg_pokok / total_sto,
                    "D",
                    "JURNAL PRODUKSI WIP %s %s" % (x[1].name, btc[0].bcode),
                    None,
                    None,
                )

                db.session.add(trans_btc_prod)
                db.session.commit()


        if delete:
            old_trans_mtrl = TransDdb.query.filter(TransDdb.trx_code == btc[0].bcode).all()

            if old_trans_mtrl:
                for x in old_trans_mtrl:
                    db.session.delete(x)
                    db.session.commit()


        else:
            for x in material:
                hrg_pokok = 0
                total_sto = 0

                for y in sto:
                    if x[0].prod_id == y.prod_id:
                        total_sto += y.trx_qty 
                        hrg_pokok += y.trx_hpok


                trans_btc_mtrl = TransDdb(
                    btc[0].bcode,
                    btc[0].batch_date,
                    x[2].acc_sto,
                    btc[3].id,
                    None,
                    None,
                    None,
                    None,
                    None,
                    hrg_pokok / total_sto,
                    "K",
                    "JURNAL PRODUKSI %s %s" % (x[1].name, btc[0].bcode),
                    None,
                    None,
                )

                db.session.add(trans_btc_mtrl)
                db.session.commit()