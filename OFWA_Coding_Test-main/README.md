# Galamsay Data Analysis and API

This project analyzes data on illegal small-scale mining activities (Galamsay) in Ghana, stores the analysis results in a database, and exposes them via a RESTful API.

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install pandas flask
   ```

3. **Run the data analysis and database setup**
   ```bash
   python data_analysis.py
   python database_setup.py
   ```

4. **Start the Flask API**
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000/api/analysis`

## Testing

Run the test suite using:
```bash
python -m unittest test_app.py
```

## Git Usage

Ensure to make meaningful commit messages and include at least 3 commits in your Git history.

## Submission

Submit a link to the remote Git repository by noon of February 1, 2025. 