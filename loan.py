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
    with open("C:/Users/LENOVO/PycharmProjects/Verify/InputFiles/city_Loan.json") as f:
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
    page.wait_for_selector("#root>div>section>div>div>div>header", timeout=BROWSER_SETTINGS["default_timeout"])

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
    page.evaluate("window.scrollBy(0, 250);")
    org_element.click(timeout=15000)

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

    # Co-Applicant Number
    page.get_by_label("Co-Applicant Number").click()
    page.wait_for_timeout(FORM_DELAY)
    page.get_by_title("1").locator("div").click()
    page.wait_for_timeout(FORM_DELAY)


    """Main execution flow"""
def main(org_name: str = "Bank Details"):
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
            
            # Applicant House Trip details
            page.get_by_text("Applicant House").click()
            page.fill("#APPLICANT_HOUSE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 250);")

            # Applicant Office Trip details 
            page.get_by_text("Applicant Office").click()
            page.fill("#APPLICANT_OFFICE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_role("cell", name="Default", exact=True).get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_role("list").get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 550);")

            # Co-Applicant information
            page.get_by_role("button", name="right Co-Applicant 1 Information").click()
            page.fill("#CO_APPLICANT1_name", config["co-applicant"]["name"])
            page.fill("#CO_APPLICANT1_spouse", config["co-applicant"]["spouse"])
            page.fill("#CO_APPLICANT1_phone", config["co-applicant"]["phone"])
            page.fill("#CO_APPLICANT1_designation", config["co-applicant"]["designation"])
            page.wait_for_timeout(FORM_DELAY)

            # co-applicant House Trip details
            page.get_by_role("button", name="right Co-Applicant 1 House").click()
            page.fill("#CO_APPLICANT1_HOUSE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 250);")

            # co-applicant Office Trip details 
            page.get_by_role("button", name="right Co-Applicant 1 Office").click()
            page.fill("#CO_APPLICANT1_OFFICE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_role("cell", name="Default", exact=True).get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_role("list").get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 550);")

            # Guarantor information
            page.get_by_role("button", name="right First Guarantor").click()
            page.fill("#FIRST_GUARANTOR_name", config["Guarantor"]["name"])
            page.fill("#FIRST_GUARANTOR_spouse", config["Guarantor"]["spouse"])
            page.fill("#FIRST_GUARANTOR_phone", config["Guarantor"]["phone"])
            page.fill("#FIRST_GUARANTOR_designation", config["Guarantor"]["designation"])
            page.wait_for_timeout(FORM_DELAY)

            # Guarantor House Trip details
            page.get_by_role("button", name="right First Guarantor House").click()
            page.fill("#FIRST_GUARANTOR_GUARANTOR_HOUSE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 550);")

            # Guarantor Office Trip details 
            page.get_by_role("button", name="right First Guarantor Office").click()
            page.fill("#FIRST_GUARANTOR_GUARANTOR_OFFICE_address",
              "Barikoi HQ (barikoi.com), Dr Mohsin Plaza, House  2/7, Begum Rokeya Sarani, Pallabi, Mirpur, "
              "Dhaka, Mirpur, Dhaka")
            page.wait_for_timeout(5000)
            page.get_by_role("cell", name="Default", exact=True).get_by_placeholder("Enter exact address..").fill("Barikoi")
            page.wait_for_selector("#rc-tabs-0-panel-Create\ From\ Dashboard > div > div > "
                           "div.ant-col.ant-col-14.ant-col-xs-24.ant-col-lg-24.ant-col-xl-12 > div > "
                           "div.ant-card-body > form > div:nth-child(2) > div > div > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > "
                           "div.ant-collapse.ant-collapse-icon-position-left > "
                           "div.ant-collapse-item.ant-collapse-item-active > "
                           "div.ant-collapse-content.ant-collapse-content-active > div > div > div:nth-child(2) > "
                           "div.ant-col.ant-col-24.ant-form-item-control.ant-col-xs-24.ant-col-sm-24.ant-col-md-24"
                           ".ant-col-lg-24.ant-col-xl-24.ant-col-xxl-19 > div > div > span > "
                           "div.ant-card.ant-card-bordered > div > ul > li", state="visible")
            page.wait_for_timeout(5000)
            page.get_by_role("list").get_by_text("HQ (barikoi.com), Dr Mohsin").click()
            page.wait_for_timeout(5000)
            page.evaluate("window.scrollBy(0, 500);")
            page.evaluate("window.scrollBy(0, 550);")



            # Final submission
            page.get_by_role("button", name="Submit").click()
            page.wait_for_timeout(PAGE_LOAD_DELAY)
            print("Submission successful. Page title:", page.title())

        finally:
            browser.close()

if __name__ == "__main__":
    main()