# Knowledge Screen

**Turn a spare monitor into a continuously rotating visual knowledge
display.**

Knowledge Screen is a lightweight Python application that displays
educational, technical, reference, or other images from a directory as a
full-screen slideshow. It is designed for multi-monitor setups: by
default it prefers a portrait monitor and falls back to the primary
monitor when no portrait display is available.

The project supports Windows and Linux. Runtime behavior is configured
through `settings.ini`, keeping normal user settings separate from
Python application logic.

------------------------------------------------------------------------

## Why Knowledge Screen?

Knowledge Screen started with a simple use case: keep Python learning
material, Kubernetes architecture diagrams, cloud references, cheat
sheets, and other useful visual content rotating on a spare monitor.

Instead of maintaining a presentation, Knowledge Screen discovers images
directly from a directory and displays them one at a time. The content
directory itself becomes the slideshow source.

## Current Features

-   Full-screen, borderless image display
-   PNG, JPG, and JPEG support
-   Multi-monitor detection
-   Portrait-monitor preference
-   Primary-monitor fallback
-   Manual monitor selection by index
-   Windows and Linux support
-   Configurable image-change interval
-   Recursive directory scanning
-   Optional shuffle
-   Aspect-ratio-preserving scaling
-   EXIF orientation handling
-   Configurable background color
-   Optional filename display
-   Optional hidden mouse cursor
-   Keyboard navigation
-   Pause/resume
-   INI-based configuration

------------------------------------------------------------------------

## Project Structure

``` text
knowledge-screen/
├── .gitignore
├── LICENSE
├── README.md
├── architecture_diagram.png
├── knowledge_screen.py
├── requirements.txt
└── settings.ini
```

### `knowledge_screen.py`

The main application. It reads configuration, discovers images, detects
monitors, selects the target display, creates the Tkinter window,
loads/resizes images, schedules transitions, and handles keyboard input.

### `settings.ini`

The application's configuration file. Settings are organized into
logical sections:

-   `[slideshow]` --- image source and slideshow behavior
-   `[display]` --- monitor and presentation behavior

The filename and section names are independent. `settings.ini` is the
file; `[slideshow]` and `[display]` are groups of related settings
inside it.

### `requirements.txt`

Third-party Python dependencies:

``` text
Pillow
screeninfo
```

### `.gitignore`

Local/generated content should not be committed. The virtual environment
should be ignored with:

``` gitignore
.venv/
```

### `architecture_diagram.png`

A visual explanation of the repository, configuration, program flow,
monitor selection, slideshow loop, and fresh-clone setup. It is embedded
at the end of this README.

### `LICENSE`

The project is released under the MIT License.

------------------------------------------------------------------------

# Installation

## 1. Clone the Repository

``` bash
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen
```

## 2. Verify Python

``` bash
python --version
```

On systems where Python 3 is exposed as `python3`:

``` bash
python3 --version
```

## 3. Create a Virtual Environment

A dedicated virtual environment keeps this project's packages isolated.

### Windows

``` powershell
python -m venv .venv
```

### Linux

``` bash
python3 -m venv .venv
```

## 4. Activate the Virtual Environment

### Windows PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

Verify:

``` powershell
where.exe python
```

The first result should point inside `.venv\Scripts`.

### Windows Command Prompt

``` cmd
.venv\Scripts\activate.bat
```

### Linux

``` bash
source .venv/bin/activate
```

Verify:

``` bash
which python
```

## 5. Upgrade pip

``` bash
python -m pip install --upgrade pip
```

## 6. Install Dependencies

``` bash
python -m pip install -r requirements.txt
```

### Linux Tkinter Note

Some Linux distributions package Tkinter separately. On Ubuntu/Debian:

``` bash
sudo apt install python3-tk
```

------------------------------------------------------------------------

# Configuration

Edit `settings.ini` before starting Knowledge Screen.

``` ini
[slideshow]
image_folder = D:\Learning\TechImages
image_change_seconds = 120
recursive = true
shuffle = false
background_color = black

[display]
monitor_mode = prefer_portrait
monitor_index = 0
hide_mouse_cursor = true
show_filename = false
filename_font_size = 18
```

Linux example:

``` ini
image_folder = /home/user/Pictures/TechLearning
```

## How the INI File Is Organized

