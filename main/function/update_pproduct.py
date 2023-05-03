from sqlalchemy import and_
from main.model.prod_asal_ddb import PAsalDdb
from main.model.prod_jadi_ddb import PJadiDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.hrgbl_mdb import HrgBlMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.pproduct_hdb import PproductHdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.comp_mdb import CompMdb
from main.shared.shared import db
import requests
from main.utils.response import response


class UpdatePerubahanProd:
    def __init__(self, pp_id, delete, user_product, user_company):
        pp = PproductHdb.query.filter(PproductHdb.id == pp_id).first()

        comp = CompMdb.query.filter(CompMdb.id == user_company).first()

        pasal = (
            db.session.query(PAsalDdb, ProdMdb, GroupProMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == PAsalDdb.prod_id)
            .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
            .outerjoin(LocationMdb, LocationMdb.id == PAsalDdb.loc_id)
            .filter(PAsalDdb.pp_id == pp_id)
            .all()
        )

        pjadi = (
            db.session.query(PJadiDdb, ProdMdb, GroupProMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == PJadiDdb.prod_id)
            .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
            .outerjoin(LocationMdb, LocationMdb.id == PJadiDdb.loc_id)
            .filter(PJadiDdb.pp_id == pp_id)
            .all()
        )

        sto = StCard.query.filter(and_(StCard.trx_dbcr == "d")).all()

        if delete:
            old_trans = TransDdb.query.filter(TransDdb.trx_code == pp.pp_code).all()

            old_sto = StCard.query.filter(StCard.trx_code == pp.pp_code).all()

            if old_trans:
                for x in old_trans:
                    db.session.delete(x)

            if old_sto:
                for x in old_sto:
                    db.session.delete(x)

        else:
            old_trans = TransDdb.query.filter(TransDdb.trx_code == pp.pp_code).all()

            old_sto = StCard.query.filter(StCard.trx_code == pp.pp_code).all()

            if old_trans:
                for x in old_trans:
                    db.session.delete(x)

            if old_sto:
                for x in old_sto:
                    db.session.delete(x)

            trans_pasal = []
            sto_pasal = []
            trans_pjadi = []
            sto_pjadi = []

            hpp = 0
            for x in pasal:
                hrg_pokok = 0
                total_sto = 0

                for y in sto:
                    if x[0].prod_id == y.prod_id:
                        if x[0].loc_id == y.loc_id:
                            total_sto += y.trx_qty
                            hrg_pokok += y.trx_hpok

                hpp = hrg_pokok / total_sto

                sto_pasal.append(
                    StCard(
                        pp.pp_code,
                        pp.pp_date,
                        "k",
                        "PPA",
                        None,
                        x[0].qty,
                        None,
                        None,
                        hpp * x[0].qty,
                        None,
                        None,
                        None,
                        x[0].prod_id,
                        x[0].loc_id,
                        None,
                        0,
                        0,
                        None,
                    )
                )

                if user_product == "inv+gl":
                    trans_pasal.append(
                        TransDdb(
                            pp.pp_code,
                            pp.pp_date,
                            x[2].acc_wip
                            if x[2].wip
                            else x[2].acc_sto
                            if comp.gl_detail == False
                            else x[1].acc_wip
                            if x[2].wip
                            else x[1].acc_sto,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            hpp * x[0].qty,
                            "K",
                            "JURNAL PERUBAHAN PRODUK ASAL %s %s"
                            % (x[1].name, pp.pp_code),
                            None,
                            None,
                        )
                    )

                db.session.add_all(sto_pasal)
                db.session.add_all(trans_pasal)

            # Update Kartu Stock

            for x in pjadi:
                # hrg_pokok = 0
                # total_sto = 0

                # for y in sto:
                #     if x[0].prod_id == y.prod_id:
                #         total_sto += y.trx_qty
                #         hrg_pokok += y.trx_hpok

                sto_pjadi.append(
                    StCard(
                        pp.pp_code,
                        pp.pp_date,
                        "d",
                        "PPJ",
                        None,
                        x[0].qty,
                        None,
                        None,
                        hpp * x[0].qty,
                        None,
                        None,
                        None,
                        x[0].prod_id,
                        x[0].loc_id,
                        None,
                        0,
                        0,
                        None,
                    )
                )

                if user_product == "inv+gl":
                    trans_pjadi.append(
                        TransDdb(
                            pp.pp_code,
                            pp.pp_date,
                            x[2].acc_wip
                            if x[2].wip
                            else x[2].acc_sto
                            if comp.gl_detail == False
                            else x[1].acc_wip
                            if x[2].wip
                            else x[1].acc_sto,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            hpp * x[0].qty,
                            "D",
                            "JURNAL PERUBAHAN PRODUK JADI %s %s"
                            % (x[1].name, pp.pp_code),
                            None,
                            None,
                        )
                    )

                db.session.add_all(sto_pjadi)
                db.session.add_all(trans_pjadi)

        db.session.commit()
