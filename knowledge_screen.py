import configparser
import random
import sys
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageOps, ImageTk
from screeninfo import get_monitors

from countdown_timer import CountdownTimer


APP_NAME = "Python Image Slideshow"
CONFIG_FILE = "settings.ini"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


class SlideshowConfig:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.parser = configparser.ConfigParser()

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        self.parser.read(config_path, encoding="utf-8")

        self.image_folder = Path(
            self.parser.get("slideshow", "image_folder")
        ).expanduser()

        self.image_change_seconds = self.parser.getint(
            "slideshow", "image_change_seconds", fallback=60
        )

        self.recursive = self.parser.getboolean(
            "slideshow", "recursive", fallback=True
        )

        self.shuffle = self.parser.getboolean(
            "slideshow", "shuffle", fallback=False
        )

        self.background_color = self.parser.get(
            "slideshow", "background_color", fallback="black"
        )

        self.monitor_mode = self.parser.get(
            "display", "monitor_mode", fallback="prefer_portrait"
        ).strip().lower()

        self.monitor_index = self.parser.getint(
            "display", "monitor_index", fallback=0
        )

        self.hide_mouse_cursor = self.parser.getboolean(
            "display", "hide_mouse_cursor", fallback=True
        )

        self.show_filename = self.parser.getboolean(
            "display", "show_filename", fallback=False
        )

        self.filename_font_size = self.parser.getint(
            "display", "filename_font_size", fallback=18
        )

        self.validate()

    def validate(self):
        if self.image_change_seconds <= 0:
            raise ValueError(
                "image_change_seconds must be greater than 0"
            )

        valid_modes = {
            "prefer_portrait",
            "primary",
            "index",
        }

        if self.monitor_mode not in valid_modes:
            raise ValueError(
                "monitor_mode must be one of: "
                "prefer_portrait, primary, index"
            )


