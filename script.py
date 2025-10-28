from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import sys

print("\n=== LOAS Laundry Booking Bot ===")
email = input("Enter your email: ")
password = input("Enter your password: ")

# Mappings to find the correct machine column (1-based index ughhh)
MACHINE_COLUMN_MAP = {
    "Washing Machine 1": 2,
    "Washing Machine 2": 3,
    "Washing Machine 3": 4,
    "Washing Machine 4": 5,
    "Dryer 1": 6,
    "Dryer 2": 7
}

slots = {
    "Washing Machine 1": [],
    "Washing Machine 2": [],
    "Washing Machine 3": [],
    "Washing Machine 4": [],
    "Dryer 1": [],
    "Dryer 2": []
}

valid_times = [
    f"{hour:02d}:{minute:02d}"
    for hour in range(7, 22)
    for minute in [0, 30]
]

def validate_time_slots(time_list):
    invalid_times = []
    for time_slot in time_list:
        if time_slot not in valid_times:
            invalid_times.append(time_slot)
    return invalid_times

def display_current_selections():
    print("\n" + "="*50)
    print("CURRENT SELECTIONS:")
    print("="*50)
    for machine_name, selected_times in slots.items():
        if selected_times:
            print(f"{machine_name}: {', '.join(selected_times)}")
        else:
            print(f"{machine_name}: No slots selected")
    print("="*50)
    
def get_next_day_of_week(start_date, target_day_index):
    days_ahead = target_day_index - start_date.weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def get_booking_dates_and_confirm():
    print("\n" + "="*50)
    print("DATE SELECTION")
    print("="*50)

    today = datetime.now().date()
    max_booking_date = today + timedelta(days=365)

    print(f"\nToday's date: {today.strftime('%Y-%m-%d')} ({today.strftime('%A')})")
    print(f"Last possible booking date: {max_booking_date.strftime('%Y-%m-%d')}")

    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    print("\nSelect the day of the week you want to book recurringly:")
    i = 0
    for day in day_names:
        i += 1
        print(f"{i}. {day}")

    while True:
        day_choice = input("\nEnter day number (1-7): ").strip()
        if day_choice.isdigit() and 1 <= int(day_choice) <= 7:
            selected_day_index = int(day_choice) - 1
            selected_day_name = day_names[selected_day_index]
            break
        else:
            print("⚠ Invalid choice. Please enter a number between 1-7.")

    print(f"\n✓ Selected: Every {selected_day_name}")

    first_booking_date = get_next_day_of_week(today, selected_day_index)
    print(f"\nFirst available {selected_day_name}: {first_booking_date.strftime('%Y-%m-%d')}")

    while True:
        print(f"\nEnter the LAST date you want to book (must be a {selected_day_name}):")
        print("Format: YYYY-MM-DD")
        print(f"Must be between {first_booking_date.strftime('%Y-%m-%d')} and {max_booking_date.strftime('%Y-%m-%d')}")
        
        end_date_str = input("Last booking date: ").strip()
        
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            if end_date < first_booking_date:
                print(f"⚠ End date cannot be before the first booking date ({first_booking_date.strftime('%Y-%m-%d')})")
                continue
            
            if end_date > max_booking_date:
                print(f"⚠ End date is too far in the future. Maximum date is {max_booking_date.strftime('%Y-%m-%d')}")
                continue
            
            if end_date.weekday() != selected_day_index:
                print(f"⚠ End date must be a {selected_day_name}. You entered a {day_names[end_date.weekday()]}.")
                continue
            
            print(f"✓ End date set to: {end_date.strftime('%Y-%m-%d')}")
            break
            
        except ValueError:
            print("⚠ Invalid date format. Please use YYYY-MM-DD (e.g., 2025-11-03)")

    booking_dates = []
    current_date = first_booking_date
    while current_date <= end_date:
        booking_dates.append(current_date)
        current_date += timedelta(days=7)  

    print(f"\n✓ Total {selected_day_name}s to book: {len(booking_dates)}")
    print(f"✓ Date range: {booking_dates[0].strftime('%Y-%m-%d')} to {booking_dates[-1].strftime('%Y-%m-%d')}")

    print("\nFirst 5 booking dates:")
    for i, date in enumerate(booking_dates[:5], 1):
        print(f"  {i}. {date.strftime('%Y-%m-%d')} ({date.strftime('%A')})")
    if len(booking_dates) > 5:
        print(f"  ... and {len(booking_dates) - 5} more")

    print("\n" + "="*50)
    confirm = input("\nProceed with booking? (yes/no): ").lower().strip()
    if confirm not in ['yes', 'y']:
        print("Booking cancelled.")
        return [], False
    
    return booking_dates, True

