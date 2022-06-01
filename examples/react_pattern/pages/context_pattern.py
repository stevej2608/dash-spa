from dash import html, callback
from dash_spa import prefix, register_page, NOUPDATE

from .context import createContext, useContext

# https://www.netlify.com/blog/2019/03/11/deep-dive-how-do-react-hooks-really-work/

register_page(__name__, path='/', title="React Pattern", short_name='React')

GROUP_1 = 'group_1'
GROUP_2 = 'group_2'

state = {
    GROUP_1: {'btn1': 0, 'btn2': 0},
    GROUP_2: {'btn1': 0, 'btn2': 0}
    }

ButtonContext = createContext(state, id='store');

def button_group(gid):
    pfx = prefix(gid)
    ctx = useContext(ButtonContext);

    title = html.H4(f"Button {gid}")
    btn1 = html.Button("Button1", id=pfx('btn1'))
    btn2 = html.Button("Button2", id=pfx("btn2"))

    props = ctx.props[gid]

    msg = ""
    if 'btn1' in props:
        msg += f"Button 1 pressed {props.btn1} times "

    if 'btn2' in props:
        msg += f"Button 2 pressed {props.btn2} times "

    container = html.Div(msg)

    @ctx.On(btn1.input.n_clicks)
    def btn1_update(clicks):
        if clicks:
            ctx.props[gid].btn1 += 1

    @ctx.On(btn2.input.n_clicks)
    def btn2_update(clicks):
        if clicks:
            ctx.props[gid].btn2 += 1


    return html.Div([title, btn1, btn2, container, html.Br()])


@ButtonContext.Provider()
def layout_page():
    ctx = useContext(ButtonContext);

    group1 = button_group(GROUP_1)
    group2 = button_group(GROUP_2)

    button_view = html.Div("Press a button", id='button_view')

    @callback(button_view.output.children, ctx.input.data)
    def view_cb(store):
        groups = [html.H4(f"{key} {item}") for key, item in store.items()]
        return groups

    title = html.H3('React.js Context Example')

    return html.Div([title, group1, group2, button_view])


layout = layout_page()
