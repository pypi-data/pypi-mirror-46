#!/usr/bin/env python
u"""Provides de class SyntacticTagger, which is a part-of-speech tagger and lemmatizer for Spanish.
"""

from iar_tokenizer import Tokenizer
import msgpacku as msgpack
from itertools import chain, product
from os.path import dirname, realpath, join
import bz2
from math import log10
from re import sub

# Constants
NOUN = "N"
COMMON = "C"
PROPER = "P"
MASCULINE = "M"
FEMININE = "F"
SINGULAR = "S"
PLURAL = "P"
INVARIABLE = "I"
ADJECTIVE = "A"
DETERMINER = "D"
PRONOUN = "P"
VERB = "V"
ADVERB = "R"
PREPOSITION = "S"
CONJUNCTION = "C"
INTERJECTION = "I"
PUNCTUATION = "F"
NUMBER = "Z"
AFFIX = "-"
ONOMATOPOEIA = "O"
EXPRESSION = "E"
UNKNOWN = "?"


class SyntacticTagger:
    u"""This class is a part-of-speech tagger. It uses a lexicon and a syntactic table to choose the tags.

    The main idea is that a lexicon provides the possible tags for each token, and the syntactic table is
    used in order to choose which of those tags is the most "probable" one.
    The syntactic table has been trained used the Spanish Wikipedia, and contains all the POS tags seen in it
    with a weighting whose value is based on the frequency of occurrence, the information from an electronic
    dictionary and the overal frequency of occurrence of the different syntactic categories in a plain text
    corpus.
    """

    def __init__(self):
        u"""Initializes the class by loading the data files needed for the tagging.
        """
        self._syntactic_table = self.load_data('syntactic_table')
        self._lexicon = self.load_data('lexicon')
        self._tag_number_converter = self.load_data('tag_number_converter')
        self._form_count = self.load_data('form_count')
        self._prefixes = self.load_data('prefixes')

    @staticmethod
    def load_data(data_type):
        u"""Used in the SyntacticTagger initializer to load a data file.

        :type data_type: unicode
        :param data_type: The name of the data file to be loaded.
        """
        data_file_path = join(dirname(realpath(__file__)), 'data_files', data_type + u'.msgpack.bz2')
        with bz2.BZ2File(data_file_path, 'rb') as data_file:
            return msgpack.unpack(data_file, use_list=False, encoding="utf-8")

    def get_possible_tags(self, form, return_lemmas=False, dont_lemmatize_proper_nouns=False):
        prefix = u''
        if form not in self._lexicon:
            # No está la form en el lexicón. Lo primero que miramos es si la form en minúscula está.
            # Esto es un poco así, porque dado que normalmente minusculizamos las primeras palabras de las
            # frases, puede inducir a error y hacernos cambiar un nombre propio por uno común. Pero como nos
            # interesa sobre todo acertar con la categoría, es un error menos importante.
            if form.lower() in self._lexicon:
                # Si la palabra minusculizada está, nos quedamos con ella. Puede que esté toda en mayúscula o
                # que sea un nombre propio multipalabra formado por palabras comunes en mayúscula, como el
                # nombre de un libro, película, asociación, entidad política...
                form = form.lower()
            else:
                # No está en minúscula, así que nos fijamos primero en la posibilidad de que incluya un guion
                # o cualquier símbolo pegado. Lo quitaremos y miraremos la última palabra.
                original_form = form
                tokenized_form = Tokenizer.segmenta_por_palabras(
                        Tokenizer.segmenta_por_frases(form, elimina_separadores=True,
                                                      elimina_separadores_blancos=True,
                                                      incluye_parentesis=True,
                                                      adjunta_separadores=False, agrupa_separadores=False),
                        elimina_separadores=True, segmenta_por_guiones_internos=True,
                        segmenta_por_guiones_externos=True, segmenta_por_apostrofos_internos=False,
                        segmenta_por_apostrofos_externos=True, adjunta_separadores=False,
                        agrupa_separadores=False)[-1]
                if tokenized_form in self._lexicon:
                    prefix = form[:-len(tokenized_form)]
                    form = tokenized_form
                elif tokenized_form.lower() in self._lexicon:
                    prefix = form[:-len(tokenized_form)]
                    form = tokenized_form.lower()
                else:
                    # Por último vemos si quitándole prefijos llegamos a alguna form conocida.
                    forma_desprefijada = self.get_unprefixed_form(tokenized_form.lower())
                    if forma_desprefijada != form.lower():
                        prefix = form[:len(form) - len(forma_desprefijada)].lower()
                        form = forma_desprefijada
                # Si hemos cambiado la form, nos aseguramos de que dicha form no puede ser otra cosa que
                # un nombre, adjetivo, verbo o adverbio.
                if form in self._lexicon:
                    if len([tag for lemma, weighted_tags in self._lexicon[form].items()
                            for tag in weighted_tags.keys()
                            if self._tag_number_converter[tag][0] not in NOUN + ADJECTIVE + VERB + ADVERB]):
                        form = original_form
                        prefix = u''

        if form in self._lexicon:
            form_tags = {}
            for lemma, weighted_tags in self._lexicon[form].items():
                for tag, weighting in weighted_tags.items():
                    # Especialmente en modo croquis, la form puede tener la misma etiqueta viniendo de lemas
                    # distintos (por ejemplo, dos formas verbales coincidentes como yo/él cante o yo creo).
                    # Sumamos los puntos.
                    if return_lemmas:
                        form_tags[tag] = form_tags.setdefault(tag, [0.0, (weighting, lemma)])
                        form_tags[tag][0] += weighting
                        if lemma != form_tags[tag][1][1]:
                            # Los adverbios en -mente que aparecen como entradas en la RAE se lematizan como
                            # el adjetivo. TODO: ¿Deberíamos cambiar esto?
                            if form_tags[tag][1][0] < weighting or\
                                    (form_tags[tag][1][0] == weighting and
                                     len(lemma) < len(form_tags[tag][1][1])):
                                form_tags[tag][1] = (weighting, lemma)
                    else:
                        form_tags[tag] = form_tags.setdefault(tag, 0.0) + weighting
            # A veces podemos desprefijar algo y dejar como resultado una palabra gramatical. Esto no es
            # correcto, y en dichos casos, aunque hayamos encontrado una form posible, no lo devolvemos
            if not prefix or not [tag for tag in form_tags.keys()
                                  if self._tag_number_converter[tag][0] not in NOUN + ADJECTIVE + VERB]:
                if return_lemmas:
                    form_tags = {tag: [value[0], prefix + value[1][1]]
                                 for tag, value in form_tags.items()}
                return form_tags

        # Si la form no aparece en el lexicón, creamos unas etiquetas especiales.
        lemma = u''
        has_apostrophe = sum(1 if apostrophe in form[1:-1] else 0 for apostrophe in u"'‘`’´") > 0
        if form[0] != form[0].lower() or has_apostrophe:
            if len(form) == 1 or form[1:] == form[1:].lower() or has_apostrophe:
                # Un único carácter o solo la primera está en mayúsculas.
                if form[-1] == u's':
                    number = PLURAL
                    gender = FEMININE if len(form) > 1 and form[-2] == u'a'\
                        else MASCULINE if len(form) > 1 and form[-2] == u'o' else COMMON
                    if return_lemmas:
                        if dont_lemmatize_proper_nouns:
                            lemma = form
                        else:
                            lemma = form[:-1]
                else:
                    number = SINGULAR
                    gender = FEMININE if form[-1] == u'a' else MASCULINE if form[-1] == u'o' else COMMON
                    if return_lemmas:
                        lemma = form
                tag = NOUN + PROPER + gender + number + "0000"
            else:
                # Hay más caracteres en mayúscula.
                tag = NOUN + PROPER + COMMON + INVARIABLE + "0000"
                if return_lemmas:
                    lemma = form
            if return_lemmas:
                form_tags = {self._tag_number_converter[SyntacticTagger.summarize_tag(tag)]: [1.0, lemma]}
            else:
                form_tags = {self._tag_number_converter[SyntacticTagger.summarize_tag(tag)]: 1.0}
        else:
            if any(char.isdigit() for char in form):
                if return_lemmas:
                    form_tags = {self._tag_number_converter[NUMBER]: [1.0, form]}
                else:
                    form_tags = {self._tag_number_converter[NUMBER]: 1.0}
            elif form.upper() != form:
                # Parece ser una palabra, aunque puede que esté en otro idioma o que simplemente tenga
                # algún prefijo, sea un modismo... y no la reconocemos. Nos la jugamos y la etiquetamos
                # como nombre.
                tag = NOUN + COMMON + COMMON + INVARIABLE + "0000"
                if return_lemmas:
                    form_tags = {self._tag_number_converter[SyntacticTagger.summarize_tag(tag)]:
                                 [1.0, form[:-1] if form[-1] == u's' else form]}
                else:
                    form_tags = {self._tag_number_converter[SyntacticTagger.summarize_tag(tag)]: 1.0}
            else:
                # Parece que no son caracteres ya que no varía de minúsculas a mayúsculas, y tampoco es
                # un número. Posiblemente sea algún signo.
                if return_lemmas:
                    form_tags = {self._tag_number_converter[UNKNOWN]: [1.0, form]}
                else:
                    form_tags = {self._tag_number_converter[UNKNOWN]: 1.0}
        return form_tags

    def choose_tags(self, possible_tags):
        """La idea de base es la siguiente: ya que las probabilidades de las etiquetas dependen solo de un
        número de etiquetas previas, si yo sé el valor de dichas etiquetas previas, puedo saber cuál es la
        combinación de etiquetas siguientes que más "probabilidad" tiene de continuar dicha secuencia.
        Así que dividimos la frase en fragmentos que tienen la misma longitud que la ventana (en principio
        solo hay margen izquierdo). Comenzando desde el último, calculamos cuál es la combinación posible
        más "probable" para cada una de las combinaciones de etiquetas del fragmento anterior.
        Al empezar por la última, las "probabilidades" de las combinaciones de etiquetas para el último
        fragmento solo dependen de las etiquetas del fragmento previo. En fragmentos que no sean el último
        la probabilidad de las combinaciones de este fragmento tendrán un cierto valor, pero hay que tener
        en cuenta que para dicho valor ya sabemos cuál es la combinación más "probable" que le sigue, con lo
        que se tiene en cuenta esta "probabilidad" del fragmento siguiente.

        :param possible_tags:
        :return:
        """
        left_context, right_context = 2, 1
        # Nos entra la representación de una frase como una lista de tokens. Dichos tokens representan cada
        # palabra de una frase. Cada palabra se representa con un diccionario que tiene códigos de etiquetas
        # como claves y sus porcentajes de probabilidad ponderada como valores.
        # Dividimos la frase en fragmentos del tamaño de la ventana. Cada fragmento es un trozo de la lista
        # que representa a la frase, con un tamaño máximo de margen_i.
        fragment_size = max(left_context, right_context)
        fragments = [possible_tags[fragment_order * fragment_size:(fragment_order + 1) * fragment_size]
                     for fragment_order in range((1 if len(possible_tags) % fragment_size else 0)
                                                 + int(len(possible_tags) / fragment_size))]
        fragment_number = len(fragments)
        # Para cada fragmento, calculamos todas las combinaciones posibles de etiquetas (frags_combs no
        # incluye ninguna información de "probabilidad", solo las etiquetas).
        frags_combs = [list(product(*fragment)) for fragment in fragments]
        # Creamos la estructura que tiene, para todas las combinaciones de etiquetas del fragmento actual,
        # cuál es la combinación de etiquetas de los fragmentos posteriores que tiene mayor "probabilidad".
        # Puesto que comenzamos en el último fragmento, dicha combinación sera la de ninguna etiqueta, y
        # tendrá valor 0.0 (logaritmo del 100% de "probabilidad").
        post_frag_combs = {}
        # Procesamos los fragmentos desde el último
        for current_frag_order in range(fragment_number - 1, -1, -1):
            # Cargamos el fragmento actual a procesar, que es una lista de diccionarios (cada uno representa a
            # una palabra) con claves las etiquetas posibles de la palabra y con valores sus "probabilidades".
            # Además cargamos las combinaciones de etiquetas posibles para dicho fragmento.
            fragment = fragments[current_frag_order]
            current_frag_combs = frags_combs[current_frag_order]

            # Cargamos ahora todas las posibles combinaciones de entornos que afectan a las etiquetas del
            # fragmento actual.
            prev_context = [tuple(t.keys()) for t in fragments[current_frag_order - 1][-left_context:]]\
                if current_frag_order > 0 else [(None, )] * left_context
            post_context = [tuple(t.keys()) for t in fragments[current_frag_order + 1][:right_context]]\
                if current_frag_order < fragment_number - 1 else [(None, )] * right_context
            context_combs = list(product(*(prev_context + post_context)))

            # Para este fragmento guardaremos cuál es la combinación más "probable" y su "probabilidad", para
            # cada una de las combinaciones posibles del entorno.
            combs_for_context = {}
            for context_comb in context_combs:
                # Dada esta combinación del entorno que afecta al fragmento actual, extraeremos la combinación
                # de etiquetas para este fragmento actual que maximiza la "probabilidad". Dicha "probabilidad"
                # consiste en la multiplicación de las "probabilidades" de entorno y de etiqueta de cada una
                # de las etiquetas que asignemos a este fragmento, multiplicado por la "probabilidad" máxima
                # de las etiquetas de fragmentos posteriores (cuya "probabilidad" máxima se calculó en la
                # pasada del algoritmo para el fragmento procesado en la iteración anterior -o el 100% y
                # ninguna etiqueta en el último-).
                combs_for_current_frag_in_context = {}
                for current_frag_comb in current_frag_combs:
                    current_comb_weighting = 0.0  # Está en formato logarítmico.
                    for current_tag_order, current_tag in enumerate(current_frag_comb):
                        context = \
                            (context_comb[:left_context] + current_frag_comb
                             + context_comb[left_context:])[current_tag_order:
                                                            current_tag_order + left_context + right_context
                                                            + 1]
                        # En la tabla, las tags precedentes van en orden inverso, desde la más cercana a la
                        # más lejana. Las siguientes también van de la más cercana a la más lejana, es decir,
                        # en el mismo orden en el que están.
                        reordered_context = context[left_context::-1] + context[left_context + 1:]
                        # Asignamos de entrada a la combinación la mitad de la probabilidad mínima
                        # (la probabilidad de combinaciones no vistas)
                        context_weighting = -47.6245104413 - 0.301029995664
                        current_tag_weighting = log10(fragment[current_tag_order][current_tag][0])
                        # Buscamos en la tabla si tenemos la combinación de etiquetas de este entorno. Para
                        # ello, vamos tomando las etiquetas del entorno ya reordenado y vamos adentrándonos
                        # en los diccionarios anidados que forman la tabla sintáctica, bajando un nivel en
                        # cada pasada del bucle hasta que llegamos al último o tenemos que usar el backup.
                        current_structure = self._syntactic_table
                        for order, tag in enumerate(reordered_context):
                            if tag in current_structure:
                                if order < len(reordered_context) - 1:
                                    # Aún no hemos llegado al final. Nos adentramos un nivel y reiteramos.
                                    current_structure = current_structure[tag]
                                else:
                                    # Estamos en el nivel más profundo de la tabla. Sacamos la "probabilidad".
                                    context_weighting = current_structure[tag]
                            else:
                                # Al llegar a este punto, la combinación no estaba en la tabla. Salimos del
                                # bucle (con lo que asignamos la probabilidad mínima por defecto), o bien
                                # aplicamos el mismo algoritmo pero en la tabla de backup.
                                # TODO: Igual podríamos retomar lo del cálculo del mínimo o similar como
                                # alternativa al backup. Sabiendo la probabilidad total del árbol y el número
                                # de hojas totales, se podría hacer algo teniendo en cuenta la probabilidad
                                # total de la rama y el número de hojas de la rama. También quizá usando el
                                # número de combinaciones posibles (nº etiquetas distintas ** margen_i+d) y
                                # usando logaritmos para saber el número medio de variantes en cada nodo del
                                # árbol... Alguna movida así.
                                break

                        # Metemos la multiplicación de la probabilidad del entorno por la probabilidad
                        # de la etiqueta para la forma que estamos tratando.
                        current_comb_weighting += context_weighting + current_tag_weighting
                    # Vemos si esta combinación de etiquetas tiene más "probabilidad" (o es la primera) que la
                    # combinación con "probabilidad" máxima para este entorno que hayamos visto hasta ahora.
                    # Además de la "probabilidad" de la combinación de etiquetas para este fragmento, hay que
                    # multiplicar por la "probabilidad" de todas las etiquetas hasta el final.
                    # Así que sacamos la combinación para fragmentos posteriores con entorno compatible con
                    # estas combinación de etiquetas que tiene la mayor probabilidad. La estructura obtenida
                    # tiene la estructura ((tag entorno 1, ... tag entorno margen_i+d), (prob, (tags)))
                    combs_for_current_frag_in_context[current_frag_comb] = current_comb_weighting
                combs_for_context[context_comb] = combs_for_current_frag_in_context
            if current_frag_order == len(fragments) - 1:
                post_frag_combs = combs_for_context
            else:
                combs_for_context_aux = {}
                # Para cada posible entorno posible para el fragmento actual...
                for context_tags, context_data in combs_for_context.items():
                    # ... vamos a mirar las posibles combinaciones de etiquetas para el fragmento actual...
                    for fragment_tags, weighting in context_data.items():
                        # Y para cada combinación de etiquetas posible para el fragmento actual, vamos a mirar
                        # las combinaciones que teníamos de entornos y etiquetas para el fragmento que se
                        # ha procesado en la iteración anterior...
                        for post_context_tags, post_data in post_frag_combs.items():
                            # Como tenemos que "empalmar" los fragmentos, tenemos que fijarnos primero en que
                            # solo nos valen las combinaciones de etiquetas para el fragmento anteriormente
                            # procesado que tengan un entorno que sea compatible con la combinación de
                            # etiquetas para el fragmento actual que estamos mirando.
                            if post_context_tags[:left_context] == fragment_tags[:left_context]:
                                # Efectivamente, hemos encontrado un entorno para el fragmento anteriormente
                                # procesado que es compatible con la combinación de etiquetas del fragmento
                                # actual. Para dicha combinación de entorno del fragmento procesado en la
                                # iteración anterior tenemos que buscar una combinación de etiquetas que sea
                                # compatible con el entorno del fragmento actual (su entorno por la derecha).
                                # Es decir, que tanto el entorno de la combinación buscada del fragmento
                                # siguiente tiene que ser compatible con la combinación de etiquetas del
                                # fragmento actual (la combinación del fragmento actual tiene que coincidir
                                # con el entorno por la izquierda del fragmento posterior) como a la inversa
                                # (el entorno por la derecha del fragmento actual tiene que ser compatible con
                                # el fragmento siguiente).
                                for post_fragment_tags, post_weighting in post_data.items():
                                    # Estamos mirando una de las combinaciones de etiquetas para el fragmento
                                    # posterior que tiene un entorno compatible con la combinación de
                                    # etiquetas del fragmento actual que estamos mirando ahora mismo.
                                    # Nos falta saber si el entorno de dicha combinación de etiquetas para el
                                    # fragmento actual es compatible (en su margen derecho) con la combinación
                                    # de etiquetas del fragmento siguiente que estamos mirando ahora mismo.
                                    # Por otra parte, el último fragmento puede tener menos etiquetas que el
                                    # entorno, cuando el entorno por la derecha es mayor que uno y la frase
                                    # no se divide exactamente en fragmentos.
                                    if post_fragment_tags[:right_context] ==\
                                            context_tags[left_context:][:len(post_fragment_tags
                                                                             [:right_context])]:
                                        combs_for_context_aux[context_tags] =\
                                            combs_for_context_aux.setdefault(context_tags, {})
                                        # Tenemos necesidad de guardar las etiquetas porque cuando extraigamos
                                        # el máximo del fragmento anterior, dicho máximo dependerá del entorno
                                        # y por lo tanto de las primeras margen_d etiquetas de este fragmento.
                                        # Así que nos interesa tener una única etiqueta (la más "probable")
                                        # para cada combinación de etiquetas de la parte derecha del entorno.
                                        collision =\
                                            [(k, v)
                                             for k, v in combs_for_context_aux[context_tags].items()
                                             if k[:left_context] == fragment_tags[:left_context]]
                                        if collision:
                                            if collision[0][1] < weighting + post_weighting:
                                                del combs_for_context_aux[context_tags][collision[0][0]]
                                            else:
                                                continue
                                        combs_for_context_aux[context_tags][fragment_tags +
                                                                            post_fragment_tags] =\
                                            weighting + post_weighting
                post_frag_combs = combs_for_context_aux
        highest_weighting_numerized_tags, weighting = max([(tag_list, weighting)
                                                           for dictionary in post_frag_combs.values()
                                                           for tag_list, weighting in dictionary.items()],
                                                          key=lambda x: x[1])
        highest_weighting_tags = [self._tag_number_converter[tag] for tag in highest_weighting_numerized_tags]
        highest_weighting_lemmas = [possible_tags[o][t][1]
                                    for o, t in enumerate(highest_weighting_numerized_tags)]

        return highest_weighting_tags, highest_weighting_lemmas

    @staticmethod
    def summarize_tag(tag):
        category = tag[0]
        if category == NOUN:
            return category + tag[1:4]  # -> 4 characters
        if category in [ADJECTIVE, DETERMINER, PRONOUN]:
            return category + tag[3:5]  # -> 3 characters
        if category == VERB:
            return category + tag[1:3] + tag[5:7]  # -> 5 characters
        if category == ADVERB:
            return category  # -> 1 character
        if category == CONJUNCTION:
            return category + tag[1:2]  # -> 2 characters
        if category == PREPOSITION:
            return category  # -> 1 character
        if category == AFFIX:
            return category  # -> 1 character
        if category == PUNCTUATION:
            return category + tag[1:3]  # -> 3 characters
        if category in [EXPRESSION, NUMBER, INTERJECTION, ONOMATOPOEIA, UNKNOWN]:
            return category

    def get_unprefixed_form(self, form):
        # Si uso modo r'' parece que no se come las ó con tilde.
        if sub(u'[A-ZÑÁÉÍÓÚÜa-zñáéíóúü‒–−­—―-]+', u'', form):
            # Tiene caracteres impropios de una palabra española
            return form

        # Veremos si la forma tiene algún prefijo.
        unprefixed_forms = []
        intermediate_forms = [form]
        form_order = 0
        while form_order < len(intermediate_forms):
            current_form = intermediate_forms[form_order]
            structure = self._prefixes
            while len(current_form) > 3:
                if current_form[0] in u'-‒–−­—―':
                    # A veces aparecen guiones separando el prefijo y el lexema. Lo eliminamos.
                    current_form = current_form[1:]
                    continue
                if u'' in structure:
                    # Lo anterior a esto era un prefijo. La form que queda podría ser una form
                    # conocida pero hay que tener en cuenta la doble rr, y posibles hiatos.
                    if current_form[0].lower() == u'r':
                        if current_form[1].lower() == u'r':
                            # La doble erre a inicio de palabra se convierte en una erre simple.
                            current_form = current_form[1:]
                        else:
                            # No hay palabras que empiecen por ere. La única opción es que el prefijo acabe
                            # en guion r, l, n o s.
                            if form[-len(current_form) - 1] not in u'-‒–−­—―rlns':
                                break
                    if current_form in self._lexicon:
                        # Quitando la parte de prefijos, queda una form que conocemos.
                        if current_form not in unprefixed_forms:
                            unprefixed_forms.append(current_form)
                    # Seguimos buscando a ver si se puede encontrar más prefijos o uno más grande
                    if current_form not in intermediate_forms:
                        intermediate_forms.append(current_form)
                if current_form[0] in structure:
                    structure = structure[current_form[0]]
                    current_form = current_form[1:]
                else:
                    break
            form_order += 1
        if unprefixed_forms:
            # TODO: decidir cuál escogemos.
            form = unprefixed_forms[0]
        return form

    def start_with_lowercase(self, sentence_tokens):
        # Este método se usa cuando queremos minusculizar la primera palabra de una sentence_tokens. Se tienen
        # en cuenta los posibles signos de puntuación iniciales, así como los recuentos de las palabras en
        # minúsculas y mayúsculas (para decidir si parece ser nombre propio a inicio de sentence_tokens o no).
        sentence = sentence_tokens[:]
        for token_order, token in enumerate(sentence):
            # Si solo minusculizamos la primera, modificamos (si es preciso) la primera palabra de la
            # sentence_tokens si es que no está en minúscula ya.
            # El problema es que no siempre el primer token de la sentence_tokens es la primera palabra,
            # puesto que pueden aparecer signos de puntuación.
            if token not in self._lexicon or\
                    PUNCTUATION not in [self._tag_number_converter[tag][0]
                                        for tag in chain.from_iterable(self._lexicon[token].values())]:
                # Es la primera palabra. La minusculizaremos solo si no está en minúsculas o no está
                # enteramente escrita en mayúsculas...
                if token != token.lower() and len(token) == 1 or token[1:] == token[1:].lower():
                    # ... si no hay una siguiente palabra con primer carácter en mayúscula...
                    if token_order == len(sentence) - 1 or \
                            sentence[token_order + 1][0] == \
                            sentence[token_order + 1][0].lower():
                        # ... y si la forma minúscula existe y es más común que la mayúscula.
                        if token.lower() in self._form_count and\
                                (token not in self._form_count or
                                 2 * self._form_count[token] < self._form_count[token.lower()]):
                            sentence[token_order] = token.lower()
                            break
        return sentence

    def tag_text(self, text):
        tokenized_sentences = Tokenizer.segmenta(text, separa_frases=True)
        results = []
        for sentence_order, sentence_tokens in enumerate(tokenized_sentences):
            # Extraemos todas las posibles etiquetas que corresponden a cada forma.
            tokens = self.start_with_lowercase(sentence_tokens)
            possible_sentence_tags =\
                [self.get_possible_tags(token, return_lemmas=True, dont_lemmatize_proper_nouns=True)
                 for token in tokens]
            sentence_tags, sentence_lemmas = self.choose_tags(possible_sentence_tags)
            results.append(list(zip(sentence_tokens, sentence_tags, sentence_lemmas)))
        return results

    @staticmethod
    def test():
        text = 'Su estancia acabó bruscamente al comienzo de la primavera. ' \
               'De la noche a la mañana, el enano portavoz empezó a desarrollar un carácter esquinado. ' \
               'Le sorprendí hurgando en el botiquín y al verse emboscado, se desordenó el pelo y dijo que ' \
               'tenía hambre. Le enseñé la alacena. Cuando quisiera, podía coger lo que necesitara. ' \
               'Pero a la primera de cambio, en cuanto pensaba que nadie le vigilaba, volvía al baño a por ' \
               'paracetamol o píldoras contraceptivas. ' \
               'Daba golpes en la mesa con la mano abierta. ' \
               'Protegía con el brazo el plato de la comida, y se enojaba si yo trataba de poner al otro ' \
               'enano su propio plato. ' \
               'Se escondía detrás de las cortinas y se le oía reír con la voz de un conspirador. ' \
               'Nos dimos cuenta de que ya no cambiaban de estatura. ' \
               'El enano portavoz siempre tenía altura humana, y su semblante parecía el de un príncipe ' \
               'eslavo, iracundo y feliz de estar en el destierro. ' \
               'Cuando no era presa de sus cambios de humor, paseaba por el salón y en su camino elástico ' \
               'era como si pronto fueran a llegar noticias con el resultado de una batalla. ' \
               'Alguna vez, cuando estaba con mi marido en la cama, me sorprendí pensando en el enano ' \
               'principesco, con la mirada humedecida en todos los países de Europa, y me estremecía ' \
               'imaginando sus manos enlucidas sobre mi cara. ' \
               'El otro enano desmejoraba, se quedaba flaco y amarillo; no participaba de las ' \
               'conversaciones y sonreía débilmente cuando nos dirigíamos a él. ' \
               'Fue este enano el que un día se metió en la bañera mientras me duchaba. ' \
               'No chillé. Su cara inspiraba lástima, era completamente inocuo, y estaba tan demacrado y ' \
               'recortado que podría haberlo aplastado con el pie. ' \
               'Me pidió perdón, dándome la espalda. ' \
               'Había decidido abordarme en el baño porque sólo así podría hablarme fuera de la vigilancia ' \
               'del otro. ' \
               'Es esta vida que llevamos, dijo. ' \
               'No es culpa de nadie. ' \
               'Nosotros estamos habituados al exterior, al césped, a la lluvia sobre la cara. ' \
               'A que de vez en cuando nos cosan con yeso alguna grieta. ' \
               'Todo esto es nuevo para nosotros. ' \
               'Sólo queríamos cambiar de vida. ' \
               'Intentaron desanimarnos diciéndonos que otros lo habían intentado antes y habían fracasado. '\
               'Pensamos que sólo querían retenernos, pero tenían razón. ' \
               'Tenemos que irnos. ' \
               'No sé cuánto tiempo me llevará convencerle, pero tiene que pensar que lo hace por mí,' \
               'porque no entiende que está desquiciado.'
        tagger = SyntacticTagger()
        tags = tagger.tag_text(text)
        print('\n'.join([token + ': ' + tag + ' (' + lemma + ')' for sentence in tags for token, tag, lemma in
                         sentence]))
        pass


if __name__ == "__main__":
    SyntacticTagger.test()
