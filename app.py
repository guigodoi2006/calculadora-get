# app.py
import customtkinter as ctk
from tkinter import messagebox

# Aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_WIDTH = 350
APP_HEIGHT = 550

# ---------- Fatores de Atividade por Grupo ----------
FAF_GRUPOS = {
    "População geral": {
        "Sedentário": 1.3,
        "Levemente ativo": 1.5,
        "Moderadamente ativo": 1.7,
        "Muito ativo": 2.0
    },
    "Obesos": {
        "Sedentário": 1.3,
        "Levemente ativo": 1.5,
        "Moderadamente ativo": 1.7,
        "Muito ativo": 2.0
    },
    "Idosos": {
        "Baixa atividade": 1.3,
        "Ativo": 1.5
    },
    "Criança": {
        "Leve/Sedentário": 1.55,
        "Moderado/Ativo": 1.85,
        "Intenso/Pesado": 2.2
    },
    "Atleta": {
        "Treino leve/moderado": 1.65,
        "Treino intenso diário": 1.9,
        "Atleta profissional": 2.2
    }
}

# ---------- Texto da Tela "Sobre" ----------
TEXTO_SOBRE = """
📘 SOBRE A CALCULADORA GET

Esta calculadora estima o Gasto Energético Total (GET) com base em fórmulas reconhecidas:


🏃‍♂️ Fórmulas Utilizadas

• Mifflin-St Jeor — População geral, obesos e idosos
  - Homens: (10 × peso) + (6.25 × altura) – (5 × idade) + 5
  - Mulheres: (10 × peso) + (6.25 × altura) – (5 × idade) – 161

• Katch-McArdle — Atletas
  - TMB = 370 + (21.6 × massa magra)
  (utilizada quando o usuário conhece a massa magra)

• Schofield — Crianças e Adolescentes
  👦 Meninos
    - 0–3 anos: 60.9 × peso – 54
    - 3–10 anos: 22.7 × peso + 495
    - 10–18 anos: 17.5 × peso + 651
  👧 Meninas
    - 0–3 anos: 61.0 × peso – 51
    - 3–10 anos: 22.5 × peso + 499
    - 10–18 anos: 12.2 × peso + 746


⚙️ Fatores de Atividade Física (FAF)

📍 População Geral / Obesos:
  - Sedentário: 1.2 – 1.4 → Média: 1.3
  - Levemente ativo: 1.4 – 1.6 → Média: 1.5
  - Moderadamente ativo: 1.6 – 1.8 → Média: 1.7
  - Muito ativo: 1.8 – 2.2 → Média: 2.0

📍 Idosos:
  - Baixa atividade: 1.2 – 1.4 → Média: 1.3
  - Ativo: 1.4 – 1.6 → Média: 1.5

📍 Crianças / Adolescentes:
  - Leve/Sedentário: 1.40 – 1.69 → Média: 1.55
  - Moderado/Ativo: 1.70 – 1.99 → Média: 1.85
  - Intenso/Pesado: 2.00 – 2.40 → Média: 2.20

📍 Atletas:
  - Treino leve/moderado: 1.55 – 1.75 → Média: 1.65
  - Treino intenso diário: 1.85 – 2.00 → Média: 1.90
  - Atleta profissional: 2.00 – 2.40+ → Média: 2.20


⚠️ Aviso Importante

Os resultados são estimativas médias, servindo apenas como referência.
Consulte sempre um profissional de saúde para avaliação individual.
"""

# ---------- Funções de cálculo ----------
def calcular_mifflin(peso, altura, idade, sexo, faf):
    if sexo == "Homem":
        tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * idade) - 161
    return tmb, tmb * faf

def calcular_cunningham(massa_magra, faf):
    tmb = 370 + (21.6 * massa_magra)
    return tmb, tmb * faf

def calcular_schofield(peso, idade, sexo, faf):
    if sexo == "Menino":
        if idade < 3:
            bmr = 60.9 * peso - 54
        elif idade < 10:
            bmr = 22.7 * peso + 495
        else:
            bmr = 17.5 * peso + 651
    else:
        if idade < 3:
            bmr = 61.0 * peso - 51
        elif idade < 10:
            bmr = 22.5 * peso + 499
        else:
            bmr = 12.2 * peso + 746
    return bmr, bmr * faf

