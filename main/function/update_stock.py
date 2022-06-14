from sqlalchemy import and_
from main.model.dprod_ddb import DprodDdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class UpdateStock():
    def __init__(self, order_id):
        order = OrdpbHdb.query.filter(OrdpbHdb.id == order_id).first()
        print(order)
        product = (
            db.session.query(DprodDdb, ProdMdb, GroupProMdb, LocationMdb)
            .outerjoin(ProdMdb, ProdMdb.id == DprodDdb.prod_id)
            .outerjoin(GroupProMdb, GroupProMdb.id == ProdMdb.group)
            .outerjoin(LocationMdb, LocationMdb.id == DprodDdb.location)
            .filter(DprodDdb.ord_id == order_id)
            .all()
        )

        unit = UnitMdb.query.all()

        trans = []
        krtst = []
        for x in product:
            trans.append(TransDdb(order.ord_code, order.ord_date, x[2].acc_sto, order.dep_id, None,
                                  None, None, None, None, x[0].nett_price if x[0].nett_price > 0 else x[0].total, "D", "JURNAL STOCK %s %s" % (x[1].code, x[3].code), None, None))


            old_krtst = StCard.query.filter(and_(StCard.trx_code == order.ord_code, StCard.prod_id == x[0].prod_id, StCard.loc_id == x[0].location)).first()
            if old_krtst:
                db.session.delete(old_krtst)
                db.session.commit()

            qty = 0
            if x[0].unit_id != x[1].unit:
                for y in unit:
                    if x[0].unit_id == y.id:
                        qty = x[0].order*y.qty
            else:
                qty = x[0].order

            krtst.append(StCard(order.ord_code, order.ord_date, "d", "BL", None, qty, None, None,
                         x[0].nett_price if x[0].nett_price > 0 else x[0].total, None, None, x[0].prod_id, x[0].location, None, 0, None))

        db.session.add_all(trans)
        db.session.add_all(krtst)
        db.session.commit()
