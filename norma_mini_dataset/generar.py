import csv, json, re, os
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from contenido import DOCS

OUT = os.environ.get("OUT_DATASET", os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{OUT}/pdf", exist_ok=True)

st = {
 "titulo": ParagraphStyle("t", fontName="Times-Bold", fontSize=14, alignment=TA_CENTER, spaceAfter=6),
 "subtitulo": ParagraphStyle("s", fontName="Times-Bold", fontSize=11, alignment=TA_CENTER, spaceAfter=4, leading=14),
 "encabezado": ParagraphStyle("e", fontName="Times-Bold", fontSize=12, alignment=TA_CENTER, spaceBefore=12, spaceAfter=8),
 "p": ParagraphStyle("p", fontName="Times-Roman", fontSize=11.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=9),
 "cita": ParagraphStyle("c", fontName="Times-Italic", fontSize=10.5, leading=14, alignment=TA_JUSTIFY,
                        leftIndent=1.5*cm, rightIndent=1.5*cm, spaceAfter=9),
}

def build(doc):
    path = f"{OUT}/pdf/{doc['archivo']}"
    pie = doc["pie"]
    def deco(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(2.5*cm, 1.4*cm, pie)
        c.drawRightString(letter[0]-2.5*cm, 1.4*cm, f"Página {d.page}")
        c.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=2.8*cm, rightMargin=2.8*cm,
                          topMargin=2.5*cm, bottomMargin=2.5*cm, title=doc["archivo"])
    story = [Paragraph(t, st[k]) for k, t in doc["bloques"]]
    d.build(story, onFirstPage=deco, onLaterPages=deco)
    return path

for doc in DOCS:
    build(doc)

# ---------- texto por página para anclar citas ----------
def norm(s): return re.sub(r"\s+", " ", s).strip()
paginas = {}
for doc in DOCS:
    with pdfplumber.open(f"{OUT}/pdf/{doc['archivo']}") as pdf:
        txts = []
        for p in pdf.pages:
            t = (p.extract_text() or "").replace(doc["pie"], "")
            t = re.sub(r"Página \d+", "", t)
            txts.append(norm(t))
        paginas[doc["archivo"]] = txts

def pagina(archivo, cita):
    c = norm(cita)
    for i, t in enumerate(paginas[archivo], 1):
        if c in t: return i
    # cita partida entre dos páginas
    for i in range(len(paginas[archivo]) - 1):
        if c in paginas[archivo][i] + " " + paginas[archivo][i+1]: return i + 1
    raise ValueError(f"Cita no encontrada en {archivo}: {cita[:60]}")

# ---------- taxonomía simplificada ----------
TAX = [
 ("T01","Procedimiento > Competencia de la autoridad"),
 ("T02","Procedimiento > Vía de impugnación"),
 ("T03","Procedimiento > Estándar de control judicial"),
 ("T04","Procedimiento > Prueba > Prueba indiciaria"),
 ("T05","Procedimiento > Prueba > Carga de la prueba"),
 ("T06","Análisis económico > Mercado relevante > Definición"),
 ("T07","Análisis económico > Mercado relevante > Dimensión geográfica"),
 ("T08","Análisis económico > Poder sustancial"),
 ("T09","Análisis económico > Barreras a la entrada"),
 ("T10","Análisis económico > Índices de concentración"),
 ("T11","Prácticas monopólicas relativas > Elementos > Objeto o efecto"),
 ("T12","Prácticas monopólicas relativas > Conductas > Exclusividad"),
 ("T13","Prácticas monopólicas relativas > Conductas > Comodato y uso de activos"),
 ("T14","Prácticas monopólicas relativas > Cierre de mercado"),
 ("T15","Prácticas monopólicas relativas > Ganancias en eficiencia"),
 ("T16","Prácticas monopólicas absolutas > Acuerdos entre competidores"),
 ("T17","Concentraciones > Objeto del análisis"),
 ("T18","Concentraciones > Condiciones > Suficiencia y proporcionalidad"),
 ("T19","Concentraciones > Condiciones > Remedios estructurales"),
 ("T20","Concentraciones > Notificación > Umbrales"),
 ("T21","Sanciones > Individualización de la multa"),
 ("T22","Sanciones > Motivación de la multa"),
 ("T23","Amparo > Efectos de la concesión"),
 ("T24","Derechos > Propiedad y competencia"),
]
with open(f"{OUT}/taxonomia.json", "w", encoding="utf-8") as f:
    json.dump([{"id": i, "ruta_tema": r} for i, r in TAX], f, ensure_ascii=False, indent=2)

# ---------- gold de criterios ----------
R1, R2, R3 = (d["archivo"] for d in DOCS)
G = [
 ("C01",R1,"Para determinar el mercado relevante se identifican los bienes que el consumidor considera sustitutos razonables y el área geográfica en que se ofrecen.",
  "Para determinar el mercado relevante, esta Comisión debe identificar los bienes o servicios que el consumidor considera sustitutos razonables","T06","LFCE 58",""),
 ("C02",R1,"La participación de mercado no basta para acreditar poder sustancial; deben analizarse también barreras a la entrada, competidores y acceso a insumos.",
  "La participación de mercado no basta por sí sola para acreditar poder sustancial","T08","LFCE 59",""),
 ("C03",R1,"Una cláusula que condiciona la venta o el suministro a que el cliente no adquiera productos de un competidor actualiza la exclusividad del artículo 56, fracción IV.",
  "Una cláusula de exclusividad impuesta a puntos de venta constituye la conducta prevista en la fracción IV del artículo 56 de la Ley","T12","LFCE 56-IV",""),
 ("C04",R1,"El comodato de equipos condicionado a su uso exclusivo puede tener efectos equivalentes a una exclusividad expresa, aunque el contrato no prohíba literalmente comprar a terceros.",
  "La entrega de equipos en comodato condicionada a su uso exclusivo puede tener efectos equivalentes a una cláusula de exclusividad expresa","T13","LFCE 56-IV",""),
 ("C05",R1,"El derecho de propiedad sobre un activo no autoriza usarlo para cerrar el acceso de competidores a los puntos de venta.",
  "el derecho de propiedad no autoriza el uso de un activo para cerrar el acceso de los competidores a los puntos de venta","T24","",""),
 ("C06",R1,"Para acreditar una práctica monopólica relativa basta que la conducta tenga o pueda tener por objeto o efecto el desplazamiento indebido; no se exige que se haya consumado.",
  "Para acreditar una práctica monopólica relativa no es necesario demostrar que el desplazamiento se consumó","T11","LFCE 54",""),
 ("C07",R1,"La proporción de puntos de venta del mercado sujetos a exclusividad es un indicador relevante del cierre de mercado.",
  "La cobertura de las cláusulas de exclusividad, medida como la proporción de los puntos de venta del mercado relevante sujetos a ellas, es un indicador relevante del cierre del mercado","T14","",""),
 ("C08",R1,"El agente debe probar las ganancias en eficiencia, que deben ser verificables, específicas de la conducta y trasladarse al consumidor.",
  "Corresponde al agente económico probar las ganancias en eficiencia que alegue","T15","LFCE 55",""),
 ("C09",R1,"La multa se individualiza considerando gravedad, daño, intencionalidad, participación de mercado, tamaño del mercado, duración y capacidad económica.",
  "Para individualizar la multa, esta Comisión debe considerar la gravedad de la infracción","T21","LFCE 130",""),
 ("C10",R2,"El análisis de una concentración busca determinar si tiene por objeto o efecto obstaculizar, disminuir, dañar o impedir la competencia.",
  "El análisis de una concentración tiene por objeto determinar si esta tiene por objeto o efecto obstaculizar","T17","LFCE 63; LFCE 64",""),
 ("C11",R2,"Definir el mercado relevante exige identificar los productos sustitutos para el consumidor y el área geográfica en que compiten los oferentes.",
  "La determinación del mercado relevante exige identificar los productos que los consumidores consideran sustitutos","T06","LFCE 58","C01"),
 ("C12",R2,"En la venta minorista de medicamentos el mercado geográfico tiende a ser local, porque los consumidores no se desplazan grandes distancias.",
  "En la venta minorista de medicamentos, el mercado geográfico tiende a ser local","T07","",""),
 ("C13",R2,"Los índices de concentración son un indicador inicial, no concluyente; un incremento elevado del IHH exige un análisis más detallado.",
  "Los índices de concentración son un indicador inicial y no un criterio concluyente","T10","",""),
 ("C14",R2,"La posible entrada de competidores solo atenúa los riesgos de una concentración si es probable, oportuna y suficiente.",
  "La posibilidad de entrada de nuevos competidores solo atenúa los riesgos de una concentración si es probable, oportuna y suficiente","T09","",""),
 ("C15",R2,"Una concentración puede autorizarse con condiciones si estas bastan para corregir los riesgos y guardan proporción con ellos.",
  "Esta Comisión puede autorizar una concentración sujeta a condiciones cuando estas sean suficientes para corregir los riesgos identificados","T18","LFCE 90",""),
 ("C16",R2,"Los remedios estructurales, como la desinversión, son preferibles cuando los riesgos se concentran en mercados locales identificables.",
  "Las condiciones estructurales, como la desinversión de establecimientos, son preferibles cuando los riesgos se concentran en mercados locales identificables","T19","LFCE 90",""),
 ("C17",R3,"Las resoluciones de la COFECE solo se impugnan mediante amparo indirecto y no son objeto de suspensión.",
  "Las resoluciones de la Comisión Federal de Competencia Económica solo pueden impugnarse mediante el juicio de amparo indirecto","T02","CPEUM 28",""),
 ("C18",R3,"El control judicial de determinaciones técnicas no sustituye el criterio de la Comisión; verifica que su razonamiento sea completo, coherente y probado.",
  "El control judicial de las determinaciones técnicas de la Comisión no consiste en sustituir su criterio","T03","",""),
 ("C19",R3,"Una participación de mercado elevada no basta para acreditar poder sustancial; deben valorarse barreras a la entrada y posición de competidores.",
  "una participación de mercado elevada no es suficiente para tener por acreditado el poder sustancial","T08","LFCE 59","C02"),
 ("C20",R3,"Una práctica monopólica puede acreditarse con prueba indiciaria si los indicios son plurales, concordantes y están enlazados.",
  "La autoridad de competencia puede acreditar una práctica monopólica mediante prueba indiciaria","T04","",""),
 ("C21",R3,"Individualizar la multa exige explicar cómo se ponderó cada elemento del artículo 130; enumerarlos no basta para motivar.",
  "la sola enumeración de esos elementos no satisface el deber de motivación","T22","LFCE 130",""),
 ("C22",R3,"Si el vicio se limita a la motivación de la multa, el amparo se concede para que se emita una nueva sanción, sin afectar la acreditación de la conducta.",
  "Cuando el vicio se limita a la motivación de la multa, el amparo se concede para el efecto de que la autoridad emita una nueva determinación sobre la sanción","T23","",""),
]
tax = dict(TAX)
with open(f"{OUT}/gold_criterios.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_criterio","documento","criterio","cita_literal","pagina","id_tema","ruta_tema","articulos","duplicado_de"])
    for cid, doc, crit, cita, t, art, dup in G:
        w.writerow([cid, doc, crit, cita, pagina(doc, cita), t, tax[t], art, dup])

