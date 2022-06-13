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
            db.session.delete(old_krtst)
            db.session.commit()

            qty = 0
            unit_value = 0
            if x[0].unit_id != x[1].unit:
                for z in unit:
                    if x[1].unit == y.id:
                        prod_unit = z

                for y in unit:
                    if x[0].unit_id == y.id:
                        trx_unit = y

                # if trx_unit.type == "k":
            else:
                qty = x[0].order


            # DELETE FROM "krtstmdb" where "TRX_CODE"=NEW."PUR_CODE" AND "INV_CODE"=NEW."INV_CODE" AND "LOC_CODE"=NEW."LOC_CODE";
            # INSERT INTO public.krtstmdb
            # ("TRX_CODE", "TRX_DATE", "TRX_JENS", "TRX_DBCR",  "INV_CODE", "LOC_CODE", "TRX_KUAN","TRX_HPOK")
            # VALUES
            # (NEW."PUR_CODE",TRX_DATE,'BL','D',NEW."INV_CODE",NEW."LOC_CODE",(NEW."PUR_KUAN"*INV_KONV),(NEW."PUR_HRGA"- NEW."PUR_DISC_AVG")/PPN_X);
            # end if ;
            # RETURN NEW;
            # end
            # $function$

            krtst.append(StCard(order.ord_code, order.ord_date, "d", "BL", None, qty, None, None,
                         x[0].nett_price if x[0].nett_price > 0 else x[0].total, None, None, x[0].prod_id, x[0].location, None, 0, None))

        db.session.add_all(trans)
        db.session.commit()
