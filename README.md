# funding_rate_momemtum

analysing funding rate/price momemtum

bot.py:
low latency bot finding 5 symbols with the 'most negative' funding rate adn 5 with the highest one through pairs with a bigger volume than 75% of ftx pairs,
then entering long for the 5 lowest and short for the 5 highest, rebalancing every hour.
