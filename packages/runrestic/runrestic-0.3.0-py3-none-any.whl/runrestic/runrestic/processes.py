import logging
import subprocess
import sys

logger = logging.getLogger(__name__)


def run_piping_process(firstcmd, secondcmd):
    # logger.debug(firstcmd)
    # logger.debug(secondcmd)
    ps = subprocess.Popen(firstcmd.split(" "), stdout=subprocess.PIPE)

    try:
        output = subprocess.check_output(secondcmd, stdin=ps.stdout, stderr=subprocess.STDOUT, universal_newlines=True)
        ps.wait()
        process_rc = 1 if 'error:' in output else 0
        logger.debug(output)
    except subprocess.CalledProcessError as e:
        if 'Is there a repository at the following location?' in e.output:
            logger.error("\nIt seems like the repo is not initialized. Run `runrestic init`.")
            sys.exit(1)
        output = e.output
        process_rc = e.returncode
        logger.error(output)
    return output, process_rc
