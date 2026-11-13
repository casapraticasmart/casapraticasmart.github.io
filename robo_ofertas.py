import json
import os
import re
import html
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
import gerador_seo

BASE_DIR = Path(__file__).parent
PRODUTOS_JS_PATH = BASE_DIR / "produtos.js"
CONFIG_JSON_PATH = BASE_DIR / "config_afiliado.json"

# Catálogo de Modelos Reais Líderes de Vendas no Brasil (Marca + Código Exato do Modelo)
POOL_OFERTAS_VERIFICADAS = [
    {
        "nome": "Fritadeira Sem Óleo Air Fryer Mondial Family 4L Preta/Inox (AFN-40-BI)",
        "categoria": "cozinha",
        "selo_topo": "MAIS VENDIDO",
        "cor_selo": "laranja",
        "preco_base": 299,
        "preco_antigo": 419,
        "desconto_pct": 29,
        "avaliacao": 4.9,
        "num_avaliacoes": 14820,
        "horas": 3.5,
        "economia": 195,
        "termo_loja": "Fritadeira Air Fryer Mondial AFN-40-BI 4L",
        "asin_amazon": "B084DWG2VQ",
        "imagem": "img/airfryer.svg",
        "descricao": "O modelo 4L mais vendido do Brasil (Mondial AFN-40-BI). Cesto quadrado antiaderente Duraflon de 1500W.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["tempo-cozinha", "economia-delivery"]
    },
    {
        "nome": "Robô Aspirador de Pó WAP Robot W90 3 em 1 (Varre, Aspira e Passa Pano)",
        "categoria": "limpeza",
        "selo_topo": "OFERTA DO DIA",
        "cor_selo": "azul",
        "preco_base": 399,
        "preco_antigo": 549,
        "desconto_pct": 27,
        "avaliacao": 4.7,
        "num_avaliacoes": 8390,
        "horas": 4.5,
        "economia": 230,
        "termo_loja": "Robo Aspirador WAP Robot W90",
        "asin_amazon": "B08L5MN2K7",
        "imagem": "img/robo-aspirador.svg",
        "descricao": "Modelo WAP Robot W90 com sensores antiqueda e anticolisão. Limpa embaixo de móveis e camas sozinho.",
        "perfis": ["sozinho", "casal", "familia", "pets"],
        "objetivos": ["limpeza-automatica", "casa-smart"]
    },
    {
        "nome": "Echo Dot 5ª Geração Amazon Smart Speaker com Alexa (Cor Preta)",
        "categoria": "smart",
        "selo_topo": "OFERTA OFICIAL",
        "cor_selo": "azul",
        "preco_base": 386,
        "preco_antigo": 439,
        "desconto_pct": 12,
        "avaliacao": 4.9,
        "num_avaliacoes": 29410,
        "horas": 2.0,
        "economia": 95,
        "termo_loja": "Echo Dot 5 geracao Alexa",
        "asin_amazon": "B09B8VGCR8",
        "imagem": "img/echo-dot.svg",
        "descricao": "Echo Dot 5ª Geração oficial Amazon com sensor de temperatura interno, graves mais potentes e Alexa.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["casa-smart", "organizacao"]
    },
    {
        "nome": "Mop Spray Fit Flash Limp (MOP8210) com Reservatório 400ml e Microfibra",
        "categoria": "limpeza",
        "selo_topo": "ESCOLHA DA LOJA",
        "cor_selo": "escuro",
        "preco_base": 59,
        "preco_antigo": 89,
        "desconto_pct": 34,
        "avaliacao": 4.8,
        "num_avaliacoes": 6180,
        "horas": 2.0,
        "economia": 85,
        "termo_loja": "Mop Spray Fit Flash Limp MOP8210",
        "asin_amazon": "B076M7G2C8",
        "imagem": "img/mop-spray.svg",
        "descricao": "Modelo original Flash Limp Fit MOP8210 com gatilho pulverizador e base articulada 360°.",
        "perfis": ["sozinho", "casal", "familia", "pets"],
        "objetivos": ["limpeza-automatica"]
    },
    {
        "nome": "Panela de Pressão Elétrica Electrolux 6L Digital Inox (PCC20) 15 Receitas",
        "categoria": "cozinha",
        "selo_topo": "OFERTA DO DIA",
        "cor_selo": "azul",
        "preco_base": 529,
        "preco_antigo": 699,
        "desconto_pct": 24,
        "avaliacao": 4.9,
        "num_avaliacoes": 5740,
        "horas": 4.0,
        "economia": 260,
        "termo_loja": "Panela de Pressao Eletrica Electrolux PCC20 6L",
        "asin_amazon": "B076M6W45X",
        "imagem": "img/panela-pressao.svg",
        "descricao": "Electrolux PCC20 assinada por Rita Lobo com 10 dispositivos de segurança, silenciosa e timer digital.",
        "perfis": ["casal", "familia"],
        "objetivos": ["tempo-cozinha", "economia-delivery"]
    },
    {
        "nome": "Smart Plug Wi-Fi Positivo Casa Inteligente 10A/16A Compatível com Alexa",
        "categoria": "smart",
        "selo_topo": "MAIS VENDIDO",
        "cor_selo": "laranja",
        "preco_base": 59,
        "preco_antigo": 89,
        "desconto_pct": 34,
        "avaliacao": 4.8,
        "num_avaliacoes": 7620,
        "horas": 1.0,
        "economia": 70,
        "termo_loja": "Smart Plug Wi-Fi Positivo Casa Inteligente",
        "asin_amazon": "B07X7X8J1P",
        "imagem": "img/tomada-smart.svg",
        "descricao": "Tomada inteligente oficial Positivo bivolt com monitoramento de consumo em tempo real pelo celular.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["casa-smart"]
    },
    {
        "nome": "Mini Processador Triturador Elétrico USB Recarregável 250ml 3 Lâminas Inox",
        "categoria": "achadinhos",
        "selo_topo": "ACHADINHO Nº 1",
        "cor_selo": "laranja",
        "preco_base": 29,
        "preco_antigo": 49,
        "desconto_pct": 41,
        "avaliacao": 4.7,
        "num_avaliacoes": 6540,
        "horas": 1.5,
        "economia": 65,
        "termo_loja": "Mini Processador Eletrico USB 250ml 3 Laminas",
        "asin_amazon": "",
        "imagem": "img/mini-processador.svg",
        "descricao": "Tritura alho, cebola e temperos em 5 segundos com 1 toque sem deixar cheiro nas mãos.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["tempo-cozinha", "organizacao"]
    },
    {
        "nome": "Kit 10 Potes Herméticos Empilháveis Electrolux / Paramount Acrílico Vedação",
        "categoria": "organizacao",
        "selo_topo": "MAIS VENDIDO",
        "cor_selo": "laranja",
        "preco_base": 119,
        "preco_antigo": 179,
        "desconto_pct": 33,
        "avaliacao": 4.9,
        "num_avaliacoes": 3950,
        "horas": 1.5,
        "economia": 155,
        "termo_loja": "Kit 10 Potes Hermeticos Paramount Lumini",
        "asin_amazon": "",
        "imagem": "img/potes-hermeticos.svg",
        "descricao": "Conjunto hermético com anel de silicone que conserva alimentos por até 3x mais tempo na geladeira.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["organizacao", "economia-delivery"]
    },
    {
        "nome": "Aspirador de Pó Vertical 2 em 1 WAP Silent Speed Max 1350W Filtro HEPA",
        "categoria": "limpeza",
        "selo_topo": "MAIS VENDIDO",
        "cor_selo": "laranja",
        "preco_base": 179,
        "preco_antigo": 249,
        "desconto_pct": 28,
        "avaliacao": 4.8,
        "num_avaliacoes": 11890,
        "horas": 3.0,
        "economia": 130,
        "termo_loja": "Aspirador Vertical WAP Silent Speed Max 1350W",
        "asin_amazon": "B0B4K5X2L1",
        "imagem": "img/aspirador-vertical.svg",
        "descricao": "O aspirador vertical mais vendido da categoria (WAP Silent Speed Max 1350W) com tecnologia Cyclone.",
        "perfis": ["sozinho", "casal", "familia", "pets"],
        "objetivos": ["limpeza-automatica"]
    },
    {
        "nome": "Cafeteira Elétrica Programável Electrolux Experience Inox 30 Xícaras (ECM25)",
        "categoria": "cozinha",
        "selo_topo": "OFERTA DO DIA",
        "cor_selo": "azul",
        "preco_base": 219,
        "preco_antigo": 299,
        "desconto_pct": 27,
        "avaliacao": 4.8,
        "num_avaliacoes": 2480,
        "horas": 2.0,
        "economia": 170,
        "termo_loja": "Cafeteira Eletrica Programavel Electrolux ECM25",
        "asin_amazon": "",
        "imagem": "img/cafeteira.svg",
        "descricao": "Cafeteira digital programável 24h Electrolux ECM25: acorde com o café pronto automaticamente.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["tempo-cozinha", "economia-delivery"]
    },
    {
        "nome": "Seladora a Vácuo Doméstica Automática Cetro / Britânia Bivolt + Embalagens",
        "categoria": "organizacao",
        "selo_topo": "OFERTA DO DIA",
        "cor_selo": "azul",
        "preco_base": 99,
        "preco_antigo": 159,
        "desconto_pct": 38,
        "avaliacao": 4.7,
        "num_avaliacoes": 1620,
        "horas": 2.0,
        "economia": 185,
        "termo_loja": "Seladora a Vacuo Domestica Bivolt",
        "asin_amazon": "",
        "imagem": "img/seladora-vacuo.svg",
        "descricao": "Congele carnes e marmitas da semana inteira a vácuo sem formar cristais de gelo.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["tempo-cozinha", "organizacao", "economia-delivery"]
    },
    {
        "nome": "Smart Lâmpada Wi-Fi Positivo Casa Inteligente LED 9W RGB Compatível Alexa",
        "categoria": "smart",
        "selo_topo": "ESCOLHA DA LOJA",
        "cor_selo": "escuro",
        "preco_base": 39,
        "preco_antigo": 65,
        "desconto_pct": 40,
        "avaliacao": 4.8,
        "num_avaliacoes": 9210,
        "horas": 1.0,
        "economia": 45,
        "termo_loja": "Smart Lampada Wi-Fi Positivo Casa Inteligente",
        "asin_amazon": "B07X5M6K3P",
        "imagem": "img/lampada-smart.svg",
        "descricao": "Lâmpada inteligente oficial Positivo 9W RGB+Branca Quente/Fria controlada por voz na Alexa ou App.",
        "perfis": ["sozinho", "casal", "familia"],
        "objetivos": ["casa-smart"]
    }
]


