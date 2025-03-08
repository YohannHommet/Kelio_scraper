# Python Job Scraper Project Guidelines

## Commands
- Run scraper: `python src/core/scraper.py`
- Run web interface: `python src/app.py`
- Run tests: `python -m unittest discover tests`
- Run specific test: `python -m unittest tests/unit/test_scraper.py`
- View logs: `cat logs/scraper.log | tail -n 10`
- Docker: `docker-compose up -d`, `docker-compose logs -f scraper`

## Code Style Guidelines
- **Imports**: Standard lib → Third-party → Local modules, alphabetically ordered
- **Formatting**: Use consistent indentation (4 spaces), max line length 100
- **Functions**: Use docstrings for all functions, methods and classes
- **Error Handling**: Use try/except with specific exceptions, log errors
- **Types**: Follow consistent naming: PascalCase for classes, snake_case for variables
- **Logging**: Use loguru for all logging, avoid print statements

## Architecture
- Modular design: core/ (scraper, data_handler, notifier, ai_formatter)
- Separation of concerns: data handling, scraping, notifications
- Tests: Unit tests in tests/unit/, integration tests in tests/integration/