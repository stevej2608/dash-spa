[Dash constructor](dash.py#2023)
    [init_app()](dash_spa.py#114)
      - before_first_request()
      [init_app()](dash.py#505)
        before_first_request(self.validate_pages)
        before_first_request(self._setup_server)
        *** get_app works from here on ***
        [dash.enable_pages()](dash.py#2023)
          import_layouts_from_pages()
            - imports all pages
              - register_page()
                - any static callbacks in pages files are registered (Providers)

          @self.server.before_first_request
          def router()

[app.run_server()](server.py#35)
  flask.try_trigger_before_first_request_functions:
    [validate_pages()](dash_pages.py#161)
    [_setup_server()](dash.py#1271)
      GLOBAL_CALLBACK_LIST.clear()


    [dash.router()](dash.py#2026)
