# MyAnimeList (MAL) Grabber
This Package is designed to provide developers with a straightforward way to access [MyAnimeList](https://myanimelist.net/) data programmatically.

⚠️ Note: This project is currently under rapid development. APIs and features might change without notice as we work hard to improve and enhance the package. We encourage you to test and experiment, but be aware of potential breaking changes if you choose to use this package in production.

Table of Contents
- [Features](#features)
- [Packages](#packages)
  - [Installation](#Installation)
  - [Usage](#Usage)
- API (Coming Soon)
  - Endpoints
  - Authentication
  - Example
- [Contributing](#Contributing)
- [License](#License)
- [Disclaimer](#Disclaimer)

## Features

- Fetch anime/manga details based on titles, genres, and more.
- Fetch top/popular/upcoming/airing anime/movies/ova/ona/manga etc.
- Easy-to-use API for integrating MyAnimeList functionality into your projects. (Coming Soon)

## Installation

### For Python
```sh
pip install malgrabber
```
## Usage
```python
from mal import mal

print(mal.topanime())
```
For more detailed documentation, please refer to the Documentation (Coming Soon).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Any form of Contribution are welcomed! If you have any feature suggestions, bug reports, or pull requests, please open an issue or a pull request on GitHub.

## Disclaimer
This package is developed independently and is not affiliated with or endorsed by [MyAnimeList](https://myanimelist.net/).

[![PyPI version](https://badge.fury.io/py/malgrabber.svg)](https://pypi.org/project/mediafiregrabber/) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
