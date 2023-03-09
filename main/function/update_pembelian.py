from operator import or_
from sqlalchemy import and_
from main.model.apcard_mdb import ApCard
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.fkpb_det_ddb import FkpbDetDdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.jasa_mdb import JasaMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.setup_mdb import SetupMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.currency_mdb import CurrencyMdb
from main.model.user import User
from main.shared.shared import db, ma


class UpdatePembelian:
    def __init__(self, fk_id, user_id, delete):

        # update kartu ap
        x = (
            db.session.query(FkpbHdb, OrdpbHdb, FkpbDetDdb)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbDetDdb.ord_id)
            .outerjoin(FkpbHdb, FkpbHdb.id == FkpbDetDdb.fk_id)
            .filter(OrdpbHdb.id == fk_id)
            .first()
        )

        if delete:
            # if x[2]:
            old_ap = ApCard.query.filter(
                    and_(
                        ApCard.ord_id == x[1].id,
                        ApCard.trx_type == "LP",
                        ApCard.pay_type == "P1",
                    )
                ).first()
            if old_ap:
                    db.session.delete(old_ap)

            old_fk = FkpbHdb.query.filter(FkpbHdb.ord_id == x[1].id).first()

            if old_fk:
                    db.session.delete(old_fk)

            old_trans = TransDdb.query.filter(TransDdb.trx_code == x[0].fk_code).all()

            if old_trans:
                for x in old_trans:
                    db.session.delete(x)

        else:
            dprod = DprodDdb.query.filter(DprodDdb.ord_id == x[2].ord_id).all()

            djasa = DjasaDdb.query.filter(DjasaDdb.ord_id == x[2].ord_id).all()

            sup = SupplierMdb.query.filter(SupplierMdb.id == x[1].sup_id).first()

            gprod = (
                db.session.query(ProdMdb, GroupProMdb)
                .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
                .all()
            )

            # comp = CompMdb.query.filter(CompMdb.id == user_company).first()

            # setup = SetupMdb.query.filter(SetupMdb.cp_id == user_company).first()

            ppn = (
                db.session.query(OrdpbHdb, SupplierMdb, PajakMdb, CurrencyMdb)
                .outerjoin(SupplierMdb, SupplierMdb.id == OrdpbHdb.sup_id)
                .outerjoin(PajakMdb, PajakMdb.id == SupplierMdb.sup_ppn)
                .outerjoin(CurrencyMdb, CurrencyMdb.id == SupplierMdb.sup_curren)
                .filter(SupplierMdb.id == x[0].sup_id)
                .first()
            )

            total_product = 0
            total_fc = 0
            acc_ns = None
            acc_ns_prd = None
            for y in dprod:
                # if x[1].ns:
                #     for z in gprod:
                #         if y.prod_id == z[0].id:
                #             acc_ns = z[1].biaya
                #             acc_ns_prd = z[0].biaya

                if y.nett_price and y.nett_price > 0:
                    total_product += y.nett_price
                else:
                    total_product += y.total

                total_fc += y.total_fc

            total_jasa = 0
            jtotal_fc = 0
            for y in djasa:
                total_jasa += y.total
                jtotal_fc += y.total_fc

            trx_amnh = 0
            trx_amnv = 0
            if x[1].split_inv:
                if sup.sup_ppn != None:
                    trx_amnh = (total_product * ((100 + ppn[2].nilai) / 100)) + (
                        total_jasa * ((100 + 2) / 100)
                    )

                    trx_amnv = (total_fc * ((100 + ppn[2].nilai) / 100)) + (
                        jtotal_fc * ((100 + 2) / 100)
                    )
                else:
                    trx_amnh = (total_product * ((100 + 0) / 100)) + (
                        total_jasa * ((100 + 2) / 100)
                    )

                    trx_amnv = (total_fc * ((100 + 0) / 100)) + (
                        jtotal_fc * ((100 + 2) / 100)
                    )
            else:
                if sup.sup_ppn != None:
                    trx_amnh = (total_product + total_jasa) * (
                        (100 + ppn[2].nilai) / 100
                    )

                    trx_amnv = (total_fc + jtotal_fc) * ((100 + ppn[2].nilai) / 100)
                else:
                    trx_amnh = (total_product + total_jasa) * ((100 + 0) / 100)

                    trx_amnv = (total_fc + jtotal_fc) * ((100 + 0) / 100)

            # Insert Kartu AP
            old_ap = ApCard.query.filter(
                and_(
                    ApCard.ord_id == x[2].ord_id,
                    ApCard.trx_type == "LP",
                    ApCard.pay_type == "P1",
                )
            ).first()

            if old_ap:
                db.session.delete(old_ap)

            ap_card = ApCard(
                x[2].ord_code,
                x[0].sup_id,
                x[2].ord_id,
                x[1].ord_date,
                x[1].due_date,
                x[1].po_id,
                None,
                None,
                sup.sup_curren,
                "k",
                "LP",
                "P1",
                trx_amnh,
                trx_amnh / ppn[3].rate if sup.sup_curren != None else 0,
                None,
                None,
                None,
                None,
                None,
                False,
            )

            db.session.add(ap_card)

            # insert jurnal ap
            old_hut = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == x[0].fk_code,
                    TransDdb.trx_desc == "JURNAL HUTANG %s" % (x[0].fk_code),
                )
            ).first()

            if old_hut:
                db.session.delete(old_hut)

            trans_ap = TransDdb(
                x[0].fk_code,
                x[0].fk_date,
                sup.sup_hutang,
                x[1].dep_id,
                None,
                None,
                sup.sup_curren,
                ppn[3].rate if sup.sup_curren != None else 0,
                trx_amnv if sup.sup_curren != None else 0,
                trx_amnh,
                "K",
                "JURNAL HUTANG %s" % (x[0].fk_code),
                None,
                None,
            )

            db.session.add(trans_ap)

            # insert jurnal ppn
            old_ppn = TransDdb.query.filter(
                and_(
                    TransDdb.trx_code == x[0].fk_code,
                    TransDdb.trx_desc == "JURNAL PPN KELUARAN %s" % (x[0].fk_code),
                )
            ).first()

            if old_ppn:
                db.session.delete(old_ppn)

            if sup.sup_ppn != None:
                trans_ppn = TransDdb(
                    x[0].fk_code,
                    x[0].fk_date,
                    ppn[2].acc_pur_tax,
                    x[1].dep_id,
                    None,
                    None,
                    sup.sup_curren,
                    ppn[3].rate if sup.sup_curren != None else 0,
                    total_fc * ppn[2].nilai / 100,
                    total_product * ppn[2].nilai / 100
                    if total_jasa == 0
                    else (total_product + total_jasa) * ppn[2].nilai / 100,
                    "D",
                    "JURNAL PPN KELUARAN %s" % (x[0].fk_code),
                    None,
                    None,
                )

                db.session.add(trans_ppn)

            # Insert Jurnal Biaya
            # if user_product == "inv+gl":
            #     if x[1].ns:
            #         trans_biaya = TransDdb(
            #             x[0].fk_code,
            #             x[0].fk_date,
            #             acc_ns if comp.gl_detail == False else acc_ns_prd,
            #             x[1].dep_id,
            #             None,
            #             None,
            #             sup.sup_curren,
            #             ppn[3].rate,
            #             total_fc,
            #             total_product,
            #             "D",
            #             "JURNAL BIAYA %s" % (x[0].fk_code),
            #             None,
            #             None,
            #         )

            #         db.session.add(trans_biaya)

        db.session.commit()
