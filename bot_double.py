import requests
from telegram_service import TelegramFunctions
import keyboard

def main(token):
    """
    Função principal que monitora o jogo Blaze Double e envia mensagens via Telegram.

    Essa função faz uma verificação contínua do estado do jogo e, com base nas condições, envia mensagens
    para um bot do Telegram usando a biblioteca 'telegram_service'.

    O jogo Blaze Double é monitorado para detectar quando entrar no preto (Black) ou no vermelho (Red) e
    fazer uma aposta correspondente. Também verifica a sequência de três vezes a cor vermelha e aposta no vermelho se a sequência ocorrer.

    Certifique-se de que o token do bot do Telegram ('telegram') esteja configurado corretamente.

    Para interromper a execução, você pode interromper o programa pressionando a tecla Space(espaço).

    """

    telegram = TelegramFunctions(token)

    mensagem_black = '''🚨 Entrada Confirmada 🚨\n⬛ Entrar no Preto ⬛\n⚠️ Fazer 1 Giro ⚠️\n🎰 Blaze Double: 🎰\n🔗 https://blaze.com/pt/games/double 🔗'''
    mensagem_red = '''🚨 Entrada Confirmada 🚨\n🟥 Entrar no Vermelho 🟥\n⚠️ Fazer 1 Giro ⚠️\n🎰 Blaze Double: 🎰\n🔗 https://blaze.com/pt/games/double 🔗'''

    id = ''
    while keyboard.is_pressed('space') == False:
        dados = requests.get('https://blaze.com/api/roulette_games/recent').json()
        double = [[dado['id'],dado['roll'],dado['color']]for dado in dados]

        print(double[0][1])
        if double[0][1] == 14:
            telegram.send_aposta(mensagem_black)
            telegram.conferir_aposta(double[0][0], double[0][2])
        
        elif double[0][1] == 8 and all(1 == num[2] for num in double[1:3]):
            telegram.send_aposta(mensagem_black)
            telegram.conferir_aposta(double[0][0], double[0][2])

        elif id != double[0][0] and double[0][2] == 1:
            id = double[0][0]
            contador = 1
            while keyboard.is_pressed('space') == False:
                print(double[0][1])
                double = requests.get('https://blaze.com/api/roulette_games/recent').json()
                double_id = [resultado['id'] for resultado in double]
                double_cor = [resultado['color'] for resultado in double]
                if id != double[0][0] and double[0][2] == 1:
                    id = double[0][0]
                    contador += 1
                elif id != double[0][0] and double[0][2] in [0,2]:
                    break
                elif contador == 3:
                    telegram.send_aposta(mensagem_red)
                    telegram.conferir_aposta(double[0][0], double[0][2])
                    break
        
if __name__ == '__main__':
    main('SEU_TOKEN_AQUI')