# 🤖 API de un Asistente Virtual de tipo Chatbot para el Sistema de Gestión de una Biblioteca Universitaria

Este proyecto consiste en el desarrollo de una **API para un asistente virtual tipo chatbot**, diseñado específicamente para el **Sistema de Gestión Bibliotecaria** de una **Biblioteca Universitaria**. El asistente está integrado por un agente inteligente capaz de responder preguntas relacionadas con información bibliográfica y servicios de la biblioteca, utilizando procesamiento de lenguaje natural (NLP) y modelos de lenguaje avanzados.

## 📚 Descripción

La **Inteligencia Artificial (IA)**, rama de la informática dedicada a automatizar comportamientos inteligentes, ha transformado profundamente la forma en que las instituciones procesan y acceden a la información. Entre sus áreas más destacadas se encuentra el **Procesamiento de Lenguaje Natural (NLP)**, que permite a las máquinas comprender y generar texto en lenguaje humano de manera coherente.

Los **Modelos de Lenguaje de Gran Escala (LLM)** son protagonistas clave en esta revolución, proporcionando capacidades avanzadas para interpretar y responder preguntas complejas. En este contexto, la técnica **Retrieval-Augmented Generation (RAG)** combina modelos LLM con bases de conocimiento para generar respuestas precisas y relevantes en un dominio específico.

A esto se suman los **agentes inteligentes**, componentes de software autónomos capaces de percibir su entorno, razonar y actuar para cumplir objetivos definidos. Esta combinación ha dado lugar a asistentes virtuales tipo chatbot, capaces de interactuar con los usuarios de manera natural, respondiendo consultas y brindando asistencia automatizada.

## 🛠️ Tecnologías utilizadas

El proyecto se apoya en tecnologías modernas de IA, backend y bases de datos:

- FastAPI – Framework para construir APIs web de alto rendimiento.

- LangChain – Marco para construir aplicaciones LLM con componentes reutilizables como agentes y cadenas.

- Ollama – Plataforma para ejecutar modelos de lenguaje localmente.

- Llama 3.1 8B – LLM utilizado a través de Ollama.

- nomic-embed-text – Modelo de generación de embeddings.

- Chroma DB – Base de datos vectorial para búsquedas semánticas.

- PostgreSQL – Sistema de gestión de bases de datos relacional (Para almacenar chats y retroalimentación de obtención de tesis).

## 🚀 Cómo ejecutar el proyecto

1. Clona este repositorio

2. Accede al directorio del código fuente:

   ```bash
   cd src
   ```

3. Ejecuta el servidor FastAPI:

   ```bash
   fastapi dev main.py
   ```

> Asegúrate de tener configurados y corriendo los servicios necesarios (como Ollama con el modelo LLaMA 3.1 8B y nomic-embed-text, así como Chroma DB) antes de iniciar la API.
