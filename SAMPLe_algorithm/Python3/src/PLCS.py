import random as rnd
def runPLCS(a, b, probability):
  return internalsPLCS(a, b, probability, 0)
def internalsPLCS(a, b, probability, currentPLCS):
  try:
    if head(a) == head(b):
      return internalsPLCS(tail(a), tail(b), probability, currentPLCS + 1)
    else:
      if rnd.random() < (probability / 4):
        return internalsPLCS(tail(a), tail(b), probability, currentPLCS + 1)
      else:
        return internalsPLCS(tail(a), tail(b), probability, currentPLCS)
  except IndexError:
    return currentPLCS
def tail(ls):
  return ls[1:]
def head(ls):
  return ls[0]