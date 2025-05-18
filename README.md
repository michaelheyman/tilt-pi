# tilt-pi

A Python client for interacting with the Tilt Pi API.

This library provides a Python interface to the Tilt Pi, allowing you to retrieve data from Tilt
Hydrometers connected to it.

The Tilt Pi is a Raspberry Pi-based device that can read data from Tilt Hydrometers and broadcast it
over the network. The Tilt Pi can be used to monitor the fermentation of beer, wine, cider, and
other beverages.

The benefit of the Tilt Pi is that it can be placed in a location with better reception than the
Tilt Hydrometer itself, allowing for more reliable data collection.

## Installation

You can install `tilt-pi` using pip:

```bash
pip install tilt-pi
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

To set up for development:

1. Clone the repository.
2. Install Poetry if you haven't already.
3. Run `poetry install --with dev` to install dependencies, including development tools.

### Linting and Formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.
You can run Ruff with:

```bash
poetry run ruff check .
poetry run ruff format .
```

### Testing

Tests are written using [pytest](https://pytest.org/).
You can run tests with:

```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