# ---------- negativos para el ejercicio de validación ----------
N = [
 ("N01",R1,"transcripcion","El Cliente se obliga a destinar el equipo exclusivamente a la exhibición y conservación de los productos de la Comodante.",""),
 ("N02",R1,"hecho","Entre enero de 2021 y junio de 2024, Lácteos Sierra Morena celebró contratos de comodato de refrigeradores con 4,812 puntos de venta",""),
 ("N03",R1,"valoracion_prueba","Del análisis de las facturas exhibidas se advierte que el 78% de las ventas de la investigada",""),
 ("N04",R1,"argumento_parte","La investigada argumentó que es propietaria de los refrigeradores y que puede decidir libremente su uso.",""),
 ("N05",R2,"hecho","Farmacias del Río opera 412 farmacias en nueve entidades federativas.",""),
 ("N06",R2,"aplicacion_al_caso","En once de los trece municipios con traslape, el incremento del índice es menor a 75 puntos.",""),
 ("N07",R3,"tramite","La demanda se admitió el veinte de junio de dos mil veinticinco.",""),
 ("N08",R3,"aplicacion_al_caso","la cláusula contractual, los correos de seguimiento comercial y la cobertura del 64% de los puntos de venta forman una cadena de indicios suficiente",""),
]
with open(f"{OUT}/negativos_validacion.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","documento","tipo","texto_literal","pagina"])
    for nid, doc, tipo, txt, _ in N:
        w.writerow([nid, doc, tipo, txt, pagina(doc, txt)])

