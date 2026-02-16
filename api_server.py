"""
API REST para exposición de datos de robótica
Servicio backend para dashboards y aplicaciones
"""

from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Template HTML para dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Robotics Data Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #4CAF50;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric-card {
            background-color: #2a2a2a;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
        }
        .metric-label {
            color: #aaa;
            margin-top: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: #2a2a2a;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #444;
        }
        th {
            background-color: #333;
            color: #4CAF50;
        }
        .status-active {
            color: #4CAF50;
            font-weight: bold;
        }
        .status-maintenance {
            color: #ff9800;
            font-weight: bold;
        }
        .battery-bar {
            background-color: #333;
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }
        .battery-fill {
            height: 100%;
            background-color: #4CAF50;
            transition: width 0.3s;
        }
        .battery-low {
            background-color: #ff9800;
        }
        .battery-critical {
            background-color: #f44336;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Robotics Data Dashboard</h1>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{{ metrics.total_robots }}</div>
                <div class="metric-label">Total Robots</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.active_robots }}</div>
                <div class="metric-label">Robots Activos</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.average_battery }}%</div>
                <div class="metric-label">Batería Promedio</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ metrics.total_inspections }}</div>
                <div class="metric-label">Inspecciones</div>
            </div>
        </div>
        
        <h2>Estado de Robots</h2>
        <table>
            <thead>
                <tr>
                    <th>ID Robot</th>
                    <th>Estado</th>
                    <th>Batería</th>
                    <th>Ubicación (X, Y, Z)</th>
                </tr>
            </thead>
            <tbody>
                {% for robot in robots %}
                <tr>
                    <td>{{ robot.id }}</td>
                    <td>
                        <span class="status-{{ robot.status }}">
                            {{ robot.status|upper }}
                        </span>
                    </td>
                    <td>
                        {{ robot.battery }}%
                        <div class="battery-bar">
                            <div class="battery-fill {% if robot.battery < 30 %}battery-critical{% elif robot.battery < 50 %}battery-low{% endif %}" 
                                 style="width: {{ robot.battery }}%"></div>
                        </div>
                    </td>
                    <td>[{{ robot.location[0] }}, {{ robot.location[1] }}, {{ robot.location[2] }}]</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <h2>Inspecciones Recientes</h2>
        <table>
            <thead>
                <tr>
                    <th>ID Inspección</th>
                    <th>Robot</th>
                    <th>Fecha</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
                {% for inspection in inspections %}
                <tr>
                    <td>{{ inspection.id }}</td>
                    <td>{{ inspection.robot_id }}</td>
                    <td>{{ inspection.date }}</td>
                    <td>{{ inspection.status|upper }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
        <p style="color: #888; margin-top: 30px; text-align: center;">
            Última actualización: {{ timestamp }}
        </p>
    </div>
</body>
</html>
"""


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


@app.route('/', methods=['GET'])
def dashboard():
    """Dashboard principal en HTML"""
    # Calcular métricas
    active_robots = len([r for r in SAMPLE_DATA['robots'] if r['status'] == 'active'])
    avg_battery = sum(r['battery'] for r in SAMPLE_DATA['robots']) / len(SAMPLE_DATA['robots'])
    
    metrics = {
        'total_robots': len(SAMPLE_DATA['robots']),
        'active_robots': active_robots,
        'average_battery': round(avg_battery, 2),
        'total_inspections': len(SAMPLE_DATA['inspections'])
    }
    
    return render_template_string(
        DASHBOARD_HTML,
        metrics=metrics,
        robots=SAMPLE_DATA['robots'],
        inspections=SAMPLE_DATA['inspections'],
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("API SERVER - ROBOTICS DATA")
    print("=" * 60)
    print("Endpoints disponibles:")
    print("  GET  / - Dashboard HTML")
    print("  GET  /api/health - Health check (JSON)")
    print("  GET  /api/robots - Lista de robots (JSON)")
    print("  GET  /api/robots/<id> - Info de robot (JSON)")
    print("  GET  /api/inspections - Lista de inspecciones (JSON)")
    print("  GET  /api/metrics - Métricas agregadas (JSON)")
    print("  POST /api/data/upload - Subir datos")
    print("=" * 60)
    print("\nServidor iniciando en http://localhost:5000")
    print("Presiona Ctrl+C para detener\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