while True:
    display_current_selections()
    
    print("\nSelect a machine to add time slots:")
    print("a. Washing Machine 1")
    print("b. Washing Machine 2")
    print("c. Washing Machine 3")
    print("d. Washing Machine 4")
    print("e. Dryer 1")
    print("f. Dryer 2")
    print("g. Continue to date selection")
    print("h. Clear all selections")

    choice = input("\nSelect an option (a-h): ").lower().strip()
    
    machine_dic = {
        'a': "Washing Machine 1",
        'b': "Washing Machine 2",
        'c': "Washing Machine 3",
        'd': "Washing Machine 4",
        'e': "Dryer 1",
        'f': "Dryer 2"
    }
    
    if choice in machine_dic:
        machine = machine_dic[choice]
        print(f"\nEnter time slots for {machine}")
        print("Format: HH:MM, HH:MM (e.g., 08:00, 08:30, 11:00, 14:30)")
        print("Available times: 07:00 to 21:00 in 30-minute intervals")
        print("Leave blank & enter to skip.")
        
        user_input = input("Time slots: ").strip()
        
        if user_input:
            new_slots = [t.strip() for t in user_input.split(",")]
            
            invalid_times = validate_time_slots(new_slots)
            
            if invalid_times:
                print(f"\n⚠ Invalid time slots: {', '.join(invalid_times)}")
                print("Please use format HH:MM between 07:00 and 21:00")
            else:
                slots[machine] = new_slots
                print(f"✓ Added {len(new_slots)} slot(s) for {machine}")
        else:
            print(f"Skipped {machine}")
            
    elif choice == 'g':
        total_slots = sum(len(times) for times in slots.values())
        if total_slots == 0:
            print("\n⚠ No slots selected! Please select at least one time slot.")
            continue
        
        print(f"\n✓ Proceeding to book {total_slots} total slot(s)...")
        
        booking_dates, proceed = get_booking_dates_and_confirm()
        
        if proceed:
            print("✓ Date selection complete, proceeding to browser setup.")
            break
        else:
            print("\nReturning to machine selection menu.")
            continue
        
    elif choice == 'h':
        slots = {key: [] for key in slots}
        print("\n✓ All selections cleared!")
        
    else:
        print("\n⚠ Invalid choice. Please select a-h.")
        
if 'booking_dates' not in locals() or not booking_dates:
    print("\nExiting script due to cancellation or missing dates.")
    sys.exit()

chrome_options = Options()
chrome_options.add_argument("--lang=en") 
# for testing/debugging purposes. Uncomment the line below:
# chrome_options.add_argument("--headless") 

