SEXO_CHOICES = (
    ('M', 'MASCULINO'),
    ('F', 'FEMININO'),
)

SANGUE = (
    ('INDEFINIDO', 'INDEFINIDO'),
    ('AB', 'AB'),
    ('A', 'A'),
    ('B', 'B'),
    ('O', 'O'),
)

# SANGUE = (
#     (5, 'INDEFINIDO'),
#     (2, 'AB'),
#     (4, 'A'),
#     (1, 'B'),
#     (3, 'O'),
# )

ESTADO_CIVIL_CHOICES = (
    ('SOLTEIRO', 'SOLTEIRO'),
    ('CASADO', 'CASADO'),
    ('VIUVO', 'VIUVO'),
    ('SEPARADO JUDICIALMENTE', 'SEPARADO JUDICIALMENTE'),
    ('DIVORCIADO', 'DIVORCIADO'),
    ('UNIAO ESTAVEL', 'UNIAO ESTAVEL'),
    ('NAO FOI DEFINIDO NO CADASTRO', 'NÃO FOI DEFINIDO NO CADASTRO'),
)

# ESTADO_CIVIL_CHOICES = (
#     (1, u'SOLTEIRO'),
#     (2, u'CASADO'),
#     (3, u'VIUVO'),
#     (4, u'SEPARADO JUDICIALMENTE'),
#     (5, u'DIVORCIADO'),
#     (6, u'UNIAO ESTAVEL'),
#     (7, u'NÃO FOI DEFINIDO NO CADASTRO'),
# )

RACA_COR_CHOICES = (
    ('BRANCA', u'BRANCA'),
    ('PARDA', u'PARDA'),
    ('AMARELA', u'AMARELA'),
    ('NEGRA', u'NEGRA'),
    ('INDÍGENA', u'INDÍGENA'),
    ('QUILOMBOLA', u'QUILOMBOLA'),
    ('NAO INFORMADO', u'NÃO INFORMADO')
)

# RACA_COR_CHOICES = (
#     (6, u'BRANCA'),
#     (1, u'PARDA'),
#     (2, u'AMARELA'),
#     (3, u'NEGRA'),
#     (4, u'INDÍGENA'),
#     (7, u'QUILOMBOLA'),
#     (5, u'NÃO INFORMADO')
# )

FATOR_RH = (
    ('INDEFINIDO', 'INDEFINIDO'),
    ('+', '+'),
    ('-', '-'),
)

# FATOR_RH = (
#     (3, 'INDEFINIDO'),
#     (2, '+'),
#     (1, '-'),
# )

DOCUMENTO_CHOICES = (
    (1, u'TÍTULO DE ELEITOR'),
    (2, u'CNH'),
    (3, u'CTPS'),
    (4, u'PIS/PASEP'),
    (5, u'NIS'),
    (7, u'IPSEP'),
    (8, u'INSS'),
    (9, u'RESERVISTA'),
    (10, u'CONSELHO PROFISSIONAL'),
)

TIPO_ENDERECO_CHOICES = (
    (1, u'RESIDENCIAL'),
    (2, u'COMERCIAL'),
    (3, u'INSTITUCIONAL'),
)

TIPO_LOGRADOURO_ENDERECO_CHOICES = (
    (8, 'RUA'),
    (9, 'QUADRA'),
    (1, u'AVENIDA'),
    (2, u'PRAÇA'),
    (3, u'VIELA'),
    (4, u'PONTO'),
    (5, u'VIADUTO'),
    (6, u'ALAMEDA'),
    (7, u'OUTROS'),
)


TIPO_TELEFONE_CHOICES = (
    ('RESIDENCIAL', 'RESIDENCIAL'),
    ('COMERCIAL', 'COMERCIAL'),
    ('CELULAR', 'COMERCIAL'),
    ('FAX', 'FAX'),
    ('INSTITUCIONAL', 'INSTITUCIONAL'),
)


PAISES = (
    (1, 'BRASIL'),
    (2, 'AFRICA DO SUL'),
    (3, 'INDIA'),
    (4, 'CHINA'),
)

TIPO_CONTA_CHOICES = (
    (1, 'CORRENTE'),
    (2, 'POUPANÇA'),
    (3, 'INVESTIMENTO')
)


ESPECIFICIDADE_DOCUMENTO_CHOICES = (
    (1, u'TÍTULO DE ELEITOR.ZONA'),
    (2, u'TÍTULO DE ELEITOR.SEÇÃO'),
    (3, u'TÍTULO DE ELEITOR.UF'),
    (7, u'TÍTULO DE ELEITOR.MUNICIPIO'),
    (4, u'CNH.CATEGORIA'),
    (5, u'RESERVISTA.CLASSE'),
    (6, u'CTPS.SERIE'),
)

DOCUMENTO_CHOICES = (
    (1, u'TÍTULO DE ELEITOR'),
    (2, u'CNH'),
    (3, u'CTPS'),
    (4, u'PIS/PASEP'),
    (5, u'NIS'),
    (7, u'IPSEP'),
    (8, u'INSS'),
    (9, u'RESERVISTA'),
    (10, u'CONSELHO PROFISSIONAL'),
)

GRAU_INSTRUCAO_CHOICES = (
    ('ANALFABETO', 'ANALFABETO'),
    ('ALFABETIZADO SEM CURSOS REGULARES', 'ALFABETIZADO SEM CURSOS REGULARES'),
    ('FUNDAMENTAL INCOMPLETO', 'FUNDAMENTAL INCOMPLETO'),
    ('FUNDAMENTAL COMPLETO', 'FUNDAMENTAL COMPLETO'),
    ('MÉDIO INCOMPLETO', u'MÉDIO INCOMPLETO'),
    ('MÉDIO COMPLETO', u'MÉDIO COMPLETO'),
    ('TÉCNICO', u'TÉCNICO'),
    ('SUPERIOR INCOMPLETO', u'SUPERIOR INCOMPLETO'),
    ('SUPERIOR COMPLETO', u'SUPERIOR COMPLETO'),
    ('ESPECIALIZAÇÃO/PÓS-GRADUAÇÃO', u'ESPECIALIZAÇÃO/PÓS-GRADUAÇÃO'),
    ('MESTRADO', u'MESTRADO'),
    ('DOUTORADO', u'DOUTORADO'),
    ('PÓS-DOUTORADO', u'PÓS-DOUTORADO'),
    ('INFORMADO', u'INFORMADO'),
)

# GRAU_INSTRUCAO_CHOICES = (
#     (1, 'ANALFABETO'),
#     (2, 'ALFABETIZADO SEM CURSOS REGULARES'),
#     (3, 'FUNDAMENTAL INCOMPLETO'),
#     (4, 'FUNDAMENTAL COMPLETO'),
#     (5, u'MÉDIO INCOMPLETO'),
#     (6, u'MÉDIO COMPLETO'),
#     (13, u'TÉCNICO'),
#     (7, u'SUPERIOR INCOMPLETO'),
#     (8, u'SUPERIOR COMPLETO'),
#     (9, u'ESPECIALIZAÇÃO/PÓS-GRADUAÇÃO'),
#     (10, u'MESTRADO'),
#     (11, u'DOUTORADO'),
#     (12, u'PÓS-DOUTORADO'),
#     (14, u'INFORMADO'),
# )
