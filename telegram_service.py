import requests

class TelegramFunctions:
    """
    Uma classe que fornece funcionalidades para interagir com o Telegram Bot API.

    Esta classe é projetada para enviar mensagens e imagens para um chat específico do Telegram
    usando um token de bot Telegram. Ela também inclui métodos para verificar o resultado de
    apostas em um jogo.

    Args:
        token (str): O token de autenticação do bot do Telegram.

    Atributos:
        url_base (str): A URL base da API do Telegram com o token de autenticação.
        chat_id (int): O ID do chat Telegram para onde as mensagens serão enviadas.

    Métodos:
        - send_aposta(mensagem): Envia uma mensagem de aposta para o chat Telegram.
        - conferir_aposta(id, color): Monitora o resultado de uma aposta no jogo Blaze Double e envia uma mensagem de resultado.
        - send_resultado(vitoria=False): Envia uma imagem ou mensagem de resultado (vitória ou derrota) para o chat Telegram.

    """

    def __init__(self,token):
        """
        Inicializa a classe com o token de autenticação e obtém o ID do chat Telegram.

        Args: 
            token (str): O token de autenticação do bot do Telegram.

        """

        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.chat_id = requests.get(f'{self.url_base}getUpdates').json()['result'][0]['channel_post']['sender_chat']['id']

    def send_aposta(self,mensagem):
        """
        Envia uma mensagem para o chat Telegram.

        Args:
            mensagem (str): A mensagem a ser enviada.

        """

        requests.get(f'{self.url_base}sendMessage?chat_id={self.chat_id}&text={mensagem}&disable_web_page_preview=True')

    def send_resultado(self,vitoria):
        """
        Envia uma imagem e mensagem de resultado (vitória ou derrota) para o chat Telegram.

        Args:
            vitoria (bool): Se True, indica que a aposta foi vencida. Caso contrário, assume-se que a aposta foi perdida.

        """

        img_win = 'https://i.ibb.co/C0ChS0D/win.jpg'
        img_loss = 'https://i.ibb.co/59GsVVs/loss.jpg'
        if vitorio:
            if requests.get(img_win).status_code != 404:
                requests.get(f'{self.url_base}sendPhoto?chat_id={self.chat_id}&photo={img_win}')
            else:
                mensagem_win = '''🟩🟩🟩 Win 🟩🟩🟩'''
                self.send_aposta(mensagem_win)
        else:
            if requests.get(img_loss).status_code != 404:
                requests.get(f'{self.url_base}sendPhoto?chat_id={self.chat_id}&photo={img_loss}')
            else:    
                mensagem_loss =  '''🟥🟥🟥 Loss 🟥🟥🟥'''
                self.send_aposta(mensagem_loss)

    def conferir_aposta(self,id,color):
        """
        Monitora o resultado de uma aposta no jogo Blaze Double e envia uma mensagem de resultado.

        Args:
            id (int): O ID da aposta a ser monitorada.
            color (int): A cor da aposta (1 para Vermelho, 2 para Preto).

        """

        if color == 2:
            while True:
                resultado = requests.get('https://blaze.com/api/roulette_games/recent').json()
                if id != resultado[0]['id'] and resultado[0]['color'] == 2:
                    self.send_resultado(vitoria=True)
                    break
                elif id != resultado[0]['id'] and resultado[0]['color'] != 2:
                    self.send_resultado(vitoria=False)
                    break
        else:
            while True:
                resultado = requests.get('https://blaze.com/api/roulette_games/recent').json()
                if id != resultado[0]['id'] and resultado[0]['color'] == 1:
                    self.send_resultado(vitoria=True)
                    break
                elif id != resultado[0]['id'] and resultado[0]['color'] != 1:
                    self.send_resultado(vitoria=False)
                    break