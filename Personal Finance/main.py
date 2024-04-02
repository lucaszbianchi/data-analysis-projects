from tkinter import *
from tkinter import Tk, ttk
from PIL import  Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime
from tkinter import messagebox

from view import bar_valores, inserir_categoria, inserir_receita, inserir_gastos, ver_categorias, ver_gastos, ver_receitas, tabela, deletar_gastos, deletar_receitas

def converter_data(data_str):
    # Converter string 'dd/mm/yyyy' para objeto datetime
    return datetime.strptime(data_str, '%d/%m/%Y')

################# cores ###############
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # + verde

colors = ['#5588bb', '#66bbbb','#99bb55', '#ee9944', '#444466', '#bb5555']

# Criar e configurar a janela
janela = Tk()
janela.title('Finance')
janela.geometry('1200x900')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use('clam')

# Definir os frames principais
frameCima = Frame(janela,width=1200, height=50, background= co1, relief='flat')
frameCima.grid(row=0,column=0,padx=3)

frameMeio = Frame(janela,width=1200, height=361, background= co1, pady=20,relief='raised')
frameMeio.grid(row=1,column=0, pady=1, padx=3, sticky=NSEW)

frameBaixo = Frame(janela,width=1200, height=489, background= co1, relief='flat')
frameBaixo.grid(row=2,column=0, pady=0, padx=3, sticky=NSEW)

# Criar um frame dividindo o frame do meio
frame_graficos = Frame(frameMeio, width=900, height=250, bg=co1)
frame_graficos.place(x=300, y=0)

# Criar 3 frames dividindo o frame de baixo
frame_tabela = Frame(frameBaixo, width=800, height=489,bg=co1)
frame_tabela.grid(row=0,column=0)

frame_despesas = Frame(frameBaixo, width=220, height=489,bg=co1)
frame_despesas.grid(row=0,column=1, padx=10)

frame_receitas = Frame(frameBaixo, width=220, height=489,bg=co1)
frame_receitas.grid(row=0,column=2, padx=10)


