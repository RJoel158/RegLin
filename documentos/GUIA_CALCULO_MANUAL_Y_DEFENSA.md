# GUÍA MAESTRA DE ENTENDIMIENTO, CÁLCULO MANUAL Y DEFENSA EN PIZARRA
## Regresión Lineal Múltiple aplicada a la Central de Ciclo Combinado (CCPP)

**Asignatura:** Tecnologías Emergentes I  
**Institución:** Universidad del Valle (UNIVALLE)  
**Estudiante:** Ronald Joel Saavedra Vargas  
**Docente:** Lic. Efraín Luna Flores  
**Cuaderno:** `rsaavedra_lr2.ipynb` | **Dataset:** `Folds5x2_pp.csv`  

---

## 1. ¿QUÉ ES REALMENTE UNA REGRESIÓN LINEAL? (Concepto Intuitivo y Matemático)

### 1.1. La Idea Central en Palabras Cotidianas
Imagina que eres el conductor de un camión de mudanzas y quieres calcular cuánto cobrar por un viaje antes de salir.
Sabes intuitivamente que el precio depende de:
1. La distancia en kilómetros ($X_1$).
2. El peso de la carga en toneladas ($X_2$).
3. Los pisos que habrá que subir por escalera ($X_3$).

¿Cómo calculas el precio final ($Y$)? Estableces una **tarifa base fija** solo por encender el camión (el **intercepto** $\beta_0$) y luego **sumas o restas una tarifa proporcional por cada variable** (los **coeficientes** $\beta_1, \beta_2, \beta_3$).
Eso es exactamente una **Regresión Lineal**: un modelo matemático que encuentra la mejor combinación de sumas y restas ponderadas para conectar variables de entrada (causas) con un resultado continuo (efecto).

---

### 1.2. De la Recta al Hiperplano (Geometría del Modelo)

* **Con 1 sola variable predictora ($X$ y $Y$):**
  $$y = \beta_0 + \beta_1 x + \varepsilon$$
  Geométricamente es una **LÍNEA RECTA en un plano 2D**.
  - $\beta_0$: Es el punto donde la recta corta el eje vertical $Y$ (cuando $x=0$).
  - $\beta_1$: Es la **pendiente** o inclinación de la recta. Si caminas 1 paso hacia la derecha en $X$, $\beta_1$ te dice cuántos pasos subes (si es positivo) o bajas (si es negativo) en $Y$.

* **Con 2 variables predictoras ($X_1, X_2$ y $Y$):**
  $$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \varepsilon$$
  Geométricamente es un **PLANO INCLINADO en un espacio 3D** (como una tabla inclinada flotando en una habitación).

* **Con 4 variables (Nuestro caso real en CCPP: $AT, V, AP, RH$):**
  $$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_3 + \beta_4 x_4 + \varepsilon$$
  Geométricamente ya no podemos dibujarlo con nuestros ojos porque vive en 5 dimensiones ($4 \text{ entradas} + 1 \text{ salida}$), pero matemáticamente se comporta exactamente igual: se llama **HIPERPLANO**.

---

### 1.3. Desglose Símbolo por Símbolo de la Fórmula General

$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n + \varepsilon$$

En notación matricial compacta:
$$y = \mathbf{x}^T \boldsymbol{\beta} + \varepsilon$$

| Símbolo | Nombre Técnico | Significado en Lenguaje Común | En nuestro Caso de la Planta Eléctrica |
| :---: | :--- | :--- | :--- |
| $y$ | **Variable Dependiente / Objetivo (Label)** | Lo que queremos adivinar o pronosticar. | La **Potencia Eléctrica Neta ($PE$)** en Megawatts. |
| $x_1, x_2, \dots$ | **Variables Independientes / Predictoras (Features)** | Las pistas o factores conocidos que causan el cambio. | $AT$ (Temperatura), $V$ (Vacío), $AP$ (Presión), $RH$ (Humedad). |
| $\beta_0$ | **Intercepto (Sesgo / Bias)** | El valor de partida cuando todas las $X$ valen cero. | Potencia base teórica si no hubiera clima exterior ($458.94\text{ MW}$). |
| $\beta_1, \beta_2, \dots$ | **Coeficientes de Regresión Parcial (Pesos)** | El multiplicador de impacto de cada variable. Nos dice cuánto cambia $y$ si esa $x$ sube 1 unidad, **manteniendo todas las demás fijas** (*ceteris paribus*). | Si la temperatura ($AT$) sube $1^\circ\text{C}$, perdemos $1.98\text{ MW}$ ($\beta_{\text{AT}} = -1.9840$). |
| $\varepsilon$ | **Residuo o Término de Error** | La diferencia entre la realidad y la recta. Lo que el modelo no puede explicar (ruido, viento, etc.). | Pequeña desviación física entre el sensor real y la predicción. |

