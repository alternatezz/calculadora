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
        'operacional_percentual': 13,
        'frete': 0.00  # Adicionado valor padrão para o frete
    }
    config_path = 'config.json'

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                config = json.load(f)
            except ValueError:
                config = default_config
    else:
        config = default_config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

    return config

# Função para carregar o histórico de preços de venda
def carregar_historico():
    historico_path = 'historico.json'
    if os.path.exists(historico_path):
        with open(historico_path, 'r') as f:
            try:
                historico = json.load(f)
            except ValueError:
                historico = []
    else:
        historico = []
        with open(historico_path, 'w') as f:
            json.dump(historico, f, indent=4)

    return historico

# Função para salvar o histórico de preços de venda
def salvar_historico():
    with open('historico.json', 'w') as f:
        json.dump(historico, f, indent=4)

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

        def markup(preco_venda_estimado):
            custo_total = preco_custo + frete + (preco_venda_estimado * imposto_percentual / 100) + (preco_venda_estimado * comissao_percentual / 100) + (preco_venda_estimado * operacional_percentual / 100) + taxa_embalagem
            return (preco_venda_estimado - custo_total) / preco_venda_estimado * 100

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

        adicionar_historico_venda(preco_custo, markup(preco_venda), preco_venda)
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

# Função para adicionar ao histórico da calculadora
def adicionar_historico_calc(expr, resultado):
    historico_calc_listbox.insert(tk.END, f"{expr} = {resultado}")

# Função para adicionar ao histórico de venda
def adicionar_historico_venda(preco_custo, markup_final, preco_venda):
    historico.append({
        "preco_custo": preco_custo,
        "markup_final": markup_final,
        "preco_venda": preco_venda
    })
    salvar_historico()
    historico_venda_listbox.insert(tk.END, f"Preço de Custo: {preco_custo:.2f}, Markup Final: {markup_final:.2f}%, Preço de Venda: {preco_venda:.2f}")

# Função para calcular expressão
def calcular_expressao():
    expr = entry_calculadora.get()
    try:
        resultado = eval(expr)
        adicionar_historico_calc(expr, resultado)
        entry_calculadora.delete(0, tk.END)
        entry_calculadora.insert(tk.END, str(resultado))
    except Exception as e:
        messagebox.showerror("Erro", "Expressão inválida")

# Carregar configurações e histórico
config = carregar_config()
historico = carregar_historico()

# Configurar a interface gráfica
root = tk.Tk()
root.title("Calculadora de Preço de Venda")
root.geometry("700x600")
root.attributes("-topmost", True)  # Sempre em cima

style = ttk.Style()
style.theme_use('clam')

style.configure('TNotebook.Tab', padding=[10, 5], font=('Helvetica', '12'))
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', font=('Helvetica', '12'))

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Frame para o cálculo do preço de venda
frame_precos = ttk.Frame(notebook, padding=20)
notebook.add(frame_precos, text='Preço de Venda')

# Frame para os campos de preço e markup
frame_precos_interno = ttk.Frame(frame_precos, padding=10)
frame_precos_interno.pack(pady=10, fill='both', expand=True)

# Preço de Custo e Markup Desejado à esquerda
frame_esquerda = ttk.Frame(frame_precos_interno)
frame_esquerda.pack(side=tk.LEFT, padx=10)
ttk.Label(frame_esquerda, text="Preço de Custo:").grid(row=0, column=0, pady=5)
entry_preco_custo = ttk.Entry(frame_esquerda)
entry_preco_custo.grid(row=0, column=1, pady=5)

ttk.Label(frame_esquerda, text="Markup Desejado (%):").grid(row=1, column=0, pady=5)
entry_markup = ttk.Entry(frame_esquerda)
entry_markup.grid(row=1, column=1, pady=5)

# Preço de Venda e Markup Final à direita
frame_direita = ttk.Frame(frame_precos_interno)
frame_direita.pack(side=tk.RIGHT, padx=10)
ttk.Label(frame_direita, text="Preço de Venda:").grid(row=0, column=0, pady=5)
entry_preco_venda = ttk.Entry(frame_direita, state='readonly')
entry_preco_venda.grid(row=0, column=1, pady=5)

ttk.Label(frame_direita, text="Markup Final:").grid(row=1, column=0, pady=5)
entry_markup_final = ttk.Entry(frame_direita, state='readonly')
entry_markup_final.grid(row=1, column=1, pady=5)

# Botão de Calcular Preço de Venda no meio
ttk.Button(frame_precos, text="Calcular Preço de Venda", command=calcular_preco_venda).pack(pady=10)