# Definir Título e Imagem do Head
app_img = Image.open('imagens/coin.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=' Personal Finance', width=1440, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), background= co1, fg=co4)
app_logo.place(x=0, y=0)

# Função a ser executada no botao_inserir_categoria
def nova_categoria():
    categoria = e_categoria.get()
    lista_inserir = [categoria]
    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_categoria.delete(0, 'end')

    dropdown_categoria['values'] = (ver_categorias())
# Função a ser executada no botao_inserir_receita
def nova_receita():
    fonte = 'Receita'
    descrição = 'A definir'
    data = e_cal_receitas.get()
    valor = e_valor_receitas.get()
    
    lista_inserir = [fonte,descrição,data,valor]
    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    inserir_receita(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    atualizar_interface()
# Função a ser executada no botao_inserir_despesa
def nova_despesa():
    categoria = dropdown_categoria.get()
    descrição = 'A definir'
    data = e_cal_despesas.get()
    valor = -int(e_valor_despesas.get())
    
    lista_inserir = [categoria, descrição, data, valor]
    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    dropdown_categoria.delete(0,'end')
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    atualizar_interface()
# Função a ser executada no botão_deletar
def deletar():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        categoria = treev_lista[1]

        if 'Receita' in categoria:
            deletar_receitas([valor])
        else: deletar_gastos([valor])

        messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')

        atualizar_interface()

    except IndexError:
        messagebox.showerror('Erro', 'Seleciona um dos dados na tabela')
# Barra de progresso de porcentagem de receita gasta
def porcentagem(data_inicio=None, data_fim=None):
    l_nome = Label(frame_graficos, text="Porcentagem da Receita gasta", height=1, anchor=NW, font='VERDANA 12', bg=co1, fg=co4)
    l_nome.place(x=140,y=0)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('black.Horizontal.TProgress', background='#daed6b')
    style.configure('TProgressbar',thickness=25)
    bar = Progressbar(frame_graficos, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=140, y=35)
    soma_receitas = sum([float(valor[4]) for valor in ver_receitas(data_inicio=data_inicio,data_fim=data_fim)])
    soma_despesas = sum([float(valor[4]) for valor in ver_gastos(data_inicio=data_inicio,data_fim=data_fim)])
    if soma_receitas != 0: valor = -soma_despesas*100/soma_receitas
    else: valor = 0
    bar['value'] = valor

    l_porcentagem = Label(frame_graficos, text=f"{valor:,.2f}%", anchor=NW, font='VERDANA 12', bg=co1, fg=co4)
    l_porcentagem.place(x=330, y=35)
# Grafico de barras com Renda, Despesas e Saldo
def grafico_bar():
    soma_receitas = sum([valor[3] for valor in ver_receitas()])
    soma_despesas = sum([valor[3] for valor in ver_gastos()])
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = [soma_receitas,soma_despesas,soma_receitas-soma_despesas]

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)

    c = 0
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)
# Resumo em texto
def resumo(data_inicio=None, data_fim=None):
    soma_receitas = sum([float(valor[4]) for valor in ver_receitas(data_inicio=data_inicio,data_fim=data_fim)])
    soma_despesas = sum([float(valor[4]) for valor in ver_gastos(data_inicio=data_inicio,data_fim=data_fim)])
    if soma_receitas != 0: valor = -soma_despesas*100/soma_receitas

    l_linha = Label(frameMeio, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454',)
    l_linha.place(x=59, y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal      ".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=56, y=35)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(soma_receitas), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=56, y=70)

    l_linha = Label(frameMeio, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454',)
    l_linha.place(x=59, y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=56, y=115)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(soma_despesas), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=56, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1,anchor=NW, font=('arial 1 '), bg='#545454',)
    l_linha.place(x=59, y=207)
    l_sumario = Label(frameMeio, text="Total Saldo da Caixa    ".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=56, y=190)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(soma_receitas+soma_despesas), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=56, y=220)
# Grafico de pizza com gastos de cada categoria
def grafico_pie(data_inicio=None, data_fim=None):
    figura = plt.Figure(figsize=(5,3), dpi=90)
    ax = figura.add_subplot(111)
    somas_categorias = {}

    # Calcular a soma dos gastos por categoria
    for gasto in ver_gastos(data_inicio=data_inicio,data_fim=data_fim):
        categoria = gasto[1]
        valor = -(gasto[4])
        if categoria in somas_categorias:
            somas_categorias[categoria] += valor
        else:
            somas_categorias[categoria] = valor

    # Criar a lista de valores no estilo especificado
    lista_valores = [valor for (_, valor) in somas_categorias.items()]
    lista_categorias = [categoria for (categoria, _) in somas_categorias.items()]

    explode = []
    for i in lista_categorias:
        explode.append(0.05)
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
    ax.legend(lista_categorias, loc='center right', bbox_to_anchor=(1.55,0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_graficos)
    canva_categoria.get_tk_widget().place(x=0, y=22)
# Tabela de Gastos e Receitas
def mostrar_tabela(data_inicio='01/03/2024', data_fim='30/03/2024'):
    l_income = Label(frameMeio, text="Tabela Receitas e Despesas", height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_income.place(x=5, y=309)

    tabela_head = ['#id', 'Categoria', 'Descrição', 'Data', 'valor']
    lista_itens = tabela(data_inicio=datetime.strptime(data_inicio, '%d/%m/%Y'),data_fim=datetime.strptime(data_fim, '%d/%m/%Y'))

    global tree

    tree = ttk.Treeview(frame_tabela, selectmode='extended', columns=tabela_head, show='headings', height=20)
    vsb = ttk.Scrollbar(frame_tabela, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center", "center"]
    h=[30,100,300,75,50]
    n=0

    for col in tabela_head:
            tree.heading(col, text=col.title(), anchor=CENTER)
            # adjust the column's width to the header string
            tree.column(col, width=h[n],anchor=hd[n])

            n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


# Interface despesas ------------------------------------------------
l_info = Label(frame_despesas, text="Insira novas despesas", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_categoria = Label(frame_despesas, text="Categoria", height=1,anchor=NW,relief="flat", font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

dropdown_categoria = ttk.Combobox(frame_despesas, width=10,font=('Ivy 10'))
dropdown_categoria['values'] = (ver_categorias())
dropdown_categoria.place(x=110, y=41)

l_cal_despesas = Label(frame_despesas, text="Data", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frame_despesas, locale='pt_BR', date_pattern='dd/MM/yyyy', width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_despesas.place(x=110, y=71)

l_valor_despesas = Label(frame_despesas, text="Valor (R$)", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_despesas, width=14, justify='left',relief="solid")
e_valor_despesas.place(x=110, y=101)

# Botao Inserir despesas
img_add_despesas  = Image.open('imagens/add.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesa = Button(frame_despesas, command=nova_despesa, image=img_add_despesas, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_despesa.place(x=110, y=131)

# Interface receitas ----------------------------------------------------------

l_descricao = Label(frame_receitas, text="Insira novas receitas", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_descricao.place(x=10, y=10)

l_cal_receitas = Label(frame_receitas, text="Data", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_receitas, locale='pt_BR', date_pattern='dd/MM/yyyy', width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_receitas.place(x=110, y=41)

l_valor_receitas = Label(frame_receitas, text="Valor (R$)", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_receitas, width=14, justify='left',relief="solid")
e_valor_receitas.place(x=110, y=71)

# Botao Inserir receitas
img_add_receitas  = Image.open('imagens/add.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receita = Button(frame_receitas, command=nova_receita, image=img_add_receitas, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_receita.place(x=110, y=111)

 # Interface categorias ----------------------------------------------------------------

l_n_categoria = Label(frame_receitas, text="Categoria", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_n_categoria.place(x=10, y=160)
e_categoria = Entry(frame_receitas, width=14, justify='left',relief="solid")
e_categoria.place(x=110, y=160)

# Botao Inserir Categoria
img_add_categoria  = Image.open('imagens/add.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_receitas, command=nova_categoria, image=img_add_categoria, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_categoria.place(x=110, y=190)


# Interface configurações ----------------------------------------------------------------

# operacao Excluir linha
l_n_categoria = Label(frame_despesas, text="Excluir ação", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_n_categoria.place(x=10, y=190)


# Botao excluir
img_delete  = Image.open('imagens/delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_excluir = Button(frame_despesas, command=deletar, image=img_delete, compound=LEFT, anchor=NW, text="   Deletar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_excluir.place(x=110, y=190)

def atualizar_interface():
    mostrar_tabela()
    grafico_pie()
    porcentagem()
    resumo()


atualizar_interface()



janela.mainloop()