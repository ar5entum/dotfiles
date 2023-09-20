from typing import List
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from datetime import datetime
#Colors
colors = {
    "background": "#292D3E",
    "foreground": "#A6ACCD",
    "current_group_bg": "#3B4252",
    "current_group_fg": "#D8DEE9",
    "inactive_group_bg": "#292D3E",
    "inactive_group_fg": "#4C566A",
    "highlight": "#C792EA",
}

mod = 'mod4'

# Key bindings
keys = [
    
# Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    #Kill focused window
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    #Shutdown Qtile
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    #Reload Qtile
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload Qtile"),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),  # Move focus to next pane

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),  # Swap panes

    # Change focus between screens
    Key([mod], "h", lazy.to_screen(0)),  # Focus the first screen
    Key([mod], "l", lazy.to_screen(1)),  # Focus the second screen

    # Launch terminal
    Key([mod], "Return", lazy.spawn("kitty")),

    # Launch dmenu
    Key([mod], "r", lazy.spawn("rofi -show drun")),

    #Launch file explorer
    Key([mod], "e", lazy.spawn("nautilus .")),

    #Launch browser
    Key([mod], "b", lazy.spawn("chromium")),

    # Take arscreenshot
    Key([], "Print", lazy.spawn("scrot '%Y-%m-%d_$wx$h.png' -e 'mv $f ~/Pictures/Screenshots/'"))
    ]
    # Groups
groups = [
    Group("1", label="R", layout="monadtall"),
    Group("2", label="U", layout="monadtall"),
    Group("3", label="V", layout="monadtall"),
    Group("4", label="I", layout="monadtall"),
    Group("5", label="♥", layout="monadtall"),
]

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True)
                    )
                ]
            )

# Layouts
layouts = [
    layout.MonadTall(border_focus=colors["highlight"], border_normal=colors["current_group_bg"], border_width=1),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=12,
    padding=3,
    background=colors["background"],
    foreground=colors["foreground"],
)

extension_defaults = widget_defaults.copy()

# Widgets
def init_widgets_screen1():
    widgets_screen1 = [

        widget.GroupBox(
            active=colors["current_group_fg"],
            inactive=colors["inactive_group_fg"],
            highlight_method="block",
            block_highlight_text_color=colors["foreground"],
            this_current_screen_border=colors["current_group_bg"],
            this_screen_border=colors["inactive_group_bg"],
        ),
        widget.Prompt(),
        widget.WindowName(),
        widget.Chord(
            chords_colors={
                "launch": (colors["foreground"], colors["highlight"]),
            },
            name_transform=lambda name: name.upper(),
        ),
        widget.Systray(),
        widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
    ]
    return widgets_screen1

# Function to get the current date and time
def get_date_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Create widgets
date_time_widget = widget.TextBox(
    text="date",
    foreground="ffffff",
    background="000000",
    padding=10,
    fontsize=14,
    width=bar.CALCULATED
)

volume_widget = widget.Volume(
    fmt=' {}',
    foreground=colors["highlight"],
    padding=5,
    font='mono'
)

screens = [
    Screen(top=bar.Bar([
        widget.Spacer(),
        widget.Clock(format='%d-%m-%Y %a %I %M %p'),
        widget.Spacer(),
        volume_widget,
    ], 
                       size=24),
           wallpaper='~/Pictures/wallpaper.png',
            wallpaper_mode='stretch',)
]

# Configurations
if __name__ == "__main__":
    lazy.load("libqtile.extension.dmenu")
    lazy.load("libqtile.extension.window_list")
    lazy.load("libqtile.extension.backlight")
    lazy.load("libqtile.extension.hardcode")
    lazy.load("libqtile.extension.spellcheck")
    lazy.load("libqtile.extension.mpd")
    lazy.load("libqtile.extension.notification")

    screens = [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=24))]

    keys.append(Key([mod], "r", lazy.spawncmd()))
    keys.append(Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q -D pulse sset Master 5%+")))
    keys.append(Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q -D pulse sset Master 5%-")))
    keys.append(Key([], "XF86AudioMute", lazy.spawn("amixer -q -D pulse sset Master toggle")))
    keys.append(Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 5%+")))
    keys.append(Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")))
    # Drag floating layouts
    mouse = [
        Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
    ]

    # Define a hook function to be called on startup
    def autostart():
        # Start applications
        lazy.spawn("picom &")
        lazy.spawn("nm-applet &")
        lazy.spawn("blueman-applet &")

    # Define a hook function to be called when Qtile starts up

    # Define a hook function to be called when Qtile shuts down
    def shutdown():
        # Save any necessary state or perform cleanup tasks
        pass

    # Set hooks
    hook.subscribe.startup(autostart)
    hook.subscribe.shutdown(shutdown)

    # Define Qtile config
    config = {
        "mod": "mod4",
        "terminal": "kitty",
        "keys": keys,
        "groups": groups,
        "layouts": layouts,
        "widget_defaults": widget_defaults,
        "extension_defaults": extension_defaults,
        "screens": screens,
        "mouse": mouse,
        "focus_on_window_activation": "smart",
    }

