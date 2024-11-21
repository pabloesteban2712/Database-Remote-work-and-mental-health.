import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols


# Cargar el dataset
df = pd.read_csv('Impact_of_Remote_Work_on_Mental_Health.csv')

# Guardar cambios en el dataset
# df.to_csv('Impact_of_Remote_Work_on_Mental_Health.csv', index=False)

# -----------------------
# LIMPIEZA DE DATOS
# -----------------------

# Resumen estadístico del dataset
summary = df.describe()
print("Resumen estadístico del dataset:")
print(summary)

# Comprobación de valores nulos
print("\nConteo de valores nulos por columna:")
print(df.isnull().sum())

# NOTA:
# Algunos valores nulos en 'Physical_Activity' y 'Mental_Health_Condition' pueden no ser
# realmente valores "None". Por ejemplo:
#   - En 'Physical_Activity', no hay respuestas como ("No hago deporte), tan solo hay "Active"/"None", por lo que, dichas respuestas "None" pueden significar falta de actividad 
#   - En 'Mental_Health_Condition', solo hay respuestas de personas con problemas menatales, asi que las respuestas "None" pueden interpretarse como "Sin problemas".

# Imputación de valores faltantes y reemplazo de términos
df['Physical_Activity'] = df['Physical_Activity'].fillna('Inactive')
df['Mental_Health_Condition'] = df['Mental_Health_Condition'].fillna('No Issues')
df['Work_Location'] = df['Work_Location'].replace({'Onsite': 'Office'})

# Validación de cambios en las columnas modificadas
conteo_inactivos = df['Physical_Activity'].value_counts().get('Inactive', 0)
conteo_noissues = df['Mental_Health_Condition'].value_counts().get('No Issues', 0)
print(f"\nCantidad de empleados inactivos: {conteo_inactivos}, cantidad sin problemas mentales: {conteo_noissues}")

# -----------------------
# TRATAMIENTO DE VALORES INCOHERENTES (RELACION EDAD-EXPERIENCIA)
# -----------------------

# Definir la edad mínima para trabajar
edad_minima_trabajo = 15

# Filtrar filas con incoherencias en la relación edad-experiencia
incoherencias = df[df['Years_of_Experience'] > (df['Age'] - edad_minima_trabajo)]
print("\nFilas con incoherencias de edad-experiencia:")
print(incoherencias)

# Eliminar filas incoherentes
df.drop(incoherencias.index, inplace=True)

# Verificar el resultado tras la eliminación de incoherencias
print("\nDatos sin incoherencias de edad-experiencia:")
print(df[['Age', 'Years_of_Experience']])

# Mostrar el número de filas y columnas después de la limpieza
print(f"\nNúmero de filas: {len(df)}, Número de columnas: {len(df.columns)}")

# Guardar los cambios
df.to_csv('Impact_of_Remote_Work_on_Mental_Health.csv', index=False)

# -----------------------
# ELIMINACIÓN DE DUPLICADOS
# -----------------------

# Eliminar filas duplicadas basándose en un subconjunto de columnas clave
df = df.drop_duplicates(subset=[
    'Employee_ID', 'Age', 'Gender', 'Job_Role', 'Industry', 'Years_of_Experience', 
    'Work_Location', 'Hours_Worked_Per_Week', 'Number_of_Virtual_Meetings', 
    'Work_Life_Balance_Rating', 'Stress_Level', 'Mental_Health_Condition', 
    'Access_to_Mental_Health_Resources', 'Productivity_Change', 
    'Social_Isolation_Rating', 'Satisfaction_with_Remote_Work', 
    'Company_Support_for_Remote_Work', 'Physical_Activity', 'Sleep_Quality', 'Region'
])

# Confirmación final de filas y columnas después de la eliminación de duplicados (No ha habido eliminacion de duplicados.)
print(f"\nNúmero de filas tras eliminar duplicados: {len(df)}, Número de columnas: {len(df.columns)}")

# -----------------------
# ANÁLISIS DE OUTLIERS Y PREGUNTAS A RESPONDER
# (Voy a revisar los outliers de "Age" y "Years_of_Experience", que las considero las 2 variables mas importantes, respecto a mis preguntas.) 
# -----------------------

# 1.EDAD
columna_edad = 'Age'

# Calculo del primer y tercer cuartil (Q1 y Q3)
Q1 = df[columna_edad].quantile(0.25)
Q3 = df[columna_edad].quantile(0.75)
IQR = Q3 - Q1

# Límites
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Filtra los outliers
outliers = df[(df[columna_edad] < limite_inferior) | (df[columna_edad] > limite_superior)]
print("Outliers en la columna", columna_edad)
print(outliers)

# 2.EXPERIENCIA 
columna_experiencia = 'Years_of_Experience'

# Calculo del primer y tercer cuartil (Q1 y Q3)
Q1 = df[columna_experiencia].quantile(0.25)
Q3 = df[columna_experiencia].quantile(0.75)
IQR = Q3 - Q1

# Límites
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Filtra los outliers
outliers = df[(df[columna_experiencia] < limite_inferior) | (df[columna_experiencia] > limite_superior)]
print("Outliers en la columna", columna_experiencia)
print(outliers)

# PODEMOS OBSERVAR COMO EN NINGUNO DE LAS 2 COLUMNAS HAY OUTLIERS. 

# POR TANTO, TRAS EL PREPROCESAMIENTO, VAMOS A PASAR A RESPONDER LAS PREGUNTAS QUE HEMOS PLANTEADO.

