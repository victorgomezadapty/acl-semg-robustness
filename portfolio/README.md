# Signal & Method — portfolio estático

Página de presentación del análisis, no herramienta de diagnóstico. Los gráficos interactivos usan resultados derivados guardados; no calculan función muscular del visitante ni realizan inferencia clínica.

Desde la raíz del repositorio:

```powershell
python scripts/build_portfolio.py
python -m http.server 8765 --directory portfolio/dist
```

Abrir `http://127.0.0.1:8765`. También puede abrirse `dist/index.html` directamente: los datos se cargan con `data.js`, sin petición a un servidor. Las fuentes web son opcionales y tienen alternativas locales. No hay analítica, cuentas, datos personales ni backend.

`build_portfolio.py` verifica hashes de resultados ENABL3S y protocolo congelado, exporta las seis personas elegibles y regenera un gráfico original con Matplotlib. Las demás figuras proceden del análisis existente. Para modificar la ciencia se necesita el protocolo/pipeline, no editar manualmente las cifras de la página.

`dist/` contiene los archivos desplegables; `.openai/hosting.json` conserva la identidad del sitio Sites. La publicación inicial de Sites es privada. Compartir con público general requiere configurar su audiencia. Las licencias por componente aparecen en el pie y en `dist/assets/DATA_SOURCES.md`.
