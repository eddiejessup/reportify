#! /usr/bin/env python

import os
import subprocess
from time import sleep
from datetime import datetime
from argparse import ArgumentParser, RawTextHelpFormatter


BASE = os.path.expanduser('~/')
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
REPORTIFY_CMD = os.path.join(DIR_SCRIPT, 'reportify.py')
STORY_NAME = '%s_project' % datetime.now().strftime('%Y%m')
REPORT_FN = 'Report.ipynb'
# TODO: this is quite rigid, but making it flexible is hard and it will involve lots of command line arguments
CMD = '{rc} %scode/misc/stories/{s}/report/{r} -to %sprojects/{s}/report/' % (BASE, BASE)

__description__ = '''Description.

Continuously reportify a jupyter notebook.

Notice that this uses the reportify module with the extension `--to`.

Assume
  * your reportify script is in this same directory. (If not need full path, e.g. `~/my/path/to/reportify.py`)
  * your report is in the folder ~/code/stories/201701_my_analysis/report/
  * you report is My_Report.ipynb (not sure works well if spaces!)
  * the extension py_markdown is enabled

Then you can run (from where this script is located)

$ ./const_reportify.py --story-name 201701_my_analysis --report-fn My_Report.ipynb

If for some reason your reportify script is not in this same directory:

$ ./const_reportify.py --reportify-cmd ~/my/path/to/reportify.py --story-name 201701_my_analysis --report-fn My_Report.ipynb


Then press ctrl+c in the terminal to stop it.

You can add this in your .alias "alias const_reportify='%s/const_reportify.py''"
''' % DIR_SCRIPT


def get_process(cmd):
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    return process.returncode


def run_cmd(reportify_cmd, story_name, report_fn, cmd_to_run):
    cmd = cmd_to_run if cmd_to_run is not None else CMD.format(
        rc=reportify_cmd,
        s=story_name,
        r=report_fn
    )
    p = get_process(cmd)
    if p:
        print 'Reportify failed - return code: ', p, 'Try again'
        sleep(1)
        if get_process(cmd):
            # If lack of connection then reportify failes
            print 'Second time - Something went wrong, keep life going on...'
            # raise IOError('Second time - Something went wrong')
    return


def arg_parser():
    parser = ArgumentParser(
        description=__description__,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        '-sn', '--story-name', default=STORY_NAME,
        type=str, help='story name, the folder where report is.(default %s)' % STORY_NAME
    )
    parser.add_argument(
        '-rf', '--report-fn', default=REPORT_FN,
        type=str, help='report filename, must be jupyter notebook.(default %s)' % REPORT_FN
    )
    parser.add_argument(
        '-rc', '--reportify-cmd', default=REPORTIFY_CMD,
        type=str, help='full command: `~/path/to/my/reportify.(default:%s)' % REPORTIFY_CMD
    )
    parser.add_argument(
        '-t', '--time', default=2.5,
        type=float, help='time between two calls of reportify.(default 2.5sec)'
    )
    parser.add_argument(
        '-cmd', '--command', default=None,
        help='`reportify report.ipynb -to /path/proj/report/`'
    )
    args = parser.parse_args()

    # check story folder exists
    if not os.path.isdir('%scode/misc/stories/%s' % (BASE, args.story_name)):
        raise IOError(
            'Story name does not have folder %s in misc' % args.story_name)
    # check report folder within the story exists
    if not os.path.isdir(
        '%scode/misc/stories/%s/report' % (BASE, args.story_name)
    ):
        raise IOError('Story does not have a report folder')
    # check story has a project folder (this is local)
    if not os.path.isdir('%sprojects/%s' % (BASE, args.story_name)):
        raise IOError('Story name does not have folder in projects, create it $ mkdir %sprojects/%s' % (BASE, args.story_name))
    # check jupyter-notebook report exists
    if not os.path.isfile('%scode/misc/stories/%s/report/%s' % (
        BASE, args.story_name, args.report_fn
    )):
        raise IOError('Report `report_name.ipynb` does not exists')
    return args


def main():
    args = arg_parser()
    print 'Html version of report is here (copy/paste into browser)'
    print 'file://%sprojects/%s/report/%s.html' % (
        BASE, args.story_name, args.report_fn.split('.')[0]
    )
    while True:
        run_cmd(
            args.reportify_cmd, args.story_name, args.report_fn, args.command
        )
        sleep(args.time)
    return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Finished. Enjoy your report.'
