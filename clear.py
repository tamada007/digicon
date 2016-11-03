
from libsm120 import digiscale
from libsm120 import entity

sm120 = digiscale.DigiSm120("192.168.68.200")

plumt = entity.PluMaster()
flbmt = entity.FlbMaster()
mubmt = entity.MubMaster()
tbtmt = entity.TbtMaster()
spmmt = entity.SpmMaster()
ingmt = entity.IngMaster()
texmt = entity.TexMaster()
trbmt = entity.TrbMaster()
trtmt = entity.TrtMaster()
trgmt = entity.TrgMaster()


sm120.connect()

sm120.dele(plumt)
sm120.dele(flbmt)
sm120.dele(mubmt)
sm120.dele(tbtmt)
sm120.dele(spmmt)
sm120.dele(ingmt)
sm120.dele(texmt)
sm120.dele(trbmt)
sm120.dele(trtmt)
sm120.dele(trgmt)

