import tkinter as tk
from tkinter import font, filedialog

class Conversation:
    def __init__(self, agent):
        self.agent = agent
        self.name = self.agent.__class__.__name__
        if self.name == "ChatGPT":
            self.go_back = self.agent.kanu.config_chatgpt
        elif self.name == "FuncGPT":
            self.go_back = self.agent.kanu.config_funcgpt
        else:
            self.go_back = self.agent.run

    def page(self):
        self.agent.previous = self.agent.kanu.container
        self.agent.kanu.container.pack_forget()
        self.agent.kanu.container = tk.Frame(self.agent.kanu.root)
        self.agent.kanu.container.pack(fill="both", expand=True)
        self.agent.kanu.container.bind_all("<Return>", lambda event: self.agent.send_message())
        self.agent.kanu.container.focus_set()
        l = tk.Label(self.agent.kanu.container, text=self.name)
        l.grid(row=0, column=0, sticky="ew")
        self.agent.system = tk.Text(self.agent.kanu.container, height=7)
        self.agent.system.tag_configure("system", **self.agent.settings.get_system_kwargs())
        if self.name == "DocGPT":
            if self.agent.existing:
                self.agent.system.insert(tk.END, "System: Using existing database. Embedding was skipped and no tokens were used.\n", "system")
            else:
                self.agent.system.insert(tk.END, f"System: Creating new database. Embedding used {self.agent.tokens:,} tokens or ${self.agent.price:.6f}.\n", "system")
        self.agent.system.insert(tk.END, f"System: A new chat session has been created using {self.agent.model}.\n", "system")
        self.agent.system.grid(row=1, column=0, sticky="ew")
        self.agent.session = tk.Text(self.agent.kanu.container)
        self.agent.session.grid(row=2, column=0, sticky="nsew")
        self.agent.session.tag_config("user", **self.agent.settings.get_user_kwargs())
        self.agent.session.tag_config("bot", **self.agent.settings.get_bot_kwargs())
        self.agent.user_input = tk.StringVar()
        self.agent.chatbox = tk.Entry(self.agent.kanu.container, textvariable=self.agent.user_input)
        self.agent.chatbox.grid(row=3, column=0, sticky="ew")
        self.agent.messages = []
        button_frame = tk.Frame(self.agent.kanu.container)
        button_frame.grid(row=4, column=0, sticky="ew")
        b = tk.Button(button_frame, text="Send", command=lambda: self.agent.send_message())
        b.grid(row=0, column=0, sticky="ew")
        b = tk.Button(button_frame, text="Clear", command=lambda: self.agent.clear_session())
        b.grid(row=0, column=1, sticky="ew")
        b = tk.Button(button_frame, text="Go back", command=lambda: self.go_back())
        b.grid(row=0, column=2, sticky="ew")
        b = tk.Button(button_frame, text="Settings", command=lambda: self.agent.settings.page())
        b.grid(row=0, column=3, sticky="ew")
        b = tk.Button(button_frame, text="Save", command=lambda: self.save())
        b.grid(row=0, column=4, sticky="ew")
        self.agent.kanu.container.grid_columnconfigure(0, weight=1)
        self.agent.kanu.container.grid_rowconfigure(2, weight=1)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)

    def save(self):
        file_path = filedialog.asksaveasfilename()
        if not file_path:
            return
        data = "[System]\n"
        data += self.agent.system.get("1.0", tk.END).rstrip()
        data += "\n\n[Session]\n"
        data += self.agent.session.get("1.0", tk.END).rstrip()
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(data)

