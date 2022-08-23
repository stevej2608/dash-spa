## [1.1.0] - August 28th, 2022

### Added

- Upgraded to Dash 2.6.1
- Added sidebar example
- Wrapped SPA_LOCATION in a LocalProxy
- CSS dynamic styles now working
- Added Veggy example
- Added Alerts & Notifications example
- Added add_external_stylesheets() and add_external_scripts(). This allows any module to add additional js and css to improve Dash component modularity
- Added session persistence to ContextState
- Added session context

## [1.0.1] - May 5th, 2022

This is complete rewrite. The previous Flask style blueprints have been abandoned. DashSPA now uses the Dash/Pages plugin.

### Added

- ContextState now handles lists & dicts
- Added sync lock to SessionCookieManager
- Added PostgresSessionBackend - Not tested yet!
- Added session cookies Getting session cookie inititialisation to work
- Added Session redis
- Transaction table now tracks the address bar query-string values
- Table search & pagination working
- Moved to using @dataclass for ContextState
- Added context/state pattern
- Added table search
- Added table paginator
- Added table component
- Added table size dropdown





