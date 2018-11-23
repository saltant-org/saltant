"""Constants for the frontend."""

from tasksapi.constants import (
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
)


# Colours to represent states. The bold version are the same colours but
# "bold". Note that this is excluding the "created" state, which is
# ephemeral.
STATE_COLOR_DICT = {
    PUBLISHED: "#a3d9ff",
    RUNNING: "#fcecc9",
    SUCCESSFUL: "#445e93",
    FAILED: "#f93943",
    TERMINATED: "#fcb0b3",
}
STATE_BOLD_COLOR_DICT = {
    PUBLISHED: "#2da7ff",
    RUNNING: "#fcc858",
    SUCCESSFUL: "#1c4493",
    FAILED: "#f90915",
    TERMINATED: "#fc7176",
}
