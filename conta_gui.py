import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Função para carregar as configurações do arquivo JSON
def carregar_config():
    default_config = {
        'taxa_embalagem': 4.50,
        'imposto_percentual': 4,
        'comissao_percentual': 20,
        'operacional_percentual': 13
    }
    config_path = 'config.json'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = default_config
    else:
        config = default_config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    return config

# Carregar as configurações
config = carregar_config()

# Função para salvar as configurações no arquivo JSON
def salvar_config():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Função para calcular o preço de venda
def calcular_preco_venda(event=None):
    try:
        preco_custo = float(entry_preco_custo.get())
        frete = float(entry_frete.get())
        markup_percentual = float(entry_markup_desejado.get())

        taxa_embalagem = config['taxa_embalagem']
        imposto_percentual = config['imposto_percentual']
        comissao_percentual = config['comissao_percentual']
        operacional_percentual = config['operacional_percentual']

        # Função para calcular o markup baseado no preço de venda estimado
        def markup(preco_venda_estimado):
            custo_total = preco_custo + frete + (preco_venda_estimado * imposto_percentual / 100) + (preco_venda_estimado * comissao_percentual / 100) + (preco_venda_estimado * operacional_percentual / 100) + taxa_embalagem
            return (preco_venda_estimado - custo_total) / preco_venda_estimado * 100

        # Iterar para encontrar o preço de venda que dê o markup desejado
        preco_venda = preco_custo
        while True:
            if markup(preco_venda) >= markup_percentual:
                break
            preco_venda += 0.01

        # Calcular lucro
        markup_final = markup(preco_venda)
        lucro = preco_venda * (markup_final / 100)

        # Atualizar Labels
        label_preco_venda.config(text=f"{preco_venda:.2f}")
        label_markup_final.config(text=f"{markup_final:.2f}%")
        label_lucro.config(text=f"R$ {lucro:.2f}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para salvar custos adicionais
def salvar_custos():
    try:
        config['taxa_embalagem'] = float(entry_taxa_embalagem.get())
        config['imposto_percentual'] = float(entry_imposto_percentual.get())
        config['comissao_percentual'] = float(entry_comissao_percentual.get())
        config['operacional_percentual'] = float(entry_operacional_percentual.get())
        salvar_config()
        messagebox.showinfo("Sucesso", "Custos adicionais salvos com sucesso.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para alternar visibilidade do frame de custos adicionais
def toggle_custos():
    global custos_visivel
    if custos_visivel:
        frame_custos.grid_remove()
        root.geometry("314x311")
        toggle_button.config(text="+")
    else:
        frame_custos.grid()
        root.geometry("313x596")
        toggle_button.config(text="-")
    custos_visivel = not custos_visivel

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Preço de Venda")
root.geometry("313x596")  # Tamanho inicial com custos adicionais visíveis

# Definir a janela como "topmost"
root.attributes('-topmost', True)

# Frame principal
frame_principal = ttk.Frame(root, padding=10)
frame_principal.pack(fill=tk.BOTH, expand=True)

# Frame para calcular preço de venda
frame_preco_venda = ttk.LabelFrame(frame_principal, text='Preço de Venda', padding=10)
frame_preco_venda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_preco_venda, text="Preço de Custo:").grid(row=0, column=0, pady=5)
entry_preco_custo = ttk.Entry(frame_preco_venda)
entry_preco_custo.grid(row=0, column=1, pady=5, sticky="ew")

ttk.Label(frame_preco_venda, text="Markup Desejado (%):").grid(row=1, column=0, pady=5)
entry_markup_desejado = ttk.Entry(frame_preco_venda)
entry_markup_desejado.grid(row=1, column=1, pady=5, sticky="ew")

ttk.Label(frame_preco_venda, text="Preço de Venda:").grid(row=2, column=0, pady=5)
label_preco_venda = ttk.Label(frame_preco_venda, background="lightgrey", relief="sunken", anchor="center")
label_preco_venda.grid(row=2, column=1, pady=5, padx=5, sticky="we")

ttk.Label(frame_preco_venda, text="Markup Final:").grid(row=3, column=0, pady=5)
label_markup_final = ttk.Label(frame_preco_venda, background="lightgrey", relief="sunken", anchor="center")
label_markup_final.grid(row=3, column=1, pady=5, padx=5, sticky="we")

ttk.Label(frame_preco_venda, text="Lucro (R$):").grid(row=4, column=0, pady=5)
label_lucro = ttk.Label(frame_preco_venda, background="lightgrey", relief="sunken", anchor="center")
label_lucro.grid(row=4, column=1, pady=5, padx=5, sticky="we")

calcular_button = ttk.Button(frame_preco_venda, text="Calcular Preço de Venda", command=calcular_preco_venda)
calcular_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="we")

# Bind Enter key to calcular_preco_venda
root.bind('<Return>', calcular_preco_venda)

# Frame para configurar custos adicionais
frame_custos = ttk.LabelFrame(frame_principal, text='Custos Adicionais', padding=10)
frame_custos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_custos, text="Taxa de Embalagem:").grid(row=0, column=0, pady=5)
entry_taxa_embalagem = ttk.Entry(frame_custos)
entry_taxa_embalagem.grid(row=0, column=1, pady=5, sticky="ew")
entry_taxa_embalagem.insert(0, "4.50")

ttk.Label(frame_custos, text="Imposto (%):").grid(row=1, column=0, pady=5)
entry_imposto_percentual = ttk.Entry(frame_custos)
entry_imposto_percentual.grid(row=1, column=1, pady=5, sticky="ew")
entry_imposto_percentual.insert(0, "4.00")

ttk.Label(frame_custos, text="Comissão (%):").grid(row=2, column=0, pady=5)
entry_comissao_percentual = ttk.Entry(frame_custos)
entry_comissao_percentual.grid(row=2, column=1, pady=5, sticky="ew")
entry_comissao_percentual.insert(0, "20.00")

ttk.Label(frame_custos, text="Operacional (%):").grid(row=3, column=0, pady=5)
entry_operacional_percentual = ttk.Entry(frame_custos)
entry_operacional_percentual.grid(row=3, column=1, pady=5, sticky="ew")
entry_operacional_percentual.insert(0, "13.00")

ttk.Label(frame_custos, text="Frete:").grid(row=4, column=0, pady=5)
entry_frete = ttk.Entry(frame_custos)
entry_frete.grid(row=4, column=1, pady=5, sticky="ew")
entry_frete.insert(0, "0.00")

ttk.Button(frame_custos, text="Salvar Custos Adicionais", command=salvar_custos).grid(row=5, column=0, columnspan=2, pady=10, padx=10, sticky="we")

# Botão para alternar visibilidade do frame de custos adicionais
toggle_button = ttk.Button(root, text="-", command=toggle_custos, width=2)
toggle_button.pack(side=tk.BOTTOM, pady=5)

# Ajustar pesos das colunas e linhas para o redimensionamento correto
frame_principal.columnconfigure(0, weight=1)
frame_principal.rowconfigure(0, weight=1)
frame_principal.rowconfigure(1, weight=1)
frame_preco_venda.columnconfigure(1, weight=1)
frame_custos.columnconfigure(1, weight=1)

custos_visivel = True  # Estado inicial

root.mainloop()