``` text
settings.ini
│
├── [slideshow]
│   ├── image_folder
│   ├── image_change_seconds
│   ├── recursive
│   ├── shuffle
│   └── background_color
│
└── [display]
    ├── monitor_mode
    ├── monitor_index
    ├── hide_mouse_cursor
    ├── show_filename
    └── filename_font_size
```

Python's `configparser` reads the file and then retrieves values by
section and key, for example:

``` python
parser.get("slideshow", "image_folder")
parser.getint("slideshow", "image_change_seconds")
parser.getboolean("display", "hide_mouse_cursor")
```

------------------------------------------------------------------------

# Configuration Reference

## `[slideshow]`

### `image_folder`

Directory containing images:

``` ini
image_folder = D:\Learning\TechImages
```

### `image_change_seconds`

Time each image remains visible:

``` ini
image_change_seconds = 120
```

    Value Duration
  ------- ------------
     `30` 30 seconds
     `60` 1 minute
    `120` 2 minutes
    `300` 5 minutes

### `recursive`

Search subdirectories:

``` ini
recursive = true
```

This allows organization such as:

``` text
TechLearning/
├── Python/
├── Kubernetes/
├── AWS/
├── Terraform/
└── Linux/
```

### `shuffle`

Start with shuffled image order:

``` ini
shuffle = false
```

Shuffle can also be toggled at runtime with `S`.

### `background_color`

Background shown when an image does not fill the display:

``` ini
background_color = black
```

## `[display]`

### `monitor_mode`

Supported values:

``` ini
monitor_mode = prefer_portrait
```

``` ini
monitor_mode = primary
```

``` ini
monitor_mode = index
```

### `prefer_portrait`

The recommended default. Selection works conceptually as follows:

``` text
Detect monitors
      |
      v
Portrait monitor available?
      |
   +--+--+
  Yes    No
   |      |
   v      v
Portrait  Primary monitor
monitor       |
              v
       If unavailable,
       first monitor
```

A portrait monitor is identified when:

``` python
monitor.height > monitor.width
```

### `primary`

Always select the primary monitor:

``` ini
monitor_mode = primary
```

### `index`

Select a specific detected monitor:

``` ini
monitor_mode = index
monitor_index = 1
```

Indexes start at `0`. Knowledge Screen prints monitor information at
startup to help identify the correct index.

### `hide_mouse_cursor`

``` ini
hide_mouse_cursor = true
```

### `show_filename`

``` ini
show_filename = false
```

Press `F` while running to toggle the filename.

### `filename_font_size`

``` ini
filename_font_size = 18
```

------------------------------------------------------------------------

# Running Knowledge Screen

Activate `.venv`, then run:

``` bash
python knowledge_screen.py
```

The application then:

1.  Reads `settings.ini`.
2.  Parses and validates settings.
3.  Scans the configured image directory.
4.  Filters supported images.
5.  Detects connected monitors.
6.  Selects the target display.
7.  Creates a borderless window.
8.  Loads and displays the current image.
9.  Schedules the next image.

------------------------------------------------------------------------

# Keyboard Controls

  Key             Action
  --------------- ----------------------
  `Right Arrow`   Next image
  `Space`         Next image
  `Left Arrow`    Previous image
  `P`             Pause / resume
  `S`             Toggle shuffle
  `F`             Show / hide filename
  `Esc`           Exit

------------------------------------------------------------------------

# How Image Display Works

Knowledge Screen preserves image aspect ratio rather than stretching
content to match the monitor.

Pillow performs high-quality resizing with LANCZOS:

``` python
image.thumbnail(
    (monitor_width, monitor_height),
    Image.Resampling.LANCZOS,
)
```

EXIF orientation metadata is honored with `ImageOps.exif_transpose()`.
Images that do not fill the entire monitor are centered against the
configured background.

------------------------------------------------------------------------

# How the Python Components Work

## `configparser`

Reads and parses `settings.ini`:

``` python
import configparser
```

It provides typed access through methods such as `get()`, `getint()`,
and `getboolean()`.

> **Code defines how the program works; configuration defines how a
> particular installation should behave.**

## `pathlib`

Provides portable filesystem handling:

``` python
from pathlib import Path
```

It is used for locating configuration, scanning directories, checking
paths, and examining extensions.

## Pillow

``` python
from PIL import Image, ImageOps, ImageTk
```

Handles image loading, EXIF orientation, resizing, aspect-ratio
preservation, and conversion for Tkinter.

## `screeninfo`

