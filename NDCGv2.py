import math
import statistics

score = [0] * 10
optimal = [0] * 10
for i in range(10):
    fgoogle = open('query/google/google_query_' + str(i) + '.txt', 'r', encoding='utf-8')
    fbufale = open('query/trace_' + str(i) + '.txt', 'r', encoding='utf-8')
    resgoogle = fgoogle.readlines()
    resbufale = fbufale.readlines()

    for j in range(len(resgoogle)):
        resgoogle[j] = resgoogle[j].strip()
        if resgoogle[j][len(resgoogle[j])-1] == '/':
            resgoogle[j] = resgoogle[j][:len(resgoogle[j])-1]

    for j in range(len(resbufale)):
        resbufale[j] = resbufale[j].strip()
        if resbufale[j][len(resbufale[j])-1] == '/':
            resbufale[j] = resbufale[j][:len(resbufale[j])-1]

    for res in resbufale:
        if res in resgoogle:
            posgoogle = resgoogle.index(res)
            posbufale = resbufale.index(res)
            if posbufale == 0:  # se sono tra i risultati migliori di google allora do 3 punti
                score[i] += 6 / math.log2(max(posbufale+1, 2))  # così se è alla posizione 0 del nostro allora prende 2

            elif posbufale == 1: # se sono tra i primi 4 allora do 2 punti
                score[i] += 5 / math.log2(max(posbufale + 1, 2))

            elif posbufale == 2: # per gli altri, prima di 10, do 1
                score[i] += 4 / math.log2(max(posbufale + 1, 2))

            elif posbufale == 3:  # se sono tra i risultati migliori di google allora do 3 punti
                score[i] += 3 / math.log2(max(posbufale + 1, 2))  # così se è alla posizione 0 del nostro allora prende 2

            elif posbufale == 4:  # se sono tra i primi 4 allora do 2 punti
                score[i] += 2 / math.log2(max(posbufale + 1, 2))

            elif 4 < posbufale < 10:  # per gli altri, prima di 10, do 1
                score[i] += 1 / math.log2(max(posbufale + 1, 2))

    for res in resgoogle:
        posgoogle = resgoogle.index(res)
        if posgoogle == 0:  # se sono tra i risultati migliori di google allora do 3 punti
            optimal[i] += 6 / math.log2(max(posgoogle + 1, 2))  # così se è alla posizione 0 del nostro allora prende 2

        elif posgoogle == 1:  # se sono tra i primi 4 allora do 2 punti
            optimal[i] += 5 / math.log2(max(posgoogle + 1, 2))

        elif posgoogle == 2:  # per gli altri, prima di 10, do 1
            optimal[i] += 4 / math.log2(max(posgoogle + 1, 2))

        elif posgoogle == 3:  # se sono tra i risultati migliori di google allora do 3 punti
            optimal[i] += 3 / math.log2(max(posgoogle + 1, 2))  # così se è alla posizione 0 del nostro allora prende 2

        elif posgoogle == 4:  # se sono tra i primi 4 allora do 2 punti
            optimal[i] += 2 / math.log2(max(posgoogle + 1, 2))

        elif 4 < posgoogle < 10:  # per gli altri, prima di 10, do 1
            optimal[i] += 1 / math.log2(max(posgoogle + 1, 2))

print(score)
print(optimal)
ndcg = [score[i]/optimal[i] for i in range(10)]
print(ndcg)
print(statistics.mean(ndcg))