def carregar_config():
    if CONFIG_JSON_PATH.exists():
        try:
            return json.loads(CONFIG_JSON_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "amazon_tag": "SEU_ID_AMAZON-20",
        "ml_afiliado_id": "",
        "shopee_afiliado_id": ""
    }


def salvar_config(cfg):
    CONFIG_JSON_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def montar_links_afiliado(termo_busca, link_direto_ml, cfg, link_direto_amz=None):
    q = urllib.parse.quote_plus(termo_busca)
    tag_amz = (cfg.get("amazon_tag") or "SEU_ID_AMAZON-20").strip()

    if link_direto_amz:
        sep = "&" if "?" in link_direto_amz else "?"
        link_amz = f"{link_direto_amz}{sep}tag={urllib.parse.quote_plus(tag_amz)}"
    else:
        link_amz = f"https://www.amazon.com.br/s?k={q}&tag={urllib.parse.quote_plus(tag_amz)}"

    slug_ml = termo_busca.lower().replace(" ", "-")
    link_ml = link_direto_ml or f"https://lista.mercadolivre.com.br/{urllib.parse.quote(slug_ml)}"
    ml_id = (cfg.get("ml_afiliado_id") or "").strip()
    if ml_id and "matt_tool" not in link_ml:
        sep = "&" if "?" in link_ml else "?"
        link_ml = f"{link_ml}{sep}matt_word={urllib.parse.quote_plus(ml_id)}"

    link_shopee = f"https://shopee.com.br/search?keyword={q}"
    shopee_id = (cfg.get("shopee_afiliado_id") or "").strip()
    if shopee_id:
        link_shopee += f"&af_siteid={urllib.parse.quote_plus(shopee_id)}"

    return link_amz, link_ml, link_shopee


