# Dolce Gusto Code Submitter

This project automates the submission of codes on the Nescafe Dolce Gusto website. It uses Python and Selenium to interact with the website, submitting a list of codes and handling retries in case of website unavailability. The project includes automatic download and installation of the appropriate ChromeDriver version based on the installed Chrome browser.

## Features

- Automates the process of submitting codes to the Nescafe Dolce Gusto website.
- Handles retries in case of website unavailability.
- Automatically downloads and installs the appropriate ChromeDriver version.
- Includes support for headless Chrome execution.
- Uses custom user-agent and headers to mimic a real user session.

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver
- Selenium

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/vitornere/dolce-gusto-code-submitter.git
    cd dolce-gusto-code-submitter
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have Google Chrome installed.

## Usage

The `submit_codes.py` script will automate the submission of codes to the Nescafe Dolce Gusto website.

```sh
python submit_codes.py
```

### Configuration

- **HEADLESS**: Set this to `True` to run the script in headless mode, or `False` to run with a visible UI for debugging.

- **MAX_RETRIES**: The number of times the script will retry if the website is unavailable.

- **RETRY_DELAY**: The delay (in seconds) between retries when the website is unavailable.

- **COOKIES_FILE**: Path to the JSON file containing the cookies needed for the session.

- **CODES**: A list of codes to be submitted on the website.

- **INPUT_ID**: The ID of the form input element where the code will be entered.

- **SUBMIT_CLASS**: The class name of the submit button to click after entering the code.

- **SUCCESS_CLASS**: The class name of the element that appears when a code is successfully submitted.

- **USER_AGENT**: The user-agent string to be used by the browser to mimic a real user session.

- **CUSTOM_HEADERS**: A list of custom headers to be added to the browser requests. These headers help mimic a real user session.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.
