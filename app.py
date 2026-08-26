import io
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Simulador de IRA - UNIFEI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

NOTA_APROVACAO = 6.0
FREQUENCIA_MINIMA = 75.0


# ============================================================
# ESTILO - MODO CLARO
# ============================================================

st.markdown(
    """
<style>
:root {
    --caemt: #4A148C;
    --unifei: #0056B3;
    --bg: #FFFFFF;
    --bg-soft: #F7F9FC;
    --text: #1F2937;
    --muted: #667085;
    --border: #D8DEE8;
    --green-bg: #EAF7EE;
    --green: #126836;
    --red-bg: #FDECEC;
    --red: #A32121;
    --blue-bg: #EEF4FF;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    color-scheme: light !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,.96) !important;
}

#MainMenu, footer { visibility: hidden; }

.brand-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: -8px;
}
.brand-caemt { color: var(--caemt) !important; }
.brand-unifei { color: var(--unifei) !important; }

h1 {
    text-align: center;
    color: var(--text) !important;
    font-weight: 800;
    margin-top: 10px;
}

h2, h3 { color: var(--text) !important; }

.subtitle {
    text-align: center;
    color: var(--muted) !important;
    margin-top: -8px;
    margin-bottom: 22px;
}

.grade-badge {
    width: fit-content;
    margin: 0 auto 22px auto;
    padding: 7px 12px;
    border-radius: 999px;
    background: var(--blue-bg);
    border: 1px solid #C9DBF5;
    color: var(--unifei) !important;
    font-size: .84rem;
    font-weight: 700;
}

.metric-card {
    background: var(--bg-soft);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 15px 16px;
    min-height: 92px;
}
.metric-label {
    color: var(--muted) !important;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .45px;
    text-transform: uppercase;
}
.metric-value {
    color: var(--unifei) !important;
    font-size: 1.7rem;
    font-weight: 800;
    margin-top: 5px;
}

.note-box {
    background: #FAFBFC;
    border: 1px solid var(--border);
    border-left: 4px solid var(--caemt);
    border-radius: 8px;
    padding: 11px 13px;
    color: var(--muted) !important;
    font-size: .88rem;
    margin: 8px 0 16px 0;
}

.good-box {
    background: var(--green-bg);
    color: var(--green) !important;
    border: 1px solid #CAE9D5;
    border-left: 4px solid #18864B;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 10px 0;
}

.bad-box {
    background: var(--red-bg);
    color: var(--red) !important;
    border: 1px solid #F4CDCD;
    border-left: 4px solid #C93434;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 10px 0;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stCheckbox"] p {
    color: var(--text) !important;
}

hr { border-color: var(--border) !important; opacity: .8; }

@media (max-width: 768px) {
    .brand-row { font-size: .92rem; }
    h1 { font-size: 1.9rem !important; }
    .subtitle { font-size: .92rem; }
    .metric-value { font-size: 1.45rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GRADES CURRICULARES
# ============================================================

GRADES = {'2023': {'1º Período': {'EMT101': 'Introdução à Engenharia de Materiais',
                         'CCO016': 'Fundamentos de Programação',
                         'IEPG21': 'Ciências Humanas e Sociais',
                         'MAT00A': 'Cálculo A',
                         'LET013': 'Escrita Acadêmica Científica',
                         'EMT102': 'Química Geral',
                         'DES005': 'Desenho Técnico Básico'},
          '2º Período': {'EMT037T': 'Ciência dos Materiais I - Teórica',
                         'EMT037P': 'Ciência dos Materiais I - Experimental',
                         'FIS210': 'Física I',
                         'FIS212': 'Física Experimental I',
                         'MAT00B': 'Cálculo B',
                         'MAT00D': 'Equações Diferenciais A',
                         'QUI212': 'Química Geral Experimental',
                         'EMT201': 'Química Inorgânica',
                         'DES006': 'Desenho Técnico Auxiliado por Computador'},
          '3º Período': {'EMT038': 'Ciência dos Materiais II',
                         'FIS310': 'Física II A',
                         'FIS320': 'Física II B',
                         'EME303': 'Estática',
                         'MAT00C': 'Cálculo C',
                         'MAT00N': 'Cálculo Numérico',
                         'EMT103': 'Físico-Química',
                         'QUI022': 'Química Orgânica'},
          '4º Período': {'EMT039': 'Termodinâmica',
                         'FIS410': 'Física III',
                         'EME405T': 'Resistência dos Materiais',
                         'IEM405P': 'Resistência dos Materiais - Experimental',
                         'MAT013': 'Probabilidade e Estatística',
                         'MAT00E': 'Equações Diferenciais B',
                         'EMT070': 'Materiais e Ambiente',
                         'QUI105': 'Química Analítica',
                         'QUI115': 'Química Analítica Experimental'},
          '5º Período': {'EMT502T': 'Materiais Cerâmicos',
                         'EMT502P': 'Materiais Cerâmicos - Experimental',
                         'EMT501': 'Metalurgia Física',
                         'EMT072': 'Produção de Ligas',
                         'FIS510': 'Física IV A',
                         'IEM002T': 'Fenômenos de Transporte II',
                         'IEM002P': 'Fenômenos de Transporte II - Experimental',
                         'EME505T': 'Resistência dos Materiais II',
                         'IEM505P': 'Resistência dos Materiais II - Experimental',
                         'EMT503': 'Introdução aos Polímeros'},
          '6º Período': {'EMT049T': 'Conformação de Metais e Cerâmicas',
                         'EMT049P': 'Conformação de Metais e Cerâmicas - Experimental',
                         'EMT069': 'Diagrama de Fases',
                         'EMT071': 'Processos de Fabricação I',
                         'EMT071P': 'Processos de Fabricação I - Experimental',
                         'EMT601T': 'Comportamento Mecânico dos Materiais',
                         'EME605T': 'Transferência de Calor I',
                         'EME605P': 'Transferência de Calor I - Experimental',
                         'EEB100': 'Eletricidade Básica',
                         'EMT047T': 'Estrutura e Propriedades dos Polímeros',
                         'EMT063': 'Reologia'},
          '7º Período': {'EMT024T': 'Processamento de Materiais Cerâmicos',
                         'EMT024P': 'Processamento de Materiais Cerâmicos - Experimental',
                         'EMT025T': 'Técnicas de Caracterização de Materiais',
                         'EMT125P': 'Técnicas de Caracterização de Materiais - Experimental',
                         'EMT030': 'Fundamentos de Oxidação e Corrosão de Metais',
                         'EMT066T': 'Tratamento Térmico',
                         'EMT066P': 'Tratamento Térmico - Experimental',
                         'EMT147P': 'Estrutura e Propriedades dos Polímeros - Experimental',
                         'EMT045T': 'Síntese de Polímeros',
                         'EMT701': 'Materiais Compósitos'},
          '8º Período': {'EMT027T': 'Vidros e Vitrocerâmicos',
                         'EMT046': 'Processamento Aplicado de Materiais Cerâmicos',
                         'EMT067': 'Seleção de Materiais',
                         'EMT065T': 'Processos de Fabricação II',
                         'EMT022T': 'Tratamento Superficial de Metais',
                         'EP7006': 'Higiene e Segurança do Trabalho',
                         'EMT045P': 'Síntese de Polímeros - Experimental',
                         'EMT042T': 'Processamento de Polímeros',
                         'EMT142P': 'Processamento de Polímeros - Experimental',
                         'EMT801P': 'Processamento de Compósitos - Experimental'},
          '9º Período': {'IEPG22': 'Administração Aplicada',
                         'IEPG10': 'Engenharia Econômica',
                         'EMT068': 'Aditivos e Reciclagem de Polímeros'},
          '10º Período': {'ESTEMT2023': 'Estágio Supervisionado',
                          'TCC1EMT2023': 'Trabalho de Conclusão de Curso I',
                          'TCC2EMT2023': 'Trabalho de Conclusão de Curso II'}},
 '2016': {'1º Período': {'EMT101': 'Introdução à EMT',
                         'CCO016': 'Fundamentos de Programação',
                         'SOC002': 'Ciências Humanas e Sociais',
                         'MAT001': 'Cálculo I',
                         'MAT011': 'Geometria Analítica e Álgebra Linear',
                         'FIS104': 'Mecânica Geral',
                         'FIS114': 'Laboratório de Mecânica Geral'},
          '2º Período': {'EMT037T': 'Ciência dos Materiais I - Teórica',
                         'EMT037P': 'Ciência dos Materiais I - Experimental',
                         'FIS203': 'Física Geral I',
                         'FIS213': 'Física Experimental I',
                         'MAT002': 'Cálculo II',
                         'EMT102': 'Química Geral',
                         'BAC002': 'Língua Comum'},
          '3º Período': {'EMT038': 'Ciência dos Materiais II',
                         'FIS303': 'Estática',
                         'EME303': 'Resistência dos Materiais - Teórica',
                         'FIS403': 'Física Geral III',
                         'MAT003': 'Cálculo III',
                         'EMT103': 'Físico-Química',
                         'QUI022': 'Química Orgânica'},
          '4º Período': {'EMT039': 'Termodinâmica',
                         'EME405T': 'Resistência dos Materiais - Experimental',
                         'EME405P': 'Mecânica dos Sólidos - Teórica',
                         'MAT013': 'Probabilidade e Estatística',
                         'MAT021': 'Equações Diferenciais',
                         'QUI105': 'Química Analítica',
                         'QUI115': 'Química Analítica Experimental'},
          '5º Período': {'EMT002T': 'Materiais Cerâmicos - Teórica',
                         'EMT002P': 'Materiais Cerâmicos - Experimental',
                         'EME313T': 'Fenômenos de Transporte - Teórica',
                         'EME313P': 'Fenômenos de Transporte - Experimental',
                         'EME505T': 'Resistência dos Materiais II - Teórica',
                         'EME505P': 'Resistência dos Materiais II - Experimental',
                         'EMT072': 'Produção de Ligas'},
          '6º Período': {'EMT049T': 'Conformação de Metais - Teórica',
                         'EMT049P': 'Conformação de Metais - Experimental',
                         'EMT412T': 'Estrutura e Propriedades Polímeros - Teórica',
                         'EMT412P': 'Estrutura e Propriedades Polímeros - Experimental',
                         'EME047T': 'Estrutura e Propriedades Polímeros - Teórica',
                         'EMT147P': 'Estrutura e Propriedades Polímeros - Experimental',
                         'EMT071': 'Processos de Fabricação I - Experimental',
                         'EME039T': 'Fenômenos de Transporte II - Teórica',
                         'EME039P': 'Fenômenos de Transporte II - Experimental'},
          '7º Período': {'EMT024T': 'Processamento de Materiais Cerâmicos - Teórica',
                         'EMT024P': 'Processamento de Materiais Cerâmicos - Experimental',
                         'EMT025T': 'Técnicas de Caracterização de Materiais',
                         'EMT125P': 'Técnicas de Caracterização - Experimental',
                         'EMT030': 'Fundamentos de Oxidação e Corrosão',
                         'EMT066T': 'Tratamento Térmico - Teórica',
                         'EMT066P': 'Tratamento Térmico - Experimental',
                         'EAM002': 'Ciência de Materiais',
                         'EMT067': 'Seleção de Materiais'},
          '8º Período': {'EMT027T': 'Vidros e Vitrocerâmicos',
                         'EMT046': 'Processamento de Materiais Cerâmicos II',
                         'EMT065T': 'Processos de Fabricação II',
                         'EMT022T': 'Tratamento Superficial de Metais',
                         'EMT042T': 'Processamento de Polímeros - Teórica',
                         'EMT142P': 'Processamento de Polímeros - Experimental',
                         'EPR220': 'Higiene e Segurança do Trabalho',
                         'EPR002': 'Organização Industrial e Administração'},
          '9º Período': {'IEPG01': 'Administração e Economia', 'TCC001': 'Trabalho de Conclusão de Curso I'},
          '10º Período': {'EST001': 'Estágio Supervisionado', 'TCC002': 'Trabalho de Conclusão de Curso II'}}}


# ============================================================
# FUNÇÕES DE DADOS E CÁLCULO
# ============================================================

def catalogo_grade(grade):
    catalogo = {}
    for periodo, materias in GRADES[grade].items():
        for codigo, nome in materias.items():
            catalogo[codigo] = {
                "codigo": codigo,
                "nome": nome,
                "periodo": periodo,
            }
    return catalogo


def opcoes_disciplinas(grade, incluir_outra=True):
    opcoes = []
    for periodo, materias in GRADES[grade].items():
        for codigo, nome in materias.items():
            opcoes.append(f"{codigo} — {nome} · {periodo}")
    if incluir_outra:
        opcoes.append("OUTRA — Optativa, equivalência ou componente não listado")
    return opcoes


def dados_da_opcao(grade, opcao):
    if opcao.startswith("OUTRA —"):
        return None
    codigo = opcao.split(" — ", 1)[0]
    return catalogo_grade(grade).get(codigo)


def determinar_situacao(nota, frequencia):
    if frequencia < FREQUENCIA_MINIMA:
        return "Reprovado por frequência"
    if nota < NOTA_APROVACAO:
        return "Reprovado por nota"
    return "Aprovado"


def calcular_ira(disciplinas):
    if not disciplinas:
        return None, 0.0, 0.0

    soma_ponderada = sum(float(d["nota"]) * float(d["ch"]) for d in disciplinas)
    ch_total = sum(float(d["ch"]) for d in disciplinas)

    if ch_total <= 0:
        return None, 0.0, 0.0

    return soma_ponderada / ch_total, ch_total, soma_ponderada


def calcular_novo_ira(ira_atual, ch_atual, nota, ch_nova):
    denominador = ch_atual + ch_nova
    if denominador <= 0:
        return None
    return ((ira_atual * ch_atual) + (nota * ch_nova)) / denominador


def calcular_nota_necessaria(ira_atual, ch_atual, ch_nova, ira_alvo):
    if ch_nova <= 0:
        return None
    return (ira_alvo * (ch_atual + ch_nova) - ira_atual * ch_atual) / ch_nova


def calcular_media_necessaria_semestre(ira_atual, ch_atual, ch_semestre, ira_alvo):
    if ch_semestre <= 0:
        return None
    return (ira_alvo * (ch_atual + ch_semestre) - ira_atual * ch_atual) / ch_semestre


def chave_grade(prefixo, grade):
    return f"{prefixo}_{grade}"


def init_state():
    if "grade_ira" not in st.session_state:
        st.session_state.grade_ira = "2023"

    for grade in GRADES:
        hkey = chave_grade("historico", grade)
        skey = chave_grade("semestre", grade)
        nkey = chave_grade("next_id", grade)
        snkey = chave_grade("next_sim_id", grade)

        if hkey not in st.session_state:
            st.session_state[hkey] = []
        if skey not in st.session_state:
            st.session_state[skey] = []
        if nkey not in st.session_state:
            st.session_state[nkey] = 1
        if snkey not in st.session_state:
            st.session_state[snkey] = 1


def historico_atual(grade):
    return st.session_state[chave_grade("historico", grade)]


def semestre_atual(grade):
    return st.session_state[chave_grade("semestre", grade)]


def formatar_ch(valor):
    valor = float(valor)
    return str(int(valor)) if valor.is_integer() else f"{valor:g}"


def base_de_calculo(modo, grade, ira_manual=None, ch_manual=None):
    if modo == "Usar histórico cadastrado":
        ira, ch, _ = calcular_ira(historico_atual(grade))
        return ira, ch
    return float(ira_manual), float(ch_manual)


def df_historico(disciplinas):
    return pd.DataFrame(
        [
            {
                "ID": d["id"],
                "Código": d["codigo"],
                "Disciplina": d["nome"],
                "Período": d["periodo"],
                "Nota": d["nota"],
                "CH (h)": d["ch"],
                "Frequência": f'{d["frequencia"]:.1f}%',
                "Situação": d["situacao"],
                "Nota × CH": round(d["nota"] * d["ch"], 2),
            }
            for d in disciplinas
        ]
    )


def df_semestre(disciplinas):
    return pd.DataFrame(
        [
            {
                "ID": d["id"],
                "Código": d["codigo"],
                "Disciplina": d["nome"],
                "Período": d["periodo"],
                "Nota simulada": d["nota"],
                "CH (h)": d["ch"],
            }
            for d in disciplinas
        ]
    )


init_state()


# ============================================================
# CABEÇALHO E GRADE
# ============================================================

st.markdown(
    '<div class="brand-row">'
    '<div class="brand-caemt">CAEMT</div>'
    '<div class="brand-unifei">UNIFEI</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown("<h1>Simulador de IRA</h1>", unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Calcule o IRA, projete notas futuras e descubra quanto precisa tirar para alcançar uma meta.</p>',
    unsafe_allow_html=True,
)

col_grade, col_info = st.columns([1, 2])
with col_grade:
    grade = st.selectbox(
        "Grade curricular",
        options=["2023", "2016"],
        key="grade_ira",
    )
with col_info:
    st.markdown(
        f'<div class="grade-badge">Engenharia de Materiais · Grade {grade}</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="note-box">'
    'As grades servem para selecionar o código e o nome da disciplina. '
    'Informe a carga horária em horas conforme o seu histórico/SIGAA; ela é o peso usado no cálculo do IRA.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# ABAS
# ============================================================

aba_historico, aba_meta, aba_semestre = st.tabs(
    ["📚 Meu IRA", "🎯 Nota necessária", "📈 Simular semestre"]
)


# ============================================================
# ABA 1 - HISTÓRICO
# ============================================================

with aba_historico:
    st.subheader("Histórico acadêmico")
    st.caption("Selecione as disciplinas concluídas e informe a nota final, a carga horária e a frequência.")

    catalogo = catalogo_grade(grade)
    opcoes = opcoes_disciplinas(grade)

    with st.form(f"form_historico_{grade}", clear_on_submit=False):
        c1, c2 = st.columns([2.4, 1])
        with c1:
            opcao = st.selectbox("Disciplina", opcoes, key=f"hist_disc_{grade}")
        with c2:
            ch = st.number_input(
                "Carga horária (h)",
                min_value=1.0,
                max_value=1000.0,
                value=64.0,
                step=1.0,
                key=f"hist_ch_{grade}",
            )

        selecionada = dados_da_opcao(grade, opcao)
        outra = selecionada is None

        if outra:
            c_cod, c_nome = st.columns([1, 3])
            with c_cod:
                codigo_custom = st.text_input("Código", value="OPT", key=f"hist_cod_{grade}")
            with c_nome:
                nome_custom = st.text_input("Nome da disciplina", key=f"hist_nome_{grade}")
        else:
            codigo_custom = selecionada["codigo"]
            nome_custom = selecionada["nome"]

        n1, n2 = st.columns(2)
        with n1:
            nota = st.number_input(
                "Nota final",
                min_value=0.0,
                max_value=10.0,
                value=6.0,
                step=0.1,
                format="%.1f",
                key=f"hist_nota_{grade}",
            )
        with n2:
            frequencia = st.number_input(
                "Frequência (%)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=1.0,
                format="%.1f",
                key=f"hist_freq_{grade}",
            )

        enviar = st.form_submit_button("➕ Adicionar ao histórico", use_container_width=True)

        if enviar:
            if outra and not nome_custom.strip():
                st.error("Informe o nome da disciplina.")
            else:
                periodo = selecionada["periodo"] if selecionada else "Outro"
                codigo = codigo_custom.strip() or "—"
                nome = nome_custom.strip()

                item = {
                    "id": st.session_state[chave_grade("next_id", grade)],
                    "codigo": codigo,
                    "nome": nome,
                    "periodo": periodo,
                    "nota": float(nota),
                    "ch": float(ch),
                    "frequencia": float(frequencia),
                    "situacao": determinar_situacao(float(nota), float(frequencia)),
                }
                historico_atual(grade).append(item)
                st.session_state[chave_grade("next_id", grade)] += 1
                st.rerun()

    disciplinas = historico_atual(grade)
    ira, ch_total, soma_ponderada = calcular_ira(disciplinas)

    st.divider()

    if disciplinas:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">IRA calculado</div>'
                f'<div class="metric-value">{ira:.3f}</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Carga horária</div>'
                f'<div class="metric-value">{formatar_ch(ch_total)} h</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            aprovadas = sum(1 for d in disciplinas if d["situacao"] == "Aprovado")
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Aprovações</div>'
                f'<div class="metric-value">{aprovadas}</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            reprovadas = len(disciplinas) - aprovadas
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Reprovações</div>'
                f'<div class="metric-value">{reprovadas}</div></div>',
                unsafe_allow_html=True,
            )

        st.dataframe(df_historico(disciplinas), use_container_width=True, hide_index=True)

        g1, g2, g3 = st.columns([2, 1, 1])
        with g1:
            mapa = {
                f'{d["id"]} — {d["codigo"]} — {d["nome"]}': d["id"]
                for d in disciplinas
            }
            remover_label = st.selectbox("Remover disciplina", list(mapa), key=f"remove_hist_{grade}")
        with g2:
            st.write("")
            st.write("")
            if st.button("Remover", key=f"btn_remove_hist_{grade}", use_container_width=True):
                alvo = mapa[remover_label]
                st.session_state[chave_grade("historico", grade)] = [
                    d for d in disciplinas if d["id"] != alvo
                ]
                st.rerun()
        with g3:
            st.write("")
            st.write("")
            if st.button("Limpar tudo", key=f"clear_hist_{grade}", use_container_width=True):
                st.session_state[chave_grade("historico", grade)] = []
                st.rerun()

        csv = df_historico(disciplinas).to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Exportar histórico em CSV",
            data=csv,
            file_name=f"historico_ira_grade_{grade}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:
        st.info("Nenhuma disciplina foi adicionada para esta grade.")


# ============================================================
# ABA 2 - NOTA NECESSÁRIA
# ============================================================

with aba_meta:
    st.subheader("Qual nota preciso tirar?")

    modo = st.radio(
        "Base do cálculo",
        ["Usar histórico cadastrado", "Informar IRA atual manualmente"],
        horizontal=True,
        key=f"modo_meta_{grade}",
    )

    ira_base = None
    ch_base = None

    if modo == "Usar histórico cadastrado":
        ira_base, ch_base, _ = calcular_ira(historico_atual(grade))
        if ira_base is None:
            st.warning("Adicione disciplinas na aba Meu IRA ou use o modo manual.")
        else:
            b1, b2 = st.columns(2)
            b1.metric("IRA atual", f"{ira_base:.3f}")
            b2.metric("CH considerada", f"{formatar_ch(ch_base)} h")
    else:
        b1, b2 = st.columns(2)
        with b1:
            ira_base = st.number_input(
                "IRA atual",
                min_value=0.0,
                max_value=10.0,
                value=7.0,
                step=0.01,
                format="%.3f",
                key=f"meta_ira_manual_{grade}",
            )
        with b2:
            ch_base = st.number_input(
                "Carga horária já considerada no IRA",
                min_value=0.0,
                max_value=10000.0,
                value=500.0,
                step=1.0,
                key=f"meta_ch_manual_{grade}",
            )

    if ira_base is not None:
        st.divider()
        op_meta = st.selectbox(
            "Disciplina que você quer simular",
            opcoes_disciplinas(grade),
            key=f"meta_disc_{grade}",
        )
        d_meta = dados_da_opcao(grade, op_meta)

        c1, c2 = st.columns(2)
        with c1:
            ch_nova = st.number_input(
                "Carga horária da disciplina (h)",
                min_value=1.0,
                max_value=1000.0,
                value=64.0,
                step=1.0,
                key=f"meta_ch_nova_{grade}",
            )
        with c2:
            alvo_default = min(10.0, float(ira_base) + 0.10)
            ira_alvo = st.number_input(
                "IRA desejado",
                min_value=0.0,
                max_value=10.0,
                value=alvo_default,
                step=0.01,
                format="%.3f",
                key=f"meta_alvo_{grade}",
            )

        necessaria = calcular_nota_necessaria(float(ira_base), float(ch_base), float(ch_nova), float(ira_alvo))

        st.subheader("Resultado")
        if necessaria > 10:
            maximo = calcular_novo_ira(float(ira_base), float(ch_base), 10.0, float(ch_nova))
            st.error(
                f"A meta não é alcançável apenas com essa disciplina. "
                f"A nota matemática necessária seria {necessaria:.2f}; com 10,0, o IRA iria para {maximo:.3f}."
            )
        elif necessaria <= 0:
            st.success(
                f"O IRA-alvo já é atingido mesmo com nota 0,0 nessa disciplina. "
                f"Para aprovação por nota, porém, considere a média mínima de {NOTA_APROVACAO:.1f}."
            )
        else:
            st.metric("Nota necessária", f"{necessaria:.2f}")
            nome_alvo = d_meta["nome"] if d_meta else "a disciplina selecionada"
            if necessaria < NOTA_APROVACAO:
                ira_com_6 = calcular_novo_ira(float(ira_base), float(ch_base), NOTA_APROVACAO, float(ch_nova))
                st.warning(
                    f"Matematicamente, {necessaria:.2f} basta para o IRA-alvo, mas é inferior à média de aprovação por nota. "
                    f"Com 6,0 em {nome_alvo}, o IRA projetado seria {ira_com_6:.3f}."
                )
            else:
                st.success(
                    f"Você precisa de aproximadamente {necessaria:.2f} em {nome_alvo} para alcançar IRA {ira_alvo:.3f}."
                )


# ============================================================
# ABA 3 - SIMULAR SEMESTRE
# ============================================================

with aba_semestre:
    st.subheader("Simular várias disciplinas futuras")

    modo_sem = st.radio(
        "Base do cálculo",
        ["Usar histórico cadastrado", "Informar IRA atual manualmente"],
        horizontal=True,
        key=f"modo_sem_{grade}",
    )

    ira_sem = None
    ch_sem_base = None

    if modo_sem == "Usar histórico cadastrado":
        ira_sem, ch_sem_base, _ = calcular_ira(historico_atual(grade))
        if ira_sem is None:
            st.warning("Adicione disciplinas na aba Meu IRA ou use o modo manual.")
    else:
        s1, s2 = st.columns(2)
        with s1:
            ira_sem = st.number_input(
                "IRA atual",
                min_value=0.0,
                max_value=10.0,
                value=7.0,
                step=0.01,
                format="%.3f",
                key=f"sem_ira_manual_{grade}",
            )
        with s2:
            ch_sem_base = st.number_input(
                "Carga horária acumulada",
                min_value=0.0,
                max_value=10000.0,
                value=500.0,
                step=1.0,
                key=f"sem_ch_manual_{grade}",
            )

    if ira_sem is not None:
        st.divider()

        with st.form(f"form_semestre_{grade}", clear_on_submit=False):
            opcao_sem = st.selectbox(
                "Adicionar disciplina futura",
                opcoes_disciplinas(grade),
                key=f"sem_disc_{grade}",
            )
            d_sem = dados_da_opcao(grade, opcao_sem)

            if d_sem is None:
                oc1, oc2 = st.columns([1, 3])
                with oc1:
                    cod_sem = st.text_input("Código", value="OPT", key=f"sem_cod_{grade}")
                with oc2:
                    nome_sem = st.text_input("Nome da disciplina", key=f"sem_nome_{grade}")
                periodo_sem = "Outro"
            else:
                cod_sem = d_sem["codigo"]
                nome_sem = d_sem["nome"]
                periodo_sem = d_sem["periodo"]

            sc1, sc2 = st.columns(2)
            with sc1:
                nota_sem = st.number_input(
                    "Nota simulada",
                    min_value=0.0,
                    max_value=10.0,
                    value=7.0,
                    step=0.1,
                    format="%.1f",
                    key=f"sem_nota_{grade}",
                )
            with sc2:
                ch_sem = st.number_input(
                    "Carga horária (h)",
                    min_value=1.0,
                    max_value=1000.0,
                    value=64.0,
                    step=1.0,
                    key=f"sem_ch_{grade}",
                )

            add_sem = st.form_submit_button("➕ Adicionar à simulação", use_container_width=True)

            if add_sem:
                if d_sem is None and not nome_sem.strip():
                    st.error("Informe o nome da disciplina.")
                else:
                    item = {
                        "id": st.session_state[chave_grade("next_sim_id", grade)],
                        "codigo": cod_sem.strip() or "—",
                        "nome": nome_sem.strip(),
                        "periodo": periodo_sem,
                        "nota": float(nota_sem),
                        "ch": float(ch_sem),
                    }
                    semestre_atual(grade).append(item)
                    st.session_state[chave_grade("next_sim_id", grade)] += 1
                    st.rerun()

        simuladas = semestre_atual(grade)

        if simuladas:
            ch_futura = sum(d["ch"] for d in simuladas)
            pontos_futuros = sum(d["nota"] * d["ch"] for d in simuladas)
            media_semestre = pontos_futuros / ch_futura
            novo_ira = ((ira_sem * ch_sem_base) + pontos_futuros) / (ch_sem_base + ch_futura)
            variacao = novo_ira - ira_sem

            q1, q2, q3, q4 = st.columns(4)
            q1.metric("IRA atual", f"{ira_sem:.3f}")
            q2.metric("IRA projetado", f"{novo_ira:.3f}", delta=f"{variacao:+.3f}")
            q3.metric("Média do semestre", f"{media_semestre:.2f}")
            q4.metric("CH futura", f"{formatar_ch(ch_futura)} h")

            st.dataframe(df_semestre(simuladas), use_container_width=True, hide_index=True)

            r1, r2 = st.columns([2, 1])
            with r1:
                mapa_sem = {
                    f'{d["id"]} — {d["codigo"]} — {d["nome"]}': d["id"]
                    for d in simuladas
                }
                rem_sem = st.selectbox("Remover da simulação", list(mapa_sem), key=f"remove_sem_{grade}")
            with r2:
                st.write("")
                st.write("")
                if st.button("Remover", key=f"btn_remove_sem_{grade}", use_container_width=True):
                    alvo = mapa_sem[rem_sem]
                    st.session_state[chave_grade("semestre", grade)] = [
                        d for d in simuladas if d["id"] != alvo
                    ]
                    st.rerun()

            if st.button("Limpar simulação", key=f"clear_sem_{grade}"):
                st.session_state[chave_grade("semestre", grade)] = []
                st.rerun()

            st.divider()
            st.markdown("#### Meta para o fim do semestre")
            ira_meta_sem = st.number_input(
                "IRA desejado após essas disciplinas",
                min_value=0.0,
                max_value=10.0,
                value=min(10.0, float(ira_sem) + 0.10),
                step=0.01,
                format="%.3f",
                key=f"ira_meta_sem_{grade}",
            )
            media_necessaria = calcular_media_necessaria_semestre(
                float(ira_sem), float(ch_sem_base), float(ch_futura), float(ira_meta_sem)
            )

            if media_necessaria > 10:
                st.error(
                    f"Para chegar a IRA {ira_meta_sem:.3f} com essa carga horária futura, "
                    f"seria necessária média {media_necessaria:.2f}, acima de 10,0."
                )
            elif media_necessaria <= 0:
                st.success("A meta já é mantida mesmo com média 0,0 nas disciplinas futuras.")
            else:
                st.info(
                    f"Considerando apenas a carga horária das disciplinas adicionadas, "
                    f"a média ponderada necessária no semestre é aproximadamente {media_necessaria:.2f}."
                )
        else:
            st.info("Adicione uma ou mais disciplinas para projetar o IRA do semestre.")


# ============================================================
# RODAPÉ
# ============================================================

st.divider()
st.caption(
    "Ferramenta independente e não oficial. O cálculo é uma simulação e os valores oficiais devem ser conferidos no SIGAA/UNIFEI."
)
