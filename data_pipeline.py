"""
Pipeline de datos para robótica
ETL para procesamiento de datos de robots y sensores
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RoboticsDataPipeline:
    """Pipeline ETL para datos de robótica"""
    
    def __init__(self):
        self.raw_data = None
        self.processed_data = None
        self.metadata = {}
    
    def extract_sensor_data(self, n_samples=1000):
        """
        Simula extracción de datos de sensores
        En producción vendría de robots, IMU, LiDAR, etc.
        """
        logger.info(f"Extrayendo datos de sensores ({n_samples} muestras)...")
        
        np.random.seed(42)
        base_time = datetime.now() - timedelta(hours=2)
        
        data = {
            'timestamp': [base_time + timedelta(seconds=i*2) for i in range(n_samples)],
            'robot_id': np.random.choice(['ROBOT-001', 'ROBOT-002', 'ROBOT-003'], n_samples),
            'position_x': np.random.normal(0, 1, n_samples),
            'position_y': np.random.normal(0, 1, n_samples),
            'position_z': np.random.normal(1.5, 0.3, n_samples),
            'orientation_roll': np.random.normal(0, 5, n_samples),
            'orientation_pitch': np.random.normal(0, 5, n_samples),
            'orientation_yaw': np.random.normal(0, 10, n_samples),
            'battery_level': np.random.uniform(20, 100, n_samples),
            'temperature': np.random.normal(25, 5, n_samples),
            'sensor_status': np.random.choice(['OK', 'WARNING', 'ERROR'], n_samples, p=[0.85, 0.12, 0.03])
        }
        
        df = pd.DataFrame(data)
        self.raw_data = df
        
        logger.info(f"Datos extraídos: {len(df)} registros")
        return df
    
    def validate_data(self, df):
        """Valida calidad de los datos"""
        logger.info("Validando datos...")
        
        errors = []
        
        # Validar rangos
        if 'battery_level' in df.columns:
            invalid_battery = ((df['battery_level'] < 0) | (df['battery_level'] > 100)).sum()
            if invalid_battery > 0:
                errors.append(f"Batería fuera de rango: {invalid_battery} registros")
        
        if 'temperature' in df.columns:
            extreme_temp = ((df['temperature'] < -10) | (df['temperature'] > 60)).sum()
            if extreme_temp > 0:
                errors.append(f"Temperatura extrema: {extreme_temp} registros")
        
        # Validar valores nulos críticos
        critical_cols = ['robot_id', 'timestamp']
        for col in critical_cols:
            if col in df.columns:
                nulls = df[col].isnull().sum()
                if nulls > 0:
                    errors.append(f"Valores nulos en {col}: {nulls}")
        
        if errors:
            logger.warning(f"Errores de validación: {len(errors)}")
            for error in errors:
                logger.warning(f"  - {error}")
        else:
            logger.info("Validación exitosa")
        
        return len(errors) == 0
    
    def transform_data(self, df):
        """Transforma y enriquece los datos"""
        logger.info("Transformando datos...")
        
        df = df.copy()
        
        # Calcular métricas derivadas
        if all(col in df.columns for col in ['position_x', 'position_y', 'position_z']):
            df['distance_from_origin'] = np.sqrt(
                df['position_x']**2 + 
                df['position_y']**2 + 
                df['position_z']**2
            )
        
        # Categorizar nivel de batería
        if 'battery_level' in df.columns:
            df['battery_status'] = pd.cut(
                df['battery_level'],
                bins=[0, 20, 50, 80, 100],
                labels=['Bajo', 'Medio', 'Alto', 'Optimo']
            )
        
        # Extraer información temporal
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['minute'] = df['timestamp'].dt.minute
        
        # Calcular estadísticas por robot
        if 'robot_id' in df.columns:
            robot_stats = df.groupby('robot_id').agg({
                'battery_level': 'mean',
                'temperature': 'mean',
                'distance_from_origin': 'mean'
            }).to_dict('index')
            self.metadata['robot_stats'] = robot_stats
        
        self.processed_data = df
        logger.info(f"Transformación completada: {len(df)} registros")
        
        return df
    
    def load_to_database(self, df, output_format='csv'):
        """Carga datos procesados (simula carga a BD)"""
        logger.info(f"Cargando datos en formato {output_format}...")
        
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        if output_format == 'csv':
            output_path = output_dir / 'processed_sensor_data.csv'
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        elif output_format == 'json':
            output_path = output_dir / 'processed_sensor_data.json'
            df.to_json(output_path, orient='records', indent=2, date_format='iso')
        else:
            raise ValueError(f"Formato no soportado: {output_format}")
        
        logger.info(f"Datos cargados en: {output_path}")
        return output_path
    
    def generate_report(self):
        """Genera reporte del pipeline"""
        if self.processed_data is None:
            return None
        
        df = self.processed_data
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'robots': df['robot_id'].unique().tolist() if 'robot_id' in df.columns else [],
            'date_range': {
                'start': df['timestamp'].min().isoformat() if 'timestamp' in df.columns else None,
                'end': df['timestamp'].max().isoformat() if 'timestamp' in df.columns else None
            },
            'statistics': {
                'avg_battery': float(df['battery_level'].mean()) if 'battery_level' in df.columns else None,
                'avg_temperature': float(df['temperature'].mean()) if 'temperature' in df.columns else None,
                'sensor_status_distribution': df['sensor_status'].value_counts().to_dict() if 'sensor_status' in df.columns else {}
            },
            'metadata': self.metadata
        }
        
        return report
    
    def run(self):
        """Ejecuta el pipeline completo"""
        logger.info("=" * 60)
        logger.info("INICIANDO PIPELINE DE DATOS DE ROBOTICA")
        logger.info("=" * 60)
        
        # Extract
        self.extract_sensor_data()
        
        # Validate
        is_valid = self.validate_data(self.raw_data)
        if not is_valid:
            logger.warning("Datos con problemas detectados, continuando...")
        
        # Transform
        self.transform_data(self.raw_data)
        
        # Load
        self.load_to_database(self.processed_data, 'csv')
        self.load_to_database(self.processed_data, 'json')
        
        # Report
        report = self.generate_report()
        
        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETADO")
        logger.info("=" * 60)
        
        return report


def main():
    """Función principal"""
    pipeline = RoboticsDataPipeline()
    report = pipeline.run()
    
    # Mostrar reporte
    print("\n" + "=" * 60)
    print("REPORTE DEL PIPELINE")
    print("=" * 60)
    print(f"Total de registros: {report['total_records']}")
    print(f"Robots procesados: {len(report['robots'])}")
    if report['statistics']['avg_battery']:
        print(f"Batería promedio: {report['statistics']['avg_battery']:.2f}%")
    if report['statistics']['avg_temperature']:
        print(f"Temperatura promedio: {report['statistics']['avg_temperature']:.2f}°C")
    print("=" * 60)


if __name__ == "__main__":
    import os
    os.makedirs('output', exist_ok=True)
    main()
