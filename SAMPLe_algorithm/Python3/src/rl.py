import S3L, environment
import random as rnd, math as math
global agentmodel
def realLearnStep():
  policy = agentmodel.selectPolicy()
  performance = environment.evaluatePolicy(policy)
  agentmodel.updateQTable(policy, performance)
  print("Agent tried policy {} with result {}. ".format(policy, performance))
  return [policy, performance]
def pureExplorationStep():
  policy = [ rnd.random() for _ in range(dims)]
  performance = environment.evaluatePolicy(policy)
  agentmodel.updateQTable(policy, performance)
  print("Agent explored policy {} with result {}. ".format(policy, performance))
def realLearning(accept):
  global agentmodel
  for _ in range(2):
    pureExplorationStep()
  notdone = True
  cnt = 1
  while notdone:
    realLearnStep()
    try:
      [bestpolicy, bestperformance] = list(reversed(sorted(
        agentmodel.qtable,
        key = lambda x : x[1]
      )))[0]
      notdone = bestperformance < accept
      print("NOT DONE" if notdone else "DONE")
    except:
      notdone = True
    print("{} steps have passed. ".format(cnt))
    cnt += 1
  top = list(reversed(sorted(agentmodel.qtable, key = lambda x : x[1])))[0]
  [policy, performance] = top
  return policy
def reinforcmentLearning(dims, mip, j, accept):
  global agentmodel
  agentmodel = S3l.S3L_agent(dims, mip, j)
  return realLearning(accept)
