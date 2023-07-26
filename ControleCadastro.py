from PyQt5 import uic, QtWidgets
from reportlab.pdfgen import canvas
#from PyQt5.QtCore import Qt, QSortFilterProxyModel
#from PyQt5.QtGui import QstandardItem, QstandardItemModel
import mysql.connector

num_id = 0
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="livraria"
)

def editar_dados():
    global num_id
    linha = listar.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM estoque")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM estoque WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    num_id = valor_id

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    
def update_dados():
    
    #pegar numero Id 
    global num_id
    #valores nos campos lineEdit
    nome = tela_editar.lineEdit_2.text()
    genero = tela_editar.lineEdit_3.text()
    ano = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #atualizar no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE estoque SET nome = '{}', genero = '{}', ano = '{}', categoria = '{}' WHERE id = '{}'" . format(nome,genero,ano,categoria, num_id))
    #atualizando apos salvar 
    tela_editar.close()
    listar.close()
    funcao_listar()


def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM estoque"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("listacadastro.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawAlignedString(400,800, "Lista de estoque")
    pdf.setFont("Times-Bold", 18)

    pdf.drawAlignedString(30,750, "ID")
    pdf.drawAlignedString(160,750, "NOME")
    pdf.drawAlignedString(270,750, "GÊNERO")
    pdf.drawAlignedString(345,750, "ANO")
    pdf.drawAlignedString(470,750, "CATEGORIA")

    for i in range (0, len(dados_lidos)):
        y = y + 50
        
        pdf.drawAlignedString(20,750 - y, str(dados_lidos[i][0]))
        pdf.drawAlignedString(170,750 - y, str(dados_lidos[i][1]))
        pdf.drawAlignedString(270,750 - y, str(dados_lidos[i][2]))
        pdf.drawAlignedString(345,750 - y, str(dados_lidos[i][3]))
        pdf.drawAlignedString(440,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")

def excluir_dados():
    linha = listar.tableWidget.currentRow()
    listar.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM estoque")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM estoque WHERE id=" + str(valor_id))

def funcao_principal():
    linha1 = cadastro.linenome.text()
    linha2 = cadastro.linegenero.text()
    linha3 = cadastro.lineano.text()

    categoria = ""

    if cadastro.radiolivro.isChecked():
        print("Categoria livro foi selecionada")
        categoria = "livro"

    elif cadastro.radiofilme.isChecked():
        print("Categoria livro foi selecionada")
        categoria = "filme"
   
    print("Nome:", linha1)
    print("Genero:", linha2)
    print("Ano:", linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO estoque (nome,genero,ano,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()

    cadastro.linenome.setText("")
    cadastro.linegenero.setText("")
    cadastro.lineano.setText("")

def funcao_listar(): 
    listar.show()
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM estoque"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    print(dados_lidos[0][0])

    listar.tableWidget.setRowCount(len(dados_lidos))
    listar.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            listar.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



app=QtWidgets.QApplication([])
cadastro=uic.loadUi("cadastro.ui")
listar=uic.loadUi("listardados.ui")
tela_editar=uic.loadUi("editar.ui")
cadastro.salvar.clicked.connect(funcao_principal)
cadastro.listar.clicked.connect(funcao_listar)
listar.pdf.clicked.connect(gerar_pdf)
listar.excluir.clicked.connect(excluir_dados)
listar.editar.clicked.connect(editar_dados)
tela_editar.salvar.clicked.connect(update_dados)

cadastro.show()
app.exec()