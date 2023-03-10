
import xml.etree.ElementTree as ET
import re
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def getdistrito(elem):
    x = elem.text.split('Distrito', 1)
    x = x[1].split('Barrio', 1)
    distrito = cleanhtml(x[0]).strip()
    return distrito


def getnombre(elem):
    x = elem.text.split('Calle', 1)
    x = x[1].split('Nº Finca', 1)
    calle = cleanhtml(x[0]).strip()
    calleaux = calle.split(',')
    calle = ''
    if len(calleaux) > 1:
        calleaux2 = calleaux[1:]
        calleaux2.append(calleaux[0])
        for i in calleaux2:
            calle = calle + i.strip() + ' '
    x = elem.text.split('Nº Finca', 1)
    x = x[1].split('Tipo de Reserva', 1)
    numero = cleanhtml(x[0]).strip()
    nombre = calle.strip() + ' ' + numero
    return nombre


if __name__ == '__main__':
    distritos = ['01  CENTRO','02  ARGANZUELA','03  RETIRO','04  SALAMANCA','05  CHAMARTÍN','06  TETUÁN','07  CHAMBERÍ','08  FUENCARRAL-EL PARDO','09  MONCLOA-ARAVACA','10  LATINA','11  CARABANCHEL','12  USERA','13  PUENTE DE VALLECAS','14  MORATALAZ','15  CIUDAD LINEAL','16  HORTALEZA','17  VILLAVERDE','18  VILLA DE VALLECAS','19  VICÁLVARO','20  SAN BLAS-CANILLEJAS','21  BARAJAS']
    filtro = distritos[0]
    tree = ET.parse('source/doc.kml')
    root = tree.getroot()
    for child in root:
        for item in reversed(child):
            if 'Placemark' in item.tag:
                for elem in item:
                    if 'description' in elem.tag:
                        distrito = getdistrito(elem)
                        nombre = getnombre(elem)
                        new = ET.Element('name')
                        new.text = nombre
                        item.append(new)
                        if distrito != filtro:
                            child.remove(item)
    tree.write('newdoc' + filtro + '.kml')
    f = open('newdoc' + filtro + '.kml', 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('ns0:', '')
    text = text.replace('<table', '<![CDATA[<table')
    text = text.replace('</table>', '</table>]]>')
    text = text.replace('<name>INCA</name>', '<name>' + filtro + '</name>')
    f = open('newdoc' + filtro + '.kml', 'w', encoding='utf-8')
    f.write(text)
    f.close()