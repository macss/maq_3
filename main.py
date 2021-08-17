# Máquina Trifásica, 10MVA, 14kV, ligação Y

import numpy as np
import matplotlib.pyplot as plt
import math
import cmath

data = {
    "s_nom": 10000000,
    "v_nom": 14000,
    "lig": "Y",
    "if": np.array([0, 100, 150, 200, 250, 300, 350]),
    "v_vz": np.array([0, 9, 12, 14, 15.3, 15.9, 16.4])*1000
}

data["i_cc"] = 490/data["if"][3] * data["if"]
data["v_ef"] = 18000/data["if"][3] * data["if"]

data["lin_ef"] = data["v_vz"][1]/data["if"][1]*data["if"]

# Calculando Parâmetros

i_nom = data["s_nom"]/(math.sqrt(3)*data["v_nom"])

xs_unsaturated = (data["v_ef"][1]/math.sqrt(3))/data["i_cc"][1]
xs_saturated = (data["v_vz"][4]/math.sqrt(3))/data["i_cc"][4]

rcc = 200 / 209.33 #Valor de 209.33 obtido por interpolação

z_base = data["v_nom"]/(math.sqrt(3)*i_nom)

xs_u_pu = xs_unsaturated / z_base
xs_s_pu = xs_saturated / z_base

print(f'Relação de curto-circuito {rcc} pu. \n')
print(f'Reatância sincrona saturada {xs_saturated} omhs.')
print(f'Reatância sincrona não saturada {xs_unsaturated} omhs. \n')
print(f'Reatância sincrona saturada {xs_s_pu} pu.')
print(f'Reatância sincrona não saturada {xs_u_pu} pu.')
# Desenhando os gráficos

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Corrente de campo (If)')
ax1.set_ylabel('Tensão terminal (Vt)', color=color)
ax1.set_title('Ensaios')
ax1.plot(data["if"], data["v_vz"], color=color, label="CAV")

color = 'tab:green'
ax1.plot(data["if"][0:3], data["lin_ef"][0:3], color=color, label="Linha entreferro")

ax1.legend()

axes = plt.gca()
axes.set_ylim([0,18000])
axes.set_xlim([0,400])

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Corrente de armadura (Ia)', color=color)
ax2.plot(data["if"], data["i_cc"], label="CCC")
axes = plt.gca()
axes.set_ylim([0,1200])

ax2.legend()
plt.savefig('g1.png')

# Característica terminal
i_arm = np.linspace(0, i_nom, 10)

fp_ind = i_arm * cmath.rect(1, -math.acos(0.8))
fp_cap = i_arm * cmath.rect(1, +math.acos(0.8))

vt_ind = (data["v_nom"]) - (1j * xs_saturated * fp_ind)
vt_cap = (data["v_nom"]) - (1j * xs_saturated * fp_cap)

fig, ax3 = plt.subplots()
ax3.plot(i_arm, abs(vt_ind), label="FP indutivo")
ax3.plot(i_arm, abs(vt_cap), label="FP capacitivo")
ax3.set(xlabel="Corrente de armadura (Ia)", ylabel="Tensão terminal (Vt)", title="Vt x Ia")

ax3.legend()
plt.savefig('g2.png')

# Potência dependendo do angulo de conjugado
ang_conj = np.linspace(0, math.pi, 50)
p_saida = [data["s_nom"] * math.sin(x) for x in ang_conj]

fig, ax4 = plt.subplots()

ax4.plot(ang_conj, p_saida, label="Potência de saída")
ax4.set(xlabel="Ângulo Conjugado", ylabel="Potência de saída", title="Po x Ângulo")
ax4.legend()
plt.savefig('g3.png')
#Fim
