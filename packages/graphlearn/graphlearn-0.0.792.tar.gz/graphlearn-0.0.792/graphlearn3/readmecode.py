from graphlearn3.lsgg import lsgg
from graphlearn3.util import util
import structout as so

gr = util.get_cyclegraphs()

sampler = lsgg()
sampler.fit(gr)
graphs =  list(sampler.neighbors(gr[0]))
so.gprint(graphs)
