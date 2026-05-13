import tkinter as tk
from tkinter import scrolledtext


FAQ = {
    "courses": "We offer B.Tech, BCA, BBA, B.Com, and M.Tech programs.",
    "fees": "B.Tech fee is about Rs 1,20,000 per year. Other courses vary by department.",
    "deadline": "Admission form deadline is 30 June 2026.",
    "documents": "Required: 10th and 12th marksheets, ID proof, photos, transfer certificate.",
    "eligibility": "For UG programs, minimum 50% in 12th is required.",
    "scholarship": "Scholarships are available based on merit, category, and entrance score.",
    "hostel": "Hostel is available for boys and girls with mess and Wi-Fi facilities.",
    "contact": "Call 1800-123-456 or email admissions@college.edu.",
}


def bot_reply(message):
    text = message.lower()
    if any(word in text for word in ("hi", "hello", "hey")):
        return "Hello. How can I help with your admission today?"
    if "apply" in text or "application" in text:
        return "You can apply online from the admissions portal and submit scanned documents."
    for key, answer in FAQ.items():
        if key in text:
            return answer
    return "Please ask about courses, fees, eligibility, documents, deadline, scholarship, hostel, or contact."


def create_app():
    root = tk.Tk()
    root.title("College Admission Desk")
    root.geometry("540x640")
    root.minsize(420, 520)
    root.configure(bg="#f5f7fb")

    tk.Label(root, text="College Admission Desk", bg="#0f172a", fg="#e2e8f0",
             font=("Segoe UI", 16, "bold"), pady=14).pack(fill="x")

    chat = scrolledtext.ScrolledText(root, state="disabled", wrap="word", relief="flat",
                                     bg="#ffffff", fg="#0f172a", padx=12, pady=12,
                                     font=("Segoe UI", 11))
    chat.pack(fill="both", expand=True, padx=14, pady=12)
    chat.tag_config("user", foreground="#1d4ed8", font=("Segoe UI", 11, "bold"))
    chat.tag_config("bot", foreground="#0f172a")

    box = tk.Frame(root, bg="#f5f7fb")
    box.pack(fill="x", padx=14, pady=(0, 14))
    entry = tk.Entry(box, font=("Segoe UI", 11), bd=0, relief="flat", bg="#ffffff")
    entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))

    def post(role, text, tag):
        chat.configure(state="normal")
        chat.insert("end", f"{role}: {text}\n\n", tag)
        chat.configure(state="disabled")
        chat.yview("end")

    def send():
        message = entry.get().strip()
        if not message:
            return
        entry.delete(0, "end")
        post("You", message, "user")
        post("Desk Bot", bot_reply(message), "bot")

    entry.bind("<Return>", lambda _: send())
    tk.Button(box, text="Send", command=send, bg="#1d4ed8", fg="white", bd=0,
              activebackground="#1e40af", activeforeground="white",
              font=("Segoe UI", 10, "bold"), padx=14, pady=8).pack(side="right")

    post(
        "Desk Bot",
        "Welcome to College Admission Desk. Ask me about courses, fees, eligibility, "
        "documents, deadline, scholarship, hostel, or contact.",
        "bot",
    )
    return root


if __name__ == "__main__":
    create_app().mainloop()
