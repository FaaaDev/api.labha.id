from ...model.ccost_mdb import CcostMdb
from ...schema.ccost_mdb import *
from ...utils.response import response
from sqlalchemy import func, or_


class CcostFilter:
    def __new__(self, page, length, filter):
        all = (
            CcostMdb.query
            .filter(
                or_(
                    func.lower(CcostMdb.ccost_code).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                    func.lower(CcostMdb.ccost_name).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                    func.lower(CcostMdb.ccost_ket).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                )
            )
            .all()
        )

        paging = (
            CcostMdb.query
            .filter(
                or_(
                    func.lower(CcostMdb.ccost_code).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                    func.lower(CcostMdb.ccost_name).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                    func.lower(CcostMdb.ccost_ket).like(
                        "%{}%".format(filter.lower() if filter != "0" else "")
                    ),
                )
            )
            .order_by(CcostMdb.id.desc())
            .offset(length * (page - 1))
            .limit(length)
            .all()
        )

        return response(200, "Berhasil", True, {"data": ccosts_schema.dump(paging), "length": len(all)})
