# 🏞️ Planeador de Excursiones

**Amanda Cordero Lezcano**  
**Christopher Guerra Herrero**  
**Alfredo Nuño Oquendo**  
Facultad de Matemática y Computación, Universidad de La Habana  
📅 Septiembre, 2024

---
## 📝 Abstract

Esta investigación presenta una simulación de un grupo de personas en una excursión, donde se recolectan características de los excursionistas mediante encuestas. Posteriormente, utilizando la metaheurística de Recocido Simulado, se planifica una ruta que maximice la satisfacción de los participantes. Finalmente, se simula la excursión con un modelo basado en agentes BDI y un controlador difuso para ajustar los tiempos de espera de los excursionistas en diferentes puntos del recorrido.
📚 Introducción
## Breve descripción del proyecto

El objetivo de esta investigación es simular una excursión con un grupo de excursionistas basándose en sus preferencias individuales, las características del terreno y las rutas disponibles. Para ello, se recolecta información de los excursionistas a través de encuestas. Se utiliza la metaheurística de Recocido Simulado y varias simulaciones para computar el costo de las rutas y seleccionar la mejor opción en cuanto a la satisfacción de los participantes.

## 🔢 Fundamento Matemático

Esta sección presenta los fundamentos matemáticos de las técnicas utilizadas para implementar la simulación: la metaheurística de Recocido Simulado, el modelo de agentes BDI y el controlador difuso.
### 🔍 Metaheurística de Recocido Simulado

El recocido simulado es una técnica de optimización inspirada en el proceso de recocido en metalurgia. Su objetivo es encontrar una solución aproximada a problemas complejos mediante la búsqueda aleatoria de soluciones vecinas. A diferencia de otros algoritmos, acepta no solo mejoras, sino también soluciones peores con cierta probabilidad, lo cual ayuda a evitar quedar atrapado en óptimos locales.

La temperatura, un parámetro clave, controla la aceptación de soluciones peores. Comienza alta para permitir una exploración amplia del espacio de soluciones y disminuye gradualmente, restringiendo la búsqueda para favorecer la convergencia hacia una solución óptima.

### 🤖 Modelo de Agentes BDI

El modelo BDI (Belief-Desire-Intention) se basa en la lógica modal para representar el comportamiento racional de los agentes. Los agentes tienen:

- **Creencias ($B$)**: Representan lo que el agente sabe o cree acerca del mundo.
- **Deseos ($D$)**: Los objetivos que el agente intenta alcanzar.
- **Intenciones ($I$)**: Los planes o acciones que el agente ha decidido ejecutar para lograr sus deseos.

Matemáticamente, el comportamiento de los agentes se puede describir usando una estructura modal $\langle B, D, I \rangle$, donde cada componente se actualiza según las reglas del sistema. La lógica BDI sigue el principio de que las intenciones deben ser consistentes con las creencias y deseos actuales.

### ⚙️ Controlador Difuso

En general, los controladores difusos son sistemas expertos especiales. Cada uno emplea una base de conocimientos, expresada en términos de reglas de inferencia difusa relevantes, y un motor de inferencia adecuado para resolver un problema de control determinado. Los controladores difusos varían sustancialmente según la naturaleza de los problemas de control que se supone deben resolver.

Un controlador difuso general consiste en cuatro módulos: una base de reglas difusas, un motor de inferencia difusa, y módulos de fuzzificación/defuzzificación.

---

## 💻 Detalles de Implementación

### Pasos seguidos para la implementación

Se desarrolló un sitio web en Django para interactuar con el guía de la excursión. En el mismo se encuentra una encuesta para los excursionistas, con la cual se obtendrán datos sobre sus preferencias. Posteriormente, el guía puede introducir en la plataforma el mapa de la región de interés. Usamos A* para planificar una ruta óptima en función de las preferencias y características del terreno. Luego se muestra en la web un anuncio elaborado por el modelo de lenguaje Mistralai, a partir de las características del camino seleccionado.

