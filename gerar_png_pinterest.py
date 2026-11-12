import struct
import zlib
from pathlib import Path

# Gera imagens PNG reais 600x600 para o Feed RSS do Pinterest (que exige PNG/JPG e nao aceita SVG)
IMG_DIR = Path(__file__).parent / "img"

PALETAS = {
    "airfryer": ((19, 25, 33), (255, 153, 0)),
    "robo-aspirador": ((15, 23, 42), (56, 189, 248)),
    "echo-dot": ((17, 24, 39), (14, 165, 233)),
    "mop-spray": ((6, 78, 59), (16, 185, 129)),
    "panela-pressao": ((30, 41, 59), (245, 158, 11)),
    "smart-plug": ((23, 37, 84), (96, 165, 250)),
    "mini-processador": ((6, 95, 70), (52, 211, 153)),
    "aspirador-vertical": ((127, 29, 29), (248, 113, 113)),
    "potes-hermeticos": ((30, 58, 138), (59, 130, 246)),
    "lampada-smart": ((49, 46, 129), (167, 139, 250)),
    "cafeteira": ((69, 26, 3), (217, 119, 6)),
    "seladora-vacuo": ((20, 83, 45), (74, 222, 128)),
}


def criar_png_card(caminho: Path, cor_topo, cor_destaque, largura=600, altura=600):
    linhas = []
    for y in range(altura):
        row = bytearray([0])  # filtro PNG None
        for x in range(largura):
            # Topo colorido (faixa de 110px) e base branca de estúdio com moldura central
            if y < 110:
                r, g, b = cor_topo
            elif 110 <= y < 118:
                r, g, b = cor_destaque
            elif 490 <= y < 560 and 60 <= x < 540:
                r, g, b = cor_destaque
            elif 150 <= y < 450 and 130 <= x < 470:
                # Silhueta central limpa do produto em destaque
                dist_cx = abs(x - 300)
                dist_cy = abs(y - 300)
                if dist_cx < 110 and dist_cy < 110:
                    if (dist_cx > 95 or dist_cy > 95):
                        r, g, b = cor_destaque
                    else:
                        r, g, b = cor_topo
                else:
                    r, g, b = (248, 250, 252)
            else:
                r, g, b = (255, 255, 255)
            row.extend((r, g, b))
        linhas.append(bytes(row))

    raw_data = b"".join(linhas)

    def chunk(tipo: bytes, dados: bytes) -> bytes:
        return (
            struct.pack(">I", len(dados))
            + tipo
            + dados
            + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", largura, altura, 8, 2, 0, 0, 0)
    idat = zlib.compress(raw_data, level=6)
    png_bytes = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    caminho.write_bytes(png_bytes)


if __name__ == "__main__":
    IMG_DIR.mkdir(exist_ok=True)
    for nome, (c1, c2) in PALETAS.items():
        criar_png_card(IMG_DIR / f"{nome}.png", c1, c2)
    print("12 imagens PNG geradas para o Pinterest RSS!")
