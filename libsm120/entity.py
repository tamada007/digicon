import os
from master import *


# import const
# import common.common

class MgpMaster(Master):
    def __init__(self):
        file_struct = const.mgp_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(MgpMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(MgpMaster, self).__init__(file_abbr, file_struct)


class DatMaster(Master):
    def __init__(self):
        file_struct = const.dat_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(DatMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(DatMaster, self).__init__(file_abbr, file_struct)


class PlaMaster(Master):
    def __init__(self):
        file_struct = const.pla_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PlaMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PlaMaster, self).__init__(file_abbr, file_struct)


class PluMaster(Master):
    def __init__(self):
        file_struct = const.plu_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PluMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PluMaster, self).__init__(file_abbr, file_struct)


class DepMaster(Master):
    def __init__(self):
        file_struct = const.dep_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(DepMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(DepMaster, self).__init__(file_abbr, file_struct)


class KasMaster(Master):
    def __init__(self):
        file_struct = const.kas_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(KasMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(KasMaster, self).__init__(file_abbr, file_struct)


class TrgMaster(Master):
    def __init__(self):
        file_struct = const.trg_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(TrgMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(TrgMaster, self).__init__(file_abbr, file_struct)


class TrbMaster(Master):
    def __init__(self):
        file_struct = const.trb_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(TrbMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(TrbMaster, self).__init__(file_abbr, file_struct)


class TrtMaster(Master):
    def __init__(self):
        file_struct = const.trt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(TrtMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(TrtMaster, self).__init__(file_abbr, file_struct)


class TbtMaster(Master):
    def __init__(self):
        file_struct = const.tbt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(TbtMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(TbtMaster, self).__init__(file_abbr, file_struct)


class PrfMaster(Master):
    def __init__(self):
        file_struct = const.prf_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PrfMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PrfMaster, self).__init__(file_abbr, file_struct)


class PffMaster(Master):
    def __init__(self):
        file_struct = const.pff_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PffMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PffMaster, self).__init__(file_abbr, file_struct)


class FlbMaster(Master):
    def __init__(self):
        file_struct = const.flb_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(FlbMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(FlbMaster, self).__init__(file_abbr, file_struct)


class MubMaster(Master):
    def __init__(self):
        file_struct = const.mub_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(MubMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(MubMaster, self).__init__(file_abbr, file_struct)


class SpmMaster(Master):
    def __init__(self):
        file_struct = const.spm_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(SpmMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(SpmMaster, self).__init__(file_abbr, file_struct)


class IngMaster(Master):
    def __init__(self):
        file_struct = const.ing_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(IngMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            # Master.__init__(self, file_abbr, file_struct)
            super(IngMaster, self).__init__(file_abbr, file_struct)


class TexMaster(Master):
    def __init__(self):
        file_struct = const.tex_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(TexMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(TexMaster, self).__init__(file_abbr, file_struct)


class PltMaster(Master):
    def __init__(self):
        file_struct = const.plt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PltMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PltMaster, self).__init__(file_abbr, file_struct)


class DptMaster(Master):
    def __init__(self):
        file_struct = const.dpt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(DptMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(DptMaster, self).__init__(file_abbr, file_struct)


class MgtMaster(Master):
    def __init__(self):
        file_struct = const.mgt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(MgtMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(MgtMaster, self).__init__(file_abbr, file_struct)


class PtrMaster(Master):
    def __init__(self):
        file_struct = const.ptr_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PtrMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PtrMaster, self).__init__(file_abbr, file_struct)


class RtbMaster(Master):
    def __init__(self):
        file_struct = const.rtb_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(RtbMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(RtbMaster, self).__init__(file_abbr, file_struct)


class RttMaster(Master):
    def __init__(self):
        file_struct = const.rtt_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(RttMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(RttMaster, self).__init__(file_abbr, file_struct)


class ScdMaster(Master):
    def __init__(self):
        file_struct = const.scd_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(ScdMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(ScdMaster, self).__init__(file_abbr, file_struct)


class PasMaster(Master):
    def __init__(self):
        file_struct = const.pas_struct
        file_abbr = self.__class__.__name__.lower()[:3]
        scale_file = file_abbr + '.json'
        if os.path.isfile(scale_file):
            super(PasMaster, self).__init__(file_abbr, common.common.get_json_from_file(scale_file))
        else:
            super(PasMaster, self).__init__(file_abbr, file_struct)


class MasterFactory:
    def __init__(self):
        pass

    def createMaster(self, master_name):
        master_list = {
            "Scd": lambda: ScdMaster(),
            "Plu": lambda: PluMaster(),
            "Mgp": lambda: MgpMaster(),
            "Dat": lambda: DatMaster(),
            "Pla": lambda: PlaMaster(),
            "Dep": lambda: DepMaster(),
            "Kas": lambda: KasMaster(),
            "Trg": lambda: TrgMaster(),
            "Trb": lambda: TrbMaster(),
            "Trt": lambda: TrtMaster(),
            "Tbt": lambda: TbtMaster(),
            "Prf": lambda: PrfMaster(),
            "Pff": lambda: PffMaster(),
            "Flb": lambda: FlbMaster(),
            "Mub": lambda: MubMaster(),
            "Spm": lambda: SpmMaster(),
            "Ing": lambda: IngMaster(),
            "Tex": lambda: TexMaster(),
            "Plt": lambda: PltMaster(),
            "Dpt": lambda: DptMaster(),
            "Mgt": lambda: MgtMaster(),
            "Ptr": lambda: PtrMaster(),
            "Rtb": lambda: RtbMaster(),
            "Rtt": lambda: RttMaster(),
            "Pas": lambda: PasMaster(),
        }
        if master_name in master_list:
            return master_list[master_name]()
        return None


if __name__ == '__main__':
    pass
    # print type(MgpMaster().get_free_value_of_key())
