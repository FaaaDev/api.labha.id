from operator import and_
from main.model.ccost_mdb import CcostMdb
from main.model.fmtrl_ddb import FmtrlDdb
from main.model.fprdc_hdb import FprdcHdb
from main.model.fprod_ddb import FprodDdb
from main.model.lokasi_mdb import LocationMdb
from main.model.plan_hdb import PlanHdb
from main.model.prod_mdb import ProdMdb
from main.model.rpbb_mdb import RpbbMdb
from main.model.stcard_mdb import StCard
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class UpdateRpbb:
    def __init__(self, pl_id, delete):
        if delete:
            old_rpbb = RpbbMdb.query.filter(RpbbMdb.pl_id == pl_id).all()
            if old_rpbb:
                for x in old_rpbb:
                    db.session.delete(x)
                db.session.commit()
        else:
            old_rpbb = RpbbMdb.query.filter(RpbbMdb.pl_id == pl_id).all()
            if old_rpbb:
                for x in old_rpbb:
                    db.session.delete(x)
                db.session.commit()

            plan = PlanHdb.query.filter(PlanHdb.id == pl_id).first()

            material = (
                db.session.query(FmtrlDdb, ProdMdb, UnitMdb)
                .outerjoin(ProdMdb, ProdMdb.id == FmtrlDdb.prod_id)
                .outerjoin(UnitMdb, UnitMdb.id == FmtrlDdb.unit_id)
                .filter(FmtrlDdb.form_id == plan.form_id)
                .all()
            )

            sto = StCard.query.filter().all()

            all_rpbb = []
            for x in material:
                total_sto = 0

                for y in sto:
                    if x[0].prod_id == y.prod_id and plan.loc_id == y.loc_id:
                        if y.trx_dbcr == "d":
                            total_sto += y.trx_qty
                        else:
                            total_sto -= y.trx_qty

                pl = x[0].qty * plan.total
                sisa = total_sto - pl

                all_rpbb.append(
                    RpbbMdb(
                        plan.id,
                        x[0].prod_id,
                        total_sto,
                        pl,
                        sisa,
                        pl - total_sto if sisa < 0 else 0,
                        plan.loc_id,
                    )
                )

            if len(all_rpbb) > 0:
                db.session.add_all(all_rpbb)

            db.session.commit()
