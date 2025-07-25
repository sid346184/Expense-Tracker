# Expense Tracker

A Django-based web application for tracking personal expenses, calculating monthly expenses with interest, and managing financial records.

## Features

- User registration and authentication
- Add and track expenses
- Calculate monthly expenses with interest rates
- View expense history and summaries
- Secure database storage using PostgreSQL
- Responsive user interface

## Technologies Used

- Django 5.2.4
- Python
- PostgreSQL (via Supabase)
- HTML/CSS
- python-dotenv for environment management

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/sid346184/Expense-Tracker.git
   cd Expense-Tracker
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django python-dotenv dj-database-url psycopg2-binary
   ```

4. Create a `.env` file in the project root and add your database configuration:
   ```
   DATABASE_URL=your_postgres_database_url
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

## Usage

1. Register a new account or login with existing credentials
2. Add new expenses with details like amount, date, and description
3. View your expense history
4. Calculate monthly expenses with or without interest

## Project Structure

```
ExpenseTracker/
├── exp_tracker/            # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── urls.py           # URL routing
│   ├── static/           # Static files (CSS, JS)
│   └── templates/        # HTML templates
├── ExpenseTracker/        # Project configuration
│   ├── settings.py       # Project settings
│   └── urls.py          # Project URL routing
└── manage.py             # Django management script
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request



