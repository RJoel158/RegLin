import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
            # Crisp user logo
            self.drawImage("logo_cube.png", 36, h - 56, width=54, height=42, preserveAspectRatio=True, mask='auto')
        if os.path.exists("logo_seal.png"):
            self.drawImage("logo_seal.png", w - 80, h - 56, width=44, height=42, preserveAspectRatio=True, mask='auto')
        
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(colors.HexColor("#1A1A1A"))
        self.drawCentredString(w / 2.0, h - 28, "UNIVERSIDAD DEL VALLE")
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#333333"))
        self.drawCentredString(w / 2.0, h - 42, "LI21 - Exposición con demostración de un caso ejemplo con regresión lineal con DATASET")
        
        # Subtle header line
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.6)
        self.line(36, h - 60, w - 36, h - 60)

        # Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        self.drawString(36, 22, "Estudiante: Ronald Joel Saavedra Vargas  |  Docente: Lic. Efraín Luna Flores  |  UNIVALLE 2026")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(w - 36, 22, page_str)
        self.line(36, 32, w - 36, 32)
        self.restoreState()

def yellow_box(text, is_sub=False, is_red=False):
    """Generates a soft yellow highlighter callout box for assignments/prompts."""
    text_color = "#C00000" if is_red else "#1A1A1A"
    style = ParagraphStyle(
        f'YellowPrompt_{is_sub}_{is_red}',
        fontName='Helvetica-Bold',
        fontSize=9.5 if not is_sub else 8.8,
        leading=13 if not is_sub else 12,
        textColor=colors.HexColor(text_color)
    )
    p = Paragraph(text, style)
    t = Table([[p]], colWidths=[523])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF08A')), # Warm highlighter yellow
        ('BOX', (0, 0), (-1, -1), 0.7, colors.HexColor('#EAB308')),   # Distinctive yellow border
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t

