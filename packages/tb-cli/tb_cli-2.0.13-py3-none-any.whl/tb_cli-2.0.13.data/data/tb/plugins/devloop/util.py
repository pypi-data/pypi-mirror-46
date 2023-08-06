from __future__ import print_function

import json
import re
from datetime import datetime

import dateutil.parser
import dateutil.parser
from blessings import Terminal
from tb import ColoredTerminal

HAS_JSON = re.compile(r'^(.*?)(\{.*"@?time(?:stamp)?".*\})')
LOCAL_LINE = re.compile(r'(.*) (DEBUG|INFO|WARN|ERROR|FATAL)\s+\[(.*)\] (.*)')

colors = Terminal()


def print_local_line(term: ColoredTerminal, line):
    line = line.strip()

    # Looks for json inside a docker_compose line
    m = HAS_JSON.match(line)
    if m:
        prefix = m.group(1)
        line = m.group(2)
        term.print_ansi(prefix, end='')
        print_json_lines(term, [line])
        return

    m = LOCAL_LINE.search(line)
    if m:
        c = level_to_color(m.group(2))
        ansi_line = "{} {} [{}] {}".format(m.group(1), c(m.group(2)), c(m.group(3)), c(m.group(4)))
        term.print_ansi(ansi_line)
    else:
        term.print_ansi("{}".format(line))


def print_json_line(term: ColoredTerminal, ts, data, min_level='debug'):
    trace_id = data.get('traceId', data.get('request_id', data.get('dd.trace_id', '')))
    msg = data.get('message', '')
    if isinstance(msg, dict):
        msg = json.dumps(msg)
    else:
        msg = msg  # .encode('utf8')
    level = data.get('level', 'INFO')
    min_level = min_level.upper()
    if min_level == 'ERROR' and level in ('DEBUG', 'INFO', 'WARN'):
        return
    elif min_level == 'WARN' and level in ('DEBUG', 'INFO'):
        return
    elif min_level == 'INFO' and level == 'DEBUG':
        return

    role = data.get('m', {}).get('g', '?')
    container = data.get('micros_container', '?')
    # if msg.startswith('{'):
    #     print(colors.red("weird line: {}".format(line)))
    #     print(colors.red("JSON: {}".format(data)))
    color = None
    if msg.startswith("=====> New request"):
        color = colors.blue
    if msg.startswith("=====> Request complete"):
        color = colors.blue
    if color is None:
        color = level_to_color(level)
    try:
        ansi_line = format_line(role="{}:{}".format(role, container),
                                instance=data.get('ec2', {}).get('id', '?'),
                                time=ts,
                                level=color(colors.bold(level)),
                                msg=color(msg),
                                trace=trace_id,
                                color=color,
                                stacktrace=data.get('stack_trace',
                                                    data.get('exc_info', '')))
        term.print_ansi(ansi_line)
    except Exception as e:
        term.print_ansi("err: {}".format(e))
        term.print_ansi(data)


def print_json_lines(term: ColoredTerminal, line_iterator, tag=None, min_level='debug'):
    for line in line_iterator:
        data = line_to_json(term, line)
        if not data:
            continue

        if tag and data.get('m', {}).get('t', '') != tag:
            continue

        print_json_line(term, data.get('timestamp', data.get('@timestamp', data.get('time'))), data,
                        min_level=min_level)


def line_to_json(term: ColoredTerminal, line):
    line = line.strip()
    if not line:
        return

    try:
        return json.loads(line)
    except Exception as e:
        term.print_ansi(line)


def format_line(role, instance, time, level, msg, trace, color, stacktrace):
    if time is not None:
        if not isinstance(time, datetime):
            time = dateutil.parser.parse(time)
        time = time.strftime('%H:%M:%S.%f')[:-3]
    return "{time} {t.magenta}[{role}:{instance}] ({trace}) {level} {msg}{stacktrace}".format(
        t=colors,
        instance=instance,
        role=role,
        time=colors.green(time),
        level=color(colors.bold(level)),
        msg=color(msg),
        trace=trace,
        color=color,
        stacktrace='' if not stacktrace else '\n{}'.format(colors.bold_red(stacktrace)))


def level_to_color(level):
    if level == "DEBUG":
        color = colors.bold_black
    elif level == "INFO":
        color = lambda c: colors.normal + c + colors.normal
    elif level == "WARN" or "WARNING":
        color = colors.yellow_on_black
    elif level == "ERROR":
        color = colors.red
    elif level == "FATAL":
        color = colors.white_on_red
    else:
        color = lambda c: colors.normal + c + colors.normal
    return color
