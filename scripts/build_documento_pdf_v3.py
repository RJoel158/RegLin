import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register robust Windows TrueType fonts to ensure zero missing glyphs
pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', r'C:\Windows\Fonts\arialbd.ttf'))
pdfmetrics.registerFont(TTFont('ArialItalic', r'C:\Windows\Fonts\ariali.ttf'))
pdfmetrics.registerFont(TTFont('ArialBoldItalic', r'C:\Windows\Fonts\arialbi.ttf'))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold', italic='ArialItalic', boldItalic='ArialBoldItalic')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = A4
        # Draw header on all pages
        if os.path.exists("logo_cube.png"):
            self.drawImage("logo_cube.png", 36, h - 56, width=54, height=42, preserveAspectRatio=True, mask='auto')
        if os.path.exists("logo_seal.png"):
            self.drawImage("logo_seal.png", w - 80, h - 56, width=44, height=42, preserveAspectRatio=True, mask='auto')
        
        self.setFont("ArialBold", 11)
        self.setFillColor(colors.HexColor("#1A1A1A"))
        self.drawCentredString(w / 2.0, h - 28, "UNIVERSIDAD DEL VALLE")
        self.setFont("ArialBold", 9)
        self.setFillColor(colors.HexColor("#333333"))
        self.drawCentredString(w / 2.0, h - 42, "LI21 - Exposición con demostración de un caso ejemplo con regresión lineal con DATASET")
        
        # Header separator
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.6)
        self.line(36, h - 60, w - 36, h - 60)

        # Footer
        self.setFont("Arial", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(36, 20, "Estudiante: Ronald Joel Saavedra Vargas  |  Docente: Lic. Efraín Luna Flores  |  UNIVALLE 2026")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(w - 36, 20, page_str)
        self.line(36, 30, w - 36, 30)
        self.restoreState()

def yellow_box(text, is_sub=False, is_red=False):
    """Callout box with warm pastel yellow highlighter background for prompts."""
    text_color = "#C00000" if is_red else "#1A1A1A"
    style = ParagraphStyle(
        f'YellowPrompt_{is_sub}_{is_red}',
        fontName='ArialBold',
        fontSize=9.2 if not is_sub else 8.7,
        leading=12.5 if not is_sub else 11.8,
        textColor=colors.HexColor(text_color)
    )
    p = Paragraph(text, style)
    t = Table([[p]], colWidths=[523])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF08A')),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor('#EAB308')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t

def equation_box(math_html, font_size=9.8):
    """Elegantly styled formula block."""
    style = ParagraphStyle(
        'EqStyle',
        fontName='Arial',
        fontSize=font_size,
        leading=font_size + 4,
        alignment=1, # Centered
        textColor=colors.HexColor('#0B2545')
    )
    p = Paragraph(math_html, style)
    t = Table([[p]], colWidths=[523])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6F9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
    ]))
    return t

