import tkinter as tk
from tkinter import scrolledtext, ttk


TREND_OPTIONS = [
    "Strong Uptrend",
    "Uptrend",
    "Sideways",
    "Downtrend",
    "Strong Downtrend",
]
NEWS_OPTIONS = ["Positive", "Neutral", "Negative"]
RISK_OPTIONS = ["Conservative", "Moderate", "Aggressive"]

TREND_SCORES = {
    "strong uptrend": 2,
    "uptrend": 1,
    "sideways": 0,
    "downtrend": -1,
    "strong downtrend": -2,
}
NEWS_SCORES = {"positive": 1, "neutral": 0, "negative": -1}
RISK_BIAS = {"conservative": -0.5, "moderate": 0, "aggressive": 0.5}
VALID_INPUTS = {
    "trend": set(x.lower() for x in TREND_OPTIONS),
    "news": set(x.lower() for x in NEWS_OPTIONS),
    "risk": set(x.lower() for x in RISK_OPTIONS),
}


def expert_system(trend, news, risk):
    score = TREND_SCORES[trend] + NEWS_SCORES[news] + RISK_BIAS[risk]
    action = "BUY" if score >= 2 else "SELL" if score <= -2 else "HOLD"
    confidence = int(max(55, min(95, 60 + abs(score) * 12)))

    strategies = {
        "BUY": "Consider staggered entries and place a stop-loss below support.",
        "SELL": "Reduce exposure, avoid averaging losers, and protect capital.",
        "HOLD": "Wait for confirmation and trade only after clear breakout or reversal.",
    }

    return (
        f"Decision: {action}\n"
        f"Confidence: {confidence}%\n"
        "Rationale:\n"
        f"- Trend: {trend.title()}\n"
        f"- News Sentiment: {news.title()}\n"
        f"- Risk Profile: {risk.title()}\n"
        f"Strategy: {strategies[action]}\n"
        "Note: Educational use only, not financial advice."
    )


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Market Expert System")
        self.geometry("900x580")
        self.configure(bg="#0f172a")

        self.state = "intro"
        self.answers = {}

        self._build_header()
        self._build_tabs()
        self.reset_chat()

    def _build_header(self):
        tk.Label(
            self,
            text="Stock Market Expert System",
            bg="#111827",
            fg="#e2e8f0",
            font=("Segoe UI", 18, "bold"),
            pady=10,
        ).pack(fill="x")

    def _build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.chat_tab = tk.Frame(notebook, bg="#f8fafc")
        self.expert_tab = tk.Frame(notebook, bg="#f8fafc")
        notebook.add(self.chat_tab, text="Chat")
        notebook.add(self.expert_tab, text="Expert Panel")

        self._build_chat_tab()
        self._build_expert_tab()

    def _build_chat_tab(self):
        self.chat = scrolledtext.ScrolledText(
            self.chat_tab,
            font=("Segoe UI", 11),
            state="disabled",
            wrap="word",
            height=16,
        )
        self.chat.pack(fill="both", expand=True, padx=14, pady=(14, 8))

        row = tk.Frame(self.chat_tab, bg="#f8fafc")
        row.pack(fill="x", padx=14, pady=(0, 14))

        self.chat_entry = tk.Entry(row, font=("Segoe UI", 11))
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self.chat_entry.bind("<Return>", lambda _: self.send_chat())

        tk.Button(
            row,
            text="Send",
            command=self.send_chat,
            bg="#0284c7",
            fg="white",
            bd=0,
            padx=12,
            pady=7,
        ).pack(side="left")

        tk.Button(
            row,
            text="Reset",
            command=self.reset_chat,
            bg="#475569",
            fg="white",
            bd=0,
            padx=12,
            pady=7,
        ).pack(side="left", padx=8)

    def _build_expert_tab(self):
        self.panel_vars = {
            "Trend": tk.StringVar(value="Uptrend"),
            "News": tk.StringVar(value="Positive"),
            "Risk": tk.StringVar(value="Moderate"),
        }

        rows = [
            ("Trend", TREND_OPTIONS),
            ("News", NEWS_OPTIONS),
            ("Risk", RISK_OPTIONS),
        ]
        for i, (label, options) in enumerate(rows):
            tk.Label(
                self.expert_tab,
                text=label,
                bg="#f8fafc",
                font=("Segoe UI", 11, "bold"),
            ).grid(row=i, column=0, sticky="w", padx=16, pady=10)
            ttk.Combobox(
                self.expert_tab,
                textvariable=self.panel_vars[label],
                values=options,
                state="readonly",
                width=24,
            ).grid(row=i, column=1, sticky="w", padx=8, pady=10)

        tk.Button(
            self.expert_tab,
            text="Generate Advice",
            command=self.generate_from_panel,
            bg="#0284c7",
            fg="white",
            bd=0,
            padx=12,
            pady=7,
        ).grid(row=3, column=0, padx=16, pady=6, sticky="w")

        self.panel_output = scrolledtext.ScrolledText(
            self.expert_tab,
            font=("Segoe UI", 11),
            state="disabled",
            wrap="word",
            height=12,
        )
        self.panel_output.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=16, pady=10)

        self.expert_tab.grid_columnconfigure(1, weight=1)
        self.expert_tab.grid_rowconfigure(4, weight=1)

    def post_chat(self, role, message):
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{role}: {message}\n\n")
        self.chat.configure(state="disabled")
        self.chat.yview("end")

    def reset_chat(self):
        self.state = "intro"
        self.answers = {}
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self.post_chat("Expert", "Hello. Type yes to start your stock analysis.")

    def send_chat(self):
        raw = self.chat_entry.get().strip()
        self.chat_entry.delete(0, "end")
        if not raw:
            return

        user = raw.lower()
        self.post_chat("You", raw)

        if user in {"reset", "restart"}:
            self.reset_chat()
            return

        if self.state == "intro":
            if user in {"yes", "y"}:
                self.state = "trend"
                self.post_chat("Expert", "Enter trend: strong uptrend, uptrend, sideways, downtrend, or strong downtrend.")
            else:
                self.post_chat("Expert", "Please type yes when you are ready.")
            return

        if user not in VALID_INPUTS[self.state]:
            self.post_chat("Expert", f"Invalid {self.state}. Try valid options.")
            return

        self.answers[self.state] = user
        if self.state == "trend":
            self.state = "news"
            self.post_chat("Expert", "Enter news sentiment: positive, neutral, or negative.")
            return
        if self.state == "news":
            self.state = "risk"
            self.post_chat("Expert", "Enter risk profile: conservative, moderate, or aggressive.")
            return

        result = expert_system(self.answers["trend"], self.answers["news"], user)
        self.post_chat("Expert", result)
        self.state = "intro"
        self.post_chat("Expert", "Type yes for another analysis or reset to clear chat.")

    def generate_from_panel(self):
        trend = self.panel_vars["Trend"].get().lower()
        news = self.panel_vars["News"].get().lower()
        risk = self.panel_vars["Risk"].get().lower()
        result = expert_system(trend, news, risk)

        self.panel_output.configure(state="normal")
        self.panel_output.delete("1.0", "end")
        self.panel_output.insert("end", result)
        self.panel_output.configure(state="disabled")


if __name__ == "__main__":
    App().mainloop()