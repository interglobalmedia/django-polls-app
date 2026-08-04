# Official Django Polls App

A Django Polls application built by following Django's own official Polls
tutorial from the ground up. The tutorial is maintained by the Django
developers themselves, and this build is structured as a set of reusable
apps rather than a single monolithic project.

## What's included

- Poll models (`Question` and `Choice`) and the database schema behind them
- A registered, customized Django admin interface for managing polls
- Views and namespaced URLconfs for the index, detail, and results pages
- Templates for browsing and voting on polls
- A voting form with validation
- An automated test suite covering models and views
- Static files wired up for local development
- The Django Debug Toolbar for inspecting requests in the browser
- Code quality enforced with flake8, Black, and djLint, run automatically
  through pre-commit hooks

## Running the application

Clone the repository and `cd` into it:

```shell
git clone https://github.com/interglobalmedia/django-polls-app.git
cd django-polls-app
```

Create and activate a virtual environment:

```shell
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```shell
pip install -r requirements.txt
```

Apply migrations and create a superuser so you can access the admin
interface:

```shell
python manage.py migrate
python manage.py createsuperuser
```

Run the development server:

```shell
python manage.py runserver
```

Visit `http://127.0.0.1:8000/polls/` for the app itself, or
`http://127.0.0.1:8000/admin/` to manage polls through the admin interface.

To run the test suite:

```shell
python manage.py test
```

## Code quality

This project uses [flake8](https://flake8.pycqa.org/), [Black](https://black.readthedocs.io/),
and [djLint](https://www.djlint.com/) to keep Python and template code
consistent, wired up through pre-commit hooks. After installing
dependencies, set up the hooks with:

```shell
pre-commit install
```

## Related resources

For the full walkthrough behind this project, see the companion series,
[Creating the official Django Polls app](https://www.mariadcampbell.com/blog/creating-the-official-django-polls-app-table-of-contents),
which breaks the build down into eight parts from initial setup through
testing, static files, and next steps.
