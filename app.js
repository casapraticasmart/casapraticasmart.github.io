(function () {
  const STORAGE_KEY = "casa_pratica_catalogo_v3_models";
  const TAG_STORAGE_KEY = "casa_pratica_amazon_tag";

  let produtos = carregarProdutos();
  let categoriaAtiva = "todas";
  let termoBusca = "";

  function carregarProdutos() {
    try {
      const salvo = localStorage.getItem(STORAGE_KEY);
      if (salvo) {
        const parsed = JSON.parse(salvo);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.warn("Erro ao ler localStorage:", e);
    }
    return [...(window.CATALOGO_INICIAL || [])];
  }

  function salvarProdutos() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(produtos));
  }

  function formatarMoeda(valor) {
    return Number(valor || 0).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0
    });
  }

  function formatarLinkAmazon(url) {
    if (!url) return "";
    const tagSalva = localStorage.getItem(TAG_STORAGE_KEY) || "";
    if (!tagSalva) return url;
    try {
      const u = new URL(url);
      u.searchParams.set("tag", tagSalva.trim());
      return u.toString();
    } catch {
      return url;
    }
  }

  function criarCardProdutoHTML(p) {
    const linkAmz = formatarLinkAmazon(p.linkAmazon);
    const linkPrincipal = linkAmz || p.linkMercadoLivre || p.linkShopee || "#";
    const precoAtual = Number(p.precoEstimado || 99);
    const precoAntigo = Number(p.precoAntigo || Math.round(precoAtual * 1.32));
    const descontoPct = p.descontoPct || Math.round((1 - precoAtual / precoAntigo) * 100);
    const numParcelas = p.numParcelas || (precoAtual >= 150 ? 10 : 6);
    const valorParcela = (precoAtual / numParcelas).toFixed(2).replace(".", ",");
    const avaliacao = p.avaliacao || "4.9";
    const numAvaliacoes = Number(p.numAvaliacoes || 1840).toLocaleString("pt-BR");
    const corSelo = p.corSelo || "azul";

    return `
      <article class="product-card">
        <a href="${linkPrincipal}" target="_blank" rel="noopener sponsored" class="product-img-wrap" title="${p.nome}">
          <img class="product-img" src="${p.imagem || 'img/airfryer.svg'}" alt="${p.nome}" loading="lazy" />
        </a>
        <div class="product-body">
          <div class="retail-badge-row">
            <span class="retail-badge ${corSelo}">${p.badge || "OFERTA DO DIA"}</span>
          </div>
          <h3 class="product-title" title="${p.nome}">${p.nome}</h3>
          <div class="rating-row">
            <span class="rating-score">${avaliacao}</span>
            <span class="rating-stars">★★★★★</span>
            <span>(${numAvaliacoes})</span>
          </div>
          <div class="price-block">
            <span class="price-ref-caption">Faixa média em oferta (ref. até <span class="old-price-inline">${formatarMoeda(precoAntigo)}</span>)</span>
            <div class="current-price-row">
              <span class="price-prefix">~</span>
              <span class="price-main">${formatarMoeda(precoAtual)}</span>
              <span class="discount-tag">até ${descontoPct}% menor</span>
            </div>
            <div class="installment-text">Costuma parcelar em até ${numParcelas}x sem juros nas lojas</div>
          </div>
          <div class="shipping-row">
            <span>✔ Elegível a Frete Grátis</span>
            <span class="full-tag">⚡ FULL / Prime</span>
          </div>
          <div class="smart-roi-strip">
            <span>⏱ <strong>-${p.horasEconomizadasSemana || 2}h</strong>/sem</span>
            <span>💰 Econ. <strong>${formatarMoeda(p.economiaMensalReais || 100)}</strong>/mês</span>
          </div>
          <div class="affiliate-buttons">
            <a href="${linkPrincipal}" target="_blank" rel="noopener sponsored" class="btn-main-offer">🔍 Consultar preço de hoje</a>
            <div class="secondary-stores-row">
              ${linkAmz ? `<a href="${linkAmz}" target="_blank" rel="noopener sponsored" class="btn-mini-store amz">Amazon</a>` : `<span class="btn-mini-store">-</span>`}
              ${p.linkMercadoLivre ? `<a href="${p.linkMercadoLivre}" target="_blank" rel="noopener sponsored" class="btn-mini-store ml">M. Livre</a>` : `<span class="btn-mini-store">-</span>`}
              ${p.linkShopee ? `<a href="${p.linkShopee}" target="_blank" rel="noopener sponsored" class="btn-mini-store shp">Shopee</a>` : `<span class="btn-mini-store">-</span>`}
            </div>
          </div>
        </div>
      </article>
    `;
  }

  // =========================================================================
  // 1. PLANEJADOR / QUIZ PERSONALIZADO
  // =========================================================================
  function atualizarPlanejador() {
    const perfil = document.getElementById("quiz-perfil").value;
    const objetivo = document.getElementById("quiz-objetivo").value;
    const orcamento = document.getElementById("quiz-orcamento").value;

    let recomendados = produtos.filter((p) => {
      const matchPerfil = !p.perfis || p.perfis.includes(perfil) || perfil === "todos";
      const matchObjetivo = !p.objetivos || p.objetivos.includes(objetivo) || objetivo === "todos";
      const matchOrcamento = !p.orcamento || p.orcamento.includes(orcamento) || orcamento === "todos";
      return matchPerfil && matchObjetivo && matchOrcamento;
    });

    // Se o filtro ficar muito restrito, relaxa o critério de orçamento para sempre mostrar boas opções
    if (recomendados.length === 0) {
      recomendados = produtos.filter((p) => {
        const matchObjetivo = !p.objetivos || p.objetivos.includes(objetivo) || objetivo === "todos";
        return matchObjetivo;
      });
    }
    if (recomendados.length === 0) {
      recomendados = produtos.slice(0, 4);
    }

    const totalInvestimento = recomendados.reduce((acc, p) => acc + Number(p.precoEstimado || 0), 0);
    const totalHorasSemana = recomendados.reduce((acc, p) => acc + Number(p.horasEconomizadasSemana || 0), 0);
    const totalEconomiaMes = recomendados.reduce((acc, p) => acc + Number(p.economiaMensalReais || 0), 0);
    const mesesPayback = totalEconomiaMes > 0 ? Math.max(0.5, (totalInvestimento / totalEconomiaMes)).toFixed(1) : "1.5";

    document.getElementById("res-horas").textContent = `${totalHorasSemana.toFixed(1)}h / sem`;
    document.getElementById("res-economia").textContent = `${formatarMoeda(totalEconomiaMes)} / mês`;
    document.getElementById("res-investimento").textContent = formatarMoeda(totalInvestimento);
    document.getElementById("res-payback").textContent = `~${mesesPayback} meses`;

    const container = document.getElementById("quiz-results-grid");
    container.innerHTML = recomendados.map(criarCardProdutoHTML).join("");
  }

  // =========================================================================
  // 2. CALCULADORA DELIVERY & TEMPO VS. COZINHA PRÁTICA
  // =========================================================================
  function atualizarCalculadoraROI() {
    const pedidosSemana = Number(document.getElementById("calc-pedidos").value || 0);
    const ticketMedio = Number(document.getElementById("calc-ticket").value || 0);
    const horasFaxinaSemana = Number(document.getElementById("calc-faxina").value || 0);

    document.getElementById("val-pedidos").textContent = `${pedidosSemana}x por semana`;
    document.getElementById("val-ticket").textContent = formatarMoeda(ticketMedio);
    document.getElementById("val-faxina").textContent = `${horasFaxinaSemana}h por semana`;

    const gastoDeliveryMes = pedidosSemana * ticketMedio * 4.3;
    // Considerando que ter itens práticos reduz 60% dos pedidos por cansaço
    const economiaPotencialMes = Math.round(gastoDeliveryMes * 0.6);
    const economiaAnual = economiaPotencialMes * 12;
    const horasLivresAno = Math.round(horasFaxinaSemana * 0.55 * 52);

    document.getElementById("roi-gasto-atual").textContent = formatarMoeda(gastoDeliveryMes);
    document.getElementById("roi-economia-ano").textContent = formatarMoeda(economiaAnual);
    document.getElementById("roi-horas-ano").textContent = `${horasLivresAno} horas/ano`;

    // Seleciona os produtos campeões de economia de tempo e delivery
    const topROI = [...produtos]
      .sort((a, b) => (b.economiaMensalReais || 0) - (a.economiaMensalReais || 0))
      .slice(0, 4);

    const custoKitTop = topROI.reduce((s, i) => s + Number(i.precoEstimado || 0), 0);
    const diasParaPagar = economiaPotencialMes > 0
      ? Math.max(7, Math.round((custoKitTop / economiaPotencialMes) * 30))
      : 35;

    document.getElementById("roi-dias-payback").textContent = `${diasParaPagar} dias`;
    document.getElementById("calc-results-grid").innerHTML = topROI.map(criarCardProdutoHTML).join("");
  }

  // =========================================================================
  // 3. VITRINE COMPLETA DE ACHADINHOS
  // =========================================================================
  function atualizarVitrine() {
    const filtrados = produtos.filter((p) => {
      const matchCat = categoriaAtiva === "todas" || p.categoria === categoriaAtiva;
      const texto = `${p.nome} ${p.descricao} ${p.badge}`.toLowerCase();
      const matchBusca = !termoBusca || texto.includes(termoBusca.toLowerCase());
      return matchCat && matchBusca;
    });

    const grid = document.getElementById("vitrine-grid");
    if (filtrados.length === 0) {
      grid.innerHTML = `<p style="color: var(--text-muted); grid-column: 1/-1; text-align:center; padding: 32px;">Nenhum produto encontrado para esse filtro.</p>`;
      return;
    }
    grid.innerHTML = filtrados.map(criarCardProdutoHTML).join("");
  }

  // =========================================================================
  // 4. PAINEL DO DONO (GERENCIADOR VISUAL SEM PROGRAMAR)
  // =========================================================================
  function atualizarTabelaAdmin() {
    const tbody = document.getElementById("admin-tbody");
    const countEl = document.getElementById("count-produtos");
    if (countEl) countEl.textContent = produtos.length;
    const tagInput = document.getElementById("admin-amazon-tag");
    if (tagInput) {
      tagInput.value = localStorage.getItem(TAG_STORAGE_KEY) || "";
    }

    tbody.innerHTML = produtos
      .map(
        (p, idx) => `
      <tr>
        <td><strong>${p.nome}</strong></td>
        <td>${p.categoria}</td>
        <td>${formatarMoeda(p.precoEstimado)}</td>
        <td>
          ${p.linkAmazon ? "✅ Amz " : ""}
          ${p.linkMercadoLivre ? "✅ ML " : ""}
          ${p.linkShopee ? "✅ Shopee" : ""}
        </td>
        <td>
          <button class="btn-delete" data-idx="${idx}">Excluir</button>
        </td>
      </tr>
    `
      )
      .join("");

    tbody.querySelectorAll(".btn-delete").forEach((btn) => {
      btn.addEventListener("click", () => {
        const i = Number(btn.getAttribute("data-idx"));
        produtos.splice(i, 1);
        salvarProdutos();
        atualizarTudo();
      });
    });
  }

  function configurarAdmin() {
    const form = document.getElementById("form-novo-produto");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const novo = {
        id: "item-" + Date.now(),
        nome: document.getElementById("adm-nome").value.trim(),
        categoria: document.getElementById("adm-categoria").value,
        badge: document.getElementById("adm-badge").value.trim() || "Destaque",
        precoEstimado: Number(document.getElementById("adm-preco").value || 99),
        horasEconomizadasSemana: Number(document.getElementById("adm-horas").value || 2),
        economiaMensalReais: Number(document.getElementById("adm-economia").value || 100),
        descricao: document.getElementById("adm-descricao").value.trim(),
        imagem: document.getElementById("adm-imagem").value.trim(),
        perfis: ["sozinho", "casal", "familia", "pets"],
        orcamento: ["economico", "custo-beneficio", "completo"],
        objetivos: [document.getElementById("adm-objetivo").value],
        linkAmazon: document.getElementById("adm-amz").value.trim(),
        linkMercadoLivre: document.getElementById("adm-ml").value.trim(),
        linkShopee: document.getElementById("adm-shopee").value.trim()
      };

      produtos.unshift(novo);
      salvarProdutos();
      form.reset();
      atualizarTudo();
      alert("Produto adicionado com sucesso! Ele já aparece na Calculadora e na Vitrine.");
    });

    document.getElementById("btn-salvar-tag").addEventListener("click", () => {
      const val = document.getElementById("admin-amazon-tag").value.trim();
      localStorage.setItem(TAG_STORAGE_KEY, val);
      atualizarTudo();
      alert("Tag da Amazon salva! Todos os botões da Amazon agora incluem sua tag automaticamente.");
    });

    const btnRobo = document.getElementById("btn-disparar-robo");
    if (btnRobo) {
      btnRobo.addEventListener("click", async () => {
        const badge = document.getElementById("status-robo-badge");
        const msg = document.getElementById("msg-retorno-robo");
        const amzTag = document.getElementById("admin-amazon-tag").value.trim();
        const mlTag = (document.getElementById("admin-ml-tag") || {}).value || "";
        const shopeeTag = (document.getElementById("admin-shopee-tag") || {}).value || "";

        if (amzTag) localStorage.setItem(TAG_STORAGE_KEY, amzTag);

        btnRobo.disabled = true;
        btnRobo.textContent = "⏳ Buscando ofertas e preços do dia...";
        if (badge) badge.textContent = "Robô em execução...";

        try {
          const resp = await fetch("/api/rodar-robo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              amazon_tag: amzTag || "SEU_ID_AMAZON-20",
              ml_afiliado_id: mlTag,
              shopee_afiliado_id: shopeeTag,
              quantidade: 12
            })
          });
          if (!resp.ok) throw new Error("Falha ao comunicar com servidor do robô");
          const dados = await resp.json();
          if (dados && Array.isArray(dados.produtos)) {
            produtos = dados.produtos;
            if (Array.isArray(dados.guiasSeo)) {
              window.GUIAS_SEO = dados.guiasSeo;
            }
            salvarProdutos();
            atualizarTudo();
            if (badge) badge.textContent = `Atualizado: ${dados.atualizadoEm}`;
            if (msg) {
              msg.textContent = `✅ Sucesso! ${dados.totalProdutos} produtos e ${dados.totalGuiasSeo || 4} páginas comparativas de SEO foram geradas (${dados.atualizadoEm}).`;
            }
          }
        } catch (err) {
          if (badge) badge.textContent = "Modo Local Offline";
          if (msg) {
            msg.textContent = "⚠️ Para usar o botão ao vivo no navegador, certifique-se de que o servidor_robo.py está rodando (ou clique duas vezes em RODAR_ROBO_DIARIO.bat na pasta).";
          }
        } finally {
          btnRobo.disabled = false;
          btnRobo.textContent = "🚀 Disparar Robô Agora (Atualizar 12 Ofertas do Dia)";
        }
      });
    }

    const btnImportarUrl = document.getElementById("btn-importar-url");
    if (btnImportarUrl) {
      btnImportarUrl.addEventListener("click", async () => {
        const inputUrl = document.getElementById("input-importar-url");
        const msgUrl = document.getElementById("msg-importar-url");
        const urlVal = (inputUrl.value || "").trim();
        if (!urlVal) {
          alert("Cole a URL de um produto da Amazon ou do Mercado Livre primeiro.");
          return;
        }
        btnImportarUrl.disabled = true;
        btnImportarUrl.textContent = "⏳ Lendo página do produto...";
        if (msgUrl) msgUrl.textContent = "Extraindo título, preço real e foto da loja...";

        try {
          const resp = await fetch("/api/importar-url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: urlVal })
          });
          const dados = await resp.json();
          if (dados && dados.sucesso && dados.produto) {
            produtos.unshift(dados.produto);
            salvarProdutos();
            atualizarTudo();
            inputUrl.value = "";
            if (msgUrl) {
              msgUrl.textContent = `✅ Produto capturado com sucesso: "${dados.produto.nome}" (R$ ${dados.produto.precoEstimado}) com link direto!`;
            }
          } else {
            if (msgUrl) msgUrl.textContent = `⚠️ ${dados.erro || "Não foi possível ler os dados dessa URL."}`;
          }
        } catch (e) {
          if (msgUrl) msgUrl.textContent = "⚠️ Erro ao conectar com o extrator local.";
        } finally {
          btnImportarUrl.disabled = false;
          btnImportarUrl.textContent = "⚡ Capturar Produto Exato";
        }
      });
    }

    document.getElementById("btn-exportar-js").addEventListener("click", () => {
      const conteudo = `window.CONFIG_LOJA = ${JSON.stringify(window.CONFIG_LOJA || {}, null, 2)};\n\nwindow.CATALOGO_INICIAL = ${JSON.stringify(produtos, null, 2)};\n`;
      const blob = new Blob([conteudo], { type: "application/javascript;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "produtos.js";
      a.click();
      URL.revokeObjectURL(url);
    });

    document.getElementById("btn-resetar-catalogo").addEventListener("click", () => {
      if (confirm("Deseja restaurar os produtos originais de fábrica?")) {
        localStorage.removeItem(STORAGE_KEY);
        produtos = carregarProdutos();
        atualizarTudo();
      }
    });
  }

  function configurarAbas() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    const panels = document.querySelectorAll(".panel");

    function ativarAba(targetId) {
      tabBtns.forEach((b) => b.classList.toggle("active", b.getAttribute("data-tab") === targetId));
      panels.forEach((p) => p.classList.toggle("active", p.id === targetId));
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        ativarAba(btn.getAttribute("data-tab"));
      });
    });

    const linkAdminFooter = document.getElementById("open-admin-btn");
    if (linkAdminFooter) {
      linkAdminFooter.addEventListener("click", () => {
        ativarAba("tab-admin");
      });
    }
  }

  function atualizarGuiasSeo() {
    const grid = document.getElementById("guias-seo-grid");
    if (!grid) return;
    const lista = window.GUIAS_SEO || [];
    if (lista.length === 0) {
      grid.innerHTML = `<p style="color:var(--text-muted);">Rode o robô no Painel do Dono para gerar as páginas comparativas de SEO.</p>`;
      return;
    }
    grid.innerHTML = lista
      .map(
        (g) => `
      <article class="field-group" style="display:flex; flex-direction:column; justify-content:space-between; background:#ffffff;">
        <div>
          <span class="tag-economy" style="display:inline-block; margin-bottom:8px;">🔍 Página Indexável Google (SEO)</span>
          <h3 style="font-size:1.1rem; margin-bottom:8px;">${g.titulo}</h3>
          <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:12px;">${g.resumo}</p>
          <p style="font-size:0.82rem; background:var(--surface-alt); padding:10px; border-radius:8px; margin-bottom:14px;"><strong>Veredito:</strong> ${g.veredito}</p>
        </div>
        <a href="${g.url_relativa}" class="btn-primary" style="text-decoration:none; text-align:center; display:block;">📄 Abrir Página Comparativa Completa →</a>
      </article>
    `
      )
      .join("");
  }

  function atualizarTudo() {
    atualizarPlanejador();
    atualizarCalculadoraROI();
    atualizarVitrine();
    atualizarGuiasSeo();
    atualizarTabelaAdmin();
  }

  document.addEventListener("DOMContentLoaded", () => {
    configurarAbas();
    configurarAdmin();

    // Listeners do Planejador
    ["quiz-perfil", "quiz-objetivo", "quiz-orcamento"].forEach((id) => {
      document.getElementById(id).addEventListener("change", atualizarPlanejador);
    });

    // Listeners da Calculadora ROI
    ["calc-pedidos", "calc-ticket", "calc-faxina"].forEach((id) => {
      document.getElementById(id).addEventListener("input", atualizarCalculadoraROI);
    });

    // Listeners da Vitrine
    document.querySelectorAll(".pill-btn").forEach((pill) => {
      pill.addEventListener("click", () => {
        document.querySelectorAll(".pill-btn").forEach((p) => p.classList.remove("active"));
        pill.classList.add("active");
        categoriaAtiva = pill.getAttribute("data-cat");
        atualizarVitrine();
      });
    });

    document.getElementById("busca-vitrine").addEventListener("input", (e) => {
      termoBusca = e.target.value;
      atualizarVitrine();
    });

    const btnShareWhats = document.getElementById("btn-share-whats-quiz");
    if (btnShareWhats) {
      btnShareWhats.addEventListener("click", () => {
        const horas = document.getElementById("res-horas").textContent;
        const econ = document.getElementById("res-economia").textContent;
        const payback = document.getElementById("res-payback").textContent;
        const texto = `Olha que legal essa calculadora de Casa & Cozinha Inteligente! Meu kit ideal economiza *${horas}* e *${econ}* (se paga sozinho em ${payback}). Veja os produtos recomendados aqui: ${window.location.href}`;
        window.open(`https://wa.me/?text=${encodeURIComponent(texto)}`, "_blank");
      });
    }

    atualizarTudo();
  });
})();
