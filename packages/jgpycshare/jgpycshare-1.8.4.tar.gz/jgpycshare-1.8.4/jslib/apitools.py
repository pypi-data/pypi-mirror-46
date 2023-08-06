import jgpycshare.jgencode
import json


class JGCheckSign:
    def __init__(self,otherpubkey,owerprikey):
        self.otherpubkey = otherpubkey
        self.owerprikey = owerprikey

    def getReqstCheck(self,appid,data,timespan,signnature):
        gsignstr = appid + data + timespan
        return jgpycshare.jgencode.JGRSA.ali_pub_check_signfor_key(gsignstr, signnature, self.otherpubkey)

    def toJson(self,appid,data,timespan):
        gsignstr =  appid + data + timespan
        sign = jgpycshare.jgencode.JGRSA.ali_pri_sign_key(gsignstr,self.owerprikey)
        bak = dict(
            data = data,
            timespan = timespan,
            sign = sign
        )
        return json.dumps(bak)