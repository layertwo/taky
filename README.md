# taky

taky - A simple COT server for ATAK

This is the [layertwo](https://github.com/layertwo/taky) production fork of
[tkuester/taky](https://github.com/tkuester/taky). It addresses upstream stagnation by fixing the
XML parser memory leak, hardening the stream framer, modernizing the packaging, and containerizing
properly.

![python](https://img.shields.io/badge/python-3.11%2B-blue)
![CI](https://github.com/layertwo/taky/actions/workflows/python-tests.yml/badge.svg)
![Coverage](https://raw.githubusercontent.com/layertwo/taky/python-coverage-comment-action-data/badge.svg)

## Features (and anti-Features!)

 * Designed with security in mind!
   * First class SSL support with client keys!
   * Data Package Server requires client keys!
   * XXE protection via defusedxml -- no raw lxml exposure!
   * Does not require root to run!

 * Light weight COT Router and Data Package Server
   * Only ~2k SLOC for the whole shebang!
   * Supports multiple ATAK clients simultaneously! You can see them on the map!
   * Actually somewhat decent CoT routing, with Marti support!
   * Hardened stream framer that handles partial reads and malformed XML without corrupting parser state!
   * Advanced Pythonic implementation of CoT model, with only 5 hours of combined
     industry experience in implementing CoT technology!

 * Simplicity of Design, Use, and Configuration
   * Server shuts down with only one Ctrl+C!
   * Thread safety? Where we're going, we don't need threads!
   * Handy CLI utilities for generating systemd service files and client keys!
   * Advanced usage of synchronous I/O multiplexing avoids `time.sleep`!
   * Stupid fast for no good reason! Routes 1000 packets / second on an old
     Core i5-2500k!

 * Misc
   * Optional redis backed object persistence storage!
   * DPS doesn't have a database! Just plain old file storage!
   * Tested for easy deployment on Ubuntu and CentOS!

Looking for an indepth feature comparison?

## Hardware and Software Requirements

 * Python 3.11 or greater
 * defusedxml 0.7.1 (MIT)
 * python-dateutil (Apache 2.0 / BSD 3-clause)
 * flask (BSD 3-clause)
 * cryptography (Apache 2.0 / BSD 3-clause / PSF)
 * gunicorn (MIT)
 * redis (MIT)

This fork is developed and tested with Python 3.11+ on modern ATAK, WinTAK, and iTAK clients. The
package is available on pip and should run on most modern Linux distros and Docker containers.

taky has minimal hardware requirements, and runs comfortably on small VPS's, embedded systems, and
old desktops. Many users have reported successful usage on older models of RaspberryPi and the
smallest Digital Ocean droplets. If you have at least 128 MB of RAM free, you should be able to run
taky just fine with up to 100 clients.

## Installation

To install the latest release from pip:

```
$ pip install taky
```

To install from source (development build):

```
$ git clone https://github.com/layertwo/taky
$ cd taky
$ pip install .
```

For a development install with test and lint tooling:

```
$ pip install -e ".[dev]"
```

## Usage

Right out of the box, with no configuration, you can build a simple COT server
for you and your friends to play with over TCP!

```
$ taky -h
usage: taky [-h] [-l {debug,info,warning,error,critical}] [-c CFG_FILE] [--version]

Start the taky server

optional arguments:
  -h, --help            show this help message and exit
  -l {debug,info,warning,error,critical}
                        Log verbosity
  -c CFG_FILE           Path to configuration file
  --version             show program's version number and exit

# Run taky on 0.0.0.0:8087
$ taky
INFO:root:taky v1.0
INFO:COTServer:Listening for tcp on :8087
```

## Deploying Taky

Taky has been written with ease of administration in mind. It should be easy to
install, upgrade, build (and run) multiple instances, manage with systemd
scripts, and adhere to standard Linux service organization and package
management. Additionally, there is no tie in to operating systems. This should
be just as easy to setup on Fedora as it is on Ubuntu -- though the
instructions have been written for Ubuntu.

See the README_QUICKSTART.md guide in the `doc/` folder to get up and running!
For more advanced setups, look at the README_DEPLOYMENT.md file!

## Development Status

As far as the "[Unicorn Test Readiness
Level](https://www.granttremblay.com/blog/trls)" goes, `taky` is not a high
heritage space unicorn. We are somewhere between TRL 5 and 6. The horse is
outside, and we're tentatively calling it a unicorn. Users have reported that
`taky` worked well on ANW2C networks, L3Harris radios, passed custom COT
messages without complaint, and even found taky deployments in the field with
coalition forces!

The COT server is the most mature part of the codebase. The layertwo fork has
addressed several stability concerns from the original:

 * The XML parser memory leak has been resolved by replacing lxml with
   defusedxml + stdlib ElementTree. Memory growth under sustained load is
   now negligible.
 * The stream framer has been hardened to handle partial reads, framing
   edge cases, and malformed XML without corrupting server state.
 * Packaging has been modernized: pyproject.toml, ruff, pytest, and
   pytest-asyncio have replaced the old setup.py / tox / unittest stack.

The Data Package server (DPS) is starting to mature, but has not been as
extensively tested. Simple client-to-client and client-to-server transfers seem
to work well, although some features like Video and posting tracks have not
been implemented yet.

All said and done, `taky` is experimental software. You are free to use it as
you see fit, but please take into serious consideration various failure modes,
and craft contingency plans if the service fails, especially if life, wellbeing,
or safety are on the line.

Feel free to checkout the
[milestones](https://github.com/layertwo/taky/milestones) page to see what is
planned for the next version of taky! Pull requests and issues are welcome!

<p align="center">
  <img src="https://raw.githubusercontent.com/layertwo/taky/main/doc/taky.png" alt="taky logo" width="200" />
</p>
