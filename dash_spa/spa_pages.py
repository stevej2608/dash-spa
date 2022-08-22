from typing import Callable, Union, List
from werkzeug.local import LocalProxy
import os
import sys
import time
import importlib
import re
from urllib import parse
from collections import OrderedDict
from flask import current_app
import dash
from dash._utils import interpolate_str
from dash.development.base_component import Component
from dash import _validate
from dash_prefix import prefix
from .logging import log
from .spa_globals import Globals

page_container = Globals.page_container
location = Globals.location

_default_index = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        {%styles%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

def clear_globals():
    """Reset global variables"""
    global container_registry, style_registry, external_scripts, external_stylesheets, internal_stylesheets

    # container_registry = {}
    # style_registry = []

    # external_scripts = []
    # external_stylesheets = []
    # internal_stylesheets = []

    # while len(Globals.page_container.children) > 4:
    #     Globals.page_container.children.pop()

    GLOBAL_CALLBACK_LIST = []
    GLOBAL_CALLBACK_MAP = {}

def page_layout(page, **kwargs):

    if 'layout' in page and page['layout']:
        layout = page['layout']
    elif 'supplied_layout' in page and page['supplied_layout']:
        layout = page['supplied_layout']
    else:
        raise KeyError(f"Unable to resolve layout for page {page['module']}")

    # Test to see if a content container id define for the page
    # if so call the container

    if 'container' in page:
        container_name = page['container']
        if container_name in Globals.container_registry:
            container = Globals.container_registry[container_name]
            return container(page, layout, **kwargs)

    # No container handle the page layout directly

    if callable(layout):
        layout = layout(**kwargs)

    return layout


def layout_delegate(page):
    page = page.copy()
    def wrapper(**kwargs):
        return page_layout(page, **kwargs)
    return wrapper


class DashSPA(dash.Dash):

    start_time = 0

    @property
    def is_live(self):
        return self._is_live

    @property
    def got_first_request(self):
        try:
            return current_app.got_first_request
        except:
            return False

    def __init__(self, name=None, **kwargs):
        log.info('Create DashSPA(%s)', name)
        Globals.dump()
        Globals.clear()

        self._is_live = False
        DashSPA.start_time = time.time()

        # _cb_initialised = {}
        # GLOBAL_CALLBACK_LIST = []
        # GLOBAL_CALLBACK_MAP = {}

        use_pages = kwargs.pop('use_pages', True)
        index_string = kwargs.pop('index_string', _default_index)

        super().__init__(
            name=name,
            use_pages=use_pages,
            index_string=index_string,
            **kwargs
            )

    def init_app(self, app=None, **kwargs):
        #self.server.before_first_request(self.validate_pages)
        super().init_app(app, **kwargs)

        # All the pages have now been registered. We now need to
        # iterate over all te registered page layouts to force the
        # registration of any embedded callbacks.

        log.info('************** init_app(): pages %s **************', len(Globals.PAGE_REGISTRY))

        for page in Globals.PAGE_REGISTRY.values():
            layout = page['layout']
            if callable(layout):
                layout()


    def run(self, *args, **kwargs):
        Globals.dump()
        # Globals.save_or_restore()
        self._is_live = True
        super().run(*args, **kwargs)


    def interpolate_index(self,
            metas="",
            title="",
            css="",
            config="",
            scripts="",
            app_entry="",
            favicon="",
            renderer=""):

        # Intercede in the final markup generation to add style sheets
        # and scripts that have been requested programmatically.

        for path in Globals.internal_stylesheets:
            css += f'\n<link rel="stylesheet" href="/internal{path}">'

        for path in Globals.external_stylesheets:
            css += f'\n<link rel="stylesheet" href="{path}">'

        for path in Globals.external_scripts:
            scripts += f'\n<script src="{path}"></script>'

        return interpolate_str(
            self.index_string,
            metas=metas,
            title=title,
            css=css,
            styles = '\n'.join(Globals.style_registry),
            config=config,
            scripts=scripts,
            favicon=favicon,
            renderer=renderer,
            app_entry=app_entry,
        )

    # def validate_pages(self):

    #     log.info('************** Validate pages %s **************', len(Globals.PAGE_REGISTRY))

    #     for page in Globals.PAGE_REGISTRY.values():
    #         layout = page['layout']
    #         if callable(layout):
    #             layout()

    #     self._setup_completed = True

    #     log.info('************** Starting Server **************')

    def _import_layouts_from_pages(self):

        log.info('_import_layouts_from_pages()')

        walk_dir = self.config.pages_folder

        # FIXME: This is needed to resolve 404 page in dash.py update()
        self.pages_folder = os.path.relpath(walk_dir).replace(os.path.sep, '.')


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
                    if "register_page" not in content and "register_container" not in content:
                        continue

                file_name = file.replace(".py", "")
                module_name = f"{pages_package}.{file_name}"

                if module_name in sys.modules:
                    log.info('module %s is already loaded', module_name)

                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(root, file)
                )
                page_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(page_module)

                # if module_name in Globals.PAGE_REGISTRY:
                #     page = Globals.PAGE_REGISTRY[module_name]
                #     if page["supplied_layout"]:
                #         layout = page["supplied_layout"]
                #     else:
                #         _validate.validate_pages_layout(module_name, page_module)
                #         layout = getattr(page_module, "layout")

                #     page["layout"] = layout

                #     if layout not layout_delegate:


                #     page['layout'] = layout_delegate(page)


                if (
                    module_name in Globals.PAGE_REGISTRY
                    and not Globals.PAGE_REGISTRY[module_name]["supplied_layout"]
                ):
                    _validate.validate_pages_layout(module_name, page_module)
                    page = Globals.PAGE_REGISTRY[module_name]
                    page["layout"] = getattr(page_module, "layout")
                    page['layout'] = layout_delegate(page)

                    # Globals.dump()


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
    # log.info('Globals.page_container_append id=%s', id)

    for child in Globals.page_container.children:
        if child.id == id:
            Globals.page_container.children.remove(child)

    Globals.page_container.children.append(component)


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
    if not tag in Globals.style_registry:
        Globals.style_registry.append(tag)

