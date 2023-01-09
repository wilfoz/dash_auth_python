from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash

from app import *

card_style = {
    "width": "300px",
    "min-height": "300px",
    "padding-top": "25px",
    "padding-right": "25px",
    "padding-left": "25px",
    "align-self": "center",
}

def render_layout(message):
    message = "Ocorreu algum erro durante o registro." if message == "error" else message

    register = dbc.Card([
        html.Legend("Registro"),
        dbc.Input(id="user_register", placeholder="Username", type="text"),
        dbc.Input(id="pwd_register", placeholder="Password", type="password"),
        dbc.Input(id="email_register", placeholder="E-mail", type="email"),
        dbc.Button("Registrar", id="register_button"),
        html.Span(message, style={"text-align": "center"}),
        html.Div([
            html.Label("Ou", style={"margin-right": "5px"}),
            dcc.Link("faça login", href="/login"),
        ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

    ], style=card_style)
    return register

@app.callback(
    Output('register-state', 'data'),
    Input('register_button', 'n_clicks'),
    [
        State('user_register', 'value'),
        State('pwd_register', 'value'),
        State('email_register', 'value'),
    ]
)
def register(n_clicks, username, password, email):
    if n_clicks == None:
        raise PreventUpdate
    
    if username is not None and password is not None and email is not None:
        hashed_password = generate_password_hash(password, method='sha256')
        ins = Users_table.insert().values(username=username, password=hashed_password, email=email)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return ''
    else:
        return 'error'