# ---------- App ----------
app = ctk.CTk()
app.title("Calculadora GET")
app.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
app.resizable(False, False)

def mostrar_frame(frame):
    for f in (frame_menu, frame_calcular, frame_resultado, frame_sobre):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ---------- MENU ----------
frame_menu = ctk.CTkFrame(app)
ctk.CTkLabel(frame_menu, text="Calculadora GET", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 10))
ctk.CTkLabel(frame_menu, text="Cálculo do Gasto Energético Total", text_color="gray").pack(pady=(0, 20))
ctk.CTkButton(frame_menu, text="Calcular", width=200, command=lambda: mostrar_frame(frame_calcular)).pack(pady=10)
ctk.CTkButton(frame_menu, text="Sobre", width=200, command=lambda: mostrar_frame(frame_sobre)).pack(pady=10)

# ---------- SOBRE (com Scroll) ----------
frame_sobre = ctk.CTkFrame(app)
ctk.CTkLabel(frame_sobre, text="Sobre a Calculadora", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 8))

# Frame com scroll
scroll_frame = ctk.CTkScrollableFrame(frame_sobre, width=320, height=420)
scroll_frame.pack(pady=5)
ctk.CTkLabel(scroll_frame, text=TEXTO_SOBRE, wraplength=300, justify="left").pack(padx=10, pady=10)

ctk.CTkButton(frame_sobre, text="Voltar", width=160, command=lambda: mostrar_frame(frame_menu)).pack(pady=15)

# ---------- CALCULAR ----------
frame_calcular = ctk.CTkFrame(app)
ctk.CTkLabel(frame_calcular, text="Calcular GET", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 8))

grupos = ["População geral", "Obesos", "Idosos", "Criança", "Atleta"]
var_grupo = ctk.StringVar(value=grupos[0])
ctk.CTkLabel(frame_calcular, text="Selecione o grupo:").pack()
opt_grupo = ctk.CTkOptionMenu(frame_calcular, values=grupos, variable=var_grupo)
opt_grupo.pack(pady=5)

frame_campos = ctk.CTkFrame(frame_calcular, fg_color="transparent")
frame_campos.pack(pady=8)

# Campos dinâmicos
label_sexo = ctk.CTkLabel(frame_campos, text="Sexo:")
opt_sexo = ctk.CTkOptionMenu(frame_campos, values=["Homem", "Mulher"])
label_peso = ctk.CTkLabel(frame_campos, text="Peso (kg):")
entry_peso = ctk.CTkEntry(frame_campos)
label_altura = ctk.CTkLabel(frame_campos, text="Altura (cm):")
entry_altura = ctk.CTkEntry(frame_campos)
label_idade = ctk.CTkLabel(frame_campos, text="Idade (anos):")
entry_idade = ctk.CTkEntry(frame_campos)
label_massa = ctk.CTkLabel(frame_campos, text="Massa magra (kg):")
entry_massa = ctk.CTkEntry(frame_campos)
label_atividade = ctk.CTkLabel(frame_campos, text="Nível de atividade:")
opt_atividade = ctk.CTkOptionMenu(frame_campos, values=list(FAF_GRUPOS["População geral"].keys()))

