import requests
import  xml.etree.ElementTree as ET


class Get_Address:
        
    def __request_WebService(self):
        
        try:
            #print(self.__cep)
            #url webservice passando o paramentro cep
            url="https://viacep.com.br/ws/{}/xml/".format(self.__cep)
            #informa o tipo do retorno que deseja do webservice (XML/JSon e etc).. Armazena em um dict
            retorno_xml={ 'Accept': 'application/xml' }
            #Realizando a requisição pro webservice com GET
            requisicao=requests.get(url,headers=retorno_xml)
            #Guardando o resultado da requição na bibilioteca xml.etree.ElementTree que nos ajudar a acessar as tags XML
            ELEMENTO=ET.ElementTree(ET.fromstring(requisicao.content))
            #agora só acessar as tags e atribuir em suas variaveis ou nos atributos da classe
            #atribuindo os valores nos atributos das classes.
            self.__logradouro = ELEMENTO.find("logradouro").text
            self.__bairro = ELEMENTO.find("bairro").text
            self.__cidade=ELEMENTO.find("localidade").text
            self.__uf=ELEMENTO.find("uf").text
            return 1

        except:
            print("Não foi possivel consultar no webservice, verifique se o CEP está correto ou se existe! ") 
            return 0
        


  
    #Definindo o metodo construtor    
    def __init__(self,CEP):
        
        CEP = CEP.replace("-","")
        CEP = CEP.replace("/","")
        CEP = CEP.replace(" ","")
        CEP = CEP.replace(".","")
        CEP = CEP.strip()
        self.__cep=CEP
        self.__logradouro=""
        self.__bairro=""
        self.__cidade=""
        self.__uf=""
        self.__request_WebService()  

    #Criando os metodos de acesso 
    @property
    def cep(self):
        return self.__cep
    @property
    def logradouro(self):
        return self.__logradouro
    @property
    def bairro(self):
        return self.__bairro
    @property
    def cidade(self):
        return self.__cidade
    @property
    def uf(self):
        return self.__uf
    
    @cep.setter
    def cep(self,new_cep):
        self.__cep=new_cep
        self.__request_WebService() 
    
    #metodo duck type, retornando a string do objeto, basta chamar print(objetoCriado), com metodos duck type deixamos nosso objeto mais "Pythonizado"
    def __str__(self):
        return f"Rua : {self.__logradouro} bairro:{self.__bairro} cidade: {self.__cidade} Estado: {self.__uf} cep:{self.__cep}"
        
        
    