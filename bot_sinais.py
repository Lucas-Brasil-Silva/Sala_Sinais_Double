import requests
from telegram_service import TelegramFunctions
import keyboard

def main():
    """
    Função principal que monitora o jogo Blaze Double e envia mensagens via Telegram.

    Essa função faz uma verificação contínua do estado do jogo e, com base nas condições, envia mensagens
    para um bot do Telegram usando a biblioteca 'telegram_service'.

    O jogo Blaze Double é monitorado para detectar quando entrar no preto (Black) ou no vermelho (Red) e
    fazer uma aposta correspondente. Também verifica a sequência de três vezes a cor vermelha e aposta no vermelho se a sequência ocorrer.

    Certifique-se de que o token do bot do Telegram ('telegram') esteja configurado corretamente.

    Para interromper a execução, você pode interromper o programa pressionando a tecla Space(espaço).

    """

    telegram = TelegramFunctions('6567594833:AAErr5EqdsuK-HswFlmUBdjoUuXhFF6aW64')

    mensagem_black = '''🚨 Entrada Confirmada 🚨\n⬛ Entrar no Preto ⬛\n⚠️ Fazer 1 Giro ⚠️\n🎰 Blaze Double: 🎰\n🔗 https://blaze.com/pt/games/double 🔗'''
    mensagem_red = '''🚨 Entrada Confirmada 🚨\n🟥 Entrar no Vermelho 🟥\n⚠️ Fazer 1 Giro ⚠️\n🎰 Blaze Double: 🎰\n🔗 https://blaze.com/pt/games/double 🔗'''
    id = ''
    while keyboard.is_pressed('space') == False:
        double = requests.get('https://blaze.com/api/roulette_games/recent').json()
        double_id = [resultado['id'] for resultado in double]
        double_num = [resultado['roll'] for resultado in double]
        double_cor = [resultado['color'] for resultado in double]
        
        if double_num[0] == 14:
            telegram.send_aposta(mensagem_black)
            telegram.conferir_aposta(double_id[0], double_cor[0])
        
        elif double_num[0] == 8 and all(1 == num for num in double_cor[1:3]):
            telegram.send_aposta(mensagem_black)
            telegram.conferir_aposta(double_id[0], double_cor[0])

        elif id != double_id[0] and double_cor[0] == 1:
            id = double_id[0]
            contador = 1
            while keyboard.is_pressed('space') == False:
                double = requests.get('https://blaze.com/api/roulette_games/recent').json()
                double_id = [resultado['id'] for resultado in double]
                double_cor = [resultado['color'] for resultado in double]
                if id != double_id[0] and double_cor[0] == 1:
                    id = double_id[0]
                    contador += 1
                elif id != double_id[0] and double_cor[0] in [0,2]:
                    break
                elif contador == 3:
                    telegram.send_aposta(mensagem_red)
                    telegram.conferir_aposta(double_id[0], double_cor[0])
                    break
        
if __name__ == '__main__':
    main()