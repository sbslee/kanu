import tkinter as tk
from tkinter import font

# https://openai.com/pricing#language-models
def tokens2price(tokens, model, task):
    if model == "gpt-3.5-turbo":
        if task in ["prompt", "completion"]:
            return 0.002 / 1000 * tokens
        else:
            raise ValueError(f"Invalid task for {model}: {task}")
    elif model == "text-embedding-ada-002":
        if task == "embedding":
            return 0.0004 / 1000 * tokens
        else:
            raise ValueError(f"Invalid task for {model}: {task}")
    elif model == "gpt-4":
        if task == "completion":
            return 0.06 / 1000 * tokens
        elif task == "prompt":
            return 0.03 / 1000 * tokens
        else:
            raise ValueError(f"Invalid task for {model}: {task}")
    else:
        raise ValueError(f"Invalid model: {model}")

def text2tokens(model, text):
    import tiktoken
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

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
        self.agent.kanu.container.pack()

    def apply(self):
        self.agent.session.tag_config("user", **self.get_user_kwargs())
        self.agent.session.tag_config("bot", **self.get_bot_kwargs())
        self.agent.system.tag_config("system", **self.get_system_kwargs())
        self.agent.kanu.container.pack_forget()
        self.agent.kanu.container = self.agent.previous
        self.agent.kanu.container.pack()

    def reset(self):
        self.user_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_background_color)
        self.user_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_user_foreground_color)
        self.user_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_user_font_family)
        self.user_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_user_font_size)
        self.bot_background_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_background_color)
        self.bot_foreground_color = tk.StringVar(self.agent.kanu.container, value=self.default_bot_foreground_color)
        self.bot_font_family = tk.StringVar(self.agent.kanu.container, value=self.default_bot_font_family)
        self.bot_font_size = tk.IntVar(self.agent.kanu.container, value=self.default_bot_font_size)
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