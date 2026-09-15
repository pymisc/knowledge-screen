# Knowledge Screen

**Turn a spare monitor into a continuously rotating visual knowledge
display.**

Knowledge Screen is a lightweight, cross-platform Python application
that displays a directory of educational, technical, reference, or other
images as a full-screen slideshow.

It is designed especially for multi-monitor setups. By default,
Knowledge Screen **prefers a portrait monitor** when one is available.
If no portrait monitor is detected, it automatically falls back to the
**primary monitor**.

The project currently supports Windows and Linux and uses a simple INI
configuration file so normal settings can be changed without modifying
Python code.

------------------------------------------------------------------------

## Why Knowledge Screen?

Knowledge Screen started from a simple use case: keep technical
diagrams, Python learning material, Kubernetes architecture images,
cheat sheets, and other useful visual references rotating on a spare
portrait monitor.

Instead of loading an entire presentation, Knowledge Screen discovers
image files from a directory and displays them one at a time. This keeps
the application simple and makes the content directory itself the source
of the slideshow.

Possible content includes:

-   Python learning diagrams
-   Kubernetes architecture diagrams
-   AWS/cloud reference material
-   Terraform and DevOps cheat sheets
-   Linux command references
-   Networking diagrams
-   Certification study material
-   Personal notes exported as images
-   Any PNG, JPG, or JPEG reference images

------------------------------------------------------------------------

## Current Features

-   Full-screen, borderless image display
-   PNG, JPG, and JPEG support
-   Multi-monitor detection
-   Prefer portrait monitor automatically
-   Automatic fallback to the primary monitor
-   Manual monitor selection by index
-   Windows and Linux support
-   Configurable image-change interval
-   Recursive directory scanning
-   Optional shuffle
-   Aspect-ratio-preserving image scaling
-   EXIF orientation handling
-   Configurable background color
-   Optional filename display
-   Optional hidden mouse cursor
-   Keyboard controls for navigation
-   Pause/resume support
-   Configuration through `slideshow.ini`

------------------------------------------------------------------------

## Project Structure

``` text
knowledge-screen/
├── .gitignore
├── LICENSE
├── README.md
├── python_image_slideshow.py
├── requirements.txt
└── slideshow.ini
```

> If the main script is renamed to `knowledge_screen.py`, substitute
> that filename in the commands below.

### `python_image_slideshow.py`

This is the main application.

It is responsible for:

-   reading the configuration
-   discovering supported images
-   detecting available monitors
-   selecting the target monitor
-   creating the Tkinter display window
-   loading and resizing images with Pillow
-   moving between images
-   handling the slideshow timer
-   processing keyboard commands
-   handling basic runtime errors

### `slideshow.ini`

This contains user-configurable settings.

The important design idea is to keep **configuration separate from
application logic**. For example, changing the slideshow interval or
image directory should not require editing Python source code.

### `requirements.txt`

Lists third-party Python dependencies required by the project.

Currently:

``` text
Pillow
screeninfo
```

### `.gitignore`

Prevents local/generated files such as the Python virtual environment
from being committed to Git.

A recommended entry is:

``` gitignore
.venv/
```

### `LICENSE`

Contains the project's open-source license.

------------------------------------------------------------------------

# Installation

## 1. Clone the Repository

``` bash
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen
```

------------------------------------------------------------------------

## 2. Verify Python

Knowledge Screen requires Python 3.

``` bash
python --version
```

On some Linux distributions the command may be:

``` bash
python3 --version
```

------------------------------------------------------------------------

## 3. Create a Project Virtual Environment

Using a virtual environment keeps Knowledge Screen's Python packages
isolated from packages installed globally or for other projects.

Create a virtual environment named `.venv`:

### Windows

``` powershell
python -m venv .venv
```

### Linux

``` bash
python3 -m venv .venv
```

This creates a local directory:

``` text
knowledge-screen/
└── .venv/
```

The `.venv/` directory should **not** be committed to Git.

------------------------------------------------------------------------

## 4. Activate the Virtual Environment

### Windows PowerShell

``` powershell
.\.venv\Scripts\Activate.ps1
```

The prompt should change to something similar to:

``` text
(.venv) PS C:\...\knowledge-screen>
```

To verify which Python executable is being used:

``` powershell
where.exe python
```

The first result should point into:

``` text
knowledge-screen\.venv\Scripts\python.exe
```

### Windows Command Prompt

``` cmd
.venv\Scripts\activate.bat
```

### Linux

``` bash
source .venv/bin/activate
```

The shell prompt should now normally contain:

``` text
(.venv)
```

You can verify it with:

``` bash
which python
```

------------------------------------------------------------------------

## 5. Upgrade pip (Recommended)

``` bash
python -m pip install --upgrade pip
```

------------------------------------------------------------------------

## 6. Install Dependencies

``` bash
python -m pip install -r requirements.txt
```

This installs the required packages into `.venv`, not globally.

