from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkscrolledframe import ScrolledFrame
import requests
import webbrowser
from io import BytesIO
from googletrans import Translator

# Cores (branco e cinza)
cor_de_fundo = "#f0f0f0"  # Branco
cor_texto = "#333333"    # Cinza escuro
cor_destaque = "#cccccc" # Cinza claro
cor_card = "#ffffff"     # Branco para cards
cor_link = "#0000ff"     # Azul para links

# Configurações iniciais da janela
janela = Tk()
janela.title("Notícias")
janela.geometry("900x600")  # Tamanho padrão para a janela
janela.configure(bg=cor_de_fundo)
janela.resizable(width=False, height=False)

# Configurar os frames
frameCima = Frame(janela, bg=cor_de_fundo)
frameCima.pack(side=TOP, fill=X, padx=10, pady=10)

frameMeio = Frame(janela, bg=cor_de_fundo)
frameMeio.pack(side=TOP, fill=X, padx=10, pady=5)

frameBaixo = Frame(janela, bg=cor_de_fundo)
frameBaixo.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

# ScrolledFrame para exibir os resultados das notícias
sf = ScrolledFrame(frameBaixo, bg=cor_de_fundo)
sf.pack(side=LEFT, fill=BOTH, expand=True)

framecanva = sf.display_widget(Frame, bg=cor_de_fundo)

# Configuração da imagem e do título
app_imagem = Image.open("logo.png")
app_imagem = app_imagem.resize((70, 70))
app_imagem = ImageTk.PhotoImage(app_imagem)

app_logo = Label(frameCima, image=app_imagem, bg=cor_de_fundo, fg=cor_destaque)
app_logo.pack(side=LEFT, padx=10)

app_ = Label(frameCima, text="Automação de Pesquisa", font=("Verdana", 20, "bold"), bg=cor_de_fundo, fg=cor_destaque)
app_.pack(side=LEFT, padx=10)


# Campo de entrada e botão de pesquisa
app_busca = Label(frameMeio, text="Pesquisa", font=("Ivy", 12), bg=cor_de_fundo)
app_busca.pack(side=LEFT, padx=10)

app_busca_entrada = Entry(frameMeio, font=("Ivy", 12), bg=cor_de_fundo, fg=cor_texto, width=50)
app_busca_entrada.pack(side=LEFT, padx=10)

def abrir_link(url):
    webbrowser.open(url)

def obter_noticias():
    pesquisa = app_busca_entrada.get()
    api_key = "92c1bd82a83a4ac8a2c6af2613378686"
    translator = Translator()

    try:
        news_url = f"https://newsapi.org/v2/everything?q={pesquisa}&apiKey={api_key}"
        response = requests.get(news_url)
        response.raise_for_status()
        json_data = response.json()
        articles = json_data.get("articles", [])[:5]

        # Limpar frame anterior
        for widget in framecanva.winfo_children():
            widget.destroy()

        # Exibir resultados
        for i, article in enumerate(articles):
            titulo = article.get("title", "Sem título")
            url = article.get("url", "Sem URL")
            texto = article.get("description", "")
            imagem_url = article.get("urlToImage", "")

            # Traduzir título e texto
            try:
                titulo_traduzido = translator.translate(titulo, dest='pt').text
                texto_traduzido = translator.translate(texto, dest='pt').text
            except Exception:
                titulo_traduzido = titulo
                texto_traduzido = texto

            # Criar um frame para cada notícia
            news_frame = Frame(framecanva, bg=cor_card, padx=10, pady=10, relief=RAISED, borderwidth=1)
            news_frame.pack(pady=10, fill=X, padx=10)

            # Exibir imagem
            if imagem_url:
                try:
                    img_response = requests.get(imagem_url)
                    img_response.raise_for_status()
                    img_data = BytesIO(img_response.content)
                    img = Image.open(img_data)
                    img = img.resize((200, 150), Image.Resampling.LANCZOS)  # Proporção ajustada
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = Label(news_frame, image=img_tk, bg=cor_card)
                    img_label.image = img_tk  # Manter uma referência para a imagem
                    img_label.pack(side=LEFT, padx=5)
                except requests.exceptions.RequestException:
                    pass

            # Título da notícia
            lbl_titulo = Label(news_frame, text=f"{i + 1}. {titulo_traduzido}", font=("Ivy", 14, "bold"), bg=cor_card, fg=cor_texto, anchor="w", justify=LEFT, cursor="hand2", wraplength=550)
            lbl_titulo.pack(fill=X)

            # Texto da notícia
            lbl_texto = Label(news_frame, text=texto_traduzido, font=("Ivy", 12), bg=cor_card, fg=cor_texto, anchor="w", justify=LEFT, wraplength=550)
            lbl_texto.pack(fill=X, pady=5)

            # URL da notícia
            lbl_url = Label(news_frame, text=url, font=("Ivy", 12, "underline"), bg=cor_card, fg=cor_link, anchor="w", justify=LEFT, cursor="hand2", wraplength=550)
            lbl_url.pack(pady=2)
            lbl_url.bind("<Button-1>", lambda e, url=url: abrir_link(url))

        # Atualizar o scrollregion após adicionar o conteúdo
        framecanva.update_idletasks()
        sf._canvas.configure(scrollregion=sf._canvas.bbox("all"))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao obter notícias: {e}")

# Associar função ao botão de pesquisa
app_busca_button = Button(frameMeio, text="Pesquisar", width=12, bg=cor_destaque, command=obter_noticias)
app_busca_button.pack(side=RIGHT, padx=10)

# Configurar rolagem
def configurar_scroll():
    sf._canvas.configure(scrollregion=sf._canvas.bbox("all"))
    sf.bind_all("<MouseWheel>", lambda event: sf._canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

configurar_scroll()

janela.mainloop()
