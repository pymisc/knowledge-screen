import tkinter as tk


class CountdownTimer:
    """Bottom-center countdown timer for Knowledge Screen."""

    def __init__(
        self,
        parent,
        duration_seconds,
        background_color="black",
        text_color="lightgray",
        font_size=18,
        enabled=True,
    ):
        self.parent = parent
        self.duration_seconds = duration_seconds
        self.enabled = enabled

        self.seconds_remaining = duration_seconds
        self.countdown_id = None
        self.paused = False

        self.label = tk.Label(
            parent,
            bg=background_color,
            fg=text_color,
            font=("Arial", font_size),
            anchor="center",
        )

        if self.enabled:
            self.label.place(
                relx=0.99,
                rely=0.99,
                anchor="se",
            )

    def start(self):
        """Start or reset the countdown."""
        if not self.enabled:
            return

        self.cancel()
        self.paused = False
        self.seconds_remaining = self.duration_seconds
        self._update()

    def _update(self):
        """Update the displayed countdown once per second."""
        if not self.enabled or self.paused:
            return

        self.label.config(text=str(self.seconds_remaining))

        if self.seconds_remaining > 0:
            self.seconds_remaining -= 1
            self.countdown_id = self.parent.after(
                1000,
                self._update,
            )

    def pause(self):
        """Pause the countdown at its current value."""
        if not self.enabled:
            return

        self.paused = True
        self.cancel()

    def resume(self):
        """Resume the countdown from its current value."""
        if not self.enabled or not self.paused:
            return

        self.paused = False
        self._update()

    def reset(self):
        """Reset the countdown to the configured duration."""
        if not self.enabled:
            return

        self.cancel()
        self.seconds_remaining = self.duration_seconds
        self.label.config(text=str(self.seconds_remaining))

    def cancel(self):
        """Cancel the scheduled countdown callback."""
        if self.countdown_id is not None:
            self.parent.after_cancel(self.countdown_id)
            self.countdown_id = None

    def stop(self):
        """Stop the countdown and clean up."""
        self.cancel()