from main.function.update_table import UpdateTable
from main.model.akhir_mdb import AkhirMdb
from main.model.comp_mdb import CompMdb
from main.model.accou_ddb import AccouDdb
from main.model.accou_mdb import AccouMdb
from main.model.neraca_ddb import NeracaDdb
from main.model.neraca_hdb import NeracaHdb
from main.model.user import User
from main.schema.accou_ddb import accddb_schema, accddbs_schema
from main.shared.shared import db
from main.utils.response import response
from datetime import date, datetime, time
from sqlalchemy.exc import *


class SaldoAwalGlStatus:
    def __new__(self, user, request):
        try:
            sa = (
                db.session.query(AccouDdb, AccouMdb)
                .outerjoin(AccouMdb, AccouMdb.acc_code == AccouDdb.acc_code)
                .filter(AccouDdb.sa == True)
                .order_by(AccouDdb.acc_code.asc())
                .all()
            )

            setup_neraca = (
                db.session.query(NeracaHdb, NeracaDdb)
                .outerjoin(NeracaDdb, NeracaDdb.tittle_id == NeracaHdb.id)
                .filter(NeracaHdb.cp_id == user.company)
                .all()
            )

            for x in setup_neraca:
                x[1].accounts = (
                    x[1].accounts.replace("{", "").replace("}", "").split(",")
                    if x[1].accounts
                    else None
                )

            aktiva = 0
            pasiva = 0
            for x in setup_neraca:
                for y in sa:
                    if x[0].type == 1 and str(y[1].kat_code) in x[1].accounts:
                        aktiva += (
                            y[0].acc_akhir
                            if y[1].sld_type == "D"
                            else 0 - y[0].acc_akhir
                        )
                    elif x[0].type == 2 and str(y[1].kat_code) in x[1].accounts:
                        pasiva += (
                            y[0].acc_akhir
                            if y[1].sld_type == "K"
                            else 0 - y[0].acc_akhir
                        )

            return response(200, "Berhasil", True, aktiva == pasiva)
        # except Exception as e:
        #     return response(400, "Gagal", True, str(e))

        except ProgrammingError as e:
            return UpdateTable([AccouDdb, AccouMdb, NeracaHdb, NeracaDdb], request)
