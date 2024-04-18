# Click Counter Application

## Overview

This application processes click data to compute the number of clicks received for URLs shortened using a specific service in the year 2021. The program reads from a `.csv` file containing mappings of long URLs to their shortened versions, and a `.json` file containing click events, then outputs the number of clicks per URL in a sorted format.

## Dependencies

This project requires Python 3.8 or later. Below is a list of Python libraries which would be needed:

- `numpy`
- `pandas`
- `pytest` for running tests.

### Installing Dependencies

The required packages can be installed using the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

The application can be run using the following command:

```bash
python main.py
```

## Output:

The application outputs the following to the terminal:

```
[{'https://youtube.com/': 557}, {'https://twitter.com/': 512}, {'https://reddit.com/': 510}, {'https://github.com/': 497}, {'https://linkedin.com/': 496}, {'https://google.com/': 492}]
```

## Running Tests

The project utilizes `pytest` as a testing framework, chosen for its simplicity and robustness, allowing for more readable tests and a rich set of features to effectively test the application. The tests have been compiled in the `test_click_counter.py` file.

The tests can be executed using the command :

```bash
pytest
```

## Design Decisions

### Modular Functions:
Functions are modular and serve single responsibilities (e.g., `loading data`, `filtering data`, `counting clicks`), making the codebase easier to test and extend.

### Error Handling:
Significant Error handling schemes have been implemented to manage common issues such as file not found errors, which could be common as the application expects file paths to be correct and files to be formatted correctly.

### Logging:

Logs are generated in a file of the following format : `LOGS/LOGS_{timestamp}.txt`

which is located in the `LOGS` folder. This helps in debugging and provides an audit trail of operations performed by the script.


