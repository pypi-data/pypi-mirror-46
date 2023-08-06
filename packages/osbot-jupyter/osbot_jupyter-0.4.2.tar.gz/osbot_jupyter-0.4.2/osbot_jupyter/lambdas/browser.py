


def run(event, context):
    url = event.get('url')
    if url:
        from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
        browser = Browser_Lamdba_Helper().setup()
        return browser.get_screenshot_png(url)
