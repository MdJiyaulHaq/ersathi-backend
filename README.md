# erSathi Backend

erSathi is a comprehensive backend system built with Django and Django REST framework, designed to manage educational assessments, user progress tracking, and gamification features. The system provides a robust API for integrating with frontend applications.

## Project Overview

This project provides the following key features:

- User authentication and authorization
- Exam/Assessment management system
- Study materials management
- Progress tracking for students
- Gamification elements (badges and likes)
- Tagging system for organizing content
- Discipline-based content organization
- Question bank management

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository:

```bash
git clone [your-repository-url]
cd ersathi-backend
```

2. Create a virtual environment and install dependencies:

````bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

3. Configure your environment variables:
- Copy `.env.example` to `.env` and update the settings as needed

4. Run migrations:
```bash
python manage.py migrate
````

5. Start the development server:

```bash
python manage.py runserver
```

### Docker Setup

1. Build the Docker image:

```bash
docker-compose build
```

2. Start the containers:

```bash
docker-compose up
```

The application will be available at `http://localhost:8000`

## Project Structure

The project is organized into several Django apps:

- **core**: Core user models and authentication
- **assessments**: Exam and assessment management
- **disciplines**: Discipline-based content organization
- **gamification**: Badge and achievement system
- **likes**: Voting system for content
- **progress**: Student progress tracking
- **questions**: Question bank management
- **study_materials**: Study materials and resources
- **subjects**: Subject management
- **tags**: Tagging system

## Features

### Users & Authentication

- User registration and login
- Role-based access control
- Student and educator profiles

### Exams & Assessments

- Create and manage exams
- Multiple question types support
- Exam attempts and results tracking

### Study Materials

- Upload and manage study resources
- Organize by subjects and disciplines
- Access control for materials

### Progress Tracking

- Track student progress
- Generate progress reports
- Set learning goals

### Gamification

- Earn badges based on achievements
- Leaderboard system
- Points system

### API Documentation

The API documentation is automatically generated using drf-yasg and can be accessed at:

```
http://localhost:8000/api/docs/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please contact the maintainers before starting any significant work to discuss your plans. Token will be created for you to use in the development environment. Whoever wants to work on the feature will have a token.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
