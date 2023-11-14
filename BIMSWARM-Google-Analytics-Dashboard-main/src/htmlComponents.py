from dash import html


def totalCard(label: str, value, suffix: str = None, id: str = None):
    value = str(value) + (suffix if suffix is not None else "")
    return html.Div(
        className="total-card-wrapper",
        children=html.Div(
            className="total-card",
            children=[
                html.P(
                    className="title",
                    children=label
                ),
                html.P(
                    className="total-value",
                    children=value,
                    id=id
                )
            ]
        )
    )


def totalCardsWrapper(children):
    return html.Div(
        className="total-cards-wrapper",
        children=children
    )


def graphCard(title: str, children):
    return html.Div(
        className="col-xs-12 col-md-6",
        children=html.Div(
            className="graph-card",
            children=[
                html.P(
                    className="title",
                    children=title
                ),
                children
            ]
        )
    )


def mapCard(title: str, dropDown, map):
    return html.Div(
        className="col-xs-12",
        children=html.Div(
            className="map-card",
            children=[
                html.Div(
                    className="title",
                    children=title,
                ),
                html.Div(
                    className="dropdown-wrapper",
                    children=dropDown
                ),
                html.Div(
                    className="map-wrapper",
                    children=map
                )
            ]
        )
    )
