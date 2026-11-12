from pathlib import Path

IMG_DIR = Path(__file__).parent / "img"
IMG_DIR.mkdir(exist_ok=True)

SVGS = {
    "airfryer.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="bodyG" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="inox" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#cbd5e1"/>
      <stop offset="50%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#94a3b8"/>
    </linearGradient>
  </defs>
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="268" rx="82" ry="12" fill="#e2e8f0"/>
  <!-- Corpo da Airfryer -->
  <path d="M82,55 C82,36 218,36 218,55 L230,235 C230,255 70,255 70,235 Z" fill="url(#bodyG)"/>
  <!-- Faixa Inox -->
  <rect x="74" y="138" width="152" height="10" fill="url(#inox)"/>
  <!-- Painel Digital Touch -->
  <rect x="112" y="62" width="76" height="48" rx="10" fill="#020617" stroke="#475569" stroke-width="1.5"/>
  <text x="150" y="88" font-family="sans-serif" font-size="18" font-weight="bold" fill="#38bdf8" text-anchor="middle">200°C</text>
  <circle cx="128" cy="100" r="3" fill="#38bdf8"/>
  <circle cx="150" cy="100" r="3" fill="#22c55e"/>
  <circle cx="172" cy="100" r="3" fill="#38bdf8"/>
  <!-- Cesto e Puxador -->
  <path d="M74,148 L226,148 L222,235 C222,250 78,250 78,235 Z" fill="#1e293b" stroke="#334155" stroke-width="1"/>
  <rect x="136" y="155" width="28" height="82" rx="12" fill="url(#inox)"/>
  <rect x="142" y="164" width="16" height="64" rx="6" fill="#0f172a"/>
</svg>""",

    "robo-aspirador.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <defs>
    <radialGradient id="topR" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="65%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </radialGradient>
  </defs>
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="248" rx="102" ry="18" fill="#e2e8f0"/>
  <!-- Escovas laterais -->
  <line x1="65" y1="210" x2="38" y2="230" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <line x1="65" y1="210" x2="45" y2="195" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <line x1="235" y1="210" x2="262" y2="230" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <line x1="235" y1="210" x2="255" y2="195" stroke="#64748b" stroke-width="3" stroke-linecap="round"/>
  <!-- Disco principal 3D -->
  <ellipse cx="150" cy="172" rx="96" ry="74" fill="#0f172a"/>
  <ellipse cx="150" cy="160" rx="96" ry="74" fill="url(#topR)" stroke="#64748b" stroke-width="1.5"/>
  <ellipse cx="150" cy="158" rx="82" ry="62" fill="none" stroke="#334155" stroke-width="1.5"/>
  <!-- Sensor Laser LiDAR -->
  <circle cx="150" cy="138" r="22" fill="#1e293b" stroke="#94a3b8" stroke-width="2"/>
  <circle cx="150" cy="138" r="8" fill="#38bdf8"/>
  <!-- Botão Power LED -->
  <circle cx="150" cy="192" r="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
</svg>""",

    "mini-processador.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="262" rx="68" ry="10" fill="#e2e8f0"/>
  <!-- Copo Acrílico Transparente -->
  <path d="M92,135 L208,135 L198,242 C198,255 102,255 102,242 Z" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="3"/>
  <!-- Lâminas Inox Internas -->
  <rect x="146" y="140" width="8" height="95" rx="3" fill="#94a3b8"/>
  <path d="M150,175 L190,165 L186,182 Z" fill="#64748b"/>
  <path d="M150,205 L110,195 L114,212 Z" fill="#64748b"/>
  <!-- Tampa Motor USB -->
  <path d="M88,135 L212,135 L206,75 C206,58 94,58 94,75 Z" fill="#0f766e"/>
  <rect x="88" y="126" width="124" height="10" fill="#cbd5e1"/>
  <!-- Botão Superior -->
  <rect x="130" y="50" width="40" height="12" rx="6" fill="#14b8a6"/>
  <circle cx="150" cy="98" r="5" fill="#5eead4"/>
</svg>""",

    "mop-spray.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="265" rx="90" ry="10" fill="#e2e8f0"/>
  <!-- Base Microfibra -->
  <polygon points="75,245 225,245 240,262 60,262" fill="#0284c7"/>
  <polygon points="82,238 218,238 225,248 75,248" fill="#e2e8f0" stroke="#94a3b8"/>
  <!-- Haste Alumínio -->
  <line x1="150" y1="30" x2="150" y2="240" stroke="#94a3b8" stroke-width="9" stroke-linecap="round"/>
  <!-- Reservatório de Água -->
  <rect x="134" y="135" width="32" height="72" rx="10" fill="#bae6fd" stroke="#0284c7" stroke-width="2"/>
  <rect x="136" y="158" width="28" height="47" rx="8" fill="#38bdf8" opacity="0.6"/>
  <!-- Gatilho Cabo -->
  <path d="M145,30 L168,30 C175,30 175,55 165,55 L150,55" fill="none" stroke="#0f172a" stroke-width="7" stroke-linecap="round"/>
</svg>""",

    "echo-dot.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <defs>
    <radialGradient id="sphere" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="65%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#090d16"/>
    </radialGradient>
  </defs>
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="252" rx="82" ry="14" fill="#bae6fd"/>
  <!-- Anel Luminoso Alexa Azul -->
  <ellipse cx="150" cy="242" rx="68" ry="12" fill="#00d2ff"/>
  <!-- Esfera Smart Speaker -->
  <circle cx="150" cy="162" r="84" fill="url(#sphere)"/>
  <!-- Botões Superiores -->
  <circle cx="150" cy="96" r="5" fill="#94a3b8" opacity="0.5"/>
  <text x="122" y="102" font-family="sans-serif" font-size="14" fill="#94a3b8">+</text>
  <text x="174" y="102" font-family="sans-serif" font-size="14" fill="#94a3b8">−</text>
</svg>""",

    "potes-hermeticos.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="264" rx="98" ry="11" fill="#e2e8f0"/>
  <!-- Pote Alto Esquerdo -->
  <rect x="64" y="78" width="76" height="178" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
  <rect x="68" y="135" width="68" height="117" rx="5" fill="#fde68a"/>
  <rect x="60" y="66" width="84" height="16" rx="5" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
  <rect x="88" y="70" width="28" height="8" rx="3" fill="#64748b"/>
  <!-- Pote Médio Direito Inferior -->
  <rect x="156" y="168" width="80" height="88" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
  <rect x="160" y="198" width="72" height="54" rx="5" fill="#fca5a5"/>
  <rect x="152" y="156" width="88" height="16" rx="5" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
  <!-- Pote Médio Direito Superior -->
  <rect x="156" y="78" width="80" height="72" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
  <rect x="160" y="108" width="72" height="38" rx="5" fill="#86efac"/>
  <rect x="152" y="66" width="88" height="16" rx="5" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
</svg>""",

    "panela-pressao.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="45%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#64748b"/>
    </linearGradient>
  </defs>
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="265" rx="88" ry="12" fill="#e2e8f0"/>
  <!-- Alças Laterais -->
  <rect x="52" y="115" width="24" height="18" rx="6" fill="#0f172a"/>
  <rect x="224" y="115" width="24" height="18" rx="6" fill="#0f172a"/>
  <!-- Corpo Inox -->
  <rect x="72" y="95" width="156" height="150" rx="8" fill="url(#steel)" stroke="#64748b"/>
  <!-- Base e Tampa Preta -->
  <path d="M72,225 L228,225 L224,255 L76,255 Z" fill="#0f172a"/>
  <path d="M74,95 C74,62 226,62 226,95 Z" fill="#0f172a"/>
  <rect x="130" y="52" width="40" height="16" rx="6" fill="#334155"/>
  <!-- Painel Digital Frontal -->
  <rect x="106" y="128" width="88" height="74" rx="8" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <rect x="122" y="142" width="56" height="24" rx="4" fill="#020617"/>
  <text x="150" y="159" font-family="monospace" font-size="16" font-weight="bold" fill="#ef4444" text-anchor="middle">00:30</text>
  <circle cx="130" cy="182" r="5" fill="#475569"/>
  <circle cx="150" cy="182" r="5" fill="#475569"/>
  <circle cx="170" cy="182" r="5" fill="#475569"/>
</svg>""",

    "tomada-smart.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="255" rx="68" ry="10" fill="#e2e8f0"/>
  <rect x="78" y="88" width="144" height="144" rx="34" fill="#f8fafc" stroke="#cbd5e1" stroke-width="3"/>
  <rect x="92" y="102" width="116" height="116" rx="26" fill="#ffffff" stroke="#e2e8f0" stroke-width="2"/>
  <!-- 3 Pinos Padrão Brasileiro -->
  <circle cx="122" cy="162" r="7" fill="#1e293b"/>
  <circle cx="150" cy="146" r="7" fill="#1e293b"/>
  <circle cx="178" cy="162" r="7" fill="#1e293b"/>
  <!-- LED Wi-Fi Azul -->
  <circle cx="150" cy="196" r="4" fill="#0ea5e9"/>
</svg>""",

    "cafeteira.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="264" rx="82" ry="11" fill="#e2e8f0"/>
  <!-- Corpo Cafeteira -->
  <rect x="82" y="52" width="124" height="202" rx="12" fill="#1e293b"/>
  <rect x="88" y="64" width="112" height="65" rx="6" fill="#334155"/>
  <!-- Jarra de Café -->
  <rect x="96" y="142" width="96" height="92" rx="10" fill="#bae6fd" opacity="0.35" stroke="#94a3b8" stroke-width="2"/>
  <rect x="98" y="178" width="92" height="54" rx="8" fill="#451a03"/>
  <!-- Alça da Jarra -->
  <path d="M192,152 L216,152 L216,216 L192,216" fill="none" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>
  <!-- Visor Digital -->
  <rect x="124" y="84" width="40" height="18" rx="3" fill="#020617"/>
  <text x="144" y="97" font-family="monospace" font-size="12" fill="#22c55e" text-anchor="middle">07:00</text>
</svg>""",

    "aspirador-vertical.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="265" rx="75" ry="10" fill="#e2e8f0"/>
  <!-- Bocal de Piso -->
  <rect x="92" y="242" width="116" height="20" rx="6" fill="#1e293b"/>
  <rect x="100" y="254" width="100" height="5" fill="#dc2626"/>
  <!-- Haste e Motor Portátil -->
  <line x1="150" y1="36" x2="150" y2="244" stroke="#334155" stroke-width="8"/>
  <rect x="132" y="110" width="36" height="86" rx="16" fill="#dc2626"/>
  <rect x="135" y="145" width="30" height="42" rx="8" fill="#cbd5e1" opacity="0.8"/>
  <!-- Alça Ergonômica -->
  <path d="M150,36 C175,36 175,68 150,68" fill="none" stroke="#1e293b" stroke-width="7" stroke-linecap="round"/>
</svg>""",

    "seladora-vacuo.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="230" rx="112" ry="12" fill="#e2e8f0"/>
  <!-- Saquinho a Vácuo -->
  <rect x="85" y="155" width="130" height="90" rx="6" fill="#e0f2fe" opacity="0.6" stroke="#bae6fd" stroke-width="2"/>
  <rect x="108" y="180" width="84" height="48" rx="10" fill="#ef4444" opacity="0.75"/>
  <!-- Máquina Seladora -->
  <rect x="42" y="112" width="216" height="52" rx="14" fill="#1e293b" stroke="#475569" stroke-width="2"/>
  <rect x="52" y="122" width="196" height="12" rx="4" fill="#94a3b8"/>
  <circle cx="222" cy="146" r="6" fill="#22c55e"/>
  <circle cx="202" cy="146" r="6" fill="#38bdf8"/>
</svg>""",

    "lampada-smart.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <defs>
    <radialGradient id="bulbG" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#f0abfc"/>
      <stop offset="50%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </radialGradient>
  </defs>
  <rect width="300" height="300" fill="#ffffff"/>
  <ellipse cx="150" cy="264" rx="55" ry="9" fill="#e2e8f0"/>
  <!-- Rosca E27 -->
  <rect x="128" y="212" width="44" height="38" rx="6" fill="#94a3b8"/>
  <line x1="128" y1="224" x2="172" y2="224" stroke="#64748b" stroke-width="3"/>
  <line x1="128" y1="236" x2="172" y2="236" stroke="#64748b" stroke-width="3"/>
  <path d="M138,250 L162,250 L156,258 L144,258 Z" fill="#1e293b"/>
  <!-- Corpo Branco Wi-Fi -->
  <path d="M112,148 L188,148 L172,214 L128,214 Z" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="2"/>
  <!-- Difusor RGB LED -->
  <circle cx="150" cy="118" r="56" fill="url(#bulbG)"/>
</svg>"""
}

for name, content in SVGS.items():
    (IMG_DIR / name).write_text(content, encoding="utf-8")

print(f"Geradas {len(SVGS)} imagens de estudio em {IMG_DIR}")
