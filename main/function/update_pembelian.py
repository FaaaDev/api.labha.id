from sqlalchemy import and_
from main.model.apcard_mdb import ApCard
from main.model.djasa_ddb import DjasaDdb
from main.model.dprod_ddb import DprodDdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.jasa_mdb import JasaMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.pajak_mdb import PajakMdb
from main.model.prod_mdb import ProdMdb
from main.model.setup_mdb import SetupMdb
from main.model.supplier_mdb import SupplierMdb
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.model.user import User
from main.shared.shared import db, ma


class UpdatePembelian:
    def __init__(self, fk_id, user_id, delete):

        # update kartu ap
        x = (
            db.session.query(FkpbHdb, OrdpbHdb)
            .outerjoin(OrdpbHdb, OrdpbHdb.id == FkpbHdb.ord_id)
            .filter(FkpbHdb.id == fk_id)
            .first()
        )

        if delete:
            if x[1]:
                old_ap = ApCard.query.filter(
                    and_(
                        ApCard.ord_id == x[1].id,
                        ApCard.trx_type == "LP",
                        ApCard.pay_type == "P1",
                    )
                ).first()
                if old_ap:
                    db.session.delete(old_ap)
                    db.session.commit()

            old_trans = TransDdb.query.filter(TransDdb.trx_code == x[0].fk_code).all()

            if old_trans:
                for x in old_trans:
                    db.session.delete(x)
                    db.session.commit()
        else:
            dprod = DprodDdb.query.filter(DprodDdb.ord_id == x[1].id).all()

            djasa = DjasaDdb.query.filter(DjasaDdb.ord_id == x[1].id).all()

            total_product = 0
            for y in dprod:
                if y.nett_price and y.nett_price > 0:
                    total_product += y.nett_price
                else:
                    total_product += y.total

            total_jasa = 0
            for y in djasa:
                total_jasa += y.total

            sup = (
                db.session.query(SupplierMdb, PajakMdb)
                .outerjoin(PajakMdb, PajakMdb.id == SupplierMdb.sup_ppn)
                .filter(SupplierMdb.id == x[1].sup_id)
                .first()
            )

            trx_amnh = 0
            if x[1].split_inv:
                trx_amnh = (total_product * ((100 + 11) / 100)) + (
                    total_jasa * ((100 + 2) / 100)
                )
            else:
                trx_amnh = (total_product + total_jasa) * ((100 + 11) / 100)

            old_ap = ApCard.query.filter(
                and_(
                    ApCard.ord_id == x[1].id,
                    ApCard.trx_type == "LP",
                    ApCard.pay_type == "P1",
                )
            ).first()
            if old_ap:
                db.session.delete(old_ap)
                db.session.commit()

            ap_card = ApCard(
                x[1].sup_id,
                x[1].id,
                x[1].ord_date,
                x[1].due_date,
                x[1].po_id,
                None,
                None,
                None,
                "d",
                "LP",
                "P1",
                trx_amnh,
                None,
                None,
                None,
                None,
                None,
            )

            db.session.add(ap_card)
            db.session.commit()

            old_trans = TransDdb.query.filter(TransDdb.trx_code == x[0].fk_code).all()

            if old_trans:
                for x in old_trans:
                    db.session.delete(x)
                    db.session.commit()
            # insert jurnal ap
            trans_ap = TransDdb(
                x[0].fk_code,
                x[0].fk_date,
                sup[0].sup_hutang,
                x[1].dep_id,
                None,
                None,
                None,
                None,
                None,
                trx_amnh,
                "K",
                "JURNAL HUTANG",
                None,
                None,
            )

            db.session.add(trans_ap)
            db.session.commit()

            # insert jurnal ppn
            setup = (
                db.session.query(User, SetupMdb)
                .outerjoin(SetupMdb, SetupMdb.cp_id == User.company)
                .filter(User.id == user_id)
                .first()
            )
            trans_ppn = TransDdb(
                x[0].fk_code,
                x[0].fk_date,
                setup[1].pur_tax,
                x[1].dep_id,
                None,
                None,
                None,
                None,
                None,
                total_product * 11 / 100,
                "D",
                "JURNAL PPN KELUARAN %s" % (x[0].fk_code),
                None,
                None,
            )

            db.session.add(trans_ppn)
            db.session.commit()
