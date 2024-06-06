from tkinter import *   
from tkinter import filedialog
import pandas as pd
from win10toast import ToastNotifier

OCEANOS = ("Artico", "Atlantico", "Indico", "Pacifico")
DIAS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
MESES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
ANOS = [2023, 2024]

def notificacao_erro(dia_i, mes_i, ano_i, dia_f, mes_f, ano_f):
    toaster = ToastNotifier()

    toaster.show_toast(
        "EcoSystem Data Analysis",
        f"Data incial: {dia_i}/{mes_i}/{ano_i} não pode ser depois da Data final: {dia_f}/{mes_f}/{ano_f}!",
        threaded=True,
        icon_path=None,
        duration=5
    )
    janela_analise.destroy()
    
def notificacao_salvo():
    toaster = ToastNotifier()

    toaster.show_toast(
        "EcoSystem Data Analysis",
        "Documento salvo com sucesso!",
        threaded=True,
        icon_path=None,
        duration=5
    )
    
def notificacao_no_doc(): 
    toaster = ToastNotifier()

    toaster.show_toast(
        "EcoSystem Data Analysis",
        "Nenhum documento selecionado!",
        threaded=True,
        icon_path=None,
        duration=5
    )
    inicial.destroy()
    
def leitor(arquivo):
    try:
        return pd.read_csv(arquivo)
    except (UnicodeDecodeError, pd.errors.ParserError):
        try: 
            return pd.read_excel(arquivo)
        except ValueError:
            return pd.read_json(arquivo)
               
def analise(arquvio, oceano, dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final):
    df = leitor(arquvio)
    df.loc[(df['Oceano'] == oceano) & (df['pH'] >= 7) & (df['pH'] <= 9) | (df['Temperatura'] < 4) , 'Status'] = 'Saudável'
    df.loc[(df['Oceano'] == oceano) & (df['pH'] >= 3) & (df['pH'] <= 6) | (df['Temperatura'] > 4) & (df['Temperatura'] < 5) , 'Status'] = 'Alerta'
    df.loc[(df['Oceano'] == oceano) & (df['pH'] < 3) | (df['Temperatura'] > 5) , 'Status'] = 'Perigo'

    df_final = df[(df['Oceano'] == oceano) & (df['Ano'] >= ano_inicial) & (df['Ano'] <= ano_final) & (df['Mês']>= mes_inicial) & (df['Mês'] <= mes_final) & (df['Dia'] >= dia_inicial) & (df['Dia'] <= dia_final)]

    return df_final

def valida_datas(arquvio, oceano, dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final):
    if ano_inicial > ano_final:
        notificacao_erro(dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final)
        janela_analise.destroy()
    elif ano_inicial == ano_final:
        if mes_inicial > mes_final:
            notificacao_erro(dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final)
            janela_analise.destroy()
        elif mes_inicial == mes_final:
            if dia_inicial > dia_final:
                notificacao_erro(dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final)
                janela_analise.destroy()
    else:
        janela_save_file(arquvio, oceano, dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final)

def janela_save_file(arquvio, oceano, dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final):
    def save_files():
            file = filedialog.asksaveasfile(defaultextension=".xlsx",
                                            filetypes=[("CSV files", "*.csv"), 
                                                        ("Excel files", "*.xlsx"),
                                                        ("JSON files", "*.json"),
                                                        ("all files", "*.*")])
        
            dados = str(analise(arquvio, oceano, dia_inicial, mes_inicial, ano_inicial, dia_final, mes_final, ano_final))
            file.write(dados)
            file.close()
            janela_save.destroy()
            notificacao_salvo()
        
    def exit():
        janela_save.destroy()
        
        
        
    janela_save = Tk()
        
    janela_save.title('EcoSystem Data Analysis')
    janela_save.geometry('500x500')
    janela_save.config(bg='#1f7a8c')
        
    label = Label(janela_save,  
                        text = "EcoSystem Data Analysis", 
                        width = 45, height = 4, 
                        background="#022b3a",  
                        fg = "#bfdbf7", font=('Arial',15))
        
    label.grid(row = 0, column= 0, columnspan=5)
        
    save = Label(janela_save, text='Salvar arquivo:', bg='#1f7a8c', fg='white', font=('Arial',14))
        
    save.grid(row = 1, column= 0, columnspan=5)
        
    button_salvar = Button(janela_save, text="SALVAR", command=save_files)
        
    button_exit = Button(janela_save,  
                         text = "Exit", 
                         command = exit)
        
        
    button_salvar.grid(row = 2, column= 0, columnspan=5, padx=10, pady=10)
    button_exit.grid(row = 3, column = 0, columnspan=5, padx=10, pady=10)
        
        
    janela_save.mainloop()