def build_pdf():
    pdf_filename = "LI21_Exposicion_Demostracion_LR_Ronald_Saavedra.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=64,
        bottomMargin=36
    )

    body = ParagraphStyle(
        'Body',
        fontName='Arial',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor("#222222"),
        spaceAfter=3,
        spaceBefore=1
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='ArialBold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Arial',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#222222")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='ArialBold'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=1
    )

    story = []

    # ================= PAGE 1 =================
    story.append(yellow_box("Siga las instrucciones siguientes:"))
    story.append(Spacer(1, 2))

    # Point 1
    story.append(yellow_box("1. Ingresar a la plataforma de Google Colab"))
    p1_text = (
        "Se ingresó a la plataforma oficial en la nube mediante el enlace <b>https://colab.research.google.com/</b>. "
        "Google Colaboratory provee un entorno virtual interactivo basado en Linux con memoria RAM y capacidad de procesamiento dedicada, "
        "lo que permite ejecutar algoritmos de analítica avanzada y flujos distribuidos en Apache Spark de manera fluida y accesible "
        "desde cualquier navegador web, sin requerir instalaciones locales complejas."
    )
    story.append(Paragraph(p1_text, body))
    story.append(Spacer(1, 2))

    # Point 2
    story.append(yellow_box('2. Crear un cuaderno que tenga el siguiente nombre: <font color="#C00000">rsaavedra</font>_lr2.ipynb<br/><font size="7.5" color="#444444">Lo que está en rojo es su letra de primer nombre, seguido de su apellido.</font>'))
    p2_text = (
        "Siguiendo estrictamente el criterio de estandarización docente, se creó el cuaderno con la inicial del primer nombre ('r' de Ronald) "
        "y el apellido del estudiante ('saavedra'), resultando en <b>rsaavedra_lr2.ipynb</b>. Este documento almacena en formato estructurado JSON "
        "la secuencia íntegra de celdas explicativas, transformaciones de datos, entrenamiento del modelo y evaluaciones visuales."
    )
    story.append(Paragraph(p2_text, body))
    story.append(Spacer(1, 2))

    # Point 3
    story.append(yellow_box("3. Mostrar el usuario asociado a su cuaderno de trabajo."))
    story.append(Spacer(1, 1))

    # User's genuine screenshot
    if os.path.exists("evidencia_colab_real_cropped.png"):
        story.append(Image("evidencia_colab_real_cropped.png", width=460, height=170))
        story.append(Spacer(1, 2))

    p3_text = (
        "<b>Evidencia de Identidad Académica:</b> En la captura de pantalla superior se constata la sesión activa en Google Colab con la cuenta "
        "del estudiante <b>Ronald Joel Saavedra Vargas</b> (usuario principal <code>Joel Saavedra Vargas</code>), operando directamente "
        "sobre el cuaderno <b>rsaavedra_lr2.ipynb</b> y mostrando la correcta inicialización del entorno y la ejecución del código."
    )
    story.append(Paragraph(p3_text, body))
    story.append(Spacer(1, 2))

    # Point 4
    p4_prompt = (
        "4. Seleccionar un dataset, NO DEBE REPETIRSE CON OTRO QUE HAYA ELEGIDO ALGUIEN EN LA CLASE "
        "(DECLARAR QUÉ DATASET USARÁ EN EL GRUPO DE WHATSAPP, SE RESPETA EL PRIMERO QUE ENVIÓ EL ENLACE DEL DATASET "
        "SELECCIONADO, CONSIDERE QUE PUEDE MANDAR UN ENLACE DIFERENTE DESDE OTRO DOMINIO Y CONTENER EL MISMO DATASET, "
        "DEBE REVISAR PREVIAMENTE)"
    )
    story.append(yellow_box(p4_prompt, is_red=True))
    p4_text = (
        "Para garantizar total originalidad y rigor, se seleccionó y reservó formalmente en el grupo de WhatsApp el dataset "
        "<b>Combined Cycle Power Plant (CCPP)</b> proveniente del repositorio oficial de la Universidad de California en Irvine (UCI): "
        "<b>https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant</b> (archivo <code>Folds5x2_pp.csv</code>). "
        "Este conjunto registra 9,568 observaciones horarias de una central termoeléctrica real tomadas a lo largo de seis años continuos, "
        "midiendo cuatro variables ambientales para estimar con alta precisión la potencia eléctrica neta producida."
    )
    story.append(Paragraph(p4_text, body))
    story.append(Spacer(1, 2))

    # Point 5
    story.append(yellow_box("5. Aplicar todo lo que ha ejecutado en el LI22"))
    p5_text = (
        "Se aplicó el flujo completo de ingeniería y modelado distribuido con <b>Apache Spark (PySpark MLlib)</b>: "
        "inicialización de la sesión distribuida <code>SparkSession(appName='rsaavedra_lr2')</code>, ingestión estructurada de los datos "
        "verificando la ausencia total de valores nulos, agrupamiento de las características independientes en un vector denso mediante "
        "<code>VectorAssembler</code>, partición controlada 80% entrenamiento y 20% prueba con semilla reproducible (<code>seed=42</code>), "
        "ajuste del modelo lineal multivariado y transformación de las predicciones a tuplas y colecciones RDD para su posterior validación diagnóstica."
    )
    story.append(Paragraph(p5_text, body))

    # ================= PAGE 2 =================
    story.append(PageBreak())

    story.append(yellow_box("6. Preparar una breve presentación explicando los siguientes puntos:"))
    story.append(Spacer(1, 3))

    # 6.a
    story.append(yellow_box("a. Investigue y describa qué es una regresión lineal.", is_sub=True))
    p6a_intro = (
        "La <b>Regresión Lineal</b> es uno de los pilares fundamentales de la estadística y del aprendizaje automático supervisado. "
        "Su propósito es descubrir y cuantificar la relación existente entre una o varias variables explicativas (causas) y una variable "
        "continua de respuesta (efecto). De forma intuitiva, podemos pensar en trazar con una regla la línea recta óptima que pase "
        "lo más cerca posible de una nube de datos dispersos: esa recta nos resume la tendencia general del fenómeno y nos permite "
        "calcular estimaciones confiables sobre eventos futuros reduciendo al mínimo la incertidumbre."
    )
    story.append(Paragraph(p6a_intro, body))
    story.append(Spacer(1, 2))

    # Formula 1
    f1 = "<i>y</i> = &beta;<sub>0</sub> + &beta;<sub>1</sub><i>x</i><sub>1</sub> + &beta;<sub>2</sub><i>x</i><sub>2</sub> + ... + &beta;<sub>n</sub><i>x</i><sub>n</sub> + &epsilon; &nbsp;&nbsp;=&nbsp;&nbsp; <b>x</b><sup>T</sup><b>&beta;</b> + &epsilon;"
    story.append(equation_box(f1))
    story.append(Spacer(1, 2))

    p6a_body1 = (
        "En esta expresión matricial, <i>y</i> simboliza la magnitud continua que buscamos predecir (en nuestro proyecto, los Megawatts producidos), "
        "el vector <b>x</b> agrupa las condiciones climáticas observadas, &beta;<sub>0</sub> representa el <i>intercepto</i> o potencia base esperada "
        "si todas las variables predictoras fueran nulas, y cada coeficiente &beta;<sub>j</sub> mide el impacto marginal individual: "
        "nos indica con exactitud cuánto aumenta o disminuye la energía generada por cada unidad adicional en una variable meteorológica, "
        "asumiendo que las demás permanecen estrictamente constantes (principio de <i>ceteris paribus</i>). Por último, &epsilon; captura "
        "las pequeñas perturbaciones aleatorias y fluctuaciones térmicas no medibles."
    )
    story.append(Paragraph(p6a_body1, body))
    story.append(Spacer(1, 2))

    # Formula 2 - OLS
    f2 = "<b>&beta;</b><sub>OLS</sub> = (<b>X</b><sup>T</sup><b>X</b>)<sup>-1</sup><b>X</b><sup>T</sup><b>y</b>"
    story.append(equation_box(f2))
    story.append(Spacer(1, 2))

    p6a_body2 = (
        "Para trazar la recta más acertada, el algoritmo ajusta los parámetros de tal modo que minimiza la <b>Suma de Cuadrados de los Residuos (RSS)</b>, "
        "es decir, castiga la distancia entre los valores reales medidos en la planta y los pronosticados por el modelo. "
        "Matemáticamente, esto puede resolverse de forma analítica en un solo paso mediante la fórmula de <b>Mínimos Cuadrados Ordinarios (OLS)</b>. "
        "No obstante, en infraestructuras de Big Data como Apache Spark, invertir matrices gigantescas consume demasiada memoria; "
        "por ello, Spark recurre al <b>Descenso de Gradiente (L-BFGS)</b>, un método iterativo que refina progresivamente los coeficientes "
        "siguiendo la pendiente del error hasta converger a la solución matemática óptima de manera distribuida.<br/><br/>"
        "Bajo el <b>Teorema de Gauss-Markov</b>, este estimador garantiza ser el <i>Mejor Estimador Lineal Insesgado (MELI / BLUE)</i> "
        "siempre que se verifiquen cinco supuestos clave: relación lineal en los parámetros, varianza de error uniforme en todo el rango "
        "(homocedasticidad), independencia estocástica entre observaciones consecutivas (sin autocorrelación), normalidad en la distribución "
        "de los residuos (&epsilon; ~ <i>N</i>(0, &sigma;<sup>2</sup>)) y ausencia de multicolinealidad exacta entre las variables ambientales."
    )
    story.append(Paragraph(p6a_body2, body))
    story.append(Spacer(1, 3))

    # 6.b
    story.append(yellow_box("b. Desarrolle para qué tipo de escenarios se aplica LR", is_sub=True))
    p6b_text = (
        "La regresión lineal es la herramienta predilecta en la industria cuando la variable que se busca pronosticar es un valor numérico "
        "continuo (como potencia eléctrica, costos operativos, ingresos o temperatura) y, fundamentalmente, cuando se exige una "
        "<b>máxima transparencia e interpretabilidad física o jurídica</b>. En el sector energético permite programar el despacho de carga a la red nacional "
        "según el pronóstico meteorológico del día; en finanzas sustenta la valoración de carteras inmobiliarias y el análisis de riesgo; "
        "en mercadotecnia cuantifica el retorno directo de cada dólar invertido en publicidad; y en el ámbito biomédico relaciona la dosificación de un fármaco "
        "con la respuesta fisiológica del paciente.<br/><br/>"
        "Se debe optar por este modelo cuando se requiere rapidez de cómputo, claridad explicativa para la toma de decisiones y un punto de partida "
        "analítico sólido (<i>baseline</i>). Por el contrario, no es aplicable cuando la meta es clasificar elementos discretos en categorías "
        "(como detectar correos no deseados o diagnosticar positivo/negativo, donde corresponde usar regresión logística o árboles de decisión), "
        "ni ante fenómenos gobernados por patrones altamente no lineales o dinámicas caóticas complejas."
    )
    story.append(Paragraph(p6b_text, body))

    # ================= PAGE 3 =================
    story.append(PageBreak())

    # 6.c
    story.append(yellow_box("c. Describa de qué trata su DATASET seleccionado.", is_sub=True))
    p6c_text = (
        "Para comprender el funcionamiento físico de los datos, imaginemos una planta termoeléctrica de <b>Ciclo Combinado</b> como un sistema "
        "de doble aprovechamiento energético sumamente eficiente: en primer lugar, se quema gas natural para accionar una <b>turbina de gas</b> "
        "(Ciclo Brayton); posteriormente, en lugar de desaprovechar los gases calientes de escape que abandonan la chimenea a más de 500 °C, "
        "estos se dirigen a una caldera de recuperación para generar vapor a alta presión que impulsa una segunda <b>turbina de vapor</b> (Ciclo Rankine). "
        "Esta tecnología permite alcanzar un rendimiento superior al 55%, pero su producción final de energía se ve fuertemente condicionada por la meteorología exterior.<br/><br/>"
        "El archivo <code>Folds5x2_pp.csv</code> contiene 9,568 lecturas continuas registradas por los sensores de planta durante seis años completos:"
    )
    story.append(Paragraph(p6c_text, body))

    # Table of Dataset Variables
    table_data = [
        [
            Paragraph("Variable", table_header),
            Paragraph("Magnitud Física", table_header),
            Paragraph("Unidad", table_header),
            Paragraph("Rango", table_header),
            Paragraph("Correlación", table_header),
            Paragraph("Comportamiento e Impacto Físico en la Generación", table_header)
        ],
        [
            Paragraph("<b>AT</b>", table_cell_center),
            Paragraph("Ambient Temperature (Temperatura)", table_cell),
            Paragraph("°C", table_cell_center),
            Paragraph("1.81 a 37.11", table_cell_center),
            Paragraph("<b>-0.9481</b>", table_cell_center),
            Paragraph("<b>Factor más crítico.</b> El aire caliente pierde densidad; entra menor masa de oxígeno al compresor y cae la potencia.", table_cell)
        ],
        [
            Paragraph("<b>V</b>", table_cell_center),
            Paragraph("Exhaust Vacuum (Vacío de Escape)", table_cell),
            Paragraph("cm Hg", table_cell_center),
            Paragraph("25.36 a 81.56", table_cell_center),
            Paragraph("<b>-0.8698</b>", table_cell_center),
            Paragraph("Mide la contrapresión en el condensador de vapor. A mayor contrapresión, menor salto entálpico y menos potencia útil.", table_cell)
        ],
        [
            Paragraph("<b>AP</b>", table_cell_center),
            Paragraph("Ambient Pressure (Presión Barométrica)", table_cell),
            Paragraph("mbar", table_cell_center),
            Paragraph("992.89 a 1033.3", table_cell_center),
            Paragraph("<b>+0.5184</b>", table_cell_center),
            Paragraph("Una presión atmosférica alta comprime el aire de admisión de forma natural, inyectando más masa y ganando potencia.", table_cell)
        ],
        [
            Paragraph("<b>RH</b>", table_cell_center),
            Paragraph("Relative Humidity (Humedad Relativa)", table_cell),
            Paragraph("%", table_cell_center),
            Paragraph("25.56 a 100.16", table_cell_center),
            Paragraph("<b>+0.3898</b>", table_cell_center),
            Paragraph("El contenido de vapor modifica la capacidad calorífica del aire húmedo durante la combustión en los inyectores.", table_cell)
        ],
        [
            Paragraph("<b>PE</b>", table_cell_center),
            Paragraph("<b>Electrical Output (Potencia Neta)</b>", table_cell_bold),
            Paragraph("<b>MW</b>", table_cell_center),
            Paragraph("420.26 a 495.76", table_cell_center),
            Paragraph("<b>1.0000</b>", table_cell_center),
            Paragraph("<b>Variable Objetivo (Label).</b> Megavatios netos producidos por hora por el conjunto de la central termoeléctrica.", table_cell_bold)
        ]
    ]

    t_dataset = Table(table_data, colWidths=[42, 115, 42, 65, 75, 184])
    t_dataset.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F9F9F9")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#EBF3FB")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 4))

    # 6.d
    story.append(yellow_box("d. Describa los pasos del ciclo y su relación con su código:", is_sub=True))
    if os.path.exists("diagrama_ciclo_ml.png"):
        story.append(Image("diagrama_ciclo_ml.png", width=520, height=82))
        story.append(Spacer(1, 2))

    p6d_table_data = [
        [
            Paragraph("Etapa del Ciclo", table_header),
            Paragraph("Objetivo Metodológico y Conceptual", table_header),
            Paragraph("Implementación en PySpark (rsaavedra_lr2.ipynb)", table_header)
        ],
        [
            Paragraph("<b>1. Recolección de Datos</b>", table_cell_bold),
            Paragraph("Ingestión masiva del archivo CSV deduciendo automáticamente esquemas numéricos continuos.", table_cell),
            Paragraph("<code>df = spark.read.csv('Folds5x2_pp.csv', header=True, inferSchema=True)</code>", table_cell)
        ],
        [
            Paragraph("<b>2. Preparación y Limpieza</b>", table_cell_bold),
            Paragraph("Auditoría de integridad estructural. Se comprobó la existencia de 0 nulos en las 9,568 observaciones.", table_cell),
            Paragraph("<code>df.select([count(when(isnan(c) | col(c).isNull(), c)) for c in df.columns]).show()</code>", table_cell)
        ],
        [
            Paragraph("<b>3. Feature Engineering</b>", table_cell_bold),
            Paragraph("Empaquetamiento obligatorio de las 4 variables predictoras continuas en una única columna vectorial densa.", table_cell),
            Paragraph("<code>assembler = VectorAssembler(inputCols=['AT','V','AP','RH'], outputCol='features')</code><br/><code>final_df = assembler.transform(df).select('features', 'PE')</code>", table_cell)
        ],
        [
            Paragraph("<b>4. Entrenamiento y Validación</b>", table_cell_bold),
            Paragraph("Partición determinística 80% train y 20% test, ajuste de coeficientes lineales y evaluación diagnóstica.", table_cell),
            Paragraph("<code>train_data, test_data = final_df.randomSplit([0.8, 0.2], seed=42)</code><br/><code>lr = LinearRegression(featuresCol='features', labelCol='PE')</code><br/><code>lr_model = lr.fit(train_data)</code>", table_cell)
        ]
    ]

    t_ciclo = Table(p6d_table_data, colWidths=[105, 165, 253])
    t_ciclo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2A5298")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_ciclo)

    # ================= PAGE 4 =================
    story.append(PageBreak())

    # 6.e
    story.append(yellow_box("e. Haga la demostración de ejecución en Google Colab.", is_sub=True))
    p6e_text = (
        "Durante la exposición oral ante el docente, la demostración práctica en vivo se estructura en cinco momentos clave:<br/>"
        "1. <b>Inicialización del Clúster:</b> Ejecutar las celdas 1 y 2 para constatar que la sesión de Spark <code>rsaavedra_lr2</code> se inicia correctamente sobre la máquina virtual.<br/>"
        "2. <b>Carga con Triple Respaldo:</b> Mostrar cómo el script comprueba la existencia local del dataset <code>Folds5x2_pp.csv</code> o lo obtiene de forma autónoma desde el repositorio UCI sin interrupciones.<br/>"
        "3. <b>Comprobación de Calidad:</b> Proyectar la verificación de integridad que demuestra 0 valores nulos en el 100% de los 9,568 registros.<br/>"
        "4. <b>Demostración de RDD (Requisito Estricto de la Guía):</b> Demostrar la manipulación distribuida a bajo nivel ejecutando "
        "<code>predictions_and_actuals_rdd.take(2)</code> para exhibir los objetos estructurados <code>Row(prediction=468.21, PE=464.0)</code>, "
        "seguido de <code>.map(tuple).take(2)</code> para ilustrar la transformación a tuplas nativas <code>(468.21, 464.0)</code> idénticas al pantallazo docente.<br/>"
        "5. <b>Validación Gráfica:</b> Desplegar el panel de 4 visualizaciones que evalúa la dispersión ideal de 45°, la normalidad en campana de Gauss de los residuos, la homocedasticidad y la magnitud de los parámetros."
    )
    story.append(Paragraph(p6e_text, body))
    story.append(Spacer(1, 3))

    # 6.f
    story.append(yellow_box("f. Explique los resultados obtenidos.", is_sub=True))
    p6f_intro = (
        "Tras procesar y ajustar el modelo sobre las 7,654 observaciones del conjunto de entrenamiento en PySpark, "
        "la ecuación lineal resultante queda expresada de la siguiente manera:"
    )
    story.append(Paragraph(p6f_intro, body))
    story.append(Spacer(1, 2))

    # Formula 3 - Fitted Equation
    f3 = "<b>PE<sub>predicho</sub></b> = 458.9396 - 1.9840&middot;<b>AT</b> - 0.2307&middot;<b>V</b> + 0.0579&middot;<b>AP</b> - 0.1599&middot;<b>RH</b>"
    story.append(equation_box(f3, font_size=9.5))
    story.append(Spacer(1, 2))

    p6f_body = (
        "Esta fórmula resume con total claridad la dinámica operativa de la planta. Por ejemplo, si la temperatura ambiental exterior aumenta "
        "tan solo 1 °C en una tarde calurosa de verano, la pérdida de densidad en el aire ingresado provocará que la central pierda en promedio "
        "casi 2 Megawatts de potencia neta (aproximadamente la energía que abastece a unas 2,000 familias). "
        "El desglose analítico de cada parámetro estimado se detalla a continuación:"
    )
    story.append(Paragraph(p6f_body, body))
    story.append(Spacer(1, 2))

    p6f_coef_table = [
        [
            Paragraph("Parámetro", table_header),
            Paragraph("Coeficiente (&beta;)", table_header),
            Paragraph("Unidad Física", table_header),
            Paragraph("Interpretación Física y Significado Termodinámico", table_header)
        ],
        [
            Paragraph("<b>Intercepto (&beta;<sub>0</sub>)</b>", table_cell_bold),
            Paragraph("<b>+458.9396</b>", table_cell_center),
            Paragraph("MW", table_cell_center),
            Paragraph("Nivel de potencia teórica base si todos los sensores registraran un valor numérico cero.", table_cell)
        ],
        [
            Paragraph("<b>Temperatura (AT)</b>", table_cell_bold),
            Paragraph("<b>-1.9840</b>", table_cell_center),
            Paragraph("MW / °C", table_cell_center),
            Paragraph("<b>Factor dominante negativo.</b> Por cada 1 °C que sube el calor exterior, la planta <b>pierde ~1.98 MW</b> de potencia neta.", table_cell)
        ],
        [
            Paragraph("<b>Vacío de Escape (V)</b>", table_cell_bold),
            Paragraph("<b>-0.2307</b>", table_cell_center),
            Paragraph("MW / cm Hg", table_cell_center),
            Paragraph("Por cada 1 cm Hg de incremento en la contrapresión del condensador, la producción neta <b>se reduce en 0.23 MW</b>.", table_cell)
        ],
        [
            Paragraph("<b>Presión Atm. (AP)</b>", table_cell_bold),
            Paragraph("<b>+0.0579</b>", table_cell_center),
            Paragraph("MW / mbar", table_cell_center),
            Paragraph("Una mayor presión barométrica comprime el aire de admisión en el compresor, <b>ganando 0.058 MW</b> por cada milibar adicional.", table_cell)
        ],
        [
            Paragraph("<b>Humedad Rel. (RH)</b>", table_cell_bold),
            Paragraph("<b>-0.1599</b>", table_cell_center),
            Paragraph("MW / %", table_cell_center),
            Paragraph("Al controlar conjuntamente temperatura y presión, un incremento del 1% en la humedad reduce marginalmente la potencia en 0.16 MW.", table_cell)
        ]
    ]

    t_coef = Table(p6f_coef_table, colWidths=[105, 80, 75, 263])
    t_coef.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_coef)

    # ================= PAGE 5 =================
    story.append(PageBreak())

    # 6.g
    p6g_prompt = (
        "g. Investigue sobre las métricas de error, cómo se las debe interpretar y cuándo elegir cuál; "
        "menciona cómo se interpreta cada una, por ejemplo, cada métrica a qué elementos toma más en cuenta."
    )
    story.append(yellow_box(p6g_prompt, is_sub=True))
    p6g_intro = (
        "Al evaluar un modelo predictivo, ningún indicador aislado es suficiente para dictaminar su éxito. "
        "Cada métrica estadística examina los errores residuales bajo una lupa matemática distinta, balanceando la sensibilidad ante "
        "valores atípicos, la escala de medida física y la facilidad de comprensión para diferentes audiencias:"
    )
    story.append(Paragraph(p6g_intro, body))
    story.append(Spacer(1, 2))

    metrics_table_data = [
        [
            Paragraph("Métrica", table_header),
            Paragraph("Fórmula Matemática", table_header),
            Paragraph("Valor Obtenido", table_header),
            Paragraph("¿A qué elementos toma más en cuenta?", table_header),
            Paragraph("Criterio de Elección: ¿Cuándo seleccionarla?", table_header)
        ],
        [
            Paragraph("<b>R² (Determinación)</b>", table_cell_bold),
            Paragraph("1 - [ SS<sub>res</sub> / SS<sub>tot</sub> ]", table_cell_center),
            Paragraph("<b>0.9284<br/>(92.84%)</b>", table_cell_center),
            Paragraph("Mide la proporción de la varianza total explicada por el modelo. Es adimensional (de 0 a 1).", table_cell),
            Paragraph("<b>Para medir ajuste global.</b> Comunica qué porcentaje del comportamiento real del fenómeno capturó la recta.", table_cell)
        ],
        [
            Paragraph("<b>RMSE (Raíz Cuadrática)</b>", table_cell_bold),
            Paragraph("&radic;[ (1/N) &Sigma;(y - y<sub>pred</sub>)<sup>2</sup> ]", table_cell_center),
            Paragraph("<b>4.5110 MW</b>", table_cell_center),
            Paragraph("<b>Penaliza fuertemente desvíos grandes y outliers</b> al elevar los errores al cuadrado antes de promediar.", table_cell),
            Paragraph("<b>Cuando los fallos grandes son críticos.</b> Ej: una subestimación de 20 MW desestabilizaría la red eléctrica.", table_cell)
        ],
        [
            Paragraph("<b>MAE (Absoluto Medio)</b>", table_cell_bold),
            Paragraph("(1/N) &Sigma; |y - y<sub>pred</sub>|", table_cell_center),
            Paragraph("<b>3.6124 MW</b>", table_cell_center),
            Paragraph("<b>Pondera todos los errores de forma lineal y uniforme.</b> Resulta muy robusto ante ruidos aislados.", table_cell),
            Paragraph("<b>Para reportar el error típico mediano</b> sin que unas pocas mediciones anómalas distorsionen el reporte global.", table_cell)
        ],
        [
            Paragraph("<b>MSE (Cuadrático Medio)</b>", table_cell_bold),
            Paragraph("(1/N) &Sigma; (y - y<sub>pred</sub>)<sup>2</sup>", table_cell_center),
            Paragraph("<b>20.3488 MW²</b>", table_cell_center),
            Paragraph("Varianza de los residuos. Al encontrarse en unidades al cuadrado (MW²), carece de intuición directa.", table_cell),
            Paragraph("<b>Como función matemática de optimización</b> para algoritmos de gradiente, pero no para presentación pública.", table_cell)
        ],
        [
            Paragraph("<b>MAPE (Porcentual Medio)</b>", table_cell_bold),
            Paragraph("(100/N) &Sigma; |(y-y<sub>pred</sub>)/y|", table_cell_center),
            Paragraph("<b>0.795 %</b>", table_cell_center),
            Paragraph("Evalúa la magnitud del desvío en proporción porcentual relativa al valor real generado.", table_cell),
            Paragraph("<b>Para comunicación ejecutiva y directiva.</b> Permite certificar que el margen de desvío es inferior al 1%.", table_cell)
        ]
    ]

    t_metrics = Table(metrics_table_data, colWidths=[85, 90, 68, 140, 140])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1B365D")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 4))

    conclusion_box = [
        [
            Paragraph(
                "<b>SÍNTESIS FINAL PARA LA DEFENSA ORAL ANTE EL DOCENTE:</b><br/>"
                "• El modelo de Regresión Lineal Múltiple entrenado en <b>Apache Spark MLlib</b> explica el <b>92.84%</b> de la energía generada (<i>R</i><sup>2</sup> = 0.9284) con un error típico de tan sólo <b>4.51 MW</b> (margen relativo inferior al 0.8%).<br/>"
                "• La variable física con mayor incidencia destructiva es la <b>Temperatura Ambiente (AT)</b> con <b>-1.98 MW/°C</b>, seguida del Vacío de Escape (V) con <b>-0.23 MW/cm Hg</b>.<br/>"
                "• El cuaderno de trabajo <b><code>rsaavedra_lr2.ipynb</code></b> satisface la totalidad de las consignas institucionales: verificación de identidad en Google Colab, reserva exclusiva en WhatsApp, pipeline de Spark MLlib, conversión RDD con <code>.map(tuple)</code> y visualizaciones analíticas completas.",
                body
            )
        ]
    ]
    t_conclusion = Table(conclusion_box, colWidths=[523])
    t_conclusion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF3FB")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#2A5298")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_conclusion)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully with TrueType Arial and beautiful math equations.")

if __name__ == '__main__':
    build_pdf()
