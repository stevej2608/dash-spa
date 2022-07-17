from dash_svg import Svg, Path

# heroicons: https://heroicons.dev/

ARROW = Svg([
        Path(fillRule='evenodd', d='M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z', clipRule='evenodd')
    ], className='icon icon-sm', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')


DOWN_ARROW = Svg([
        Path(fillRule='evenodd', d='M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z', clipRule='evenodd')
    ], className='icon icon-xs ms-1', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

PLUS = Svg([
        Path(strokeLinecap='round', strokeLinejoin='round', strokeWidth='2', d='M12 6v6m0 0v6m0-6h6m-6 0H6')
    ], className='icon icon-xs me-2', fill='none', stroke='currentColor', viewBox='0 0 24 24', xmlns='http://www.w3.org/2000/svg')
