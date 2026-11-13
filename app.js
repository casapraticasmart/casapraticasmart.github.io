(function () {
  const STORAGE_KEY = "casa_pratica_catalogo_v4_afiliados";
  const TAG_STORAGE_KEY = "casa_pratica_amazon_tag";

  // Limpa tag placeholder antiga caso estivesse salva no navegador
  if (localStorage.getItem(TAG_STORAGE_KEY) === "SEU_ID_AMAZON-20") {
    localStorage.removeItem(TAG_STORAGE_KEY);
  }

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
      tagInput.value = localStorage.getItem(TAG_STORAGE_KEY) || (window.CONFIG_LOJA && window.CONFIG_LOJA.amazonTagAtiva) || "";
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

    const selProdGerador = document.getElementById("gerador-produto-select");
    const selCanalGerador = document.getElementById("gerador-canal-select");
    const txtOutGerador = document.getElementById("gerador-texto-output");
    const msgCopiarPost = document.getElementById("msg-copiar-post");

    if (selProdGerador && selCanalGerador && txtOutGerador) {
      const regerar = () => {
        txtOutGerador.value = gerarTextoOfertaSocial(selProdGerador.value, selCanalGerador.value);
      };
      selProdGerador.addEventListener("change", regerar);
      selCanalGerador.addEventListener("change", regerar);

      const btnCopiarPost = document.getElementById("btn-copiar-post");
      if (btnCopiarPost) {
        btnCopiarPost.addEventListener("click", () => {
          navigator.clipboard.writeText(txtOutGerador.value);
          if (msgCopiarPost) {
            msgCopiarPost.textContent = "✅ Copiado! Só colar.";
            setTimeout(() => {
              msgCopiarPost.textContent = "";
            }, 3000);
          }
        });
      }

      const btnWhatsPost = document.getElementById("btn-enviar-whats-post");
      if (btnWhatsPost) {
        btnWhatsPost.addEventListener("click", () => {
          window.open(`https://wa.me/?text=${encodeURIComponent(txtOutGerador.value)}`, "_blank");
        });
      }

      const btnSortear = document.getElementById("btn-sortear-oferta");
      if (btnSortear) {
        btnSortear.addEventListener("click", () => {
          if (produtos.length > 0) {
            const rnd = Math.floor(Math.random() * produtos.length);
            selProdGerador.value = String(rnd);
            regerar();
          }
        });
      }
    }
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
    const navAdminBtn = document.getElementById("nav-admin-btn");
    const params = new URLSearchParams(window.location.search);
    const ehLocal = ["localhost", "127.0.0.1"].includes(window.location.hostname) || window.location.protocol === "file:";
    const modoDonoAtivo = ehLocal || params.get("dono") === "1";

    if (modoDonoAtivo) {
      if (navAdminBtn) navAdminBtn.style.display = "";
      if (linkAdminFooter) linkAdminFooter.style.display = "";
      if (params.get("dono") === "1") {
        ativarAba("tab-admin");
      }
    }

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

  function gerarTextoOfertaSocial(indiceOuModo, canal) {
    const urlSite = "https://casapraticasmart.github.io/";
    if (indiceOuModo === "top3") {
      const top3 = produtos.slice(0, 3);
      const blocos = top3.map((p, i) => {
        const link = formatarLinkAmazon(p.linkAmazon) || p.linkMercadoLivre || urlSite;
        const precoAntigo = p.precoAntigo || Math.round((p.precoEstimado || 99) * 1.3);
        return `${i + 1}️⃣ *${p.nome}*\n   ❌ Ref. até ~R$ ${precoAntigo}~ → 🔥 *~R$ ${p.precoEstimado}*\n   ⏱ Economiza ${p.horasEconomizadasSemana || 2}h/sem | 👉 ${link}`;
      });
      return `🔥 *TOP 3 ACHADINHOS DE CASA & COZINHA DO DIA*\nItens que se pagam sozinhos economizando tempo e delivery:\n\n${blocos.join("\n\n")}\n\n🧮 *Simule quanto sua casa economiza por mês:* ${urlSite}`;
    }

    const idx = Number(indiceOuModo) || 0;
    const p = produtos[idx] || produtos[0];
    if (!p) return "";

    const linkAmz = formatarLinkAmazon(p.linkAmazon);
    const linkMl = p.linkMercadoLivre;
    const precoAtual = p.precoEstimado || 99;
    const precoAntigo = p.precoAntigo || Math.round(precoAtual * 1.32);
    const descPct = p.descontoPct || Math.round((1 - precoAtual / precoAntigo) * 100);
    const horas = p.horasEconomizadasSemana || 2;
    const econMes = p.economiaMensalReais || 120;

    if (canal === "pinterest") {
      return `TÍTULO DO PIN:\n${p.nome} Vale a Pena? Veja Quanto Economiza por Mês!\n\nDESCRIÇÃO SEO DO PIN:\n${p.descricao || p.nome}. Faixa média em oferta ~R$ ${precoAtual} (até ${descPct}% menor que R$ ${precoAntigo}). Economiza cerca de ${horas} horas por semana na rotina doméstica e até R$ ${econMes}/mês! Confira o comparativo completo e preço atualizado hoje.\n\nLINK DE DESTINO DO PIN:\n${linkAmz || linkMl || urlSite}\n\n#casainteligente #cozinhapratica #achadinhos #economia #organização`;
    }

    if (canal === "telegram") {
      return `⚡ <b>${p.badge || "OFERTA DO DIA"} — ${p.nome}</b>\n\n📉 Ref. até R$ ${precoAntigo}\n🔥 <b>Faixa em oferta hoje: ~R$ ${precoAtual}</b> (até ${descPct}% OFF)\n\n💡 <b>Por que vale cada centavo:</b>\n• ${p.descricao || "Praticidade diária para quem trabalha fora."}\n• Economiza <b>~${horas}h/semana</b> e até <b>R$ ${econMes}/mês</b>\n\n🛒 <b>Confira o preço ao vivo nas lojas oficiais:</b>\n${linkAmz ? `👉 Amazon: ${linkAmz}\n` : ""}${linkMl ? `👉 Mercado Livre: ${linkMl}\n` : ""}\n🧭 Calculadora completa: ${urlSite}`;
    }

    // Default: WhatsApp
    return `🔥 *${p.badge || "ACHADINHO DO DIA"}: ${p.nome}*\n\n❌ Preço comum: ~R$ ${precoAntigo}~\n✅ *Faixa em oferta hoje: ~R$ ${precoAtual}* _(até ${descPct}% menor)_\n\n⏱ Economiza *${horas}h toda semana* + *R$ ${econMes}/mês* na rotina!\n💬 _${p.descricao || "Ideal para quem trabalha fora e quer praticidade."}_\n\n🔍 *Consultar preço de hoje na loja oficial:*\n${linkAmz ? `🛒 *Amazon:* ${linkAmz}\n` : ""}${linkMl ? `⚡ *Mercado Livre:* ${linkMl}\n` : ""}\n🧮 *Calcule o retorno do seu Kit:* ${urlSite}`;
  }

  function atualizarGeradorPosts() {
    const selProd = document.getElementById("gerador-produto-select");
    const selCanal = document.getElementById("gerador-canal-select");
    const txtOut = document.getElementById("gerador-texto-output");
    if (!selProd || !selCanal || !txtOut) return;

    const valorAtual = selProd.value || "0";
    selProd.innerHTML =
      `<option value="top3">🏆 Resumo: Top 3 Ofertas Campeãs do Dia</option>` +
      produtos
        .map((p, idx) => `<option value="${idx}">📦 ${p.nome} (~R$ ${p.precoEstimado})</option>`)
        .join("");

    if ([...selProd.options].some((o) => o.value === valorAtual)) {
      selProd.value = valorAtual;
    } else {
      selProd.value = "0";
    }

    txtOut.value = gerarTextoOfertaSocial(selProd.value, selCanal.value);
  }

  function atualizarTudo() {
    atualizarPlanejador();
    atualizarCalculadoraROI();
    atualizarVitrine();
    atualizarGuiasSeo();
    atualizarTabelaAdmin();
    atualizarGeradorPosts();
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
        const urlPublica = window.location.origin + window.location.pathname;
        const texto = `Olha que legal essa calculadora de Casa & Cozinha Inteligente! Meu kit ideal economiza *${horas}* e *${econ}* (se paga sozinho em ${payback}). Veja os produtos recomendados aqui: ${urlPublica}`;
        window.open(`https://wa.me/?text=${encodeURIComponent(texto)}`, "_blank");
      });
    }

    atualizarTudo();
    iniciarRastreamentoConversao();
  });

  function iniciarRastreamentoConversao() {
    const cfg = window.CONFIG_LOJA || {};
    const ga4Id = (cfg.ga4Id || "").trim();
    const pixelId = (cfg.metaPixelId || "").trim();

    if (ga4Id) {
      const s = document.createElement("script");
      s.async = true;
      s.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(ga4Id)}`;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", ga4Id);
    }

    if (pixelId) {
      !(function (f, b, e, v, n, t, s) {
        if (f.fbq) return;
        n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
        if (!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = !0;
        n.version = "2.0";
        n.queue = [];
        t = b.createElement(e);
        t.async = !0;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t, s);
      })(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");
      window.fbq("init", pixelId);
      window.fbq("track", "PageView");
    }

    document.addEventListener("click", (e) => {
      const link = e.target.closest("a");
      if (!link) return;
      const isAfiliado = link.classList.contains("btn-main-offer") || link.classList.contains("btn-mini-store");
      const isTelegram = link.getAttribute("data-track") === "telegram-join";

      if (isAfiliado) {
        const loja = link.classList.contains("ml") ? "MercadoLivre" : link.classList.contains("shp") ? "Shopee" : "Amazon";
        if (typeof window.gtag === "function") {
          window.gtag("event", "click_afiliado", { loja, url: link.href });
        }
        if (typeof window.fbq === "function") {
          window.fbq("trackCustom", "ClickAfiliado", { loja });
        }
      } else if (isTelegram) {
        if (typeof window.gtag === "function") {
          window.gtag("event", "join_telegram_click");
        }
        if (typeof window.fbq === "function") {
          window.fbq("track", "Lead", { content_name: "Canal Telegram" });
        }
      }
    });
  }
})();
