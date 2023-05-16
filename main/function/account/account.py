from main.function.update_table import UpdateTable
from main.shared.shared import db
from main.utils.response import response
from sqlalchemy.exc import *
from main.model.accou_mdb import AccouMdb
from main.schema.accou_mdb import accou_schema
from main.schema.kateg_mdb import kateg_schema
from main.model.kateg_mdb import KategMdb
from main.schema.klasi_mdb import klasi_schema
from main.model.klasi_mdb import KlasiMdb
from sqlalchemy import func, cast, case, literal_column


class Account:
    def __new__(self, user, request):
        if request.method == "POST":
            if "kode_acc" in request.json:
                acc_code = request.json["kode_acc"]
                acc_name = request.json["acc_name"]
                umm_code = request.json["kode_umum"]
                kat_code = request.json["kode_kategori"]
                dou_type = request.json["du"]
                sld_type = request.json["kode_saldo"]
                connect = request.json["terhubung"]
                sld_awal = request.json["saldo_awal"]
                level = request.json["level"]
                try:
                    account = AccouMdb(
                        acc_code,
                        acc_name,
                        umm_code,
                        kat_code,
                        dou_type,
                        sld_type,
                        connect,
                        sld_awal,
                        level,
                        user.id,
                    )
                    db.session.add(account)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()
                    db.session.close()
                    print(e)
                    return response(
                        400, "Kode akun " + acc_code + " sudah digunakan", False, None
                    )
                finally:
                    return response(200, "Berhasil", True, accou_schema.dump(account))
            else:
                return response(406, "Data isian belum lengkap", False, None)
        else:
            try:
                result = (
                    db.session.query(
                        AccouMdb,
                        KategMdb,
                        KlasiMdb,
                        cast(
                            func.right(func.split_part(AccouMdb.acc_code, ".", 2), 4),
                            db.Integer,
                        ),
                        cast(
                            case(
                                (
                                    func.split_part(AccouMdb.acc_code, ".", 3) == "",
                                    literal_column("'0'"),
                                ),
                                else_=func.split_part(AccouMdb.acc_code, ".", 3),
                            ),
                            db.Integer,
                        ),
                        cast(
                            case(
                                (
                                    func.split_part(AccouMdb.acc_code, ".", 4) == "",
                                    literal_column("'0'"),
                                ),
                                else_=func.split_part(AccouMdb.acc_code, ".", 4),
                            ),
                            db.Integer,
                        ),
                        cast(
                            func.left(
                                cast(
                                    cast(
                                        case(
                                            (
                                                func.split_part(
                                                    AccouMdb.acc_code, ".", 3
                                                )
                                                == "",
                                                literal_column("'0'"),
                                            ),
                                            else_=func.split_part(
                                                AccouMdb.acc_code, ".", 3
                                            ),
                                        ),
                                        db.Integer,
                                    ),
                                    db.String,
                                ),
                                1,
                            ),
                            db.Integer,
                        ),
                    )
                    .outerjoin(KategMdb, KategMdb.id == AccouMdb.kat_code)
                    .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                    # .order_by(KategMdb.kode_klasi.asc())
                    # .order_by(AccouMdb.kat_code.asc())
                    .order_by(
                        cast(
                            func.right(func.split_part(AccouMdb.acc_code, ".", 2), 4),
                            db.Integer,
                        ),
                        cast(
                            case(
                                (
                                    func.split_part(AccouMdb.acc_code, ".", 3) == "",
                                    literal_column("'0'"),
                                ),
                                else_=func.split_part(AccouMdb.acc_code, ".", 3),
                            ),
                            db.Integer,
                        ),
                        cast(
                            func.left(
                                cast(
                                    cast(
                                        case(
                                            (
                                                func.split_part(
                                                    AccouMdb.acc_code, ".", 3
                                                )
                                                == "",
                                                literal_column("'0'"),
                                            ),
                                            else_=func.split_part(
                                                AccouMdb.acc_code, ".", 3
                                            ),
                                        ),
                                        db.Integer,
                                    ),
                                    db.String,
                                ),
                                1,
                            ),
                            db.Integer,
                        ),
                        cast(
                            case(
                                (
                                    func.split_part(AccouMdb.acc_code, ".", 4) == "",
                                    literal_column("'0'"),
                                ),
                                else_=func.split_part(AccouMdb.acc_code, ".", 4),
                            ),
                            db.Integer,
                        ),
                    )
                    .all()
                )

                data = [
                    {
                        "account": accou_schema.dump(x[0]),
                        "kategory": kateg_schema.dump(x[1]),
                        "klasifikasi": klasi_schema.dump(x[2]),
                    }
                    for x in result
                ]

                return response(200, "Berhasil", True, data)

            except ProgrammingError as e:
                return UpdateTable([AccouMdb, KategMdb, KlasiMdb], request)
