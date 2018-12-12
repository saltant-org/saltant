"""Constants for the frontend."""

from tasksapi.constants import (
    CREATED,
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

STATE_COLOR_LIGHTER_DICT = {
    CREATED: "#f9ebd1",
    PUBLISHED: "#f9ebd1",
    RUNNING: "#b2e8c0",
    SUCCESSFUL: "#bce3ff",
    FAILED: "#ffa8b0",
    TERMINATED: "#f9d9dc",
}

# Cookie attribute name of selected task class
SELECTED_TASK_CLASS = "selected_task_class"

# The default number of days to plot for task instances, provided there
# are tasks within this range.
DEFAULT_DAYS_TO_PLOT = 7
