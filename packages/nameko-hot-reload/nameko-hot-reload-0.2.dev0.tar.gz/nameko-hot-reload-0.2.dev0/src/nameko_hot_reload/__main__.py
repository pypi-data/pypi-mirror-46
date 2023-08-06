import sys
from nameko_hot_reload.cli.main import main

# allow running nameko_hot_reload with `python -m nameko_hot_reload <args>`
if __name__ == '__main__':
    sys.exit(main())
