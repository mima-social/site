"""Animation scenes for app-shots/animate.py.

A scene is a list of steps played in order over the dummy app pages that
build.py writes. Each step shows one view for `ms` milliseconds:

    view   the dummy page (app-shots/<view>.html)
    ms     how long the step lasts
    to     CSS selector in that view; the pointer glides to its centre
    click  True: the pointer clicks when it arrives, at the end of the step
    fade   crossfade from the previous view, in ms (default 200)

`size` is the window in CSS px, like the stills in render.sh. `poster_ms` picks
the still shown before the video plays (default: the last frame, so the
poster shows the result). `alt` describes the whole animation in words, for
the sidecar and for whoever writes the guide's alt text.
"""

SCENES = {
    "connect-claude-desktop": {
        "size": (960, 800),
        "fps": 20,
        "start": (0.45, 0.62),  # where the pointer begins, as a fraction of the window
        "alt": "In Mima, the pointer clicks Connect Mima to your agent in the top right. Settings opens on "
               "Connectors with the Local MCP server off. A click on Connect to Claude Desktop turns the "
               "server on and marks Claude Desktop as connected. Back on the News Wall, the header button "
               "reads Mima is connected to your agent.",
        "steps": [
            {"view": "anim-news", "ms": 1900, "to": ".agent-btn", "click": True},
            {"view": "anim-connectors-off", "ms": 2400, "to": '[data-anim="connect-claude"]', "click": True},
            {"view": "anim-connectors-connecting", "ms": 800, "fade": 0},
            {"view": "anim-connectors-done", "ms": 2600, "fade": 150},
            {"view": "anim-connectors-done", "ms": 1500, "to": '[data-anim="close-settings"]', "click": True, "fade": 0},
            {"view": "anim-news-connected", "ms": 2800},
        ],
    },
}
