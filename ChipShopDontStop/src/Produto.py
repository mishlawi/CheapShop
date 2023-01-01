class Produto :
    strToda = ''
    nome = ''
    marca = ''
    quantidade = ''
    preco = ''
    ppu = ''
    promo = ''
    EANOriginal = ''
    EANCopiados = []

    def __init__(self) -> None:
        self.strToda = 'z'
        self.nome = 'z'
        self.marca = 'z'
        self.quantidade = 'z'
        self.preco = 'z'
        self.ppu = 'z'
        self.promo = 'z'
        self.EANOriginal = 'z'
        self.EANCopiados = ['','','']
    
    def __init__(self,strToda,nome,marca,quantidade,preco,ppu) -> None:
        self.strToda = strToda
        self.nome = nome
        self.marca = marca
        self.quantidade = quantidade
        self.preco = preco
        self.ppu = ppu
        self.promo = 'z'
        self.EANOriginal = 'z'
        self.EANCopiados = ['','','']

    def __init__(self,strToda,nome,marca,quantidade,preco,ppu,promo) -> None:
        self.strToda = strToda
        self.nome = nome
        self.marca = marca
        self.quantidade = quantidade
        self.preco = preco
        self.ppu = ppu
        self.promo = promo
        self.EANOriginal = 'z'
        self.EANCopiados = ['','','']

    def __str__(self) -> str:
        return "Produto{  ",self.strToda,'\'',"  }"

    def getEANOriginal(self):
        return self.EANOriginal
    
    def getEANCopiados(self):
        return self.EANCopiados

    def setEANOriginal(self,EANOriginal):
        self.EANOriginal = EANOriginal
    
    def setEANCopiados(self,EANCopiados):
        self.EANCopiados = EANCopiados

    def addEANCopiado(self,EAN):
        self.EANCopiados.append(EAN)

    def getStrToda(self):
        return self.strToda
    
    def setStrToda(self,strToda):
        self.strToda = strToda
    
    def getNome(self):
        return self.nome

    def setNome(self,nome):
        self.nome = nome
    
    def getMarca(self):
        return self.marca
    
    def setMarca(self,marca):
        self.marca = marca

    def getQuantidade(self):
        return self.quantidade

    def setQuantidade(self,quantidade):
        self.quantidade = quantidade
    
    def getPreco(self):
        return self.preco

    def getPreco(self,preco):
        self.preco = preco

    def getPPU(self):
        return self.ppu

    def getPPU(self,ppu):
        self.ppu = ppu

    def getPromo(self):
        return self.promo

    def getPromo(self,promo):
        self.promo = promo