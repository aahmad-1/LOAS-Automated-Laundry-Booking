from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#User Cred
print("=== LOAS Laundry Booking Bot ===\n")
email = input("Enter your email: ")
password = input("Enter your password: ")

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

# Menu for selecting time slots
while True:
    display_current_selections()
    
    print("\nSelect a machine to add time slots:")
    print("a. Washing Machine 1")
    print("b. Washing Machine 2")
    print("c. Washing Machine 3")
    print("d. Washing Machine 4")
    print("e. Dryer 1")
    print("f. Dryer 2")
    print("g. Continue to booking")
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
            
            # Validate time slots
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
        # Check if any slots are selected
        total_slots = sum(len(times) for times in slots.values())
        if total_slots == 0:
            print("\n⚠ No slots selected! Please select at least one time slot.")
            continue
        
        print(f"\n✓ Proceeding to book {total_slots} total slot(s)...")
        break
        
    elif choice == 'h':
        slots = {key: [] for key in slots}
        print("\n✓ All selections cleared!")
        
    else:
        print("\n⚠ Invalid choice. Please select a-h.")

# Browser setup
chrome_options = Options()
chrome_options.add_argument("--lang=en") 

service = Service("C:\\WebDriver\\chromedriver-win64\\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=chrome_options)
browser.maximize_window()

def initialize_browser():
    try:
        print("\n" + "="*50)
        print("STARTING BROWSER AUTOMATION")
        print("="*50)
        
        # Navigate to login page
        print("\n[1/5] Navigating to login page...")
        browser.get("https://intra.loas.fi/bookings")
        
        wait = WebDriverWait(browser, 10)
        
        # Enter credentials
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
        
        # Wait for redirect
        print("[5/5] Waiting for login...")
        wait.until(EC.url_contains("/complexes/"))
        
        print("\n✓ Successfully logged in!")
        print(f"✓ Current URL: {browser.current_url}")
        
        time.sleep(3)
        
    except Exception as e:
        print(f"\n✗ Login error: {str(e)}")
        browser.quit()
        
initialize_browser()

# TODO: Add booking logic here using the 'slots' dictionary

print("\n[Browser will remain open for testing]")
input("Press Enter to close browser...")
browser.quit()