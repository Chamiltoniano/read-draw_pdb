from flask import Flask, render_template, request
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

            # Listas para guardar datos
            x, y, z, colors, sizes = [], [], [], [], []

            # Mapeo de colores y números atómicos
            color_map = {
                'H': 'white',
                'C': 'gray',
                'N': 'blue',
                'O': 'red',
                'S': 'orange'
            }
            atomic_numbers = {
                'H': 1,
                'C': 6,
                'N': 7,
                'O': 8,
                'S': 16
            }

            with open(filepath, 'r') as f:
                for line in f:
                    if line.startswith(('ATOM', 'HETATM')):
                        parts = line.split()
                        if len(parts) >= 8:
                            try:
                                symbol = parts[2][0]  # Primer carácter del nombre atómico
                                x_coord = float(parts[5])
                                y_coord = float(parts[6])
                                z_coord = float(parts[7])

                                # Asigna color y tamaño
                                color = color_map.get(symbol, 'violet')
                                size = atomic_numbers.get(symbol, 20)  # 20 como default para otros

                                x.append(x_coord)
                                y.append(y_coord)
                                z.append(z_coord)
                                colors.append(color)
                                sizes.append(size)
                            except ValueError:
                                continue

            fig = go.Figure(data=[go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='markers',
                marker=dict(
                    size=sizes,
                    color=colors,
                    opacity=0.8
                )
            )])

            fig.update_layout(
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    bgcolor='black'
                ),
                paper_bgcolor='black',
                plot_bgcolor='black',
                title=dict(text='Átomos en 3D', font=dict(color='white')),
                font=dict(color='white')
            )

            graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