def register_container(container, name='default'):
    """Register a container wih the given name"""
    Globals.container_registry[name] = container


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
        if not url in Globals.external_scripts:
            Globals.external_scripts.append(url)

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
        if not url in Globals.external_stylesheets:
            Globals.external_stylesheets.append(url)


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

def _register_page(
    module: str = None,
    path: str = None,
    path_template: str = None,
    name: str = None,
    order: str = None,
    title: str = None,
    description: str =None,
    image: str = None,
    image_url: str =None,
    redirect_from: str = None,
    layout: Union[Component , LayoutFunc] = None,
    container = 'default',
    **kwargs,
) -> DashPage:
    """
    Assigns the variables to `_pages.Globals.PAGE_REGISTRY` as an `OrderedDict`
    (ordered by `order`).

    `_pages.Globals.PAGE_REGISTRY` is used by `pages_plugin` to set up the layouts as
    a multi-page Dash app. This includes the URL routing callbacks
    (using `dcc.Location`) and the HTML templates to include title,
    meta description, and the meta description image.

    `_pages.Globals.PAGE_REGISTRY` can also be used by Dash developers to create the
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

    log.info('register page %s', module)

    if module is None:
        pfx = prefix('spa')
        module = pfx(path[1:])

    kwargs['container'] = container

    dash.register_page(
        module,
        path,
        path_template,
        name,
        order,
        title,
        description,
        image,
        image_url,
        redirect_from,
        layout,
        **kwargs)

    page = Globals.PAGE_REGISTRY[module]

    if layout:
        page['layout'] = layout_delegate(page)

    Globals.PAGE_REGISTRY[module]['page'] = DashPage(page)


# def register_page(module, **_kwargs):

#     def wrapper():
#         if not module in Globals.PAGE_REGISTRY:
#             try:
#                 _register_page(module, **_kwargs)
#             except:
#                 return None

#         return Globals.PAGE_REGISTRY[module]['page']

#     page = LocalProxy(wrapper)

#     # If the host page does not reference the returned
#     # DashPage instance the page will never be
#     # registered. So we need to force a registration here.

#     try:
#         assert page.module == module
#     except:
#         pass

#     return page


def register_page(module, **_kwargs):

    def wrapper():
        if not module in Globals.PAGE_REGISTRY:
            try:
                _register_page(module, **_kwargs)
            except:
                return None

        return Globals.PAGE_REGISTRY[module]['page']

    page = wrapper()

    if page is None:
        page = page = LocalProxy(wrapper)

    return page


def get_page(path:str) -> DashPage:
    for page in Globals.PAGE_REGISTRY.values():
        if page['path'] == path:
            return DashPage(page)
    raise Exception(f"No page for path '{path}' defined")


def page_for(module:str) -> str:
    if module in Globals.PAGE_REGISTRY:
        page = Globals.PAGE_REGISTRY[module]
        return DashPage(page)
    raise Exception(f"No page for module \"{module}\" defined")


def url_for(module:str, args: dict=None, attr=None) -> str:

    if module in Globals.PAGE_REGISTRY:
        page = Globals.PAGE_REGISTRY[module]
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