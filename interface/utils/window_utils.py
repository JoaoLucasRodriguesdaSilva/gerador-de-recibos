import tkinter as tk


def center_window(popup: tk.Toplevel, parent: tk.Widget) -> None:
    """Centraliza o popup na janela pai."""
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    if width <= 1:
        width = popup.winfo_reqwidth()
    if height <= 1:
        height = popup.winfo_reqheight()

    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    x = parent_x + (parent_width // 2) - (width // 2)
    y = parent_y + (parent_height // 2) - (height // 2)

    popup.geometry(f"+{x}+{y}")
