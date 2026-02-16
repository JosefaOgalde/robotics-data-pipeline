# Robotics Data Pipeline - Software y Robótica

Pipeline completo de procesamiento de datos para robótica e inspección de activos. Incluye procesamiento de imágenes, análisis de nubes de puntos 3D, ETL de datos de sensores y API REST para exposición de datos.

## Descripción

Este proyecto implementa un sistema completo para procesamiento de datos de robótica que incluye:
- Procesamiento de imágenes con OpenCV para inspección
- Análisis de nubes de puntos 3D (LiDAR)
- Pipeline ETL para datos de sensores y robots
- API REST para exposición de datos
- Visualizaciones y dashboards

Desarrollado para demostrar competencias en software de robótica, procesamiento de datos y desarrollo de plataformas.

## Tecnologías

- Python 3.8+
- OpenCV - procesamiento de imágenes
- NumPy, Pandas - análisis de datos
- Scikit-learn - segmentación y clustering
- Flask - API REST
- Matplotlib - visualizaciones

## Estructura del Proyecto

```
robotics-data-pipeline/
│
├── image_processor.py        # Procesamiento de imágenes (OpenCV)
├── pointcloud_processor.py   # Análisis de nubes de puntos 3D
├── data_pipeline.py          # Pipeline ETL de datos de sensores
├── api_server.py             # API REST para exposición de datos
├── requirements.txt          # Dependencias
└── README.md                # Documentación
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/JosefaOgalde/robotics-data-pipeline.git
cd robotics-data-pipeline

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Procesamiento de Imágenes

```bash
python image_processor.py
```

Procesa imágenes para inspección de activos, detecta defectos y genera métricas.

### Análisis de Nubes de Puntos

```bash
python pointcloud_processor.py
```

Analiza nubes de puntos 3D, filtra, segmenta y calcula métricas espaciales.

### Pipeline de Datos

```bash
python data_pipeline.py
```

Ejecuta pipeline ETL completo para datos de sensores y robots.

### API REST

```bash
python api_server.py
```

Inicia servidor API en http://localhost:5000

Endpoints disponibles:
- `GET /api/health` - Health check
- `GET /api/robots` - Lista de robots
- `GET /api/robots/<id>` - Info de robot específico
- `GET /api/inspections` - Lista de inspecciones
- `GET /api/metrics` - Métricas agregadas
- `POST /api/data/upload` - Subir datos

## Funcionalidades

**Procesamiento de Imágenes**
- Detección de bordes y contornos
- Análisis de defectos
- Cálculo de métricas de imagen
- Exportación de resultados

**Nubes de Puntos 3D**
- Generación y procesamiento de datos LiDAR
- Filtrado espacial
- Segmentación en clusters
- Cálculo de métricas 3D

**Pipeline ETL**
- Extracción de datos de sensores
- Validación de calidad
- Transformación y enriquecimiento
- Carga en múltiples formatos

**API REST**
- Endpoints para consulta de datos
- Métricas en tiempo real
- Integración con dashboards

## Ejemplo de Uso

```python
from image_processor import ImageProcessor
from pointcloud_processor import PointCloudProcessor
from data_pipeline import RoboticsDataPipeline

# Procesar imagen
processor = ImageProcessor()
result = processor.process_image('sample_asset.jpg')

# Procesar nube de puntos
pc_processor = PointCloudProcessor()
pointcloud = pc_processor.generate_sample_pointcloud()
analysis = pc_processor.process_pointcloud(pointcloud)

# Ejecutar pipeline
pipeline = RoboticsDataPipeline()
report = pipeline.run()
```

## Autor

Josefa Ogalde - Ingeniera en Informática

---

*Proyecto desarrollado para demostrar competencias en software de robótica, procesamiento de datos y desarrollo de plataformas.*
