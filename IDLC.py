from playwright.sync_api import sync_playwright, Page

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page: Page = browser.new_page()

    # Go to the login page
    page.goto("https://verify.barikoimaps.dev/login")
    page.wait_for_timeout(5000)

    # Login to the dashboard
    page.fill("#email", "brotatihalderkatha@gmail.com")
    page.fill("#password", "12345678")
    page.wait_for_timeout(2000)
    page.click("button[type='submit']")
    page.wait_for_timeout(2000)

    # Logged in dashboard
    page.wait_for_selector("#root > div > section > div > div > div > header > div > a")
    page.wait_for_timeout(5000)

    # Create file page
    page.get_by_role("link", name="Create File").click()
    page.wait_for_timeout(4000)
    page.get_by_text("Create From Dashboard").click()
    page.wait_for_timeout(4000)

    # IDLC file set up
    page.get_by_label("Select Organization").click()
    page.wait_for_timeout(4000)
    page.get_by_text("IDLC").click()
    page.wait_for_timeout(4000)

    page.get_by_label("Application Type").click()
    page.wait_for_timeout(4000)
    page.get_by_text("Loan").click()
    page.wait_for_timeout(4000)

    page.get_by_label("Application Sub Type").click()
    page.wait_for_timeout(4000)
    page.get_by_text("Home Loan").click()
    page.wait_for_timeout(3000)

    page.evaluate("window.scrollBy(0, 200);")
    page.fill("#application_application_id", "0012")
    page.evaluate("window.scrollBy(0, 500);")
    page.wait_for_timeout(3000)

    page.get_by_label("Application Tag").click()
    page.get_by_title("Ordinary").click()
    page.wait_for_timeout(3000)
    page.get_by_label("Co-Applicant Number").click()
    page.get_by_title("0").click()
    page.wait_for_timeout(3000)
    page.get_by_text("IN_STATION").click()
    page.wait_for_timeout(3000)

    page.get_by_text("Applicant Information").click()
    page.fill("#APPLICANT_name", "test by playwright")
    page.fill("#APPLICANT_spouse", "xyz")
    page.fill("#APPLICANT_phone", "01762108999")
    page.fill("#APPLICANT_designation", "dr")
    page.evaluate("window.scrollBy(0, 500);")
    page.wait_for_timeout(3000)

    # Applicant House setup
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


    # Submit File
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(5000)

    error_message = page.get_by_text("success")
    page.wait_for_timeout(4000)
    assert error_message == "success"


    # page.get_by_text("Default").click()
    # page.get_by_text("Rupantor", exact=True).click()
    # page.wait_for_timeout(5000)
    # page.get_by_label("Not Exact").click()










