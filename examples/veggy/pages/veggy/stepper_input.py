from dash import html, dcc
from dash_spa import prefix, callback, isTriggered, copy_factory

class StepperInput(html.Div):
    def __init__(self, id):
        pid = prefix(id)

        add_btn = html.A("+", className='increment', id=pid('add'))
        remove_btn = html.A("–", className='decrement', id=pid('remove'))
        input_number = dcc.Input(type='number', className='quantity', value='1', id=pid('input'))

        @callback(input_number.output.value,
                  add_btn.input.n_clicks,
                  remove_btn.input.n_clicks,
                  input_number.state.value,
                  prevent_initial_call=True)
        def add_cb(add_clicks, remove_clicks, value):
            try:
                count = int(value)
                if isTriggered(add_btn.input.n_clicks):
                    count += 1
                elif isTriggered(remove_btn.input.n_clicks):
                    if count > 1: count -= 1
                return str(count)
            except Exception:
                return value

        super().__init__([remove_btn, input_number, add_btn], className='stepper-input')
        copy_factory(input_number, self)
