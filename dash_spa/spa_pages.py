from typing import Callable, Union, List
import os
import importlib
import re
from urllib import parse
from collections import OrderedDict
import dash
from dash._utils import interpolate_str
from dash.development.base_component import Component
from dash_prefix import prefix
from .logging import log

page_container = dash.page_container
location = page_container.children[0]

container_registry = {}
style_registry = []

external_scripts = []
external_stylesheets = []
internal_stylesheets = []

from dash import _pages, _validate

class DashSPA(dash.Dash):

    def __init__(self, name=None, **kwargs):
        use_pages = kwargs.pop('use_pages', True)
        super().__init__(name=name, use_pages=use_pages, **kwargs)

    def interpolate_index(self,
            metas="",
            title="",
            css="",
            config="",
            scripts="",
            app_entry="",
            favicon="",
            renderer=""):

        for path in internal_stylesheets:
            css += f'\n<link rel="stylesheet" href="/internal{path}">'

        for path in external_stylesheets:
            css += f'\n<link rel="stylesheet" href="{path}">'

        for path in external_scripts:
            scripts += f'\n<script src="{path}"></script>'

        return interpolate_str(
            self.index_string,
            metas=metas,
            title=title,
            css=css,
            config=config,
            scripts=scripts,
            favicon=favicon,
            renderer=renderer,
            app_entry=app_entry,
        )

    def validate_pages(self):

        def page_layout(page, layout=None, path_variables={}, query_parameters={}):

            layout = page["layout"] if layout is None else  layout

            # Test to see if a content container id define for the page
            # if so call the container

            if 'container' in page:
                container_name = page['container']
                if container_name in dash.container_registry:
                    container = dash.container_registry[container_name]
                    return (
                            container(page, layout, **path_variables, **query_parameters)
                            if path_variables
                            else container(page, layout, **query_parameters)
                        )

            # No container handle the page layout directly

            if callable(layout):
                layout = (
                    layout(**path_variables, **query_parameters)
                    if path_variables
                    else layout(**query_parameters)
                )

            return layout

        for page in dash.page_registry.values():
            page_layout(page)

    def init_app(self, app=None, **kwargs):
        self.server.before_first_request(self.validate_pages)
        super().init_app(app, **kwargs)

    def _import_layouts_from_pages(self):
        walk_dir = self.config.pages_folder

        for (root, _, files) in os.walk(walk_dir):
            pages_package = os.path.relpath(root).replace(os.path.sep, '.')
            for file in files:
                if (
                    file.startswith("_")
                    or file.startswith(".")
                    or not file.endswith(".py")
                ):
                    continue
                with open(os.path.join(root, file), encoding="utf-8") as f:
                    content = f.read()
                    if "register_page" not in content:
                        continue

                file_name = file.replace(".py", "")
                module_name = f"{pages_package}.{file_name}"

                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(root, file)
                )
                page_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(page_module)

                if (
                    module_name in _pages.PAGE_REGISTRY
                    and not _pages.PAGE_REGISTRY[module_name]["supplied_layout"]
                ):
                    _validate.validate_pages_layout(module_name, page_module)
                    _pages.PAGE_REGISTRY[module_name]["layout"] = getattr(
                        page_module, "layout"
                    )


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
    log.info('page_container_append id=%s', id)

    for child in page_container.children:
        if child.id == id:
            page_container.children.remove(child)

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
    tag = f"<style>{style}</style>"
    if not tag in dash.style_registry:
        style_registry.append(tag)

def register_container(container, name='default'):
    """Register a container wih the given name"""
    dash.container_registry[name] = container


def add_external_scripts(url: Union[str, List[str]]) -> None:
    """Add given script(s) to the external_scripts list

    Args:
        url (Union[str, List[str]]): Script url or list of script urls

    Example:
    ```
            add_external_scripts("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.js")
    ```
    """
    urls = url if isinstance(url, list) else [url]
    for url in urls:
        if not url in external_scripts:
            external_scripts.append(url)

def add_external_stylesheets(url):
    """Add given stylesheet(s) to the external_stylesheets list

    Args:
        url (Union[str, List[str]]): Stylesheet url or list of stylesheet urls

    Example:
    ```
            add_external_stylesheets("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.css")
    ```
    """
    urls = url if isinstance(url, list) else [url]
    for url in urls:
        if not url in external_stylesheets:
            external_stylesheets.append(url)


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

    if not module in dash.page_registry:
        if module is None:
            pfx = prefix('spa')
            module = pfx(path[1:])
        dash.register_page(module, path, path_template, name, order, title, description, image, redirect_from, layout, **kwargs)

    page_def = dash.page_registry[module]
    return DashPage(page_def)


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