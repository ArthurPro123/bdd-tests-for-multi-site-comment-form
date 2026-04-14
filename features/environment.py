# environment.py

import yaml
from playwright.sync_api import sync_playwright
import re

def before_all(context):

    context.config.setup_logging()
    
    # Get site filter from command line
    context.site_filter = context.config.userdata.get('site', None)
    
    # Load config
    with open("config/sites.yaml", 'r') as f:
        context.sites_config = yaml.safe_load(f)['sites']
    
    if context.site_filter:
        print(f"\n*** Running tests ONLY on site: {context.site_filter} ***\n")
    else:
        print(f"\n*** Running tests on ALL sites: {', '.join(context.sites_config.keys())} ***\n")
    

    # Start Playwright
    context.playwright = sync_playwright().start()

    context.browser = context.playwright.chromium.launch(
        headless=False,
        args=['--ignore-certificate-errors', '--ignore-ssl-errors']
    )


def before_scenario(context, scenario):

    # Extract site from scenario name (e.g., "... on site1 -- @1.1")
    site_match = re.search(r'on (\S+) --', scenario.name)
    
    if site_match:
        scenario_site = site_match.group(1)
        
        # Skip if filtering and this scenario is for a different site
        if hasattr(context, 'site_filter') and context.site_filter:

            if scenario_site != context.site_filter:
                scenario.skip(reason=f"Skipping {scenario_site} - only running {context.site_filter}")
                return
    
    # New browser session for each scenario
    context.browser_session = context.browser.new_context(ignore_https_errors=True)


def after_scenario(context, scenario):
    # Clean up browser session
    if hasattr(context, 'browser_session'):
        context.browser_session.close()


def after_all(context):
    # Clean up Playwright
    context.browser.close()
    context.playwright.stop()
