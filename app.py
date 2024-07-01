# dashboard.py

from flask import Flask
from dash import dcc, html
import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from nat_simulation import simulate_traffic, get_packets_log
import threading
import time
import signal
import sys

# Inicializa o servidor Flask
server = Flask(__name__)

# Inicializa o aplicativo Dash
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Variável para controlar a execução do thread de simulação
running = True

# Layout do Dashboard
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("NAT Dashboard", className="text-center mt-3 mb-3"))),
        dbc.Row(dbc.Col(html.Div(id='live-update-text', className="text-center mb-3"))),
        dcc.Interval(
            id='interval-component',
            interval=2*1000,  # atualiza a cada segundo
            n_intervals=0
        )
    ],
    fluid=True
)

# Callback para atualizar o log de pacotes em tempo real
@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_packets_log(n):
    packets = get_packets_log()
    return html.Table(
        [html.Tr([html.Th("Global Entry"), html.Th("Local Entry"), html.Th("Global Exit"), html.Th("Local Exit")])] +
        [html.Tr([html.Td(packet[0]), html.Td(packet[1]), html.Td(packet[2]), html.Td(packet[3])]) for packet in packets],
        style={'width': '100%', 'borderCollapse': 'separate', 'borderSpacing': '10px', 'textAlign': 'center'}
    )

# Função para rodar a simulação de tráfego em um thread separado
def run_simulation():
    while running:
        simulate_traffic()
        time.sleep(1)

def signal_handler(sig, frame):
    global running
    print("Encerrando...")
    running = False
    sys.exit(0)

if __name__ == '__main__':
    # Configura o handler para sinal de interrupção
    signal.signal(signal.SIGINT, signal_handler)

    # Inicia o thread da simulação
    simulation_thread = threading.Thread(target=run_simulation)
    simulation_thread.daemon = True
    simulation_thread.start()

    # Inicia o servidor Flask/Dash
    app.run_server(debug=True)
