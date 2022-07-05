from dash import html, dcc
from ..icons.hero import LIGHTENING_ICON, CHART_PIE_ICON, VIEW_GRID_ICON, CALENDER_ICON, TABLE_ICON, FIRE_ICON, PAGES_ICON, CRATE_ICON, CREDIT_CARD_ICON

from .mobile_nav import mobileSidebarHeader
from dash_spa.components.dropdown_folder_aoi import DropdownFolderAIO, dropdownFolderEntry

def _sidebarLink(text, icon, href, active="", hyperlink=False, target=""):
    Element = html.A if hyperlink else dcc.Link
    return  html.Li([
        Element([
            html.Span([
                icon
            ], className='sidebar-icon'),
            html.Span(text, className='mt-1 ms-1 sidebar-text')
        ], href=href, className='nav-link', target=target)
    ], className=f'nav-item {active}')


def _sidebarButtonLink(text, icon, href, active=""):
    return  html.Li([
        dcc.Link([
            html.Span([
                icon
            ], className='sidebar-icon d-inline-flex align-items-center justify-content-center'),
            html.Span(text, className="sidebar-text")
        ], href=href, className='btn btn-secondary d-flex align-items-center justify-content-center btn-upgrade-pro')
    ], className=f'nav-item {active}')


def sideBar():
    return html.Nav([
        html.Div([

            mobileSidebarHeader(),

            # Sidebar List of entries

            html.Ul([
                _sidebarLink("Volt Overview", LIGHTENING_ICON, 'https://demo.themesberg.com/volt/pages/dashboard/dashboard.html', hyperlink=True, target="_blank"),
                _sidebarLink("Dashboard", CHART_PIE_ICON, '/pages/dashboard.html'),
                _sidebarLink("Tansactions", CREDIT_CARD_ICON, '/pages/transactions'),
                _sidebarLink("Settings", VIEW_GRID_ICON, '/pages/settings.html'),
                _sidebarLink("Calendar", CALENDER_ICON, 'https://demo.themesberg.com/volt-pro/pages/calendar.html'),

                DropdownFolderAIO([
                    dropdownFolderEntry("Bootstrap Tables", '/pages/tables/boostrap-tables.html'),
                ], "Tables", TABLE_ICON),

                # Page examples drop down

                DropdownFolderAIO([
                    dropdownFolderEntry("Sign In", '/pages/sign-in.html'),
                    dropdownFolderEntry("Sign Up", '/pages/sign-up.html'),
                    dropdownFolderEntry("Forgot password", '/pages/forgot-password.html'),
                    dropdownFolderEntry("Reset password", '/pages/reset-password.html'),
                    dropdownFolderEntry("Lock", '/pages/lock.html'),
                    dropdownFolderEntry("404 Not Found", '/pages/???.html'),
                    dropdownFolderEntry("500 Not Found", '/pages/500.html'),
                ], "Page examples", PAGES_ICON),

                # Components  drop down

                DropdownFolderAIO([
                    dropdownFolderEntry("Buttons", '/pages/components/buttons.html'),
                ], "Components", CRATE_ICON),


                # Bottom Item

                _sidebarButtonLink("Upgrade to Pro", FIRE_ICON, '../pages/upgrade-to-pro.html')

            ], className='nav flex-column pt-3 pt-md-0')
        ], className='sidebar-inner px-4 pt-3')
    ], id='sidebarMenu', className='sidebar d-lg-block bg-gray-800 text-white collapse', **{"data-simplebar": ""})
