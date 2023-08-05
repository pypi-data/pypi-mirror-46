import sys

from .console_calendar import main

if __name__ == '__main__':
    try:
        sys.exit(main())
    except (KeyboardInterrupt, SystemExit):
        pass