# ---------- pares para el gate de fidelidad ----------
F = [
 ("F01","C04","Un comodato de equipos condicionado a su uso exclusivo puede equivaler a una cláusula de exclusividad.","fiel"),
 ("F02","C04","Todo contrato de comodato de equipos constituye una práctica monopólica relativa.","generalizacion_no_sostenida"),
 ("F03","C13","Un incremento del IHH superior a 75 puntos hace ilegal una concentración.","generalizacion_no_sostenida"),
 ("F04","C12","El mercado geográfico de todos los productos de consumo es local.","generalizacion_no_sostenida"),
 ("F05","C12","En el comercio minorista de medicamentos, el mercado geográfico suele ser local por la poca disposición de los consumidores a desplazarse.","fiel"),
 ("F06","C21","Si la multa no está motivada, debe anularse toda la resolución, incluida la acreditación de la conducta.","generalizacion_no_sostenida"),
]
with open(f"{OUT}/pares_fidelidad.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id","criterio_fuente","abstraccion","etiqueta"]); w.writerows(F)

# ---------- gold de información general ----------
I = [
 dict(documento=R1, autoridad="COFECE · Pleno", tipo_procedimiento="COFECE_INV", expediente="DE-FIC-017-2024",
      fecha_resolucion="2025-05-15", fecha_demanda="", agentes="Lácteos Sierra Morena, S.A. de C.V.",
      sentido="sancion", multa_mxn="38450000", monto_operacion_mxn="", votacion="unanimidad",
      articulos_principales="LFCE 54; 55; 56-IV; 58; 59; 130"),
 dict(documento=R2, autoridad="COFECE · Pleno", tipo_procedimiento="COFECE_CNT", expediente="CNT-FIC-088-2025",
      fecha_resolucion="2025-07-03", fecha_demanda="", agentes="Farmacias del Río, S.A. de C.V.; Boticas Unidas del Centro, S.A.P.I. de C.V.",
      sentido="autorizacion_con_condiciones", multa_mxn="", monto_operacion_mxn="2350000000", votacion="mayoria",
      articulos_principales="LFCE 58; 63; 64; 86; 90"),
 dict(documento=R3, autoridad="Juzgado Segundo de Distrito Especializado en Competencia Económica, Radiodifusión y Telecomunicaciones",
      tipo_procedimiento="PJF_JD", expediente="FIC-45/2025", fecha_resolucion="2026-02-20", fecha_demanda="2025-06-17",
      agentes="Lácteos Sierra Morena, S.A. de C.V.", sentido="ampara_en_parte",
      multa_mxn="", monto_operacion_mxn="", votacion="no_aplica", articulos_principales="CPEUM 28; LFCE 130"),
]
with open(f"{OUT}/gold_info_general.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(I[0].keys())); w.writeheader(); w.writerows(I)

for k, v in paginas.items():
    print(k, len(v), "páginas")
print(len(G), "criterios;", len(N), "negativos;", len(F), "pares de fidelidad")
