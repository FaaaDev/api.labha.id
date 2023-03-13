import logging
from ...function.update_table import UpdateTable
from ...model.accou_mdb import AccouMdb
from ...model.saldo_akhir import SldAkhir
from ...model.setup_mdb import SetupMdb
from ...model.transddb import TransDdb
from ...model.comp_mdb import CompMdb
from ...model.set_sld_ak_mdb import SetupSAMdb
from ...schema.saldo_akhir import sld_akhirs_schema
from ...schema.accou_mdb import accou_schema
from ...shared.shared import db
from ...utils.response import response
from datetime import datetime
from sqlalchemy.exc import *
import time


class SaldoAkhir:
    def __new__(self, request, user_id, company):
        if request.method == "POST":
            try:
                sld_akhir = request.json["sld_akhir"]

                setup = SetupSAMdb.query.filter(SetupSAMdb.cp_id == company).all()
                account = AccouMdb.query.all()

                final = []
                if setup:
                    for z in setup:
                        setup_dict = dict(
                            (col, getattr(z, col)) for col in z.__table__.columns.keys()
                        )

                        for key, value in setup_dict.items():
                            if key != "id" and key != "cp_id" and key != "user_id":
                                for x in account:
                                    if value:
                                        if value == x.id:
                                            setup_dict[key] = accou_schema.dump(x)
                        final.append(setup_dict)

                sld = []
                trans = []
                for x in sld_akhir:
                    id = x["id"]
                    acc_code = x["acc_code"]
                    date = x["date"]
                    saldo = x["saldo"]
                    now = datetime.now().strftime("%d%m%y")
                    trx = "SLDAKHIR-" + now + "-" + str(round(time.time() * 10000))[-6:]

                    if id == 0:
                        sld.append(SldAkhir(trx, acc_code, date, saldo, False, user_id))
                        for y in final:
                            if y["sto"]["acc_code"] == acc_code:
                                trans.extend(
                                    [
                                        TransDdb(
                                            trx,
                                            date,
                                            y["sto"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Saldo Awal %s-%s"
                                            % (
                                                y["sto"]["acc_code"],
                                                y["sto"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["pur"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Pembelian %s-%s"
                                            % (
                                                y["pur"]["acc_code"],
                                                y["pur"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["pur_shipping"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Beban %s-%s"
                                            % (
                                                y["pur_shipping"]["acc_code"],
                                                y["pur_shipping"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["pur_retur"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Purchase Retur %s-%s"
                                            % (
                                                y["pur_retur"]["acc_code"],
                                                y["pur_retur"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["pur_discount"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Discount %s-%s"
                                            % (
                                                y["pur_discount"]["acc_code"],
                                                y["pur_discount"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["hpp"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Harga Pokok %s-%s"
                                            % (
                                                y["hpp"]["acc_code"],
                                                y["hpp"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            trx,
                                            date,
                                            y["sto"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            saldo,
                                            "D",
                                            "Saldo Akhir Persediaan %s-%s"
                                            % (
                                                y["sto"]["acc_code"],
                                                y["sto"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                    ]
                                )
                    else:
                        old_sa = SldAkhir.query.filter(SldAkhir.id == id).first()

                        old_sa.saldo = saldo

                        old_trans = TransDdb.query.filter(
                            TransDdb.trx_code == old_sa.trx
                        ).all()

                        for y in old_trans:
                            db.session.delete(y)

                        for y in final:
                            if y["sto"]["acc_code"] == acc_code:
                                trans.extend(
                                    [
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["sto"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Saldo Awal %s-%s"
                                            % (
                                                y["sto"]["acc_code"],
                                                y["sto"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["pur"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Pembelian %s-%s"
                                            % (
                                                y["pur"]["acc_code"],
                                                y["pur"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["pur_shipping"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "K",
                                            "Beban %s-%s"
                                            % (
                                                y["pur_shipping"]["acc_code"],
                                                y["pur_shipping"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["pur_retur"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Purchase Retur %s-%s"
                                            % (
                                                y["pur_retur"]["acc_code"],
                                                y["pur_retur"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["pur_discount"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Discount %s-%s"
                                            % (
                                                y["pur_discount"]["acc_code"],
                                                y["pur_discount"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["hpp"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            0,
                                            "D",
                                            "Harga Pokok %s-%s"
                                            % (
                                                y["hpp"]["acc_code"],
                                                y["hpp"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                        TransDdb(
                                            old_sa.trx,
                                            old_sa.date,
                                            y["sto"]["id"],
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            None,
                                            saldo,
                                            "D",
                                            "Saldo Akhir Persediaan %s-%s"
                                            % (
                                                y["sto"]["acc_code"],
                                                y["sto"]["acc_name"],
                                            ),
                                            False,
                                            None,
                                            user_id,
                                        ),
                                    ]
                                )

                if len(sld) > 0:
                    db.session.add_all(sld)
                    db.session.commit()

                if len(trans) > 0:
                    db.session.add_all(trans)
                    db.session.commit()

                return response(200, "Berhasil", True, sld_akhirs_schema.dump(sld))
            except Exception as e:
                db.session.close()
                logging.critical(e, exc_info=True)
                return response(400, str(e), False, None)
        else:
            try:
                sld = SldAkhir.query.order_by(SldAkhir.id.asc()).all()

                return response(200, "Berhasil", True, sld_akhirs_schema.dump(sld))
            except ProgrammingError as e:
                return UpdateTable([SldAkhir, TransDdb, AccouMdb, SetupSAMdb], request)


class SaldoAkhirId:
    def __new__(self, request, id):
        sld = SldAkhir.query.filter(SldAkhir.id == id).first()
        sld.saldo = request.json["saldo"]
        db.session.commit()

        return response(200, "Berhasil", True, None)