def janela_analise(arquivo):
    def ok():
        janela_analise.destroy()
        valida_datas(arquivo, oceano.get() ,dia_i.get(), mes_i.get(), ano_i.get(), dia_f.get(), mes_f.get(), ano_f.get())
        
        
    
    def exit(): 
        janela_analise.destroy() 
        return
            
    
    
    janela_analise = Tk()
    
    janela_analise.title('EcoSystem Data Analysis')
    janela_analise.geometry('500x500')
    janela_analise.config(bg='#1f7a8c')
    
    label = Label(janela_analise,  
                  text = "EcoSystem Data Analysis", 
                  width = 45, height = 4, 
                  background="#022b3a",  
                  fg = "#bfdbf7", font=('Arial',15))
    
    label.grid(row = 0, column= 0, columnspan=5)
    
    label_oceano = Label(janela_analise, text='Escolha um oceano:', bg='#1f7a8c', fg='white', font=('Arial',14), pady=5)
    label_oceano.grid(row = 1, column= 0, columnspan=5)
    
    oceano = StringVar(janela_analise)
    oceano.set("Escolha um...")
    oceanos = OptionMenu(janela_analise, oceano, *OCEANOS)
    oceanos.grid(row = 2, column = 0, columnspan=5, padx=20, pady=20)
    
    data_inicial = Label(janela_analise, text='Data Inicial', bg='#1f7a8c', fg='white', font=('Arial',14), pady=5)
    data_inicial.grid(row=3, column=0, columnspan=5)

    dia_i = IntVar(janela_analise)
    dia_i.set("Escolha o Dia")
    dias_i = OptionMenu(janela_analise, dia_i, *DIAS)

    mes_i = IntVar(janela_analise)
    mes_i.set("Escolha o Mês")
    meses_i = OptionMenu(janela_analise, mes_i, *MESES)

    ano_i = IntVar(janela_analise)
    ano_i.set("Escolha o Mês")
    anos_i = OptionMenu(janela_analise, ano_i, *ANOS)

    dash1 = Label(janela_analise, text='/', bg='#1f7a8c')
    dash2 = Label(janela_analise, text='/', bg='#1f7a8c')

    dias_i.grid(row = 4, column = 0)
    dash1.grid(row = 4, column = 1)
    meses_i.grid(row = 4, column = 2)
    dash2.grid(row = 4, column = 3)
    anos_i.grid(row = 4, column = 4)



    data_final = Label(janela_analise, text='Data Final', bg='#1f7a8c', fg='white', font=('Arial',14), pady=5)
    data_final.grid(row=5, column=0, columnspan=5)

    dia_f = IntVar(janela_analise)
    dia_f.set("Escolha o Dia")
    dias_f = OptionMenu(janela_analise, dia_f, *DIAS)

    mes_f = IntVar(janela_analise)
    mes_f.set("Escolha o Mês")
    meses_f = OptionMenu(janela_analise, mes_f, *MESES)

    ano_f = IntVar(janela_analise)
    ano_f.set("Escolha o Mês")
    anos_f = OptionMenu(janela_analise, ano_f, *ANOS)

    dash3 = Label(janela_analise, text='/', bg='#1f7a8c')
    dash4 = Label(janela_analise, text='/', bg='#1f7a8c')

    dias_f.grid(row = 6, column = 0)
    dash3.grid(row = 6, column = 1)
    meses_f.grid(row = 6, column = 2)
    dash4.grid(row = 6, column = 3)
    anos_f.grid(row = 6, column = 4)
    
    
    
    button_okay = Button(janela_analise, text="OK", command=ok)
    
    button_exit = Button(janela_analise,  
                     text = "Exit", 
                     command = exit)
    
    
    button_okay.grid(row = 7, column= 0, columnspan=5, padx=10, pady=10)
    button_exit.grid(row = 8, column = 0, columnspan=5, padx=10, pady=10)
    
    
    janela_analise.mainloop()
    
def browseFiles(): 
    file = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Escolha um Arquivo", 
                                          filetypes = (("XLSX files", 
                                                        "*.xlsx*"),
                                                       ("CSV files", 
                                                        "*.csv*"), 
                                                       ("all files", 
                                                        "*.*")))
    inicial.destroy() 
    if file.count('.xlsx') == 0 and file.count('.csv') == 0 and file.count('.json') == 0:
        notificacao_no_doc()
    else:
        janela_analise(file)

def exit(): 
    inicial.destroy()


inicial = Tk() 
   
inicial.title('EcoSystem Data Analysis') 
   
inicial.geometry("500x500") 
   
inicial.config(background = "#1f7a8c")
   
label = Label(inicial,  
              text = "EcoSystem Data Analysis", 
                width = 45, height = 4, 
                background="#022b3a",  
                fg = "#bfdbf7", font=('Arial',15)) 
   
label_button = Label(inicial,
                     text="Escolha um arquivo para análise:",
                     background = "#1f7a8c",
                     font=('Arial',12), fg='white')

label_button.grid(column = 1, row = 2, padx=20, pady=20)      

button_explore = Button(inicial,  
                        text = "Browse Files",
                        command = browseFiles)  
   
button_exit = Button(inicial,  
                     text = "Exit", 
                     command = exit)  

label.grid(column = 1, row = 1) 
   
button_explore.grid(column = 1, row = 3) 
   
button_exit.grid(column = 1,row = 4, padx=10, pady=10) 
   
inicial.mainloop() 