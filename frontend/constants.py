"""Constants for the frontend."""

from tasksapi.constants import (
    PUBLISHED,
    RUNNING,
    SUCCESSFUL,
    FAILED,
    TERMINATED,
)

# Use this to translate from weekday number to day of week
DATES_LIST = ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"]

# States we care about emphasizing. The order here is signicant
INTERESTING_STATES = (SUCCESSFUL, FAILED, TERMINATED, RUNNING, PUBLISHED)

# Colours to represent states we care about.
STATE_COLOR_DICT = {
    PUBLISHED: "#f2efea",
    RUNNING: "#9bdeac",
    SUCCESSFUL: "#a3d9ff",
    FAILED: "#ff6978",
    TERMINATED: "#fac8cd",
}

# Cookie attribute name of selected task class
SELECTED_TASK_CLASS = "selected_task_class"

# The default number of days to plot on the home page
HOMEPAGE_DEFAULT_DAYS_TO_PLOT = 7
