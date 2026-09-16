import tkinter as tk


class KeyboardLegend:
    """Bottom-left keyboard shortcut legend for Knowledge Screen."""

    LEGEND_TEXT = (
        "Keyboard controls:\n"
        "Right Arrow / Space : Next image\n"
        "Left Arrow          : Previous image\n"
        "P                   : Pause / Resume\n"
        "S                   : Toggle shuffle\n"
        "F                   : Show / hide filename\n"
        "Esc                 : Exit"
    )

    def __init__(
        self,
        parent,
        background_color="black",
        text_color="lightgray",
        font_size=12,
        enabled=True,
    ):
        self.enabled = enabled

        self.label = tk.Label(
            parent,
            text=self.LEGEND_TEXT,
            bg=background_color,
            fg=text_color,
            font=("Courier New", font_size),
            justify="left",
            anchor="sw",
        )

        if self.enabled:
            self.label.place(
                relx=0.01,
                rely=0.99,
                anchor="sw",
            )