def build_pdf():
    pdf_filename = "LI21_Exposicion_Demostracion_LR_Ronald_Saavedra.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=62,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor("#222222"),
        spaceAfter=4,
        spaceBefore=2
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    callout_intuitive = ParagraphStyle(
        'CalloutIntuitive',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor("#0f5132")
    )

    callout_technical = ParagraphStyle(
        'CalloutTechnical',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor("#084298")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
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

    # Intro instructions in yellow
    story.append(yellow_box("Siga las instrucciones siguientes:"))
    story.append(Spacer(1, 2))

    # Point 1
    story.append(yellow_box("1. Ingresar a la plataforma de Google Colab"))
    p1_desc = (
        "<b>Enlace Oficial:</b> <font color='#0055aa'><u>https://colab.research.google.com/</u></font><br/>"
        "• <i>Explicación sencilla:</i> Google Colab es un entorno web gratuito que nos permite ejecutar programas pesados de inteligencia artificial en computadoras virtuales de Google, sin necesidad de instalar librerías complejas en nuestra propia máquina.<br/>"
        "• <i>Detalle técnico:</i> Entorno interactivo Jupyter basado en Linux con asignación dinámica de memoria RAM y CPU, configurado con soporte para computación distribuida mediante Apache Spark (PySpark)."
    )
    story.append(Paragraph(p1_desc, body))
    story.append(Spacer(1, 2))

    # Point 2
    story.append(yellow_box('2. Crear un cuaderno que tenga el siguiente nombre: <font color="#C00000">rsaavedra</font>_lr2.ipynb<br/><font size="7.5" color="#555555">Lo que está en rojo es su letra de primer nombre, seguido de su apellido.</font>'))
    p2_desc = (
        "• <i>Explicación sencilla:</i> Se cumplió la regla institucional de nomenclatura: 'r' (inicial de Ronald) + 'saavedra' + sufijo del laboratorio '_lr2.ipynb'.<br/>"
        "• <i>Detalle técnico:</i> Cuaderno creado bajo el estándar JSON <code>nbformat 4.2</code> con 21 celdas estructuradas que aseguran trazabilidad completa de código y visualizaciones."
    )
    story.append(Paragraph(p2_desc, body))
    story.append(Spacer(1, 2))

    # Point 3
    story.append(yellow_box("3. Mostrar el usuario asociado a su cuaderno de trabajo."))
    story.append(Spacer(1, 2))
    
    # User's genuine screenshot
    if os.path.exists("evidencia_colab_real_cropped.png"):
        story.append(Image("evidencia_colab_real_cropped.png", width=460, height=170))
        story.append(Spacer(1, 3))
    
    p3_desc = (
        "<b>Evidencia Oficial de Identidad:</b> Captura de pantalla de la sesión activa en Google Colab. "
        "Se verifica la identidad del estudiante <b>Ronald Joel Saavedra Vargas</b> (cuenta <code>Joel Saavedra Vargas</code>) "
        "con el cuaderno de trabajo <b><code>rsaavedra_lr2.ipynb</code></b> en ejecución activa en la nube."
    )
    story.append(Paragraph(p3_desc, body))
    story.append(Spacer(1, 2))

    # Point 4
    p4_prompt = (
        "4. Seleccionar un dataset, NO DEBE REPETIRSE CON OTRO QUE HAYA ELEGIDO ALGUIEN EN LA CLASE "
        "(DECLARAR QUÉ DATASET USARÁ EN EL GRUPO DE WHATSAPP, SE RESPETA EL PRIMERO QUE ENVIÓ EL ENLACE DEL DATASET "
        "SELECCIONADO, CONSIDERE QUE PUEDE MANDAR UN ENLACE DIFERENTE DESDE OTRO DOMINIO Y CONTENER EL MISMO DATASET, "
        "DEBE REVISAR PREVIAMENTE)"
    )
    story.append(yellow_box(p4_prompt, is_red=True))
    p4_desc = (
        "<b>Dataset Seleccionado y Reservado:</b> Combined Cycle Power Plant (CCPP) - Archivo: <code>Folds5x2_pp.csv</code><br/>"
        "<b>Enlace Oficial UCI:</b> <font color='#0055aa'><u>https://archive.ics.uci.edu/dataset/294/combined+cycle+power+plant</u></font><br/>"
        "• <i>Explicación sencilla:</i> Elegimos los datos de una central eléctrica real durante 6 años. Predecimos cuánta electricidad genera en base al clima (calor, humedad y presión del aire). Registrado en WhatsApp a nombre de Ronald Saavedra para garantizar exclusividad.<br/>"
        "• <i>Detalle técnico:</i> 9,568 observaciones continuas horarias tomadas a plena carga con 4 sensores ambientales y la potencia de salida como target."
    )
    story.append(Paragraph(p4_desc, body))
    story.append(Spacer(1, 2))

    # Point 5
    story.append(yellow_box("5. Aplicar todo lo que ha ejecutado en el LI22"))
    p5_desc = (
        "• <i>Explicación sencilla:</i> Usamos Apache Spark para que la computadora procese los datos como si tuviera múltiples cerebros trabajando a la vez. Agrupamos las características en un solo paquete y le pedimos al algoritmo que encuentre la recta que mejor predice la energía.<br/>"
        "• <i>Detalle técnico:</i> Implementación en PySpark MLlib: creación de <code>SparkSession(appName='rsaavedra_lr2')</code>, vectorización densa con <code>VectorAssembler</code>, partición determinística 80% entrenamiento (7,654 filas) y 20% prueba (1,914 filas, <code>seed=42</code>), ajuste con <code>LinearRegression</code> y transformación de predicciones a tuplas RDD mediante <code>.map(tuple)</code>."
    )
    story.append(Paragraph(p5_desc, body))

    # Page Break for Presentation Section
    story.append(PageBreak())

    # Point 6 Header
    story.append(yellow_box("6. Preparar una breve presentación explicando los siguientes puntos:"))
    story.append(Spacer(1, 2))

    # 6.a
    story.append(yellow_box("a. Investigue y describa qué es una regresión lineal.", is_sub=True))
    p6a_desc = (
        "<b>1. Explicación Intuitiva (Para todo público):</b><br/>"
        "Imagina que quieres estimar el precio de una taza de café en función del tamaño del vaso. Intuitivamente sabes que a vaso más grande, mayor precio. "
        "Si dibujas muchos cafés en un gráfico y con una regla trazas <i>la línea recta que pase lo más cerca posible de todos los puntos</i>, "
        "has creado una <b>Regresión Lineal</b>. Esa línea te dice dos cosas: el precio mínimo de partida (la base) y cuánto dinero aumenta por cada centímetro que crece el vaso.<br/><br/>"
        "<b>2. Formulación Matemática Rigurosa:</b><br/>"
        "La Regresión Lineal Múltiple modela la variable continua dependiente <i>y</i> como una combinación lineal ponderada de <i>n</i> variables predictoras más un error aleatorio:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε = xᵀβ + ε</b><br/>"
        "Donde <b>y</b> es la potencia neta (MW), <b>x</b> es el vector de variables del clima, <b>β₀</b> es el intercepto (ordenada al origen), "
        "<b>βᵢ</b> son las pendientes parciales que miden el impacto individual de cada variable manteniendo las demás fijas (ceteris paribus), "
        "y <b>ε</b> es el residuo o perturbación no explicada.<br/><br/>"
        "<b>3. Función de Pérdida y Métodos de Optimización (OLS vs. Gradiente Descendente):</b><br/>"
        "El objetivo es minimizar la Suma de Residuos al Cuadrado: <i>RSS(β) = Σ(yᵢ - ŷᵢ)²</i>.<br/>"
        "• <b>Mínimos Cuadrados Ordinarios (OLS):</b> Solución analítica exacta mediante cálculo matricial: <b>β̂ = (XᵀX)⁻¹ Xᵀy</b>. Es óptima en un solo paso, pero invertir matrices gigantes consume memoria cúbica <i>O(d³)</i>.<br/>"
        "• <b>Descenso de Gradiente (Gradient Descent / L-BFGS):</b> Método iterativo que va ajustando los coeficientes paso a paso en sentido opuesto a la pendiente del error. Es el estándar en Big Data y Spark MLlib porque procesa terabytes divididos entre muchos nodos de forma escalable.<br/><br/>"
        "<b>4. Supuestos Clave de Gauss-Markov (Condiciones para que el modelo sea MELI / BLUE):</b><br/>"
        "Para que los estimadores sean insesgados y de varianza mínima: 1) Linealidad en parámetros, 2) Homocedasticidad (la dispersión del error es constante), "
        "3) No autocorrelación (los errores son independientes entre sí), 4) Normalidad de residuos (distribución en campana de Gauss ε ~ N(0, σ²)), y 5) No multicolinealidad perfecta."
    )
    story.append(Paragraph(p6a_desc, body))
    story.append(Spacer(1, 2))

    # 6.b
    story.append(yellow_box("b. Desarrolle para qué tipo de escenarios se aplica LR", is_sub=True))
    p6b_desc = (
        "<b>1. Casos Reales en la Industria:</b><br/>"
        "• <i>Sector Eléctrico:</i> Pronóstico de la potencia entregada a la red nacional según el calor y la presión atmosférica (nuestro proyecto CCPP).<br/>"
        "• <i>Finanzas y Banca:</i> Evaluación de solvencia de clientes y fijación de precios en el mercado inmobiliario según metros cuadrados y ubicación.<br/>"
        "• <i>Comercio y Retail:</i> Estimación de ventas semanales basándose en inversión publicitaria en redes y ofertas aplicadas.<br/>"
        "• <i>Medicina:</i> Predicción del nivel de glucosa o tiempo de recuperación de un paciente en función de la dosis de fármaco administrada.<br/><br/>"
        "<b>2. Criterios de Selección: ¿Cuándo SÍ y cuándo NO utilizar Regresión Lineal?</b><br/>"
        "• <b>Cuándo SÍ:</b> Cuando lo que queremos predecir es un número continuo (dinero, megawatts, temperatura); cuando la ley o el negocio exige <i>explicar con absoluta transparencia</i> qué peso tiene cada variable; y como punto de partida veloz antes de modelos complejos.<br/>"
        "• <b>Cuándo NO:</b> Cuando queremos clasificar categorías (ej. detectar si un correo es 'Spam' o 'No Spam'); o cuando el fenómeno tiene quiebres bruscos y curvas no lineales que una recta no puede seguir."
    )
    story.append(Paragraph(p6b_desc, body))

    # Page Break for Dataset Description
    story.append(PageBreak())

    # 6.c
    story.append(yellow_box("c. Describa de qué trata su DATASET seleccionado.", is_sub=True))
    p6c_desc = (
        "<b>1. Explicación Intuitiva: ¿Qué es una Central de Ciclo Combinado?</b><br/>"
        "Imagina que cocinas en una hornilla de gas: la llama calienta directamente la sartén (primer motor: <i>turbina de gas</i>). "
        "Pero en lugar de dejar que el humo y calor salgan por la chimenea, colocas encima una caldera con agua; el vapor caliente a alta presión hace girar un segundo molino "
        "(segundo motor: <i>turbina de vapor</i>). Al reciclar el calor de escape, ¡obtenemos dos fuentes de energía con el mismo combustible!<br/><br/>"
        "<b>2. Detalle de las Variables Físicas del Dataset (Folds5x2_pp.csv):</b><br/>"
        "Contiene 9,568 lecturas de sensores tomadas en tiempo real durante 6 años de operación continua a plena carga:"
    )
    story.append(Paragraph(p6c_desc, body))

    # Table of Dataset Variables
    table_data = [
        [
            Paragraph("Variable", table_header),
            Paragraph("Nombre Físico", table_header),
            Paragraph("Unidad", table_header),
            Paragraph("Rango", table_header),
            Paragraph("Correlación", table_header),
            Paragraph("Impacto Físico en la Generación", table_header)
        ],
        [
            Paragraph("<b>AT</b>", table_cell_center),
            Paragraph("Ambient Temperature (Temperatura)", table_cell),
            Paragraph("°C", table_cell_center),
            Paragraph("1.81 a 37.11", table_cell_center),
            Paragraph("<b>-0.9481</b>", table_cell_center),
            Paragraph("<b>Impacto más destructor.</b> El calor dilata el aire (menor densidad); el compresor traga menos masa de oxígeno y la turbina produce menos energía.", table_cell)
        ],
        [
            Paragraph("<b>V</b>", table_cell_center),
            Paragraph("Exhaust Vacuum (Vacío de Escape)", table_cell),
            Paragraph("cm Hg", table_cell_center),
            Paragraph("25.36 a 81.56", table_cell_center),
            Paragraph("<b>-0.8698</b>", table_cell_center),
            Paragraph("Mide la contrapresión en el condensador de vapor. A mayor contrapresión, menor fuerza tiene el vapor al expandirse.", table_cell)
        ],
        [
            Paragraph("<b>AP</b>", table_cell_center),
            Paragraph("Ambient Pressure (Presión Atmosférica)", table_cell),
            Paragraph("mbar", table_cell_center),
            Paragraph("992.89 a 1033.3", table_cell_center),
            Paragraph("<b>+0.5184</b>", table_cell_center),
            Paragraph("Un barómetro alto comprime naturalmente el aire, empujando más masa hacia la combustión y ganando potencia.", table_cell)
        ],
        [
            Paragraph("<b>RH</b>", table_cell_center),
            Paragraph("Relative Humidity (Humedad Relativa)", table_cell),
            Paragraph("%", table_cell_center),
            Paragraph("25.56 a 100.16", table_cell_center),
            Paragraph("<b>+0.3898</b>", table_cell_center),
            Paragraph("El contenido de vapor de agua altera la capacidad calorífica del aire durante el encendido de los inyectores.", table_cell)
        ],
        [
            Paragraph("<b>PE</b>", table_cell_center),
            Paragraph("<b>Electrical Output (Potencia Neta)</b>", table_cell_bold),
            Paragraph("<b>MW</b>", table_cell_center),
            Paragraph("420.26 a 495.76", table_cell_center),
            Paragraph("<b>1.0000</b>", table_cell_center),
            Paragraph("<b>Variable Objetivo (Label).</b> Megavatios netos producidos por hora por toda la central termoeléctrica.", table_cell_bold)
        ]
    ]

    t_dataset = Table(table_data, colWidths=[42, 115, 42, 65, 75, 184])
    t_dataset.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#F9F9F9")]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#EBF3FB")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 6))

    # 6.d
    story.append(yellow_box("d. Describa los pasos del ciclo y su relación con su código:", is_sub=True))
    if os.path.exists("diagrama_ciclo_ml.png"):
        story.append(Image("diagrama_ciclo_ml.png", width=520, height=88))
        story.append(Spacer(1, 3))

    p6d_table_data = [
        [
            Paragraph("Fase del Ciclo", table_header),
            Paragraph("Significado Intuitivo y Metodológico", table_header),
            Paragraph("Línea de Código en PySpark (rsaavedra_lr2.ipynb)", table_header)
        ],
        [
            Paragraph("<b>1. Recolección de Datos</b>", table_cell_bold),
            Paragraph("Cargar la tabla de datos a la memoria de Spark reconociendo nombres y números.", table_cell),
            Paragraph("<code>df = spark.read.csv('Folds5x2_pp.csv', header=True, inferSchema=True)</code>", table_cell)
        ],
        [
            Paragraph("<b>2. Preparación y Limpieza</b>", table_cell_bold),
            Paragraph("Revisar que no existan huecos ni datos faltantes. Confirmamos 0 nulos en las 9,568 filas.", table_cell),
            Paragraph("<code>df.select([count(when(isnan(c) | col(c).isNull(), c)) for c in df.columns]).show()</code>", table_cell)
        ],
        [
            Paragraph("<b>3. Feature Engineering</b>", table_cell_bold),
            Paragraph("Spark exige juntar las 4 variables independientes (AT, V, AP, RH) dentro de un solo paquete compacto.", table_cell),
            Paragraph("<code>assembler = VectorAssembler(inputCols=['AT','V','AP','RH'], outputCol='features')</code><br/><code>final_df = assembler.transform(df).select('features', 'PE')</code>", table_cell)
        ],
        [
            Paragraph("<b>4. Entrenamiento y Validación</b>", table_cell_bold),
            Paragraph("Separar 80% para estudiar (train) y 20% para el examen final (test), entrenando la regresión.", table_cell),
            Paragraph("<code>train_data, test_data = final_df.randomSplit([0.8, 0.2], seed=42)</code><br/><code>lr = LinearRegression(featuresCol='features', labelCol='PE')</code><br/><code>lr_model = lr.fit(train_data)</code>", table_cell)
        ]
    ]

    t_ciclo = Table(p6d_table_data, colWidths=[105, 165, 253])
    t_ciclo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2a5298")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_ciclo)

    # Page Break for Demo & Results
    story.append(PageBreak())

    # 6.e
    story.append(yellow_box("e. Haga la demostración de ejecución en Google Colab.", is_sub=True))
    p6e_desc = (
        "<b>Guion Paso a Paso para la Exposición Oral ante el Docente:</b><br/>"
        "1. <b>Inicio:</b> Mostrar la celda 1 y 2 ejecutándose en vivo, creando la sesión de Spark <code>rsaavedra_lr2</code> sin advertencias de error.<br/>"
        "2. <b>Resiliencia en Carga:</b> Explicar la triple contingencia (lee el archivo local <code>Folds5x2_pp.csv</code> o lo descarga automáticamente del repositorio UCI).<br/>"
        "3. <b>Comprobación de Calidad:</b> Proyectar la tabla que demuestra que el 100% de los 9,568 registros están limpios (cero nulos).<br/>"
        "4. <b>Demostración de RDD (Exigencia del Docente en Guía):</b> Ejecutar las celdas de transformación:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <code>predictions_and_actuals_rdd.take(2)</code> devuelve objetos estructurados <code>Row(prediction=468.21, PE=464.0)</code>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <code>predictions_and_actuals_rdd.map(tuple).take(2)</code> transforma cada fila en tuplas nativas <code>(468.21, 464.0)</code>.<br/>"
        "5. <b>Panel Gráfico de Diagnóstico:</b> Mostrar en pantalla los 4 gráficos generados (Recta 45° de predicción perfecta, Histograma de Residuos Normal, Homocedasticidad y Barras de Coeficientes)."
    )
    story.append(Paragraph(p6e_desc, body))
    story.append(Spacer(1, 2))

    # 6.f
    story.append(yellow_box("f. Explique los resultados obtenidos.", is_sub=True))
    p6f_desc = (
        "<b>Ecuación Matemática Estimada por el Modelo PySpark:</b><br/>"
        "<font size='9'><b>PE = 458.9396 - 1.9840·(AT) - 0.2307·(V) + 0.0579·(AP) - 0.1599·(RH)</b></font><br/><br/>"
        "• <i>En palabras sencillas:</i> Si afuera hace más calor, la planta sufre mucho: por cada grado centígrado que sube la temperatura exterior, perdemos casi 2 Megawatts (suficiente para apagar 2,000 casas). Si la presión atmosférica sube, la planta respira mejor y ganamos energía.<br/>"
        "• <i>Desglose Técnico de Coeficientes Parciales (ceteris paribus):</i>"
    )
    story.append(Paragraph(p6f_desc, body))

    p6f_coef_table = [
        [
            Paragraph("Parámetro", table_header),
            Paragraph("Coeficiente (β)", table_header),
            Paragraph("Unidad Física", table_header),
            Paragraph("Interpretación Física y Termodinámica Rigurosa", table_header)
        ],
        [
            Paragraph("<b>Intercepto (β₀)</b>", table_cell_bold),
            Paragraph("<b>+458.9396</b>", table_cell_center),
            Paragraph("MW", table_cell_center),
            Paragraph("Potencia base teórica si todos los sensores climáticos marcaran matemáticamente cero.", table_cell)
        ],
        [
            Paragraph("<b>Temperatura (AT)</b>", table_cell_bold),
            Paragraph("<b>-1.9840</b>", table_cell_center),
            Paragraph("MW / °C", table_cell_center),
            Paragraph("<b>Factor dominante.</b> Por cada 1°C adicional en el ambiente, la planta <b>pierde en promedio 1.98 MW</b> por pérdida de densidad de aire.", table_cell)
        ],
        [
            Paragraph("<b>Vacío de Escape (V)</b>", table_cell_bold),
            Paragraph("<b>-0.2307</b>", table_cell_center),
            Paragraph("MW / cm Hg", table_cell_center),
            Paragraph("Por cada 1 cm Hg que sube la contrapresión del condensador, la potencia <b>cae en 0.23 MW</b> por menor caída entálpica en el vapor.", table_cell)
        ],
        [
            Paragraph("<b>Presión Atm. (AP)</b>", table_cell_bold),
            Paragraph("<b>+0.0579</b>", table_cell_center),
            Paragraph("MW / mbar", table_cell_center),
            Paragraph("Mayor presión barométrica comprime el aire de admisión, <b>ganando 0.058 MW</b> por cada milibar adicional.", table_cell)
        ],
        [
            Paragraph("<b>Humedad Rel. (RH)</b>", table_cell_bold),
            Paragraph("<b>-0.1599</b>", table_cell_center),
            Paragraph("MW / %", table_cell_center),
            Paragraph("Aislada de la temperatura, cada 1% adicional de humedad reduce levemente la potencia en 0.16 MW al enfriar la llama.", table_cell)
        ]
    ]

    t_coef = Table(p6f_coef_table, colWidths=[105, 80, 75, 263])
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
    p6g_prompt = (
        "g. Investigue sobre las métricas de error, cómo se las debe interpretar y cuándo elegir cuál; "
        "menciona cómo se interpreta cada una, por ejemplo, cada métrica a qué elementos toma más en cuenta."
    )
    story.append(yellow_box(p6g_prompt, is_sub=True))
    p6g_intro = (
        "<b>1. Explicación Intuitiva para Todo Público:</b><br/>"
        "Imagina que tiramos flechas a una diana. Si queremos calificar qué tan buenos somos arqueros, no basta con un solo número:<br/>"
        "• <b>R²:</b> Es la 'nota de examen' del modelo (del 0 al 100%). Nuestro modelo obtuvo <b>92.84%</b>, lo que significa que comprende casi a la perfección el comportamiento de la central eléctrica.<br/>"
        "• <b>RMSE (4.51 MW):</b> Es el 'castigador de fallos grandes'. Si una flecha se desvía por 10 metros, la penaliza 100 veces más fuerte. Nos dice que el error típico en megawatts es mínimo.<br/>"
        "• <b>MAE (3.61 MW):</b> Es el 'promedio justo y bondadoso'. Mide el error promedio simple en megawatts sin dramatizar si hubo un pico atípico.<br/>"
        "• <b>MAPE (0.79%):</b> El porcentaje que le mostramos al gerente de la planta: <i>'Señor, nuestro modelo sólo se equivoca en un 0.8% frente a la realidad'</i>.<br/><br/>"
        "<b>2. Comparativa Técnica y Criterios Rigurosos de Elección:</b>"
    )
    story.append(Paragraph(p6g_intro, body))

    metrics_table_data = [
        [
            Paragraph("Métrica", table_header),
            Paragraph("Fórmula", table_header),
            Paragraph("Valor Obtenido", table_header),
            Paragraph("¿A qué elementos toma más en cuenta?", table_header),
            Paragraph("Criterio de Elección: ¿Cuándo usarla?", table_header)
        ],
        [
            Paragraph("<b>R² (Determinación)</b>", table_cell_bold),
            Paragraph("1 - [SS_res / SS_tot]", table_cell_center),
            Paragraph("<b>0.9284<br/>(92.84%)</b>", table_cell_center),
            Paragraph("Porcentaje de varianza total explicado por las variables. Adimensional (0 a 1).", table_cell),
            Paragraph("<b>Para medir ajuste global.</b> Comunica qué tan bien el modelo aprendió la tendencia general de los datos.", table_cell)
        ],
        [
            Paragraph("<b>RMSE (Raíz Cuadrática)</b>", table_cell_bold),
            Paragraph("√[ (1/N) Σ(y - ŷ)² ]", table_cell_center),
            Paragraph("<b>4.5110 MW</b>", table_cell_center),
            Paragraph("<b>Penaliza fuertemente errores grandes / outliers</b> porque eleva al cuadrado los desvíos antes de promediar.", table_cell),
            Paragraph("<b>Cuando los fallos grandes son peligrosos.</b> Ej: una subestimación de 20 MW sobrecargaría y apagaría la red.", table_cell)
        ],
        [
            Paragraph("<b>MAE (Absoluto Medio)</b>", table_cell_bold),
            Paragraph("(1/N) Σ |y - ŷ|", table_cell_center),
            Paragraph("<b>3.6124 MW</b>", table_cell_center),
            Paragraph("<b>Pondera todos los desvíos de forma lineal y uniforme.</b> Es inmune a picos de ruido aislados.", table_cell),
            Paragraph("<b>Para conocer el error típico del día a día</b> sin que mediciones anómalas extremas inflen artificialmente el reporte.", table_cell)
        ],
        [
            Paragraph("<b>MSE (Cuadrático Medio)</b>", table_cell_bold),
            Paragraph("(1/N) Σ (y - ŷ)²", table_cell_center),
            Paragraph("<b>20.3488 MW²</b>", table_cell_center),
            Paragraph("Varianza del error. Al estar en unidades al cuadrado (MW²), carece de significado intuitivo directo.", table_cell),
            Paragraph("<b>Como función matemática de costo</b> para optimizar algoritmos numéricos, pero NO para exponer ante personas.", table_cell)
        ],
        [
            Paragraph("<b>MAPE (Porcentual Medio)</b>", table_cell_bold),
            Paragraph("(100/N) Σ |(y-ŷ)/y|", table_cell_center),
            Paragraph("<b>0.795 %</b>", table_cell_center),
            Paragraph("Mide el tamaño relativo del error en comparación con el valor real de producción.", table_cell),
            Paragraph("<b>Para directivos y audiencia no técnica.</b> Permite decir que el desvío es inferior al 1% de la capacidad de la planta.", table_cell)
        ]
    ]

    t_metrics = Table(metrics_table_data, colWidths=[85, 85, 70, 140, 143])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1b365d")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9F9F9")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 6))

    conclusion_box = [
        [
            Paragraph(
                "<b>SÍNTESIS FINAL PARA LA DEFENSA ORAL ANTE EL DOCENTE:</b><br/>"
                "• El modelo de Regresión Lineal Múltiple entrenado en <b>Apache Spark MLlib</b> explica el <b>92.84%</b> de la energía generada ($R^2 = 0.9284$) con un error típico de sólo <b>4.51 MW</b> ($<1.0\%$).<br/>"
                "• La variable con mayor impacto destructivo es la <b>Temperatura Ambiente (AT)</b> con <b>-1.98 MW/°C</b>, seguida del Vacío de Escape con <b>-0.23 MW/cm Hg</b>.<br/>"
                "• El cuaderno <b><code>rsaavedra_lr2.ipynb</code></b> cumple el 100% de los requerimientos de la guía docente: verificación de identidad en Google Colab, reserva exclusiva en WhatsApp, pipeline de Spark MLlib, conversión RDD con <code>.map(tuple)</code> y gráficos diagnósticos.",
                body
            )
        ]
    ]
    t_conclusion = Table(conclusion_box, colWidths=[523])
    t_conclusion.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF3FB")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#2a5298")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_conclusion)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully with yellow highlighted prompts and dual redacting.")

if __name__ == '__main__':
    build_pdf()
