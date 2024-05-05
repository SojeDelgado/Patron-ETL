##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: dashboard.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define los elementos visuales de la pantalla
#   del tablero
#
#-------------------------------------------------------------------------
from src.controller.dashboard_controller import DashboardController
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State

class Dashboard:

    def __init__(self):
        self.controller = DashboardController()

    def register_callbacks(self, app):
        @app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs', 'value')]
        )
        def render_content(tab):
            if tab == 'sales':
                return self._sales_tab_content()
            elif tab == 'stats':
                return self._stats_tab_content()
            elif tab == 'period_sales':
                return self._period_sales_tab_content()

        @app.callback(
            Output('period-sales-report', 'children'),
            [Input('generate-report-btn', 'n_clicks')],
            [State('date-picker-range', 'start_date'),
            State('date-picker-range', 'end_date')]
        )
        def generate_period_sales_report(n_clicks, start_date, end_date):
            if n_clicks is not None and start_date is not None and end_date is not None:

                products = DashboardController.load_sales_per_date(start_date, end_date)

                return html.Div([
                    html.H3('Period Sales Report'),
                    dbc.Row([
                        dbc.Col(self._panel_sales_per_period(start_date, end_date), width=6),
                        dbc.Col(self._panel_product_per_period(start_date, end_date), width=6)
                    ])
                ])

            
    def _sales_tab_content(self):
        return html.Div([
            self._bar_chart_sales_per_location(),
            self._bar_chart_orders_per_location(),
            self._bar_chart_providers_by_location()
        ])
    
    def _stats_tab_content(self):
        return html.Div([
            dbc.Row([
                dbc.Col(self._panel_best_sellers(), width=6),
                dbc.Col(self._panel_worst_sales(), width=6),
            ]),
            html.Div(),
            html.Br(),
            dbc.Row(
                [dbc.Col(self._panel_most_selled_products())]
            )
        ])
    
    def _period_sales_tab_content(self):
        return html.Div(style={'text-align': 'center'}, children=[
            html.Br(),
            html.Label('Select Period:', style={'text-align': 'center'}),
            dcc.DatePickerRange(
                id='date-picker-range',
                display_format='YYYY-MM-DD',
                start_date_placeholder_text='Start Period',
                end_date_placeholder_text='End Period'
            ),
            html.Button('Generate Report', id='generate-report-btn', className='btn btn-primary'),
            html.Div(style={'text-align': 'start'},id='period-sales-report')
        ])

    def document(self, app):
        self.register_callbacks(app)
        return dbc.Container(
            fluid = True,
            children = [
                html.Br(),
                self._header_title("Sales Report"),
                html.Div(html.Hr()),
                self._header_subtitle("Sales summary financial report"),
                html.Br(),
                self._highlights_cards(),
                html.Br(),
                dcc.Tabs(id='tabs', value='sales', children=[
                    dcc.Tab(label='Sales per Location', value='sales'),
                    dcc.Tab(label='Best, Worst, Most Sold', value='stats'),
                    dcc.Tab(label='Sales per Period', value='period_sales')
                ]),
                html.Div(id='tabs-content')
            ]
        )

    def _header_title(self, title):
        return dbc.Row(
            [
                dbc.Col(html.H2(title, className="display-4"))
            ]
        )

    def _header_subtitle(self, subtitle):
        return html.Div(
            [
                html.P(
                    subtitle,
                    className="lead",
                ),
            ],
            id="blurb",
        )

    def _card_value(self, label, value):
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H2(value, className="card-title"),
                    ]
                ),
                dbc.CardFooter(label),
            ]
        )

    def _highlights_cards(self):
        products = DashboardController.load_products()
        orders = DashboardController.load_orders()
        providers = DashboardController.load_providers()
        locations = DashboardController.load_locations()
        sales = DashboardController.load_sales()
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            self._card_value("Products", products["products"])
                        ),
                        dbc.Col(
                            self._card_value("Orders", orders["orders"])
                        ),
                        dbc.Col(
                            self._card_value("Providers", providers["providers"])
                        ),
                        dbc.Col(
                            self._card_value("Locations", locations["locations"])
                        ),
                        dbc.Col(
                            self._card_value("Sales", "$ {:,.2f}".format(float(sales['sales'])))
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_providers_by_location(self):
        data = DashboardController.load_providers_per_location()
        bar_char_fig = px.bar(data, x="location", y="providers")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Providers per location", className="card-title"),
                        dcc.Graph(
                            id='providers-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_sales_per_location(self):
        data = DashboardController.load_sales_per_location()
        bar_char_fig = px.bar(data, x="location", y="sales")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Sales per location", className="card-title"),
                        dcc.Graph(
                            id='sales-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _bar_chart_orders_per_location(self):
        data = DashboardController.load_orders_per_location()
        bar_char_fig = px.bar(data, x="location", y="orders")
        return dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H3("Orders per location", className="card-title"),
                        dcc.Graph(
                            id='orders-per-location',
                            figure=bar_char_fig
                        ),
                    ]
                ),
            ]
        )

    def _panel_best_sellers(self):
        best_sellers = DashboardController.load_best_sellers()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Best sellers", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in best_sellers
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_worst_sales(self):
        worst_sales = DashboardController.load_worst_sales()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Worst sales", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- [{sale['invoice']}] $ {sale['total']:,.2f}", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in worst_sales
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _panel_most_selled_products(self):
        most_selled = DashboardController.load_most_selled_products()
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Most selled", className="card-title"),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"- {product['product']} [{product['times']} time(s) sold]", style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for product in most_selled
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _panel_sales_per_period(self, start_date_str, end_date_str):
        sales_per_period = DashboardController.load_sales_per_date(start_date_str, end_date_str)
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Sales", className="card-title"),
                                html.P(f'Start Date: {start_date_str}, End Date: {end_date_str}'),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"-----[{sale['date'].split('T')[0]}]-----",style={"font-weight":"bold"}),
                                                        html.Div(
                                                            [
                                                                html.H5(f"\t{product['description']}, {product['price']}", style={"font-weight":"bold"})
                                                                for product in sale['product']
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in sales_per_period
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _panel_product_per_period(self, start_date_str, end_date_str):
        product_per_period = DashboardController.load_product_per_date(start_date_str, end_date_str)
        return html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.H3("Best Products", className="card-title"),
                                html.P(f'Start Date: {start_date_str}, End Date: {end_date_str}'),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H5(f"-[Quantity:{sale['times']}] - {sale['description']}, {sale['date'].split('T')[0]}",style={"font-weight":"bold"}),
                                                    ]
                                                ),
                                            ]
                                        )

                                        for sale in product_per_period
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )