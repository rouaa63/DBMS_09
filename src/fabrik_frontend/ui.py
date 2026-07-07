import tkinter as tk
from tkinter import ttk, messagebox
from fabrik_frontend import api


class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        master.title("Factory Demo – Material Planning")
        master.minsize(820, 520)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self._build_parts_tab(notebook)
        self._build_products_tab(notebook)
        self._build_bom_tab(notebook)
        self._build_warnings_tab(notebook)

        self._refresh_all()

    # ------------------------------------------------------------------
    # Parts tab
    # ------------------------------------------------------------------

    def _build_parts_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Parts")

        # Treeview
        cols = ("id", "name", "unit", "stock", "min_stock", "reorder")
        self._parts_tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for col, heading, width in [
            ("id",       "ID",             40),
            ("name",     "Part",          180),
            ("unit",     "Unit",           60),
            ("stock",    "Stock",          70),
            ("min_stock","Min stock",      70),
            ("reorder",  "Reorder?",       70),
        ]:
            self._parts_tree.heading(col, text=heading)
            self._parts_tree.column(col, width=width, anchor=tk.CENTER)
        self._parts_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        btn_row = ttk.Frame(frame)
        btn_row.pack(fill=tk.X)
        ttk.Button(btn_row, text="Refresh",        command=self._load_parts).pack(side=tk.LEFT, padx=4)

        # Deliver parts form
        delivery = ttk.LabelFrame(frame, text=" Deliver parts (POST /wareneingang) ")
        delivery.pack(fill=tk.X, pady=8)
        self._d_teil_id = self._labeled_entry(delivery, "Part ID", 0)
        self._d_menge   = self._labeled_entry(delivery, "Quantity", 1)
        self._d_notiz   = self._labeled_entry(delivery, "Note (optional)", 2)
        ttk.Button(delivery, text="Deliver",
                   command=self._deliver).grid(row=3, column=1, pady=6, sticky=tk.W)

        # Stocktake form
        stocktake = ttk.LabelFrame(frame, text=" Set stock manually – stocktake (PUT /teile/{id}) ")
        stocktake.pack(fill=tk.X, pady=4)
        self._s_teil_id = self._labeled_entry(stocktake, "Part ID", 0)
        self._s_bestand = self._labeled_entry(stocktake, "New stock", 1)
        ttk.Button(stocktake, text="Set stock",
                   command=self._set_stock).grid(row=2, column=1, pady=6, sticky=tk.W)

    def _load_parts(self):
        for row in self._parts_tree.get_children():
            self._parts_tree.delete(row)
        try:
            for p in api.get_teile():
                self._parts_tree.insert("", tk.END, values=(
                    p["id"], p["name"], p["einheit"],
                    p["bestand"], p["mindestbestand"],
                    "YES" if p["unter_mindestbestand"] else "no",
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _deliver(self):
        try:
            result = api.post_wareneingang(
                int(self._d_teil_id.get()),
                int(self._d_menge.get()),
                self._d_notiz.get(),
            )
            messagebox.showinfo("Delivered", str(result))
            self._load_parts()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _set_stock(self):
        try:
            result = api.put_teil_bestand(
                int(self._s_teil_id.get()),
                int(self._s_bestand.get()),
            )
            messagebox.showinfo("Updated", str(result))
            self._load_parts()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------
    # Products tab
    # ------------------------------------------------------------------

    def _build_products_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Products")

        cols = ("id", "name", "stock", "total_produced", "total_checked_out")
        self._prod_tree = ttk.Treeview(frame, columns=cols, show="headings", height=8)
        for col, heading, width in [
            ("id",                "ID",             40),
            ("name",              "Product",       200),
            ("stock",             "In stock",       80),
            ("total_produced",    "Total produced", 100),
            ("total_checked_out", "Total out",      80),
        ]:
            self._prod_tree.heading(col, text=heading)
            self._prod_tree.column(col, width=width, anchor=tk.CENTER)
        self._prod_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        ttk.Button(frame, text="Refresh", command=self._load_products).pack(anchor=tk.W)

        prod_form = ttk.LabelFrame(frame, text=" Record production run (POST /produktion) ")
        prod_form.pack(fill=tk.X, pady=8)
        self._p_prod_id = self._labeled_entry(prod_form, "Product ID", 0)
        self._p_menge   = self._labeled_entry(prod_form, "Quantity", 1)
        ttk.Button(prod_form, text="Produce",
                   command=self._produce).grid(row=2, column=1, pady=6, sticky=tk.W)

        out_form = ttk.LabelFrame(frame, text=" Check out from warehouse (POST /lagerausgang) ")
        out_form.pack(fill=tk.X, pady=4)
        self._o_prod_id = self._labeled_entry(out_form, "Product ID", 0)
        self._o_menge   = self._labeled_entry(out_form, "Quantity", 1)
        self._o_notiz   = self._labeled_entry(out_form, "Note (optional)", 2)
        ttk.Button(out_form, text="Check out",
                   command=self._checkout).grid(row=3, column=1, pady=6, sticky=tk.W)

    def _load_products(self):
        for row in self._prod_tree.get_children():
            self._prod_tree.delete(row)
        try:
            for p in api.get_produkte():
                self._prod_tree.insert("", tk.END, values=(
                    p["id"], p["name"], p["bestand"],
                    p["gesamt_produziert"], p["gesamt_ausgecheckt"],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _produce(self):
        try:
            result = api.post_produktion(
                int(self._p_prod_id.get()), int(self._p_menge.get()))
            messagebox.showinfo("Produced", str(result))
            self._load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _checkout(self):
        try:
            result = api.post_lagerausgang(
                int(self._o_prod_id.get()),
                int(self._o_menge.get()),
                self._o_notiz.get(),
            )
            messagebox.showinfo("Checked out", str(result))
            self._load_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------
    # Bill of materials tab
    # ------------------------------------------------------------------

    def _build_bom_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Bill of Materials")

        input_row = ttk.Frame(frame)
        input_row.pack(fill=tk.X, pady=6)
        tk.Label(input_row, text="Product ID:").pack(side=tk.LEFT, padx=4)
        self._bom_id = ttk.Entry(input_row, width=6)
        self._bom_id.pack(side=tk.LEFT)
        ttk.Button(input_row, text="Load",
                   command=self._load_bom).pack(side=tk.LEFT, padx=6)

        cols = ("teil_id", "name", "qty", "unit")
        self._bom_tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for col, heading, width in [
            ("teil_id", "Part ID",  60),
            ("name",    "Part",    220),
            ("qty",     "Qty",      60),
            ("unit",    "Unit",     80),
        ]:
            self._bom_tree.heading(col, text=heading)
            self._bom_tree.column(col, width=width, anchor=tk.CENTER)
        self._bom_tree.pack(fill=tk.BOTH, expand=True)

    def _load_bom(self):
        for row in self._bom_tree.get_children():
            self._bom_tree.delete(row)
        try:
            for pos in api.get_stueckliste(int(self._bom_id.get())):
                self._bom_tree.insert("", tk.END, values=(
                    pos["teil_id"], pos["teil_name"],
                    pos["menge"], pos["einheit"],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------
    # Reorder warnings tab
    # ------------------------------------------------------------------

    def _build_warnings_tab(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Reorder Warnings")

        ttk.Button(frame, text="Refresh",
                   command=self._load_warnings).pack(anchor=tk.W, pady=6)

        cols = ("id", "teil_id", "name", "stock_at_warning", "timestamp")
        self._warn_tree = ttk.Treeview(frame, columns=cols, show="headings", height=14)
        for col, heading, width in [
            ("id",               "ID",          40),
            ("teil_id",          "Part ID",     60),
            ("name",             "Part",       180),
            ("stock_at_warning", "Stock",       70),
            ("timestamp",        "Timestamp",  180),
        ]:
            self._warn_tree.heading(col, text=heading)
            self._warn_tree.column(col, width=width, anchor=tk.CENTER)
        self._warn_tree.pack(fill=tk.BOTH, expand=True)

    def _load_warnings(self):
        for row in self._warn_tree.get_children():
            self._warn_tree.delete(row)
        try:
            for w in api.get_bestellwarnungen():
                self._warn_tree.insert("", tk.END, values=(
                    w["id"], w["teil_id"], w["teil_name"],
                    w["bestand_bei_warnung"], w["zeitstempel"],
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _labeled_entry(self, parent, label: str, row: int) -> ttk.Entry:
        ttk.Label(parent, text=label + ":").grid(
            row=row, column=0, padx=8, pady=4, sticky=tk.E)
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=8, pady=4, sticky=tk.W)
        return entry

    def _refresh_all(self):
        self._load_parts()
        self._load_products()
        self._load_warnings()
