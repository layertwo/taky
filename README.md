# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/layertwo/taky/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                            |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| taky/\_\_init\_\_.py            |        6 |        2 |        0 |        0 |     67% |       7-8 |
| taky/config.py                  |       73 |       41 |       34 |        7 |     38% |53-60, 70-77, 87-88, 94-100, 105, 109-110, 117-134, 137 |
| taky/cot/\_\_init\_\_.py        |        4 |        0 |        0 |        0 |    100% |           |
| taky/cot/\_\_main\_\_.py        |       70 |       70 |        6 |        0 |      0% |     2-118 |
| taky/cot/client.py              |      222 |      115 |       54 |       13 |     45% |47-\>exit, 55, 57-58, 65, 70, 77, 91-104, 113-114, 120-121, 124-130, 140-150, 153-161, 206, 211-215, 226-276, 287, 297, 300-301, 303-\>306, 308-320, 330, 333, 342, 349-358, 390-397 |
| taky/cot/mgmt.py                |       75 |       63 |       24 |        0 |     12% |16-19, 23-24, 27-28, 31-55, 58-79, 82-113 |
| taky/cot/models/\_\_init\_\_.py |        8 |        0 |        0 |        0 |    100% |           |
| taky/cot/models/detail.py       |       32 |        6 |       12 |        4 |     77% |21, 26, 42, 49, 60, 68 |
| taky/cot/models/errors.py       |        1 |        0 |        0 |        0 |    100% |           |
| taky/cot/models/event.py        |       68 |        1 |       20 |        3 |     95% |78-\>75, 90, 105-\>108 |
| taky/cot/models/geochat.py      |       77 |       22 |       16 |        5 |     65% |81, 85-\>87, 91, 102, 103-\>107, 114-161 |
| taky/cot/models/point.py        |       23 |        1 |        0 |        0 |     96% |        25 |
| taky/cot/models/takuser.py      |       91 |        5 |       26 |        6 |     91% |23, 85-86, 102, 108-\>117, 129-\>131, 132, 145-\>155 |
| taky/cot/models/teams.py        |       17 |        0 |        0 |        0 |    100% |           |
| taky/cot/persistence.py         |      152 |       92 |       38 |        6 |     37% |59, 62-69, 82-\>87, 83-\>82, 91, 127, 151-152, 169-170, 173, 192-211, 218-223, 226-232, 235, 238-251, 254, 257-296, 299-306 |
| taky/cot/router.py              |       91 |       28 |       54 |        5 |     63% |38-41, 53, 101-122, 136, 140-\>144, 147, 149, 156-159 |
| taky/cot/server.py              |      219 |      194 |       76 |        0 |      8% |16-36, 41-48, 53-65, 80-91, 97-138, 144-174, 180-191, 197-241, 244-255, 261-266, 272-324, 330-371, 374-376 |
| taky/dps/\_\_init\_\_.py        |       28 |       28 |        6 |        0 |      0% |      1-47 |
| taky/dps/\_\_main\_\_.py        |       93 |       93 |       22 |        0 |      0% |     1-174 |
| taky/dps/views/\_\_init\_\_.py  |        1 |        1 |        0 |        0 |      0% |         1 |
| taky/dps/views/datapackage.py   |       97 |       97 |       20 |        0 |      0% |     1-203 |
| taky/dps/views/index.py         |        8 |        8 |        0 |        0 |      0% |      1-12 |
| taky/dps/views/kml.py           |       15 |       15 |        0 |        0 |      0% |      1-32 |
| taky/dps/views/version.py       |        8 |        8 |        0 |        0 |      0% |      1-12 |
| taky/dps/views/video.py         |       63 |       63 |       20 |        0 |      0% |      1-94 |
| taky/util/\_\_init\_\_.py       |       34 |       30 |       12 |        0 |      9% |12-28, 39-62 |
| taky/util/anc.py                |      145 |      124 |       32 |        0 |     12% |51-67, 78-127, 152-274, 279-282, 285-309, 312-322, 325-338, 341-343, 346-352, 355-365 |
| taky/util/datapackage.py        |       40 |       34 |       18 |        0 |     10% |9-13, 20-53, 61-90 |
| taky/util/stream\_framer.py     |       93 |        0 |       44 |        0 |    100% |           |
| **TOTAL**                       | **1854** | **1141** |  **534** |   **49** | **37%** |           |


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