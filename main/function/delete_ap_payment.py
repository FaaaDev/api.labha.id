from sqlalchemy import and_
from ..model.acq_ddb import AcqDdb
from ..model.apcard_mdb import ApCard
from ..model.dprod_ddb import DprodDdb
from ..model.exp_hdb import ExpHdb
from ..model.fkpb_hdb import FkpbHdb
from ..model.giro_hdb import GiroHdb
from ..model.group_prod_mdb import GroupProMdb
from ..model.lokasi_mdb import LocationMdb
from ..model.ordpb_hdb import OrdpbHdb
from ..model.prod_mdb import ProdMdb
from ..model.stcard_mdb import StCard
from ..model.transddb import TransDdb
from ..model.unit_mdb import UnitMdb
from ..shared.shared import db


class DeleteApPayment():
    def __init__(self, exp_id):
        acq = AcqDdb.query.filter(AcqDdb.exp_id == exp_id).all()

        if acq:
            for x in acq:
                db.session.delete(x)
                db.session.commit()

        giro = GiroHdb.query.filter(GiroHdb.pay_code == exp_id).first()

        if giro:
            db.session.delete(giro)
            db.session.commit()
