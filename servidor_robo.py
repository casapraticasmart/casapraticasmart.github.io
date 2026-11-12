import http.server
import json
import socketserver
from pathlib import Path
import robo_ofertas

PORT = 8090
BASE_DIR = Path(__file__).parent


class RoboHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def _enviar_json(self, dados, status=200):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path.startswith("/api/status-robo"):
            cfg = robo_ofertas.carregar_config()
            self._enviar_json({"ativo": True, "config": cfg})
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/rodar-robo"):
            tamanho = int(self.headers.get("Content-Length", 0))
            body_raw = self.rfile.read(tamanho).decode("utf-8") if tamanho > 0 else "{}"
            try:
                payload = json.loads(body_raw)
            except Exception:
                payload = {}

            cfg = robo_ofertas.carregar_config()
            if "amazon_tag" in payload and payload["amazon_tag"]:
                cfg["amazon_tag"] = payload["amazon_tag"].strip()
            if "ml_afiliado_id" in payload:
                cfg["ml_afiliado_id"] = payload["ml_afiliado_id"].strip()
            if "shopee_afiliado_id" in payload:
                cfg["shopee_afiliado_id"] = payload["shopee_afiliado_id"].strip()
            robo_ofertas.salvar_config(cfg)

            qtd = int(payload.get("quantidade", 12))
            resultado = robo_ofertas.executar_robo(quantidade=qtd, tentar_api_ao_vivo=True)
            self._enviar_json(resultado)
            return

        if self.path.startswith("/api/importar-url"):
            tamanho = int(self.headers.get("Content-Length", 0))
            body_raw = self.rfile.read(tamanho).decode("utf-8") if tamanho > 0 else "{}"
            try:
                payload = json.loads(body_raw)
            except Exception:
                payload = {}
            url_alvo = (payload.get("url") or "").strip()
            cfg = robo_ofertas.carregar_config()
            res = robo_ofertas.extrair_produto_de_url(url_alvo, cfg)
            self._enviar_json(res)
            return

        self._enviar_json({"erro": "Rota nao encontrada"}, status=404)


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), RoboHandler) as httpd:
        print(f"Servidor + Robo de Ofertas rodando em http://localhost:{PORT}")
        httpd.serve_forever()