# PREGUNTAS A RESPONDER:
# 1 - ¿Existe correlación entre la forma de realizar el trabajo (remoto/presencial) y la aparicion de enfermedades mentales? (Work_Location - Mental_Health_Condition)

work_location_mental_health = df.groupby(['Work_Location', 'Mental_Health_Condition']).size().unstack()

# Dibujamos el gráfico de barras.
work_location_mental_health.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Salud Mental y Localización del Trabajo')
plt.xlabel('Localización del Trabajo')
plt.ylabel('Número de Empleados')
plt.xticks(rotation=45)
plt.legend(title='Condiciones de Salud Mental')

# Se ajusta el diseño para evitar solapamientos
plt.tight_layout()
plt.show()

# Como podemos observar en el grafico, vemos una distribucion uniforme y no hay diferencias significativas entre las formas de trabajo (Presencial - Hibrido - Remoto)
# y las condiciones de salud mental (Depresion - Ansiedad - Agotamiento - Ningun problema) en los trabajadores. 
# Para confirmar si realmente no existe una relación significativa, vamos a complementar el análisis con el Test de Chi-cuadrado.

#Tabla de contingencia
table = pd.crosstab (df['Work_Location'], df ['Mental_Health_Condition'])

#Prueba de Chi - Cuadrado
chi2, p, dof, expected = chi2_contingency(table)

# Resultados
print("Chi-cuadrado:", chi2) #Un valor más alto sugiere una mayor diferencia entre las frecuencias observadas y las esperadas.
print("Valor p:", p)
print("Grados de libertad:", dof)
print("Frecuencias esperadas:\n", expected)

# Interpretacion
if p > 0.05:
    print("No hay evidencia suficiente para afirmar que existe una relación significativa entre la loacalizacion del trabajo y las condiciones de salud mental.")
else:
    print("Existe una relación significativa entre la loacalizacion del trabajo y las condiciones de salud mental.")

# El valor es 0.0519
# Como el valor p es mayor que 0.05, no podemos rechazar la hipótesis nula. 
# Esto sugiere que no hay evidencia suficiente para afirmar que las variables están relacionadas. Es decir, las variables son independientes en el contexto de tu prueba.

# 2 - ¿Existe correlación entre el género y la satisfacción con el trabajo remoto? (Gender - Satisfaction_with_Remote_Work)

gender_remote_satisfaction = pd.crosstab(df['Gender'], df['Satisfaction_with_Remote_Work'])

# Dibujamos el grafcio de barras.
gender_remote_satisfaction.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.title('Género y Satisfacción con el Trabajo Remoto')
plt.xlabel('Género')
plt.ylabel('Número de Empleados')
plt.xticks(rotation=0)
plt.legend(title='Satisfacción con Trabajo Remoto')
plt.tight_layout()
plt.show()

# Prueba de Chi - Cuadrado
chi2, p, dof, expected = chi2_contingency(gender_remote_satisfaction)

# Resultados
print("Chi-cuadrado:", chi2) #Un valor más alto sugiere una mayor diferencia entre las frecuencias observadas y las esperadas.
print("Valor p:", p)
print("Grados de libertad:", dof)
print("Frecuencias esperadas:\n", expected)

# Interpretación
if p > 0.05:
    print("No hay evidencia suficiente para afirmar que existe una relación significativa entre el género y la satisfacción con el trabajo remoto.")
else:
    print("Existe una relación significativa entre el género y la satisfacción con el trabajo remoto.")

# El valor es 0.26
# Como el valor p es mayor que 0.05, no podemos rechazar la hipótesis nula. 
# Esto sugiere que no hay evidencia suficiente para afirmar que las variables están relacionadas. Es decir, las variables son independientes en el contexto de tu prueba

# 3 - ¿Existe correlación entre la edad y la satisfacción con el trabajo remoto? (Age - Satisfaction_with_Remote_Work)

# Visualización: Distribución de la edad según la satisfacción con el trabajo remoto
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Satisfaction_with_Remote_Work', y='Age', palette='viridis')
plt.title('Distribución de la Edad según la Satisfacción con el Trabajo Remoto')
plt.xlabel('Satisfacción con el Trabajo Remoto')
plt.ylabel('Edad')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ANOVA: Comparar la edad entre los niveles de satisfacción con el trabajo remoto
# Crear el modelo lineal
model = ols('Age ~ C(Satisfaction_with_Remote_Work)', data=df).fit()

# Generar la tabla ANOVA
anova_table = sm.stats.anova_lm(model, typ=2)

# Mostrar la tabla ANOVA
print("Resultados ANOVA:")
print(anova_table)

# Interpretación del resultado
print("\nInterpretación:")
if anova_table["PR(>F)"][0] > 0.05:
    print("No hay evidencia suficiente para afirmar que las edades difieren significativamente entre los niveles de satisfacción con el trabajo remoto.")
else:
    print("Hay evidencia suficiente para concluir que las edades difieren significativamente entre los niveles de satisfacción con el trabajo remoto.")

# El valor p obtenido en la prueba ANOVA es 0.4196, lo cual es mayor que 0.05.
# Esto indica que no hay evidencia estadísticamente significativa para afirmar que la edad varía según los niveles de satisfacción con el trabajo remoto.
# El boxplot muestra que las distribuciones de edad son bastante similares entre los grupos.
# Es decir, como conclusion final: No existe una relación significativa entre la edad y la satisfacción con el trabajo remoto.