---

## 2. LA FÓRMULA DE NUESTRO PROYECTO (CCPP) Y CÓMO SE USA PASO A PASO

### 2.1. Ecuación Entrenada en Apache Spark
Tras entrenar sobre los datos con PySpark MLlib, la ecuación matemática obtenida es:

$$\widehat{\text{PE}} = 458.9396 - 1.9840 \cdot \text{AT} - 0.2307 \cdot \text{V} + 0.0579 \cdot \text{AP} - 0.1599 \cdot \text{RH}$$

*(El sombrerito $\widehat{\text{PE}}$ significa "potencia estimada o predicha por el modelo", para diferenciarla de la potencia real medida).*

---

### 2.2. Demostración Práctica con Números Reales (Para hacer en vivo en clase)

Supongamos que los sensores de la planta marcan los siguientes valores meteorológicos en un momento determinado:
* Temperatura Ambiente: $\text{AT} = 14.47^\circ\text{C}$
* Vacío de Escape: $\text{V} = 41.76\text{ cm Hg}$
* Presión Atmosférica: $\text{AP} = 1021.98\text{ mbar}$
* Humedad Relativa: $\text{RH} = 78.41\%$

**¿Cómo calcula el modelo la predicción paso a paso?**

1. **Paso 1 (Escribir la fórmula reemplazando los números):**
   $$\widehat{\text{PE}} = 458.9396 - (1.9840 \times 14.47) - (0.2307 \times 41.76) + (0.0579 \times 1021.98) - (0.1599 \times 78.41)$$

2. **Paso 2 (Multiplicar cada impacto individual):**
   * Impacto de la Temperatura: $-(1.9840 \times 14.47) = \mathbf{-28.7085\text{ MW}}$
   * Impacto del Vacío: $-(0.2307 \times 41.76) = \mathbf{-9.6340\text{ MW}}$
   * Impacto de la Presión: $+(0.0579 \times 1021.98) = \mathbf{+59.1726\text{ MW}}$
   * Impacto de la Humedad: $-(0.1599 \times 78.41) = \mathbf{-12.5378\text{ MW}}$

3. **Paso 3 (Sumar todo aritméticamente partiendo de la base):**
   $$\widehat{\text{PE}} = 458.9396 - 28.7085 - 9.6340 + 59.1726 - 12.5378 = \mathbf{467.2319\text{ MW}}$$

4. **Paso 4 (Comparar con el sensor real):**
   * El wattímetro real de la planta midió exactamente: $\text{PE}_{\text{real}} = \mathbf{464.00\text{ MW}}$.
   * El error o residuo de esta predicción fue:
     $$e = \text{PE}_{\text{real}} - \widehat{\text{PE}} = 464.00 - 467.2319 = \mathbf{-3.23\text{ MW}}$$
   * ¡El modelo se equivocó en apenas $3.23\text{ MW}$ sobre $464\text{ MW}$, un error relativo de apenas **$0.69\%$**!

---

### 2.3. ¿Por qué cada variable tiene ese signo? (Física Termodinámica Explicada Fácil)

1. **¿Por qué la Temperatura ($\text{AT}$) tiene signo NEGATIVO ($-1.9840$)?**
   * *Explicación Física:* El calor dilata el aire, haciéndolo menos denso y más liviano. La turbina de gas es un compresor gigante que aspira aire; si el aire es liviano, entra **menos masa de oxígeno por segundo**, la llama quema con menor fuerza y la turbina pierde potencia.
2. **¿Por qué el Vacío ($\text{V}$) tiene signo NEGATIVO ($-0.2307$)?**
   * *Explicación Física:* $V$ mide la presión en el condensador de la turbina de vapor. Si esa presión sube (peor vacío), el vapor no se puede expandir libremente hacia la salida, creando una resistencia ("freno de contrapresión") que reduce el trabajo mecánico.
3. **¿Por qué la Presión Atmosférica ($\text{AP}$) tiene signo POSITIVO ($+0.0579$)?**
   * *Explicación Física:* Cuando el barómetro sube, la atmósfera comprime el aire naturalmente antes de entrar a la central. Hay más moléculas de aire apretadas por metro cúbico, lo que alimenta mejor al compresor y genera más energía.
