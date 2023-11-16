import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QVBoxLayout, QPushButton, QMessageBox

class FormularioInscricao(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Inscrições para Evento")
        self.setGeometry(100, 100, 400, 300)

        self.cadastros_realizados = 0
        self.cadastros_restantes = 50
        self.nomes_cadastrados = set()
        self.cadastros = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label_cadastros = QLabel("Não há cadastros")
        layout.addWidget(self.label_cadastros)

        self.nome_label = QLabel("Nome e Sobrenome:")
        self.nome_input = QLineEdit()
        self.nome_input.setMaxLength(50)
        layout.addWidget(self.nome_label)
        layout.addWidget(self.nome_input)

        self.idade_label = QLabel("Qual a sua idade?")
        self.idade_input = QLineEdit()
        self.idade_input.setMaxLength(3)
        layout.addWidget(self.idade_label)
        layout.addWidget(self.idade_input)

        self.endereco_label = QLabel("Forneça o seu endereço:")
        self.endereco_input = QLineEdit()
        self.endereco_input.setMaxLength(50)
        layout.addWidget(self.endereco_label)
        layout.addWidget(self.endereco_input)

        self.reside_sp_checkbox = QCheckBox("Reside em SP?")
        layout.addWidget(self.reside_sp_checkbox)

        self.disponibilidade_noite_checkbox = QCheckBox("Você tem disponibilidade à noite?")
        layout.addWidget(self.disponibilidade_noite_checkbox)

        self.botao_cadastrar = QPushButton("Cadastrar")
        self.botao_cadastrar.clicked.connect(self.validar_cadastro)
        layout.addWidget(self.botao_cadastrar)

        self.setLayout(layout)

    def validar_cadastro(self):
        nome = self.nome_input.text()
        idade = self.idade_input.text()
        endereco = self.endereco_input.text()
        reside_sp = self.reside_sp_checkbox.isChecked()
        disponibilidade_noite = self.disponibilidade_noite_checkbox.isChecked()

        mensagens_erro = []

        if not nome or len(nome) < 3 or any(char.isdigit() for char in nome):
            mensagens_erro.append("O nome precisa ter pelo menos 3 caracteres e não pode conter números!")

        try:
            idade = int(idade)
            if idade < 18:
                mensagens_erro.append("O evento é proibido para menores de 18 anos!")
            elif idade <= 0:
                mensagens_erro.append("A idade precisa ser um número positivo!")
        except ValueError:
            mensagens_erro.append("A idade precisa ser um número inteiro!")

        if not endereco or len(endereco) < 4 or not any(char.isdigit() for char in endereco):
            mensagens_erro.append("O campo endereço precisa ser preenchido com nome da rua/avenida e número de residência!")

        if not disponibilidade_noite:
            mensagens_erro.append("O campo 'Tem disponibilidade à noite?' não foi marcado!")

        if not reside_sp:
            mensagens_erro.append("O campo 'Reside em SP?' não foi marcado!")

        if nome in self.nomes_cadastrados:
            mensagens_erro.append("Este nome já foi cadastrado!")

        if len(mensagens_erro) == 0:
            if self.cadastros_realizados < 50:
                self.cadastros_realizados += 1
                self.cadastros_restantes -= 1
                self.nomes_cadastrados.add(nome)
                self.cadastros.append({'Nome': nome, 'Idade': idade, 'Endereço': endereco, 'Reside em SP': reside_sp, 'Disponibilidade à noite': disponibilidade_noite})
                QMessageBox.information(self, "Cadastro Validado", f"Cadastro validado com sucesso!\nVagas restantes: {self.cadastros_restantes}")
            else:
                QMessageBox.warning(self, "As inscrições estão encerradas!", "Desculpe, as inscrições estão encerradas.")
        else:
            QMessageBox.warning(self, "Erro no Cadastro!", "\n".join(mensagens_erro))

        self.atualizar_label_cadastros()

    def atualizar_label_cadastros(self):
        if self.cadastros_realizados == 0:
            self.label_cadastros.setText("Não há cadastros!")
        else:
            self.label_cadastros.setText(f"Cadastros realizados: {self.cadastros_realizados}\nCadastros restantes: {self.cadastros_restantes}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    formulario = FormularioInscricao()
    formulario.show()
    sys.exit(app.exec_())
