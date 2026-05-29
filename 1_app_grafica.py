# Ploty: visualización, gráficas, etc.
# Dash: herramienta para habilitar la comunicación entre componentes interactivos de un dashboard
# * maneja 3 conceptos básicos para una app
# 1. **Componentes**: botones, filtros, gráficas, etc.
# 2. **Layout**: permite indicar cómo acomodar los elementos en la app
# 3. **Callback**: la programación interna que permite la interactividad

from dash import Dash, dcc, html, Input, Output
# python3 -m pip install dash

import dash_bootstrap_components as dbc 
# python3 -m pip install dash-bootstrap-components

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# 1. CARGA DE DATOS
df = pd.read_csv('sleep_deprivation_dataset_detailed.csv')

# Paleta de colores personalizada, para que se aplique globalmente a todas las gráficas
triada = ['#2baf9d', '#9d2baf', '#af9d2b']
analogos = ['#2baf9d', '#2b7faf', '#2baf5b']
complementarios_divididos = ['#2baf9d', '#332baf', '#af682b']
monocromaticos = ['#00493c', '#0a6556', '#178172', '#24a08e', '#43baaa', '#6ad1c6', '#8de8e2', '#aeffff']
complementario = ['#2baf9d', '#af2b3d']

#---------------------------------------------
# 2.CONFIGURACIÓN DE Aplicación
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# 3. COMPONENTES DE LA INTERFAZ (LAYOUT)
md_title = dcc.Markdown(children='## **DASHboards y Plotly - Privación de sueño**')
md_integrantes = dcc.Markdown(children='Integrantes: **Alina A. Reyes Muñiz | A01752345** & **Montserrat Hernández Pérez | A01276367**')


# > Componente de Entrada
dropdown_graficas = dcc.Dropdown(options=[
        {'label': 'Gráfico 1: Nivel de Actividad Física', 'value': 'graf1'},
        {'label': 'Gráfico 2: Daytime Sleepiness por Género', 'value': 'graf2'},
        {'label': 'Gráfico 3: Sueño, precisión cognitiva y regulación emocional', 'value': 'graf3'},
        {'label': 'Gráfico 4: Daytime Sleepiness promedio por grupo de edad y género', 'value': 'graf4'},
        {'label': 'Gráfico 5: Horas de sueño vs tiempo de reacción (PVT)', 'value': 'graf5'},
        {'label': 'Gráfico 6: Relación entre Sleep_Quality_Score & Emotion_Regulation_Score', 'value': 'graf6'},
        {'label': 'Gráfico 7: Relación entre variables del sueño, consumo de cafeína, niveles de estrés y regulación emocional, según la edad', 'value': 'graf7'},
        {'label': 'Gráfico 8: Diferencias entre los puntajes de regulación emocional de hombres y mujeres', 'value': 'graf8'},
        {'label': 'Gráfico 9: Nivel de estrés vs. Retención temporal de información', 'value': 'graf9'},
        {'label': 'Gráfico 10: Calidad de Sueño de acuerdo a Consumo de Cafeína (bajo, intermedio, alto), comparación entre mujeres y hombres', 'value': 'graf10'},
    ],
    value='graf1', # Gráfica que se muestra por defecto al cargar la app
    clearable=False
)


# > Componente de Salida
grafica_output = dcc.Graph(figure={}) # vacío porque su valor depende del callback
markdown_output = dcc.Markdown(children='') # Texto explicativo que depende del callback


# > Layout
app.layout = dbc.Container([
    html.Br(),
    md_title,
    md_integrantes,
    html.Hr(),
    html.Label("Selecciona una gráfica (10 posibles gráficas):"),
    dropdown_graficas,
    html.Br(),
    grafica_output,
    html.Br(),
    markdown_output,
    html.Br()
], fluid=True)

