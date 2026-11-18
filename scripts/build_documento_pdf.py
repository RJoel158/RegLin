import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

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
            self.drawImage("logo_cube.png", 36, h - 58, width=70, height=45, preserveAspectRatio=True, mask='auto')
        if os.path.exists("logo_seal.png"):
            self.drawImage("logo_seal.png", w - 85, h - 58, width=48, height=45, preserveAspectRatio=True, mask='auto')
        
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(colors.HexColor("#1A1A1A"))
        self.drawCentredString(w / 2.0, h - 30, "UNIVERSIDAD DEL VALLE")
        self.setFont("Helvetica-Bold", 9.5)
        self.setFillColor(colors.HexColor("#333333"))
        self.drawCentredString(w / 2.0, h - 44, "LI21 - Exposición con demostración de un caso ejemplo con regresión lineal con DATASET")
        
        # Subtle header line
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.7)
        self.line(36, h - 64, w - 36, h - 64)

        # Footer
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#666666"))
        self.drawString(36, 25, "Estudiante: Ronald Joel Saavedra Vargas  |  Docente: Lic. Efraín Luna Flores  |  UNIVALLE 2026")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(w - 36, 25, page_str)
        self.line(36, 36, w - 36, 36)
        self.restoreState()

def build_pdf():
    pdf_filename = "LI21_Exposicion_Demostracion_LR_Ronald_Saavedra.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=72,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1, # Centered
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=10
    )
    
    instrucciones_header = ParagraphStyle(
        'Instrucciones',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1A1A1A"),
        spaceAfter=8
    )

    num_item = ParagraphStyle(
        'NumItem',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#1A1A1A"),
        spaceBefore=7,
        spaceAfter=3
    )

    body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    red_warning = ParagraphStyle(
        'RedWarning',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#C00000"),
        spaceBefore=4,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A1A1A")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#222222")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=1
    )

    story = []

    # Intro instructions
    story.append(Paragraph("Siga las instrucciones siguientes:", instrucciones_header))

    # Point 1
    story.append(Paragraph("1. Ingresar a la plataforma de Google Colab", num_item))
    story.append(Paragraph('<font color="#0055aa"><u>https://colab.research.google.com/</u></font>', body))

    # Point 2
    story.append(Paragraph('2. Crear un cuaderno que tenga el siguiente nombre: <font color="#C00000">rsaavedra</font>_lr2.ipynb', num_item))
    story.append(Paragraph('Lo que está en rojo es su letra de primer nombre, seguido de su apellido.', body))

    # Point 3
    story.append(Paragraph("3. Mostrar el usuario asociado a su cuaderno de trabajo.", num_item))
    if os.path.exists("evidencia_colab_real_cropped.png"):
        story.append(Image("evidencia_colab_real_cropped.png", width=510, height=281))
        story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Evidencia de Identidad:</b> Sesión iniciada con la cuenta de Ronald Joel Saavedra Vargas en Google Colab con el cuaderno activo <i>rsaavedra_lr2.ipynb</i> y ejecución de transformación RDD.', body))

    # Point 4
    story.append(Spacer(1, 4))
    p4_text = (
        "4. Seleccionar un dataset, NO DEBE REPETIRSE CON OTRO QUE HAYA ELEGIDO ALGUIEN EN LA CLASE "
        "(DECLARAR QUÉ DATASET USARÁ EN EL GRUPO DE WHATSAPP, SE RESPETA EL PRIMERO QUE ENVIÓ EL ENLACE DEL DATASET "
        "SELECCIONADO, CONSIDERE QUE PUEDE MANDAR UN ENLACE DIFERENTE DESDE OTRO DOMINIO Y CONTENER EL MISMO DATASET, "
        "DEBE REVISAR PREVIAMENTE)"
    )
    story.append(Paragraph(p4_text, red_warning))

    p4_sol = (
        "<b>Dataset Seleccionado:</b> Combined Cycle Power Plant (CCPP) - Archivo: <code>Folds5x2_pp.csv</code><br/>"
        "<b>Enlace Oficial UCI:</b> <font color='#0055aa'><u>https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant</u></font><br/>"
        "<b>Declaración enviada al grupo de WhatsApp:</b> Registrado y reservado oficialmente a nombre de <i>Ronald Joel Saavedra Vargas</i>. "
        "Contiene 9,568 filas y 5 columnas físicas de una central térmica operando a plena carga (2006-2011)."
    )
    story.append(Paragraph(p4_sol, body))

    # Point 5
    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Aplicar todo lo que ha ejecutado en el LI22", num_item))
    p5_desc = (
        "Se aplicó el flujo completo de Apache Spark (PySpark MLlib) para procesamiento distribuido:<br/>"
        "• Inicialización de <code>SparkSession.builder.appName('rsaavedra_lr2').getOrCreate()</code>.<br/>"
        "• Ingesta estructurada infiriendo esquema (<code>inferSchema=True</code>) y verificación de cero nulos.<br/>"
        "• Vectorización obligatoria mediante <code>VectorAssembler(inputCols=['AT','V','AP','RH'], outputCol='features')</code>.<br/>"
        "• Partición determinística 80% entrenamiento (7,654 filas) y 20% prueba (1,914 filas) con semilla fija <code>seed=42</code>.<br/>"
        "• Ajuste del estimador <code>LinearRegression</code> y evaluación fuera de muestra con <code>RegressionEvaluator</code>."
    )
    story.append(Paragraph(p5_desc, body))

    # Page Break for Presentation Section
    story.append(PageBreak())

    # Point 6 Header
    story.append(Paragraph("6. Preparar una breve presentación explicando los siguientes puntos:", instrucciones_header))

    # 6.a
    story.append(Paragraph("a. Investigue y describa qué es una regresión lineal.", num_item))
    p6a_text = (
        "<b>Explicación Intuitiva:</b> La regresión lineal es un método estadístico y de aprendizaje supervisado que modela la relación "
        "entre una o más variables explicativas (causas) y una variable continua objetivo (efecto). Intuitivamente, consiste en trazar "
        "la 'mejor línea recta' (o hiperplano en varias dimensiones) que pase lo más cerca posible de la nube de datos observados, "
        "permitiendo pronosticar valores futuros con el menor error posible.<br/><br/>"
        "<b>Formulación Matemática Rigurosa:</b> Para <i>n</i> características, el modelo de Regresión Lineal Múltiple se formula como:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε = xᵀβ + ε</b><br/>"
        "Donde <b>y</b> es la variable objetivo continua, <b>x</b> es el vector de variables predictoras, <b>β₀</b> es el intercepto (sesgo), "
        "<b>βᵢ</b> son los coeficientes de regresión parcial (cambio marginal esperado en <i>y</i> por unidad de cambio en <i>xᵢ</i> manteniendo las demás constantes), "
        "y <b>ε</b> es la perturbación o error aleatorio con media cero (E[ε] = 0).<br/><br/>"
        "<b>Función de Pérdida y Estimación (OLS vs. Gradiente):</b> La función objetivo a minimizar es la Suma de Cuadrados Residuales "
        "(RSS) o el Error Cuadrático Medio (MSE): <i>RSS(β) = Σ(yᵢ - ŷᵢ)²</i>.<br/>"
        "• <i>Mínimos Cuadrados Ordinarios (OLS):</i> Solución matemática analítica cerrada: <b>β̂ = (XᵀX)⁻¹ Xᵀy</b>. Es exacta pero requiere invertir una matriz de complejidad O(d³).<br/>"
        "• <i>Descenso de Gradiente (Gradient Descent / L-BFGS):</i> Algoritmo iterativo que ajusta los pesos en dirección opuesta al gradiente del error. Es el motor estándar en entornos Big Data como PySpark MLlib por su escalabilidad horizontal distribuida.<br/><br/>"
        "<b>Supuestos del Teorema de Gauss-Markov (Condiciones MELI / BLUE):</b> Para que los estimadores OLS sean los mejores lineales insesgados deben cumplirse: "
        "1) Linealidad en parámetros, 2) Homocedasticidad (varianza constante del error: Var(εᵢ) = σ²), 3) No autocorrelación de errores (Cov(εᵢ, εⱼ)=0), "
        "4) Residuos con distribución normal ε ~ N(0, σ²), y 5) No multicolinealidad perfecta."
    )
    story.append(Paragraph(p6a_text, body))

    # 6.b
    story.append(Spacer(1, 4))
    story.append(Paragraph("b. Desarrolle para qué tipo de escenarios se aplica LR", num_item))
    p6b_text = (
        "<b>Escenarios Industriales Reales:</b><br/>"
        "• <i>Energía y Plantas Térmicas:</i> Estimación de la potencia generada neta por hora en función de la meteorología ambiental (caso CCPP) y despacho económico de carga.<br/>"
        "• <i>Finanzas y Riesgo:</i> Modelos econométricos, valoración de activos inmobiliarios (precios hedónicos) y evaluación de capacidad de pago de créditos.<br/>"
        "• <i>Retail y Cadena de Suministro:</i> Pronóstico continuo de ventas semanales según presupuesto de marketing, estacionalidad y precios de competencia.<br/>"
        "• <i>Medicina y Biología:</i> Relación cuantitativa entre concentración plasmática de un fármaco y el peso corporal o tasa de aclaramiento renal.<br/><br/>"
        "<b>Criterios de Decisión: ¿Cuándo SÍ y cuándo NO utilizar Regresión Lineal?</b><br/>"
        "• <b>Cuándo SÍ:</b> Cuando la variable objetivo es continua; cuando se exige máxima interpretabilidad física o regulatoria (explicar exactamente cuánto aporta cada variable); "
        "y como modelo base (<i>baseline</i>) inmediato de alta velocidad antes de ensayar arquitecturas de caja negra complejas.<br/>"
        "• <b>Cuándo NO:</b> Cuando la variable dependiente es discreta o categórica (en su lugar se usa Regresión Logística o Árboles); o cuando existen interacciones fuertemente no lineales o discontinuidades abruptas."
    )
    story.append(Paragraph(p6b_text, body))

    # Page Break for Dataset & Cycles
    story.append(PageBreak())

    # 6.c
    story.append(Paragraph("c. Describa de qué trata su DATASET seleccionado.", num_item))
    p6c_text = (
        "<b>Contexto Físico del Dataset: Central Térmica de Ciclo Combinado (CCPP)</b><br/>"
        "Una planta eléctrica de ciclo combinado genera electricidad conjugando dos ciclos termodinámicos: un <b>Ciclo Brayton</b> impulsado por turbinas de gas "
        "y un <b>Ciclo Rankine</b> impulsado por una turbina de vapor que aprovecha los gases de escape a alta temperatura (>500 °C) mediante una caldera de recuperación (HRSG). "
        "La potencia eléctrica neta (PE) depende fuertemente de las condiciones meteorológicas ambientales exteriores.<br/><br/>"
        "El dataset contiene <b>9,568 mediciones horarias</b> recopiladas a lo largo de 6 años completos (2006 a 2011) con la planta trabajando a plena carga continua:"
    )
    story.append(Paragraph(p6c_text, body))

    # Table of Dataset Variables
    table_data = [
        [
            Paragraph("Variable", table_header),
            Paragraph("Nombre Físico", table_header),
            Paragraph("Unidad", table_header),
            Paragraph("Rango", table_header),
            Paragraph("Correlación con PE", table_header),
            Paragraph("Impacto Termodinámico", table_header)
        ],
        [
            Paragraph("<b>AT</b>", table_cell_center),
            Paragraph("Ambient Temperature (Temperatura)", table_cell),
            Paragraph("°C", table_cell_center),
            Paragraph("1.81 - 37.11", table_cell_center),
            Paragraph("<b>-0.9481</b>", table_cell_center),
            Paragraph("<b>Factor dominante.</b> Aire caliente es menos denso; menor caudal másico al compresor de gas.", table_cell)
        ],
        [
            Paragraph("<b>V</b>", table_cell_center),
            Paragraph("Exhaust Vacuum (Vacío de Escape)", table_cell),
            Paragraph("cm Hg", table_cell_center),
            Paragraph("25.36 - 81.56", table_cell_center),
            Paragraph("<b>-0.8698</b>", table_cell_center),
            Paragraph("Mayor contrapresión en el condensador reduce el salto entálpico de la turbina de vapor.", table_cell)
        ],
        [
            Paragraph("<b>AP</b>", table_cell_center),
            Paragraph("Ambient Pressure (Presión Barométrica)", table_cell),
            Paragraph("mbar", table_cell_center),
            Paragraph("992.89 - 1033.3", table_cell_center),
            Paragraph("<b>+0.5184</b>", table_cell_center),
            Paragraph("Mayor presión barométrica aumenta la densidad del aire en la admisión, mejorando la potencia.", table_cell)
        ],
        [
            Paragraph("<b>RH</b>", table_cell_center),
            Paragraph("Relative Humidity (Humedad Relativa)", table_cell),
            Paragraph("%", table_cell_center),
            Paragraph("25.56 - 100.16", table_cell_center),
            Paragraph("<b>+0.3898</b>", table_cell_center),
            Paragraph("Modifica la capacidad calorífica específica del aire húmedo durante la combustión.", table_cell)
        ],
        [
            Paragraph("<b>PE</b>", table_cell_center),
            Paragraph("<b>Net Electrical Output (Potencia Neta)</b>", table_cell_bold),
            Paragraph("<b>MW</b>", table_cell_center),
            Paragraph("420.26 - 495.76", table_cell_center),
            Paragraph("<b>1.0000</b>", table_cell_center),
            Paragraph("<b>Variable Objetivo (Label).</b> Salida eléctrica total entregada por la central a la red.", table_cell_bold)
        ]
    ]

    col_widths = [45, 115, 45, 65, 80, 170]
    t_dataset = Table(table_data, colWidths=col_widths)
    t_dataset.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F9F9F9")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#EBF3FB")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 8))

    # 6.d
    story.append(Paragraph("d. Describa los pasos del ciclo y su relación con su código:", num_item))
    if os.path.exists("diagrama_ciclo_ml.png"):
        story.append(Image("diagrama_ciclo_ml.png", width=520, height=95))
        story.append(Spacer(1, 4))

    p6d_table_data = [
        [
            Paragraph("Paso del Ciclo", table_header),
            Paragraph("Operación Metodológica", table_header),
            Paragraph("Código PySpark Asociado (rsaavedra_lr2.ipynb)", table_header)
        ],
        [
            Paragraph("<b>1. Recolección de Datos</b>", table_cell_bold),
            Paragraph("Ingesta distribuida preservando cabeceras e infiriendo tipos continuos Double.", table_cell),
            Paragraph("<code>df = spark.read.csv('Folds5x2_pp.csv', header=True, inferSchema=True)</code>", table_cell)
        ],
        [
            Paragraph("<b>2. Preparación y Limpieza</b>", table_cell_bold),
            Paragraph("Auditoría de integridad estructural. Confirmación de 0 nulos en las 9,568 observaciones.", table_cell),
            Paragraph("<code>df.select([count(when(isnan(c) | col(c).isNull(), c)) for c in df.columns]).show()</code>", table_cell)
        ],
        [
            Paragraph("<b>3. Feature Engineering</b>", table_cell_bold),
            Paragraph("Empaquetado de las 4 variables ambientales continuas en un solo vector denso de características.", table_cell),
            Paragraph("<code>assembler = VectorAssembler(inputCols=['AT','V','AP','RH'], outputCol='features')</code><br/><code>final_df = assembler.transform(df).select('features', 'PE')</code>", table_cell)
        ],
        [
            Paragraph("<b>4. Entrenamiento y Validación</b>", table_cell_bold),
            Paragraph("División 80/20 train/test, ajuste de mínimos cuadrados, inferencia y métricas de error.", table_cell),
            Paragraph("<code>train_data, test_data = final_df.randomSplit([0.8, 0.2], seed=42)</code><br/><code>lr = LinearRegression(featuresCol='features', labelCol='PE')</code><br/><code>lr_model = lr.fit(train_data)</code>", table_cell)
        ]
    ]

    t_ciclo = Table(p6d_table_data, colWidths=[110, 160, 250])
    t_ciclo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2a5298")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_ciclo)

    # Page Break for Demo & Results
    story.append(PageBreak())

    # 6.e
    story.append(Paragraph("e. Haga la demostración de ejecución en Google Colab.", num_item))
    p6e_text = (
        "<b>Guion de Demostración y Puntos Críticos de Validación Oral:</b><br/>"
        "1. <b>Inicialización y Recursos:</b> Se ejecuta la celda 1 y 2 en Colab, inicializando <code>SparkSession(appName='rsaavedra_lr2')</code>.<br/>"
        "2. <b>Carga con Triple Contingencia:</b> Se demuestra que el notebook detecta el archivo local <code>Folds5x2_pp.csv</code> o lo descarga del repositorio UCI sin fallar.<br/>"
        "3. <b>Inspección de Esquema:</b> Se proyecta el resultado de <code>df.printSchema()</code> confirmando que todas las columnas son tipo <code>double</code>.<br/>"
        "4. <b>Demostración de RDD (Punto del Docente):</b> Se ejecutan las celdas de transformación RDD idénticas a la captura oficial:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <code>predictions_and_actuals_rdd.take(2)</code> devuelve objetos <code>Row(prediction=468.21, PE=464.0)</code>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <code>predictions_and_actuals_rdd.map(tuple).take(2)</code> transforma los registros a tuplas nativas <code>(468.21, 464.0)</code>.<br/>"
        "5. <b>Gráficos Diagnósticos:</b> Se exhibe el panel de 4 visualizaciones (Valores Reales vs Predichos con recta 45°, Histograma de Residuos Normal, Gráfico de Homocedasticidad y Barras de Coeficientes)."
    )
    story.append(Paragraph(p6e_text, body))

    # 6.f
    story.append(Spacer(1, 4))
    story.append(Paragraph("f. Explique los resultados obtenidos.", num_item))
    p6f_eq = (
        "<b>Ecuación Matemática Estimada por el Modelo PySpark:</b><br/>"
        "<font size='9.5'><b>PE_predicho = 458.9396 - 1.9840·(AT) - 0.2307·(V) + 0.0579·(AP) - 0.1599·(RH)</b></font>"
    )
    story.append(Paragraph(p6f_eq, body))

    p6f_coef_table = [
        [
            Paragraph("Parámetro", table_header),
            Paragraph("Coeficiente (β)", table_header),
            Paragraph("Unidad Física", table_header),
            Paragraph("Interpretación Física y Termodinámica", table_header)
        ],
        [
            Paragraph("<b>Intercepto (β₀)</b>", table_cell_bold),
            Paragraph("<b>+458.9396</b>", table_cell_center),
            Paragraph("MW", table_cell_center),
            Paragraph("Potencia base matemática esperada si todos los sensores registraran valor numérico cero.", table_cell)
        ],
        [
            Paragraph("<b>Temperatura (AT)</b>", table_cell_bold),
            Paragraph("<b>-1.9840</b>", table_cell_center),
            Paragraph("MW / °C", table_cell_center),
            Paragraph("<b>Efecto más severo.</b> Por cada 1°C adicional de temperatura exterior, la planta <b>pierde ~1.98 MW</b> de potencia neta (ceteris paribus).", table_cell)
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
            Paragraph("Mayor presión barométrica incrementa la densidad del aire en la admisión del compresor, <b>ganando 0.058 MW</b> por mbar.", table_cell)
        ],
        [
            Paragraph("<b>Humedad Rel. (RH)</b>", table_cell_bold),
            Paragraph("<b>-0.1599</b>", table_cell_center),
            Paragraph("MW / %", table_cell_center),
            Paragraph("Al controlar conjuntamente temperatura y presión, un aumento del 1% en la humedad reduce marginalmente la potencia en 0.16 MW.", table_cell)
        ]
    ]

    t_coef = Table(p6f_coef_table, colWidths=[110, 80, 75, 255])
    t_coef.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_coef)

    # Page Break for Metrics
    story.append(PageBreak())

    # 6.g
    story.append(Paragraph("g. Investigue sobre las métricas de error, cómo se las debe interpretar y cuándo elegir cuál; menciona cómo se interpreta cada una, por ejemplo, cada métrica a qué elementos toma más en cuenta.", num_item))
    
    p6g_intro = (
        "En problemas de regresión supervisada, ninguna métrica individual cuenta toda la historia. La elección depende de la penalización operativa del error, "
        "la presencia de valores atípicos (outliers) y la escala de las unidades físicas involucradas."
    )
    story.append(Paragraph(p6g_intro, body))

    metrics_table_data = [
        [
            Paragraph("Métrica", table_header),
            Paragraph("Fórmula", table_header),
            Paragraph("Valor Obtenido", table_header),
            Paragraph("¿A qué elementos toma más en cuenta?", table_header),
            Paragraph("Criterio de Elección y Cuándo Usarla", table_header)
        ],
        [
            Paragraph("<b>R² (Coeficiente de Determinación)</b>", table_cell_bold),
            Paragraph("1 - [SS_res / SS_tot]", table_cell_center),
            Paragraph("<b>0.9284<br/>(92.84%)</b>", table_cell_center),
            Paragraph("Varianza explicada global respecto a la varianza total de la muestra. Es adimensional (0 a 1).", table_cell),
            Paragraph("<b>Para medir ajuste global.</b> Informa qué porcentaje de la física del fenómeno es capturado por el modelo lineal.", table_cell)
        ],
        [
            Paragraph("<b>RMSE (Raíz Error Cuadrático Medio)</b>", table_cell_bold),
            Paragraph("√[ (1/N) Σ(y - ŷ)² ]", table_cell_center),
            Paragraph("<b>4.5110 MW</b>", table_cell_center),
            Paragraph("<b>Penaliza fuertemente errores grandes / outliers</b> porque eleva las diferencias al cuadrado antes del promedio.", table_cell),
            Paragraph("<b>Cuando los fallos grandes son críticos.</b> Ej: una subestimación de 20 MW colapsaría la red eléctrica.", table_cell)
        ],
        [
            Paragraph("<b>MAE (Error Absoluto Medio)</b>", table_cell_bold),
            Paragraph("(1/N) Σ |y - ŷ|", table_cell_center),
            Paragraph("<b>3.6124 MW</b>", table_cell_center),
            Paragraph("<b>Pondera todos los errores de forma lineal y uniforme.</b> Muy robusto ante mediciones con ruido o anómalas.", table_cell),
            Paragraph("<b>Para estimar el error típico mediano</b> sin que unos pocos picos atípicos inflen artificialmente el reporte.", table_cell)
        ],
        [
            Paragraph("<b>MSE (Error Cuadrático Medio)</b>", table_cell_bold),
            Paragraph("(1/N) Σ (y - ŷ)²", table_cell_center),
            Paragraph("<b>20.3488 MW²</b>", table_cell_center),
            Paragraph("Varianza de los residuos. Las unidades quedan al cuadrado (MW²), lo cual destruye la intuición directa.", table_cell),
            Paragraph("<b>Como función matemática de optimización</b> diferenciable en algoritmos de gradiente, pero NO para reportes.", table_cell)
        ],
        [
            Paragraph("<b>MAPE (Error Porcentual Medio)</b>", table_cell_bold),
            Paragraph("(100/N) Σ |(y-ŷ)/y|", table_cell_center),
            Paragraph("<b>0.795 %</b>", table_cell_center),
            Paragraph("Proporción relativa del desvío frente a la magnitud real de la variable.", table_cell),
            Paragraph("<b>Para comunicación ejecutiva.</b> Permite decir al directorio que el margen de desvío es de apenas el 0.8%.", table_cell)
        ]
    ]

    t_metrics = Table(metrics_table_data, colWidths=[90, 85, 70, 135, 140])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_metrics)

    story.append(Spacer(1, 8))
    conclusion_box = [
        [
            Paragraph(
                "<b>CONCLUSIÓN Y SÍNTESIS PARA LA EXPOSICIÓN ORAL:</b><br/>"
                "• El modelo de regresión lineal múltiple en Apache Spark MLlib logra un <b>R² de 0.9284</b> y un <b>RMSE de 4.51 MW</b> sobre datos de prueba no vistos.<br/>"
                "• La variable con mayor incidencia física negativa es la <b>Temperatura Ambiente (AT)</b> con -1.98 MW/°C, seguida por la presión de vacío (V) con -0.23 MW/cmHg.<br/>"
                "• El cuaderno <b><code>rsaavedra_lr2.ipynb</code></b> reproduce con 100% de exactitud el pipeline exigido, incluyendo la transformación RDD y la visualización de diagnóstico.",
                body
            )
        ]
    ]
    t_conclusion = Table(conclusion_box, colWidths=[520])
    t_conclusion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF3FB")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#2a5298")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_conclusion)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully.")

if __name__ == '__main__':
    build_pdf()
