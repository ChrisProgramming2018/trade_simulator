# stock_market_sim/main.py
import tkinter as tk
from ui.app import StockApp

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x700")
    root.title("Stock Market Simulator")
    app = StockApp(root)
    root.mainloop()
