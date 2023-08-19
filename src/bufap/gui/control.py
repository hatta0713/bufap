import tkinter as tk

from bufap.gui.views import MainView


class MainLogic:
    def __init__(self):
        pass


class MainControl:
    def __init__(self):
        root = tk.Tk()
        root.title("sample1view")
        self.main_view = MainView(root)
        root.geometry("900x500")
        self.set_conf_radio_command()
        root.mainloop()

    def set_conf_radio_command(self):
        print("MainControl:set_conf_radio_command")
        self.main_view.conf_view.set_radio_click_command(self.radio_click_command)

    def radio_click_command(self):
        print("radio_click_command")
        tk.messagebox.showinfo(
            "確認", f"（変更）表示モードが選択されました{self.main_view.conf_view.disp_mode.get()}"
        )


if __name__ == "__main__":
    control = MainControl()
