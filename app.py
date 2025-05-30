from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_html = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            
            # Parse PDB file
            x, y, z = [], [], []
            with open(filepath, 'r') as f:
                for line in f:
                    if line.startswith(('ATOM', 'HETATM')):
                        parts = line.split()
                        if len(parts) >= 8:
                            try:
                                x.append(float(parts[5]))
                                y.append(float(parts[6]))
                                z.append(float(parts[7]))
                            except ValueError:
                                continue
            
            # Plotly 3D scatter plot
            fig = go.Figure(data=[go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='markers',
                marker=dict(
                    size=4,
                    color='blue',
                    opacity=0.8
                )
            )])
            
            fig.update_layout(
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'
                ),
                title='Átomos en 3D'
            )
            
            graph_html = pio.to_html(fig, full_html=False)
    
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
