import D3AC as D3AC, functools as ft, D3AC_N as D3AC_N
def cluster(data):
  currw = 0
  w_hist = []
  while currw < (D3AC.max2D(data) - D3AC.min2D(data)):
    currw += min([ min(map(abs, i)) for i in data]) / 2
    res = D3AC.cluster(data, currw)
    print("w of {} lead to {} clusters. ".format(currw, len(res)))
    if (len(res) != 1) and (len(res) != len(data)):
      if not (len(res) in [ i[0] for i in w_hist ]):
        w_hist.append([len(res), 1])
      else:
        for i in range(len(w_hist)):
          if w_hist[i][0] == len(res):
            w_hist[i] = [w_hist[i][0], w_hist[i][1] + 1]
  nmode = max(w_hist, key = lambda x : x[1])[0]
  res = D3AC_N.cluster(data, nmode)
  return res