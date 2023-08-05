from pysyte.bash import cmnds


class NoTerminalAvailable(NotImplementedError):
    pass


def _tput(tput_command):
    command = 'tput %s' % tput_command
    status, output = cmnds.getstatusoutput(command)
    if status:
        if 'No value for $TERM' in output:
            raise NoTerminalAvailable(output)
        raise NotImplementedError(output)
    if not output:
        return 0
    try:
        return int(output) - 1
    except TypeError:
        return 0


def screen_width():
    return _tput('cols')


def screen_height():
    return _tput('lines')
