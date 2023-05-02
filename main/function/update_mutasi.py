from sqlalchemy import and_
from ..model.djasa_ddb import DjasaDdb
from ..model.dprod_ddb import DprodDdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.hrgbl_mdb import HrgBlMdb
from ..model.jasa_mdb import JasaMdb
from ..model.lokasi_mdb import LocationMdb
from ..model.ordpb_hdb import OrdpbHdb
from ..model.prod_mdb import ProdMdb
from ..model.stcard_mdb import StCard
from ..model.transddb import TransDdb
from ..model.unit_mdb import UnitMdb
from ..model.mtsi_hdb import MtsiHdb
from ..model.mtsi_ddb import MtsiDdb
from ..shared.shared import db


class UpdateMutasi:
    def __init__(self, mtsi_id, delete):
        mtsi = MtsiHdb.query.filter(MtsiHdb.id == mtsi_id).first()

        product = MtsiDdb.query.filter(MtsiDdb.mtsi_id == mtsi_id).all()

        sto = StCard.query.filter(
            and_(StCard.trx_dbcr == "d", StCard.loc_id == mtsi.loc_from)
        ).all()

        if delete:
            old_st = StCard.query.filter(StCard.trx_code == mtsi.mtsi_code).all()
            if old_st:
                for x in old_st:
                    db.session.delete(x)
                db.session.commit()
        else:
            old_st = StCard.query.filter(StCard.trx_code == mtsi.mtsi_code).all()
            if old_st:
                for x in old_st:
                    db.session.delete(x)
                db.session.commit()
            st_k = []
            st_d = []
            for x in product:
                hrg_pokok = 0
                total_sto = 0

                for y in sto:
                    if x.prod_id == y.prod_id:
                        total_sto += y.trx_qty
                        hrg_pokok += y.trx_hpok

                st_k.append(
                    StCard(
                        mtsi.mtsi_code,
                        mtsi.mtsi_date,
                        "k",
                        "MD",
                        None,
                        x.qty,
                        None,
                        None,
                        x.qty*(hrg_pokok/total_sto),
                        None,
                        None,
                        x.prod_id,
                        mtsi.loc_from,
                        None,
                        0,
                        None,
                    )
                )

                st_d.append(
                    StCard(
                        mtsi.mtsi_code,
                        mtsi.mtsi_date,
                        "d",
                        "MK",
                        None,
                        x.qty,
                        None,
                        None,
                        x.qty*(hrg_pokok/total_sto),
                        None,
                        None,
                        x.prod_id,
                        mtsi.loc_from,
                        None,
                        0,
                        None,
                    )
                )

            if len(st_k) > 0:
                db.session.add_all(st_k)
            if len(st_d) > 0:
                db.session.add_all(st_d)

            db.session.commit()
