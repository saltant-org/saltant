"""Contains helpers for getting task instance logs."""

from django.conf import settings
import boto3


def get_s3_logs_for_task_instance(job_uuid):
    """Get logs for a task instance.

    The text from the job logs will be one long text strings, so no
    splitting at new lines here.

    Args:
        job_uuid: A string specifying the UUID of the task instance to
            get logs for.

    Returns:
        A dictionary where keys are file names and values are the text
        they contain.
    """
    # This'll grab its settings from the environment (ultimately coming
    # from .env file)
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(settings.AWS_LOGS_BUCKET_NAME)

    # Get the files
    log_files_dict = {}
    log_files = bucket.objects.filter(Prefix=job_uuid)

    for log_file in log_files:
        # Extract the file name and text
        file_name = log_file.key[len(job_uuid) + 1 :]
        file_text = log_file.get()["Body"].read().decode("utf-8")

        # Add in this log file to our output
        log_files_dict[file_name] = file_text

    return log_files_dict


def get_s3_logs_for_executable_task_instance(job_uuid):
    """Get stdout and stderr logs for executable task instances.

    This is basically the same thing as get_s3_logs_for_task_instance
    except it changes the key names to "stdout" and "stderr" (since those
    are the only two types of logs an executable task type can have).

    Args:
        job_uuid: A string specifying the UUID of the exedcutable task
            instance to get logs for.

    Returns:
        A dictionary with keys "stdout" and "stderr" where the values are text
        containing the corresponding log text.
    """
    # Call the base function
    these_logs = get_s3_logs_for_task_instance(job_uuid)

    # Update the key names
    these_logs["stdout"] = these_logs.pop(job_uuid + "-" + "stdout.txt")
    these_logs["stderr"] = these_logs.pop(job_uuid + "-" + "stderr.txt")

    return these_logs
