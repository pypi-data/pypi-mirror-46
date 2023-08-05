"""
submission related util functions
"""
import click
import json
import os
import shutil
from mimir_cli.strings import (
    ERR_INVALID_FILE,
    SUB_CONFIRM_FORCE,
    SUB_SUCCESS_URL,
    SUB_WARNING,
    ZIP_LOC,
)
from mimir_cli.utils.auth import post
from mimir_cli.utils.state import (
    api_submit_url,
    api_view_submission_url,
    debug,
    error_out,
)


def collect_submission_file(filename):
    """tries to collect the submission file and zip if need be"""
    submission_file = False
    if filename.lower().endswith(".zip"):
        submission_file = open(filename, "rb")
    else:
        if os.path.isdir(filename):
            try:
                os.remove(ZIP_LOC)
            except OSError:
                pass
            shutil.make_archive(os.path.splitext(ZIP_LOC)[0], "zip", filename)
            submission_file = open(ZIP_LOC, "rb")
        else:
            submission_file = open(filename, "rb")
    if not submission_file:
        click.echo(ERR_INVALID_FILE.format(filename))
    return submission_file


def _submit_post(url, filename, project_id, on_behalf_of=None, custom_penalty=0):
    """actually perform the submit"""
    data = {"projectSubmission[projectId]": project_id, "submission_source": "cli"}

    if on_behalf_of and isinstance(on_behalf_of, str):
        data["submitting_on_behalf"] = True
        data["submitting_as_email"] = on_behalf_of
        data["custom_penalty"] = custom_penalty

    submission_file = collect_submission_file(filename)
    files = {"zip_file[]": submission_file}
    debug(data)
    click.echo("submitting...")
    submission_request = post(url, files=files, data=data)
    if submission_request.status_code == 401:
        error_out("unauthorized - please try logging back in!")
    if submission_request.status_code == 404:
        error_out("invalid project_id given!")
    if submission_request.status_code == 412:
        error_out("mimir classroom trial expired!")
    submission_file.close()
    result = json.loads(submission_request.text)
    debug(result)
    if "projectSubmission" in result:
        click.echo(
            "{}{}\n".format(
                SUB_SUCCESS_URL,
                api_view_submission_url(result["projectSubmission"]["id"]),
            )
        )
    return result


def submit_to_mimir(
    filename, project_id, on_behalf_of=None, custom_penalty=0, forced=False
):
    """submits file(s) to the mimir platform"""
    url = api_submit_url(project_id)

    def do_submit(force: bool = False):
        """actually do the submit"""
        return _submit_post(
            url + ("?ignore_filenames=true" if force else ""),
            filename,
            project_id,
            on_behalf_of=on_behalf_of,
            custom_penalty=custom_penalty,
        )

    def display_result(result):
        """handles displaying post request results"""
        if "errorMessage" in result:
            error_out(result["errorMessage"])
        if "submitErrorMessage" in result:
            if "missing_files" not in result["submitError"]:
                error_out(result["submitErrorMessage"])

    result = do_submit(force=forced)
    debug(result)
    display_result(result)

    if "submitErrorMessage" in result and result["submitError"] == "missing_files":
        click.echo(SUB_WARNING)
        click.echo(result["submitErrorMessage"])
        if click.confirm(SUB_CONFIRM_FORCE):
            result = do_submit(force=True)
            display_result(result)
        else:
            click.echo("\nsubmission canceled\n")
