

def background_img(url, width=0, height=0):
    if width or height:
        return {
            "background": f'rgba(0, 0, 0, 0) url("{url}") repeat scroll 0% 0%',
            "background-size" : f'{height}px {width}px'
            }
    else:
        return {"background": f'rgba(0, 0, 0, 0) url("{url}") repeat scroll 0% 0%'}