### Linux Tkinter Note

Tkinter is part of Python's standard library, but some minimal Linux
distributions package it separately.

On Ubuntu/Debian:

``` bash
sudo apt install python3-tk
```

------------------------------------------------------------------------

# Configuration

Edit:

``` text
slideshow.ini
```

before starting Knowledge Screen.

Example:

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

For Linux, an image directory might look like:

``` ini
image_folder = /home/user/Pictures/TechLearning
```

------------------------------------------------------------------------

# Configuration Reference

## `[slideshow]`

### `image_folder`

Directory containing images to display.

Windows example:

``` ini
image_folder = D:\Learning\TechImages
```

Linux example:

``` ini
image_folder = /home/user/Pictures/TechLearning
```

### `image_change_seconds`

How long each image remains visible.

``` ini
image_change_seconds = 120
```

Examples:

    Value Duration
  ------- ------------
     `30` 30 seconds
     `60` 1 minute
    `120` 2 minutes
    `300` 5 minutes

### `recursive`

Controls whether subdirectories are searched.

``` ini
recursive = true
```

With recursive scanning enabled, a directory can be organized naturally:

``` text
TechLearning/
├── Python/
├── Kubernetes/
├── AWS/
├── Terraform/
└── Linux/
```

All supported images underneath these directories will be discovered.

### `shuffle`

Controls whether the initial image list is randomized.

``` ini
shuffle = false
```

### `background_color`

Background shown around an image when its aspect ratio does not fill the
complete display.

``` ini
background_color = black
```

------------------------------------------------------------------------

## `[display]`

### `monitor_mode`

Controls which monitor Knowledge Screen uses.

Three modes are supported:

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

This is the recommended default.

The selection logic is:

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

In other words:

1.  Find monitors where `height > width`.
2.  If a portrait monitor exists, use the first one.
3.  Otherwise use the operating system's primary monitor.
4.  If no primary monitor is reported, use the first available monitor.

This means Knowledge Screen also works normally on a laptop or desktop
with only a landscape display.

### `primary`

Always use the primary monitor:

``` ini
monitor_mode = primary
```

### `index`

Manually select a detected monitor:

``` ini
monitor_mode = index
monitor_index = 1
```

Monitor numbering begins at `0`.

Knowledge Screen prints detected monitors when it starts, for example:

``` text
Detected monitors:
  [0] 2560x1440 at (0, 0) Landscape Primary=True
  [1] 1080x1920 at (2560, 0) Portrait Primary=False

Monitor selection: portrait monitor found.
Displaying on: 1080x1920 at (2560, 0)
```

### `hide_mouse_cursor`

``` ini
hide_mouse_cursor = true
```

Hides the pointer while Knowledge Screen is running.

### `show_filename`

``` ini
show_filename = false
```

Controls whether the current filename is shown near the bottom of the
display.

It can also be toggled at runtime with `F`.

### `filename_font_size`

``` ini
filename_font_size = 18
```

Sets the filename text size.

------------------------------------------------------------------------

# Running Knowledge Screen

Activate the virtual environment first.

Then run:

``` bash
python python_image_slideshow.py
```

If the script has been renamed:

``` bash
python knowledge_screen.py
```

Knowledge Screen will:

1.  Read `slideshow.ini`.
2.  Validate important configuration settings.
3.  Search the configured image directory.
4.  Detect available monitors.
5.  Select the preferred display.
6.  Create a borderless window covering that monitor.
7.  Display the first image.
8.  Automatically advance according to the configured interval.

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

Knowledge Screen intentionally preserves the original image aspect
ratio.

For example, suppose the target portrait monitor is:

``` text
1080 x 1920
```

A portrait image can occupy most of that display.

A landscape image may instead be resized to something similar to:

``` text
1080 x 650
```

and centered against the configured background.

The image is **not stretched** to 1080 x 1920.

Pillow performs the resize using high-quality LANCZOS resampling:

``` python
image.thumbnail(
    (monitor_width, monitor_height),
    Image.Resampling.LANCZOS,
)
```

The program also applies EXIF orientation information when present,
which helps photographs appear in their intended orientation.

------------------------------------------------------------------------

# How the Python Components Work

Knowledge Screen is also a practical example of several useful Python
concepts.

## `configparser`

Python's standard `configparser` module reads `slideshow.ini`.

``` python
import configparser
```

This lets the program read typed values such as integers and booleans:

``` python
parser.getint(...)
parser.getboolean(...)
```

This demonstrates an important application-design principle:

> **Code defines how the program works; configuration defines how a
> particular installation should behave.**

------------------------------------------------------------------------

## `pathlib`

The application uses `Path` rather than manually constructing filesystem
path strings:

``` python
from pathlib import Path
```

It is used for tasks including:

-   locating `slideshow.ini`
-   checking whether the image directory exists
-   recursively finding files
-   examining file extensions

`pathlib` also helps keep filesystem code portable between Windows and
Linux.

