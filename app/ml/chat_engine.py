import re
from typing import List, Optional


class ChatEngine:
    def generate_response(
        self,
        message: str,
        context: Optional[str] = None,
        zones: Optional[List[dict]] = None,
        user_name: str = "Motorista",
        user_earnings: float = 0,
        user_rides: int = 0,
    ) -> str:
        msg = message.lower().strip()

        top_zones = zones[:5] if zones else []
        top_name = top_zones[0]["name"] if top_zones else "n/a"
        top_score = top_zones[0]["score"] if top_zones else 0
        top_earnings = top_zones[0]["earnings_per_hour"] if top_zones else 0
        top_wait = top_zones[0]["wait_time"] if top_zones else 0

        if any(w in msg for w in ["melhor local", "melhor região", "onde ir", "recomenda"]):
            return (
                f"Com base nos dados em tempo real, a melhor região agora é:\n\n"
                f"📍 **{top_name}** — Score {top_score}/100\n"
                f"💰 Ganho estimado: R$ {top_earnings:.2f}/h\n"
                f"⏱ Espera média: {top_wait} min\n\n"
                f"📊 Previsão:\n"
                f"• Próximos 15min: Demanda {'crescendo' if top_zones[0].get('predicted_15m', 0) > 0.5 else 'estável'}\n"
                f"• Próximos 30min: {'Alta probabilidade de corridas longas' if top_zones[0].get('predicted_30m', 0) > 0.6 else 'Demanda moderada'}\n\n"
                + ("💡 Dica: Ative o Modo Economia para maximizar seus ganhos." if user_earnings > 0 else "")
            )

        if any(w in msg for w in ["aeroporto", "airport"]):
            airport_zone = next((z for z in zones if "aeroport" in z["name"].lower()), None)
            if airport_zone:
                return (
                    f"✅ **Aeroporto** é uma excelente escolha!\n\n"
                    f"Score: {airport_zone['score']}/100\n"
                    f"Ganho médio: R$ {airport_zone['earnings_per_hour']:.2f}/h\n"
                    f"Demanda: {'Alta' if airport_zone['demand'] > 0.7 else 'Média'}\n"
                    f"Concorrência: {'Baixa' if airport_zone.get('competition', 5) < 3 else 'Moderada'}\n\n"
                    f"📌 {_get_airport_tip()}"
                )
            return "No momento o aeroporto não está entre as regiões mais aquecidas. Recomendo verificar o ranking completo."

        if any(w in msg for w in ["centro", "centro", " downtown"]):
            center_zone = next((z for z in zones if "centro" in z["name"].lower()), None)
            if center_zone:
                return (
                    f"📍 **Centro** — Score {center_zone['score']}/100\n\n"
                    f"💰 R$ {center_zone['earnings_per_hour']:.2f}/h\n"
                    f"⏱ Espera: {center_zone['wait_time']} min\n"
                    f"🚦 Trânsito: {_get_traffic_level(center_zone.get('competition', 3))}\n\n"
                    f"Vale a pena sim! O centro tem demanda consistente e tarifas dinâmicas frequentes."
                )
            return "O centro não está no top 10 no momento. Que tal verificar outras regiões?"

        if any(w in msg for w in ["vale a pena", "lucrativ", "ganhar mais", "renda", "faturar"]):
            table = "🏆 **Top Regiões por Rentabilidade:**\n\n"
            for i, z in enumerate(top_zones[:5], 1):
                stars = "⭐" * max(1, z["score"] // 25)
                table += f"{i}. **{z['name']}** {stars} {z['score']}/100\n"
                table += f"   • R$ {z['earnings_per_hour']:.2f}/h | Espera: {z['wait_time']} min\n"
            return table + "\n💡 Dica: Regiões com score > 80 oferecem o melhor custo-benefício."

        if any(w in msg for w in ["próxim", "previsão", "vai aquecer", "daqui a", "minutos"]):
            return (
                f"📊 **Previsão para os próximos minutos:**\n\n"
                f"🔮 **15 min:** {top_name} deve continuar aquecido\n"
                f"🔮 **30 min:** {top_zones[1]['name'] if len(top_zones) > 1 else top_name} tende a crescer\n"
                f"🔮 **60 min:** {top_zones[2]['name'] if len(top_zones) > 2 else 'Mudanças no padrão'} pode ser a melhor opção\n\n"
                f"Baseado em: padrões históricos + condições atuais de trânsito e clima."
            )

        if any(w in msg for w in ["olá", "oi", "bom dia", "boa tarde", "boa noite", "hey"]):
            return (
                f"Olá {user_name}! 👋\n\n"
                f"Sou seu copiloto inteligente do DriverAI Pro. "
                f"Posso ajudar com:\n\n"
                f"📍 Melhores regiões para trabalhar\n"
                f"📊 Previsão de demanda\n"
                f"💰 Análise de rentabilidade\n"
                f"🚗 Dicas personalizadas\n\n"
                f"O que você gostaria de saber?"
            )

        return (
            f"Analisando os dados em tempo real para sua pergunta:\n\n"
            f"📊 **Região recomendada:** {top_name} (Score: {top_score}/100)\n"
            f"💰 Ganho estimado: R$ {top_earnings:.2f}/h\n\n"
            f"Posso fornecer mais detalhes sobre:\n"
            f"• Previsão para os próximos minutos\n"
            f"• Regiões específicas (aeroporto, centro, shopping)\n"
            f"• Comparativo entre regiões\n"
            f"• Dicas de economia\n\n"
            f"Como posso ajudar melhor?"
        )


def _get_airport_tip() -> str:
    return "Aeroportos têm picos de demanda alinhados com chegadas de voos. Verifique o quadro de voos para maximizar suas corridas."


def _get_traffic_level(competition: int) -> str:
    if competition >= 4: return "Intenso"
    if competition >= 2: return "Moderado"
    return "Leve"
