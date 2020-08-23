import logging
import logging.config

logging.config.fileConfig("./etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('jiragantt')

def main() -> str :
    logger.debug('Hello, world.')
    return 'Hello, world.'

if __name__=='__main__':
    print(main())