------------------------------------------------------------------------

## Pillow

Pillow provides image processing:

``` python
from PIL import Image, ImageOps, ImageTk
```

It handles:

-   opening image files
-   EXIF orientation
-   resizing images
-   preserving aspect ratio
-   converting images for Tkinter display

------------------------------------------------------------------------

## `screeninfo`

`screeninfo` provides multi-monitor information:

``` python
from screeninfo import get_monitors
```

The program can inspect:

-   monitor width
-   monitor height
-   X/Y desktop coordinates
-   primary-monitor status

Portrait detection is conceptually:

``` python
monitor.height > monitor.width
```

------------------------------------------------------------------------

## Tkinter

Tkinter provides the application's graphical window and event loop.

It is responsible for:

-   creating the slideshow window
-   displaying the image
-   processing keyboard input
-   scheduling image changes
-   keeping the application running

The program uses a borderless window positioned explicitly at the
selected monitor's coordinates. This is useful for multi-monitor setups
because the application controls exactly where the slideshow appears.

------------------------------------------------------------------------

## Classes

The application currently separates responsibilities into classes.

### `SlideshowConfig`

Responsible for reading and validating configuration.

### `ImageSlideshow`

Responsible for the running application:

-   monitor selection
-   image discovery
-   display
-   timers
-   navigation
-   keyboard input

This keeps configuration handling separate from slideshow behavior.

------------------------------------------------------------------------

## Exceptions and Validation

The program checks for problems such as:

-   missing configuration file
-   invalid image directory
-   no supported images
-   invalid monitor mode
-   invalid monitor index
-   image loading failures

Instead of silently failing, useful errors are printed to the terminal.

------------------------------------------------------------------------

# Supported Image Formats

Currently:

``` text
.png
.jpg
.jpeg
```

The check is case-insensitive.

------------------------------------------------------------------------

# Stopping Knowledge Screen

Press:

``` text
Esc
```

To leave the Python virtual environment afterward:

``` bash
deactivate
```

------------------------------------------------------------------------

# Typical Workflow After Cloning

For a new user, the complete workflow is:

### Windows PowerShell

``` powershell
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Edit:

``` text
slideshow.ini
```

Set at least:

``` ini
image_folder = C:\path\to\your\images
```

Then:

``` powershell
python python_image_slideshow.py
```

Exit with `Esc`.

When finished:

``` powershell
deactivate
```

### Linux

``` bash
git clone https://github.com/pymisc/knowledge-screen.git
cd knowledge-screen

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Edit `slideshow.ini`:

``` ini
image_folder = /path/to/your/images
```

Then:

``` bash
python python_image_slideshow.py
```

When finished:

``` bash
deactivate
```

------------------------------------------------------------------------

# Development Setup

If you plan to modify Knowledge Screen rather than only run it, use the
same `.venv` environment.

A useful development cycle is:

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
Run locally
      |
      v
Test
      |
      v
Commit changes
```

Do not commit `.venv/`. Dependencies needed by the project belong in
`requirements.txt`.

------------------------------------------------------------------------

# Roadmap

Knowledge Screen intentionally starts small, but the name and
architecture leave room for expansion.

Potential future capabilities include:

-   GIF support
-   WebP support
-   PDF page display
-   automatic directory watching
-   automatically include newly added files
-   categories
-   playlists
-   playlist scheduling
-   different content at different times of day
-   Raspberry Pi support
-   kiosk mode
-   better logging
-   automated tests
-   test coverage
-   CI/CD with GitHub Actions
-   application packaging
-   standalone executable builds

A possible evolution:

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

## No images found

Verify `image_folder` in `slideshow.ini` and make sure the directory
contains `.png`, `.jpg`, or `.jpeg` files.

If images are stored in subdirectories, use:

``` ini
recursive = true
```

## Wrong monitor selected

Start the application from a terminal and inspect the detected monitor
list.

You can force a monitor with:

``` ini
monitor_mode = index
monitor_index = 1
```

## PowerShell blocks virtual-environment activation

If PowerShell prevents `Activate.ps1` from running because of the local
execution policy, review your organization's/security policy before
changing it. An alternative is to use Command Prompt activation:

``` cmd
.venv\Scripts\activate.bat
```

## Tkinter missing on Linux

On Ubuntu/Debian:

``` bash
sudo apt install python3-tk
```

------------------------------------------------------------------------

# Contributing

Contributions, bug reports, testing feedback, and feature ideas are
welcome.

When contributing:

1.  Create a branch.
2.  Keep changes focused.
3.  Test the change locally.
4.  Update documentation when behavior changes.
5.  Open a pull request describing the change and why it is useful.

------------------------------------------------------------------------

# License

Knowledge Screen is open-source software released under the license
included in the repository.

------------------------------------------------------------------------

## Project Philosophy

Knowledge Screen follows a simple idea:

> **Useful knowledge should not have to stay buried in folders. Put it
> on a screen where you can see it.**
