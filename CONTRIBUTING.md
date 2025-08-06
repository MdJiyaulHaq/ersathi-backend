# Contributing to erSathi Backend

Thank you for considering contributing to erSathi! This guide will help you understand how to contribute effectively.

## Ground Rules

- Be respectful and inclusive.
- Use clear, descriptive titles and commit messages.
- Follow the code style and structure already used in the project.
- All significant changes should be discussed before implementation (via GitHub issues).

## Prerequisites

Before contributing, make sure you have:

- Docker and Docker Compose installed
- Python 3.12+ (for local testing if not using Docker)
- A GitHub account
- Basic knowledge of Django and REST framework

## Getting Started

1. **Fork the Repository**

   Go to the GitHub repo: https://github.com/MdJiyaulHaq/ersathi-backend and click **Fork**.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/ersathi-backend.git
   cd ersathi-backend
   ```

3. **Create a new branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up the development environment**

   Use Docker (preferred):

   ```bash
   cp .env.example .env
   docker-compose up --build
   ```

   This will start the app at `http://localhost:8000`.

5. **Run Linter and Tests**

   Before pushing any changes:

   ```bash
   docker compose run --rm web sh -c "flake8"
   docker compose run --rm web sh -c "pytest"
   ```

## Writing and Testing Code

- Write clean, readable, and well-documented code.
- Add or update unit tests for new features or bug fixes.(optional but recommended)
- Follow Django best practices and use consistent formatting (we recommend [Black](https://black.readthedocs.io/)).

## Making a Pull Request

⚠️ Please do not push directly to the `main` branch.

All changes must go through Pull Requests from feature branches on your own fork. The `main` branch is protected and requires review before merging.

1. Push your branch:

   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to your fork on GitHub and open a Pull Request (PR) into `main`.

3. Fill in the PR template and describe your changes clearly.

4. Wait for review. Be open to feedback!

## Code of Conduct

We are committed to a welcoming and inclusive environment. Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

## Need Help?

If you're unsure about something, feel free to open an issue or contact the maintainers on the Discord channel.

Happy coding!
