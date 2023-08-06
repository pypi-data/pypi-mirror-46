import os
import time

from loguru import logger

from ddwrt_conn_tracker.ddwrt import RouterSSH
from ddwrt_conn_tracker.utils import start_args

env = os.environ


def track(host=None, port=None, user=None, password=None):
    from ddwrt_conn_tracker.models import EventModel

    if any((host, port, user, password)):
        router = RouterSSH(host=host, port=port, user=user, password=password)

    elif not start_args:
        try:
            router = RouterSSH(
                    host=env['DDWRT_HOST'],
                    port=env['DDWRT_PORT'],
                    user=env['DDWRT_USER'],
                    password=env['DDWRT_PASSWORD']
                    )
        except KeyError:
            logger.error(
                    f'Provide connection arguments either in environment variables DDWRT_HOST, DDWRT_PORT, DDWRT_USER, '
                    f'DDWRT_PASSWORD or as '
                    f'command line arguments python tracker.py --host (-H) HOST --port (-p) PORT --user (-u) USER '
                    f'--pwd (-P) PASSWORD')
            exit(1)

    else:
        router = RouterSSH(**start_args)
    logger.info(f'Starting DD-WRT connection logger')

    sleep_time = env.get('DDWRT_SLEEP', 1)

    logger.info(f'Getting connections and updating database every {sleep_time}s. Press CTRL+C to exit.')
    while True:
        active_connections = router.get_active_connections()
        EventModel.update(active_connections)
        time.sleep(sleep_time)


if __name__ == '__main__':
    try:
        track()
    except KeyboardInterrupt:
        logger.info(f'Exiting. Thank you for using DD-WRT Connection Tracker')
