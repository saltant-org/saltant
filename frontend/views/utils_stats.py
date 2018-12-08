"""Contains helpers for getting and packaging data statistics."""

from datetime import date, timedelta
from frontend.constants import (
    DATES_LIST,
    DEFAULT_DAYS_TO_PLOT,
    INTERESTING_STATES,
    STATE_COLOR_DICT,
)
from tasksapi.constants import CONTAINER_TASK, CREATED
from tasksapi.models import ContainerTaskInstance, ExecutableTaskInstance


def translate_date_to_string(
    this_date, day_of_week=False, today_and_yesterday=True, today=None
):
    """Translate a date to a string.

    Args:
        this_date: A datetime.date to translate.
        day_of_week: An optional Boolean specifying whether to use the
            days of the week as the string names. Defaults to False.
        today_and_yesterday: An optional Boolean specifying whether to
            use the "Today" and "Yesterday" as strings for the current
            and previous date, respectively. Defaults to True.
        today: A datetime.date indicating the current date. If this is
            None and today_and_yesterday is True, then a
            datetime.date.today call will be made per function call,
            which might not be efficient. Defaults to None. Does nothing
            if day_of_week is False.
    """
    if today_and_yesterday:
        # Load up today if necessary
        if today is None:
            today = date.today()

        # Translate
        if this_date == today:
            return "Today"
        elif this_date == today - timedelta(days=1):
            return "Yesterday"

    if day_of_week:
        return DATES_LIST[this_date.weekday()]

    # Use ISO 8601
    return this_date.isoformat()


def determine_days_to_plot(task_class="both", task_type_pk=None):
    """Determine how many days to plot using the "default behavior".

    The default behavior is as follows: use a default number of days,
    but if there aren't any tasks within the default, then show up to
    the week before the most recent task. And if there aren't any tasks,
    just use the default number of days.

    Args:
        task_class: An optional string indicating which task class to
            use. Can be either "container", "executable", or "both". The
            former two are defined as constants in tasksapi, which we'll
            be using here. Defaults to "both".
        task_type_pk: An optional integer indicating the primary key of
            the task type to use. Defaults to None, which means,
            consider all task types.

    Returns:
        An integer specifying the number of days to plot.
    """
    # First build a list of the task instance models to use
    if task_class == "both":
        instance_models = [ContainerTaskInstance, ExecutableTaskInstance]
    elif task_class == CONTAINER_TASK:
        instance_models = [ContainerTaskInstance]
    else:
        instance_models = [ExecutableTaskInstance]

    # Now build the corresponding querysets
    querysets = [x.objects.all() for x in instance_models]

    # Now filter by task type, possibly
    if task_type_pk is not None:
        querysets = [x.filter(task_type__pk=task_type_pk) for x in querysets]

    # Grab the latest dates of an instance for each queryset, making
    # sure to not include jobs with "created" state (since these aren't
    # shown in the plot).
    latest_dates = [
        i.datetime_created.date()
        for i in [q.exclude(state=CREATED).first() for q in querysets]
        if i is not None
    ]

    # Make sure we have any instances at all, if not, just use default
    # value.
    if not latest_dates:
        return DEFAULT_DAYS_TO_PLOT

    # Now pick out the latest date
    latest_date = max(latest_dates)

    # Count how many days between today and that date
    delta_days = (date.today() - latest_date).days

    # If the latest date is within the range of the default, just use
    # the default
    if delta_days <= DEFAULT_DAYS_TO_PLOT:
        return DEFAULT_DAYS_TO_PLOT

    # Otherwise use the number of days between today and that date, plus
    # 7 days
    return delta_days + 7


