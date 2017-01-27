from subprocess import check_output
import sys
import logging

from ob_pipelines.s3 import s3args

logger = logging.getLogger('ob-pipelines')


@s3args
def sync_and_run(*cmds):
    logger.info('Running:\n{}'.format(' '.join(cmds)))
    print('Running:\n{}'.format(' '.join(cmds)))
    check_output(cmds)


if __name__ == '__main__':
	args = sys.argv[1:]
	sync_and_run(*args)
