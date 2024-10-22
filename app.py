# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dfmea.db'
db = SQLAlchemy(app)

class DFMEA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(500), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    occurrence = db.Column(db.Integer, nullable=False)
    detection = db.Column(db.Integer, nullable=False)
    rpn = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_dfmea', methods=['POST'])
def add_dfmea():
    data = request.json
    new_dfmea = DFMEA(
        problem=data['problem'],
        severity=data['severity'],
        occurrence=data['occurrence'],
        detection=data['detection'],
        rpn=data['rpn']
    )
    db.session.add(new_dfmea)
    db.session.commit()
    return jsonify({'message': 'DFMEA item added successfully'}), 201

@app.route('/update_dfmea/<int:id>', methods=['PUT'])
def update_dfmea(id):
    dfmea = DFMEA.query.get_or_404(id)
    data = request.json
    dfmea.problem = data['problem']
    dfmea.severity = data['severity']
    dfmea.occurrence = data['occurrence']
    dfmea.detection = data['detection']
    dfmea.rpn = data['rpn']
    db.session.commit()
    return jsonify({'message': 'DFMEA item updated successfully'}), 200

@app.route('/delete_dfmea/<int:id>', methods=['DELETE'])
def delete_dfmea(id):
    dfmea = DFMEA.query.get_or_404(id)
    db.session.delete(dfmea)
    db.session.commit()
    return jsonify({'message': 'DFMEA item deleted successfully'}), 200

@app.route('/get_dfmea')
def get_dfmea():
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')

    if sort_by not in ['id', 'problem', 'severity', 'occurrence', 'detection', 'rpn', 'created_at']:
        sort_by = 'id'
    
    if order not in ['asc', 'desc']:
        order = 'asc'

    query = DFMEA.query.order_by(getattr(getattr(DFMEA, sort_by), order)())
    dfmea_items = query.all()

    return jsonify([{
        'id': item.id,
        'problem': item.problem,
        'severity': item.severity,
        'occurrence': item.occurrence,
        'detection': item.detection,
        'rpn': item.rpn,
        'created_at': item.created_at.isoformat()
    } for item in dfmea_items])

@app.route('/get_dfmea/<int:id>')
def get_single_dfmea(id):
    dfmea = DFMEA.query.get_or_404(id)
    return jsonify({
        'id': dfmea.id,
        'problem': dfmea.problem,
        'severity': dfmea.severity,
        'occurrence': dfmea.occurrence,
        'detection': dfmea.detection,
        'rpn': dfmea.rpn,
        'created_at': dfmea.created_at.isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=1234)
