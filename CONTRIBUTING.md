# Contributing to Botsy

We welcome contributions to the Botsy information scraping framework! Here's how you can help:

## Ways to Contribute

1. **Add New Scrapers**: Create scrapers for new categories or improve existing ones
2. **Improve APIs**: Add support for new free APIs in existing categories
3. **Documentation**: Improve documentation or add tutorials
4. **Bug Fixes**: Fix bugs and improve error handling
5. **Testing**: Add tests and improve code coverage

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-scraper`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## Adding a New Scraper

1. Create a new directory in `scrapers/` for your category
2. Implement a scraper class inheriting from `BaseScraper`
3. Add the scraper to the main orchestrator
4. Update the configuration
5. Add documentation

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and small

## API Guidelines

- Only use free APIs or those with generous free tiers
- Always respect rate limits and terms of service
- Include proper error handling and logging
- Document API limitations in the scraper

## Testing

- Add unit tests for new scrapers
- Test error conditions and edge cases
- Ensure scrapers handle API failures gracefully

## Documentation

- Update README.md if adding new categories
- Add API documentation for new tools
- Update the GitHub Pages site if needed

## Questions?

Open an issue for questions or discussion about contributions.