def get_job_state_data(
    task_class="both",
    task_type_pk=None,
    start_date=date.today(),
    end_date=date.today(),
):
    """Get data for job states.

    This gets the state counts of jobs created in a time range. In the
    arguments below, both start and end date are inclusive. Note that
    providing both task_class = "both" and a non-None task_type_pk
    doesn't really make sense, since task types are specific to task
    classes.

    Args:
        task_class: An optional string indicating which task class to
            use. Can be either "container", "executable", or "both". The
            former two are defined as constants in tasksapi, which we'll
            be using here. Defaults to "both".
        task_type_pk: An optional integer indicating the primary key of
            the task type to use. Defaults to None, which means,
            consider all task types.
        start_date: An optional datetime.date indicating the start of
            the date range. Defaults to today.
        end_date: An optional datetime.date indicating the end of the
            date range. Defaults to today.

    Returns:
        Nested dictionaries following the "datasets" and "labels" schema
        for Chart.js pie chargs. To use with Chart.js, make sure to
        encode the dictionaries to JSON strings first.
    """
    # First build a list of the task instance models to use
    if task_class == "both":
        instance_models = [ContainerTaskInstance, ExecutableTaskInstance]
    elif task_class == CONTAINER_TASK:
        instance_models = [ContainerTaskInstance]
    else:
        instance_models = [ExecutableTaskInstance]

    # Now build the corresponding querysets
    querysets = [x.objects.all() for x in instance_models]

    # Now filter by task type, possibly
    if task_type_pk is not None:
        querysets = [x.filter(task_type__pk=task_type_pk) for x in querysets]

    # And filter by date
    if start_date == end_date:
        querysets = [
            x.filter(datetime_created__date=start_date) for x in querysets
        ]
    else:
        querysets = [
            x.filter(datetime_created__date__gte=start_date).filter(
                datetime_created__date__lte=end_date
            )
            for x in querysets
        ]

    # Now build up the dataset based on state
    dataset = dict()

    dataset["data"] = [
        sum([x.filter(state=state).count() for x in querysets])
        for state in INTERESTING_STATES
    ]
    dataset["backgroundColor"] = [
        STATE_COLOR_DICT[state] for state in INTERESTING_STATES
    ]

    # Record if our datasets has any non-zero data
    has_data = bool(sum(dataset["data"]) > 0)

    # List the labels
    labels = list(INTERESTING_STATES)

    return {"labels": labels, "datasets": [dataset], "has_data": has_data}


def get_job_state_data_date_enumerated(
    task_class="both",
    task_type_pk=None,
    start_date=date.today(),
    end_date=date.today(),
    use_day_of_week=False,
    use_today_and_yesterday=True,
):
    """Get data for job states eumerated by date.

    This is very similar too the "get_job_state" function above, but
    different enough that it warrants another function. The main
    differences are how the datasets dictionary is structured (which is
    an essential difference).

    Args:
        task_class: An optional string indicating which task class to
            use. Can be either "container", "executable", or "both". The
            former two are defined as constants in tasksapi, which we'll
            be using here. Defaults to "both".
        task_type_pk: An optional integer indicating the primary key of
            the task type to use. Defaults to None, which means,
            consider all task types.
        start_date: An optional datetime.date indicating the start of
            the date range. Defaults to today.
        end_date: An optional datetime.date indicating the end of the
            date range. Defaults to today.
        use_day_of_week: An optional Boolean specifying whether to
            enumerate dates as Mon, Tues, Wed, etc. Defaults to False,
            which means that it will use ISO 8601 dates instead.
        use_today_and_yesterday: An optional Boolean specifying whether
            to label dates which are the current or previous date with
            "Today" and "Yesterday", respectively. Defaults to True.

    Returns:
        Nested dictionaries following the "datasets" and "labels" schema
        for Chart.js pie chargs. To use with Chart.js, make sure to
        encode the dictionaries to JSON strings first.
    """
    # First build a list of the task instance models to use
    if task_class == "both":
        instance_models = [ContainerTaskInstance, ExecutableTaskInstance]
    elif task_class == CONTAINER_TASK:
        instance_models = [ContainerTaskInstance]
    else:
        instance_models = [ExecutableTaskInstance]

    # Now build the corresponding querysets
    querysets = [x.objects.all() for x in instance_models]

    # Now filter by task type, possibly
    if task_type_pk is not None:
        querysets = [x.filter(task_type__pk=task_type_pk) for x in querysets]

    # Now figure out what dates we care about
    delta = end_date - start_date

    my_dates = [start_date + timedelta(i) for i in range(delta.days + 1)]

    # Here we have datasets for each state, each of which has data per
    # date
    datasets = []

    for state in INTERESTING_STATES:
        dataset = dict()
        dataset["backgroundColor"] = STATE_COLOR_DICT[state]
        dataset["label"] = state

        dataset["data"] = [
            sum(
                [
                    x.filter(state=state)
                    .filter(datetime_created__date=d)
                    .count()
                    for x in querysets
                ]
            )
            for d in my_dates
        ]

        datasets.append(dataset)

    # List the dates for the chart labels
    labels = [
        translate_date_to_string(
            d,
            day_of_week=use_day_of_week,
            today_and_yesterday=use_today_and_yesterday,
            today=date.today(),
        )
        for d in my_dates
    ]

    return {"labels": labels, "datasets": datasets}
