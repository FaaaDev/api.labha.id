from sqlalchemy import and_
from main.model.acq_ddb import AcqDdb
from main.model.apcard_mdb import ApCard
from main.model.dprod_ddb import DprodDdb
from main.model.exp_hdb import ExpHdb
from main.model.fkpb_hdb import FkpbHdb
from main.model.giro_hdb import GiroHdb
from main.model.group_prod_mdb import GroupProMdb
from main.model.lokasi_mdb import LocationMdb
from main.model.ordpb_hdb import OrdpbHdb
from main.model.prod_mdb import ProdMdb
from main.model.stcard_mdb import StCard
from main.model.transddb import TransDdb
from main.model.unit_mdb import UnitMdb
from main.shared.shared import db


class DeleteApPayment():
    def __init__(self, exp_id):
        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp_id).all()

        if acq:
            for x in acq:
                db.session.delete(x)
                db.session.commit()

        giro = GiroHdb.query.filter(GiroHdb.pay_code == exp_id).first()

        db.session.delete(giro)
        db.session.commit()
