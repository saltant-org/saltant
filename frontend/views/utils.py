"""Contains general helpers for frontend views."""

from datetime import date, timedelta
import json
from .utils_stats import determine_days_to_plot, get_job_state_data


def translate_num_days_to_plot_title(num_days):
    """Translate a date range to a plot title.

    Args:
        num_days: An integer specifying how many days back to look.

    Returns:
        A string to be used for the pie plot title.
    """
    if num_days == 7:
        return "last week's jobs"

    # Get the number of weeks
    num_weeks = num_days / 7

    if num_weeks.is_integer():
        num_weeks_str = str(int(num_weeks))
    else:
        num_weeks_str = "{0:.1f}".format(num_weeks)

    return "last %s weeks' jobs" % num_weeks_str


def get_context_data_for_chartjs(task_class="both", task_type_pk=None):
    """Get Chart.js data to pass to the context.

    Args:
        task_class: An optional string indicating which task class to
            use. Can be either "container", "executable", or "both".
        task_type_pk: An optional integer indicating the primary key of
            the task type to use. Defaults to None, which means,
            consider all task types.

    Returns:
        A dictionary ready to meld with the context dictionary.
    """
    context = {}

    # Get data for Chart.js
    days_to_plot = determine_days_to_plot(
        task_class=task_class, task_type_pk=task_type_pk
    )
    today = date.today()
    other_date = date.today() - timedelta(days=days_to_plot)

    chart_data = get_job_state_data(
        task_class=task_class,
        task_type_pk=task_type_pk,
        start_date=other_date,
        end_date=today,
    )

    # Add the Charts.js stuff to our context
    context["show_chart"] = chart_data["has_data"]
    context["labels"] = json.dumps(chart_data["labels"])
    context["datasets"] = json.dumps(chart_data["datasets"])
    context["chart_title"] = translate_num_days_to_plot_title(days_to_plot)

    return context
