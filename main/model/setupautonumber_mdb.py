from ..shared.shared import db


class SetupAutoNumberMdb(db.Model):
    __table_args__ = {"schema": "master"}
    __tablename__ = "SETUPAUTONUMBERMDB"

    id = db.Column(db.Integer, primary_key=True)
    cp_id = db.Column(db.Integer)
    rp_no_ref = db.Column(db.String(255))
    rp_ref_month = db.Column(db.String(255))
    rp_ref_year = db.Column(db.Integer)
    rp_depart = db.Column(db.String(255))
    rp_reset_month = db.Column(db.String)
    po_no_ref = db.Column(db.String(255))
    po_ref_month = db.Column(db.String(255))
    po_ref_year = db.Column(db.Integer)
    po_depart = db.Column(db.String(255))
    po_reset_month = db.Column(db.String)
    gr_no_ref = db.Column(db.String(255))
    gr_ref_month = db.Column(db.String(255))
    gr_ref_year = db.Column(db.Integer)
    gr_depart = db.Column(db.String(255))
    gr_reset_month = db.Column(db.String)
    pi_no_ref = db.Column(db.String(255))
    pi_ref_month = db.Column(db.String(255))
    pi_ref_year = db.Column(db.Integer)
    pi_depart = db.Column(db.String(255))
    pi_reset_month = db.Column(db.String)
    pr_no_ref = db.Column(db.String(255))
    pr_ref_month = db.Column(db.String(255))
    pr_ref_year = db.Column(db.Integer)
    pr_depart = db.Column(db.String(255))
    pr_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)
    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)
    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)
    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)
    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)
    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    so_no_ref = db.Column(db.String(255))
    so_ref_month = db.Column(db.String(255))
    so_ref_year = db.Column(db.Integer)
    so_depart = db.Column(db.String(255))
    so_reset_month = db.Column(db.String)
    sl_no_ref = db.Column(db.String(255))
    sl_ref_month = db.Column(db.String(255))
    sl_ref_year = db.Column(db.Integer)
    sl_depart = db.Column(db.String(255))
    sl_reset_month = db.Column(db.String)
    ip_no_ref = db.Column(db.String(255))
    ip_ref_month = db.Column(db.String(255))
    ip_ref_year = db.Column(db.Integer)
    ip_depart = db.Column(db.String(255))
    ip_reset_month = db.Column(db.String)
    fp_no_ref = db.Column(db.String(255))
    fp_ref_month = db.Column(db.String(255))
    fp_ref_year = db.Column(db.Integer)
    fp_depart = db.Column(db.String(255))
    fp_reset_month = db.Column(db.String)

    rpen_no_ref = db.Column(db.String(255))
    rpen_ref_month = db.Column(db.String(255))
    rpen_ref_year = db.Column(db.Integer)
    rpen_depart = db.Column(db.String(255))
    rpen_reset_month = db.Column(db.String)

    mutasiantarlok_no_ref = db.Column(db.String(255))
    mutasiantarlok_ref_month = db.Column(db.String(255))
    mutasiantarlok_ref_year = db.Column(db.Integer)
    mutasiantarlok_depart = db.Column(db.String(255))
    mutasiantarlok_reset_month = db.Column(db.Integer)
    korpersediaan_no_ref = db.Column(db.String(255))
    korpersediaan_ref_month = db.Column(db.String(255))
    korpersediaan_ref_year = db.Column(db.Integer)
    korpersediaan_depart = db.Column(db.String(255))
    korpersediaan_reset_month = db.Column(db.Integer)
    pemakaianbb_no_ref = db.Column(db.String(255))
    pemakaianbb_ref_month = db.Column(db.String(255))
    pemakaianbb_ref_year = db.Column(db.Integer)
    pemakaianbb_depart = db.Column(db.String(255))
    pemakaianbb_reset_month = db.Column(db.Integer)
    penerimaanhj_no_ref = db.Column(db.String(255))
    penerimaanhj_ref_month = db.Column(db.String(255))
    penerimaanhj_ref_year = db.Column(db.Integer)
    penerimaanhj_depart = db.Column(db.String(255))
    penerimaanhj_reset_month = db.Column(db.Integer)
    memorial_no_ref = db.Column(db.String(255))
    memorial_ref_month = db.Column(db.String(255))
    memorial_ref_year = db.Column(db.Integer)
    memorial_depart = db.Column(db.String(255))
    memorial_reset_month = db.Column(db.Integer)
    pengeluaran_no_ref = db.Column(db.String(255))
    pengeluaran_ref_month = db.Column(db.String(255))
    pengeluaran_ref_year = db.Column(db.Integer)
    pengeluaran_depart = db.Column(db.String(255))
    pengeluaran_reset_month = db.Column(db.Integer)
    pencairangirokeluar_no_ref = db.Column(db.String(255))
    pencairangirokeluar_ref_month = db.Column(db.String(255))
    pencairangirokeluar_ref_year = db.Column(db.Integer)
    pencairangirokeluar_depart = db.Column(db.String(255))
    pencairangirokeluar_reset_month = db.Column(db.Integer)
    koreksihutang_no_ref = db.Column(db.String(255))
    koreksihutang_ref_month = db.Column(db.String(255))
    koreksihutang_ref_year = db.Column(db.Integer)
    koreksihutang_depart = db.Column(db.String(255))
    koreksihutang_reset_month = db.Column(db.Integer)
    pemasukan_no_ref = db.Column(db.String(255))
    pemasukan_ref_month = db.Column(db.String(255))
    pemasukan_ref_year = db.Column(db.Integer)
    pemasukan_depart = db.Column(db.String(255))
    pemasukan_reset_month = db.Column(db.Integer)
    pencairangiromasuk_no_ref = db.Column(db.String(255))
    pencairangiromasuk_ref_month = db.Column(db.String(255))
    pencairangiromasuk_ref_year = db.Column(db.Integer)
    pencairangiromasuk_depart = db.Column(db.String(255))
    pencairangiromasuk_reset_month = db.Column(db.Integer)
    koreksipiutang_no_ref = db.Column(db.String(255))
    koreksipiutang_ref_month = db.Column(db.String(255))
    koreksipiutang_ref_year = db.Column(db.Integer)
    koreksipiutang_depart = db.Column(db.String(255))
    koreksipiutang_reset_month = db.Column(db.Integer)
    mesin_no_ref = db.Column(db.String(255))
    mesin_ref_month = db.Column(db.String(255))
    mesin_ref_year = db.Column(db.Integer)
    mesin_depart = db.Column(db.String(255))
    mesin_reset_month = db.Column(db.Integer)

    formula_no_ref = db.Column(db.String(255))
    formula_ref_month = db.Column(db.String(255))
    formula_ref_year = db.Column(db.Integer)
    formula_depart = db.Column(db.String(255))
    formula_reset_month = db.Column(db.Integer)
    planning_no_ref = db.Column(db.String(255))
    planning_ref_month = db.Column(db.String(255))
    planning_ref_year = db.Column(db.Integer)
    planning_depart = db.Column(db.String(255))
    planning_reset_month = db.Column(db.Integer)
    batch_no_ref = db.Column(db.String(255))
    batch_ref_month = db.Column(db.String(255))
    batch_ref_year = db.Column(db.Integer)
    batch_depart = db.Column(db.String(255))
    batch_reset_month = db.Column(db.Integer)
    penerimaanhasiljadi_no_ref = db.Column(db.String(255))
    penerimaanhasiljadi_ref_month = db.Column(db.String(255))
    penerimaanhasiljadi_ref_year = db.Column(db.Integer)
    penerimaanhasiljadi_depart = db.Column(db.String(255))
    penerimaanhasiljadi_reset_month = db.Column(db.Integer)
    pembebanan_no_ref = db.Column(db.String(255))
    pembebanan_ref_month = db.Column(db.String(255))
    pembebanan_ref_year = db.Column(db.Integer)
    pembebanan_depart = db.Column(db.String(255))
    pembebanan_reset_month = db.Column(db.Integer)

    def __init__(
        self,
        cp_id,
        rp_no_ref,
        rp_ref_month,
        rp_ref_year,
        rp_depart,
        rp_reset_month,
        po_no_ref,
        po_ref_month,
        po_ref_year,
        po_depart,
        po_reset_month,
        gr_no_ref,
        gr_ref_month,
        gr_ref_year,
        gr_depart,
        gr_reset_month,
        pi_no_ref,
        pi_ref_month,
        pi_ref_year,
        pi_depart,
        pi_reset_month,
        pr_no_ref,
        pr_ref_month,
        pr_ref_year,
        pr_depart,
        pr_reset_month,
        so_no_ref,
        so_ref_month,
        so_ref_year,
        so_depart,
        so_reset_month,
        sl_no_ref,
        sl_ref_month,
        sl_ref_year,
        sl_depart,
        sl_reset_month,
        ip_no_ref,
        ip_ref_month,
        ip_ref_year,
        ip_depart,
        ip_reset_month,
        fp_no_ref,
        fp_ref_month,
        fp_ref_year,
        fp_depart,
        fp_reset_month,
        rpen_no_ref,
        rpen_ref_month,
        rpen_ref_year,
        rpen_depart,
        rpen_reset_month,
        mutasiantarlok_no_ref,
        mutasiantarlok_ref_month,
        mutasiantarlok_ref_year,
        mutasiantarlok_depart,
        mutasiantarlok_reset_month,
        korpersediaan_no_ref,
        korpersediaan_ref_month,
        korpersediaan_ref_year,
        korpersediaan_depart,
        korpersediaan_reset_month,
        pemakaianbb_no_ref,
        pemakaianbb_ref_month,
        pemakaianbb_ref_year,
        pemakaianbb_depart,
        pemakaianbb_reset_month,
        penerimaanhj_no_ref,
        penerimaanhj_ref_month,
        penerimaanhj_ref_year,
        penerimaanhj_depart,
        penerimaanhj_reset_month,
        memorial_no_ref,
        memorial_ref_month,
        memorial_ref_year,
        memorial_depart,
        memorial_reset_month,
        pengeluaran_no_ref,
        pengeluaran_ref_month,
        pengeluaran_ref_year,
        pengeluaran_depart,
        pengeluaran_reset_month,
        pencairangirokeluar_no_ref,
        pencairangirokeluar_ref_month,
        pencairangirokeluar_ref_year,
        pencairangirokeluar_depart,
        pencairangirokeluar_reset_month,
        koreksihutang_no_ref,
        koreksihutang_ref_month,
        koreksihutang_ref_year,
        koreksihutang_depart,
        koreksihutang_reset_month,
        pemasukan_no_ref,
        pemasukan_ref_month,
        pemasukan_ref_year,
        pemasukan_depart,
        pemasukan_reset_month,
        pencairangiromasuk_no_ref,
        pencairangiromasuk_ref_month,
        pencairangiromasuk_ref_year,
        pencairangiromasuk_depart,
        pencairangiromasuk_reset_month,
        koreksipiutang_no_ref,
        koreksipiutang_ref_month,
        koreksipiutang_ref_year,
        koreksipiutang_depart,
        koreksipiutang_reset_month,
        mesin_no_ref,
        mesin_ref_month,
        mesin_ref_year,
        mesin_depart,
        mesin_reset_month,
        formula_no_ref,
        formula_ref_month,
        formula_ref_year,
        formula_depart,
        formula_reset_month,
        planning_no_ref,
        planning_ref_month,
        planning_ref_year,
        planning_depart,
        planning_reset_month,
        batch_no_ref,
        batch_ref_month,
        batch_ref_year,
        batch_depart,
        batch_reset_month,
        penerimaanhasiljadi_no_ref,
        penerimaanhasiljadi_ref_month,
        penerimaanhasiljadi_ref_year,
        penerimaanhasiljadi_depart,
        penerimaanhasiljadi_reset_month,
        pembebanan_no_ref,
        pembebanan_ref_month,
        pembebanan_ref_year,
        pembebanan_depart,
        pembebanan_reset_month,

    ):
        self.cp_id = cp_id
        self.rp_no_ref = rp_no_ref
        self.rp_ref_month = rp_ref_month
        self.rp_ref_year = rp_ref_year
        self.rp_depart = rp_depart
        self.rp_reset_month = rp_reset_month
        self.po_no_ref = po_no_ref
        self.po_ref_month = po_ref_month
        self.po_ref_year = po_ref_year
        self.po_depart = po_depart
        self.po_reset_month = po_reset_month
        self.gr_no_ref = gr_no_ref
        self.gr_ref_month = gr_ref_month
        self.gr_ref_year = gr_ref_year
        self.gr_depart = gr_depart
        self.gr_reset_month = gr_reset_month
        self.pi_no_ref = pi_no_ref
        self.pi_ref_month = pi_ref_month
        self.pi_ref_year = pi_ref_year
        self.pi_depart = pi_depart
        self.pi_reset_month = pi_reset_month
        self.pr_no_ref = pr_no_ref
        self.pr_ref_month = pr_ref_month
        self.pr_ref_year = pr_ref_year
        self.pr_depart = pr_depart
        self.pr_reset_month = pr_reset_month

        self.so_no_ref = so_no_ref
        self.so_ref_month = so_ref_month
        self.so_ref_year = so_ref_year
        self.so_depart = so_depart
        self.so_reset_month = so_reset_month
        self.sl_no_ref = sl_no_ref
        self.sl_ref_month = sl_ref_month
        self.sl_ref_year = sl_ref_year
        self.sl_depart = sl_depart
        self.sl_reset_month = sl_reset_month
        self.ip_no_ref = ip_no_ref
        self.ip_ref_month = ip_ref_month
        self.ip_ref_year = ip_ref_year
        self.ip_depart = ip_depart
        self.ip_reset_month = ip_reset_month
        self.fp_no_ref = fp_no_ref
        self.fp_ref_month = fp_ref_month
        self.fp_ref_year = fp_ref_year
        self.fp_depart = fp_depart
        self.fp_reset_month = fp_reset_month
        self.rpen_no_ref = rpen_no_ref
        self.rpen_ref_month = rpen_ref_month
        self.rpen_ref_year = rpen_ref_year
        self.rpen_depart = rpen_depart
        self.rpen_reset_month = rpen_reset_month

        self.mutasiantarlok_no_ref = mutasiantarlok_no_ref
        self.mutasiantarlok_ref_month = mutasiantarlok_ref_month
        self.mutasiantarlok_ref_year = mutasiantarlok_ref_year
        self.mutasiantarlok_depart = mutasiantarlok_depart
        self.mutasiantarlok_reset_month = mutasiantarlok_reset_month

        self.korpersediaan_no_ref = korpersediaan_no_ref
        self.korpersediaan_ref_month = korpersediaan_ref_month
        self.korpersediaan_ref_year = korpersediaan_ref_year
        self.korpersediaan_depart = korpersediaan_depart
        self.korpersediaan_reset_month = korpersediaan_reset_month

        self.pemakaianbb_no_ref = pemakaianbb_no_ref
        self.pemakaianbb_ref_month = pemakaianbb_ref_month
        self.pemakaianbb_ref_year = pemakaianbb_ref_year
        self.pemakaianbb_depart = pemakaianbb_depart
        self.pemakaianbb_reset_month = pemakaianbb_reset_month

        self.penerimaanhj_no_ref = penerimaanhj_no_ref
        self.penerimaanhj_ref_month = penerimaanhj_ref_month
        self.penerimaanhj_ref_year = penerimaanhj_ref_year
        self.penerimaanhj_depart = penerimaanhj_depart
        self.penerimaanhj_reset_month = penerimaanhj_reset_month

        self.memorial_no_ref = memorial_no_ref
        self.memorial_ref_month = memorial_ref_month
        self.memorial_ref_year = memorial_ref_year
        self.memorial_depart = memorial_depart
        self.memorial_reset_month = memorial_reset_month

        self.pengeluaran_no_ref = pengeluaran_no_ref
        self.pengeluaran_ref_month = pengeluaran_ref_month
        self.pengeluaran_ref_year = pengeluaran_ref_year
        self.pengeluaran_depart = pengeluaran_depart
        self.pengeluaran_reset_month = pengeluaran_reset_month

        self.pencairangirokeluar_no_ref = pencairangirokeluar_no_ref
        self.pencairangirokeluar_ref_month = pencairangirokeluar_ref_month
        self.pencairangirokeluar_ref_year = pencairangirokeluar_ref_year
        self.pencairangirokeluar_depart = pencairangirokeluar_depart
        self.pencairangirokeluar_reset_month = pencairangirokeluar_reset_month

        self. koreksihutang_no_ref = koreksihutang_no_ref
        self. koreksihutang_ref_month = koreksihutang_ref_month
        self. koreksihutang_ref_year = koreksihutang_ref_year
        self. koreksihutang_depart = koreksihutang_depart
        self. koreksihutang_reset_month = koreksihutang_reset_month

        self. pemasukan_no_ref = pemasukan_no_ref
        self. pemasukan_ref_month = pemasukan_ref_month
        self. pemasukan_ref_year = pemasukan_ref_year
        self. pemasukan_depart = pemasukan_depart
        self. pemasukan_reset_month = pemasukan_reset_month

        self.pencairangiromasuk_no_ref = pencairangiromasuk_no_ref
        self.pencairangiromasuk_ref_month = pencairangiromasuk_ref_month
        self.pencairangiromasuk_ref_year = pencairangiromasuk_ref_year
        self.pencairangiromasuk_depart = pencairangiromasuk_depart
        self.pencairangiromasuk_reset_month = pencairangiromasuk_reset_month

        self.koreksipiutang_no_ref = koreksipiutang_no_ref
        self.koreksipiutang_ref_month = koreksipiutang_ref_month
        self.koreksipiutang_ref_year = koreksipiutang_ref_year
        self.koreksipiutang_depart = koreksipiutang_depart
        self.koreksipiutang_reset_month = koreksipiutang_reset_month

        self.mesin_no_ref = mesin_no_ref
        self.mesin_ref_month = mesin_ref_month
        self.mesin_ref_year = mesin_ref_year
        self.mesin_depart = mesin_depart
        self.mesin_reset_month = mesin_reset_month

        self.formula_no_ref = formula_no_ref
        self.formula_ref_month = formula_ref_month
        self.formula_ref_year = formula_ref_year
        self.formula_depart = formula_depart
        self.formula_reset_month = formula_reset_month

        self.planning_no_ref = planning_no_ref
        self.planning_ref_month = planning_ref_month
        self.planning_ref_year = planning_ref_year
        self.planning_depart = planning_depart
        self.planning_reset_month = planning_reset_month

        self.batch_no_ref = batch_no_ref
        self.batch_ref_month = batch_ref_month
        self.batch_ref_year = batch_ref_year
        self.batch_depart = batch_depart
        self.batch_reset_month = batch_reset_month

        self.penerimaanhasiljadi_no_ref = penerimaanhasiljadi_no_ref
        self.penerimaanhasiljadi_ref_month = penerimaanhasiljadi_ref_month
        self.penerimaanhasiljadi_ref_year = penerimaanhasiljadi_ref_year
        self.penerimaanhasiljadi_depart = penerimaanhasiljadi_depart
        self.penerimaanhasiljadi_reset_month = penerimaanhasiljadi_reset_month

        self.pembebanan_no_ref = pembebanan_no_ref
        self.pembebanan_ref_month = pembebanan_ref_month
        self.pembebanan_ref_year = pembebanan_ref_year
        self.pembebanan_depart = pembebanan_depart
        self.pembebanan_reset_month = pembebanan_reset_month
