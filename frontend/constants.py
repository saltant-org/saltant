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
    PUBLISHED: "#f2efea",
    RUNNING: "#9bdeac",
    SUCCESSFUL: "#a3d9ff",
    FAILED: "#ff6978",
    TERMINATED: "#fac8cd",
}