``` python
from screeninfo import get_monitors
```

Provides connected-monitor dimensions, coordinates, and primary-monitor
information.

## Tkinter

Provides the graphical window and event loop. It displays images,
receives keyboard events, and schedules timed image changes.

## `random`

Provides runtime image-list shuffling.

------------------------------------------------------------------------

# Application Classes

## `SlideshowConfig`

Responsible for reading configuration, retrieving `[slideshow]` and
`[display]` values, applying fallback values, and validating settings.

## `ImageSlideshow`

Responsible for image discovery, monitor selection, window setup,
rendering, timers, navigation, pause/resume, shuffle, filename display,
keyboard handling, and cleanup.

------------------------------------------------------------------------

# Supported Image Formats

``` text
.png
.jpg
.jpeg
```

Extension matching is case-insensitive.

------------------------------------------------------------------------

# Typical Fresh-Clone Workflow

## Windows PowerShell

``` powershell
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Edit `settings.ini` and set:

``` ini
image_folder = C:\path\to\your\images
```

Run:

``` powershell
python knowledge_screen.py
```

Exit with `Esc`, then deactivate:

``` powershell
deactivate
```

## Linux

``` bash
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Edit:

``` ini
image_folder = /path/to/your/images
```

Run:

``` bash
python knowledge_screen.py
```

When finished:

``` bash
deactivate
```

------------------------------------------------------------------------

# Development Setup

A simple development cycle:

``` text
Clone repository
      |
      v
Create .venv
      |
      v
Activate .venv
      |
      v
Install requirements
      |
      v
Modify code
      |
      v
Run and test
      |
      v
Commit changes
```

Do not commit `.venv/`. Project dependencies belong in
`requirements.txt`.

------------------------------------------------------------------------

# Roadmap

Potential future capabilities include:

-   GIF and WebP support
-   PDF page display
-   directory watching
-   automatic discovery of newly added content
-   categories and playlists
-   scheduled/time-based content
-   Raspberry Pi and kiosk mode
-   structured logging
-   automated tests and coverage
-   GitHub Actions CI/CD
-   application packaging / standalone executable builds

``` text
Knowledge Screen
│
├── Images
│   ├── PNG / JPG / JPEG
│   ├── GIF
│   └── WebP
│
├── Documents
│   └── PDF
│
├── Content Organization
│   ├── Categories
│   ├── Playlists
│   └── Directory watching
│
├── Display
│   ├── Portrait preference
│   ├── Multi-monitor
│   ├── Fullscreen / kiosk
│   └── Raspberry Pi
│
└── Automation
    ├── Scheduled playlists
    ├── Time-based content
    └── Automatic refresh
```

------------------------------------------------------------------------

# Troubleshooting

## Configuration file not found

Verify that `settings.ini` exists in the same directory as
`knowledge_screen.py`.

## No images found

Verify `image_folder` in `settings.ini` and confirm that the directory
contains `.png`, `.jpg`, or `.jpeg` files. For subdirectories:

``` ini
recursive = true
```

## Wrong monitor selected

Inspect the monitor information printed at startup. To force a monitor:

``` ini
monitor_mode = index
monitor_index = 1
```

## PowerShell blocks virtual-environment activation

If local execution policy prevents `Activate.ps1`, review the applicable
security policy. Command Prompt activation is an alternative:

``` cmd
.venv\Scripts\activate.bat
```

## Tkinter missing on Linux

Ubuntu/Debian:

``` bash
sudo apt install python3-tk
```

------------------------------------------------------------------------

# Contributing

Contributions, bug reports, testing feedback, and feature ideas are
welcome.

1.  Fork or clone the repository.
2.  Create a focused branch.
3.  Create and activate `.venv`.
4.  Install dependencies.
5.  Make and test the change.
6.  Update documentation when behavior changes.
7.  Open a pull request describing the change.

------------------------------------------------------------------------

# License

Knowledge Screen is open-source software released under the [MIT
License](LICENSE).

------------------------------------------------------------------------

# Architecture Diagram

The diagram below summarizes the repository structure, configuration,
Python components, monitor selection, application flow, slideshow loop,
and fresh-clone workflow.

[![Knowledge Screen - How It
Works](architecture_diagram.png)](architecture_diagram.png)

------------------------------------------------------------------------

## Project Philosophy

> **Useful knowledge should not have to stay buried in folders. Put it
> on a screen where you can see it.**
