from ..shared.shared import ma


class GroupProMdb(ma.Schema):
    class Meta:
        ordered = True
        fields = (
            "id",
            "code",
            "name",
            "div_code",
            "stok",
            "wip",
            "acc_sto",
            "acc_send",
            "acc_terima",
            "hrg_pokok",
            "acc_penj",
            "acc_wip",
            "potongan",
            "pengembalian",
            "selisih",
            "biaya",
        )


groupPro_schema = GroupProMdb()
groupPros_schema = GroupProMdb(many=True)
