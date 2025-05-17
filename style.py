from tkinter import ttk
from tkinter.font import Font
from typing import Literal

FontWeight = Literal["normal", "bold", "italic"]
FontSize = Literal["small", "medium", "large", "xlarge"]
# Font Definitions
FONTS = {
    "small": ("Helvetica", 14, "normal"),
    "medium": ("Helvetica", 16, "normal"),
    "large": ("Helvetica", 18, "normal"),
    "xlarge": ("Helvetica", 24, "bold"),
}
BUTTON = {
    "font": FONTS["large"],
    "width": 15,
    "height": 2,
    "borderwidth": 2,
    "relief": "groove",
    "padx": 10,
    "pady": 5
}
# Theme Base Class
class ColorTheme:
    def __init__(self):
        self.primary = "#3498db"
        self.secondary = "#2ecc71"
        self.danger = "#e74c3c"
        self.background = "#34495e"
        self.surface = "#ecf0f1"
        self.text = "#2c3e50"
        self.text_inverse = "#ecf0f1"
        self.correct = "#90EE90"
        self.incorrect = "#FFCCCB"

        self.button = {
            "bg": self.primary,
            "active": "#2980b9",
            "fg": self.text_inverse
        }
        self.start_button = {
            "bg": self.secondary,
            "active": "#27ae60",
            "fg": self.text_inverse
        }
        self.exit_button = {
            "bg": self.danger,
            "active": "#c0392b",
            "fg": self.text_inverse
        }
        self.radio = {
            "select": self.text,
            "active": self.primary
        }
        self.question_bg = self.background
        self.button_bg = self.button["bg"]
        self.button_active = self.button["active"]
        self.highlight_bg = "#fff8dc"
# Dark Theme Variant
class DarkTheme(ColorTheme):
    def __init__(self):
        super().__init__()
        self.background = "#2c3e50"
        self.surface = "#34495e"
        self.text = "#ecf0f1"
        self.text_inverse = "#2c3e50"
        self.highlight_bg = "#556b2f"
# Light Theme Variant
class LightTheme(ColorTheme):
    def __init__(self):
        super().__init__()
        self.background = "#ecf0f1"
        self.surface = "#ffffff"
        self.text = "#2c3e50"
        self.text_inverse = "#ecf0f1"
        self.button["fg"] = self.text_inverse
        self.start_button["fg"] = self.text_inverse
        self.exit_button["fg"] = self.text_inverse
        self.highlight_bg = "#fffacd"
COLOR_THEME = ColorTheme()

DIMENSIONS = {
    "border_radius": 8,
    "padding_small": 5,
    "padding_medium": 10,
    "padding_large": 20,
    "button_width": 15,
    "button_height": 2,
    "input_width": 25
}
ANIMATION = {
    "duration_ms": 200,
    "hover_scale": 1.05
}
COMPONENT_STYLES = {
    "question": {
        "bg": COLOR_THEME.surface,
        "fg": COLOR_THEME.text,
        "font": FONTS["xlarge"],
        "padding": DIMENSIONS["padding_large"],
        "wraplength": 600
    },
    "answer": {
        "bg": COLOR_THEME.surface,
        "fg": COLOR_THEME.text,
        "font": FONTS["large"],
        "anchor": "w",
        "wraplength": 550
    },
    "header": {
        "bg": COLOR_THEME.background,
        "fg": COLOR_THEME.text_inverse,
        "font": ("Helvetica", 24, "bold"),
        "padding": (0, 0, 20, 0)
    },
    "footer": {
        "bg": COLOR_THEME.background,
        "fg": COLOR_THEME.text_inverse,
        "font": FONTS["small"],
        "padding": (20, 0, 0, 0)
    },
    "selected_answer": {
        "bg": "#d0f0c0",
        "fg": "#000000",
        "font": FONTS["medium"],
        "anchor": "w",
        "wraplength": 700
    }
}
def configure_styles(root) -> None:
    style = ttk.Style(root)
    style.theme_use('clam')
    
    root.option_add("*TLabel.Font", FONTS["medium"])
    root.option_add("*TButton.Font", FONTS["large"])
    root.option_add("*TRadiobutton.Font", FONTS["large"])
    root.option_add("*Font", FONTS["medium"])
    
    style.configure('.', background=COLOR_THEME.background, foreground=COLOR_THEME.text)
    style.configure('Card.TFrame',
                    background=COLOR_THEME.surface,
                    borderwidth=2,
                    relief="solid")
    style.configure('TButton',
                    padding=(BUTTON["padx"], BUTTON["pady"]),
                    borderwidth=BUTTON["borderwidth"],
                    relief=BUTTON["relief"],
                    background=COLOR_THEME.button["bg"],
                    foreground=COLOR_THEME.button["fg"])
    style.configure('Primary.TButton',
                    background=COLOR_THEME.button["bg"],
                    foreground=COLOR_THEME.button["fg"])
    style.configure('Start.TButton',
                    background=COLOR_THEME.start_button["bg"],
                    foreground=COLOR_THEME.start_button["fg"])
    style.configure('Exit.TButton',
                    background=COLOR_THEME.exit_button["bg"],
                    foreground=COLOR_THEME.exit_button["fg"])
    
    # Ensure font size for Question is applied
    style.configure('Question.TLabel',
                    background=COLOR_THEME.surface,
                    foreground=COLOR_THEME.text,
                    font=("Helvetica", 24, "bold"),  # Hardcoded font size and style for question
                    padding=DIMENSIONS["padding_large"],
                    wraplength=600)

    style.configure('Answer.TRadiobutton',
                    background=COLOR_THEME.surface,
                    foreground=COLOR_THEME.text,
                    font=("Helvetica", 16, "normal"),  # Hardcoded font size for answers
                    anchor="w",
                    wraplength=550)

    # Apply selected answer style
    style.configure('SelectedAnswer.TRadiobutton',
                    background=COMPONENT_STYLES["selected_answer"]["bg"],
                    foreground=COMPONENT_STYLES["selected_answer"]["fg"],
                    font=COMPONENT_STYLES["selected_answer"]["font"],
                    anchor=COMPONENT_STYLES["selected_answer"]["anchor"],
                    wraplength=COMPONENT_STYLES["selected_answer"]["wraplength"])

    # Header and footer styles
    style.configure('Header.TLabel',
                    background=COMPONENT_STYLES["header"]["bg"],
                    foreground=COMPONENT_STYLES["header"]["fg"],
                    font=COMPONENT_STYLES["header"]["font"],
                    padding=COMPONENT_STYLES["header"]["padding"])
    
    style.configure('Footer.TLabel',
                    background=COMPONENT_STYLES["footer"]["bg"],
                    foreground=COMPONENT_STYLES["footer"]["fg"],
                    font=COMPONENT_STYLES["footer"]["font"],
                    padding=COMPONENT_STYLES["footer"]["padding"])

    # Custom styles for warning and highlighted frames
    style.configure('Warning.TFrame',
                    background="#ffcccc")
    style.configure('Highlighted.TFrame',
                    background=COLOR_THEME.highlight_bg,
                    borderwidth=2,
                    relief="solid")
