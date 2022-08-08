from typing import Callable, Union, List
import re
from urllib import parse
from collections import OrderedDict
import dash
from dash.development.base_component import Component
from dash_prefix import prefix
from .logging import log

from .plugins import pages


spa_plugin = __name__
page_container = pages.page_container

# location = dcc.Location(id='spa#location')
location = page_container.children[0]

def page_container_append(component: Component):
    """Append given component to the page container"""

    def get_id(component):
        if hasattr(component, 'id'):
            return component.id
        elif hasattr(component, 'children'):
            children = component.children
            children = children if isinstance(children, list) else [children]
            for component in children:
                if hasattr(component, 'id'):
                    return component.id
        return "NO ID"

    id = get_id(component)
    # log.info('page_container_append id=%s', id)
    page_container.children.append(component)


def add_style(style: str):
    """Add given style to the html header

    Args:
        style (str): CSS style to be added

    Example
    ```
     add_style('''
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f5f5f5;
            }
        ''')
    ```
    """
    pages.add_style(style)

class DashPage:

    @property
    def path(self):
        return self._page['path']

    @property
    def title(self):
        return self._page['title']

    @property
    def short_name(self):
        if 'short_name' in self._page:
            return self._page['short_name']
        else:
            return None

    @property
    def module(self):
        return self._page['module']

    def __init__(self, page: OrderedDict):
        self._page = page
        self.pfx= prefix(self.module)

    def id(self, id):
        return self.pfx(id)

    def layout(self):
        _layout = self._page['layout']
        return _layout() if callable(_layout) else _layout


LayoutFunc = Callable[[], Component]

def register_page(
    module: str = None,
    path: str = None,
    path_template: str = None,
    name: str = None,
    order: str = None,
    title: str = None,
    description: str =None,
    image: str = None,
    redirect_from: str = None,
    layout: Union[Component , LayoutFunc] = None,
    **kwargs,
) -> DashPage:
    """
    Assigns the variables to `dash.page_registry` as an `OrderedDict`
    (ordered by `order`).

    `dash.page_registry` is used by `pages_plugin` to set up the layouts as
    a multi-page Dash app. This includes the URL routing callbacks
    (using `dcc.Location`) and the HTML templates to include title,
    meta description, and the meta description image.

    `dash.page_registry` can also be used by Dash developers to create the
    page navigation links or by template authors.

    - `module`:
       The module path where this page's `layout` is defined. Often `__name__`.

    - `path`:
       URL Path, e.g. `/` or `/home-page`.
       If not supplied, will be inferred from the `path_template` or `module`,
       e.g. based on path_template: `/asset/<asset_id` to `/asset/none`
       e.g. based on module: `pages.weekly_analytics` to `/weekly-analytics`

    - `path_template`:
       Add variables to a URL by marking sections with <variable_name>. The layout function
       then receives the <variable_name> as a keyword argument.
       e.g. path_template= "/asset/<asset_id>"
            then if pathname in browser is "/assets/a100" then layout will receive **{"asset_id":"a100"}

    - `name`:
       The name of the link.
       If not supplied, will be inferred from `module`,
       e.g. `pages.weekly_analytics` to `Weekly analytics`

    - `order`:
       The order of the pages in `page_registry`.
       If not supplied, then the filename is used and the page with path `/` has
       order `0`

    - `title`:
       (string or function) The name of the page <title>. That is, what appears in the browser title.
       If not supplied, will use the supplied `name` or will be inferred by module,
       e.g. `pages.weekly_analytics` to `Weekly analytics`

    - `description`:
       (string or function) The <meta type="description"></meta>.
       If not supplied, then nothing is supplied.

    - `image`:
       The meta description image used by social media platforms.
       If not supplied, then it looks for the following images in `assets/`:
        - A page specific image: `assets/<title>.<extension>` is used, e.g. `assets/weekly_analytics.png`
        - A generic app image at `assets/app.<extension>`
        - A logo at `assets/logo.<extension>`
        When inferring the image file, it will look for the following extensions: APNG, AVIF, GIF, JPEG, PNG, SVG, WebP.

    - `redirect_from`:
       A list of paths that should redirect to this page.
       For example: `redirect_from=['/v2', '/v3']`

    - `layout`:
       The layout function or component for this page.
       If not supplied, then looks for `layout` from within the supplied `module`.

    - `**kwargs`:
       Arbitrary keyword arguments that can be stored

    ***

    `page_registry` stores the original property that was passed in under
    `supplied_<property>` and the coerced property under `<property>`.
    For example, if this was called:
    ```
    register_page(
        'pages.historical_outlook',
        name='Our historical view',
        custom_key='custom value'
    )
    ```
    Then this will appear in `page_registry`:
    ```
    OrderedDict([
        (
            'pages.historical_outlook',
            dict(
                module='pages.historical_outlook',

                supplied_path=None,
                path='/historical-outlook',

                supplied_name='Our historical view',
                name='Our historical view',

                supplied_title=None,
                title='Our historical view'

                supplied_layout=None,
                layout=<function pages.historical_outlook.layout>,

                custom_key='custom value'
            )
        ),s
    ])
    ```

    """

    if module is None:
        pfx = prefix('spa')
        module = pfx(path[1:])

    dash.register_page(module, path, path_template, name, order, title, description, image, redirect_from, layout, **kwargs)
    page_def = dash.page_registry[module]
    return DashPage(page_def)

def plug(dash: dash.Dash):
    pages.plug(dash)

def get_page(path:str) -> DashPage:
    for page in dash.page_registry.values():
        if page['path'] == path:
            return DashPage(page)
    raise Exception(f"No page for path '{path}' defined")


def page_for(module:str) -> str:
    if module in dash.page_registry:
        page = dash.page_registry[module]
        return DashPage(page)
    raise Exception(f"No page for module \"{module}\" defined")


def url_for(module:str, args: dict=None, attr=None) -> str:

    if module in dash.page_registry:
        page = dash.page_registry[module]
        path = page['path']
        if args:
            if attr:
                args = {k:v for k,v in args.items() if k in attr and v is not (None or "")}
            path += '?' + parse.urlencode(args)
        return path

    raise Exception(f"No page for module \"{module}\" defined")

def page_id(page:dict):
    id = re.sub('^.*?pages\.', '', page['module'])
    return prefix(id.replace('.','_'))

def register_container(module, name='default'):
    """Register a container wih the given name"""
    dash.register_container(module, name)

def add_external_scripts(url: Union[str, List[str]]) -> None:
    """Add given script(s) to the external_scripts list

    Args:
        url (Union[str, List[str]]): Script url or list of script urls

    Example:
    ```
            add_external_scripts("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.js")
    ```
    """
    dash.add_external_scripts(url)

def add_external_stylesheets(url:Union[str, List[str]]) -> None:
    """Add given stylesheet(s) to the external_stylesheets list

    Args:
        url (Union[str, List[str]]): Stylesheet url or list of stylesheet urls

    Example:
    ```
            add_external_stylesheets("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.css")
    ```
    """
    dash.add_external_stylesheets(url)