Para la simulación se modelan los excursionistas con agentes BDI. Aquí se diferencia el agente que representa al guía del resto de los excursionistas, debido a que entre los deseos del guía se encuentra también garantizar un recorrido seguro. Para los excursionistas se utiliza un controlador difuso; con las creencias de estos (características del mapa hasta el punto recorrido) y sus deseos (características recogidas en la encuesta) se aplican reglas como:

$$
 \mu_{\text{gusto\_historia\_bajo}} \implies \mu_{\text{tiempo\_espera\_corto}}
$$

Esta regla indica que si el gusto del usuario por la historia es bajo, entonces el tiempo de espera será corto.

$$
\mu_{\text{gusto\_historia\_medio}} \land \mu_{\text{indice\_historia\_bajo}} \implies \mu_{\text{tiempo\_espera\_corto}}
$$

Aquí se establece que si el gusto del usuario por la historia es medio y el índice de lugares históricos en el lugar es bajo, entonces el tiempo de espera será corto.

$$
\mu_{\text{gusto\_historia\_medio}}  \land (\mu_{\text{indice\_historia\_medio}} \lor \mu_{\text{indice\_historia\_alto}}) \implies \mu_{\text{tiempo\_espera\_medio}}
$$

Esta regla señala que si el gusto del usuario por la historia es medio y el índice de lugares históricos en el lugar es medio o alto, entonces el tiempo de espera será medio.

**📊 Descripción de Variables**

- $\mu_{\text{gusto\_historia\_bajo}}$: Función de pertenencia que describe un bajo gusto del usuario por la historia.
- $\mu_{\text{gusto\_historia\_medio}}$: Función de pertenencia que describe un gusto medio del usuario por la historia.
- $\mu_{\text{indice\_historia\_bajo}}$: Función de pertenencia que describe un índice bajo de sitios históricos en el lugar.
- $\mu_{\text{indice\_historia\_medio}}$: Función de pertenencia que describe un índice medio de sitios históricos en el lugar.
- $\mu_{\text{indice\_historia\_alto}}$: Función de pertenencia que describe un índice alto de sitios históricos en el lugar.
- $\mu_{\text{tiempo\_espera\_corto}}$: Función de pertenencia que describe un tiempo de espera corto para el usuario.
- $\mu_{\text{tiempo\_espera\_medio}}$: Función de pertenencia que describe un tiempo de espera medio para el usuario.

---

## 🧪 Resultados y Experimentos

El sistema desarrollado permite al guía planificar estratégicamente puntos de descanso, almuerzo y campamento basándose en las preferencias individuales de los excursionistas y las características del terreno.

Se realizaron diversas simulaciones con diferentes configuraciones de excursionistas, utilizando el algoritmo A* para calcular los puntos óptimos de descanso, almuerzo y campamento. Los resultados muestran que este enfoque optimiza el recorrido al seleccionar puntos estratégicos que maximicen la eficiencia de la excursión.

---

## 🔚 Conclusiones

Esta investigación ha demostrado que es posible planificar de manera efectiva una excursión utilizando un modelo de simulación basado en las preferencias individuales de los excursionistas y las características del terreno. El sistema ayuda al guía a identificar los puntos óptimos para descansos, almuerzos y campamentos, garantizando una experiencia más organizada y satisfactoria para el grupo.

Mediante la recolección de datos previos a la excursión y el uso del algoritmo A*, se maximizan el disfrute de los campistas. La simulación con agentes BDI y un controlador difuso asegura que la planificación de los puntos clave se adapte a las necesidades del grupo, manteniendo a los excursionistas cohesionados bajo la guía supervisada. Este enfoque ofrece un método eficiente para gestionar excursiones de manera óptima y personalizada.

---

## 📚 Referencias

1. Klir, G. J., & Yuan, B. (1995). *Fuzzy Sets and Fuzzy Logic: Theory and Applications*. Prentice Hall. Información extraída de las páginas 330-332.