service = Service("C:\\WebDriver\\chromedriver-win64\\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.maximize_window()

def initialize_browser(browser, email, password):
    try:
        print("\n" + "="*50)
        print("STARTING BROWSER AUTOMATION")
        print("="*50)
        
        print("\n[1/5] Navigating to login page...")
        browser.get("https://intra.loas.fi/bookings")
        
        wait = WebDriverWait(browser, 10)
        
        print("[2/5] Entering email...")
        email_field = wait.until(
            EC.presence_of_element_located((By.ID, "customer_email")))
        email_field.clear()
        email_field.send_keys(email)
        
        print("[3/5] Entering password...")
        password_field = browser.find_element(By.ID, "customer_password")
        password_field.clear()
        password_field.send_keys(password)
        
        print("[4/5] Clicking login button...")
        login_button = browser.find_element(By.CSS_SELECTOR, "input[value='Kirjaudu sisään']")
        login_button.click()
        
        print("[5/5] Waiting for successful login and redirect...")
        wait.until(EC.url_contains("/complexes/")) 
        
    
        time.sleep(2)
        scroll_to = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/h1')
        browser.execute_script("arguments[0].scrollIntoView();", scroll_to)
        time.sleep(2)
        
        print("\n✓ Successfully logged in!")
        
        # Extract the base URL: e.g., https://intra.loas.fi/complexes/##/leases/#####/rooms
        base_url = browser.current_url.split('?')[0]
        print(f"✓ Base URL set: {base_url}")
        
        return base_url

    except Exception as e:
        print(f"\n✗ Login error: {str(e)}")
        browser.quit()
        sys.exit()

def book_slots_for_date(browser, base_url, date_str, slots):

    
    # Construct the new dated URL and navigate to it
    date_url = f"{base_url}?selected_date={date_str}"
    print(f"\n--- Navigating existing session to date: {date_str} ---")
    browser.get(date_url) 
    
    wait = WebDriverWait(browser, 10)
    
    try:
        scroll_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "booking-table-container-scroll"))
        )
        print(f"Page loaded for {date_str}. Starting booking attempts...")

        # find the tb in the container
        table_body = scroll_container.find_element(By.TAG_NAME, "tbody")
        
        # find all time rows in tb
        time_rows = table_body.find_elements(By.TAG_NAME, "tr")
        
        # Create a mapping of time string ('HH:MM') to the row element
        row_map = {}
        for row in time_rows:
            # first column is time (td:first-child)
            try:
                time_td = row.find_element(By.CSS_SELECTOR, "td:first-child")
                time_str = time_td.text.strip()
                row_map[time_str] = row
            except:
                continue

        for machine_name, time_slots in slots.items():
            if not time_slots:
                continue
                
            col_index = MACHINE_COLUMN_MAP[machine_name]
            print(f"Attempting to book {len(time_slots)} slot(s) for {machine_name}...")
            
            for time_slot in time_slots:
                if time_slot not in row_map:
                    print(f"  ✗ Time slot {time_slot} not found in the table. Skipping.")
                    continue

                row_element = row_map[time_slot]
                
                # Scroll the *inner* table container to make the row visible
                browser.execute_script(
                    "arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;", 
                    scroll_container, 
                    row_element
                )
                time.sleep(0.1) 

                # XPath to find the 'Book' button within the correct cell (td:nth-child)
                # targets the TD at the correct column index and looks for the button 
                # with the data-role='reserve-button' (which is the 'Book' button).
                xpath_selector = f"./td[{col_index}]//button[@data-role='reserve-button']"

                try:
                    # Find the specific 'Book' button within the correct row's cell
                    book_button = row_element.find_element(By.XPATH, xpath_selector)
                    
                    wait.until(EC.element_to_be_clickable(book_button))
                    book_button.click()
                    
                    print(f"  ✓ Successfully booked {machine_name} at {time_slot} on {date_str}")
                    
                    time.sleep(1.5) 

                except Exception as e:
                    print(f"  ✗ Failed to book {machine_name} at {time_slot}: Slot unavailable or button element not found.")
                    
    except Exception as e:
        print(f"✗ A critical error occurred while processing date {date_str}: {e}")

BASE_URL = initialize_browser(browser, email, password)

if booking_dates:
    print(f"\nBooking process will start for {len(booking_dates)} dates...")
    
    for date_object in booking_dates:
        date_str = date_object.strftime('%Y-%m-%d')
        book_slots_for_date(browser, BASE_URL, date_str, slots)
    
    print("\n✅ All dates processed.")
else:
    print("\nNo dates to book (user cancelled or no dates were generated).")


print("\n[Browser will remain open for testing]")
input("Press Enter to close browser...")
browser.quit()