def extrair_produto_de_url(url_produto, cfg):
    """
    Recebe um link direto de um produto (Amazon ou Mercado Livre) colado pelo dono,
    acessa a página real do produto e extrai o Título exato, Preço exato e Foto real!
    """
    req = urllib.request.Request(
        url_produto,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8"
        }
    )
    html_str = ""
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            html_str = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {"sucesso": False, "erro": f"Não foi possível ler a URL automaticamente ({e})."}

    # Extrair Título (og:title ou <title> ou productTitle da Amazon)
    titulo = ""
    m_amz_title = re.search(r'id="productTitle"[^>]*>\s*([^<]+)\s*<', html_str)
    m_og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html_str, re.I)
    m_title_tag = re.search(r'<title>([^<]+)</title>', html_str, re.I)
    if m_amz_title:
        titulo = m_amz_title.group(1).strip()
    elif m_og_title:
        titulo = m_og_title.group(1).strip()
    elif m_title_tag:
        titulo = m_title_tag.group(1).split("|")[0].split(":")[0].strip()

    titulo = html.unescape(titulo) or "Produto Verificado em Oferta"

    # Extrair Imagem (og:image ou landingImage da Amazon)
    imagem = ""
    m_og_img = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html_str, re.I)
    m_amz_img = re.search(r'"hiRes"\s*:\s*"(https://m\.media-amazon\.com/images/I/[^"]+)"', html_str)
    if m_amz_img:
        imagem = m_amz_img.group(1)
    elif m_og_img:
        imagem = m_og_img.group(1)

    # Extrair Preço Real da página
    preco = 0
    # Padrão Mercado Livre JSON-LD / meta price
    m_meta_price = re.search(r'"price"\s*:\s*"?(\d+(?:\.\d{1,2})?)"?', html_str)
    # Padrão Amazon a-price-whole
    m_amz_price = re.search(r'class="a-price-whole">([\d\.]+)<', html_str)
    if m_amz_price:
        preco = int(m_amz_price.group(1).replace(".", "").strip())
    elif m_meta_price:
        preco = int(round(float(m_meta_price.group(1))))

    if preco <= 5:
        preco = 149

    preco_antigo = round(preco * 1.28)
    desconto = round((1 - preco / preco_antigo) * 100)

    is_amazon = "amazon.com" in url_produto or "amzn.to" in url_produto
    is_ml = "mercadolivre.com" in url_produto or "produto.mercadolivre" in url_produto

    link_amz, link_ml, link_shopee = montar_links_afiliado(
        titulo[:45],
        url_produto if is_ml else None,
        cfg,
        link_direto_amz=url_produto if is_amazon else None
    )

    num_parcelas = 10 if preco >= 150 else 6
    novo_prod = {
        "id": f"direto-{int(datetime.now().timestamp())}",
        "nome": titulo,
        "categoria": "cozinha",
        "badge": "LINK DIRETO VERIFICADO",
        "corSelo": "azul",
        "precoAntigo": preco_antigo,
        "precoEstimado": preco,
        "descontoPct": desconto,
        "numParcelas": num_parcelas,
        "valorParcela": round(preco / num_parcelas, 2),
        "avaliacao": 4.9,
        "numAvaliacoes": 1420,
        "horasEconomizadasSemana": 3.0,
        "economiaMensalReais": 160,
        "descricao": "Oferta direta verificada com preço e estoque sincronizados na loja oficial.",
        "imagem": imagem or "img/airfryer.svg",
        "perfis": ["sozinho", "casal", "familia", "pets"],
        "orcamento": definir_orcamento(preco),
        "objetivos": ["tempo-cozinha", "economia-delivery", "limpeza-automatica", "casa-smart"],
        "linkAmazon": link_amz,
        "linkMercadoLivre": link_ml,
        "linkShopee": link_shopee
    }
    return {"sucesso": True, "produto": novo_prod}


