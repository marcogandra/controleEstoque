# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView
from Views.mainProdutos import Ui_ct_MainProdutos
from Views.formProdutos import Ui_ct_FormProdutos
from Crud.CrudProdutos import CrudProdutos
from functools import partial
import os


class MainProdutos(Ui_ct_MainProdutos, Ui_ct_FormProdutos):

    def mainprodutos(self, frame):
        super(MainProdutos, self).setMainProdutos(frame)
        self.frameMainProdutos.show()

        # Icone Botoes
        self.IconeBotaoForm(self.bt_AddNovoProduto,
                            self.resourcepath('Images/addNovo.svg'))
        self.IconeBotaoMenu(self.bt_BuscaProduto,
                            self.resourcepath('Images/search.png'))
        self.IconeBotaoMenu(self.bt_PrintRelatProdutos,
                            self.resourcepath('Images/gtk-print.png'))

        # Desabiltando Signals tabela
        self.tb_produtos.blockSignals(True)

        # Tamanho campos tabela
        self.tb_produtos.setColumnHidden(0, True)
        self.tb_produtos.setColumnWidth(1, 10)
        self.tb_produtos.setColumnWidth(2, 40)
        self.tb_produtos.setColumnWidth(3, 450)
        self.tb_produtos.setColumnWidth(4, 80)
        self.tb_produtos.setColumnWidth(5, 147)
        self.tb_produtos.setColumnWidth(6, 147)
        self.tb_produtos.setColumnWidth(7, 40)

        # Populando tabela produtos
        self.DataTabProdutos()

        # Busca produto
        self.tx_BuscaProduto.textEdited.connect(self.DataTabProdutos)

        # Botao Adicionar Produto
        self.bt_AddNovoProduto.clicked.connect(self.FormProdutos)

        # Botao Imprimir Produtos
        self.bt_PrintRelatProdutos.clicked.connect(self.imprimirProdutos)

        # Dados Tabela Produto
    def DataTabProdutos(self):
        lista = CrudProdutos()
        busca = self.tx_BuscaProduto.text()
        lista.ListaProdutoTabela(busca)
        i = 0

        while self.tb_produtos.rowCount() > 0:
            self.tb_produtos.removeRow(0)

        if len(lista.descricaoProduto) >= 1:
            while i < len(lista.descricaoProduto):
                self.tb_produtos.insertRow(i)
                self.conteudoTabela(self.tb_produtos, i, 0,
                                    str(lista.idProduto[i]))
                self.TabelaStatus(self.tb_produtos, i, 1,
                                  self.StatusEntrega(1))
                self.TabelaID(self.tb_produtos, i, 2, lista.idProduto[i])
                self.TabelaNomeTelefone(self.tb_produtos, i, 3,
                                        lista.descricaoProduto[i], lista.marca[i])
                self.TabelaQtdeStatus(self.tb_produtos, i, 4,
                                      str(lista.qtdeProduto[i]),
                                      self.StatusStoque(lista.qtdeProduto[i],
                                                        lista.estoqueMinimo[i]))
                self.ValorProduto(self.tb_produtos, i, 5,
                                  lista.valorUnitario[i])
                self.ValorProduto(self.tb_produtos, i, 6,
                                  lista.valorAtacado[i])
                # Sinal click tabela
                self.botaoTabela(self.tb_produtos, i, 7,
                                 partial(
                                     self.SelectProduto, lista.idProduto[i]),
                                 "#005099")
                i += 1
        pass

    # Frame Formulário Produtos
    def FormProdutos(self):
        self.DesativaBotaoProdutos()
        self.LimpaFrame(self.ct_containerProdutos)
        super(MainProdutos, self).setFormProdutos(self.ct_containerProdutos)
        # Ocultando alguns Campos
        self.tx_AddCategoria.setHidden(True)
        self.tx_AddMarca.setHidden(True)
        self.bt_CalcelAddMarca.setHidden(True)
        self.bt_CancelAddCatergoria.setHidden(True)
        self.bt_DelImagem.setHidden(True)
        # Mostandro Frame
        self.fr_FormProdutos.show()

        # Icone Botoes
        self.IconeBotaoMenu(self.bt_SalvarProdutos,
                            self.resourcepath('Images/salvar.png'))
        self.IconeBotaoMenu(self.bt_CancelarProdutos,
                            self.resourcepath('Images/cancelar.png'))
        self.IconeBotaoMenu(self.bt_BuscaProduto,
                            self.resourcepath('Images/search.png'))
        self.IconeBotaoMenu(self.bt_AddImagem,
                            self.resourcepath('Images/edit-add.png'))
        self.IconeBotaoMenu(self.bt_DelImagem,
                            self.resourcepath('Images/edit-delete.png'))
        self.IconeBotaoMenu(self.bt_AddCategoriaProduto,
                            self.resourcepath('Images/edit-add.png'))
        self.IconeBotaoMenu(self.bt_AddMarcaProduto,
                            self.resourcepath('Images/edit-add.png'))

        self.IconeBotaoMenu(self.bt_CalcelAddMarca,
                            self.resourcepath('Images/edit-delete.png'))
        self.IconeBotaoMenu(self.bt_CancelAddCatergoria,
                            self.resourcepath('Images/edit-delete.png'))
        self.lb_qtdeMin.setPixmap(QtGui.QPixmap(
            self.resourcepath('Images/warnig.svg')))
        self.label_2.setPixmap(QtGui.QPixmap(
            self.resourcepath('Images/CodBarra.png')))

        # Checando se existe ID válido
        self.IdCheckProduto()

        # Validar campos Inteiros
        validar = QtGui.QIntValidator(1, 999, self)
        self.tx_EstoqueMaximoProduto.setValidator(validar)
        self.tx_EstoqueMinimoProduto.setValidator(validar)
        self.tx_MinimoAtacado.setValidator(validar)
        validarValor = QtGui.QDoubleValidator(0.50, 999.99, 2, self)
        validarValor.setNotation(QtGui.QDoubleValidator.StandardNotation)
        validarValor.setDecimals(2)
        # validarValor.setRange(000.50, 999.99, 2)
        self.tx_ValorCompraProduto.setValidator(validarValor)
        self.tx_ValorAtacadoProduto.setValidator(validarValor)
        self.tx_ValorUnitarioProduto.setValidator(validarValor)
        # Fim Valida Campos

        # Calculando Margem de lucro
        self.tx_ValorUnitarioProduto.textChanged.connect(
            partial(self.CalculoPorcentagem, self.tx_ValorUnitarioProduto,
                    self.tx_PorcentagemVarejo))
        self.tx_ValorAtacadoProduto.textChanged.connect(
            partial(self.CalculoPorcentagem, self.tx_ValorAtacadoProduto,
                    self.tx_PorcentagemAtacado))
        # Fim Calculo porcentagem

        # Botao Upload e Cancelar Imagem
        self.bt_AddImagem.clicked.connect(self.UploadImagem)
        self.bt_DelImagem.clicked.connect(self.DelImagem)

        # Botao Add Categoria e populando combobox e check
        self.modelCombo = self.cb_CategoriaProduto.model()
        self.ListaCategoria()
        self.bt_AddCategoriaProduto.clicked.connect(self.AddCategoria)
        self.tx_AddCategoria.returnPressed.connect(
            self.AddCategoriaDb)
        self.cb_CategoriaProduto.currentIndexChanged.connect(self.listaMarca)
        self.bt_CancelAddCatergoria.clicked.connect(
            partial(self.CalcelAdd, self.bt_CancelAddCatergoria,
                    self.bt_AddCategoriaProduto, self.tx_AddCategoria,
                    self.cb_CategoriaProduto))
        # Fim Add Categoria

        # Botao Add Marca
        self.bt_AddMarcaProduto.clicked.connect(self.AddMarca)
        self.tx_AddMarca.returnPressed.connect(self.AddMarcaDb)
        self.bt_CalcelAddMarca.clicked.connect(
            partial(self.CalcelAdd, self.bt_CalcelAddMarca,
                    self.bt_AddMarcaProduto, self.tx_AddMarca,
                    self.cb_MarcaProduto))
        # Fim Add Marca

        # Botão Voltar
        self.bt_CancelarProdutos.clicked.connect(self.janelaProdutos)

        # Botao Salvar
        self.bt_SalvarProdutos.clicked.connect(self.VerificaInputProduto)

    # Desativando Botões
    def DesativaBotaoProdutos(self):
        self.bt_AddNovoProduto.setEnabled(False)
        self.tx_BuscaProduto.setEnabled(False)
        self.bt_BuscaProduto.setEnabled(False)
    # Ativando Botes

    def AtivaBotaoProdutos(self):
        self.bt_AddNovoProduto.setEnabled(True)
        self.tx_BuscaProduto.setEnabled(True)
        self.bt_BuscaProduto.setEnabled(True)

    # upload Imagem
    def UploadImagem(self):
        Dialog = QtWidgets.QFileDialog()
        Dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)

        fname = Dialog.getOpenFileName(
            self, "Selecionar Imagem", "", "Image files (*.jpg *.png)")[0]

        self.lb_FotoProduto.setPixmap(QtGui.QPixmap(fname).scaledToWidth(
            150, QtCore.Qt.TransformationMode(QtCore.Qt.FastTransformation)))
        # self.lb_FotoProduto.setScaledContents(True)
        self.bt_AddImagem.setHidden(True)
        self.bt_DelImagem.setVisible(True)

    def DelImagem(self):
        self.lb_FotoProduto.clear()
        self.bt_DelImagem.setHidden(True)
        self.bt_AddImagem.setVisible(True)

    # checando campo Id se é Edicao ou Novo Produto
    def IdCheckProduto(self):
        if not self.tx_idProduto.text():
            busca = CrudProdutos()
            self.tx_idProduto.setText(str(busca.lastIdProduto()))

    # Lista combobox categoria
    def ListaCategoria(self):
        busca = CrudProdutos()
        busca.listaCategoria()
        i = 0
        while i < len(busca.categoria):
            self.cb_CategoriaProduto.addItem(
                busca.categoria[i], str(busca.idCategoria[i]))
            i += 1

    # Listando marca por categoria
    def listaMarca(self, index):
        self.cb_MarcaProduto.clear()
        # self.cb_CategoriaProduto.clear()
        self.cb_MarcaProduto.addItem("SELECIONE")
        busca = CrudProdutos()

        if self.cb_CategoriaProduto.count() > 0:
            id = self.cb_CategoriaProduto.currentData()
            busca.idCategoria = id
        busca.listaMarca()
        i = 0
        while i < len(busca.marca):
            self.cb_MarcaProduto.addItem(
                busca.marca[i], str(busca.idMarca[i]))
            i += 1
            pass
        # self.cb_MarcaProduto.addItems(busca.marca)
        # cindex = self.cb_MarcaProduto.findData('4')
        # self.cb_MarcaProduto.setCurrentIndex(cindex)

    # Funcao Botao Add Categoria e marca
    def AddMarca(self):
        self.cb_MarcaProduto.setHidden(True)
        self.bt_AddMarcaProduto.setHidden(True)
        self.bt_CalcelAddMarca.setVisible(True)
        self.tx_AddMarca.setVisible(True)
        self.tx_AddMarca.setFocus()

    def AddCategoria(self):
        self.cb_CategoriaProduto.setHidden(True)
        self.bt_AddCategoriaProduto.setHidden(True)
        self.bt_CancelAddCatergoria.setVisible(True)
        self.tx_AddCategoria.setVisible(True)
        self.tx_AddCategoria.setFocus()
    # Fim Botoes Categoria e Marca

    # Cancelado Add Marca / Categoria
    def CalcelAdd(self, *args):
        args[0].setHidden(True)
        args[1].setVisible(True)
        args[2].setHidden(True)
        args[3].setVisible(True)
        args[3].setFocus()

    # Add Marca Banco de Dados
    def AddMarcaDb(self):
        rowMarca = self.cb_MarcaProduto.count()
        INSERT = CrudProdutos()
        self.cb_MarcaProduto.addItem(
            self.tx_AddMarca.text(), str(INSERT.lastIdMarca()))
        self.tx_AddMarca.setHidden(True)
        self.cb_MarcaProduto.setVisible(True)
        self.cb_MarcaProduto.setCurrentIndex(rowMarca)
        self.tx_AddMarca.clear()
        INSERT.idCategoria = self.cb_CategoriaProduto.currentIndex()
        INSERT.marca = self.cb_MarcaProduto.currentText()
        INSERT.Addmarca()
        self.CalcelAdd(self.bt_CalcelAddMarca,
                       self.bt_AddMarcaProduto, self.tx_AddMarca,
                       self.cb_MarcaProduto)

    # Add Categoria Banco de Dados
    def AddCategoriaDb(self):
        rowCategoria = self.cb_CategoriaProduto.count()
        INSERT = CrudProdutos()
        self.cb_CategoriaProduto.addItem(
            self.tx_AddCategoria.text(), INSERT.lasIdcategoria())
        self.tx_AddCategoria.setHidden(True)
        self.cb_CategoriaProduto.setVisible(True)
        INSERT.idCategoria = INSERT.lasIdcategoria()
        INSERT.categoria = self.tx_AddCategoria.text()
        INSERT.AddCategoria()
        self.tx_AddCategoria.clear()

        self.CalcelAdd(self.bt_CancelAddCatergoria,
                       self.bt_AddCategoriaProduto, self.tx_AddCategoria,
                       self.cb_CategoriaProduto)
        self.cb_CategoriaProduto.setCurrentIndex(rowCategoria)

    # Calculo porcentagem
    def CalculoPorcentagem(self, *args):
        if self.tx_ValorCompraProduto.text().replace(',', '.'):
            if float(self.tx_ValorCompraProduto.text().replace(',', '.')) > float(0):
                if args[0].text().replace(',', '.') and float(args[0].text().replace(',', '.')) > 0:
                    lucro = float(args[0].text().replace(',', '.')) - \
                        float(self.tx_ValorCompraProduto.text().replace(',', '.'))
                    lucro = lucro / \
                        float(args[0].text().replace(',', '.')) * 100
                args[1].setText(format(lucro, ".2f"))

    # Verificando Inputs
    def VerificaInputProduto(self):
        if not self.tx_DescricaoProduto.text():
            self.tx_DescricaoProduto.setFocus()
        elif self.cb_CategoriaProduto.currentIndex() == 0:
            self.cb_CategoriaProduto.setFocus()
        elif self.cb_MarcaProduto.currentIndex() == 0:
            self.cb_MarcaProduto.setFocus()
        elif not self.tx_EstoqueMinimoProduto.text():
            self.tx_EstoqueMinimoProduto.setFocus()
        elif not self.tx_EstoqueMaximoProduto.text():
            self.tx_EstoqueMaximoProduto.setFocus()
        elif not self.tx_ValorCompraProduto.text():
            self.tx_ValorCompraProduto.setFocus()
        elif not self.tx_ValorUnitarioProduto.text():
            self.tx_ValorUnitarioProduto.setFocus()
        elif not self.tx_ValorAtacadoProduto.text():
            self.tx_ValorAtacadoProduto.setFocus()
        elif not self.tx_MinimoAtacado.text():
            self.tx_MinimoAtacado.setFocus()
        else:
            self.cadProduto()
        pass

        # Cadastro Produto
    def cadProduto(self):
        INSERI = CrudProdutos()
        INSERI.idProduto = self.tx_idProduto.text()
        INSERI.descricaoProduto = self.tx_DescricaoProduto.text().upper()
        if self.lb_FotoProduto.pixmap():
            imagem = QtGui.QPixmap(self.lb_FotoProduto.pixmap())
            data = QtCore.QByteArray()
            buf = QtCore.QBuffer(data)
            imagem.save(buf, 'PNG')
            INSERI.imagemProduto = str(data.toBase64(), encoding='utf8')

        INSERI.idCategoria = self.cb_CategoriaProduto.currentData()
        INSERI.idMarca = self.cb_MarcaProduto.currentData()
        INSERI.estoqueMinimo = self.tx_EstoqueMinimoProduto.text()
        INSERI.estoqueMaximo = self.tx_EstoqueMaximoProduto.text()
        INSERI.obsProduto = self.tx_ObsProduto.text()
        INSERI.valorCompra = self.tx_ValorCompraProduto.text()
        INSERI.valorUnitario = self.tx_ValorUnitarioProduto.text()
        INSERI.valorAtacado = self.tx_ValorAtacadoProduto.text()
        INSERI.qtdeAtacado = self.tx_MinimoAtacado.text()
        INSERI.cadProduto()

        self.janelaProdutos()

    # Selecionando Produto
    def SelectProduto(self, valor):
        id = valor
        self.FormProdutos()
        self.tx_idProduto.setText(str(id))
        busca = CrudProdutos()
        busca.SelectProdutoId(id)
        self.tx_DescricaoProduto.setText(busca.descricaoProduto)
        if busca.imagemProduto:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(
                QtCore.QByteArray.fromBase64(busca.imagemProduto))
            self.lb_FotoProduto.setPixmap(pixmap.scaledToWidth(
                150, QtCore.Qt.TransformationMode(QtCore.Qt.FastTransformation)))
            # self.lb_FotoProduto.setScaledContents(True)
            self.bt_AddImagem.setHidden(True)
            self.bt_DelImagem.setVisible(True)

        self.cb_CategoriaProduto.setCurrentIndex(
            self.cb_CategoriaProduto.findData(busca.idCategoria))
        self.cb_MarcaProduto.setCurrentIndex(
            self.cb_MarcaProduto.findData(busca.idMarca))
        self.tx_EstoqueMinimoProduto.setText(str(busca.estoqueMinimo))
        self.tx_EstoqueMaximoProduto.setText(str(busca.estoqueMaximo))
        self.tx_ObsProduto.setText(busca.obsProduto)
        self.tx_ValorCompraProduto.setText(busca.valorCompra)
        self.tx_ValorUnitarioProduto.setText(busca.valorUnitario)
        self.tx_ValorAtacadoProduto.setText(busca.valorAtacado)
        self.tx_MinimoAtacado.setText(str(busca.qtdeAtacado))

    # Imprimindo
    def imprimirProdutos(self):
        self.documento = QWebEngineView()

        headertable = ["Cod", "Descrição", "Disponível",
                       "Valor Unitário", "Valor Atacado", 'Min. Atacado']
        busca = CrudProdutos()
        busca.ListaProdutoTabela(self.tx_BuscaProduto.text())
        html = self.renderTemplate(
            "estoque.html",
            estilo=self.resourcepath('Template/estilo.css'),
            titulo="LISTAGEM PRODUTOS",
            headertable=headertable,
            codProduto=busca.idProduto,
            descPRoduto=busca.descricaoProduto,
            qtdeEstoque=busca.qtdeProduto,
            valorUnitario=busca.valorUnitario,
            valorAtacado=busca.valorAtacado,
            qtdeAtacado=busca.qtdeAtacado

        )

        self.documento.load(QtCore.QUrl("file:///" +
                                        self.resourcepath("report.html")))
        self.documento.loadFinished['bool'].connect(self.previaImpressao)
