import tkinter as tk
from tkinter import ttk
from core.portfolio import Portfolio
from core.market import Market
from charts.plot import plot_portfolio_value
import os
import json

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.portfolio = Portfolio()
        self.market = Market(self.get_available_tickers())

        self.time_range = tk.StringVar(value="1mo")

        self.build_ui()

    def get_available_tickers(self):
        config_path = "assets/config.json"
        if not os.path.exists(config_path):
            return ["NVDA", "AMD"]
        with open(config_path, "r") as f:
            data = json.load(f)
            return data.get("tickers", ["NVDA", "AMD"])

    def build_ui(self):
        tk.Label(self, text="Portfolio Overview", font=("Arial", 20)).pack(pady=10)

        # Cash & Summary
        self.summary = tk.Label(self, font=("Arial", 14), justify="left")
        self.summary.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="+ €100", command=lambda: self.add_cash(100)).pack(side="left", padx=5)
        tk.Button(button_frame, text="+ €500", command=lambda: self.add_cash(500)).pack(side="left", padx=5)

        # Time Range
        tk.Label(self, text="Chart Time Range:").pack(pady=5)
        time_options = ["5d", "1mo", "3mo", "6mo", "1y", "5y", "max"]
        ttk.OptionMenu(self, self.time_range, self.time_range.get(), *time_options, command=self.update_chart).pack()

        # Chart Placeholder
        self.chart_placeholder = tk.Label(self)
        self.chart_placeholder.pack(pady=10)

        # Holdings Table
        self.holdings_table = tk.Text(self, height=10, width=90)
        self.holdings_table.pack(pady=5)

        # Navigation
        nav = tk.Frame(self)
        nav.pack(pady=10)
        tk.Button(nav, text="Market", command=lambda: self.controller.show_frame("MarketFrame")).pack(side="left", padx=5)
        tk.Button(nav, text="History", command=lambda: self.controller.show_frame("HistoryFrame")).pack(side="left", padx=5)

    def refresh(self, **kwargs):
        self.market.update_prices()
        self.update_summary()
        self.update_holdings()
        self.update_chart(self.time_range.get())

    def update_summary(self):
        prices = self.market.get_all_prices()
        total = self.portfolio.get_total_value(prices)
        invested = total - self.portfolio.cash
        summary_text = f"Current Day\nCash: €{self.portfolio.cash:.2f}\nInvested: €{invested:.2f}\nTotal: €{total:.2f}"
        self.summary.config(text=summary_text)

    def update_holdings(self):
        prices = self.market.get_all_prices()
        lines = ["Ticker\tShares\tAvg Price\tInvested\tCurrent\tChange (%)"]
        for ticker, info in self.portfolio.holdings.items():
            shares = info['shares']
            avg_price = info['avg_price']
            current_price = prices.get(ticker, 0)
            invested = shares * avg_price
            current = shares * current_price
            change = ((current - invested) / invested * 100) if invested > 0 else 0
            lines.append(f"{ticker}\t{shares}\t{avg_price:.2f}\t{invested:.2f}\t{current:.2f}\t{change:.2f}%")
        self.holdings_table.delete(1.0, tk.END)
        self.holdings_table.insert(tk.END, "\n".join(lines))

    def update_chart(self, period):
        fig_path = plot_portfolio_value(self.portfolio, self.market, period)
        if os.path.exists(fig_path):
            img = tk.PhotoImage(file=fig_path)
            self.chart_placeholder.configure(image=img)
            self.chart_placeholder.image = img

    def add_cash(self, amount):
        self.portfolio.add_cash(amount)
        self.refresh()
