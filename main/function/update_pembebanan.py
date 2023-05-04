from sqlalchemy import and_, or_
from main.model.direct_batch_mdb import DirectBatchMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.btcprod_ddb import BtcprodDdb
from main.model.btcmtrl_ddb import BtcmtrlDdb
from main.model.btcrejc_ddb import BtcrejcDdb
from main.model.ccost_mdb import CcostMdb
from main.model.transddb import TransDdb
from main.model.stcard_mdb import StCard
from main.model.group_prod_mdb import GroupProMdb
from main.model.prod_mdb import ProdMdb
from main.model.unit_mdb import UnitMdb
from main.model.msn_mdb import MsnMdb
from main.model.pbb_hdb import PbbHdb
from main.model.upah_ddb import UpahDdb
from main.model.overhead_ddb import OverhDdb
from main.model.pbprod_ddb import PbprodDdb
from main.model.pbpanen_ddb import PbpanenDdb
from main.model.comp_mdb import CompMdb
from main.shared.shared import db


class updatePembebanan:
    def __init__(self, pbb_id, user_product, user_company, delete):
        try:
            pbb = (
                db.session.query(PbbHdb, DirectBatchMdb)
                .outerjoin(DirectBatchMdb, DirectBatchMdb.id == PbbHdb.batch_id)
                .filter(PbbHdb.id == pbb_id)
                .first()
            )

            prod = (
                db.session.query(BtcprodDdb, ProdMdb, GroupProMdb, DirectBatchMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(DirectBatchMdb, DirectBatchMdb.id == BtcprodDdb.btc_id)
                .filter(BtcprodDdb.btc_id == pbb[0].batch_id)
                .all()
            )

            mtr = (
                db.session.query(BtcmtrlDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcmtrlDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(BtcmtrlDdb.btc_id == pbb[0].batch_id)
                .all()
            )

            rej = (
                db.session.query(BtcrejcDdb, ProdMdb, GroupProMdb, DirectBatchMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcrejcDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(DirectBatchMdb, DirectBatchMdb.id == BtcrejcDdb.btc_id)
                .filter(BtcrejcDdb.btc_id == pbb[0].batch_id)
                .all()
            )

            pbprod = (
                db.session.query(PbprodDdb, ProdMdb, GroupProMdb, StCard)
                .outerjoin(ProdMdb, ProdMdb.id == PbprodDdb.prd_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(StCard, StCard.id == PbprodDdb.trn_id)
                .filter(PbprodDdb.pbb_id == pbb[0].id)
                .all()
            )

            pbpanen = (
                db.session.query(PbpanenDdb, ProdMdb, GroupProMdb, StCard)
                .outerjoin(ProdMdb, ProdMdb.id == PbpanenDdb.prd_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(StCard, StCard.id == PbpanenDdb.trn_id)
                .filter(PbpanenDdb.pbb_id == pbb[0].id)
                .all()
            )

            sto = StCard.query.filter(
                or_(
                    StCard.trx_type == "PJ",
                    StCard.trx_type == "HRV",
                    StCard.trx_type == "MD",
                    StCard.trx_type == "MK",
                )
            ).all()

            st = (
                db.session.query(StCard, ProdMdb, GroupProMdb, LocationMdb)
                .outerjoin(ProdMdb, ProdMdb.id == StCard.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .outerjoin(LocationMdb, LocationMdb.id == StCard.loc_id)
                .all()
            )

            comp = CompMdb.query.filter(CompMdb.id == user_company).first()

            uph = UpahDdb.query.filter(UpahDdb.pbb_id == pbb_id).all()

            ovr = OverhDdb.query.filter(OverhDdb.pbb_id == pbb_id).all()

            # Update Jurnal

            amnt_uph = 0
            amnt_ovr = 0
            amnt_prod_u = 0
            amnt_prod_o = 0
            amnt_rej = 0
            t_biaya = 0

            for x in uph:
                amnt_uph += x.nom_uph
            for x in ovr:
                amnt_ovr += x.nom_ovr

            t_biaya = amnt_uph + amnt_ovr

            if delete:
                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == pbb[0].pbb_code
                ).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

                for z in sto:
                    t_qty = 0
                    if pbb[0].type_pb == 1:
                        if z.trx_hpok:
                            if pbb[1].bcode == z.trx_code:

                                for a in prod:
                                    if (
                                        z.trx_code == a[3].bcode
                                        and z.prod_id == a[0].prod_id
                                    ):
                                        z.trx_b_hpok = None
                                        z.trx_hpok = z.trx_hpok - (
                                            t_biaya * a[0].aloc / 100
                                        )
                                        z.flag = z.flag - 1

                                if z.trx_hpok != None:
                                    for b in rej:
                                        if (
                                            z.trx_code == b[3].bcode
                                            and z.prod_id == b[0].prod_id
                                        ):
                                            z.trx_b_hpok = None
                                            z.trx_hpok = z.trx_hpok - (
                                                t_biaya * b[0].aloc / 100
                                            )
                                            z.flag = z.flag - 1

                    if pbb[0].type_pb == 2:
                        if z.trx_hpok:
                            for x in pbprod:
                                aloc_b = 0
                                if x[0].trn_id == z.id and x[0].prd_id == z.prod_id:
                                    aloc_b = t_biaya * x[0].aloc / 100
                                    z.trx_b_hpok = None
                                    z.trx_hpok = z.trx_hpok - (
                                        aloc_b * x[0].aloc_qty / 100
                                    )
                                    z.flag = z.flag - 1

                    if pbb[0].type_pb == 3:
                        if z.trx_hpok:
                            for x in pbpanen:
                                aloc_b = 0
                                if (
                                    x[0].trn_id == z.id
                                    and x[0].prd_id == z.prod_id
                                    and pbb[0].panen_loc == z.loc_id
                                ):
                                    aloc_b = t_biaya * x[0].aloc / 100
                                    z.trx_b_hpok = None
                                    z.trx_hpok = z.trx_hpok - aloc_b
                                    z.flag = z.flag - 1

            else:
                # Insert Jurnal Pembebanan
                for z in sto:
                    t_qty = 0
                    if pbb[0].type_pb == 1:
                        if pbb[1].bcode == z.trx_code:
                            for a in prod:
                                if (
                                    z.trx_code == a[3].bcode
                                    and z.prod_id == a[0].prod_id
                                ):
                                    if z.trx_b_hpok != None:
                                        z.trx_hpok = z.trx_b_hpok + (
                                            t_biaya * a[0].aloc / 100
                                        )
                                    else:
                                        z.trx_b_hpok = z.trx_hpok
                                        z.trx_hpok = z.trx_hpok + (
                                            t_biaya * a[0].aloc / 100
                                        )
                                        z.flag = z.flag + 1

                            if z.trx_hpok != None:
                                for b in rej:
                                    if (
                                        z.trx_code == b[3].bcode
                                        and z.prod_id == b[0].prod_id
                                    ):
                                        if z.trx_b_hpok != None:
                                            z.trx_hpok = z.trx_b_hpok + (
                                                t_biaya * b[0].aloc / 100
                                            )
                                        else:
                                            z.trx_b_hpok = z.trx_hpok
                                            z.trx_hpok = z.trx_hpok + (
                                                t_biaya * b[0].aloc / 100
                                            )
                                            z.flag = z.flag + 1

                    if pbb[0].type_pb == 2:
                        for x in pbprod:
                            aloc_b = 0
                            if x[0].trn_id == z.id and x[0].prd_id == z.prod_id:
                                aloc_b = t_biaya * x[0].aloc / 100
                                if z.trx_b_hpok != None:
                                    z.trx_hpok = z.trx_b_hpok + (
                                        aloc_b * x[0].aloc_qty / 100
                                    )
                                else:
                                    z.trx_b_hpok = z.trx_hpok
                                    z.trx_hpok = z.trx_hpok + (
                                        aloc_b * x[0].aloc_qty / 100
                                    )
                                    z.flag = z.flag + 1

                    if pbb[0].type_pb == 3:
                        for x in pbpanen:
                            aloc_b = 0
                            if (
                                x[0].trn_id == z.id
                                and x[0].prd_id == z.prod_id
                                and pbb[0].panen_loc == z.loc_id
                            ):
                                aloc_b = t_biaya * x[0].aloc / 100
                                if z.trx_b_hpok != None:
                                    z.trx_hpok = z.trx_b_hpok + aloc_b
                                else:
                                    z.trx_b_hpok = z.trx_hpok
                                    z.trx_hpok = z.trx_hpok + aloc_b
                                    z.flag = z.flag + 1

                if user_product == "inv+gl":
                    # Insert Jurnal Upah

                    old_trans = TransDdb.query.filter(
                        TransDdb.trx_code == pbb[0].pbb_code
                    ).all()

                    if old_trans:
                        for x in old_trans:
                            db.session.delete(x)

                    for x in uph:
                        # if pbb[0].type_pb == 1:
                        new_trans_uph = TransDdb(
                            pbb[0].pbb_code,
                            pbb[0].pbb_date,
                            x.acc_id,
                            pbb[1].dep_id if pbb[0].type_pb == 1 else None,
                            pbb[0].proj_id,
                            None,
                            None,
                            None,
                            None,
                            x.nom_uph,
                            "K",
                            "JURNAL PEMBEBANAN BIAYA %s"
                            % (pbb[1].bcode if pbb[0].type_pb == 1 else ""),
                            None,
                            None,
                        )
                        # if len(new_trans_uph) > 0:
                        db.session.add(new_trans_uph)


                    # Insert Jurnal Pembebanan K
                    amnt_pm = 0
                    amnt_pj = 0
                    amnt_pr = 0
                    acc_prd = None
                    acc_prd_pnn = None
                    code = None
                    hpp_pm = 0
                    hpp_pj = 0
                    hpp_pr = 0
                    hpp_pnn = 0
                    for s in st:
                        trx_code = None
                        if pbb[0].type_pb == 1:
                            if s[0].trx_code == pbb[1].bcode:
                                if s[0].trx_type == "PM":
                                    amnt_pm += s[0].trx_hpok

                                if s[0].trx_type == "PJ":
                                    amnt_pj += s[0].trx_hpok

                                if s[0].trx_type == "PR":
                                    amnt_pr += s[0].trx_hpok

                        if pbb[0].type_pb == 2:
                            for a in pbprod:
                                if a[3].trx_code == s[0].trx_code:
                                    # trx_code = s[0].trx_code
                                    if s[0].trx_type == "PM":
                                        hpp_pm += s[0].trx_hpok
                                        if comp.gl_detail:
                                            if s[2].wip:
                                                acc_prd = s[1].acc_wip
                                            else:
                                                acc_prd = s[1].acc_sto

                                        else:
                                            if s[2].wip:
                                                acc_prd = s[2].acc_wip
                                            else:
                                                acc_prd = s[2].acc_sto

                                    if s[0].trx_type == "PJ":
                                        hpp_pj += s[0].trx_hpok
                                        if comp.gl_detail:
                                            if a[2].wip:
                                                acc_prd = a[1].acc_wip
                                            else:
                                                acc_prd = a[1].acc_sto

                                        else:
                                            if a[2].wip:
                                                acc_prd = a[2].acc_wip
                                            else:
                                                acc_prd = a[2].acc_sto

                        if pbb[0].type_pb == 3:
                            for a in pbpanen:
                                if a[0].trn_id == s[0].id:
                                    hpp_pnn += s[0].trx_hpok

                    acc = None
                    if pbb[0].type_pb != 3:
                        for m in mtr:
                            if comp.gl_detail:
                                if m[2].wip:
                                    acc = m[1].acc_wip
                                else:
                                    acc = m[1].acc_sto

                            else:
                                if m[2].wip:
                                    acc = m[2].acc_wip
                                else:
                                    acc = m[2].acc_sto

                        new_trans_pm = TransDdb(
                            pbb[0].pbb_code,
                            pbb[0].pbb_date,
                            acc if pbb[0].type_pb == 1 else acc_prd,
                            pbb[1].dep_id if pbb[0].type_pb == 1 else None,
                            pbb[0].proj_id,
                            None,
                            None,
                            None,
                            None,
                            amnt_pm if pbb[0].type_pb == 1 else hpp_pm,
                            "K",
                            "JURNAL PEMBEBANAN MATERIAL %s"
                            % (pbb[1].bcode if pbb[0].type_pb == 1 else ""),
                            None,
                            None,
                        )
                        db.session.add(new_trans_pm)

                        acc_p = None
                        for p in prod:
                            if comp.gl_detail:
                                if p[2].wip:
                                    acc_p = p[1].acc_wip
                                else:
                                    acc_p = p[1].acc_sto

                            else:
                                if p[2].wip:
                                    acc_p = p[2].acc_wip
                                else:
                                    acc_p = p[2].acc_sto

                        new_trans_pj = TransDdb(
                            pbb[0].pbb_code,
                            pbb[0].pbb_date,
                            acc_p if pbb[0].type_pb == 1 else acc_prd,
                            pbb[1].dep_id if pbb[0].type_pb == 1 else None,
                            pbb[0].proj_id,
                            None,
                            None,
                            None,
                            None,
                            amnt_pj if pbb[0].type_pb == 1 else hpp_pj,
                            "D",
                            "JURNAL PEMBEBANAN ATAS FINISH GOOD %s"
                            % (pbb[1].bcode if pbb[0].type_pb == 1 else ""),
                            None,
                            None,
                        )
                        db.session.add(new_trans_pj)

                        acc_r = None
                        for r in rej:
                            if comp.gl_detail:
                                if r[2].wip:
                                    acc_r = r[1].acc_wip
                                else:
                                    acc_r = r[1].acc_sto

                            else:
                                if r[2].wip:
                                    acc_r = r[2].acc_wip
                                else:
                                    acc_r = r[2].acc_sto

                        if len(rej) > 0:
                            new_trans_pr = TransDdb(
                                pbb[0].pbb_code,
                                pbb[0].pbb_date,
                                acc_p if pbb[0].type_pb == 1 else acc_prd,
                                pbb[1].dep_id if pbb[0].type_pb == 1 else None,
                                pbb[0].proj_id,
                                None,
                                None,
                                None,
                                None,
                                amnt_pr,
                                "D",
                                "JURNAL PEMBEBANAN ATAS PROD REJECT %s"
                                % (pbb[1].bcode if pbb[0].type_pb == 1 else ""),
                                None,
                                None,
                            )
                        db.session.add(new_trans_pr)

                    else:
                        acc_pnn = None
                        for p in pbpanen:
                            if comp.gl_detail:
                                if p[2].wip:
                                    acc_pnn = p[1].acc_wip
                                else:
                                    acc_pnn = p[1].acc_sto

                            else:
                                if p[2].wip:
                                    acc_pnn = p[2].acc_wip
                                else:
                                    acc_pnn = p[2].acc_sto

                        new_trans_pnn = TransDdb(
                            pbb[0].pbb_code,
                            pbb[0].pbb_date,
                            acc_pnn,
                            pbb[0].dep_id if pbb[0].type_pb == 1 else None,
                            pbb[0].proj_id,
                            None,
                            None,
                            None,
                            None,
                            hpp_pnn,
                            "D",
                            "JURNAL PEMBEBANAN ATAS %s" % (p[3].trx_code),
                            None,
                            None,
                        )
                        db.session.add(new_trans_pnn)

            db.session.commit()

        except Exception as e:
            print(e)