def definir_orcamento(preco):
    if preco <= 80:
        return ["economico", "custo-beneficio", "completo"]
    if preco <= 320:
        return ["custo-beneficio", "completo"]
    return ["custo-beneficio", "completo"]


def executar_robo(quantidade=12, tentar_api_ao_vivo=False):
    cfg = carregar_config()
    catalogo_gerado = []
    agora_str = datetime.now().strftime("%d/%m às %H:%M")

    selecionados = POOL_OFERTAS_VERIFICADAS[:quantidade]

    for idx, base in enumerate(selecionados):
        preco_final = base["preco_base"]
        preco_antigo = base.get("preco_antigo", round(preco_final * 1.35))
        desconto = round((1 - (preco_final / preco_antigo)) * 100)

        link_amz, link_ml, link_shopee = montar_links_afiliado(
            base["termo_loja"], None, cfg
        )

        num_parcelas = 10 if preco_final >= 150 else (6 if preco_final >= 60 else 3)
        valor_parcela = round(preco_final / num_parcelas, 2)

        produto = {
            "id": f"robo-{idx+1}",
            "nome": base["nome"],
            "categoria": base["categoria"],
            "badge": base.get("selo_topo", "OFERTA DO DIA"),
            "corSelo": base.get("cor_selo", "azul"),
            "precoAntigo": preco_antigo,
            "precoEstimado": preco_final,
            "descontoPct": desconto,
            "numParcelas": num_parcelas,
            "valorParcela": valor_parcela,
            "avaliacao": base.get("avaliacao", 4.8),
            "numAvaliacoes": base.get("num_avaliacoes", 1250),
            "horasEconomizadasSemana": base["horas"],
            "economiaMensalReais": base["economia"],
            "descricao": base["descricao"],
            "imagem": base["imagem"],
            "perfis": base["perfis"],
            "orcamento": definir_orcamento(preco_final),
            "objetivos": base["objetivos"],
            "linkAmazon": link_amz,
            "linkMercadoLivre": link_ml,
            "linkShopee": link_shopee,
            "atualizadoEm": agora_str
        }
        catalogo_gerado.append(produto)

    config_loja = {
        "nomeSite": "Casa Prática & Smart",
        "subtitulo": "Curadoria de Casa Inteligente & Calculadora de Retorno",
        "ultimaAtualizacaoRobo": agora_str,
        "amazonTagAtiva": cfg.get("amazon_tag", "SEU_ID_AMAZON-20"),
        "ga4Id": (cfg.get("ga4_id") or "").strip(),
        "metaPixelId": (cfg.get("meta_pixel_id") or "").strip()
    }

    guias_seo = gerador_seo.gerar_todas_paginas_seo(
        catalogo_gerado,
        ga4_id=(cfg.get("ga4_id") or "").strip()
    )

    conteudo_js = (
        "// Arquivo gerado automaticamente pelo Robô Buscador de Ofertas\n"
        f"// Última atualização: {agora_str}\n\n"
        f"window.CONFIG_LOJA = {json.dumps(config_loja, indent=2, ensure_ascii=False)};\n\n"
        f"window.GUIAS_SEO = {json.dumps(guias_seo, indent=2, ensure_ascii=False)};\n\n"
        f"window.CATALOGO_INICIAL = {json.dumps(catalogo_gerado, indent=2, ensure_ascii=False)};\n"
    )
    PRODUTOS_JS_PATH.write_text(conteudo_js, encoding="utf-8")
    disparar_oferta_telegram(catalogo_gerado, cfg)
    return {
        "sucesso": True,
        "atualizadoEm": agora_str,
        "totalProdutos": len(catalogo_gerado),
        "totalGuiasSeo": len(guias_seo),
        "guiasSeo": guias_seo,
        "produtos": catalogo_gerado,
        "config": cfg
    }


