# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/layertwo/taky/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                            |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| taky/\_\_init\_\_.py            |        6 |        2 |        0 |        0 |     67% |       7-8 |
| taky/config.py                  |       73 |       41 |       34 |        7 |     38% |56-63, 73-80, 90-91, 97-103, 108, 112-113, 120-137, 140 |
| taky/cot/\_\_init\_\_.py        |        4 |        0 |        0 |        0 |    100% |           |
| taky/cot/\_\_main\_\_.py        |       70 |       70 |        6 |        0 |      0% |     2-118 |
| taky/cot/client.py              |      222 |      115 |       54 |       13 |     45% |47-\>exit, 55, 57-58, 65, 70, 77, 91-104, 113-114, 120-121, 124-130, 140-150, 153-161, 206, 211-215, 226-276, 287, 297, 300-301, 303-\>306, 308-320, 330, 333, 342, 349-358, 390-397 |
| taky/cot/mgmt.py                |       75 |       63 |       24 |        0 |     12% |16-19, 23-24, 27-28, 31-55, 58-79, 82-113 |
| taky/cot/models/\_\_init\_\_.py |        8 |        0 |        0 |        0 |    100% |           |
| taky/cot/models/detail.py       |       33 |        8 |       12 |        6 |     69% |23, 28, 32, 44, 48, 51, 62, 70 |
| taky/cot/models/errors.py       |        1 |        0 |        0 |        0 |    100% |           |
| taky/cot/models/event.py        |       72 |        1 |       20 |        3 |     96% |64-\>61, 76, 101-\>104 |
| taky/cot/models/geochat.py      |       70 |       20 |       14 |        5 |     65% |74, 78-\>80, 84, 91, 92-\>95, 110-152 |
| taky/cot/models/point.py        |       24 |        1 |        0 |        0 |     96% |        26 |
| taky/cot/models/takuser.py      |       95 |        5 |       24 |        5 |     92% |23, 86-87, 111, 117-\>126, 141, 154-\>164 |
| taky/cot/models/teams.py        |       17 |        0 |        0 |        0 |    100% |           |
| taky/cot/persistence.py         |      152 |       92 |       38 |        6 |     37% |59, 62-69, 82-\>87, 83-\>82, 91, 127, 151-152, 169-170, 173, 192-211, 218-223, 226-232, 235, 238-251, 254, 257-296, 299-306 |
| taky/cot/router.py              |       92 |       28 |       54 |        5 |     64% |39-42, 54, 102-123, 137, 141-\>147, 150, 152, 159-162 |
| taky/cot/server.py              |      219 |      194 |       76 |        0 |      8% |16-36, 41-48, 53-65, 80-91, 97-138, 144-174, 180-191, 197-241, 244-255, 261-266, 272-324, 330-371, 374-376 |
| taky/db.py                      |       28 |       28 |       10 |        0 |      0% |      1-58 |
| taky/dps/\_\_init\_\_.py        |       28 |       28 |        6 |        0 |      0% |      1-47 |
| taky/dps/\_\_main\_\_.py        |       93 |       93 |       22 |        0 |      0% |     1-174 |
| taky/dps/views/\_\_init\_\_.py  |        1 |        1 |        0 |        0 |      0% |         1 |
| taky/dps/views/datapackage.py   |       97 |       97 |       20 |        0 |      0% |     1-203 |
| taky/dps/views/index.py         |        8 |        8 |        0 |        0 |      0% |      1-12 |
| taky/dps/views/kml.py           |       15 |       15 |        0 |        0 |      0% |      1-32 |
| taky/dps/views/version.py       |        8 |        8 |        0 |        0 |      0% |      1-12 |
| taky/dps/views/video.py         |       63 |       63 |       20 |        0 |      0% |      1-94 |
| taky/models/\_\_init\_\_.py     |        6 |        0 |        0 |        0 |    100% |           |
| taky/models/base.py             |        5 |        0 |        0 |        0 |    100% |           |
| taky/models/cot\_history.py     |       13 |        0 |        0 |        0 |    100% |           |
| taky/models/issued\_certs.py    |       11 |        0 |        0 |        0 |    100% |           |
| taky/models/packages.py         |       17 |        0 |        0 |        0 |    100% |           |
| taky/models/users.py            |       15 |        0 |        0 |        0 |    100% |           |
| taky/util/\_\_init\_\_.py       |       34 |       30 |       12 |        0 |      9% |12-28, 39-62 |
| taky/util/anc.py                |      145 |      124 |       32 |        0 |     12% |51-67, 78-127, 152-274, 279-282, 285-309, 312-322, 325-338, 341-343, 346-352, 355-365 |
| taky/util/datapackage.py        |       40 |       34 |       18 |        0 |     10% |9-13, 20-53, 61-90 |
| taky/util/stream\_framer.py     |       93 |        0 |       44 |        0 |    100% |           |
| **TOTAL**                       | **1953** | **1169** |  **540** |   **50** | **38%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/layertwo/taky/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/layertwo/taky/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/layertwo/taky/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/layertwo/taky/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Flayertwo%2Ftaky%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/layertwo/taky/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.