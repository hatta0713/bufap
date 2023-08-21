import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

DEFAULT_HOST = "192.168.17.101"
DEFAULT_USER = "admin"
DEFAULT_PASS = "password"


class MainView(tk.Frame):
    def __init__(self, parent):
        print("MainView:__init__")
        super().__init__(parent)

        self.create_widget()
        self.pack(expand=True, fill=tk.BOTH)

    def create_widget(self):
        upper_frame = tk.Frame(self)
        upper_frame.pack(expand=False, anchor=tk.NW)

        self.login_view = LoginView(upper_frame)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)

        self.conf_view = ConfView(notebook)
        self.wm_view = WirelessMonitorView(notebook)
        self.cm_view = ClientMonitorView(notebook)
        self.exec_view = ExecView(notebook)

        notebook.add(self.conf_view, text="設定")
        notebook.add(self.wm_view, text="ワイヤレス環境モニタ")
        notebook.add(self.cm_view, text="クライアントモニタ")
        notebook.add(self.exec_view, text="コマンド実行")

    def set_data(
        self, sample_conf=None, sample_wm=None, sample_cm=None, sample_exec=None
    ):
        if sample_conf is not None:
            self.conf_view.set_rows(sample_conf)
        if sample_cm is not None:
            self.cm_view.set_rows(sample_cm)
        if sample_wm is not None:
            self.wm_view.set_rows(sample_wm)
        if sample_exec is not None:
            self.exec_view.set_data(sample_exec)


class LoginView(tk.Frame):
    def __init__(
        self,
        parent,
        hostname: str = DEFAULT_HOST,
        username: str = DEFAULT_USER,
        password: str = DEFAULT_PASS,
    ):
        print("LoginView:__init__")

        super().__init__(parent)

        self.hostname = tk.StringVar(value=hostname)
        self.username = tk.StringVar(value=username)
        self.password = tk.StringVar(value=password)

        self.create_widget()
        self.pack()

    def create_widget(self):
        print("LoginView:create_widget")
        tk.Label(self, text="IPアドレス").pack(side=tk.LEFT)
        tk.Entry(self, width=15, textvariable=self.hostname).pack(side=tk.LEFT, padx=5)

        tk.Label(self, text="ユーザー名").pack(side=tk.LEFT)
        tk.Entry(self, width=15, textvariable=self.username).pack(side=tk.LEFT, padx=5)

        tk.Label(self, text="パスワード").pack(side=tk.LEFT)
        tk.Entry(self, width=15, textvariable=self.password).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="情報取得", command=self.get_info).pack(side=tk.LEFT)

    def set_action(self, func):
        pass

    def get_info(self):
        tk.messagebox.showinfo("(view)", "情報取得ボタンが押下されました")


class ConfView(tk.Frame):
    DISP_ALL = 0
    DISP_USER_ONLY = 1

    def __init__(self, parent):
        print("ConfView:__init__")
        super().__init__(parent)

        self.disp_mode = tk.IntVar()
        self.disp_mode.set(self.DISP_ALL)
        self.create_widget()
        self.pack(expand=True)

    def get_columns(self):
        columns = {self.DISP_USER_ONLY: ["ユーザー設定"], self.DISP_ALL: ["ユーザー設定", "初期値"]}
        print(self.disp_mode.get())

        return columns[self.disp_mode.get()]

    def create_widget(self):
        upper_frame = tk.Frame(self)
        upper_frame.pack(expand=False, fill=tk.X)
        self.radio_button1 = tk.Radiobutton(
            upper_frame,
            text="全て",
            value=self.DISP_ALL,
            variable=self.disp_mode,
            command=self.radio_click,
        )
        self.radio_button1.pack(side=tk.LEFT)

        self.radio_button2 = tk.Radiobutton(
            upper_frame,
            text="ユーザー設定のみ",
            value=self.DISP_USER_ONLY,
            variable=self.disp_mode,
            command=self.radio_click,
        )
        self.radio_button2.pack(side=tk.LEFT)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(expand=True, fill=tk.BOTH)
        self.tree = ttk.Treeview(bottom_frame, columns=self.get_columns())
        self.tree["show"] = "headings"

        ysbar = tk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysbar.set)

        # xsbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        # self.tree.configure(xscrollcommand=xsbar.set)

        # xsbar.pack(side=tk.BOTTOM, fill="x")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ysbar.pack(side=tk.RIGHT, fill=tk.Y)

    def set_colomns(self):
        """
        テーブルの列名を指定
        """
        columns = self.get_columns()
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)

    def set_row(self, index="", row_data=[]):
        """
        新規レコードの挿入
        """
        self.tree.insert("", index="end", text=index, values=row_data)

    def set_rows(self, rows_data):
        """
        複数の新規レコードの挿入
        """
        for i, row_data in enumerate(rows_data):
            self.set_row(index=i, row_data=row_data)

    def delete_rows(self):
        """
        レコードの全削除
        """
        children = self.tree.get_children("")
        for child in children:
            self.tree.delete(child)

    def radio_click(self):
        tk.messagebox.showinfo("(view)", f"{self.disp_mode.get()}が選択されました")

    def set_radio_click_command(self, command):
        self.radio_button1["command"] = command
        self.radio_button2["command"] = command


