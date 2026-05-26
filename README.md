# 🏥 Plataforma Clínica Distribuida e Interoperable (FHIR)
Proyecto académico de Sistemas Distribuidos para la Corporación Universitaria Antonio José de Sucre (Corposucre) - Año 2026.

## 📋 Integrantes
* Cesar Camilo Furnieles Padilla
* Marlon Méndez

---

## 🛠️ Evidencias del Despliegue de Infraestructura (Docker)

### Paso 1: Inicialización del Clúster Distribuido
Se evidencia la descarga, construcción y ejecución de las imágenes de los servidores HAPI FHIR replicados y las bases de datos mediante contenedores aislados en la terminal de Kali Linux.
![Despliegue inicial de contenedores](captura%20paso%201.PNG)

### Paso 2: Creación de Redes y Volúmenes Persistentes
Demostración de la asignación automática de la red interna aislada (`node1_fhir-net`) y los volúmenes nombrados para garantizar que los expedientes clínicos persistan ante reinicios del sistema.
![Redes y volúmenes creados](Captura%20paso%202.PNG)

---

## 🕹️ Guía de Pruebas y Flujo de Interoperabilidad Clínica

### Flujo 1: Autenticación de Seguridad JWT
El sistema bloquea el acceso a los recursos distribuidos hasta que se genera un token firmado válido. Al ingresar las credenciales del sistema (`admin`), el middleware responde con éxito.
![Token JWT Generado con Éxito](uno.PNG)

### Flujo 2: Admisión Transaccional del Paciente (Resource Patient)
Registro del expediente maestro del paciente ingresando ID único y enlazándolo directamente de forma geográfica al Nodo Sincelejo en el puerto 8083.
![Registro del recurso Patient](dos.PNG)

### Flujo 3: Triage Reactivo y Signos Vitales (Resource Observation)
Evaluación en tiempo real aplicando la Escala Manchester. Al digitar una Frecuencia Cardíaca crítica de 130 bpm, la interfaz reacciona pintándose instantáneamente de color Rojo Crítico.
![Inserción de Observation y Triage](tres.PNG)

### Flujo 4: Consulta Médica e Historia Clínica Cruzada (Resource Condition)
Asociación del diagnóstico de *Crisis Hipertensiva* e inyección del recurso al clúster clínico. El módulo derecho unifica de forma asíncrona la información dispersa en los nodos.
![Persistencia final e Historia Cruzada](cuatro.PNG)
