# LOAS Automated Laundry Booking Bot

## Project Overview
This project automates the laundry booking process for LOAS housing residents. It uses Selenium WebDriver to interact with the LOAS booking system, enabling users to schedule recurring laundry reservations across multiple dates with a single execution.

## Key Features & Benefits
*   **Recurring Bookings:** Book washing machines and dryers for multiple weeks in advance with a single script execution.
*   **Multi-Machine Support:** Reserve time slots across up to 4 washing machines and 2 dryers simultaneously.
*   **Flexible Scheduling:** Select specific time slots (in 30-minute intervals from 07:00 to 21:00) for each machine.
*   **Date Range Selection:** Choose a recurring day of the week and specify the booking period (up to 1 year in advance).
*   **Interactive Interface:** User-friendly command-line interface with clear prompts and confirmation steps.
*   **Session Management:** Maintains browser session across multiple date bookings for efficiency.

## Prerequisites & Dependencies

### Software Requirements
*   **Python 3.6+:** Ensure Python is installed on your system. Verify with `python --version`.
*   **Google Chrome Browser:** The script automates Chrome to perform bookings.
*   **ChromeDriver:** Required for Selenium to control Chrome.

### Python Libraries
*   **Selenium:** Web browser automation library. Install using `pip install selenium`.

### ChromeDriver Setup
**Important:** The script expects ChromeDriver to be located at:
```
C:\WebDriver\chromedriver-win64\chromedriver.exe
```

To set this up:
1.  Check your Chrome version: Navigate to `chrome://settings/help` in your browser.
2.  Download the matching ChromeDriver version from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
3.  Extract the downloaded archive.
4.  Create the directory `C:\WebDriver\chromedriver-win64\` on your system.
5.  Place the `chromedriver.exe` executable in this directory.

**Alternative:** If you prefer a different location, modify line 226 in `script.py`:
```python
service = Service("YOUR_CUSTOM_PATH\\chromedriver.exe")
```

## Installation & Setup Instructions

1.  **Clone the repository:**
```bash
    git clone https://github.com/aahmad-1/LOAS-Automated-Laundry-Booking.git
    cd LOAS-Automated-Laundry-Booking
```

2.  **Install required dependencies:**
```bash
    pip install selenium
```

3.  **Verify ChromeDriver installation:**
    Ensure `chromedriver.exe` is located at `C:\WebDriver\chromedriver-win64\chromedriver.exe` as described in the prerequisites section.

## Usage Instructions

### Running the Script

1.  **Execute the script:**
```bash
    python script.py
```

2.  **Provide login credentials:**
```
    === LOAS Laundry Booking Bot ===
    Enter your email: your_email@example.com
    Enter your password: your_password
```

3.  **Select machines and time slots:**
    The script will display a menu to select machines and add time slots:
```
    Select a machine to add time slots:
    a. Washing Machine 1
    b. Washing Machine 2
    c. Washing Machine 3
    d. Washing Machine 4
    e. Dryer 1
    f. Dryer 2
    g. Continue to date selection
    h. Clear all selections
```

4.  **Enter time slots:**
    When you select a machine (options a-f), enter your desired time slots in 24-hour format:
```
    Time slots: 08:00, 10:30, 14:00
```
    Valid times range from 07:00 to 21:00 in 30-minute intervals (07:00, 07:30, 08:00, etc.).

5.  **Configure booking dates:**
    After selecting option 'g', choose:
    *   The day of the week for recurring bookings (e.g., every Monday)
    *   The last date you want to book (must fall on your selected day of the week)
    
    The script will calculate all dates in the range and display them for confirmation.

6.  **Confirm and execute:**
    Review the summary of bookings and confirm to proceed. The script will:
    *   Log into the LOAS booking system
    *   Navigate to each date in sequence
    *   Attempt to book all selected time slots
    *   Provide real-time status updates for each booking attempt

### Example Workflow
```
=== LOAS Laundry Booking Bot ===
Enter your email: john.doe@example.com
Enter your password: ********

Select a machine to add time slots:
> a

Enter time slots for Washing Machine 1: 08:00, 10:00, 12:00
Successfully added 3 slot(s) for Washing Machine 1

Select a machine to add time slots:
> e

Enter time slots for Dryer 1: 09:00, 11:00
Successfully added 2 slot(s) for Dryer 1

Select a machine to add time slots:
> g

Select the day of the week: 1 (Monday)
Last booking date: 2025-12-29

Total Mondays to book: 9
Proceed with booking? yes

[Browser automation begins...]
```

## Configuration Options

### Modifying ChromeDriver Path
Edit line 226 in `script.py` to specify a custom ChromeDriver location:
```python
service = Service("C:\\WebDriver\\chromedriver-win64\\chromedriver.exe")
```

### Headless Mode
To run the browser in headless mode (no visible window), uncomment line 225:
```python
chrome_options.add_argument("--headless")
```

### Machine Configuration
The script supports 6 machines by default. To modify machine availability or names, edit the `MACHINE_COLUMN_MAP` and `slots` dictionaries at the top of the script (lines 13-27).

## Troubleshooting

### Common Issues

**ChromeDriver version mismatch:**
*   Error: "This version of ChromeDriver only supports Chrome version X"
*   Solution: Download the ChromeDriver version matching your installed Chrome browser.

**Login fails:**
*   Verify your credentials are correct.
*   Check that the LOAS booking system is accessible at `https://intra.loas.fi/bookings`.

**Bookings fail silently:**
*   Slots may already be reserved by other users.
*   The website structure may have changed. Inspect the page source to verify element selectors.

**"Element not found" errors:**
*   The booking page layout may have been updated. Check the XPath and CSS selectors in the `book_slots_for_date()` function.

## Contributing Guidelines

Contributions are welcome! To contribute:

1.  Fork the repository on GitHub.
2.  Create a feature branch: `git checkout -b feature/your-feature-name`
3.  Make your changes with clear, descriptive commit messages.
4.  Test your changes thoroughly.
5.  Push to your fork: `git push origin feature/your-feature-name`
6.  Submit a pull request with a detailed description of your changes.

### Code Standards
*   Follow PEP 8 Python style guidelines.
*   Add comments for complex logic.
*   Update the README if you add new features or change existing functionality.

## Acknowledgments

This project utilizes the following tools and libraries:
*   **Selenium WebDriver:** Browser automation framework.
*   **ChromeDriver:** Chromium WebDriver implementation.

---

**Note:** This bot is designed specifically for the LOAS housing booking system. Ensure you have permission to use automation tools on the platform, and use responsibly to avoid overwhelming the booking system.
