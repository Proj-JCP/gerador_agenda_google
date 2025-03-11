import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta

# Lista para armazenar eventos
eventos = []
FUSO_BRASIL = timezone(timedelta(hours=-3))

# Função para adicionar eventos
def adicionar_evento():
    titulo = entry_titulo.get()
    data_inicio = f"{entry_data_inicio.entry.get()} {hora_inicio_var.get()}:{minuto_inicio_var.get()}"
    data_fim = f"{entry_data_fim.entry.get()} {hora_fim_var.get()}:{minuto_fim_var.get()}"
    local = entry_local.get()
    categoria = entry_categoria.get()
    descricao = entry_descricao.get("1.0", "end").strip()
    
    if not titulo or not data_inicio or not data_fim:
        messagebox.showwarning("Aviso", "Preencha os campos obrigatórios: Título, Data de Início e Data de Fim.")
        return
    
    try:
        data_inicio_formatada = datetime.strptime(data_inicio, "%d/%m/%Y %H:%M").replace(tzinfo=FUSO_BRASIL).isoformat()
        data_fim_formatada = datetime.strptime(data_fim, "%d/%m/%Y %H:%M").replace(tzinfo=FUSO_BRASIL).isoformat()
    except ValueError:
        messagebox.showerror("Erro", "Formato de data ou hora inválido! Use DD/MM/AAAA HH:MM")
        return
    
    evento = Event()
    evento.name = titulo
    evento.begin = data_inicio_formatada
    evento.end = data_fim_formatada
    evento.location = local
    evento.description = f"Categoria: {categoria}\n\n{descricao}"
    
    eventos.append(evento)
    messagebox.showinfo("Sucesso", "Evento adicionado!")
    limpar_campos()

# Função para salvar arquivo ICS
def salvar_ics():
    if not eventos:
        messagebox.showwarning("Aviso", "Nenhum evento foi adicionado!")
        return
    
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("Arquivo ICS", "*.ics")])
    if not caminho_arquivo:
        return
    
    calendario = Calendar()
    for evento in eventos:
        calendario.events.add(evento)
    
    with open(caminho_arquivo, 'w') as f:
        f.write(str(calendario))
    
    messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_arquivo}")
    eventos.clear()

# Função para limpar os campos
def limpar_campos():
    entry_titulo.delete(0, "end")
    entry_data_inicio.entry.delete(0, "end")
    hora_inicio_var.set("12")
    minuto_inicio_var.set("00")
    entry_data_fim.entry.delete(0, "end")
    hora_fim_var.set("12")
    minuto_fim_var.set("00")
    entry_local.delete(0, "end")
    entry_categoria.delete(0, "end")
    entry_descricao.delete("1.0", "end")

# Criando a interface gráfica com ttkbootstrap
root = ttk.Window(themename="superhero")
root.title("Criador de Arquivo .ics")
root.geometry("400x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

# Campos de entrada
ttk.Label(frame, text="Título:").pack()
entry_titulo = ttk.Entry(frame, width=40)
entry_titulo.pack()

ttk.Label(frame, text="Data de Início:").pack()
entry_data_inicio = ttk.DateEntry(frame, bootstyle="info")
entry_data_inicio.pack()

ttk.Label(frame, text="Hora de Início:").pack()
hora_inicio_var = ttk.StringVar(value="12")
minuto_inicio_var = ttk.StringVar(value="00")
frame_hora_inicio = ttk.Frame(frame)
frame_hora_inicio.pack()
spin_hora_inicio = ttk.Spinbox(frame_hora_inicio, from_=0, to=23, textvariable=hora_inicio_var, width=3, bootstyle="info")
spin_hora_inicio.pack(side="left")
ttk.Label(frame_hora_inicio, text=":").pack(side="left")
spin_minuto_inicio = ttk.Spinbox(frame_hora_inicio, from_=0, to=59, textvariable=minuto_inicio_var, width=3, bootstyle="info")
spin_minuto_inicio.pack(side="left")

ttk.Label(frame, text="Data de Fim:").pack()
entry_data_fim = ttk.DateEntry(frame, bootstyle="info")
entry_data_fim.pack()

ttk.Label(frame, text="Hora de Fim:").pack()
hora_fim_var = ttk.StringVar(value="12")
minuto_fim_var = ttk.StringVar(value="00")
frame_hora_fim = ttk.Frame(frame)
frame_hora_fim.pack()
spin_hora_fim = ttk.Spinbox(frame_hora_fim, from_=0, to=23, textvariable=hora_fim_var, width=3, bootstyle="info")
spin_hora_fim.pack(side="left")
ttk.Label(frame_hora_fim, text=":").pack(side="left")
spin_minuto_fim = ttk.Spinbox(frame_hora_fim, from_=0, to=59, textvariable=minuto_fim_var, width=3, bootstyle="info")
spin_minuto_fim.pack(side="left")

ttk.Label(frame, text="Local:").pack()
entry_local = ttk.Entry(frame, width=40)
entry_local.pack()

ttk.Label(frame, text="Categoria:").pack()
entry_categoria = ttk.Entry(frame, width=40)
entry_categoria.pack()

ttk.Label(frame, text="Descrição:").pack()
entry_descricao = ttk.Text(frame, height=5, width=40)
entry_descricao.pack()

# Botões
btn_adicionar = ttk.Button(frame, text="Adicionar Evento", bootstyle="success", command=adicionar_evento)
btn_adicionar.pack(pady=5)

btn_salvar = ttk.Button(frame, text="Salvar .ics", bootstyle="primary", command=salvar_ics)
btn_salvar.pack(pady=5)

root.mainloop()
