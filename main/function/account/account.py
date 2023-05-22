from ...shared.shared import db
from ...utils.response import response
from sqlalchemy.exc import *
from ...function.update_table import UpdateTable
from ...model.accou_mdb import AccouMdb
from ...schema.accou_mdb import accou_schema
from ...schema.kateg_mdb import kateg_schema
from ...model.kateg_mdb import KategMdb
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb
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
                        user.company,
                    )
                    db.session.add(account)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()
                    db.session.close()
                    print()
                    return response(
                        400, "Kode akun " + acc_code + " sudah digunakan", False, None
                    )
                finally:
                    return response(200, "Berhasil", True,
                                    accou_schema.dump(account))
            else:
                self.response = response(
                    406, "Data isian belum lengkap", False, None)
        else:
            try:
                query = (
                    db.session.query(
                        AccouMdb,
                        KategMdb,
                        KlasiMdb,
                        cast(
                            func.right(
                                func.split_part(
                                    AccouMdb.acc_code, '.', 2
                                ), 4
                            ), db.Integer
                        ).label('right_1'),
                        cast(
                            case(
                                [
                                    (
                                        func.split_part(
                                            AccouMdb.acc_code, '.', 3
                                        ) == '', '0'
                                    )
                                ], else_=func.split_part(
                                    AccouMdb.acc_code, '.', 3
                                )
                            ), db.Integer
                        ).label('anon_1'),
                        cast(
                            case(
                                [
                                    (
                                        func.split_part(
                                            AccouMdb.acc_code, '.', 3
                                        ) == '', '0'
                                    )
                                ], else_=func.left(
                                    func.split_part(
                                        AccouMdb.acc_code, '.', 3
                                    ), 4
                                )
                            ), db.Integer
                        ).label('anon_1_1'),
                        cast(
                            case(
                                [
                                    (
                                        func.split_part(
                                            AccouMdb.acc_code, '.', 3
                                        ) == '', '0'
                                    )], else_=case(
                                    [(
                                        AccouMdb.dou_type == 'U', case(
                                            [
                                                (func.char_length(
                                                    func.split_part(
                                                        AccouMdb.acc_code, '.', 3
                                                    )
                                                ) > 4, 1
                                                )
                                            ], else_=0
                                        )
                                    )
                                    ], else_=case(
                                        [
                                            (
                                                func.char_length(
                                                    func.split_part(
                                                        AccouMdb.acc_code, '.', 3
                                                    )
                                                ) > 4, 1
                                            )
                                        ], else_=2
                                    )
                                )
                            ), db.Integer
                        ).label('anon_1_2'),
                        cast(
                            case(
                                [
                                    (func.split_part
                                     (AccouMdb.acc_code, '.', 3
                                      ) == '', '0'
                                     )
                                ], else_=case([
                                    (AccouMdb.dou_type == 'U', case(
                                        [
                                            (func.char_length(
                                                func.split_part(
                                                    AccouMdb.acc_code, '.', 3
                                                )
                                            ) > 4, cast(
                                                func.substr(
                                                    func.split_part(
                                                        AccouMdb.acc_code, '.', 3
                                                    ),
                                                    5
                                                ), db.Integer
                                            )
                                            )
                                        ], else_=0)
                                     )
                                ], else_=case(
                                    [
                                        (func.char_length(
                                            func.split_part(
                                                AccouMdb.acc_code, '.', 3
                                            )
                                        ) > 4, cast(
                                            func.substr(
                                                func.split_part(
                                                    AccouMdb.acc_code, '.', 3
                                                ), 5
                                            ), db.Integer
                                        )
                                        )
                                    ], else_=0
                                )
                                )
                            ), db.Integer
                        ).label('anon_1_3'),
                        cast(
                            case
                            (
                                [
                                    (func.split_part
                                     (AccouMdb.acc_code, '.', 4
                                      ) == '', '0'
                                     )
                                ], else_=func.split_part
                                (
                                    AccouMdb.acc_code, '.', 4
                                )
                            ), db.Integer
                        ).label('anon_2'),
                        cast(
                            func.left(
                                cast(
                                    cast(
                                        case(
                                            (
                                                func.split_part(
                                                    AccouMdb.acc_code, ".", 3)
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
                        ).label('left_1')
                    )
                    .outerjoin(KategMdb, KategMdb.id == AccouMdb.kat_code)
                    .outerjoin(KlasiMdb, KategMdb.kode_klasi == KlasiMdb.id)
                    .order_by('right_1', 'anon_1_1', 'anon_1_2', 'anon_1_3', 'anon_2', 'left_1')
                )

                result = query.all()

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
                print(user.company)
                return UpdateTable([AccouMdb,
                                    KategMdb,
                                    KlasiMdb, ], request)