class Settings:
    def __init__(self, agent):
        self.agent = agent
        self.default_font = font.nametofont("TkDefaultFont").actual()
        self.default_user_background_color = "gray85"
        self.default_user_foreground_color = "black"
        self.default_user_font_family = self.default_font["family"]
        self.default_user_font_size = self.default_font["size"]
        self.default_bot_background_color = "white"
        self.default_bot_foreground_color = "black"
        self.default_bot_font_family = self.default_font["family"]
        self.default_bot_font_size = self.default_font["size"]
        self.default_system_background_color = "white"
        self.default_system_foreground_color = "black"
        self.default_system_font_family = self.default_font["family"]
        self.default_system_font_size = self.default_font["size"]
        self.user_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_background_color)
        self.user_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_foreground_color)
        self.user_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_user_font_family)
        self.user_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_user_font_size)
        self.bot_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_background_color)
        self.bot_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_foreground_color)
        self.bot_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_bot_font_family)
        self.bot_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_bot_font_size)
        self.system_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_system_background_color)
        self.system_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_system_foreground_color)
        self.system_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_system_font_family)
        self.system_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_system_font_size)

    def get_user_kwargs(self):
        return dict(
            background=self.user_background_color.get(),
            foreground=self.user_foreground_color.get(),
            font=(self.user_font_family.get(), self.user_font_size.get())
        )
            
    def get_bot_kwargs(self):
        return dict(
            background=self.bot_background_color.get(),
            foreground=self.bot_foreground_color.get(),
            font=(self.bot_font_family.get(), self.bot_font_size.get())
        )

    def get_system_kwargs(self):
        return dict(
            background=self.system_background_color.get(),
            foreground=self.system_foreground_color.get(),
            font=(self.system_font_family.get(), self.system_font_size.get())
        )

    def page(self):
        self.agent.previous = self.agent.kanu.container
        self.agent.kanu.container.pack_forget()
        self.agent.kanu.container = tk.Frame(self.agent.kanu.root)
        self.agent.kanu.container.pack()
        l = tk.Label(self.agent.kanu.container, text=self.agent.__class__.__name__)
        l.grid(row=0, column=0, columnspan=3)
        l = tk.Label(self.agent.kanu.container, text="User background color")
        l.grid(row=1, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.user_background_color)
        e.grid(row=1, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="User foreground color")
        l.grid(row=2, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.user_foreground_color)
        e.grid(row=2, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="User font family")
        l.grid(row=3, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.user_font_family)
        e.grid(row=3, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="User font size")
        l.grid(row=4, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.user_font_size)
        e.grid(row=4, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="Bot background color")
        l.grid(row=5, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.bot_background_color)
        e.grid(row=5, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="Bot foreground color")
        l.grid(row=6, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.bot_foreground_color)
        e.grid(row=6, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="Bot font family")
        l.grid(row=7, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.bot_font_family)
        e.grid(row=7, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="Bot font size")
        l.grid(row=8, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.bot_font_size)
        e.grid(row=8, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="System background color")
        l.grid(row=9, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.system_background_color)
        e.grid(row=9, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="System foreground color")
        l.grid(row=10, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.system_foreground_color)
        e.grid(row=10, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="System font family")
        l.grid(row=11, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.system_font_family)
        e.grid(row=11, column=1, columnspan=2)
        l = tk.Label(self.agent.kanu.container, text="System font size")
        l.grid(row=12, column=0)
        e = tk.Entry(self.agent.kanu.container, textvariable=self.system_font_size)
        e.grid(row=12, column=1, columnspan=2)
        b = tk.Button(self.agent.kanu.container, text="Apply", command=lambda: self.apply())
        b.grid(row=13, column=0)
        b = tk.Button(self.agent.kanu.container, text="Reset", command=lambda: self.reset())
        b.grid(row=13, column=1)
        b = tk.Button(self.agent.kanu.container, text="Go back", command=lambda: self.go_back())
        b.grid(row=13, column=2)

    def go_back(self):
        self.agent.kanu.container.pack_forget()
        self.agent.kanu.container = self.agent.previous
        self.agent.kanu.container.pack(fill="both", expand=True)

    def apply(self):
        self.agent.session.tag_config("user", **self.get_user_kwargs())
        self.agent.session.tag_config("bot", **self.get_bot_kwargs())
        self.agent.system.tag_config("system", **self.get_system_kwargs())
        self.agent.kanu.container.pack_forget()
        self.agent.kanu.container = self.agent.previous
        self.agent.kanu.container.pack(fill="both", expand=True)

    def reset(self):
        self.user_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_background_color)
        self.user_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_foreground_color)
        self.user_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_user_font_family)
        self.user_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_user_font_size)
        self.bot_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_background_color)
        self.bot_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_foreground_color)
        self.bot_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_bot_font_family)
        self.bot_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_bot_font_size)
        self.system_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_system_background_color)
        self.system_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_system_foreground_color)
        self.system_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_system_font_family)
        self.system_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_system_font_size)
        self.apply()

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        l = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, wraplength=400)
        l.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None