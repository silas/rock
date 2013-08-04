Rock Dev
========

This is the rock development environment.

## Getting Started

 1. Clone the dev repository

        git clone git://github.com/rockstack/dev.git rock

 1. Switch to it

        cd rock

 1. Run the setup script

        ./misc/setup

 1. Setup your env

        export PATH="$( pwd )/rock/scripts:${PATH}"
        export PYTHONPATH="$( pwd )/rock:${PYTHONPATH}"

 1. Start hacking

## Tips

Run a command in all project directories

    ./misc/project git status

## License

This work is licensed under the MIT License (see the LICENSE file).
