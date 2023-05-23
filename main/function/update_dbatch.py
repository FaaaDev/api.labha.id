from sqlalchemy import and_, extract
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
from main.model.comp_mdb import CompMdb
from main.model.exp_hdb import ExpHdb
from main.model.wages_ddb import WagesDdb
from main.model.costs_ddb import CostsDdb
from main.model.usage_material_hdb import UsageMatHdb
from main.model.usage_material_ddb import UsageMatDdb
from main.model.usage_material_biaya_ddb import UsageMatBiayaDdb
from main.shared.shared import db


class updateDirectBatch:
    hpok = 0

    def __init__(self, batch_id, bp_id, user_product, user_company, delete):

        try:
            btc = (
                db.session.query(DirectBatchMdb, MsnMdb, LocationMdb, CcostMdb)
                .outerjoin(MsnMdb, MsnMdb.id == DirectBatchMdb.msn_id)
                .outerjoin(LocationMdb, LocationMdb.id == DirectBatchMdb.loc_id)
                .outerjoin(CcostMdb, CcostMdb.id == DirectBatchMdb.dep_id)
                .filter(DirectBatchMdb.id == batch_id)
                .first()
            )

            product = (
                db.session.query(BtcprodDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcprodDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(BtcprodDdb.btc_id == batch_id)
                .all()
            )

            material = (
                db.session.query(BtcmtrlDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcmtrlDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(BtcmtrlDdb.btc_id == batch_id)
                .all()
            )

            reject = (
                db.session.query(BtcrejcDdb, ProdMdb, GroupProMdb)
                .outerjoin(ProdMdb, ProdMdb.id == BtcrejcDdb.prod_id)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .filter(BtcrejcDdb.btc_id == batch_id)
                .all()
            )

            useMatHdb = UsageMatHdb.query.filter(
                UsageMatHdb.id == DirectBatchMdb.mat_id
            ).first()

            useMatDdb = UsageMatDdb.query.filter(
                UsageMatDdb.um_id == useMatHdb.id
            ).all()

            useMatBiaya = UsageMatBiayaDdb.query.filter(
                UsageMatBiayaDdb.um_id == useMatHdb.id
            ).all()

            wages = WagesDdb.query.filter(WagesDdb.btc_id == batch_id).all()

            comp = CompMdb.query.filter(CompMdb.id == user_company).first()

            sto = StCard.query.filter(and_(StCard.trx_dbcr == "d")).all()

            exps = ExpHdb.query.all()

            # cost = CostsDdb.query.all()

            # Update Jurnal
            if delete:
                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == btc[0].bcode
                ).all()

                old_sto = StCard.query.filter(StCard.trx_code == btc[0].bcode).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)

                if old_sto:
                    for x in old_sto:
                        db.session.delete(x)

                # db.session.commit()

            else:
                old_trans = TransDdb.query.filter(
                    TransDdb.trx_code == btc[0].bcode
                ).all()

                old_sto = StCard.query.filter(StCard.trx_code == btc[0].bcode).all()

                if old_trans:
                    for x in old_trans:
                        db.session.delete(x)
                    # db.session.commit()

                if old_sto:
                    for x in old_sto:
                        db.session.delete(x)
                    # db.session.commit()

                trans_btc_mtrl = []
                sto_btc_mtrl = []
                trans_btc_rej = []
                sto_btc_rej = []
                trans_btc_prod = []
                sto_btc_prod = []
                trans_btc_wgs = []
                trans_biaya_mat = []

                total_wgs = 0
                for z in wages:
                    total_wgs += z.nom_wgs

                for x in material:
                    hrg_pokok = 0
                    total_sto = 0
                    t_hpok = 0
                    hpp = 0

                    if btc[0].mat_id == None:
                        for y in sto:
                            if x[0].prod_id == y.prod_id and btc[0].loc_id == y.loc_id:
                                total_sto += y.trx_qty
                                hrg_pokok += y.trx_hpok

                        t_hpok = hrg_pokok + total_wgs
                        hpp = (t_hpok / total_sto) * x[0].qty

                    else:
                        t_biaya_mat = 0

                        for b in useMatBiaya:
                            t_biaya_mat += b.value

                        for y in sto:
                            if x[0].prod_id == y.prod_id and btc[0].loc_id == y.loc_id:
                                total_sto += y.trx_qty
                                hrg_pokok += y.trx_hpok

                        t_hpok = hrg_pokok + t_biaya_mat + total_wgs
                        hpp = (t_hpok / total_sto) * x[0].qty

                    print("========t_b_mat===========")
                    print(t_biaya_mat)
                    print("========t_wgs===========")
                    print(total_wgs)
                    print("========t_hpok===========")
                    print(t_hpok)
                    print("========hrg_pok===========")
                    print(hrg_pokok)
                    print("========t_sto===========")
                    print(total_sto)
                    print("========hpp===========")
                    print(hpp)

                    sto_btc_mtrl.append(
                        StCard(
                            btc[0].bcode,
                            btc[0].batch_date,
                            "k",
                            "PM",
                            None,
                            x[0].qty,
                            None,
                            None,
                            hpp,
                            None,
                            None,
                            None,
                            x[0].prod_id,
                            btc[0].loc_id,
                            None,
                            None,
                            0,
                            None,
                        )
                    )

                    acc = None
                    if comp.gl_detail:
                        if x[2].wip:
                            acc = x[1].acc_wip
                        else:
                            acc = x[1].acc_sto

                    else:
                        if x[2].wip:
                            acc = x[2].acc_wip
                        else:
                            acc = x[2].acc_sto

                    if user_product == "inv+gl":
                        trans_btc_mtrl.append(
                            TransDdb(
                                btc[0].bcode,
                                btc[0].batch_date,
                                acc,
                                btc[0].dep_id,
                                None,
                                None,
                                None,
                                None,
                                None,
                                hpp - total_wgs - t_biaya_mat
                                if btc[0].mat_id
                                else hpp - total_wgs - t_biaya_mat,
                                "K",
                                "JURNAL PEMAKAIAN %s %s" % (x[1].name, btc[0].bcode),
                                None,
                                None,
                            )
                        )

                    self.hpok += hpp

                db.session.add_all(sto_btc_mtrl)
                db.session.add_all(trans_btc_mtrl)

                # Update Kartu Stock

                for x in product:
                    # hrg_pokok = 0
                    # total_sto = 0

                    # for y in sto:
                    #     if x[0].prod_id == y.prod_id:
                    #         total_sto += y.trx_qty
                    #         hrg_pokok += y.trx_hpok

                    sto_btc_prod.append(
                        StCard(
                            btc[0].bcode,
                            btc[0].batch_date,
                            "d",
                            "PJ",
                            None,
                            x[0].qty,
                            None,
                            None,
                            self.hpok * x[0].aloc / 100,
                            None,
                            None,
                            None,
                            x[0].prod_id,
                            x[0].loc_id if x[0].loc_id != None else btc[0].loc_id,
                            None,
                            None,
                            1 if total_wgs > 0 or total_wgs != None else 0,
                            None,
                        )
                    )

                    acc_pj = None
                    if comp.gl_detail:
                        if x[2].wip:
                            acc_pj = x[1].acc_wip
                        else:
                            acc_pj = x[1].acc_sto

                    else:
                        if x[2].wip:
                            acc_pj = x[2].acc_wip
                        else:
                            acc_pj = x[2].acc_sto

                    if user_product == "inv+gl":
                        trans_btc_prod.append(
                            TransDdb(
                                btc[0].bcode,
                                btc[0].batch_date,
                                acc_pj,
                                btc[0].dep_id,
                                None,
                                None,
                                None,
                                None,
                                None,
                                self.hpok * x[0].aloc / 100,
                                "D",
                                "JURNAL PRD JADI %s %s" % (btc[0].bcode, x[1].name),
                                None,
                                None,
                            )
                        )

                db.session.add_all(sto_btc_prod)
                db.session.add_all(trans_btc_prod)

                # Jurnal Produk Reject masuk kalo alocasinya tidak null

                for x in reject:
                    # hrg_pokok = 0
                    # total_sto = 0

                    # for y in sto:
                    #     if x[0].prod_id == y.prod_id:
                    #         total_sto += y.trx_qty
                    #         hrg_pokok += y.trx_hpok

                    sto_btc_rej.append(
                        StCard(
                            btc[0].bcode,
                            btc[0].batch_date,
                            "d",
                            "PR",
                            None,
                            x[0].qty,
                            None,
                            None,
                            self.hpok * x[0].aloc / 100 if x[0].aloc != None else None,
                            None,
                            None,
                            None,
                            x[0].prod_id,
                            x[0].loc_id if x[0].loc_id != None else btc[0].loc_id,
                            None,
                            None,
                            1
                            if total_wgs > 0 or total_wgs != None and x[0].aloc != None
                            else 0,
                            None,
                        )
                    )

                    acc_rj = None
                    if comp.gl_detail:
                        if x[2].wip:
                            acc_rj = x[1].acc_wip
                        else:
                            acc_rj = x[1].acc_sto

                    else:
                        if x[2].wip:
                            acc_rj = x[2].acc_wip
                        else:
                            acc_rj = x[2].acc_sto

                    if user_product == "inv+gl":
                        if x[0].aloc != None:
                            trans_btc_rej.append(
                                TransDdb(
                                    btc[0].bcode,
                                    btc[0].batch_date,
                                    acc_rj,
                                    btc[0].dep_id,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    self.hpok * x[0].aloc / 100
                                    if x[0].aloc != None
                                    else None,
                                    "D",
                                    "JURNAL PRD REJECT %s %s"
                                    % (btc[0].bcode, x[1].name),
                                    None,
                                    None,
                                )
                            )

                db.session.add_all(sto_btc_rej)
                db.session.add_all(trans_btc_rej)

                # Jurnal Biaya Wages
                for x in wages:
                    if user_product == "inv+gl":
                        trans_btc_wgs.append(
                            TransDdb(
                                btc[0].bcode,
                                btc[0].batch_date,
                                x.acc_id,
                                btc[0].dep_id,
                                None,
                                None,
                                None,
                                None,
                                None,
                                x.nom_wgs,
                                "K",
                                "JURNAL BIAYA ATAS %s" % (btc[0].bcode),
                                None,
                                None,
                            )
                        )
                db.session.add_all(trans_btc_wgs)

                if user_product == "inv+gl":
                    if btc[0].mat_id:
                        for u in useMatBiaya:
                            trans_biaya_mat.append(
                                TransDdb(
                                    btc[0].bcode,
                                    btc[0].batch_date,
                                    u.acc_id,
                                    btc[0].dep_id,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    u.value,
                                    "K",
                                    "JURNAL BIAYA ATAS PEMAKAIAN MATERIAL %s"
                                    % (useMatHdb.code),
                                    None,
                                    None,
                                )
                            )
                    db.session.add_all(trans_biaya_mat)

            db.session.commit()

        except Exception as e:
            print("update")
            print(e)
