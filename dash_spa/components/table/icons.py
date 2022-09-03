from dash_svg import Svg, Path

from dash_spa import add_style


icon_style = """
    .icon {
        height: 2rem;
        }
    .icon.icon-xxs {
        height: 1rem;
        }
    .icon.icon-xs {
        height: 1.25rem;
        }
    .icon.icon-sm {
        height: 1.5rem;
        }
"""

add_style(icon_style)

# heroicons: https://heroicons.dev/

SEARCH = Svg([
        Path(fillRule='evenodd', d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z', clipRule='evenodd')
    ], className='icon icon-xs', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 20 20', fill='currentColor')
