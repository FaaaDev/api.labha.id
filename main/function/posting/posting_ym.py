from datetime import date
from main.model.comp_mdb import CompMdb
from main.model.akhir_mdb import AkhirMdb
from main.model.user import User
from main.shared.shared import db
from main.utils.response import response


class GetYearPosting:
    def __new__(self, user, request):
        try:
            cp = CompMdb.query.filter(CompMdb.id == user.company).first()

            closing = (
                AkhirMdb.query.order_by(AkhirMdb.post_year.desc())
                .order_by(AkhirMdb.post_month.desc())
                .first()
            )

            today = date.today()

            if closing:
                return response(
                    200,
                    "Berhasil",
                    True,
                    {
                        "month": closing.post_month + 1
                        if closing.post_month and closing.post_month < 12
                        else 1,
                        "year": closing.post_year + 1
                        if closing.post_month == 12
                        else closing.post_year,
                    },
                )

            return response(
                200,
                "Berhasil",
                True,
                {
                    "month": cp.cutoff + 1,
                    "year": cp.year_co,
                },
            )
        except Exception as e:
            print(e)
            return response(
                400,
                "Gagal " + str(e),
                False,
                None,
            )
