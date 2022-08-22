from dash import html, dcc
from dash_spa import prefix
from dash_spa.components.dropdown_folder_aoi import DropdownFolderAIO, SidebarNavItem, dropdownFolderEntry

from ..icons.hero import ICON

def _sidebarLink(text, icon, href, hyperlink=False, target=""):
    Element = html.A if hyperlink else dcc.Link
    el = Element([
            html.Span([
                icon
            ], className='sidebar-icon'),
            html.Span(text, className='mt-1 ms-1 sidebar-text')
        ], href=href, className='nav-link')

    if target:
        el.target = target

    return SidebarNavItem(el, SidebarNavItem.is_active(href))


def _sidebarButtonLink(text, icon, href):
    return  SidebarNavItem([
        dcc.Link([
            html.Span([
                icon
            ], className='sidebar-icon d-inline-flex align-items-center justify-content-center'),
            html.Span(text, className="sidebar-text")
        ], href=href, className='btn btn-secondary d-flex align-items-center justify-content-center btn-upgrade-pro')
    ], active=SidebarNavItem.is_active(href))


def sideBar():
    pid = prefix('sidebar')
    return html.Nav([
        html.Div([

            # Sidebar List of entries

            html.Ul([
                _sidebarLink("Dash/SPA", ICON.LIGHTENING, '/', target="_blank"),
                _sidebarLink("Dashboard", ICON.CHART_PIE, '/pages/dashboard'),
                _sidebarLink("Transactions", ICON.CREDIT_CARD, '/pages/transactions'),
                _sidebarLink("Settings", ICON.VIEW_GRID, '/pages/settings'),
                _sidebarLink("Calendar", ICON.CALENDER, 'https://demo.themesberg.com/volt-pro/pages/calendar'),

                DropdownFolderAIO([
                    dropdownFolderEntry("Bootstrap Tables", '/pages/tables/bootstrap-tables'),
                ], "Tables", ICON.TABLE, id=pid('tables')),

                # Page examples drop down

                DropdownFolderAIO([
                    dropdownFolderEntry("Sign In", '/pages/sign-in'),
                    dropdownFolderEntry("Sign Up", '/pages/sign-up'),
                    dropdownFolderEntry("Forgot password", '/pages/forgot-password'),
                    dropdownFolderEntry("Reset password", '/pages/reset-password'),
                    dropdownFolderEntry("Lock", '/pages/lock'),
                    dropdownFolderEntry("404 Not Found", '/pages/???'),
                    dropdownFolderEntry("500 Not Found", '/pages/500'),
                ], "Page examples", ICON.PAGES, id=pid('examples')),

                # Components  drop down

                DropdownFolderAIO([
                    dropdownFolderEntry("Buttons", '/pages/components/buttons'),
                    dropdownFolderEntry("Notifications", '/pages/components/notifications'),
                    dropdownFolderEntry("Forms", '/pages/components/forms'),
                    dropdownFolderEntry("Modals", '/pages/components/modals'),
                    dropdownFolderEntry("Typography", '/pages/components/typography'),
                ], "Components", ICON.ARCHIVE, id=pid('components')),


                # Bottom Item

                _sidebarButtonLink("Exit", ICON.FIRE.ME2, '/')

            ], className='nav flex-column pt-3 pt-md-0')
        ], className='sidebar-inner px-4 pt-3')
    ], id='sidebarMenu', className='sidebar d-lg-block bg-gray-800 text-white collapse')