# Configurações de custos adicionais
frame_custos_adicionais = ttk.Frame(frame_precos, padding=10)
frame_custos_adicionais.pack(pady=10, fill='x')

ttk.Label(frame_custos_adicionais, text="Frete:").grid(row=0, column=0, pady=5)
entry_frete = ttk.Entry(frame_custos_adicionais)
entry_frete.grid(row=0, column=1, pady=5)
entry_frete.insert(0, str(config.get('frete', 0)).replace('.', ','))

ttk.Label(frame_custos_adicionais, text="Taxa de Embalagem:").grid(row=1, column=0, pady=5)
entry_taxa_embalagem = ttk.Entry(frame_custos_adicionais)
entry_taxa_embalagem.grid(row=1, column=1, pady=5)
entry_taxa_embalagem.insert(0, str(config.get('taxa_embalagem', 0)).replace('.', ','))

ttk.Label(frame_custos_adicionais, text="Imposto (%):").grid(row=2, column=0, pady=5)
entry_imposto_percentual = ttk.Entry(frame_custos_adicionais)
entry_imposto_percentual.grid(row=2, column=1, pady=5)
entry_imposto_percentual.insert(0, str(config.get('imposto_percentual', 0)).replace('.', ','))

ttk.Label(frame_custos_adicionais, text="Comissão (%):").grid(row=3, column=0, pady=5)
entry_comissao_percentual = ttk.Entry(frame_custos_adicionais)
entry_comissao_percentual.grid(row=3, column=1, pady=5)
entry_comissao_percentual.insert(0, str(config.get('comissao_percentual', 0)).replace('.', ','))

ttk.Label(frame_custos_adicionais, text="Operacional (%):").grid(row=4, column=0, pady=5)
entry_operacional_percentual = ttk.Entry(frame_custos_adicionais)
entry_operacional_percentual.grid(row=4, column=1, pady=5)
entry_operacional_percentual.insert(0, str(config.get('operacional_percentual', 0)).replace('.', ','))

ttk.Button(frame_precos, text="Salvar Custos Adicionais", command=salvar_custos).pack(pady=10)

# Frame para o histórico de preço de venda
frame_historico_venda = ttk.Frame(frame_precos, padding=10)
frame_historico_venda.pack(pady=10, fill='both', expand=True)

historico_venda_listbox = tk.Listbox(frame_historico_venda, font=('Helvetica', 12))
historico_venda_listbox.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar_venda = tk.Scrollbar(frame_historico_venda)
scrollbar_venda.pack(side=tk.RIGHT, fill='y')

historico_venda_listbox.config(yscrollcommand=scrollbar_venda.set)
scrollbar_venda.config(command=historico_venda_listbox.yview)

# Carregar histórico de vendas
for item in historico:
    historico_venda_listbox.insert(tk.END, f"Preço de Custo: {item['preco_custo']:.2f}, Markup Final: {item['markup_final']:.2f}%, Preço de Venda: {item['preco_venda']:.2f}")

# Frame para a calculadora
frame_calculadora = ttk.Frame(notebook, padding=20)
notebook.add(frame_calculadora, text='Calculadora')

entry_calculadora = ttk.Entry(frame_calculadora, font=('Helvetica', 14), justify='right')
entry_calculadora.pack(pady=10, padx=10, fill='x')

frame_botoes = ttk.Frame(frame_calculadora)
frame_botoes.pack()

botoes = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

linha = 0
coluna = 0
for botao in botoes:
    comando = lambda x=botao: click_botao(x)
    if botao == '=':
        ttk.Button(frame_botoes, text=botao, width=10, command=calcular_expressao).grid(row=linha, column=coluna, columnspan=2)
        coluna += 1
    else:
        ttk.Button(frame_botoes, text=botao, width=5, command=comando).grid(row=linha, column=coluna)
    coluna += 1
    if coluna > 3:
        coluna = 0
        linha += 1

def click_botao(botao):
    if botao == '=':
        calcular_expressao()
    else:
        entry_calculadora.insert(tk.END, botao)

# Histórico da calculadora
frame_historico_calc = ttk.Frame(frame_calculadora, padding=10)
frame_historico_calc.pack(pady=10, fill='both', expand=True)

historico_calc_listbox = tk.Listbox(frame_historico_calc, font=('Helvetica', 12))
historico_calc_listbox.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar_calc = tk.Scrollbar(frame_historico_calc)
scrollbar_calc.pack(side=tk.RIGHT, fill='y')

historico_calc_listbox.config(yscrollcommand=scrollbar_calc.set)
scrollbar_calc.config(command=historico_calc_listbox.yview)

root.mainloop()
