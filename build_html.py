#!/usr/bin/env python3
"""
Monta o HTML final (mangas-do-brasil.html) injetando os dados no template.

Le:   src/template.html  +  src/brmap.json  +  os dicionarios abaixo (variedades, estados).
Gera: mangas-do-brasil.html (na raiz do projeto).

Para alterar variedades ou predominancia por estado, edite os dicionarios
`varieties` e `states` neste arquivo e rode:  python3 build_html.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
mapdata = json.load(open(os.path.join(HERE, "src", "brmap.json"), encoding="utf-8"))

# ---- Variety catalog ----
varieties = [
 {"key":"tommy","nome":"Tommy Atkins","sil":"oval","grad":["#86b23a","#e8731f","#9c1f3a"],
  "origem":"EUA (Flórida), anos 1960","peso":"400–700 g","fibra":"Média","brix":"~16–17°",
  "uso":"In natura · exportação","cor":"#d2552b",
  "desc":"A rainha do mercado. Domina ~80% dos plantios por ser resistente a pragas e ter longa vida de prateleira — não pelo sabor, que é mediano e fibroso."},
 {"key":"palmer","nome":"Palmer","sil":"elong","grad":["#b5283f","#7d1530","#3a0a1c"],
  "origem":"EUA (Flórida)","peso":"500–700 g","fibra":"Baixa / nula","brix":"~21,6°",
  "uso":"In natura · exportação","cor":"#7e1f3c",
  "desc":"Caroço pequeno, polpa rende ~72% do fruto. Ótimo sabor e quase sem fibra. Lidera as exportações brasileiras e ganha espaço no mercado interno."},
 {"key":"espada","nome":"Espada","sil":"long","grad":["#c3d24a","#84a82f","#4f7d1f"],
  "origem":"Filipínica — a mais antiga no Brasil","peso":"200–300 g","fibra":"Alta","brix":"—",
  "uso":"In natura (de chupar)","cor":"#7a9e34",
  "desc":"A clássica manga comprida de base tortinha, casca amarelo-esverdeada. Poliembriônica, rústica e barata; a tradicional 'manga de chupar'."},
 {"key":"rosa","nome":"Rosa","sil":"heart","grad":["#f4c63a","#ef7a3a","#c52b53"],
  "origem":"Pernambuco","peso":"~350 g","fibra":"Média","brix":"Alto",
  "uso":"In natura","cor":"#d63b63",
  "desc":"Formato de coração, casca do amarelo ao rosa-avermelhado, muito aromática. Adaptou-se ao clima quente do Nordeste e Centro-Oeste."},
 {"key":"uba","nome":"Ubá","sil":"small","grad":["#f2c12c","#e8a318","#bf7d12"],
  "origem":"Ubá (MG)","peso":"100–150 g","fibra":"Alta","brix":"Alto",
  "uso":"Suco · indústria","cor":"#e0a01c",
  "desc":"Pequena e fibrosa, mas com polpa excelente. É a principal variedade para produção de suco no Brasil, orgulho da Zona da Mata mineira."},
 {"key":"kent","nome":"Kent","sil":"broad","grad":["#9cc23a","#e0a52a","#b83a35"],
  "origem":"EUA (Flórida)","peso":"500–800 g","fibra":"Muito baixa","brix":"Alto",
  "uso":"Premium · exportação","cor":"#b8902a",
  "desc":"Grande, adocicada e quase sem fibra. Variedade premium de exportação, colhida entre novembro e fevereiro. Mais cara que a Palmer."},
 {"key":"keitt","nome":"Keitt","sil":"keitt","grad":["#9bc24a","#86b23a","#c98a6a"],
  "origem":"EUA (Flórida)","peso":"600–900 g","fibra":"Baixa","brix":"Médio-alto",
  "uso":"Exportação · safra tardia","cor":"#8aa83a",
  "desc":"Grande e de maturação tardia — a casca segue esverdeada mesmo madura. Útil para estender a janela de safra no fim da temporada."},
 {"key":"bourbon","nome":"Bourbon","sil":"beak","grad":["#f0b030","#e8731f","#b52339"],
  "origem":"Brasil","peso":"~300 g","fibra":"Média","brix":"Bom",
  "uso":"In natura","cor":"#e07b22",
  "desc":"Reconhecível pelo biquinho curvo. Forte em São Paulo e no Mato Grosso; pode ser consumida com casca e é rica em fibras."},
 {"key":"haden","nome":"Haden","sil":"haden","grad":["#f2c233","#ef8a2a","#c9343f"],
  "origem":"EUA — introduzida nos anos 1930","peso":"400–600 g","fibra":"Baixa","brix":"~17°",
  "uso":"In natura","cor":"#d77a2c",
  "desc":"Casca amarelo-rosada, polpa sucosa e doce. Tradicional e base genética de muitas variedades modernas, incluindo a Tommy Atkins."},
 {"key":"coquinho","nome":"Coquinho / Ourinho","sil":"small","grad":["#f6d96a","#ecc23a","#d39a1f"],
  "origem":"Cultivar brasileira","peso":"70–150 g","fibra":"Média","brix":"Bom",
  "uso":"Porta-enxerto · in natura","cor":"#cda81f",
  "desc":"Pequenina e amarela-clara. Poliembriônica e rústica, muito usada como porta-enxerto (o 'cavalo' da muda), com nicho próprio em São Paulo."},
 {"key":"maca","nome":"Maçã / Coração","sil":"haden","grad":["#f2cf3a","#ef9a3a","#d23a4a"],
  "origem":"Brasil","peso":"200–350 g","fibra":"Baixa","brix":"Alto",
  "uso":"In natura","cor":"#d9622f",
  "desc":"Arredondada, em formato de coração, casca do amarelo ao vermelho. Polpa firme, doce e com pouca fibra — muito apreciada para consumo fresco."},
 {"key":"mallika","nome":"Mallika","sil":"elong","grad":["#f4b232","#ee8a1f","#c85a1a"],
  "origem":"Índia (Neelum × Dasheri), intro. anos 1990","peso":"300–500 g","fibra":"Nula","brix":"Muito alto",
  "uso":"In natura · gourmet","cor":"#e08a1f",
  "desc":"Híbrida indiana monoembriônica. Polpa alaranjada intensa, sem fibra, aroma marcante e doçura elevada — uma das favoritas de quem busca sabor."},
 {"key":"ataulfo","nome":"Ataúlfo / Mel","sil":"flat","grad":["#f7d54a","#eeb024","#cf8a14"],
  "origem":"México","peso":"150–300 g","fibra":"Nula","brix":"Muito alto",
  "uso":"In natura","cor":"#e0a81c",
  "desc":"Pequena e achatada, casca dourada. Polpa amanteigada, sem fibra e muito doce — a 'manga-mel'. Caroço fino, alto rendimento de polpa."},
 {"key":"vandyke","nome":"Van Dyke","sil":"oval","grad":["#e85d3a","#c5283a","#7d1530"],
  "origem":"EUA (Flórida), anos 1960","peso":"250–400 g","fibra":"Baixa","brix":"Alto",
  "uso":"In natura","cor":"#c5384a",
  "desc":"Casca vermelha vistosa sobre fundo amarelo. Pequena a média, doce e com pouca fibra; usada também como polinizadora em pomares."},
 {"key":"osteen","nome":"Osteen","sil":"elong","grad":["#b0384a","#7d2540","#3f1530"],
  "origem":"EUA (Flórida)","peso":"400–600 g","fibra":"Baixa","brix":"Médio-alto",
  "uso":"In natura · exportação","cor":"#8a3350",
  "desc":"Oval e alongada, casca arroxeada-avermelhada. Pouca fibra e boa conservação; é a manga mais cultivada na Espanha e ganha interesse comercial."},
 {"key":"sensation","nome":"Sensation","sil":"small","grad":["#a02438","#6d1530","#33101f"],
  "origem":"EUA (Flórida)","peso":"200–350 g","fibra":"Baixa","brix":"Alto",
  "uso":"In natura · polinizadora","cor":"#7e2238",
  "desc":"Pequena, casca vermelho-escura a roxa, maturação tardia. Pouca fibra; muito usada como polinizadora ao lado de variedades comerciais."},
 {"key":"itamaraca","nome":"Itamaracá","sil":"small","grad":["#f0cf3a","#e0a82a","#b8841f"],
  "origem":"Pernambuco","peso":"até 200 g","fibra":"Média","brix":"Bom",
  "uso":"In natura (regional)","cor":"#c79a22",
  "desc":"Variedade regional pernambucana, pequena e de casca amarelada. Tradicional em quintais e feiras do litoral nordestino."},
]

# ---- State predominance ----
states = {
 "PE":{"predom":"tommy","vars":["tommy","palmer","kent","keitt","itamaraca"],"tier":"polo","conf":"alta","nota":"Coração do Vale do São Francisco e maior exportador do país."},
 "BA":{"predom":"tommy","vars":["tommy","palmer","kent","keitt","espada","rosa"],"tier":"polo","conf":"alta","nota":"2º maior produtor nacional; Juazeiro lidera a área plantada do Brasil."},
 "SP":{"predom":"palmer","vars":["palmer","tommy","bourbon","haden","maca","coquinho"],"tier":"polo","conf":"alta","nota":"3º produtor; forte mercado interno e ampla diversidade de variedades de mesa."},
 "MG":{"predom":"uba","vars":["uba","tommy","haden","palmer","maca"],"tier":"relevante","conf":"alta","nota":"Zona da Mata é o polo da Ubá para a indústria de suco."},
 "CE":{"predom":"tommy","vars":["tommy","palmer","espada","rosa"],"tier":"relevante","conf":"alta","nota":"Produção irrigada e de sequeiro em expansão."},
 "RN":{"predom":"tommy","vars":["tommy","kent","palmer"],"tier":"relevante","conf":"alta","nota":"Exportação crescente, com destaque para o Vale do Açu."},
 "MT":{"predom":"rosa","vars":["rosa","tommy","palmer","bourbon","kent","keitt"],"tier":"emergente","conf":"estimativa","nota":"Rosa típica de quintal na Baixada Cuiabana; cultivo comercial emergente."},
 "GO":{"predom":"rosa","vars":["rosa","tommy","palmer","espada"],"tier":"emergente","conf":"estimativa","nota":"Consumo regional e produção crescente no Cerrado."},
 "DF":{"predom":"rosa","vars":["rosa","tommy","espada"],"tier":"consumo","conf":"estimativa","nota":"Consumo regional."},
 "MS":{"predom":"espada","vars":["espada","rosa","tommy"],"tier":"consumo","conf":"estimativa","nota":"Consumo regional; quintais e pequenas áreas."},
 "PB":{"predom":"espada","vars":["espada","rosa","tommy"],"tier":"consumo","conf":"estimativa","nota":"Variedades tradicionais de quintal."},
 "PI":{"predom":"espada","vars":["espada","rosa","tommy"],"tier":"consumo","conf":"estimativa","nota":"Variedades tradicionais de quintal."},
 "SE":{"predom":"rosa","vars":["rosa","espada","tommy"],"tier":"consumo","conf":"estimativa","nota":"Consumo regional."},
 "AL":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Variedades tradicionais."},
 "MA":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Variedades tradicionais de quintal."},
 "PA":{"predom":"rosa","vars":["rosa","espada"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "AM":{"predom":"rosa","vars":["rosa","espada"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "AP":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "RR":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "AC":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "RO":{"predom":"espada","vars":["espada","rosa"],"tier":"consumo","conf":"estimativa","nota":"Quintais e feiras locais."},
 "TO":{"predom":"espada","vars":["espada","rosa","tommy"],"tier":"consumo","conf":"estimativa","nota":"Consumo regional."},
 "ES":{"predom":"tommy","vars":["tommy","uba","espada"],"tier":"consumo","conf":"estimativa","nota":"Proximidade com MG traz alguma presença de Ubá."},
 "RJ":{"predom":"espada","vars":["espada","tommy","rosa"],"tier":"consumo","conf":"estimativa","nota":"Consumo abastecido majoritariamente por outros estados."},
 "PR":{"predom":"tommy","vars":["tommy","espada"],"tier":"consumo","conf":"estimativa","nota":"Baixa produção; consumo abastecido pelo Nordeste."},
 "SC":{"predom":"tommy","vars":["tommy","espada"],"tier":"consumo","conf":"estimativa","nota":"Baixa produção; consumo abastecido pelo Nordeste."},
 "RS":{"predom":"tommy","vars":["tommy","espada"],"tier":"consumo","conf":"estimativa","nota":"Baixa produção; consumo abastecido pelo Nordeste."},
}

ufnames = {"AC":"Acre","AL":"Alagoas","AM":"Amazonas","AP":"Amapá","BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão","MG":"Minas Gerais","MS":"Mato Grosso do Sul","MT":"Mato Grosso","PA":"Pará","PB":"Paraíba","PE":"Pernambuco","PI":"Piauí","PR":"Paraná","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RO":"Rondônia","RR":"Roraima","RS":"Rio Grande do Sul","SC":"Santa Catarina","SE":"Sergipe","SP":"São Paulo","TO":"Tocantins"}

payload = {
  "map": mapdata,
  "varieties": varieties,
  "states": states,
  "ufnames": ufnames,
}

TEMPLATE = open(os.path.join(HERE, "src", "template.html"), encoding="utf-8").read()
html = TEMPLATE.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))
out = os.path.join(HERE, "mangas-do-brasil.html")
open(out, "w", encoding="utf-8").write(html)
print(f"OK -> {out} ({len(html)} bytes, {len(varieties)} variedades)")
