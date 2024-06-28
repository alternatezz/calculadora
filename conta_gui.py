import tkinter as tk
from tkinter import messagebox
import json
import os

# Função para carregar as configurações do arquivo JSON
def carregar_config():
    default_config = {
        'taxa_embalagem': 4.50,
        'imposto_percentual': 4,
        'comissao_percentual': 20,
        'operacional_percentual': 13,
        'frete': 0.00  # Adicionado valor padrão para o frete
    }
    config_path = 'config.json'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                config = json.load(f)
            except ValueError:  # Alterado para capturar ValueError
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
def calcular_preco_venda():
    try:
        preco_custo = float(entry_preco_custo.get().replace(',', '.'))
        frete = float(entry_frete.get().replace(',', '.'))
        markup_percentual = float(entry_markup.get().replace(',', '.'))
        
        # Verificar se as chaves estão presentes em config
        if 'taxa_embalagem' not in config:
            config['taxa_embalagem'] = 0
        if 'imposto_percentual' not in config:
            config['imposto_percentual'] = 0
        if 'comissao_percentual' not in config:
            config['comissao_percentual'] = 0
        if 'operacional_percentual' not in config:
            config['operacional_percentual'] = 0

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

        entry_preco_venda.config(state='normal')
        entry_preco_venda.delete(0, tk.END)
        entry_preco_venda.insert(0, f"{preco_venda:.2f}".replace('.', ','))
        entry_preco_venda.config(state='readonly')
        
        entry_markup_final.config(state='normal')
        entry_markup_final.delete(0, tk.END)
        entry_markup_final.insert(0, f"{markup(preco_venda):.2f}%".replace('.', ','))
        entry_markup_final.config(state='readonly')
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para salvar custos adicionais
def salvar_custos():
    try:
        config['taxa_embalagem'] = float(entry_taxa_embalagem.get().replace(',', '.'))
        config['imposto_percentual'] = float(entry_imposto_percentual.get().replace(',', '.'))
        config['comissao_percentual'] = float(entry_comissao_percentual.get().replace(',', '.'))
        config['operacional_percentual'] = float(entry_operacional_percentual.get().replace(',', '.'))
        config['frete'] = float(entry_frete.get().replace(',', '.'))
        salvar_config()
        messagebox.showinfo("Sucesso", "Custos adicionais salvos com sucesso.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Configurar a interface gráfica
root = tk.Tk()
root.title("Calculadora de Preço de Venda")
root.geometry("500x400")
root.attributes("-topmost", True)  # Sempre em cima

# Frame para os campos de preço e markup
frame_precos = tk.Frame(root)
frame_precos.pack(pady=10)

# Preço de Custo e Markup Desejado à esquerda
frame_esquerda = tk.Frame(frame_precos)
frame_esquerda.pack(side=tk.LEFT, padx=10)
tk.Label(frame_esquerda, text="Preço de Custo:").grid(row=0, column=0)
entry_preco_custo = tk.Entry(frame_esquerda)
entry_preco_custo.grid(row=0, column=1)

tk.Label(frame_esquerda, text="Markup Desejado (%):").grid(row=1, column=0)
entry_markup = tk.Entry(frame_esquerda)
entry_markup.grid(row=1, column=1)

# Preço de Venda e Markup Final à direita
frame_direita = tk.Frame(frame_precos)
frame_direita.pack(side=tk.RIGHT, padx=10)
tk.Label(frame_direita, text="Preço de Venda:").grid(row=0, column=0)
entry_preco_venda = tk.Entry(frame_direita, state='readonly')
entry_preco_venda.grid(row=0, column=1)

tk.Label(frame_direita, text="Markup Final:").grid(row=1, column=0)
entry_markup_final = tk.Entry(frame_direita, state='readonly')
entry_markup_final.grid(row=1, column=1)

# Botão de Calcular Preço de Venda no meio
tk.Button(root, text="Calcular Preço de Venda", command=calcular_preco_venda).pack(pady=10)

# Configurações de custos adicionais
frame_custos_adicionais = tk.Frame(root)
frame_custos_adicionais.pack(pady=10)

tk.Label(frame_custos_adicionais, text="Frete:").grid(row=0, column=0)
entry_frete = tk.Entry(frame_custos_adicionais)
entry_frete.grid(row=0, column=1)
entry_frete.insert(0, str(config.get('frete', 0)).replace('.', ','))  # Usando get() para garantir que a chave exista

tk.Label(frame_custos_adicionais, text="Taxa de Embalagem:").grid(row=1, column=0)
entry_taxa_embalagem = tk.Entry(frame_custos_adicionais)
entry_taxa_embalagem.grid(row=1, column=1)
entry_taxa_embalagem.insert(0, str(config.get('taxa_embalagem', 0)).replace('.', ','))  # Usando get() para garantir que a chave exista

tk.Label(frame_custos_adicionais, text="Imposto (%):").grid(row=2, column=0)
entry_imposto_percentual = tk.Entry(frame_custos_adicionais)
entry_imposto_percentual.grid(row=2, column=1)
entry_imposto_percentual.insert(0, str(config.get('imposto_percentual', 0)).replace('.', ','))  # Usando get() para garantir que a chave exista

tk.Label(frame_custos_adicionais, text="Comissão (%):").grid(row=3, column=0)
entry_comissao_percentual = tk.Entry(frame_custos_adicionais)
entry_comissao_percentual.grid(row=3, column=1)
entry_comissao_percentual.insert(0, str(config.get('comissao_percentual', 0)).replace('.', ','))  # Usando get() para garantir que a chave exista

tk.Label(frame_custos_adicionais, text="Operacional (%):").grid(row=4, column=0)
entry_operacional_percentual = tk.Entry(frame_custos_adicionais)
entry_operacional_percentual.grid(row=4, column=1)
entry_operacional_percentual.insert(0, str(config.get('operacional_percentual', 0)).replace('.', ','))  # Usando get() para garantir que a chave exista

tk.Button(root, text="Salvar Custos Adicionais", command=salvar_custos).pack(pady=10)

root.mainloop()
