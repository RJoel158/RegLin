# LI21 - Exposición y Demostración de Regresión Lineal con PySpark

**Universidad:** Universidad del Valle (UNIVALLE)  
**Asignatura:** Tecnologías Emergentes I  
**Estudiante:** Ronald Joel Saavedra Vargas  
**Docente:** Lic. Efraín Luna Flores  
**Dataset:** Combined Cycle Power Plant (CCPP) (`Folds5x2_pp.csv`)  

---

## Estructura del Proyecto

```text
RegLin/
├── consignas/
│   └── LI21 - Exposicion con demostracion LR.pdf       # Guía oficial del docente
├── cuadernos/
│   └── rsaavedra_lr2.ipynb                             # Cuaderno Google Colab con código y salidas
├── datos/
│   ├── Folds5x2_pp.csv                                 # Dataset CCPP (9,568 observaciones)
│   └── analysis_report.json                            # Reporte numérico de métricas y correlaciones
├── documentos/
│   ├── LI21_Exposicion_Demostracion_LR_Ronald_Saavedra.pdf  # Informe oficial listo para entrega (5 págs)
│   ├── GUIA_CALCULO_MANUAL_Y_DEFENSA.md                # Explicación profunda y cálculo paso a paso a mano
│   ├── GUIA_EXPOSICION_LI21_RONALD_SAAVEDRA.md         # Guía de defensa oral y preguntas de examen
│   └── Teoria_Exposicion_CCPP_Ronald_Saavedra.md       # Marco teórico pedagógico
├── evidencias/
│   ├── logo_cube.png                                   # Isotipo UNIVALLE en alta resolución
│   ├── logo_seal.png                                   # Sello circular oficial UNIVALLE
│   ├── captura_colab_original.png                      # Captura base de la guía docente
│   ├── diagrama_ciclo_ml.png                           # Diagrama oficial de 4 fases de ML
│   ├── evidencia_colab_real.png                        # Captura real completa de la sesión de Colab
│   └── evidencia_colab_real_cropped.png                # Captura encuadrada para el informe PDF
├── scripts/
│   ├── analyze_data.py                                 # Script de análisis exploratorio y OLS exacto
│   └── build_documento_pdf_v3.py                       # Generador del informe PDF en ReportLab
├── Folds5x2_pp.csv                                     # Enlace directo en raíz para Colab / IDE
├── rsaavedra_lr2.ipynb                                 # Enlace directo en raíz para Colab / IDE
└── LI21_Exposicion_Demostracion_LR_Ronald_Saavedra.pdf # Informe PDF en raíz para entrega directa
```

---

## Resultados Principales del Modelo

$$\widehat{\text{PE}} = 458.9396 - 1.9840 \cdot \text{AT} - 0.2307 \cdot \text{V} + 0.0579 \cdot \text{AP} - 0.1599 \cdot \text{RH}$$

| Métrica | Valor Obtenido | Interpretación |
| :---: | :---: | :--- |
| **$R^2$** | **0.9284 (92.84%)** | El modelo explica el 92.84% de la variabilidad en la generación eléctrica. |
| **RMSE** | **4.5110 MW** | Desvío típico cuadrático penalizando errores grandes. |
| **MAE** | **3.6124 MW** | Desvío promedio lineal sin distorsión de outliers. |
| **MAPE** | **0.795 %** | Margen de error porcentual inferior al 1.0% sobre la potencia media de la central. |
