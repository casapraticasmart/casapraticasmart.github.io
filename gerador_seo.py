import json
import html as html_lib
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
GUIAS_DIR = BASE_DIR / "guias"

# 16 Páginas de Cauda Longa (Long-Tail SEO) com altíssima intenção de compra no Google Brasil
TEMAS_COMPARATIVOS_SEO = [
    {
        "slug": "airfryer-ou-panela-de-pressao-eletrica-qual-comprar",
        "titulo_seo": "Airfryer ou Panela de Pressão Elétrica: Qual Vale Mais a Pena em 2026?",
        "meta_desc": "Comparativo completo entre Fritadeira Airfryer Mondial e Panela de Pressão Elétrica Electrolux: consumo de energia, tempo economizado e qual se paga mais rápido.",
        "h1": "Airfryer vs. Panela de Pressão Elétrica: Qual comprar primeiro?",
        "resumo": "Se você trabalha fora e chega cansado(a) em casa, tanto a Airfryer quanto a Panela de Pressão Elétrica reduzem drasticamente os gastos com delivery.",
        "veredito_curto": "Escolha a Airfryer (Mondial AFN-40-BI) para grelhados e porções rápidas de 15 minutos. Escolha a Panela de Pressão Elétrica (Electrolux PCC20) para feijão, carnes e sopas prontas no timer.",
        "categorias_foco": ["cozinha"],
        "palavras_chave": ["air fryer", "panela"],
        "faqs": [
            {
                "pergunta": "Qual gasta mais energia: Airfryer ou Panela de Pressão Elétrica?",
                "resposta": "Ambas concentram o calor em ambiente fechado. Usando 30 minutos por dia, o acréscimo médio na conta de luz é de apenas R$ 12 a R$ 18/mês, enquanto a economia em gás e delivery supera R$ 180/mês."
            },
            {
                "pergunta": "Posso deixar a Panela de Pressão Elétrica ligada sozinha?",
                "resposta": "Sim! O modelo elétrico digital possui sensores térmicos, trava mecânica e desligamento automático ao fim do timer."
            }
        ]
    },
    {
        "slug": "robo-aspirador-vale-a-pena-para-quem-trabalha-fora",
        "titulo_seo": "Robô Aspirador Vale a Pena para Quem Trabalha Fora ou Tem Pets?",
        "meta_desc": "Descubra quantas horas por mês um Robô Aspirador WAP W90 economiza na faxina, se ele limpa pelos de cachorro/gato e os melhores modelos custo-benefício.",
        "h1": "Robô Aspirador Vale a Pena? Cálculo Real de Tempo e Economia",
        "resumo": "Quem trabalha o dia todo não quer gastar o sábado inteiro varrendo a casa. Analisamos o impacto real dos Robôs Aspiradores 3 em 1 na rotina semanal.",
        "veredito_curto": "Sim! O WAP Robot W90 economiza cerca de 4,5 horas toda semana (mais de 230 horas no ano). Para quem tem cachorro, gato ou alergia a poeira, é o item de maior retorno da casa.",
        "categorias_foco": ["limpeza"],
        "palavras_chave": ["robo", "aspirador"],
        "faqs": [
            {
                "pergunta": "Robô aspirador aspira pelos de cachorro e gato de verdade?",
                "resposta": "Sim, rodando diariamente enquanto você está no trabalho, ele impede o acúmulo de pelos nos cantos da sala e debaixo da cama."
            }
        ]
    },
    {
        "slug": "mop-spray-ou-aspirador-vertical-qual-melhor",
        "titulo_seo": "Mop Spray ou Aspirador Vertical 2 em 1: Qual Limpa Mais Rápido?",
        "meta_desc": "Comparativo prático entre Mop Spray Flash Limp e Aspirador Vertical WAP Silent Speed Max: descubra qual economiza mais esforço na limpeza diária.",
        "h1": "Mop Spray vs. Aspirador Vertical: A Dupla que Aposenta Vassoura e Balde",
        "resumo": "Varrer levanta poeira e torcer pano de chão no balde acaba com a coluna. Veja como substituir os dois gastando muito pouco.",
        "veredito_curto": "O Aspirador Vertical WAP 1350W substitui a vassoura aspirando tapetes e cantos em 5 minutos. Já o Mop Spray Flash Limp substitui o rodo e o balde para passar pano úmido em 2 minutos.",
        "categorias_foco": ["limpeza"],
        "palavras_chave": ["mop", "aspirador vertical"],
        "faqs": [
            {
                "pergunta": "O refil do Mop Spray pode ser lavado na máquina?",
                "resposta": "Sim! O refil de microfibra solta facilmente por velcro e pode ir direto na máquina de lavar."
            }
        ]
    },
    {
        "slug": "melhores-achadinhos-de-cozinha-ate-100-reais",
        "titulo_seo": "Melhores Achadinhos de Cozinha Úteis e Baratos (Até R$ 100)",
        "meta_desc": "Seleção dos achadinhos de cozinha mais bem avaliados da Amazon, Mercado Livre e Shopee que economizam tempo todos os dias custando pouco.",
        "h1": "Achadinhos de Cozinha Custo-Benefício: Pequenos Itens que Mudam a Rotina",
        "resumo": "Você não precisa gastar muito para deixar sua cozinha mais rápida. Estes itens baratos resolvem as tarefas mais chatas do preparo diário.",
        "veredito_curto": "O Mini Processador Elétrico USB (R$ 29) e a Seladora a Vácuo Doméstica (R$ 99) têm o maior retorno imediato por real investido.",
        "categorias_foco": ["achadinhos", "organizacao"],
        "palavras_chave": ["mini processador", "seladora", "mop", "tomada"],
        "faqs": [
            {
                "pergunta": "A bateria do Mini Processador Elétrico USB dura quanto tempo?",
                "resposta": "Uma única recarga via cabo USB dura em média de 25 a 30 ciclos de trituração de alho e temperos."
            }
        ]
    },
    {
        "slug": "lista-enxoval-casa-nova-casamento-custo-beneficio",
        "titulo_seo": "Lista de Enxoval de Casa Nova / Casamento Inteligente (Só o que Usa de Verdade)",
        "meta_desc": "Evite comprar eletrodomésticos que ficam parados no armário. Veja o kit essencial de casa nova focado em praticidade para casais que trabalham fora.",
        "h1": "Kit Casa Nova Inteligente: Os Eletros que Realmente Salvam a Semana",
        "resumo": "Muitas listas de casamento incluem aparelhos que você usa uma vez por ano. Esta seleção reúne apenas o que economiza horas toda semana.",
        "veredito_curto": "Para um casal que trabalha fora, o quarteto essencial é: Airfryer 4L, Panela de Pressão Elétrica, Robô Aspirador e Kit de Potes Herméticos.",
        "categorias_foco": ["cozinha", "limpeza", "organizacao"],
        "palavras_chave": ["air fryer", "panela", "robo", "potes"],
        "faqs": [
            {
                "pergunta": "Qual o investimento médio para montar a cozinha prática completa?",
                "resposta": "Com cerca de R$ 1.100 a R$ 1.400 você adquire os 4 principais eletrodomésticos e organizadores que economizam mais de R$ 600 por mês em alimentação fora."
            }
        ]
    },
    {
        "slug": "kit-casa-inteligente-alexa-barato-como-montar",
        "titulo_seo": "Como Montar uma Casa Inteligente com Alexa Gastando Pouco (Guia Prático)",
        "meta_desc": "Veja os 3 únicos itens que você precisa para automatizar luzes, cafeteira, TV e tomadas com Alexa sem precisar de reforma ou eletricista.",
        "h1": "Kit Casa Inteligente Custo-Benefício: Comece com Apenas 3 Itens",
        "resumo": "Com uma Echo Dot 5ª Geração, uma Lâmpada Smart Wi-Fi Positivo e uma Tomada Inteligente você já controla a casa inteira por voz ou celular.",
        "veredito_curto": "Comece pelo combo Echo Dot + Lâmpada Wi-Fi no quarto e um Smart Plug na cafeteira/ventilador. Instala em 5 minutos sem eletricista.",
        "categorias_foco": ["smart"],
        "palavras_chave": ["echo", "plug", "lâmpada"],
        "faqs": [
            {
                "pergunta": "Preciso trocar o interruptor da parede para usar Lâmpada Inteligente?",
                "resposta": "Não! Basta rosquear a Lâmpada Smart Positivo no bocal padrão E27 existente e conectar ao Wi-Fi 2.4GHz pelo aplicativo."
            }
        ]
    },
    {
        "slug": "como-economizar-no-ifood-delivery-cozinha-pratica",
        "titulo_seo": "Como Economizar até R$ 6.000 por Ano em Delivery com uma Cozinha Prática",
        "meta_desc": "Veja a matemática por trás dos pedidos de delivery por cansaço e os utensílios de cozinha que fazem o jantar ficar pronto em 15 minutos.",
        "h1": "Delivery vs. Cozinha Inteligente: Como Cortar Gastos sem Cozinhar Horas",
        "resumo": "O maior vilão do orçamento de quem trabalha fora é pedir delivery 3 a 4 vezes por semana por puro cansaço de cozinhar e lavar louça.",
        "veredito_curto": "Com Potes Herméticos + Seladora a Vácuo para deixar porções prontas e uma Airfryer para finalizar em 15 minutos, a comida fica pronta mais rápido do que a entrega.",
        "categorias_foco": ["organizacao", "cozinha"],
        "palavras_chave": ["potes", "seladora", "air fryer", "panela"],
        "faqs": [
            {
                "pergunta": "Em quanto tempo os utensílios de cozinha prática se pagam?",
                "resposta": "Reduzindo apenas 2 pedidos de delivery por semana, o kit inteiro se paga em menos de 40 dias."
            }
        ]
    },
    {
        "slug": "eletrodomesticos-para-quem-mora-sozinho-kit-essencial",
        "titulo_seo": "Melhores Eletrodomésticos para Quem Mora Sozinho (Práticos e Compactos)",
        "meta_desc": "Mora sozinho e não quer perder tempo cozinhando ou limpando? Veja os 4 aparelhos compactos que resolvem sua alimentação e faxina sem desperdício.",
        "h1": "Kit Moro Sozinho: Como Manter Casa Limpa e Comida Pronta sem Esforço",
        "resumo": "Morar sozinho exige aparelhos fáceis de limpar e que preparem porções individuais sem sujar panelas e sem deixar alimentos estragarem.",
        "veredito_curto": "Airfryer 4L, Mini Processador USB, Mop Spray e Kit de Potes Herméticos formam o combo mais econômico para apartamentos pequenos.",
        "categorias_foco": ["cozinha", "achadinhos", "limpeza"],
        "palavras_chave": ["air fryer", "mini processador", "mop", "potes"],
        "faqs": [
            {
                "pergunta": "Uma Airfryer de 4 Litros é grande demais para quem mora sozinho?",
                "resposta": "Não! O cesto de 4L (como na Mondial AFN-40-BI) é ideal porque permite colocar o prato principal e os legumes lado a lado de uma só vez."
            }
        ]
    },
    {
        "slug": "cafeteira-programavel-vale-a-pena-economia-cafe",
        "titulo_seo": "Cafeteira Elétrica Programável Vale a Pena? Veja Quanto Economiza no Mês",
        "meta_desc": "Descubra como a Cafeteira Programável Electrolux Experience ECM25 prepara o café sozinha antes de você acordar e corta gastos diários na rua.",
        "h1": "Acordar com o Café Pronto: Como Funciona a Cafeteira Programável",
        "resumo": "Tomar café expresso ou pingado na padaria antes do trabalho custa de R$ 8 a R$ 15 por dia (mais de R$ 250/mês). Veja como automatizar o café em casa.",
        "veredito_curto": "Com a Electrolux ECM25 (ou uma cafeteira comum ligada no Smart Plug Wi-Fi), você deixa o pó e a água à noite e acorda às 7h com o café recém-passado.",
        "categorias_foco": ["cozinha", "smart"],
        "palavras_chave": ["cafeteira", "plug", "echo"],
        "faqs": [
            {
                "pergunta": "Posso automatizar uma cafeteira simples usando Tomada Inteligente?",
                "resposta": "Sim! Se a sua cafeteira tiver botão físico liga/desliga, basta deixá-lo acionado e programar a Tomada Inteligente Positivo para ligar na hora que você acorda."
            }
        ]
    },
    {
        "slug": "como-conservar-alimentos-na-geladeira-potes-hermeticos-vacuo",
        "titulo_seo": "Potes Herméticos e Seladora a Vácuo: Como Fazer a Feira Durar 3x Mais",
        "meta_desc": "Veja como organizar a geladeira e congelar porções da semana usando Potes Herméticos com vedação de silicone e Seladora a Vácuo doméstica.",
        "h1": "Zero Desperdício na Cozinha: Potes Herméticos + Seladora a Vácuo",
        "resumo": "Jogar frutas, folhas e sobras fora toda semana representa até 25% do gasto mensal de supermercado. O segredo para evitar isso é bloquear a entrada de ar.",
        "veredito_curto": "Use os Potes Herméticos Empilháveis para saladas lavadas, frutas e grãos secos, e a Seladora a Vácuo para carnes e marmitas no freezer.",
        "categorias_foco": ["organizacao"],
        "palavras_chave": ["potes", "seladora", "mini processador"],
        "faqs": [
            {
                "pergunta": "Salada lavada dura quantos dias no pote hermético?",
                "resposta": "Higienizada e seca com uma folha de papel-toalha dentro do pote hermético, dura de 7 a 10 dias fresca e crocante."
            }
        ]
    },
    {
        "slug": "como-eliminar-pelos-de-cachorro-e-gato-da-casa",
        "titulo_seo": "Como Eliminar Pelos de Cachorro e Gato da Casa sem Varrer Todo Dia",
        "meta_desc": "Tem pets em casa e sofre com pelos no sofá e no chão? Veja a combinação de Robô Aspirador + Aspirador Vertical HEPA que resolve o problema.",
        "h1": "Casa com Pets Sempre Limpa: Os 3 Melhores Aliados contra Pelos",
        "resumo": "Vassoura comum apenas espalha os pelos mais finos pelo ar. Para quem tem cães ou gatos, a sucção com filtro HEPA é indispensável.",
        "veredito_curto": "Deixe o Robô Aspirador WAP W90 manter o chão limpo diariamente sozinho e use o Aspirador Vertical WAP 1350W para sofás e tapetes em 5 minutos.",
        "categorias_foco": ["limpeza"],
        "palavras_chave": ["robo", "aspirador", "mop"],
        "faqs": [
            {
                "pergunta": "O filtro HEPA ajuda quem tem rinite alérgica?",
                "resposta": "Sim, o filtro HEPA retém até 99,5% dos ácaros, poeira fina e partículas de pelo, devolvendo ar limpo ao ambiente."
            }
        ]
    },
    {
        "slug": "ideias-presente-casamento-cha-de-panela-ate-200-reais",
        "titulo_seo": "Melhores Presentes de Casamento e Chá de Casa Nova até R$ 200 (Super Úteis)",
        "meta_desc": "Procurando um presente de casamento ou chá de cozinha entre R$ 50 e R$ 200 que os noivos vão amar? Veja 6 opções modernas com entrega rápida.",
        "h1": "Presentes de Casa Nova até R$ 200 que Todo Casal Realmente Usa",
        "resumo": "Fuja dos presentes repetidos. Itens de organização, casa inteligente e limpeza prática são os mais elogiados por quem está montando a casa.",
        "veredito_curto": "O Kit 10 Potes Herméticos (~R$ 119), o Aspirador Vertical 2 em 1 (~R$ 179) e a Seladora a Vácuo (~R$ 99) parecem presentes caros e são extremamente úteis.",
        "categorias_foco": ["organizacao", "limpeza", "smart"],
        "palavras_chave": ["potes", "aspirador vertical", "seladora", "mop"],
        "faqs": [
            {
                "pergunta": "Esses produtos não têm risco de erro de voltagem (110V/220V)?",
                "resposta": "Itens como o Kit de Potes Herméticos, Mop Spray, Lâmpada Smart Wi-Fi, Smart Plug e Mini Processador USB são bivolt ou não dependem de tomada, zero risco de errar!"
            }
        ]
    },
    {
        "slug": "como-reduzir-conta-de-luz-tomada-lampada-inteligente",
        "titulo_seo": "Tomada Inteligente e Lâmpada Smart Economizam Energia? Veja o Cálculo",
        "meta_desc": "Entenda como medir o consumo em kWh dos seus eletrodomésticos pelo celular e cortar o gasto fantasma (stand-by) com Smart Plugs Wi-Fi.",
        "h1": "Automação que Paga a Conta de Luz: Smart Plug + Lâmpada LED Wi-Fi",
        "resumo": "Aparelhos esquecidos ligados e consumo em stand-by durante o horário comercial podem representar até 12% da sua fatura de energia.",
        "veredito_curto": "O Smart Plug Wi-Fi Positivo mostra no celular exatamente quantos reais cada aparelho consome e desliga tudo automaticamente quando você sai para trabalhar.",
        "categorias_foco": ["smart"],
        "palavras_chave": ["plug", "lâmpada", "echo"],
        "faqs": [
            {
                "pergunta": "Qual a potência suportada pelo Smart Plug Wi-Fi?",
                "resposta": "Os modelos de 16A suportam até 1.600W em 110V ou 3.200W em 220V, atendendo cafeteiras, ventiladores, TVs e aquecedores."
            }
        ]
    },
    {
        "slug": "marmita-da-semana-em-1-hora-equipamentos-cozinha",
        "titulo_seo": "Como Fazer as Marmitas da Semana em 1 Hora no Domingo (Sem Bagunça)",
        "meta_desc": "O método de preparo simultâneo usando Panela de Pressão Elétrica + Airfryer + Seladora/Potes Herméticos para cozinhar para a semana toda em 60 minutos.",
        "h1": "Método Cozinha em Paralelo: Marmitas da Semana Prontas em 1 Hora",
        "resumo": "O segredo para não passar o domingo inteiro na cozinha é deixar 2 aparelhos elétricos trabalhando ao mesmo tempo enquanto você descansa.",
        "veredito_curto": "Enquanto a Panela de Pressão Elétrica cozinha o feijão/carne no timer e a Airfryer assa o frango e legumes em 15 min, você só porciona nos Potes Herméticos.",
        "categorias_foco": ["cozinha", "organizacao"],
        "palavras_chave": ["panela", "air fryer", "potes", "seladora"],
        "faqs": [
            {
                "pergunta": "Comida feita na Airfryer congela bem?",
                "resposta": "Sim! Carnes em tiras, sobrecoxa desossada e legumes assados na Airfryer mantêm excelente textura ao descongelar."
            }
        ]
    },
    {
        "slug": "echo-dot-alexa-na-cozinha-utilidades-praticas",
        "titulo_seo": "Por Que Ter uma Alexa (Echo Dot) na Cozinha ou Sala? 7 Usos Diários",
        "meta_desc": "Muito além de tocar música: veja como usar a Echo Dot 5ª Geração para controlar múltiplos timers de receitas, lista de compras por voz e lembretes.",
        "h1": "7 Funções da Echo Dot (Alexa) que Economizam Tempo Todos os Dias",
        "resumo": "Com as mãos ocupadas na cozinha ou saindo apressado para o trabalho, os comandos de voz evitam esquecimentos e queimados no forno.",
        "veredito_curto": "Dizer 'Alexa, adicione café na lista de compras' no exato segundo em que o pote acaba na cozinha já economiza idas extras ao mercado.",
        "categorias_foco": ["smart", "cozinha"],
        "palavras_chave": ["echo", "lâmpada", "plug", "cafeteira"],
        "faqs": [
            {
                "pergunta": "A Alexa cobra alguma mensalidade para funcionar?",
                "resposta": "Não! Todas as funções de assistente de voz, timers, alarmes, listas de compras, previsão do tempo e controle de casa inteligente são 100% gratuitas."
            }
        ]
    },
    {
        "slug": "faxina-de-apartamento-em-30-minutos-roteiro-equipamentos",
        "titulo_seo": "Roteiro de Faxina de Apartamento em 30 Minutos para Quem Trabalha Fora",
        "meta_desc": "Aprenda a dividir a limpeza pesada em micro-tarefas automáticas usando Aspirador Vertical, Mop Spray e Robô Aspirador.",
        "h1": "Faxina Expressa de 30 Minutos: Recupere o seu Fim de Semana",
        "resumo": "Quando você elimina a vassoura e o balde pesado, a manutenção da casa deixa de ser um evento cansativo de 4 horas no sábado.",
        "veredito_curto": "Robô Aspirador rodando de segunda a sexta + 15 minutos de Aspirador Vertical nos estofados + 10 minutos de Mop Spray com desinfetante perfumado.",
        "categorias_foco": ["limpeza"],
        "palavras_chave": ["robo", "aspirador vertical", "mop"],
        "faqs": [
            {
                "pergunta": "Posso colocar desinfetante ou limpador perfumado no Mop Spray?",
                "resposta": "Sim! Basta diluir água com algumas gotas do seu limpador perfumado favorito (evitando apenas ceras espessas ou cloro puro)."
            }
        ]
    }
]


