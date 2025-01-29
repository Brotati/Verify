from playwright.sync_api import sync_playwright, Page
import json

BROWSER_SETTINGS = {
    "headless": False,       
    "slow_mo": 100,          
    "channel": "chromium",  
    "default_timeout": 45000 
}

# DELAY CONSTANTS (ms)
PAGE_LOAD_DELAY = 5000
ANIMATION_DELAY = 3000
FORM_DELAY = 2000

def load_organization_config(org_name: str) -> dict:
    """Load organization-specific configuration from JSON file"""
    with open("C:/Users/LENOVO/PycharmProjects/Verify/InputFiles/AB.json") as f:
        config = json.load(f)
    return config["organizations"][org_name]

def login(page: Page, credentials: dict):
    """Handle login process"""
    page.goto("https://verify.barikoimaps.dev/login")
    page.wait_for_timeout(PAGE_LOAD_DELAY)
    
    page.fill("#email", credentials["email"])
    page.fill("#password", credentials["password"])
    page.wait_for_timeout(FORM_DELAY)
    page.click("button[type='submit']")
    
    # Wait for dashboard to load
    page.wait_for_selector("#root > div > section > div > div > div > header", timeout=BROWSER_SETTINGS["default_timeout"])

def create_application(page: Page, config: dict):
    """Handle application creation process"""
    page.get_by_role("link", name="Create File").click()
    page.wait_for_timeout(ANIMATION_DELAY)
    page.get_by_text("Create From Dashboard").click()
    page.wait_for_timeout(ANIMATION_DELAY)

    # Select organization
    page.get_by_label("Select Organization").click()
    page.wait_for_timeout(FORM_DELAY)
    org_element = page.get_by_text(config["organization_name"], exact=True)
    org_element.scroll_into_view_if_needed()
    page.evaluate("window.scrollBy(0, 150);")
    org_element.click(timeout=15000)

    # page.wait_for_timeout(ANIMATION_DELAY)

    # Application type setup
    page.get_by_label("Application Type").click()
    page.get_by_text(config["application"]["type"]).click()
    page.wait_for_timeout(FORM_DELAY)

    page.get_by_label("Application Sub Type").click()
    page.get_by_text(config["application"]["sub_type"]).click()
    page.wait_for_timeout(FORM_DELAY)

    # Application ID
    app_id_field = page.locator("#application_application_id")
    app_id_field.scroll_into_view_if_needed()
    app_id_field.fill(config["application"]["id"])
    page.wait_for_timeout(FORM_DELAY)

    # Application tags
    page.get_by_label("Application Tag").click()
    page.get_by_title(config["application"]["tag"]).click()
    page.wait_for_timeout(FORM_DELAY)
    page.get_by_text(config["application"]["category"]).click()
    page.wait_for_timeout(FORM_DELAY)

def fill_address_section(page: Page, config: dict, section_name: str):
    """Generic function to fill address sections"""
    page.get_by_text(section_name).click()
    page.fill("#APPLICANT_HOUSE_address", config["applicant"]["address"])
    page.wait_for_timeout(FORM_DELAY)
    
    page.get_by_text("Default").first.click()
    page.get_by_text("Rupantor", exact=True).click()
    page.wait_for_timeout(FORM_DELAY)
    
    page.get_by_label("Not Exact").click()
    page.get_by_placeholder("Enter exact address..").fill("Barikoi")
    page.wait_for_selector("text=HQ (barikoi.com), Dr Mohsin", state="visible")
    page.get_by_text("HQ (barikoi.com), Dr Mohsin").click()
    page.wait_for_timeout(ANIMATION_DELAY)

def main(org_name: str = "AB Bank PLC"):
    """Main execution flow"""
    config = load_organization_config(org_name)
    
    with sync_playwright() as p:
        # Browser setup
        browser = p.chromium.launch(
            headless=BROWSER_SETTINGS["headless"],
            slow_mo=BROWSER_SETTINGS["slow_mo"],
            channel=BROWSER_SETTINGS["channel"]
        )
        page = browser.new_page()
        page.set_default_timeout(BROWSER_SETTINGS["default_timeout"])

        try:
            # Execute workflow
            login(page, config["credentials"])
            create_application(page, config)
            
            # Applicant information
            page.get_by_text("Applicant Information").click()
            page.fill("#APPLICANT_name", config["applicant"]["name"])
            page.fill("#APPLICANT_spouse", config["applicant"]["spouse"])
            page.fill("#APPLICANT_phone", config["applicant"]["phone"])
            page.fill("#APPLICANT_designation", config["applicant"]["designation"])
            page.wait_for_timeout(FORM_DELAY)

            # Address sections
            fill_address_section(page, config, "Applicant House")
            fill_address_section(page, config, "Applicant Office")

            # Final submission
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(PAGE_LOAD_DELAY)
            print("Submission successful. Page title:", page.title())

        finally:
            browser.close()

if __name__ == "__main__":
    main()