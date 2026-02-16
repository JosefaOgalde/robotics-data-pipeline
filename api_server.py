"""
API REST para exposición de datos de robótica
Servicio backend para dashboards y aplicaciones
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Datos simulados (en producción vendrían de BD)
SAMPLE_DATA = {
    'robots': [
        {'id': 'ROBOT-001', 'status': 'active', 'battery': 85, 'location': [0, 0, 1.5]},
        {'id': 'ROBOT-002', 'status': 'active', 'battery': 72, 'location': [2, 1, 1.5]},
        {'id': 'ROBOT-003', 'status': 'maintenance', 'battery': 45, 'location': [0, 0, 0]}
    ],
    'inspections': [
        {'id': 'INS-001', 'robot_id': 'ROBOT-001', 'date': '2024-02-15', 'status': 'completed'},
        {'id': 'INS-002', 'robot_id': 'ROBOT-002', 'date': '2024-02-16', 'status': 'in_progress'}
    ]
}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud del servicio"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'robotics-data-api'
    })


@app.route('/api/robots', methods=['GET'])
def get_robots():
    """Obtiene lista de robots"""
    return jsonify({
        'robots': SAMPLE_DATA['robots'],
        'count': len(SAMPLE_DATA['robots'])
    })


@app.route('/api/robots/<robot_id>', methods=['GET'])
def get_robot(robot_id):
    """Obtiene información de un robot específico"""
    robot = next((r for r in SAMPLE_DATA['robots'] if r['id'] == robot_id), None)
    
    if robot:
        return jsonify(robot)
    else:
        return jsonify({'error': 'Robot no encontrado'}), 404


@app.route('/api/inspections', methods=['GET'])
def get_inspections():
    """Obtiene lista de inspecciones"""
    return jsonify({
        'inspections': SAMPLE_DATA['inspections'],
        'count': len(SAMPLE_DATA['inspections'])
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Obtiene métricas agregadas"""
    active_robots = len([r for r in SAMPLE_DATA['robots'] if r['status'] == 'active'])
    avg_battery = sum(r['battery'] for r in SAMPLE_DATA['robots']) / len(SAMPLE_DATA['robots'])
    
    return jsonify({
        'total_robots': len(SAMPLE_DATA['robots']),
        'active_robots': active_robots,
        'average_battery': round(avg_battery, 2),
        'total_inspections': len(SAMPLE_DATA['inspections'])
    })


@app.route('/api/data/upload', methods=['POST'])
def upload_data():
    """Endpoint para subir datos (simulado)"""
    data = request.get_json()
    
    logger.info(f"Datos recibidos: {len(data)} registros")
    
    # En producción, aquí se procesaría y guardaría en BD
    return jsonify({
        'status': 'success',
        'message': 'Datos recibidos correctamente',
        'records_received': len(data) if isinstance(data, list) else 1
    }), 201


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("API SERVER - ROBOTICS DATA")
    print("=" * 60)
    print("Endpoints disponibles:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/robots - Lista de robots")
    print("  GET  /api/robots/<id> - Info de robot")
    print("  GET  /api/inspections - Lista de inspecciones")
    print("  GET  /api/metrics - Métricas agregadas")
    print("  POST /api/data/upload - Subir datos")
    print("=" * 60)
    print("\nServidor iniciando en http://localhost:5000")
    print("Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
