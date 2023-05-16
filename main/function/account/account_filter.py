from ...model.accou_mdb import AccouMdb
from ...schema.accou_mdb import accou_schema
from ...schema.kateg_mdb import kateg_schema
from ...model.kateg_mdb import KategMdb
from ...schema.klasi_mdb import klasi_schema
from ...model.klasi_mdb import KlasiMdb
from ...shared.shared import db
from ...utils.response import response
from sqlalchemy import func, cast, case, literal_column, or_


class AccountFilter:
    def __new__(self, page, length, filter):
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

            all = (
                query
                .filter(
                    or_(
                        func.lower(AccouMdb.acc_code).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                        func.lower(AccouMdb.acc_name).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                        func.lower(KategMdb.name).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                        func.lower(KlasiMdb.klasiname).like(
                            "%{}%".format(filter.lower() if filter != "0" else "")
                        ),
                    )
                )
                .all()
            )
            
            result = (
                query
                .filter(
                    or_(
                        func.lower(AccouMdb.acc_code).like(
                            "%{}%".format(
                                filter.lower() if filter != "0" else "")
                        ),
                        func.lower(AccouMdb.acc_name).like(
                            "%{}%".format(
                                filter.lower() if filter != "0" else "")
                        ),
                        func.lower(KategMdb.name).like(
                            "%{}%".format(
                                filter.lower() if filter != "0" else "")
                        ),
                        func.lower(KlasiMdb.klasiname).like(
                            "%{}%".format(
                                filter.lower() if filter != "0" else "")
                        ),
                    )
                )
                .offset(length * (page - 1))
                .limit(length)
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

            return response(200, "Berhasil", True, {"data": data, "length": len(all)})

        except ProgrammingError as e:
            return UpdateTable([AccouMdb, KategMdb, KlasiMdb], request)