# 4. CALLBACK
@app.callback(
    [Output(grafica_output, component_property='figure'),
     Output(markdown_output, component_property='children')],
    [Input(dropdown_graficas, component_property='value')]
)
def update_dashboard(selected_graph):
    # Inicializamos variables
    fig = go.Figure()
    texto_contexto = ""

    # ---- GRÁFICO 1 ----
    if selected_graph == 'graf1':
        df["Activity_Group"] = pd.cut(df["Physical_Activity_Level"],
                                bins=[-1, 3, 6, 10],
                                labels=["Bajo (0–3)", "Medio (4–6)", "Alto (7–10)"])
        activity_counts = df["Activity_Group"].value_counts().sort_index()
        
        fig = go.Figure(data=[go.Pie(labels=activity_counts.index.tolist(),
                values=activity_counts.values.tolist(), hole=0.40,
                marker_colors=['#2baf9d', '#2b7faf', '#2baf5b'],
                textinfo="percent", hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
                name="Actividad")])
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')
        fig.update_layout(title_text="> Nivel de actividad física")
        #fig.show()

        # Descripción
        texto_contexto = """
        **Descripción:** Este gráfico de dona nos muestra el grupo en el que se encuentran las personas 
        dependiendo de su actividad física. Podemos ver que la mayoría tiene un nivel bajo-medio de actividad 
        física. Solo el 21.7% tiene un nivel alto, lo que puede afectar la calidad del sueño."""



    # ---- GRÁFICO 2 ----
    elif selected_graph == 'graf2':
        fig = px.violin(df, x='Gender', y='Daytime_Sleepiness', box=True, points='all',
                  color='Gender', color_discrete_sequence=complementario,
                  title='> Daytime Sleepiness por Género')

        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')
        #fig.show()
        texto_contexto = """
        **Descripción:** con los gráficos de violín buscamos observar la distribución por género de la somnolencia 
        (necesidad de dormir) durante el día. Podemos ver que la distribución para las mujeres, se encuentra mayormente 
        en la parte baja, con menos tendencia a experimentar esto. Por el contrario los hombres tienden a presentar sueño 
        en mayores valores.
        """

    # ---- GRÁFICO 3 ----
    elif selected_graph == 'graf3':
        fig = px.scatter(df, x='Sleep_Hours', y='N_Back_Accuracy',
                   size='Emotion_Regulation_Score', color='BMI',
                   color_continuous_scale=monocromaticos,
                   title='> Sueño, precisión cognitiva y regulación emocional')
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')
        #fig.show()
        texto_contexto = """
        **Descripción:** Esta gráfica muestra la relación entre horas de sueño y memoria de trabajo (N-Back). El tamaño del 
        punto indica regulación emocional y el color el IMC de cada persona. No hay una tendencia lineal clara, lo que sugiere 
        que la precisión cognitiva depende de múltiples factores más allá del sueño.
        """

    # ---- GRÁFICO 4 ----
    elif selected_graph == 'graf4':
        bins = [18, 25, 35, 45]
        labels = ['18-25', '26-35', '36-45']
        df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False, include_lowest=True)
        # 1. Agregar los datos primero
        graf4_data = df.groupby(["Age_Group", "Gender"], observed=True)["Daytime_Sleepiness"].mean().round(1).reset_index()

        fig = px.bar(graf4_data, x="Age_Group", y="Daytime_Sleepiness",
                color="Gender", barmode="group",
                color_discrete_sequence=complementario,
                category_orders={"Age_Group": labels, "Gender": ["Male", "Female"]},
                text="Daytime_Sleepiness",                    # 2. Mostrar el valor encima de cada barra
                labels={"Age_Group": "Grupo de edad",
                        "Daytime_Sleepiness": "Daytime Sleepiness (promedio)",
                        "Gender": "Género"},
                title="> Daytime Sleepiness promedio por grupo de edad y género")

        # 4. Etiquetas encima de las barras
        fig.update_traces(textposition="outside", textfont_size=12)

        # 5. Escala del eje Y con margen para que no se corten las etiquetas
        fig.update_yaxes(range=[0, graf4_data["Daytime_Sleepiness"].max() * 1.25])

        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')
        #fig.show()
        texto_contexto = """
        **Descripción:** Aquí se dividieron las edades de los registrados en grupos de 18 a 25, 26 a 35, 
        y 36 a 45. Además, se separan por género, donde podemos ver que en dos de los grupos existen más 
        hombres en promedio, con valores altos de presentar somnolencia durante el día. De hecho, en el grupo 
        de 36 a 45 se puede ver una diferencia clara de más de 6 puntos, que los hombres experimentan esto más 
        que las mujeres. Mientas que en el grupo medio de 26 a 35 años de edad, las mujeres lo presentan más, 
        aunque la diferencia es menor a 2 puntos.
        """

    # ---- GRÁFICO 5 ----
    elif selected_graph == 'graf5':
        fig = px.scatter(df, x='Sleep_Hours', y='PVT_Reaction_Time',
                 color='Gender', size='Stress_Level', color_discrete_sequence=complementario,
                    title='> Horas de sueño vs tiempo de reacción (PVT)')

        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')
        #fig.show()
        texto_contexto = """
        **Descripción:** Este scatter plot pretende mostrar la relación entre las horas de sueño y el tiempo de 
        reacción de cada persona, se puede ver la diferencia de género por color y el tamaño de cada punto referencia 
        al nivel de estrés de cada persona. Se espera que entre un mayor descanso, se tendría que tener un mejor tiempo 
        de reacción. Podemos ver que esta relación no se cumple perfectamente, pero si tenemos más valores con tiempos 
        de reacción altos en las personas que descansaron menos. El nivel de estrés se ve más disperso, no mostrando una 
        relación, así como el género.
        """

    # ---- GRÁFICO 6 ----
    elif selected_graph == 'graf6':
        fig = px.scatter(df, x='Sleep_Quality_Score', y='Emotion_Regulation_Score',
                color='Gender', color_discrete_sequence=complementario, # doy color a cada punto segun genero
                title='> Relación entre Sleep_Quality_Score & Emotion_Regulation_Score')
        # Para el color del fondo y letras
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')

        # Para el tamaño de los círculos
        fig.update_traces(marker_size=15)

        #fig.show()
        texto_contexto = """
        **Descripción:** Esta gráfica de dispersión muestra la relación entre el puntaje de la calidad del sueño (0-20) y el 
        puntaje de la regulación emocional (10-70). El color de los círculos indica el género. A simple vista, se puede distinguir 
        que para la menor calidad de sueño (entre 0 y 5), los hombres son los que se posicionan con la regulación emocional más alta.
        Al dividir el eje de la calidad de sueño, se puede apreciar que hay una mayor concentración de participantes, tanto hombres 
        como mujeres, entre la calidad de sueño con puntaje de 5 a 15. Mientras que en la calidad de sueño entre 15 y 20, se concentran 
        muy pocas mujeres (3) comparadas con la cantidad de hombres (5), quienes también presentan una mejor regulación emocional en este 
        rango de calidad de sueño.
        """

    # ---- GRÁFICO 7 ----
    elif selected_graph == 'graf7':
        variables = ['Sleep_Hours', 'Sleep_Quality_Score', 'Caffeine_Intake', 'Stress_Level', 'Emotion_Regulation_Score', 'Age']

        fig = px.parallel_coordinates(df, dimensions=variables, color='Age', color_continuous_scale=monocromaticos,
                labels={'Age': 'Age'}, title='> Relación entre variables del sueño, consumo de cafeína, niveles de estrés y regulación emocional, según la edad')

        # Para el color del fondo y letras
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')

        #fig.show()
        texto_contexto = """
        **Descripción:** En esta gráfica de coordenadas paralelas, se están comparando el comportamiento de los participantes (tanto hombres 
        como mujeres), analizando la realación entre las horas de sueño, el puntaje de la calidad de sueño, su consumo de café, nivel de estrés, 
        puntaje de regulación emocional y como variable de 'salida', la edad de cada partipante del estudio (de 18 a 43 años). De esta manera, 
        lo más importante a resaltar es que quienes tuvieron más de 7 horas de sueño y una calidad de sueño mayor a 15, tienen una edad de entre 
        18 a 23 aproximadamente (además de un participante de 34 años). Por otro lado, el consumo de cafeína no se comporta de una manera específica 
        para cada rango de edad u horas de sueño, sino que todos presentan una cantidad muy variada de consumo de cafeína: los participantes que 
        durmieron menos de 4.5 horas, presentan tanto un consumo de cafeína muy alto, como muy bajo, al igual que quienes durmieron más de 7 horas. 
        El mismo comportamiento sucede entre la relación del consumo de cafeína y los niveles de estrés, así como la regulación emocional.
        """

    # ---- GRÁFICO 8 ----
    elif selected_graph == 'graf8':
        fig = px.histogram(df, x='Emotion_Regulation_Score',
                color='Gender', color_discrete_sequence=complementario,
                marginal='rug', facet_col='Gender',
                title='> Diferencias entre los puntajes de regulación emocional de hombres y mujeres')

        # Para el color del fondo y letras
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')

        #fig.show()
        texto_contexto = """
        **Descripción:** En estos histogramas, sólo se está comparando el comportamiento de los participantes, mujeres y hombres, con respecto a su 
        regulación emocional (con puntajes de 0 a 70). Como se puede apreciar, las mujeres tienen una menor regulación emocional, la mayoría concentrándose 
        entre los puntajes 30 y 40. Por el otro lado, la mayoría de los hombres se concentran entre los puntajes 20 y 30 y 60 y 70. Estos resultados pueden 
        ser justificados considerando el ciclo menstrual de las mujeres, donde las hormonas cambian constantemente cada 28 días, a lo largo de las 4 fases 
        (menstruación, fase folicular, fase ovulatoria y fase lútea).
        """

    # ---- GRÁFICO 9 ----
    elif selected_graph == 'graf9':
        fig = px.scatter(df, x='N_Back_Accuracy', y='Stress_Level', hover_name='Gender', hover_data=['Age'],
                color='Stress_Level', color_continuous_scale=complementarios_divididos, opacity=1,
                title='> Nivel de estrés vs. Retención temporal de información')

        # Para el color del fondo y letras
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')

        # Para el tamaño de los círculos
        fig.update_traces(marker_size=15)

        #fig.show()
        texto_contexto = """
        **Descripción:** En esta gráfica de dispersión, se está comparando la relación entre el nivel de estrés y la retención temporal de información 
        (N_Back_Accuracy), tanto de hombres como de mujeres. Como se puede identificar, los participantes que tuvieron un nivel de estrés mayor o igual 
        que 35 (puntos color café), presentan puntajes de retención de información de entre 60 y 90 (aunque hay una persona que presenta altos niveles 
        de estrés, pero tiene una retención de información mayor a 90). Mientras los que tienen un nivel de estrés bajo-medio, de entre 0 y 30, presentan 
        una retención de información mucho mejor, alcalzando el puntaje de casi 100. Esto demuestra que el nivel de estrés afecta la retención de información 
        y la memoria a corto plazo.
        """

    # ---- GRÁFICO 10 ----
    elif selected_graph == 'graf10':
        # Para hacer rangos de la variable 'Caffeine_Category'
        df['Caffeine_Category'] = df['Caffeine_Intake'].apply(lambda x: 'Bajo (<1)' if x < 2 else ('Alto (>4)' if x > 4 else 'Intermedio (2-4)'))

        # Para definir el orden de las nuevas categorías
        orden_categorias = {"Caffeine_Category": ['Bajo (<1)', 'Intermedio (2-4)', 'Alto (>4)']}

        fig = px.violin(df, x='Caffeine_Category', y='Sleep_Quality_Score',
                 color='Gender', color_discrete_sequence=complementario, points='all',
                 category_orders=orden_categorias,
                 title='> Calidad de Sueño de acuerdo a Consumo de Cafeína (bajo, intermedio, alto), comparación entre mujeres y hombres')

        # Para el color del fondo y letras
        fig.update_layout(plot_bgcolor='#808080', paper_bgcolor='#808080', font_color='white')

        # Para que la escala del eje y comience desde el 0, que es donde comienzan los datos de la variable
        fig.update_traces(spanmode='hard')

        #fig.show()
        texto_contexto = """
        **Descripción:** En esta gráfica de violines, se muestra la comparación entre el comportamiento de mujeres y hombres, con respecto a su consumo de 
        cafeína (bajo, intermedio y alto) y la calidad de sueño. Como se puede ver, las mujeres que consumieron altas cantidades de cafeína durante el día (> 4), 
        se concentraron entre la calidad de sueño de 0 a 6, mientras que los hombres entre 0 y 14. Como contraste, quienes consumieron menores cantidades de 
        cafeína (< 1), tanto mujeres como hombres, obtuvieron una calidad de sueño más variada, de entre 0 a 18. De la misma manera, quienes consumieron una cantidad 
        de cafeína intermedia (2 - 4), también obtuvieron una calidad de sueño variada, de entre 0 a 20.
        """
    # Devolvemos ambos objetos: la figura actualizada y el texto formateado en Markdown
    return fig, texto_contexto


# 5. EJECUCIÓN DE LA APP
if __name__ == '__main__':
    app.run(port=8051, debug=True)

# -------------------------------------------------------
# Preparar una nueva version de esta app donde cargues un dataframe diferente y muestres 3 graficas
# px.data.iris()
# px.data.gapminder()
# px.data.election()