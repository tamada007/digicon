from master import *


# import common.common
# import const

class MgpMaster(Master):
    def __init__(self):
        Master.__init__(self, "Mgp", 0x23, const.mgp_struct)


class PlaMaster(Master):
    def __init__(self):
        Master.__init__(self, "Pla", 0x39, const.pla_struct)


class PluMaster(Master):
    def __init__(self):
        Master.__init__(self, "Plu", 0x25, const.plu_struct)


class KasMaster(Master):
    def __init__(self):
        Master.__init__(self, "Kas", 0x41, const.kas_struct)


class PrfMaster(Master):
    def __init__(self):
        Master.__init__(self, "Prf", 0x34, const.prf_struct)


class TbtMaster(Master):
    def __init__(self):
        Master.__init__(self, "Tbt", 0xB0, const.tbt_struct)


class TrgMaster(Master):
    def __init__(self):
        Master.__init__(self, "Trg", 0x57, const.trg_struct)


class TrbMaster(Master):
    def __init__(self):
        Master.__init__(self, "Trb", 0xB3, const.trb_struct)


class TexMaster(Master):
    def __init__(self):
        Master.__init__(self, "Tex", 0x38, const.tex_struct)


class FlbMaster(Master):
    def __init__(self):
        Master.__init__(self, "Flb", 0x14, const.flb_struct)


class PtrMaster(Master):
    def __init__(self):
        Master.__init__(self, "Ptr", 0x2E, const.ptr_struct)


class PltMaster(Master):
    def __init__(self):
        Master.__init__(self, "Plt", 0x26, const.plt_struct)


class RtbMaster(Master):
    def __init__(self):
        Master.__init__(self, "Rtb", 0x51, const.rtb_struct)


class RttMaster(Master):
    def __init__(self):
        Master.__init__(self, "Rtt", 0x52, const.rtt_struct)


class ScdMaster(Master):
    def __init__(self):
        Master.__init__(self, "Scd", 0x4F, const.scd_struct)


class MasterFactory:
    def createMaster(self, master_name):
        master_list = {
            "Plu": lambda: PluMaster(),
            "Mgp": lambda: MgpMaster(),
            "Pla": lambda: PlaMaster(),
            # 			"Dep": lambda : DepMaster(),
            "Kas": lambda: KasMaster(),
            "Trg": lambda: TrgMaster(),
            "Trb": lambda: TrbMaster(),
            # 			"Trt": lambda : TrtMaster(),
            "Tbt": lambda: TbtMaster(),
            "Prf": lambda: PrfMaster(),
            # 			"Pff": lambda : PffMaster(),
            "Flb": lambda: FlbMaster(),
            # 			"Mub": lambda : MubMaster(),
            # 			"Spm": lambda : SpmMaster(),
            # 			"Ing": lambda : IngMaster(),
            "Tex": lambda: TexMaster(),
            "Plt": lambda: PltMaster(),
            # 			"Dpt": lambda : DptMaster(),
            # 			"Mgt": lambda : MgtMaster(),
            "Ptr": lambda: PtrMaster(),
            "Rtb": lambda: RtbMaster(),
            "Rtt": lambda: RttMaster(),
            "Scd": lambda: ScdMaster(),
        }
        if master_name in master_list:
            return master_list[master_name]()
        return None
