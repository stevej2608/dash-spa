from dash_svg import Svg, Path

class ICON:

    GEAR = Svg([
            Path(fillRule='evenodd', d='M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z', clipRule='evenodd')
        ], className='icon icon-sm', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

    PLUS = Svg([
            Path(strokeLinecap='round', strokeLinejoin='round', strokeWidth='2', d='M12 6v6m0 0v6m0-6h6m-6 0H6')
        ], className='icon icon-xs me-2', fill='none', stroke='currentColor', viewBox='0 0 24 24', xmlns='http://www.w3.org/2000/svg')

    TICK = Svg([
            Path(fillRule='evenodd', d='M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z', clipRule='evenodd')
        ], className='icon icon-xxs ms-auto', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

    SEARCH = Svg([
            Path(fillRule='evenodd', d='M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z', clipRule='evenodd')
        ], className='icon icon-xs', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 20 20', fill='currentColor')

    DOCUMENT = Svg([
            Path(fillRule='evenodd', d='M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z', clipRule='evenodd')
        ], className='dropdown-icon text-gray-400 me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

    class MESSAGE:
        _Path = Path(fillRule='evenodd', d='M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z', clipRule='evenodd')

        ME2 = Svg(_Path, className='dropdown-icon text-gray-400 me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
        ME2_XXS = Svg(_Path, className='icon icon-xxs me-2', viewBox='0 0 20 20', fill="currentColor", xmlns='http://www.w3.org/2000/svg')

    UPLOAD = Svg([
            Path(d='M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z'),
            Path(d='M9 13h2v5a1 1 0 11-2 0v-5z')
        ], className='dropdown-icon text-gray-400 me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

    class FIRE:
        _Path = Path(fillRule='evenodd', d='M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z', clipRule='evenodd')

        ME2 = Svg(_Path, className='icon icon-xs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
        ME2_DANGER = Svg(_Path, className='dropdown-icon text-danger me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
        LG = Svg(_Path, className='icon icon-lg text-gray-200', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
