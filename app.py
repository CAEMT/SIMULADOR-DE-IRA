from datetime import date
import html

import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Fluxograma Inteligente - Engenharia de Materiais UNIFEI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ESTILO - SOMENTE MODO CLARO
# ============================================================

st.markdown(
    """
<style>
:root {
    --caemt-color: #4A148C;
    --unifei-color: #0056B3;
    --background-color: #FFFFFF;
    --secondary-background: #F7F9FC;
    --text-color: #1F2937;
    --muted-color: #5F6B7A;
    --border-color: #D8DEE8;

    --suggestion-bg: #EAF7EE;
    --suggestion-border: #18864B;
    --suggestion-text: #126836;

    --blocked-bg: #FDECEC;
    --blocked-border: #C93434;
    --blocked-text: #A32121;

    --neutral-bg: #F7F9FC;
    --neutral-border: #D8DEE8;
    --neutral-text: #475467;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    color-scheme: light !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}

[data-testid="stHeader"] {
    background-color: rgba(255, 255, 255, 0.96) !important;
}

#MainMenu,
footer {
    visibility: hidden;
}

.brand-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: -8px;
}

.brand-caemt {
    color: var(--caemt-color) !important;
}

.brand-unifei {
    color: var(--unifei-color) !important;
}

h1 {
    text-align: center;
    color: var(--text-color) !important;
    font-weight: 800;
    margin-top: 10px;
}

h2,
h3 {
    color: var(--text-color) !important;
}

.subtitle {
    text-align: center;
    color: var(--muted-color) !important;
    margin-top: -8px;
    margin-bottom: 22px;
}

.semester-badge {
    width: fit-content;
    margin: 0 auto 24px auto;
    padding: 7px 12px;
    border-radius: 999px;
    background: #EEF4FF;
    border: 1px solid #C9DBF5;
    color: var(--unifei-color) !important;
    font-size: 0.84rem;
    font-weight: 700;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stCheckbox"] p {
    color: var(--text-color) !important;
}

[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 9px !important;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    background-color: var(--secondary-background) !important;
}

[data-testid="stExpander"] summary:hover {
    background-color: #EEF2F7 !important;
}

[data-testid="stExpander"] summary p {
    color: var(--text-color) !important;
    font-weight: 700;
}

hr {
    border-color: var(--border-color) !important;
    opacity: 0.8;
}

.status-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 28px;
    padding: 18px 24px;
    margin: 22px 0 26px 0;
    background: var(--secondary-background);
    border: 1px solid var(--border-color);
    border-radius: 10px;
}

.status-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    min-width: 125px;
}

.status-label {
    color: var(--muted-color) !important;
    font-size: 0.70rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
}

.status-value {
    color: var(--unifei-color) !important;
    font-size: 1.72rem;
    font-weight: 800;
    line-height: 1;
}

.status-divider {
    width: 1px;
    height: 42px;
    background-color: var(--border-color);
}

.sugestao-item,
.bloqueada-oferta,
.bloqueada-requisito {
    padding: 12px 15px;
    margin-bottom: 9px;
    border-radius: 7px;
    font-size: 0.94rem;
    line-height: 1.45;
}

.sugestao-item {
    background-color: var(--suggestion-bg);
    border: 1px solid #CAE9D5;
    border-left: 4px solid var(--suggestion-border);
    color: var(--suggestion-text) !important;
}

.sugestao-item strong {
    color: var(--suggestion-text) !important;
}

.bloqueada-oferta {
    background-color: var(--blocked-bg);
    border: 1px solid #F4CDCD;
    border-left: 4px solid var(--blocked-border);
    color: var(--blocked-text) !important;
}

.bloqueada-oferta strong,
.bloqueada-oferta span {
    color: var(--blocked-text) !important;
}

.bloqueada-requisito {
    background-color: var(--neutral-bg);
    border: 1px solid var(--neutral-border);
    border-left: 4px solid #98A2B3;
    color: var(--neutral-text) !important;
}

.bloqueada-requisito strong,
.bloqueada-requisito span {
    color: var(--neutral-text) !important;
}

.aviso-oferta,
.aviso-requisito {
    display: block;
    margin-top: 4px;
    font-size: 0.80rem;
    font-weight: 600;
}

.divisoria {
    margin: 24px 0 13px 0;
    padding-bottom: 7px;
    border-bottom: 1px solid var(--border-color);
    color: var(--muted-color) !important;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.35px;
}

.small-note {
    color: var(--muted-color) !important;
    font-size: 0.82rem;
}

@media (max-width: 768px) {
    .brand-container {
        font-size: 0.92rem;
    }

    h1 {
        font-size: 1.9rem !important;
    }

    .subtitle {
        font-size: 0.91rem;
    }

    .status-bar {
        gap: 8px;
        padding: 14px 6px;
    }

    .status-item {
        min-width: 0;
        flex: 1;
    }

    .status-label {
        font-size: 0.57rem;
    }

    .status-value {
        font-size: 1.30rem;
    }

    .status-divider {
        height: 34px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# GRADE 2023 - ENGENHARIA DE MATERIAIS / CAMPUS ITAJUBÁ
# ============================================================
#
# "oferta":
#   impar   -> 1º semestre do ano
#   par     -> 2º semestre do ano
#   regular -> pode ser ofertada nos dois semestres
#
# "req" contém os componentes que precisam estar concluídos
# para a disciplina aparecer como liberada no simulador.
# ============================================================

MATRIZ_2023 = {
    "1º Período": {
        "EMT101": {"nome": "Introdução à Engenharia de Materiais", "req": [], "oferta": "impar"},
        "CCO016": {"nome": "Fundamentos de Programação", "req": [], "oferta": "regular"},
        "IEPG21": {"nome": "Ciências Humanas e Sociais", "req": [], "oferta": "regular"},
        "MAT00A": {"nome": "Cálculo A", "req": [], "oferta": "regular"},
        "LET013": {"nome": "Escrita Acadêmica Científica", "req": [], "oferta": "regular"},
        "EMT102": {"nome": "Química Geral", "req": [], "oferta": "regular"},
        "DES005": {"nome": "Desenho Técnico Básico", "req": [], "oferta": "impar"},
    },
    "2º Período": {
        "EMT037T": {"nome": "Ciência dos Materiais I - Teórica", "req": ["EMT101", "EMT102"], "oferta": "par"},
        "EMT037P": {"nome": "Ciência dos Materiais I - Experimental", "req": ["EMT102"], "oferta": "par"},
        "FIS210": {"nome": "Física I", "req": ["MAT00A"], "oferta": "regular"},
        "FIS212": {"nome": "Física Experimental I", "req": [], "oferta": "regular"},
        "MAT00B": {"nome": "Cálculo B", "req": ["MAT00A"], "oferta": "regular"},
        "MAT00D": {"nome": "Equações Diferenciais A", "req": ["MAT00A"], "oferta": "regular"},
        "QUI212": {"nome": "Química Geral Experimental", "req": ["EMT102"], "oferta": "regular"},
        "EMT201": {"nome": "Química Inorgânica", "req": ["EMT102"], "oferta": "par"},
        "DES006": {"nome": "Desenho Técnico Auxiliado por Computador", "req": ["DES005"], "oferta": "par"},
    },
    "3º Período": {
        "EMT038": {"nome": "Ciência dos Materiais II", "req": ["EMT037T"], "oferta": "impar"},
        "FIS310": {"nome": "Física II A", "req": ["FIS210", "MAT00B"], "oferta": "regular"},
        "FIS320": {"nome": "Física II B", "req": ["FIS210", "MAT00B"], "oferta": "regular"},
        "EME303": {"nome": "Estática", "req": ["FIS210", "MAT00A"], "oferta": "regular"},
        "MAT00C": {"nome": "Cálculo C", "req": ["MAT00B"], "oferta": "regular"},
        "MAT00N": {"nome": "Cálculo Numérico", "req": ["MAT00A", "CCO016"], "oferta": "regular"},
        "EMT103": {"nome": "Físico-Química", "req": ["EMT102", "MAT00A"], "oferta": "impar"},
        "QUI022": {"nome": "Química Orgânica", "req": ["EMT102"], "oferta": "impar"},
    },
    "4º Período": {
        "EMT039": {"nome": "Termodinâmica", "req": ["EMT103"], "oferta": "par"},
        "FIS410": {"nome": "Física III", "req": ["FIS310", "MAT00C"], "oferta": "regular"},
        "EME405T": {"nome": "Resistência dos Materiais", "req": ["EME303"], "oferta": "regular"},
        "IEM405P": {"nome": "Resistência dos Materiais - Experimental", "req": ["EME303"], "oferta": "regular"},
        "MAT013": {"nome": "Probabilidade e Estatística", "req": ["MAT00B"], "oferta": "regular"},
        "MAT00E": {"nome": "Equações Diferenciais B", "req": ["MAT00D"], "oferta": "regular"},
        "EMT070": {"nome": "Materiais e Ambiente", "req": [], "oferta": "par"},
        "QUI105": {"nome": "Química Analítica", "req": ["QUI212"], "oferta": "par"},
        "QUI115": {"nome": "Química Analítica Experimental", "req": ["QUI212"], "oferta": "par"},
    },
    "5º Período": {
        "EMT502T": {"nome": "Materiais Cerâmicos", "req": ["EMT038", "EMT039"], "oferta": "impar"},
        "EMT502P": {"nome": "Materiais Cerâmicos - Experimental", "req": ["EMT038"], "oferta": "impar"},
        "EMT501": {"nome": "Metalurgia Física", "req": ["EMT038", "EMT039"], "oferta": "impar"},
        "EMT072": {"nome": "Produção de Ligas", "req": ["EMT038"], "oferta": "impar"},
        "FIS510": {"nome": "Física IV A", "req": ["FIS410"], "oferta": "regular"},
        "IEM002T": {"nome": "Fenômenos de Transporte II", "req": ["MAT00C", "MAT00E"], "oferta": "impar"},
        "IEM002P": {"nome": "Fenômenos de Transporte II - Experimental", "req": ["MAT00C", "MAT00E"], "oferta": "impar"},
        "EME505T": {"nome": "Resistência dos Materiais II", "req": ["EME405T"], "oferta": "impar"},
        "IEM505P": {"nome": "Resistência dos Materiais II - Experimental", "req": ["IEM405P"], "oferta": "impar"},
        "EMT503": {"nome": "Introdução aos Polímeros", "req": ["QUI022"], "oferta": "impar"},
    },
    "6º Período": {
        "EMT049T": {"nome": "Conformação de Metais e Cerâmicas", "req": ["EME405T", "EMT502T"], "oferta": "par"},
        "EMT049P": {"nome": "Conformação de Metais e Cerâmicas - Experimental", "req": ["EMT502P"], "oferta": "par"},
        "EMT069": {"nome": "Diagrama de Fases", "req": ["EMT039"], "oferta": "par"},
        "EMT071": {"nome": "Processos de Fabricação I", "req": ["EMT072"], "oferta": "par"},
        "EMT071P": {"nome": "Processos de Fabricação I - Experimental", "req": ["EMT072"], "oferta": "par"},
        "EMT601T": {"nome": "Comportamento Mecânico dos Materiais", "req": ["EME405T", "EMT038"], "oferta": "par"},
        "EME605T": {"nome": "Transferência de Calor I", "req": ["IEM002T"], "oferta": "par"},
        "EME605P": {"nome": "Transferência de Calor I - Experimental", "req": ["IEM002P"], "oferta": "par"},
        "EEB100": {"nome": "Eletricidade Básica", "req": ["FIS320"], "oferta": "regular"},
        "EMT047T": {"nome": "Estrutura e Propriedades dos Polímeros", "req": ["EMT503"], "oferta": "par"},
        "EMT063": {"nome": "Reologia", "req": ["EMT503"], "oferta": "par"},
    },
    "7º Período": {
        "EMT024T": {"nome": "Processamento de Materiais Cerâmicos", "req": ["EMT049T"], "oferta": "impar"},
        "EMT024P": {"nome": "Processamento de Materiais Cerâmicos - Experimental", "req": ["EMT049P"], "oferta": "impar"},
        "EMT025T": {"nome": "Técnicas de Caracterização de Materiais", "req": ["EMT501"], "oferta": "impar"},
        "EMT125P": {"nome": "Técnicas de Caracterização de Materiais - Experimental", "req": ["EMT501"], "oferta": "impar"},
        "EMT030": {"nome": "Fundamentos de Oxidação e Corrosão de Metais", "req": ["EMT039"], "oferta": "impar"},
        "EMT066T": {"nome": "Tratamento Térmico", "req": ["EMT069"], "oferta": "impar"},
        "EMT066P": {"nome": "Tratamento Térmico - Experimental", "req": ["EMT069"], "oferta": "impar"},
        "EMT147P": {"nome": "Estrutura e Propriedades dos Polímeros - Experimental", "req": ["EMT047T"], "oferta": "impar"},
        "EMT045T": {"nome": "Síntese de Polímeros", "req": ["QUI022"], "oferta": "impar"},
        "EMT701": {"nome": "Materiais Compósitos", "req": ["EMT038"], "oferta": "impar"},
    },
    "8º Período": {
        "EMT027T": {"nome": "Vidros e Vitrocerâmicos", "req": ["EMT024T"], "oferta": "par"},
        "EMT046": {"nome": "Processamento Aplicado de Materiais Cerâmicos", "req": ["EMT024T"], "oferta": "par"},
        "EMT067": {"nome": "Seleção de Materiais", "req": ["EMT025T"], "oferta": "par"},
        "EMT065T": {"nome": "Processos de Fabricação II", "req": ["EMT071"], "oferta": "par"},
        "EMT022T": {"nome": "Tratamento Superficial de Metais", "req": ["EMT030"], "oferta": "par"},
        "EP7006": {"nome": "Higiene e Segurança do Trabalho", "req": [], "oferta": "regular"},
        "EMT045P": {"nome": "Síntese de Polímeros - Experimental", "req": ["EMT045T"], "oferta": "par"},
        "EMT042T": {"nome": "Processamento de Polímeros", "req": ["EMT047T", "EMT045T"], "oferta": "par"},
        "EMT142P": {"nome": "Processamento de Polímeros - Experimental", "req": ["EMT047T"], "oferta": "par"},
        "EMT801P": {"nome": "Processamento de Compósitos - Experimental", "req": ["EMT701"], "oferta": "par"},
    },
    "9º Período": {
        "IEPG22": {"nome": "Administração Aplicada", "req": [], "oferta": "impar"},
        "IEPG10": {"nome": "Engenharia Econômica", "req": [], "oferta": "impar"},
        "EMT068": {"nome": "Aditivos e Reciclagem de Polímeros", "req": ["EMT042T"], "oferta": "impar"},
    },
    "10º Período": {
        "ESTEMT2023": {"nome": "Estágio Supervisionado", "req": [], "oferta": "regular"},
        "TCC1EMT2023": {"nome": "Trabalho de Conclusão de Curso I", "req": [], "oferta": "regular"},
        "TCC2EMT2023": {"nome": "Trabalho de Conclusão de Curso II", "req": ["TCC1EMT2023"], "oferta": "regular"},
    },
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================


def todas_as_disciplinas():
    """Retorna um dicionário código -> dados para toda a matriz."""
    resultado = {}

    for periodo, materias in MATRIZ_2023.items():
        for codigo, dados in materias.items():
            resultado[codigo] = {
                **dados,
                "periodo": periodo,
            }

    return resultado


DISCIPLINAS = todas_as_disciplinas()


def proximo_semestre_referencia(hoje=None):
    """Retorna (oferta, texto) para o próximo semestre civil."""
    hoje = hoje or date.today()

    if hoje.month <= 6:
        return "par", f"2º semestre de {hoje.year}"

    return "impar", f"1º semestre de {hoje.year + 1}"


def chave_checkbox(codigo):
    return f"concluida_{codigo}"


def inicializar_estado():
    for codigo in DISCIPLINAS:
        chave = chave_checkbox(codigo)
        if chave not in st.session_state:
            st.session_state[chave] = False


def disciplinas_concluidas():
    return {
        codigo
        for codigo in DISCIPLINAS
        if st.session_state.get(chave_checkbox(codigo), False)
    }


def marcar_periodo(periodo, valor):
    for codigo in MATRIZ_2023[periodo]:
        st.session_state[chave_checkbox(codigo)] = valor


def limpar_todas():
    for codigo in DISCIPLINAS:
        st.session_state[chave_checkbox(codigo)] = False


def escapar(texto):
    return html.escape(str(texto))


def renderizar_disponivel(codigo, dados):
    codigo_html = escapar(codigo)
    nome_html = escapar(dados["nome"])

    st.markdown(
        '<div class="sugestao-item">'
        f'<strong>{codigo_html}</strong> - {nome_html}'
        '</div>',
        unsafe_allow_html=True,
    )


def renderizar_nao_ofertada(codigo, dados, semestre_destino):
    codigo_html = escapar(codigo)
    nome_html = escapar(dados["nome"])

    if dados["oferta"] == "impar":
        oferta_texto = "Componente previsto para o 1º semestre do ano."
    else:
        oferta_texto = "Componente previsto para o 2º semestre do ano."

    st.markdown(
        '<div class="bloqueada-oferta">'
        f'<strong>{codigo_html}</strong> - {nome_html}'
        f'<span class="aviso-oferta">{escapar(oferta_texto)} Destino atual: {escapar(semestre_destino)}.</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def renderizar_bloqueada(codigo, dados, faltantes):
    codigo_html = escapar(codigo)
    nome_html = escapar(dados["nome"])
    faltantes_html = ", ".join(escapar(item) for item in faltantes)

    st.markdown(
        '<div class="bloqueada-requisito">'
        f'<strong>{codigo_html}</strong> - {nome_html}'
        f'<span class="aviso-requisito">Falta concluir: {faltantes_html}</span>'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# INICIALIZAÇÃO
# ============================================================

inicializar_estado()
semestre_oferta, semestre_texto = proximo_semestre_referencia()


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="brand-container">'
    '<div class="brand-caemt">CAEMT</div>'
    '<div class="brand-unifei">UNIFEI</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown("<h1>Fluxograma Inteligente</h1>", unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">'
    'Grade 2023 - Engenharia de Materiais, Campus Itajubá. '
    'Marque apenas as disciplinas que você já concluiu.'
    '</p>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="semester-badge">Planejamento automático: {escapar(semestre_texto)}</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CONTROLES RÁPIDOS
# ============================================================

controle1, controle2, espaco = st.columns([1, 1, 4])

with controle1:
    if st.button("Limpar seleção", use_container_width=True):
        limpar_todas()
        st.rerun()

with controle2:
    st.caption("A seleção fica apenas nesta sessão.")

st.markdown("---")


# ============================================================
# LAYOUT PRINCIPAL
# ============================================================

col_esquerda, col_direita = st.columns([1.18, 0.82], gap="large")


# ============================================================
# COLUNA ESQUERDA - TODAS AS DISCIPLINAS
# ============================================================

with col_esquerda:
    st.markdown("### 1. Disciplinas concluídas")
    st.caption("Abra os períodos e marque somente o que já foi concluído.")

    for periodo, materias in MATRIZ_2023.items():
        concluidas_periodo = sum(
            1
            for codigo in materias
            if st.session_state.get(chave_checkbox(codigo), False)
        )

        titulo = f"{periodo} - {concluidas_periodo}/{len(materias)} concluídas"

        with st.expander(titulo, expanded=periodo in {"1º Período", "2º Período"}):
            botao1, botao2 = st.columns(2)

            with botao1:
                if st.button(
                    "Marcar período inteiro",
                    key=f"marcar_{periodo}",
                    use_container_width=True,
                ):
                    marcar_periodo(periodo, True)
                    st.rerun()

            with botao2:
                if st.button(
                    "Desmarcar período",
                    key=f"desmarcar_{periodo}",
                    use_container_width=True,
                ):
                    marcar_periodo(periodo, False)
                    st.rerun()

            for codigo, dados in materias.items():
                st.checkbox(
                    f"**{codigo}** - {dados['nome']}",
                    key=chave_checkbox(codigo),
                )


# ============================================================
# CÁLCULOS DO ESTADO ATUAL
# ============================================================

concluidas = disciplinas_concluidas()
total_materias = len(DISCIPLINAS)
total_concluidas = len(concluidas)
progresso = round((total_concluidas / total_materias) * 100) if total_materias else 0

liberadas = []
liberadas_nao_ofertadas = []
bloqueadas = []

for codigo, dados in DISCIPLINAS.items():
    if codigo in concluidas:
        continue

    faltantes = [req for req in dados["req"] if req not in concluidas]

    if faltantes:
        bloqueadas.append((codigo, dados, faltantes))
        continue

    if dados["oferta"] == "regular" or dados["oferta"] == semestre_oferta:
        liberadas.append((codigo, dados))
    else:
        liberadas_nao_ofertadas.append((codigo, dados))


# ============================================================
# BARRA DE STATUS
# ============================================================

st.markdown(
    '<div class="status-bar">'
    '<div class="status-item">'
    '<div class="status-label">Concluídas</div>'
    f'<div class="status-value">{total_concluidas}</div>'
    '</div>'
    '<div class="status-divider"></div>'
    '<div class="status-item">'
    '<div class="status-label">Total da grade</div>'
    f'<div class="status-value">{total_materias}</div>'
    '</div>'
    '<div class="status-divider"></div>'
    '<div class="status-item">'
    '<div class="status-label">Progresso</div>'
    f'<div class="status-value">{progresso}%</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# COLUNA DIREITA - RESULTADOS
# ============================================================

with col_direita:
    st.markdown("### 2. Situação para o próximo semestre")
    st.caption(f"Análise para {semestre_texto}.")

    if liberadas:
        st.markdown(
            '<div class="divisoria">DISCIPLINAS LIBERADAS</div>',
            unsafe_allow_html=True,
        )

        for codigo, dados in liberadas:
            renderizar_disponivel(codigo, dados)
    else:
        st.info("Nenhuma disciplina foi identificada como liberada neste momento.")

    if liberadas_nao_ofertadas:
        st.markdown(
            '<div class="divisoria">LIBERADAS, MAS FORA DO SEMESTRE DE OFERTA</div>',
            unsafe_allow_html=True,
        )

        for codigo, dados in liberadas_nao_ofertadas:
            renderizar_nao_ofertada(codigo, dados, semestre_texto)

    if bloqueadas:
        with st.expander(f"Ver disciplinas ainda bloqueadas ({len(bloqueadas)})"):
            for codigo, dados, faltantes in bloqueadas:
                renderizar_bloqueada(codigo, dados, faltantes)


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")
st.caption(
    "Ferramenta independente e não oficial. A disponibilidade real de turmas, "
    "regras acadêmicas e eventuais alterações curriculares devem ser conferidas no SIGAA/UNIFEI."
)