def atualizar_campos(*_):
    for w in frame_campos.winfo_children():
        w.pack_forget()

    grupo = var_grupo.get()
    if grupo in ("População geral", "Obesos"):
        label_sexo.pack()
        opt_sexo.configure(values=["Homem", "Mulher"])
        opt_sexo.pack()
        label_peso.pack(); entry_peso.pack()
        label_altura.pack(); entry_altura.pack()
        label_idade.pack(); entry_idade.pack()
        label_atividade.pack()
        opt_atividade.configure(values=list(FAF_GRUPOS[grupo].keys()))
        opt_atividade.set("Sedentário")
        opt_atividade.pack()
    elif grupo == "Idosos":
        label_sexo.pack(); opt_sexo.configure(values=["Homem", "Mulher"]); opt_sexo.pack()
        label_peso.pack(); entry_peso.pack()
        label_altura.pack(); entry_altura.pack()
        label_idade.pack(); entry_idade.pack()
        label_atividade.pack()
        opt_atividade.configure(values=list(FAF_GRUPOS["Idosos"].keys()))
        opt_atividade.set("Baixa atividade")
        opt_atividade.pack()
    elif grupo == "Atleta":
        label_massa.pack(); entry_massa.pack()
        label_atividade.pack()
        opt_atividade.configure(values=list(FAF_GRUPOS["Atleta"].keys()))
        opt_atividade.set("Treino leve/moderado")
        opt_atividade.pack()
    else:  # Criança
        label_sexo.pack(); opt_sexo.configure(values=["Menino", "Menina"]); opt_sexo.pack()
        label_peso.pack(); entry_peso.pack()
        label_idade.pack(); entry_idade.pack()
        label_atividade.pack()
        opt_atividade.configure(values=list(FAF_GRUPOS["Criança"].keys()))
        opt_atividade.set("Leve/Sedentário")
        opt_atividade.pack()

var_grupo.trace_add("write", atualizar_campos)
atualizar_campos()

# Cálculo
def calcular():
    grupo = var_grupo.get()
    atividade = opt_atividade.get()
    faf = FAF_GRUPOS[grupo][atividade]

    try:
        if grupo in ("População geral", "Obesos", "Idosos"):
            peso = float(entry_peso.get())
            altura = float(entry_altura.get())
            idade = float(entry_idade.get())
            sexo = opt_sexo.get()
            tmb, gt = calcular_mifflin(peso, altura, idade, sexo, faf)
        elif grupo == "Atleta":
            massa = float(entry_massa.get())
            tmb, gt = calcular_cunningham(massa, faf)
        else:
            peso = float(entry_peso.get())
            idade = float(entry_idade.get())
            sexo = opt_sexo.get()
            tmb, gt = calcular_schofield(peso, idade, sexo, faf)

        emagrecer = gt - 300
        ganhar = gt + 300

        label_res_tmb.configure(text=f"TMB: {tmb:.2f} kcal/dia")
        label_res_get.configure(text=f"GET: {gt:.2f} kcal/dia")
        label_res_faf.configure(text=f"FAF aplicado: {faf:.2f}")
        label_res_emagrecer.configure(text=f"Para emagrecer: ~{emagrecer:.2f} kcal/dia")
        label_res_ganhar.configure(text=f"Para ganhar: ~{ganhar:.2f} kcal/dia")
        mostrar_frame(frame_resultado)

    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

ctk.CTkButton(frame_calcular, text="Calcular", width=200, command=calcular).pack(pady=12)
ctk.CTkButton(frame_calcular, text="Voltar", width=200, command=lambda: mostrar_frame(frame_menu)).pack()

# ---------- RESULTADO ----------
frame_resultado = ctk.CTkFrame(app)
ctk.CTkLabel(frame_resultado, text="Resultado", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
label_res_tmb = ctk.CTkLabel(frame_resultado, text=""); label_res_tmb.pack(pady=3)
label_res_get = ctk.CTkLabel(frame_resultado, text=""); label_res_get.pack(pady=3)
label_res_faf = ctk.CTkLabel(frame_resultado, text="", text_color="gray"); label_res_faf.pack(pady=3)
label_res_emagrecer = ctk.CTkLabel(frame_resultado, text=""); label_res_emagrecer.pack(pady=3)
label_res_ganhar = ctk.CTkLabel(frame_resultado, text=""); label_res_ganhar.pack(pady=3)
ctk.CTkLabel(frame_resultado, text="Esses valores são estimativas.\nConsulte um nutricionista.", text_color="gray").pack(pady=6)
ctk.CTkButton(frame_resultado, text="Voltar ao menu", width=160, command=lambda: mostrar_frame(frame_menu)).pack(pady=10)

# Inicializa no menu
mostrar_frame(frame_menu)
app.mainloop()