def formatar_moeda(valor):
    return f"R$ {int(round(float(valor or 0))):,}".replace(",", ".")


def selecionar_produtos_para_guia(produtos, tema):
    palavras = [p.lower() for p in tema.get("palavras_chave", [])]
    cats = tema.get("categorias_foco", [])

    escolhidos = []
    for prod in produtos:
        nome_low = prod.get("nome", "").lower()
        if any(k in nome_low for k in palavras):
            escolhidos.append(prod)

    for prod in produtos:
        if prod not in escolhidos and prod.get("categoria") in cats:
            escolhidos.append(prod)

    if len(escolhidos) < 2:
        escolhidos = produtos[:4]
    return escolhidos[:4]


def gerar_html_guia(tema, produtos_guia, data_str):
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f["pergunta"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f["resposta"]
                }
            }
            for f in tema.get("faqs", [])
        ]
    }

    linhas_tabela = ""
    cards_html = ""
    for p in produtos_guia:
        preco_atual = int(round(float(p.get("precoEstimado", 99))))
        preco_antigo = int(round(float(p.get("precoAntigo", preco_atual * 1.32))))
        desconto_pct = p.get("descontoPct", round((1 - preco_atual / preco_antigo) * 100))
        num_parcelas = p.get("numParcelas", 10 if preco_atual >= 150 else 6)
        preco_fmt = formatar_moeda(preco_atual)
        economia_fmt = formatar_moeda(p.get("economiaMensalReais", 100))
        horas = p.get("horasEconomizadasSemana", 2)
        link_principal = p.get("linkAmazon") or p.get("linkMercadoLivre") or "../index.html"
        img_src = p.get("imagem", "img/airfryer.svg")
        if img_src.startswith("img/"):
            img_src = "../" + img_src

        linhas_tabela += f"""
          <tr>
            <td><strong>{p['nome']}</strong></td>
            <td>~{preco_fmt}</td>
            <td><span class="tag-time">-{horas}h / semana</span></td>
            <td><span class="tag-economy">~{economia_fmt} / mês</span></td>
            <td><a href="{link_principal}" target="_blank" rel="noopener sponsored" class="btn-primary" style="padding:6px 12px; font-size:0.78rem; text-decoration:none; display:inline-block;">🔍 Consultar Preço Hoje</a></td>
          </tr>
        """

        cards_html += f"""
          <article class="product-card">
            <a href="{link_principal}" target="_blank" rel="noopener sponsored" class="product-img-wrap">
              <img class="product-img" src="{img_src}" alt="{p['nome']}" loading="lazy" />
            </a>
            <div class="product-body">
              <div class="retail-badge-row">
                <span class="retail-badge {p.get('corSelo', 'azul')}">{p.get('badge', 'OFERTA DO DIA')}</span>
              </div>
              <h3 class="product-title">{p['nome']}</h3>
              <div class="rating-row">
                <span class="rating-score">{p.get('avaliacao', '4.9')}</span>
                <span class="rating-stars">★★★★★</span>
                <span>({p.get('numAvaliacoes', 2150)})</span>
              </div>
              <div class="price-block">
                <span class="price-ref-caption">Faixa média em oferta (ref. até <span class="old-price-inline">{formatar_moeda(preco_antigo)}</span>)</span>
                <div class="current-price-row">
                  <span class="price-prefix">~</span>
                  <span class="price-main">{preco_fmt}</span>
                  <span class="discount-tag">até {desconto_pct}% menor</span>
                </div>
                <div class="installment-text">Costuma parcelar em até {num_parcelas}x sem juros nas lojas</div>
              </div>
              <div class="shipping-row">
                <span>✔ Elegível a Frete Grátis</span>
                <span class="full-tag">⚡ FULL / Prime</span>
              </div>
              <div class="smart-roi-strip">
                <span>⏱ <strong>-{horas}h</strong>/sem</span>
                <span>💰 Econ. <strong>{economia_fmt}</strong>/mês</span>
              </div>
              <div class="affiliate-buttons">
                <a href="{link_principal}" target="_blank" rel="noopener sponsored" class="btn-main-offer">🔍 Consultar preço de hoje</a>
                <div class="secondary-stores-row">
                  {f'<a href="{p["linkAmazon"]}" target="_blank" rel="noopener sponsored" class="btn-mini-store amz">Amazon</a>' if p.get("linkAmazon") else '<span class="btn-mini-store">-</span>'}
                  {f'<a href="{p["linkMercadoLivre"]}" target="_blank" rel="noopener sponsored" class="btn-mini-store ml">M. Livre</a>' if p.get("linkMercadoLivre") else '<span class="btn-mini-store">-</span>'}
                  {f'<a href="{p["linkShopee"]}" target="_blank" rel="noopener sponsored" class="btn-mini-store shp">Shopee</a>' if p.get("linkShopee") else '<span class="btn-mini-store">-</span>'}
                </div>
              </div>
            </div>
          </article>
        """

    faqs_html = "".join(
        f"""
        <div style="background: var(--surface); padding: 16px; border-radius: 6px; margin-bottom: 10px; border: 1px solid var(--border);">
          <h3 style="font-size: 0.98rem; margin-bottom: 4px; color: var(--text);">❓ {f['pergunta']}</h3>
          <p style="color: var(--text-muted); font-size: 0.88rem;">{f['resposta']}</p>
        </div>
        """
        for f in tema.get("faqs", [])
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{tema['titulo_seo']}</title>
  <meta name="description" content="{tema['meta_desc']}" />
  <meta name="robots" content="index, follow" />
  <link rel="icon" type="image/svg+xml" href="../img/favicon.svg" />
  <link rel="stylesheet" href="../styles.css" />
  <script type="application/ld+json">
{json.dumps(faq_schema, indent=2, ensure_ascii=False)}
  </script>
</head>
<body>
  <header class="hero">
    <div class="container header-top-bar">
      <div class="brand-area">
        <a href="../index.html" style="text-decoration:none;"><span class="brand-logo">CASA SMART</span></a>
        <div>
          <h1>{tema['h1']}</h1>
          <p>{tema['resumo']}</p>
        </div>
      </div>
      <a href="../index.html" class="btn-primary" style="text-decoration:none;">← Abrir Calculadora Completa</a>
    </div>
  </header>

  <main class="container main-content">
    <section class="panel active">
      <div class="results-summary" style="grid-template-columns: 1fr;">
        <div>
          <strong style="color: var(--green); text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.05em;">🏆 Veredito & Recomendação Direta</strong>
          <p style="font-size: 0.98rem; font-weight: 600; margin-top: 4px; color: var(--text);">{tema['veredito_curto']}</p>
        </div>
      </div>

      <h2 style="margin: 20px 0 10px; font-size: 1.15rem;">📊 Comparativo de Retorno, Tempo Livre e Preço Médio</h2>
      <div style="overflow-x: auto; margin-bottom: 24px;">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Modelo Oficial</th>
              <th>Faixa Média</th>
              <th>Tempo Livre</th>
              <th>Economia Mensal</th>
              <th>Checar Preço Hoje</th>
            </tr>
          </thead>
          <tbody>
            {linhas_tabela}
          </tbody>
        </table>
      </div>

      <h2 style="margin: 24px 0 12px; font-size: 1.15rem;">🔥 Modelos Recomendados para Este Perfil</h2>
      <div class="products-grid">
        {cards_html}
      </div>

      <h2 style="margin: 28px 0 12px; font-size: 1.15rem;">💬 Perguntas Frequentes (FAQ)</h2>
      {faqs_html}

      <div style="margin-top: 24px; background: var(--navy-header); color: #fff; padding: 24px; border-radius: 6px; text-align: center;">
        <h3 style="font-size: 1.15rem; margin-bottom: 6px;">Quer simular exatamente em quantos dias o seu Kit se paga?</h3>
        <p style="color: #ccc; font-size: 0.88rem; margin-bottom: 14px;">Teste gratuitamente a Calculadora de Economia Doméstica e descubra o Kit ideal para a sua rotina.</p>
        <a href="../index.html" class="btn-primary" style="text-decoration: none; display: inline-block;">🧭 Simular Meu Kit Ideal Agora</a>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p>Casa Prática & Smart — Participamos do Programa de Associados da Amazon, Mercado Livre e Shopee. Valores exibidos são faixas médias de referência; clique para consultar o preço atualizado nas lojas oficiais.</p>
    </div>
  </footer>
</body>
</html>
"""


def gerar_todas_paginas_seo(produtos, dominio_base="https://casapraticasmart.github.io"):
    GUIAS_DIR.mkdir(exist_ok=True)
    agora_str = datetime.now().strftime("%d/%m/%Y")
    guias_gerados = []

    for tema in TEMAS_COMPARATIVOS_SEO:
        prods_guia = selecionar_produtos_para_guia(produtos, tema)
        html = gerar_html_guia(tema, prods_guia, agora_str)
        arquivo_path = GUIAS_DIR / f"{tema['slug']}.html"
        arquivo_path.write_text(html, encoding="utf-8")
        guias_gerados.append({
            "slug": tema["slug"],
            "url_relativa": f"guias/{tema['slug']}.html",
            "titulo": tema["titulo_seo"],
            "resumo": tema["resumo"],
            "veredito": tema["veredito_curto"],
            "qtd_produtos": len(prods_guia)
        })

    urls_xml = [f"  <url><loc>{dominio_base}/index.html</loc><priority>1.0</priority></url>"]
    for g in guias_gerados:
        urls_xml.append(
            f"  <url><loc>{dominio_base}/{g['url_relativa']}</loc><priority>0.9</priority></url>"
        )

    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls_xml)
        + "\n</urlset>\n"
    )
    (BASE_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {dominio_base}/sitemap.xml\n"
    (BASE_DIR / "robots.txt").write_text(robots_txt, encoding="utf-8")

    # Gera Feed RSS 2.0 automático (feed.xml) para Pinterest Auto-Publish, Telegram e agregadores
    pub_date = format_datetime(datetime.now(timezone.utc))
    rss_items = []

    for p in produtos:
        nome_esc = html_lib.escape(p.get("nome", "Oferta Casa Inteligente"))
        preco_atual = p.get("precoEstimado", 99)
        preco_antigo = p.get("precoAntigo", int(preco_atual * 1.3))
        econ_mes = p.get("economiaMensalReais", 120)
        horas_sem = p.get("horasEconomizadasSemana", 2.5)
        link_amz = html_lib.escape(p.get("linkAmazon") or f"{dominio_base}/index.html")
        img_url = f"{dominio_base}/{p.get('imagem', 'img/airfryer.svg').lstrip('/')}"
        desc_texto = (
            f"🔥 Faixa média em oferta: ~R$ {preco_atual} (ref. até R$ {preco_antigo}). "
            f"Economiza ~{horas_sem}h/semana e até R$ {econ_mes}/mês no orçamento doméstico. "
            f"{p.get('descricao', '')}"
        )
        desc_esc = html_lib.escape(desc_texto)
        guid_id = html_lib.escape(f"{dominio_base}/#oferta-{p.get('id', 'item')}")
        rss_items.append(
            f"    <item>\n"
            f"      <title>{nome_esc} (~R$ {preco_atual})</title>\n"
            f"      <link>{link_amz}</link>\n"
            f"      <guid isPermaLink=\"false\">{guid_id}</guid>\n"
            f"      <pubDate>{pub_date}</pubDate>\n"
            f"      <description>{desc_esc}</description>\n"
            f"      <enclosure url=\"{html_lib.escape(img_url)}\" type=\"image/svg+xml\" length=\"4096\" />\n"
            f"    </item>"
        )

    for g in guias_gerados:
        titulo_esc = html_lib.escape(g["titulo"])
        url_guia = f"{dominio_base}/{g['url_relativa']}"
        resumo_esc = html_lib.escape(f"{g['resumo']} Veredito: {g['veredito']}")
        rss_items.append(
            f"    <item>\n"
            f"      <title>{titulo_esc}</title>\n"
            f"      <link>{url_guia}</link>\n"
            f"      <guid isPermaLink=\"true\">{url_guia}</guid>\n"
            f"      <pubDate>{pub_date}</pubDate>\n"
            f"      <description>{resumo_esc}</description>\n"
            f"    </item>"
        )

    feed_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        '  <channel>\n'
        '    <title>Casa Prática &amp; Smart — Ofertas e Comparativos</title>\n'
        f'    <link>{dominio_base}/</link>\n'
        '    <description>Curadoria automática de Casa e Cozinha Inteligente, Calculadoras de Economia e Ofertas Verificadas.</description>\n'
        '    <language>pt-br</language>\n'
        f'    <lastBuildDate>{pub_date}</lastBuildDate>\n'
        + "\n".join(rss_items)
        + "\n  </channel>\n</rss>\n"
    )
    (BASE_DIR / "feed.xml").write_text(feed_xml, encoding="utf-8")

    return guias_gerados
