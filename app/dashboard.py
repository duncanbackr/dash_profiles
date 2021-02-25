import dash
import dash_auth
from main.dropdown_layout import dropdown_layout
# from main.dashboard import dashboard_layout
from app.config import Auth


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server)
        #external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    dash_app.layout = dropdown_layout()
    # auth = dash_auth.BasicAuth(dash_app,
    #                             [[Auth.VALID_USERNAME, Auth.VALID_PASSWORD]])

    @dash_app.callback(dash.dependencies.Output('display-value', 'children'),
                       [dash.dependencies.Input('dropdown', 'value')])
    def display_value(value):
        return {'success': 'I am in the display value'} #dashboard_layout(user=value) if value else 'Select Creator'
    return dash_app.server
