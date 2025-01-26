import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize, word_tokenize

# Definir um Tokenizer Customizado
class CustomTokenizer:
    def to_sentences(self, text):
        return sent_tokenize(text)  # Usando sent_tokenize do nltk

    def to_words(self, text):
        return word_tokenize(text)  # Usando word_tokenize do nltk

# Baixar o pacote necessário
nltk.download('punkt')
nltk.download('punkt_tab')  # Garantir que o punkt_tab também seja baixado

html_text_tags = ("<p>", "</p>", "<h1>", "</h1>", "<h2>", "</h2>", "<h3>", "</h3>", "<h4>", "</h4>", "<h5>", "</h5>", "<h6>", "</h6>", 
    "<b>", "</b>", "<i>", "</i>", "<u>", "</u>", "<strong>", "</strong>", "<em>", "</em>", "<mark>", "</mark>",
    "<blockquote>", "</blockquote>", "<q>", "</q>", "<code>", "</code>",  
    "<br>", "<hr>",                              
    "<span>", "</span>", "<div>", "</div>",      
    "<a>", "</a>", "<abbr>", "</abbr>", "<cite>", "</cite>", "<time>", "</time>",               
    "<s>", "</s>", "<del>", "</del>", "<ins>", "</ins>", "<sub>", "</sub>", "<sup>", "</sup>",  
    "<small>", "</small>", "<kbd>", "</kbd>", "<samp>", "</samp>",                  
    "<address>", "</address>", "<bdi>", "</bdi>", "<bdo>", "</bdo>", "\n", "'", '"', ";", '“')

def resumirTexto(texto):
    

    # Usar o Tokenizer customizado
    tokenizer = CustomTokenizer()

    # Parser e summarizer
    parser = PlaintextParser.from_string(texto, tokenizer)
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 8) 

    textoFinal = ""
    # Imprimir o resumo
    for sentence in summary:
        textoFinal += str(sentence)


    for caractere in html_text_tags:
        textoFinal = textoFinal.replace(caractere, '')

    print(textoFinal)
    return textoFinal

if __name__ == '__main__':
    texto = """  <h1>Cientistas Descobrem Vida em Marte!</h1>

        <p><strong>Marte, 23 de janeiro de 2025</strong> - Uma equipe de cientistas internacionais fez uma descoberta revolucionária: foi encontrada vida em Marte! Após anos de pesquisa e exploração, sinais de organismos microscópicos foram detectados em amostras coletadas por sondas espaciais.</p>
        
        <p>A pesquisa, liderada pela renomada Dra. Juliana Martins, revelou que os microrganismos encontrados em Marte possuem características semelhantes às bactérias terrestres. A descoberta pode alterar completamente o entendimento da ciência sobre a origem da vida no universo.</p>
        
        <p>“Este é um marco histórico. Encontrar vida fora da Terra é a confirmação de que estamos não apenas explorando novos planetas, mas realmente conectando os pontos sobre como a vida pode surgir em diferentes ambientes", disse Dra. Martins em uma coletiva de imprensa.</p>
        
        <p>Especialistas acreditam que a descoberta poderá abrir portas para novas tecnologias e até mesmo viagens interplanetárias, visando a criação de colônias humanas em Marte.</p>
        
        <p>Embora a descoberta seja empolgante, cientistas alertam que mais estudos são necessários para entender como esses microrganismos se desenvolveram e se poderiam representar algum risco à saúde humana no futuro.</p>
        
        <p>“Este é apenas o começo de uma nova era. A ciência está evoluindo rapidamente, e Marte pode ser apenas o primeiro de muitos planetas que vamos explorar em busca de vida”, afirmou o professor Carlos Siqueira, um dos principais colaboradores da pesquisa.</p>
        
        <p>Fique atento às próximas atualizações sobre essa incrível descoberta. Em breve, mais detalhes serão divulgados em um estudo científico completo, que promete mudar a forma como vemos o cosmos.</p>
    """
    resumirTexto(texto)