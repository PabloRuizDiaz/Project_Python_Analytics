'''
Proyecto Final de Modulo Python Developer
-----------------------------------------------------
Se realiza un website con informacion extraida de un json, pasado a una base de datos
SQL. Donde al mismo a traves de diversas consultas se realizan calculos, que finalizan
en diversos graficos utilizando Matplotlib.
'''

__author__ = "Pablo Martin Ruiz Diaz"
__email__ = "rd.pablo@gmail.com"
__version__ = "1.1"


##################### Librerias #####################
# Librerias propias
import data_base
import graphs
# Librerias para flask
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, SelectField, TextField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
# Librerias para Bootstrap
from flask_bootstrap import Bootstrap
# Librerias para graficos
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from itertools import accumulate
import io


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'mysecretkey'


##################### Formularios #####################
class InfoForm1(FlaskForm):
    country = SelectField('Selecciona el Pais:',
                            validators=[DataRequired()])
    submit = SubmitField('Cargar')


##################### Main Script #####################
@app.route('/',methods=['GET','POST'])
def index():
    form = InfoForm1()

    all_countries = data_base.list_all_countries()
    form.country.choices = [(i,j) for i,j in all_countries]

    if form.is_submitted():
        country = form.country.data
        
        return redirect(url_for('line_graph_per_country',country=country))
    
    return render_template('index.html',form=form)


@app.route('/create_table')
def create_table():
    data_base.create_table_SQL()
    return redirect(url_for('index'))


@app.route('/actualise_table')
def actualise_table():
    data_base.actualise_table_SQL()
    return redirect(url_for('index'))


@app.route('/bar_graph_continent')
def bar_graph_continent():
    row = graphs.bar_graph_continent()

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.bar(row[0][1], row[0][0], label=f'{row[0][1]}')
    ax.bar(row[1][1], row[1][0], label=f'{row[1][1]}')
    ax.bar(row[2][1], row[2][0], label=f'{row[2][1]}')
    ax.bar(row[3][1], row[3][0], label=f'{row[3][1]}')
    ax.bar(row[4][1], row[4][0], label=f'{row[4][1]}')
    
    ax.set_facecolor('whitesmoke')
    ax.legend()

    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)

    return Response(img.getvalue(), mimetype='image/png')


@app.route('/bar_graph_continent_death')
def bar_graph_continent_death():
    row = graphs.bar_graph_continent_death()

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.bar(row[0][1], row[0][0], label=f'{row[0][1]}')
    ax.bar(row[1][1], row[1][0], label=f'{row[1][1]}')
    ax.bar(row[2][1], row[2][0], label=f'{row[2][1]}')
    ax.bar(row[3][1], row[3][0], label=f'{row[3][1]}')
    ax.bar(row[4][1], row[4][0], label=f'{row[4][1]}')
    
    ax.set_facecolor('whitesmoke')
    ax.legend()

    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)

    return Response(img.getvalue(), mimetype='image/png')
    

@app.route('/ranking_table_graph')
def ranking_table_graph():
    row = graphs.ranking_table_graph()
    
    val1 = ['Countries and Territories', 'Cases per week', 'Average (%)'] 
    val2 = [[i[n] for n in range(3)] for i in row]
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_axis_off()

    ax.table(cellText = val2, colLabels = val1, colColours =["palegreen"] * 10, cellLoc ='center', loc ='center')
    ax.set_title('Tabla Top 10: Contagios por Pais') 
    
    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)
    
    return Response(img.getvalue(), mimetype='image/png')


@app.route('/ranking_table_graph_death')
def ranking_table_graph_death():
    row = graphs.ranking_table_graph_death()
    
    val1 = ['Countries and Territories', 'Deaths per week', 'Average (%)'] 
    val2 = [[i[n] for n in range(3)] for i in row]
    
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_axis_off()

    ax.table(cellText = val2, colLabels = val1, colColours =["palegreen"] * 10, cellLoc ='center', loc ='center')
    ax.set_title('Tabla Top 10: Contagios por Pais') 
    
    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)
    
    return Response(img.getvalue(), mimetype='image/png')


@app.route('/line_graph')
def line_graph():
    row = graphs.line_graph()

    africa_acc = list(accumulate([i[1] for i in row if i[2] == 'Africa']))
    america_acc = list(accumulate([i[1] for i in row if i[2] == 'America']))
    asia_acc = list(accumulate([i[1] for i in row if i[2] == 'Asia']))
    europe_acc = list(accumulate([i[1] for i in row if i[2] == 'Europe']))
    oceania_acc = list(accumulate([i[1] for i in row if i[2] == 'Oceania']))

    week_year = [i[0] for i in row if i[2] == 'Africa']

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.plot(week_year, africa_acc, color='b', label='Africa')
    ax.plot(week_year, america_acc, color='c', label='America')
    ax.plot(week_year, asia_acc, color='g', label='Asia')
    ax.plot(week_year, europe_acc, color='k', label='Europe')
    ax.plot(week_year, oceania_acc, color='r', label='Oceania')
    ax.set_facecolor('whitesmoke')
    ax.set_ylabel("Cases of Covid-19")
    ax.set_xlabel("Number of week")
    plt.xticks(week_year, rotation ='vertical')
    ax.legend()
    
    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)
    
    return Response(img.getvalue(), mimetype='image/png')


@app.route('/line_graph_death')
def line_graph_death():
    row = graphs.line_graph_death()

    africa_acc = list(accumulate([i[1] for i in row if i[2] == 'Africa']))
    america_acc = list(accumulate([i[1] for i in row if i[2] == 'America']))
    asia_acc = list(accumulate([i[1] for i in row if i[2] == 'Asia']))
    europe_acc = list(accumulate([i[1] for i in row if i[2] == 'Europe']))
    oceania_acc = list(accumulate([i[1] for i in row if i[2] == 'Oceania']))

    week_year = [i[0] for i in row if i[2] == 'Africa']

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.plot(week_year, africa_acc, color='b', label='Africa')
    ax.plot(week_year, america_acc, color='c', label='America')
    ax.plot(week_year, asia_acc, color='g', label='Asia')
    ax.plot(week_year, europe_acc, color='k', label='Europe')
    ax.plot(week_year, oceania_acc, color='r', label='Oceania')
    ax.set_facecolor('whitesmoke')
    ax.set_ylabel("Cases of Covid-19")
    ax.set_xlabel("Number of the week")
    plt.xticks(week_year, rotation ='vertical')
    ax.legend()
    
    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)
    
    return Response(img.getvalue(), mimetype='image/png')


@app.route('/line_graph_per_country')
def line_graph_per_country():
    country = request.args['country']
    row = graphs.line_graph_per_country(country)

    country_acc_cases = list(accumulate([i[1] for i in row]))
    country_acc_death = list(accumulate([i[2] for i in row]))

    week_year = [i[0] for i in row]

    fig = plt.figure()
    ax = fig.add_subplot()

    ax.plot(week_year, country_acc_cases, color='b', label='cases')
    ax.plot(week_year, country_acc_death, color='r', label='death')
    ax.set_facecolor('whitesmoke')
    ax.set_title(f'{country}')
    ax.set_ylabel("Cases/Deaths of Covid-19")
    ax.set_xlabel("Number of the week")
    plt.xticks(week_year, rotation ='vertical')
    ax.legend()
    
    img = io.BytesIO() # data can be kept as bytes in an in-memory buffer when we use the io module’s Byte IO operations.
    fig.savefig(img) # image is saved in the 'img' variable
    FigureCanvas(fig).print_png(img)
    plt.close(fig)
    
    return Response(img.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)