class ImageSlideshow:
    def __init__(self, root: tk.Tk, config: SlideshowConfig):
        self.root = root
        self.config = config

        self.images = self.find_images()

        if not self.images:
            raise RuntimeError(
                f"No PNG/JPG/JPEG images found in: "
                f"{self.config.image_folder}"
            )

        self.original_images = list(self.images)

        if self.config.shuffle:
            random.shuffle(self.images)

        self.current_index = 0
        self.current_photo = None

        self.paused = False
        self.shuffle_enabled = self.config.shuffle
        self.timer_id = None

        self.target_monitor = self.select_target_monitor()

        self.configure_window()
        self.create_widgets()
        self.bind_keys()

        # Let the window manager apply geometry before rendering.
        self.root.after(250, self.start_slideshow)

    def find_images(self):
        folder = self.config.image_folder

        if not folder.exists():
            raise FileNotFoundError(
                f"Image folder does not exist: {folder}"
            )

        if not folder.is_dir():
            raise NotADirectoryError(
                f"Configured image_folder is not a directory: {folder}"
            )

        if self.config.recursive:
            files = [
                path
                for path in folder.rglob("*")
                if path.is_file()
                and path.suffix.lower() in SUPPORTED_EXTENSIONS
            ]
        else:
            files = [
                path
                for path in folder.iterdir()
                if path.is_file()
                and path.suffix.lower() in SUPPORTED_EXTENSIONS
            ]

        return sorted(files, key=lambda p: str(p).lower())

    def select_target_monitor(self):
        monitors = get_monitors()

        if not monitors:
            raise RuntimeError("No monitors detected.")

        print("\nDetected monitors:")
        for index, monitor in enumerate(monitors):
            orientation = (
                "Portrait"
                if monitor.height > monitor.width
                else "Landscape"
            )

            print(
                f"  [{index}] "
                f"{monitor.width}x{monitor.height} "
                f"at ({monitor.x}, {monitor.y}) "
                f"{orientation} "
                f"Primary={monitor.is_primary}"
            )

        mode = self.config.monitor_mode

        if mode == "prefer_portrait":
            portrait_monitors = [
                monitor
                for monitor in monitors
                if monitor.height > monitor.width
            ]

            if portrait_monitors:
                selected = portrait_monitors[0]
                print(
                    "\nMonitor selection: portrait monitor found."
                )
                return selected

            primary = self.get_primary_monitor(monitors)

            if primary:
                print(
                    "\nMonitor selection: no portrait monitor found; "
                    "falling back to primary monitor."
                )
                return primary

            print(
                "\nMonitor selection: no portrait or primary monitor "
                "reported; using first available monitor."
            )
            return monitors[0]

        if mode == "primary":
            primary = self.get_primary_monitor(monitors)

            if primary:
                print("\nMonitor selection: primary monitor.")
                return primary

            print(
                "\nMonitor selection: no primary monitor reported; "
                "using first available monitor."
            )
            return monitors[0]

        if mode == "index":
            index = self.config.monitor_index

            if index < 0 or index >= len(monitors):
                raise IndexError(
                    f"monitor_index={index} is invalid. "
                    f"Detected {len(monitors)} monitor(s)."
                )

            print(f"\nMonitor selection: monitor index {index}.")
            return monitors[index]

        # validate() should prevent reaching here.
        return monitors[0]

    @staticmethod
    def get_primary_monitor(monitors):
        for monitor in monitors:
            if monitor.is_primary:
                return monitor
        return None

    def configure_window(self):
        monitor = self.target_monitor

        self.root.title(APP_NAME)
        self.root.configure(bg=self.config.background_color)

        # Borderless window sized exactly to the selected monitor.
        #
        # This is used instead of relying exclusively on Tkinter's
        # "-fullscreen", because explicit monitor coordinates behave
        # more predictably in multi-monitor environments.
        self.root.overrideredirect(True)

        geometry = (
            f"{monitor.width}x{monitor.height}"
            f"{monitor.x:+d}{monitor.y:+d}"
        )

        self.root.geometry(geometry)

        # Bring the slideshow to the selected screen.
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()

        if self.config.hide_mouse_cursor:
            self.root.configure(cursor="none")

        print(
            f"\nDisplaying on: "
            f"{monitor.width}x{monitor.height} "
            f"at ({monitor.x}, {monitor.y})"
        )

    def create_widgets(self):
        self.container = tk.Frame(
            self.root,
            bg=self.config.background_color,
            borderwidth=0,
            highlightthickness=0,
        )

        self.container.pack(fill="both", expand=True)

        self.image_label = tk.Label(
            self.container,
            bg=self.config.background_color,
            borderwidth=0,
            highlightthickness=0,
        )

        self.image_label.pack(fill="both", expand=True)

        self.filename_label = tk.Label(
            self.container,
            bg=self.config.background_color,
            fg="white",
            font=("Arial", self.config.filename_font_size),
            anchor="center",
        )

        if self.config.show_filename:
            self.filename_label.place(
                relx=0.5,
                rely=0.98,
                anchor="s",
            )

    def bind_keys(self):
        self.root.bind("<Escape>", self.quit)
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<space>", self.next_image)
        self.root.bind("<Left>", self.previous_image)

        self.root.bind("p", self.toggle_pause)
        self.root.bind("P", self.toggle_pause)

        self.root.bind("s", self.toggle_shuffle)
        self.root.bind("S", self.toggle_shuffle)

        self.root.bind("f", self.toggle_filename)
        self.root.bind("F", self.toggle_filename)

    def start_slideshow(self):
        print(f"\nFound {len(self.images)} image(s).")

        print("\nKeyboard controls:")
        print("  Right Arrow / Space : Next image")
        print("  Left Arrow          : Previous image")
        print("  P                   : Pause / Resume")
        print("  S                   : Toggle shuffle")
        print("  F                   : Show / hide filename")
        print("  Esc                 : Exit")

        self.display_current_image()
        self.schedule_next_image()

    def display_current_image(self):
        image_path = self.images[self.current_index]

        try:
            with Image.open(image_path) as image:
                # Honor EXIF rotation metadata.
                image = ImageOps.exif_transpose(image)

                monitor_width = self.target_monitor.width
                monitor_height = self.target_monitor.height

                # Resize without changing aspect ratio.
                image.thumbnail(
                    (monitor_width, monitor_height),
                    Image.Resampling.LANCZOS,
                )

                # Convert after resizing and before the source image closes.
                self.current_photo = ImageTk.PhotoImage(image.copy())

            self.image_label.config(image=self.current_photo)

            if self.config.show_filename:
                self.filename_label.config(text=image_path.name)

            print(
                f"[{self.current_index + 1}/{len(self.images)}] "
                f"{image_path}"
            )

        except Exception as exc:
            print(
                f"Unable to display image: {image_path}\n"
                f"Reason: {exc}",
                file=sys.stderr,
            )

            self.advance_after_error()

    def advance_after_error(self):
        if len(self.images) <= 1:
            self.quit()
            return

        self.current_index = (
            self.current_index + 1
        ) % len(self.images)

        self.root.after(100, self.display_current_image)

    def schedule_next_image(self):
        self.cancel_timer()

        if not self.paused:
            self.timer_id = self.root.after(
                self.config.image_change_seconds * 1000,
                self.next_image,
            )

    def cancel_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def next_image(self, event=None):
        if not self.images:
            return

        self.current_index = (
            self.current_index + 1
        ) % len(self.images)

        self.display_current_image()
        self.schedule_next_image()

    def previous_image(self, event=None):
        if not self.images:
            return

        self.current_index = (
            self.current_index - 1
        ) % len(self.images)

        self.display_current_image()
        self.schedule_next_image()

    def toggle_pause(self, event=None):
        self.paused = not self.paused

        if self.paused:
            self.cancel_timer()
            print("Slideshow PAUSED")
        else:
            print("Slideshow RESUMED")
            self.schedule_next_image()

    def toggle_shuffle(self, event=None):
        current_image = self.images[self.current_index]

        self.shuffle_enabled = not self.shuffle_enabled

        if self.shuffle_enabled:
            random.shuffle(self.images)
            self.current_index = self.images.index(current_image)
            print("Shuffle ENABLED")
        else:
            self.images = list(self.original_images)
            self.current_index = self.images.index(current_image)
            print("Shuffle DISABLED")

        self.schedule_next_image()

    def toggle_filename(self, event=None):
        if self.filename_label.winfo_ismapped():
            self.filename_label.place_forget()
            print("Filename display DISABLED")
        else:
            self.filename_label.config(
                text=self.images[self.current_index].name
            )
            self.filename_label.place(
                relx=0.5,
                rely=0.98,
                anchor="s",
            )
            print("Filename display ENABLED")

    def quit(self, event=None):
        self.cancel_timer()
        self.root.destroy()


def main():
    script_directory = Path(__file__).resolve().parent
    config_path = script_directory / CONFIG_FILE

    try:
        config = SlideshowConfig(config_path)

        root = tk.Tk()
        ImageSlideshow(root, config)
        root.mainloop()

    except Exception as exc:
        print(f"\nERROR: {exc}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
