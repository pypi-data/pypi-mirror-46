import os
from lxml import etree
from io import StringIO, BytesIO
from pprint import pprint
from time import time


class Input:
    def __init__(self, filename, content):
        # self.parser = etree.XMLParser(encoding='utf-8',
        #                               recover=True,
        #                               remove_comments=True)
        self.filename = filename
        self.xml_obj = content


class DTDResolver(etree.Resolver):
    """
    Резолвер для определения документа при относительном импорте
    """
    def resolve(self, url, id, context):
        print('Resolving urL:', url)
        return self.resolve_string(url, context)


xsd_root = '/home/vasily/PyProjects/FLK/pfr/compendium/АДВ+АДИ+ДСВ 1.17.12д'
root = '/home/vasily/PyProjects/FLK/pfr/compendium/АДВ+АДИ+ДСВ 1.17.12д/Примеры/ВЗЛ/Входящие'
compendium_file = 'ПФР_КСАФ.xml'
xml_file = 'PFR-700-Y-2017-ORG-034-005-000023-DCK-00444-DPT-000000-DCK-00000.xml'
cp_parser = etree.XMLParser(encoding='cp1251',
                            recover=True,
                            remove_comments=True,
                            load_dtd=True)
cp_parser.resolvers.add(DTDResolver())

utf_parser = etree.XMLParser(encoding='utf-8',
                             recover=True,
                             remove_comments=True)

# Достаём информацию из компендиума
with open(os.path.join(xsd_root, compendium_file), 'rb') as handler:
    try:
        compendium = etree.fromstring(handler.read(), parser=utf_parser)
    except etree.XMLSyntaxError as ex:
        print(f'Error xml file parsing: {ex}')
        exit(1)

with open(os.path.join(root, xml_file), 'rb') as handler:
    data = handler.read()
    xml_content = etree.fromstring(data, parser=cp_parser)
    input = Input(xml_file, xml_content)

nsmap = xml_content.nsmap
nsmap['d'] = nsmap.pop(None)

try:
    doc_type = xml_content.find('.//d:ТипДокумента', namespaces=nsmap).text
except AttributeError as ex:
    print('Не определён тип документа')
    exit(1)

nsmap = compendium.nsmap
nsmap['d'] = nsmap.pop(None)

st = time()
doc_def = compendium.xpath(
    f'.//d:Валидация[contains(d:ОпределениеДокумента, "{doc_type}")]',
    namespaces=nsmap)[0]
print('Elapsed time:', time() - st)

# Путь к валидационной схеме
schemes = doc_def.xpath('./d:Схема/text()', namespaces=nsmap)

# Пути в схемах как в винде, поэтому меняем слэши
for idx, scheme in enumerate(schemes):
    schemes[idx] = scheme[1:].replace('\\', '/')

# Работаем с проверяемым .xml файлом
# Проверка, есть ли уже такой в базе
# query = self.session.query(f'db:exists("xml_db{self.db_num}", '
#                            f'"{self.db_root}/{self.xml_file}")')
# query_result = query.execute()
# if query_result == 'false':
#     # Файл не найден, добавляем
#     self.session.add(f'{self.db_root}/{self.xml_file}',
#                      self.content.decode('utf-8'))
# if query:
#     query.close()

# Пробегаем по всем .xsd схемам и проверяем файл
# for scheme in schemes:
#     print(scheme)
#     with open(os.path.join(xsd_root, scheme), 'rb') as xsd_handler:
#         try:
#             xsd_content = etree.parse(xsd_handler, parser=cp_parser).getroot()
#             xsd_scheme = etree.XMLSchema(xsd_content)
#             try:
#                 xsd_scheme.assertValid(xml_content)
#             except etree.DocumentInvalid as ex:
#                 for error in xsd_scheme.error_log:
#                     input.verify_result['xsd_asserts'] \
#                         .append(f'{error.message} (строка {error.line})')
#
#                 input.verify_result['result'] = 'failed_xsd'
#                 input.verify_result['description'] = (
#                     f'Ошибка при валидации по xsd схеме файла '
#                     f'{self.xml_file}: {ex}.')
#                 # return
#
#         except etree.XMLSyntaxError as ex:
#             #TODO: logger
#             print(f'Error xsd file parsing: {ex}')
#             # return
#
# pprint(input.verify_result)

with open('/home/vasily/PyProjects/FLK/pfr/compendium/АДВ+АДИ+ДСВ 1.17.12д/Схемы/ВЗЛ/Типы.xsd', 'rb') as xsd_handler:
    # strio = BytesIO(xsd_handler.read())
    xsd_content = etree.parse(xsd_handler, cp_parser)
    # xsd_content = etree.parse(strio, parser=cp_parser).getroot()
    # xsd_content = etree.parse(xsd_handler, parser=cp_parser).getroot()
    # print(xsd_content.find('.//xs:include', namespaces=xsd_content.nsmap).attrib)
    xsd_scheme = etree.XMLSchema(xsd_content)
    # print(xsd_scheme)
