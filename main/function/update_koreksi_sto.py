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
from ..model.koreksi_sto_hdb import KorStoHdb
from ..model.koreksi_sto_ddb import KorStoDdb
from ..shared.shared import db


class UpdateKoreksiSto:
    def __init__(self, kor_id, delete):
        kor = KorStoHdb.query.filter(KorStoHdb.id == kor_id).first()

        product = KorStoDdb.query.filter(KorStoDdb.kor_id == kor_id).all()

        sto = StCard.query.filter(
            and_(StCard.trx_dbcr == "d", StCard.loc_id == KorStoDdb.location)
        ).all()

        if delete:
            old_st = StCard.query.filter(StCard.trx_code == kor.code).all()
            if old_st:
                for x in old_st:
                    db.session.delete(x)
                db.session.commit()
        else:
            old_st = StCard.query.filter(StCard.trx_code == kor.code).all()
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
                        kor.code,
                        kor.date,
                        "d" if x.dbcr == "D" else "k",
                        "KS",
                        None,
                        x.qty,
                        None,
                        None,
                        x.qty*(hrg_pokok/total_sto),
                        None,
                        None,
                        x.prod_id,
                        x.location,
                        None,
                        0,
                        None,
                    )
                )

                # st_d.append(
                #     StCard(
                #         kor.code,
                #         kor.date,
                #         "d",
                #         "KD",
                #         None,
                #         x.qty,
                #         None,
                #         None,
                #         x.qty*(hrg_pokok/total_sto),
                #         None,
                #         None,
                #         x.prod_id,
                #         x.location,
                #         None,
                #         0,
                #         None,
                #     )
                # )

            if len(st_k) > 0:
                db.session.add_all(st_k)
            # if len(st_d) > 0:
            #     db.session.add_all(st_d)

            db.session.commit()
