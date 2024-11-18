import tkinter as tk
from tkinter import messagebox
import random
from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk  # Biblioteca necessária para carregar JPEG/PNG

class GuessingGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Adivinhação - Tela de Cadastro")
        self.root.configure(bg='#282c34')
        self.root.attributes('-fullscreen', True)
        # Criar o Canvas para colocar a imagem de fundo
        canvas = Canvas(root, width=1920, height=1080)
        canvas.pack(fill="both", expand=True)

# Carregar a imagem usando PIL
        background_image = Image.open("/home/tainara/Downloads/foto.jpg")  # Altere o caminho conforme necessário
        background_image = ImageTk.PhotoImage(background_image)  # Converte a imagem para um formato compatível com Tkinter

# Colocar a imagem no Canvas
        canvas.create_image(0, 0, image=background_image, anchor="nw")
        # Dicionário de usuários e pontuações iniciais
        self.users = {"Tainara": 500, "Wanessa": 300}
        self.current_user = None  # Usuário logado atualmente
        self.points = 1000  # Pontos iniciais

        # Botão para fechar o jogo com um X vermelho
        close_button = tk.Button(self.root, text="X", command=self.root.quit, bg='red', fg='white', font=("Helvetica", 15, "bold"))
        close_button.place(relx=1.0, rely=0.0, anchor="ne")
        
        # Tela de Cadastro de Usuário
        self.create_login_screen()

    def create_login_screen(self):
        # Limpa a tela para a tela de cadastro
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        title = tk.Label(self.root, text="Cadastro de Usuário", bg='#282c34', fg='#61dafb', font=("Helvetica", 24))
        title.pack(pady=200)

        # Nome do Usuário
        self.user_label = tk.Label(self.root, text="Digite seu nome:", bg='#282c34', fg='#abb2bf', font=("Helvetica", 18))
        self.user_label.pack(pady=5)
        self.user_entry = tk.Entry(self.root, font=("Helvetica", 21))
        self.user_entry.pack(pady=5)

        close_button = tk.Button(self.root, text="X", command=self.root.quit, bg='red', fg='white', font=("Helvetica", 15, "bold"))
        close_button.place(relx=1.0, rely=0.0, anchor="ne")

        # Botão de Cadastrar/Login
        self.register_button = tk.Button(self.root, text="Cadastrar e Iniciar", command=self.register_user, bg='#61dafb', fg='black', font=("Helvetica", 18, "bold"))
        self.register_button.pack(pady=15)

    def register_user(self):
        user_name = self.user_entry.get().strip()
        if user_name:
            if user_name not in self.users:
                self.users[user_name] = 0  # Pontuação inicial de 0
            self.current_user = user_name
            self.create_difficulty_selection()  # Abre a tela de seleção de nível
        else:
            messagebox.showwarning("Erro", "Por favor, insira um nome válido.")

    def create_difficulty_selection(self):
        # Limpa a tela para a tela de seleção de dificuldade
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        header = tk.Label(self.root, text=f"Bem-vindo, {self.current_user}! Escolha um nível de dificuldade.", bg='#282c34', fg='#61dafb', font=("Helvetica", 24))
        header.pack(pady=200)

        # Caixa de escolha de dificuldade
        self.difficulty_var = tk.StringVar(value="1")
        self.difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, "1 - Fácil", "2 - Médio", "3 - Difícil")
        self.difficulty_menu.config(font=("Helvetica", 18))
        self.difficulty_menu.pack(pady=10)

        # Botão para iniciar o jogo com o nível selecionado
        start_game_button = tk.Button(self.root, text="Iniciar Jogo", command=self.start_game, bg='#61dafb', fg='black', font=("Helvetica", 18, "bold"))
        start_game_button.pack(pady=16)

    def start_game(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "1 - Fácil":
            self.max_attempts = 20
        elif difficulty == "2 - Médio":
            self.max_attempts = 15
        else:
            self.max_attempts = 6

        self.secret_number = random.randint(0, 100)
        self.attempts = 0
        self.points = 1000
        self.create_game_screen()

    def create_game_screen(self):
        # Limpa a tela para a tela de jogo
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        header = tk.Label(self.root, text=f"Bem-vindo, {self.current_user}! Boa sorte!", bg='#282c34', fg='#61dafb', font=("Helvetica", 24))
        header.pack(pady=200)

        # Caixa de inserção de número
        self.guess_label = tk.Label(self.root, text="Chute um número entre 0 e 100:", bg='#282c34', fg='#abb2bf', font=("Helvetica", 18))
        self.guess_label.pack(pady=5)

        self.guess_entry = tk.Entry(self.root, font=("Helvetica", 21))
        self.guess_entry.pack(pady=5)

        # Botão de Enviar
        self.submit_button = tk.Button(self.root, text="Enviar", command=self.check_guess, bg='#61dafb', fg='black', font=("Helvetica", 18, "bold"))
        self.submit_button.pack(pady=15)

        # Resultado
        self.result_label = tk.Label(self.root, text="", bg='#282c34', fg='#abb2bf', font=("Helvetica", 18))
        self.result_label.pack(pady=10)

        # Botão de jogar novamente, inicialmente escondido
        self.play_again_button = tk.Button(self.root, text="Jogar Novamente", command=self.play_again, bg='#61dafb', fg='black', font=("Helvetica", 18, "bold"))
        self.play_again_button.pack(pady=15)
        self.play_again_button.pack_forget()

        # Cria um frame para o ranking com uma borda
        ranking_frame = tk.Frame(self.root, bg='#282c34', bd=5, relief="solid")
        ranking_frame.place(x=1400, y=50, width=500, height=1000)  # Ajuste o tamanho conforme necessário

    # Label do Ranking
        self.ranking_label = tk.Label(ranking_frame, text="Ranking:", bg='#282c34', fg='#61dafb', font=("Helvetica", 20, "bold"))
        self.ranking_label.pack(pady=20)

    # Lista de ranking
        self.ranking_list = tk.Label(ranking_frame, text="", bg='#282c34', fg='#abb2bf', font=("Helvetica", 20))
        self.ranking_list.pack(pady=10)


        # Botão de fechar a janela
        close_button = tk.Button(self.root, text="X", command=self.root.quit, bg='red', fg='white', font=("Helvetica", 15, "bold"))
        close_button.place(relx=1.0, rely=0.0, anchor="ne")

        # Atualiza o ranking
        self.update_ranking()

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1
            self.guess_entry.delete(0, tk.END)

            if guess < 0:
                self.result_label.config(text="Você não pode chutar números negativos.")
                return

            if guess == self.secret_number:
                self.result_label.config(text=f"Parabéns, {self.current_user}! Você acertou e fez {self.points:.2f} pontos.")
                self.users[self.current_user] += int(self.points)
                self.update_ranking()
                self.play_again_button.pack()
            elif self.attempts >= self.max_attempts:
                self.result_label.config(text=f"Você perdeu! O número secreto era {self.secret_number}.")
                self.play_again_button.pack()
            else:
                if guess > self.secret_number:
                    self.result_label.config(text="Seu chute foi maior do que o número secreto!")
                else:
                    self.result_label.config(text="Seu chute foi menor do que o número secreto!")

                points_lost = abs(guess - self.secret_number)
                self.points -= points_lost
        except ValueError:
            self.result_label.config(text="Por favor, insira um número válido.")

    def play_again(self):
        self.secret_number = random.randint(0, 100)
        self.attempts = 0
        self.points = 1000
        self.result_label.config(text="")
        self.play_again_button.pack_forget()

    def update_ranking(self):
        ranking_text = "\n".join([f"{user}: {score} pontos" for user, score in sorted(self.users.items(), key=lambda x: x[1], reverse=True)])
        self.ranking_list.config(text=ranking_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameApp(root)
    root.mainloop()
