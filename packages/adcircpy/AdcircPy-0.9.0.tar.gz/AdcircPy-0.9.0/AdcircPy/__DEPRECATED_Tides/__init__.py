# import os
# from AdcircPy.utils import __init_TPXO_cache, get_cache_dir


# class TPXO(object):
#     """
#     Runs at top level module import so that the TPXO cache gets initialized on
#     disk.
#     """
#     __init_TPXO_cache(get_cache_dir())

#     @staticmethod
#     def rebuild_cache():
#         os.remove(get_cache_dir()+"/h_tpxo9.v1.nc")
#         __init_TPXO_cache(get_cache_dir())
