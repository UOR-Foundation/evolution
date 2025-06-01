# Contributing to PrimeOS

Thank you for taking the time to contribute! This project welcomes bug reports, feature requests, and pull requests.

## Bug Reports

* Search the issue tracker to see if your issue has already been reported.
* If not, open a new issue with a clear title and description.
* Include steps to reproduce the problem and any relevant logs or screenshots.

## Feature Requests

* Use the issue tracker to propose new features.
* Explain the motivation for the feature and how it will improve the project.
* If you have an implementation in mind, feel free to open a pull request directly.

## Development Setup

1. Clone the repository and navigate into the project directory.
2. Create a Python 3.7+ virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install Flask
   ```
4. Generate the UOR program:
   ```bash
   python generate_goal_seeker_uor.py [--output <path>]
   ```
5. Run the backend server:
   ```bash
   python backend/app.py
   ```
6. Open your browser to `http://127.0.0.1:5000/` to access the frontend.

Pull requests should target the `main` branch and be focused on a single change or feature. Please ensure `git status` shows a clean working tree before submitting.
