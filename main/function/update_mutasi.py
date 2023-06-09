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
from main.model.mtsi_hdb import MtsiHdb
from main.model.mtsi_ddb import MtsiDdb
from main.shared.shared import db


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

            for p in product:
                st_panen = StCard.query.filter(
                    and_(
                        StCard.trx_type == "HRV",
                        StCard.loc_id == mtsi.loc_from,
                        StCard.prod_id == p.prod_id,
                    )
                ).all()

                if st_panen:
                    for x in st_panen:
                        x.mtsi = x.mtsi - 1
                        db.session.commit()

        else:
            old_st = StCard.query.filter(StCard.trx_code == mtsi.mtsi_code).all()
            if old_st:
                for x in old_st:
                    db.session.delete(x)

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
                        "MK",
                        None,
                        x.qty,
                        None,
                        None,
                        (hrg_pokok / total_sto) * x.qty,
                        None,
                        None,
                        x.prod_id,
                        mtsi.loc_from,
                        None,
                        0,
                        0,
                    )
                )

                st_d.append(
                    StCard(
                        mtsi.mtsi_code,
                        mtsi.mtsi_date,
                        "d",
                        "MD",
                        None,
                        x.qty_terima,
                        None,
                        None,
                        (hrg_pokok / total_sto) * x.qty,
                        None,
                        None,
                        x.prod_id,
                        mtsi.loc_to,
                        None,
                        0,
                        0,
                    )
                )

            if len(st_k) > 0:
                db.session.add_all(st_k)
            if len(st_d) > 0:
                db.session.add_all(st_d)

        db.session.commit()