class ExecView(tk.Frame):
    def __init__(self, parent):
        print("ExecView:__init__")
        super().__init__(parent)

        self.create_widget()
        self.pack()

    def create_widget(self):
        self.exec_button = tk.Button(self, text="実行", command=self.click_exec_button)
        self.exec_button.pack(anchor=tk.W)
        tk.Text(self).pack(expand=True, fill=tk.BOTH)

    def click_exec_button(self):
        tk.messagebox.showinfo("(view)", "実行ボタンがクリックされました")


class ClientMonitorView(tk.Frame):
    def __init__(self, parent):
        print("ClientMonitorView:__init__")
        super().__init__(parent)

        self.create_widget()
        self.pack()

    def create_widget(self):
        self.tree = ttk.Treeview(self, columns=self.get_columns())
        self.tree["show"] = "headings"

        ysbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysbar.set)

        ysbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.set_columns()

    def get_columns(self):
        columns = [
            {"name": "band", "width": 50, "anchor": tk.CENTER},
            {"name": "SSID", "width": len("XXXXXXXXXXXXXXXXXX") * 8, "anchor": tk.W},
            {
                "name": "MAC",
                "width": len("XX:XX:XX:XX:XX:XX") * 8,
                "anchor": tk.CENTER,
            },
            {"name": "Vendor", "width": 20 * 8, "anchor": tk.W},
            {"name": "Tx", "width": 5 * 8, "anchor": tk.CENTER},
            {"name": "Rx", "width": 5 * 8, "anchor": tk.CENTER},
            {"name": "RSSI", "width": 5 * 8, "anchor": tk.CENTER},
            {"name": "connect", "width": 15 * 8, "anchor": tk.CENTER},
            {"name": "idle", "width": 5 * 8, "anchor": tk.CENTER},
        ]

        return columns

    def set_columns(self):
        self.tree["columns"] = [c["name"] for c in self.get_columns()]
        for col in self.get_columns():
            self.tree.heading(col["name"], text=col["name"])
            self.tree.column(col["name"], width=col["width"], anchor=col["anchor"])

    def set_row(self, index="", row_data=[]):
        """
        新規レコードの挿入
        """
        self.tree.insert("", index="end", text=index, values=row_data)

    def set_rows(self, rows_data):
        """
        複数の新規レコードの挿入
        """
        for i, row_data in enumerate(rows_data):
            self.set_row(index=i, row_data=row_data)

    def delete_rows(self):
        """
        レコードの全削除
        """
        children = self.tree.get_children("")
        for child in children:
            self.tree.delete(child)


class WirelessMonitorView(tk.Frame):
    def __init__(self, parent):
        print("WirelessMonitorView:__init__")
        super().__init__(parent)

        self.create_widget()
        self.pack()

    def create_widget(self):
        self.tree = ttk.Treeview(self, columns=self.get_columns())
        self.tree["show"] = "headings"

        ysbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysbar.set)

        ysbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.set_columns()

    def get_columns(self):
        columns = [
            {"name": "Index", "width": 5 * 8, "anchor": tk.CENTER},
            {
                "name": "MAC",
                "width": len("XX:XX:XX:XX:XX:XX") * 8,
                "anchor": tk.CENTER,
            },
            {"name": "Vendor", "width": 20 * 8, "anchor": tk.W},
            {"name": "SSID", "width": len("XXXXXXXXXXXXXXXXXX") * 8, "anchor": tk.W},
            {"name": "Channel", "width": 3 * 8, "anchor": tk.CENTER},
            {"name": "Mode", "width": 10 * 8, "anchor": tk.CENTER},
            {"name": "RSSI", "width": 5 * 8, "anchor": tk.CENTER},
            {"name": "Noise", "width": 5 * 8, "anchor": tk.CENTER},
            {"name": "Security", "width": 15 * 8, "anchor": tk.CENTER},
        ]

        return columns

    def set_columns(self):
        self.tree["columns"] = [c["name"] for c in self.get_columns()]
        for col in self.get_columns():
            self.tree.heading(col["name"], text=col["name"])
            self.tree.column(col["name"], width=col["width"], anchor=col["anchor"])

    def set_row(self, index="", row_data=[]):
        """
        新規レコードの挿入
        """
        self.tree.insert("", index="end", text=index, values=row_data)

    def set_rows(self, rows_data):
        """
        複数の新規レコードの挿入
        """
        for i, row_data in enumerate(rows_data):
            self.set_row(index=i, row_data=row_data)

    def delete_rows(self):
        """
        レコードの全削除
        """
        children = self.tree.get_children("")
        for child in children:
            self.tree.delete(child)


if __name__ == "__main__":
    import samples

    root = tk.Tk()
    root.title("sample1view")
    main_view = MainView(root)
    main_view.set_data(
        sample_conf=samples.SAMPLE_CONF,
        sample_wm=samples.SAMPLE_WM,
        sample_cm=samples.SAMPLE_CM,
    )
    root.geometry("900x500")
    root.mainloop()
