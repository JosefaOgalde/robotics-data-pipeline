"""
Procesador de imágenes para robótica
Procesamiento de imágenes usando OpenCV para inspección de activos
"""

import cv2
import numpy as np
import os
from pathlib import Path
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Procesador de imágenes para análisis de inspección"""
    
    def __init__(self):
        self.results = {}
    
    def load_image(self, image_path):
        """Carga una imagen desde archivo"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagen no encontrada: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        
        logger.info(f"Imagen cargada: {image_path}, tamaño: {image.shape}")
        return image
    
    def detect_edges(self, image):
        """Detecta bordes usando Canny"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return edges
    
    def detect_contours(self, image):
        """Detecta contornos en la imagen"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def calculate_image_metrics(self, image):
        """Calcula métricas básicas de la imagen"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        metrics = {
            'width': image.shape[1],
            'height': image.shape[0],
            'channels': image.shape[2] if len(image.shape) == 3 else 1,
            'mean_intensity': float(np.mean(gray)),
            'std_intensity': float(np.std(gray)),
            'min_intensity': int(np.min(gray)),
            'max_intensity': int(np.max(gray))
        }
        
        return metrics
    
    def detect_defects(self, image, threshold=30):
        """
        Detecta posibles defectos usando análisis de textura
        Simula detección de anomalías en inspección de activos
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calcular gradiente para detectar cambios bruscos
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Detectar áreas con alto gradiente (posibles defectos)
        defect_mask = gradient_magnitude > threshold
        defect_count = np.sum(defect_mask)
        defect_percentage = (defect_count / gradient_magnitude.size) * 100
        
        return {
            'defect_count': int(defect_count),
            'defect_percentage': round(defect_percentage, 2),
            'has_defects': defect_percentage > 1.0
        }
    
    def process_image(self, image_path, output_dir='processed'):
        """
        Procesa una imagen completa y genera resultados
        """
        logger.info(f"Procesando imagen: {image_path}")
        
        # Cargar imagen
        image = self.load_image(image_path)
        
        # Calcular métricas
        metrics = self.calculate_image_metrics(image)
        
        # Detectar contornos
        contours = self.detect_contours(image)
        metrics['contour_count'] = len(contours)
        
        # Detectar posibles defectos
        defect_analysis = self.detect_defects(image)
        metrics.update(defect_analysis)
        
        # Detectar bordes
        edges = self.detect_edges(image)
        metrics['edge_pixels'] = int(np.sum(edges > 0))
        
        # Guardar imagen procesada
        os.makedirs(output_dir, exist_ok=True)
        filename = Path(image_path).stem
        output_path = os.path.join(output_dir, f"{filename}_processed.jpg")
        cv2.imwrite(output_path, edges)
        
        result = {
            'image_path': image_path,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'output_path': output_path
        }
        
        self.results[filename] = result
        logger.info(f"Procesamiento completado: {filename}")
        
        return result
    
    def export_results(self, output_path='image_analysis_results.json'):
        """Exporta resultados del procesamiento"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Resultados exportados a: {output_path}")
        return output_path


def generate_sample_image(output_path='sample_asset.jpg', width=800, height=600):
    """Genera una imagen de ejemplo para testing"""
    # Crear imagen sintética que simula una inspección
    image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    
    # Agregar algunas formas que simulen estructuras
    cv2.rectangle(image, (100, 100), (300, 300), (255, 255, 255), -1)
    cv2.circle(image, (500, 300), 100, (200, 200, 200), -1)
    
    # Agregar algunas líneas que simulen defectos
    cv2.line(image, (400, 200), (600, 400), (0, 0, 0), 3)
    cv2.line(image, (200, 400), (400, 500), (50, 50, 50), 2)
    
    cv2.imwrite(output_path, image)
    logger.info(f"Imagen de ejemplo generada: {output_path}")
    return output_path


def main():
    """Función principal para testing"""
    processor = ImageProcessor()
    
    # Generar imagen de ejemplo
    sample_image = generate_sample_image()
    
    # Procesar imagen
    result = processor.process_image(sample_image)
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DE PROCESAMIENTO DE IMAGEN")
    print("=" * 60)
    print(f"Imagen: {result['image_path']}")
    print(f"Dimensiones: {result['metrics']['width']}x{result['metrics']['height']}")
    print(f"Contornos detectados: {result['metrics']['contour_count']}")
    print(f"Defectos detectados: {result['metrics']['defect_count']} ({result['metrics']['defect_percentage']}%)")
    print(f"Tiene defectos: {result['metrics']['has_defects']}")
    print("=" * 60)
    
    # Exportar resultados
    processor.export_results()


if __name__ == "__main__":
    import os
    os.makedirs('processed', exist_ok=True)
    main()