4. **¿Por qué la Humedad ($\text{RH}$) tiene signo NEGATIVO ($-0.1599$)?**
   * *Explicación Física:* El vapor de agua disperso en el aire absorbe calor durante la ignición en lugar de empujar la turbina, reduciendo levemente la eficiencia térmica de la combustión.

---

## 3. CÓMO CALCULAR LOS BETAS A MANO EN LA PIZARRA (Toy Example Paso a Paso)

Si el docente te pide en la pizarra: *"Ronald, demuéstrame cómo se calculan los betas a mano con lápiz y papel sin usar computadora"*, este es el ejemplo perfecto que puedes resolver en 3 minutos.

### 3.1. Caso Simple (1 Variable Predictora $X$ y Objetivo $Y$)
Supongamos un conjunto de prueba de solo 3 observaciones ($N=3$):
* $X$ (Temperatura): $[1, 2, 3]^\circ\text{C}$
* $Y$ (Potencia): $[10, 8, 3]\text{ MW}$

#### Paso 1: Calcular los promedios (medias)
$$\bar{X} = \frac{1 + 2 + 3}{3} = \frac{6}{3} = \mathbf{2.0}$$
$$\bar{Y} = \frac{10 + 8 + 3}{3} = \frac{21}{3} = \mathbf{7.0}$$

#### Paso 2: Construir la tabla de desviaciones
| $i$ | $X_i$ | $Y_i$ | $(X_i - \bar{X})$ | $(Y_i - \bar{Y})$ | Producto: $(X_i - \bar{X})(Y_i - \bar{Y})$ | Cuadrado: $(X_i - \bar{X})^2$ |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | 1 | 10 | $1 - 2 = -1$ | $10 - 7 = +3$ | $(-1) \times (+3) = \mathbf{-3}$ | $(-1)^2 = \mathbf{1}$ |
| 2 | 2 | 8  | $2 - 2 = 0$  | $8 - 7 = +1$  | $(0) \times (+1) = \mathbf{0}$   | $(0)^2 = \mathbf{0}$ |
| 3 | 3 | 3  | $3 - 2 = +1$ | $3 - 7 = -4$  | $(+1) \times (-4) = \mathbf{-4}$ | $(+1)^2 = \mathbf{1}$ |
| **Sumas ($\sum$)** | - | - | $0$ | $0$ | **$\sum = -7$** | **$\sum = 2$** |

#### Paso 3: Calcular la Pendiente $\beta_1$
La fórmula de Mínimos Cuadrados Ordinarios es la covarianza dividida entre la varianza de $X$:
$$\beta_1 = \frac{\sum (X_i - \bar{X})(Y_i - \bar{Y})}{\sum (X_i - \bar{X})^2} = \frac{-7}{2} = \mathbf{-3.5}$$
*(Interpretación: Por cada grado de temperatura, la potencia cae 3.5 MW).*

#### Paso 4: Calcular el Intercepto $\beta_0$
$$\beta_0 = \bar{Y} - \beta_1 \cdot \bar{X} = 7.0 - (-3.5 \times 2.0) = 7.0 - (-7.0) = 7.0 + 7.0 = \mathbf{14.0}$$

#### Resultado de la Recta:
$$\widehat{Y} = 14.0 - 3.5 \cdot X$$

*Verificación de predicciones:*
* Para $X=1$: $\widehat{Y} = 14 - 3.5(1) = \mathbf{10.5}$ (real era 10, residuo $e_1 = 10 - 10.5 = -0.5$).
* Para $X=2$: $\widehat{Y} = 14 - 3.5(2) = \mathbf{7.0}$ (real era 8, residuo $e_2 = 8 - 7.0 = +1.0$).
* Para $X=3$: $\widehat{Y} = 14 - 3.5(3) = \mathbf{3.5}$ (real era 3, residuo $e_3 = 3 - 3.5 = -0.5$).
* **Suma total de residuos:** $(-0.5) + (+1.0) + (-0.5) = \mathbf{0.0}$. *(Propiedad fundamental de OLS: la suma de errores siempre es cero).*

---

### 3.2. Caso Matricial para Múltiples Variables (La Ecuación Normal de OLS)

Cuando hay varias variables ($X_1, X_2, \dots, X_n$), no se puede hacer una tabla simple; se usa álgebra matricial:

$$\boldsymbol{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

**¿Cómo funciona esta fórmula paso a paso?**
1. **La Matriz $\mathbf{X}$:** Se toma la tabla de datos y se le añade una primera columna de unos (llamada "columna de sesgo") para que el modelo pueda calcular $\beta_0$:
   $$\mathbf{X} = \begin{bmatrix} 1 & x_{11} & x_{12} \\ 1 & x_{21} & x_{22} \\ 1 & x_{31} & x_{32} \end{bmatrix}$$
2. **$\mathbf{X}^T$ (Transpuesta):** Se rota la matriz convirtiendo filas en columnas.
3. **$\mathbf{X}^T \mathbf{X}$ (Producto):** Al multiplicarlas, se obtiene una matriz cuadrada que contiene todas las sumas de cuadrados y productos cruzados de las variables.
4. **$(\mathbf{X}^T \mathbf{X})^{-1}$ (Inversa):** Se invierte la matriz (el equivalente matricial a "dividir").
5. **Multiplicar por $\mathbf{X}^T \mathbf{y}$:** Da directamente el vector con los valores óptimos: $[\beta_0, \beta_1, \beta_2]^T$.

> **Pregunta típica del docente:** *"Ronald, si esta fórmula de OLS da la respuesta exacta en un solo paso, ¿por qué en Apache Spark usamos Descenso de Gradiente (L-BFGS) en lugar de esta fórmula?"*  
> **Tu respuesta brillante:** *"Porque para calcular la inversa de una matriz $(\mathbf{X}^T \mathbf{X})^{-1}$ la computadora requiere un tiempo cúbico $\mathcal{O}(d^3)$. Si tuviéramos un dataset con millones de filas y miles de columnas, la memoria RAM colapsaría al intentar invertir la matriz. En cambio, el Descenso de Gradiente en Spark va dando pequeños pasos iterativos en la dirección contraria a la pendiente del error sin necesidad de invertir ninguna matriz, lo que permite procesar terabytes de datos distribuidos entre muchos servidores."*

---

## 4. CÁLCULO MANUAL PASO A PASO DE TODAS LAS MÉTRICAS DE ERROR

Usemos las 3 observaciones de nuestro ejemplo anterior para calcular a mano todas las métricas:
* Valores Reales: $y = [10, 8, 3]$
* Valores Predichos: $\hat{y} = [10.5, 7.0, 3.5]$
* Número de datos: $N = 3$
* Media real: $\bar{y} = 7.0$

### Tabla de Errores Base:
| $i$ | Real ($y_i$) | Predicho ($\hat{y}_i$) | Error Residuo: $e_i = (y_i - \hat{y}_i)$ | Error Absoluto: $\|e_i\|$ | Error al Cuadrado: $e_i^2$ | Varianza Total: $(y_i - \bar{y})^2$ |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | 10 | 10.5 | $10 - 10.5 = -0.5$ | $0.5$ | $(-0.5)^2 = 0.25$ | $(10 - 7)^2 = 3^2 = 9$ |
| 2 | 8  | 7.0  | $8 - 7.0 = +1.0$   | $1.0$ | $(+1.0)^2 = 1.00$ | $(8 - 7)^2 = 1^2 = 1$  |
| 3 | 3  | 3.5  | $3 - 3.5 = -0.5$   | $0.5$ | $(-0.5)^2 = 0.25$ | $(3 - 7)^2 = (-4)^2 = 16$ |
| **Sumas** | - | - | $\sum e_i = \mathbf{0.0}$ | $\sum \|e_i\| = \mathbf{2.0}$ | $\text{SS}_{\text{res}} = \mathbf{1.50}$ | $\text{SS}_{\text{tot}} = \mathbf{26.0}$ |

---

### 4.1. MAE (Mean Absolute Error - Error Absoluto Medio)
Es simplemente el promedio de los errores sin signo (en valor absoluto):
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} |y_i - \hat{y}_i| = \frac{0.5 + 1.0 + 0.5}{3} = \frac{2.0}{3} = \mathbf{0.67\text{ MW}}$$
* **¿Qué significa?** En promedio simple, el modelo se desvía $0.67\text{ MW}$ de la realidad.
* **Propiedad clave:** Trata a todos los errores por igual. Si hay un error de 10 MW, solo aporta 10 al promedio. Es muy robusto ante ruidos.

---

### 4.2. MSE (Mean Squared Error - Error Cuadrático Medio)
Es el promedio de los errores elevados al cuadrado:
$$\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2 = \frac{0.25 + 1.00 + 0.25}{3} = \frac{1.50}{3} = \mathbf{0.50\text{ MW}^2}$$
* **¿Qué significa?** Es la varianza del error residual.
* **Propiedad clave:** Elevar al cuadrado castiga los errores grandes (un error de 4 vale 16, un error de 10 vale 100). Sus unidades están al cuadrado ($\text{MW}^2$), por lo que no se usa para hablar con personas, sino como fórmula matemática para que la computadora optimice.

