# Análisis del Impacto del Trabajo Remoto en la Salud Mental
Este proyecto examina el impacto del trabajo remoto en la salud mental de los empleados mediante el análisis de un conjunto de datos.
Se utilizan técnicas de preprocesamiento, análisis estadístico y visualización de datos para investigar las relaciones entre variables como la localización del trabajo, las condiciones de salud mental, la edad y la satisfacción laboral.

Contenido del Análisis
1. Limpieza de Datos
Identificación y manejo de valores nulos.
Imputación de datos faltantes en columnas clave como Physical Activity y Mental Health Condition.
Revisión y corrección de incoherencias en la relación edad-experiencia laboral.
Eliminación de duplicados en el conjunto de datos.
2. Análisis de Outliers
Detección de valores atípicos en las variables Age y Years of Experience utilizando el rango intercuartílico (IQR).
Validación de la ausencia de outliers significativos tras el análisis.
3. Preguntas de Investigación
¿Existe una relación entre la localización del trabajo y las condiciones de salud mental?

Análisis mediante la prueba de Chi-cuadrado.
Resultado: No se encontró evidencia estadística de una relación significativa (valor p: 0.0519).
¿Existe correlación entre el género y la satisfacción con el trabajo remoto?

Análisis mediante la prueba de Chi-cuadrado.
Resultado: No se observaron relaciones significativas; las variables son independientes (valor p: 0.26).
¿Existe una relación entre la edad y la satisfacción con el trabajo remoto?

Análisis mediante ANOVA para determinar diferencias entre grupos.
Resultado: La edad no tiene un impacto significativo en los niveles de satisfacción (valor p: 0.4196).
4. Visualizaciones
Relación entre localización del trabajo y condiciones de salud mental: Un gráfico de barras apiladas que muestra la distribución de empleados según la localización laboral y su estado de salud mental.
Relación entre género y satisfacción laboral: Un gráfico de barras apiladas que detalla cómo varía la satisfacción según el género.
Distribución de edades por niveles de satisfacción: Un boxplot que ilustra las diferencias en la edad según los niveles de satisfacción con el trabajo remoto.
5. Métodos Estadísticos Utilizados
Prueba de Chi-cuadrado: Para evaluar la independencia entre variables categóricas como Work Location y Mental Health Condition.
ANOVA: Para comparar las distribuciones de edad entre diferentes niveles de satisfacción laboral.
Resultados Principales
Localización del trabajo vs. Salud mental: No se encontró relación significativa (valor p: 0.0519).
Género vs. Satisfacción laboral: Las variables son independientes (valor p: 0.26).
Edad vs. Satisfacción laboral: No se encontraron diferencias significativas (valor p: 0.4196).
