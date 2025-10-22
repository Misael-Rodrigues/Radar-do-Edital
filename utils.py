import datetime, requests

def buscar_editais_pncp():
    ontem = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    url = f"https://pncp.gov.br/api/consulta/v1/contratacoes?data_publicacao_inicio={ontem}"
    r = requests.get(url)
    if r.status_code == 200:
        dados = r.json()
        resultados = []
        for item in dados.get("data", []):
            resultados.append({
                "titulo": item.get("objetoResumo", "Sem título"),
                "orgao": item.get("orgaoNome", "Não informado"),
                "uf": item.get("uf", "ND"),
                "modalidade": item.get("modalidadeNome", "ND"),
                "data_publicacao": item.get("dataPublicacao", ontem),
                "link": item.get("linkPNCP", "#")
            })
        return resultados
    return []