---

### 4.3. RMSE (Root Mean Squared Error - Raíz del Error Cuadrático Medio)
Es la raíz cuadrada del MSE, para devolver el número a las unidades originales (Megawatts):
$$\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{0.50} = \mathbf{0.707\text{ MW}}$$
* **¿Por qué el RMSE ($0.71$) es mayor que el MAE ($0.67$)?**  
  Porque el error intermedio ($+1.0$) fue más grande que los otros dos ($0.5$). Al elevar al cuadrado, ese error más grande pesó más fuertemente en el resultado final.
* **Propiedad clave:** Es la métrica obligatoria cuando un error grande es muy peligroso para el negocio o la ingeniería.

---

### 4.4. $R^2$ (Coeficiente de Determinación - Bondad de Ajuste)
Mide **qué porcentaje de la variabilidad de la realidad fue capturado por el modelo**:
$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} = 1 - \frac{1.50}{26.00} = 1 - 0.0577 = \mathbf{0.9423} \quad (94.23\%)$$
* **¿Qué significa?** De toda la dispersión que tenían los datos originales ($26.0$), el modelo logró explicar el **$94.23\%$**, y solo quedó un $5.77\%$ de error residual no explicado.
* **Valores posibles:** 
  - $R^2 = 1.0$ (100%): Predicción perfecta sobre cada punto.
  - $R^2 = 0.0$: El modelo no sirve para nada (predice lo mismo que simplemente adivinar el promedio $\bar{y}$).
  - $R^2 < 0$: El modelo es peor que adivinar el promedio a ciegas.

---

### 4.5. MAPE (Mean Absolute Percentage Error - Error Porcentual Medio)
Calcula el error relativo porcentual frente a cada valor real:
$$\text{MAPE} = \frac{100\%}{N} \sum_{i=1}^{N} \left|\frac{y_i - \hat{y}_i}{y_i}\right| = \frac{100\%}{3} \left( \frac{0.5}{10} + \frac{1.0}{8} + \frac{0.5}{3} \right)$$
$$= \frac{100\%}{3} (0.050 + 0.125 + 0.167) = \frac{100\%}{3} (0.342) = \mathbf{11.4\%}$$
* **¿Qué significa?** El modelo tiene un desvío promedio relativo del $11.4\%$ respecto a la magnitud de los datos. En nuestro caso CCPP real con 9,568 filas, el MAPE dio **$0.79\%$** (un error de menos del 1%).

---

## 5. GUION MAESTRO PARA DEFENDER EN LA PIZARRA EN 3 MINUTOS

Si pasas a la pizarra durante la exposición, puedes seguir esta estructura:

1. **Apertura:**  
   *"Licenciado y compañeros, nuestro objetivo con el dataset CCPP es predecir la potencia eléctrica horaria de una central térmica que combina gas y vapor. Para ello, ajustamos un modelo de regresión lineal múltiple en Apache Spark."*
2. **Escribir la fórmula en la pizarra:**  
   $$PE = 458.94 - 1.98 \cdot AT - 0.23 \cdot V + 0.06 \cdot AP - 0.16 \cdot RH$$
3. **Explicar el comportamiento físico de los números:**  
   *"Fíjense en los signos: la temperatura exterior (AT) tiene el coeficiente negativo más alto (-1.98 MW/°C). Esto ocurre porque el aire caliente es menos denso, entra menos oxígeno a la turbina de gas y la planta pierde casi 2 MW por cada grado que sube el termómetro. En cambio, cuando sube la presión atmosférica (+0.06 MW/mbar), el aire entra más comprimido y ganamos potencia."*
4. **Resumir la calidad de las métricas:**  
   *"Evaluamos el modelo sobre 1,914 datos de prueba no vistos. Obtuvimos un $R^2$ de **0.9284**, lo que demuestra que el modelo explica el **92.84%** de la generación eléctrica. El error típico RMSE fue de apenas **4.51 MW** frente a una media de 454 MW, lo que representa un margen de error menor al 1% (MAPE = 0.79%)."*
5. **Cierre técnico con Spark:**  
   *"Comprobamos el flujo exigido en LI21 transformando las predicciones del DataFrame a RDD con `.rdd.map(tuple).take(2)` para validar que los objetos Row se mapean limpiamente a tuplas nativas, y los gráficos de residuos confirman que se cumplen los supuestos de normalidad y homocedasticidad de Gauss-Markov."*
