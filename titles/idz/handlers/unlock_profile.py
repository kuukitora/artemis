import struct

from .base import IDZHandlerBase
from core.config import CoreConfig
from ..config import IDZConfig
from ..const import IDZConstants

class IDZHandlerUnlockProfile(IDZHandlerBase):
    cmd_codes = [0x006f, 0x006f, 0x006b, 0x006b]
    rsp_codes = [0x0070, 0x0070, 0x006c, 0x006c]
    name = "unlock_profile"

    def __init__(self, core_cfg: CoreConfig, game_cfg: IDZConfig, version: int) -> None:
        super().__init__(core_cfg, game_cfg, version)
        self.size = 0x0010
    
    def handle(self, data: bytes) -> bytearray:
        ret =  super().handle(data)
        struct.pack_into("<H", ret, 0x4, 1)
        return ret