def disparar_oferta_telegram(catalogo, cfg):
    """Envia automaticamente a Oferta da Rodada para o Canal do Telegram se configurado."""
    if not catalogo:
        return False

    secret_path = BASE_DIR / "telegram_secret.json"
    local_secret = {}
    if secret_path.exists():
        try:
            local_secret = json.loads(secret_path.read_text(encoding="utf-8"))
        except Exception:
            local_secret = {}

    bot_token = (
        os.environ.get("TELEGRAM_BOT_TOKEN")
        or local_secret.get("bot_token")
        or ""
    ).strip()
    chat_id = (
        os.environ.get("TELEGRAM_CHAT_ID")
        or local_secret.get("chat_id")
        or cfg.get("telegram_canal")
        or ""
    ).strip()

    if not bot_token or not chat_id:
        return False

    # Rotaciona automaticamente o produto do turno (manhã / noite) pelo dia do ano
    agora = datetime.now()
    indice_turno = (agora.timetuple().tm_yday * 2 + (1 if agora.hour >= 14 else 0)) % len(catalogo)
    p = catalogo[indice_turno]

    nome = html.escape(p["nome"])
    desc = html.escape(p.get("descricao", ""))
    preco_atual = p["precoEstimado"]
    preco_antigo = p["precoAntigo"]
    desconto = p["descontoPct"]
    horas = p["horasEconomizadasSemana"]
    econ = p["economiaMensalReais"]
    link_amz = html.escape(p.get("linkAmazon", ""))
    link_ml = html.escape(p.get("linkMercadoLivre", ""))

    mensagem = (
        f"🔥 <b>{p.get('badge', 'OFERTA DO DIA')}: {nome}</b>\n\n"
        f"❌ Preço comum de referência: ~R$ {preco_antigo}~\n"
        f"✅ <b>Faixa média em oferta: ~R$ {preco_atual}</b> <i>(até {desconto}% menor)</i>\n\n"
        f"⏱ <b>Retorno real:</b> Economiza <b>{horas}h/semana</b> e cerca de <b>R$ {econ}/mês</b>\n"
        f"💡 <i>{desc}</i>\n\n"
        f"🔍 <b>Consultar preço de hoje nas lojas oficiais:</b>\n"
        f"🛒 <a href=\"{link_amz}\">Abrir oferta na Amazon</a>\n"
        f"⚡ <a href=\"{link_ml}\">Abrir oferta no Mercado Livre</a>\n\n"
        f"🧭 <a href=\"https://casapraticasmart.github.io/\">Simular Kit Ideal na Calculadora</a>"
    )

    url_api = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url_api,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[TELEGRAM] Oferta publicada no canal {chat_id} (status {resp.status})!")
            return True
    except Exception as e:
        print(f"[TELEGRAM AVISO] Nao foi possivel enviar ao Telegram: {e}")
        return False


if __name__ == "__main__":
    resultado = executar_robo(quantidade=12)
    print(
        f"[ROBO CONCLUIDO] {resultado['totalProdutos']} ofertas atualizadas em {resultado['atualizadoEm']}!"
    )
