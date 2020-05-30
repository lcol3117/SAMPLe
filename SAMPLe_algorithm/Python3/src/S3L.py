import functools as ft, random as rnd, math as math
class S3L_agent:
  def __init__(self, dims, mip, j):
    self.dims = dims 
    self.mip = mip 
    self.j = j 
    self.qtable = [] 
    self.epsilon = None 
  def updateQTable(self, policy, performance):
    nextentry = [policy, performance] 
    self.qtable.append(nextentry) 
  def selectPolicy(self):
    self.calcEpsilon() 
    try:
      initialpoint = self.generateAvoidancePoint() 
    except IndexError:
      initialpoint = list(map(
        lambda _ : rnd.random(),
        range(self.dims)
      )) 
    probabilisticmax = self.locateProbabilisticMax() 
    vectordelta = self.subVectors(initialpoint, probabilisticmax) 
    scalar = self.calcVectorDeltaScalar() 
    modifiedvectordelta = self.scalarVectorMultiply(vectordelta, scalar) 
    result = self.vectorSum(initialpoint, modifiedvectordelta) 
    return result
  def calcEpsilon(self):
    try: 
      qtablemax = ft.reduce(
        lambda a,x : x[1] if x[1] > a else a,
        self.qtable,
        float("-inf")
      ) 
      res = (qtablemax / self.mip) 
      if res >= 0.8:
        res = 0.8 + (((5 * (res - 0.8)) ** self.j) / 5) 
    except IndexError:
      res = 0 
    self.epsilon = res 
  def generateAvoidancePoint(self):
    initialvector = list(map(
      lambda _ : rnd.random(),
      range(self.dims)
    )) 
    iavgqtable = (3 / 4) * self.mip 
    possiblemins = list(filter(
      lambda x : x[1] < iavgqtable,
      self.qtable
    )) 
    possiblemaxs = list(filter(
      lambda x : x[1] >= iavgqtable,
      self.qtable
    )) 
    [possibleminvectors, possiblemaxvectors] = list(map(
      lambda x : list(map(
        lambda v : v[0],
        x
      )),
      [possiblemins, possiblemaxs]
    )) 
    closestmin = possibleminvectors[0] 
    bestdist = self.getL2NDist(closestmin, initialvector)
    for i in possibleminvectors:
      dist = self.getL2NDist(i, initialvector)
      if dist < bestdist:
        bestdist = dist 
        closestmin = i[:] 
    closestmax = possiblemaxvectors[0] 
    bestdist = self.getL2NDist(closestmax, initialvector)
    for i in possiblemaxvectors:
      dist = self.getL2NDist(i, initialvector)
      if dist < bestdist:
        bestdist = dist 
        closestmax = i[:] 
    ddelta = self.getL2NDist(closestmin, closestmax) 
    dmin = self.getL2NDist(initialvector, closestmin) 
    r = dmin / ddelta 
    if r < 0.5:
      tryagain = rnd.random() <= (r * self.epsilon) 
    else:
      tryagain = False 
    if tryagain:
      return self.generateAvoidancePoint() 
    else:
      return initialvector 
  def locateProbabilisticMax(self):
    e2 = self.epsilon / 2 
    ls = self.qtable[:] 
    ranking = sorted(ls, key = lambda x : x[1])[:] 
    r = list(reversed(ranking))[:] 
    for i in range(len(ranking)-1):
      if rnd.random() < e2:
        tmp = r[i+1][:] 
        r[i+1] = r[i][:] 
        r[i] = tmp[:] 
    newranking = r[:] 
    newtop = newranking[0][0] 
    return newtop 
  def calcVectorDeltaScalar(self):
    vectordeltascalar = self.epsilon ** self.j 
    return vectordeltascalar 
  def subVectors(self, pointa, pointb):
    regionpt = pointb[:] 
    r = list(range(self.dims))[:] 
    deltas = list(map(lambda i : (regionpt[i] - pointa[i]), r)) 
    return deltas 
  def scalarVectorMultiply(self, oldvector, scalar):
    newvector = list(map(lambda x : x * scalar, oldvector)) 
    return newvector 
  def vectorSum(self, a, b):
    r = list(range(self.dims))[:] 
    vsum = list(map(lambda i : (a[i] + b[i]), r)) 
    return vsum 
  def getL2NDist(self, a, b):
    sumd = ft.reduce(
      lambda a,x : a + ((x[0] - x[1]) ** 2),
      list(zip(a, b)),
      0
    ) 
    dist = math.sqrt(sumd) 
    return dist 
