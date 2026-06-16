# Urban Routes - UI Automation with Selenium + PyTest

This project contains automated UI tests created during the TripleTen QA Engineer Program.

## Project goal

Automate key user flows in the Urban Routes web application using Python, PyTest, and Selenium WebDriver.

## What is tested

* Route setup
* Plan selection
* Phone number flow
* Payment method flow
* Driver message/comments
* Order submission flow

## Tech stack

* Python
* PyTest
* Selenium WebDriver
* Page Object Model basics
* Git/GitHub

## Project structure

```text
.
├── data.example.py
├── helpers.py
├── main.py
├── pages.py
├── requirements.txt
└── selenium.downloadtest.py
```

## How to run the tests

1. Clone this repository:

```bash
git clone https://github.com/biancogoncalvesmoreira25-bit/urban-routes-ui-automation-selenium-pytest.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your local test data file:

For macOS/Linux:

```bash
cp data.example.py data.py
```

For Windows:

```bash
copy data.example.py data.py
```

4. Update `data.py` with your local test environment values.

5. Run the tests:

```bash
pytest -q
```

## Notes

This is a portfolio version of a TripleTen QA project. Sensitive or environment-specific data is not included in this repository.

Use `data.example.py` as a template to create your local `data.py` file before running the tests.

The original test environment may not be publicly available, so this repository is mainly intended to demonstrate the test automation structure, Selenium/PyTest usage, and QA documentation practices.
