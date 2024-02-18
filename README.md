## Getting Started
 
### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setting up the Virtual Environment

```bash
# Creating the virtual environment
python -m venv venv

# Activating the virtual environment
venv\Scripts\activate

# Installing all the packages through requirement.txt
pip install -r requirements.txt

# All packages that are being used in the project
1. `aniso8601==9.0.1`: Library for parsing and formatting ISO 8601 dates and times.
2. `APScheduler==3.10.4`: Advanced scheduler for Python applications.
3. `bcrypt==4.1.2`: Library for hashing passwords using the bcrypt hashing algorithm.
4. `blinker==1.7.0`: Provides a simple object-oriented interface for event-driven programming.
5. `certifi==2023.11.17`: Certificates for validating the trustworthiness of SSL/TLS connections.
6. `cffi==1.16.0`: Foreign Function Interface for calling C functions from Python.
7. `charset-normalizer==3.3.2`: Charset encoding normalization library.
8. `click==8.1.7`: A package for creating command-line interfaces.
9. `colorama==0.4.6`: Cross-platform colored terminal text.
10. `cryptography==41.0.7`: Library for secure communication and cryptography.
11. `Flask==3.0.0`: Micro web framework for Python.
12. `Flask-Bcrypt==1.0.1`: Flask extension for password hashing using bcrypt.
13. `Flask-Cors==4.0.0`: Flask extension for handling Cross-Origin Resource Sharing (CORS).
14. `Flask-JWT-Extended==4.6.0`: Extended JWT support for Flask applications.
15. `Flask-RESTful==0.3.10`: Extension for quickly building REST APIs with Flask.
16. `Flask-SQLAlchemy==3.1.1`: SQLAlchemy integration for Flask applications.
17. `fuzzywuzzy==0.18.0`: Fuzzy string matching library.
18. `greenlet==3.0.3`: Lightweight concurrency library.
19. `idna==3.6`: Internationalized Domain Names in Applications (IDNA) support library.
20. `iniconfig==2.0.0`: Library for parsing .ini-style configuration files.
21. `itsdangerous==2.1.2`: Library for creating and validating signed tokens.
22. `Jinja2==3.1.2`: Template engine for Python.
23. `Levenshtein==0.23.0`: C extension for efficient Levenshtein distance calculation.
24. `MarkupSafe==2.1.3`: Library for escaping HTML or XML characters.
25. `mysqlclient==2.2.1`: MySQL database connector for Python.
26. `packaging==23.2`: Core utilities for Python package management.
27. `pillow==10.2.0`: Python Imaging Library (PIL) fork for image processing.
28. `pluggy==1.3.0`: Plugin management library.
29. `pycparser==2.21`: C parser and AST generator for Python.
30. `PyJWT==2.8.0`: JSON Web Token implementation for Python.
31. `pypng==0.20220715.0`: Pure Python PNG image encoder/decoder.
32. `pytest==7.4.3`: A testing framework for Python.
33. `python-dotenv==1.0.0`: Reads the key-value pair from a .env file and adds them to environment variables.
34. `python-Levenshtein==0.23.0`: Python extension for computing string similarities and edit distances.
35. `pytz==2023.3.post1`: World timezone definitions for Python.
36. `qrcode==7.4.2`: QR code generation library.
37. `rapidfuzz==3.6.0`: Fast string matching and fuzzy text searching library.
38. `requests==2.31.0`: HTTP library for making requests.
39. `six==1.16.0`: Python 2 and 3 compatibility library.
40. `SQLAlchemy==2.0.23`: SQL toolkit and Object-Relational Mapping (ORM) for Python.
41. `typing_extensions==4.9.0`: Backport of the standard library `typing` module for Python 3.5 and 3.6.
42. `tzdata==2023.4`: Timezone database for Python.
43. `tzlocal==5.2`: Library to provide cross-platform, timezone-aware date-time objects.
44. `urllib3==2.1.0`: HTTP library for handling URLs.
45. `Werkzeug==3.0.1`: A comprehensive WSGI web application library.


# .env file configuration
FLASK_SECRET_KEY=: Secret key for Flask application.
FLASK_DEBUG=: Enable Flask debug mode for development.
FLASK_SQLALCHEMY_DATABASE_URI=: SQLAlchemy database URI for Flask application.
FLASK_SQLALCHEMY_ECHO=: Enable SQLAlchemy query logging.
JWT_SECRET_KEY=: Secret key for JWT authentication.
FROM_EMAIL=: Placeholder for the sender's email address.
SMTP_ENDPOINT=: Placeholder for the SMTP server endpoint.
SMTP_USER=: Placeholder for the SMTP server username.
SMTP_PASSWORD=: Placeholder for the SMTP server password.


### Run the application
python run.py




