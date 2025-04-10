import tkinter as tk
from ui.main_frame import MainFrame
from ui.market_frame import MarketFrame
from ui.history_frame import HistoryFrame
from ui.company_frame import CompanyFrame

class StockApp:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        for F in (MainFrame, MarketFrame, HistoryFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container = container
        self.show_frame("MainFrame")

    def show_frame(self, name, **kwargs):
        frame = self.frames.get(name)
        if not frame:
            if name == "CompanyFrame":
                frame = CompanyFrame(parent=self.container, controller=self, ticker=kwargs['ticker'])
                self.frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh(**kwargs)
