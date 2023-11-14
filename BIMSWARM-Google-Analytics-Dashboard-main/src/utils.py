import dash_mantine_components as dmc
from dash import html

def convertDate(date, df, minDate: bool):
    if date is None:
        if minDate:
            date = df.index.min()
        else:
            date = df.index.max()

    # Reformate les date de fin pour les utiliser dans df.loc
    date = str(date).split(" ")[0]
    date = str(date).split("T")[0]

    return date
def header():
   return dmc.Header(height=60, children=[html.A(
        href="https://bimswarm.online",
        children=[
            html.Img(
                src="./assets/BIMSWARM-Logo.png",
                style={"width":"15vh",}

            )
        ]
    ),dmc.Text("Statistik-Dashboard", style={"color":"white","font-size":"large", "font-weight":"bold", "position":"absolute", "left":"45%", "top":"25%"})], style={"backgroundColor": "#358386","color":"white", "position":"fixed"} )


def footer():
    return dmc.Footer(height='2vh',children=[ html.A('AGB',href= "https://bimswarm.online/agb",style={"color":"white", "left":"100%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              html.A('Impressum',href= "https://bimswarm.online/impressum",style={"color":"white", "left":"95%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              html.A('Datenschutz',href= "https://bimswarm.online/privacy",style={"color":"white", "left":"90%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              html.A('Kontakt',href= "contact@bimswarm.de",style={"color":"white", "left":"85%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              html.A('Produkttypen',href= "https://www.bimswarm.de/produkttypen",style={"color":"white", "left":"80%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              html.A('Newsletter',href= "https://www.bimswarm.de/newsletter-anmeldung",style={"color":"white", "left":"75%", "margin":"0.7vw", "font-weight" :"bold"}),
                                              html.A('Über BIMSWARM',href= "https://www.bimswarm.de/",style={"color":"white", "left":"70%", "margin":"0.7vw", "font-weight" :"bold" }),
                                              ],
        style={"backgroundColor": "#358386","color":"white", "position":"fixed"} )