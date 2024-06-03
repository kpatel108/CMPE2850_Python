# First voter that has >=51% of voters wins
# The way it works is that so long as no one has 51% of the votes,
# The bottom candidate is taken out and another voting round is run
# So this all starts with ballots generated (vote lists)
# Rounds to a winner
# And how many elections are held
import random
""""
        head = result[0].strip().split(',')
        data = [line.strip().split(',') for line in result[1:]]
        fresult = {(cand[1], cand[0]): int(cand[2]) for cand in data}


        candidlist = [rw for rw in rcw.keys()]
        weights = [rw for rw in rcw.values()]
"""


# Given current candidates and weighting, generate ballot sets of N
# ballots, using the weighting
# Provide initial ballot statistics..ie. % 1st, 2nd, etc, overall
# popularity to validate weighting

# Takes dict of candidates and weights, number of voters, and how many
# election rounds are held

"""
    Generate ballots

    a ballot is defined as a list of candidates with the first representing the 1st choice, and the highest index representing the last choice.
    given current candidates and weighting, generate ballot sets of N ballots, using the weighting
    provide initial ballot statistics..ie. % 1st, 2nd, etc, overall popularity to validate weighting

"""


def RunElection(cw,votes):

    #the candidates most voted for in the first round

    roundCount = 1
    elecRound = RunRound(cw,votes)

    winner = max(elecRound, key=lambda x: elecRound[x])
    loser = min(elecRound, key=lambda x: elecRound[x])
    print(f'Round {roundCount} Winner: {winner}, Votes: {elecRound[winner]} - Loser {loser}, Votes: {elecRound[loser]}')
    print(f'% of votes = {float(elecRound[winner])/int(votes)*100}')

    while(float(elecRound[winner])/int(votes)*100 < 51):
        roundCount += 1
        loserIndex = cw.index(loser)
        cw.pop(loserIndex)
        elecRound = RunRound(cw,votes)
        winner = max(elecRound, key=lambda x: elecRound[x])
        loser = min(elecRound, key=lambda x: elecRound[x])
        print(f'Round {roundCount} Winner: {winner}, Votes: {elecRound[winner]}/{votes} - Loser {loser}, Votes: {elecRound[loser]}/{votes}')
        print(f'Winner% of votes = {float(elecRound[winner])/int(votes)*100}')


    return elecRound

def RunRound(candids,voterCount):
    weights = [int(weight[2]) for weight in candids]

    #voted past on weighting and voter count
    eRound = random.choices(candids, weights=weights, k=int(voterCount))

    roundStats = {}
    for vote in eRound:
        if(roundStats.__contains__(vote)):
            roundStats[vote]+=1
        else:
            roundStats[vote]=1

    return roundStats


