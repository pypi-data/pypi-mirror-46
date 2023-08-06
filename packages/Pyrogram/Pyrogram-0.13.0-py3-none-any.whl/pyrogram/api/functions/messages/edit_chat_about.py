# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class EditChatAbout(Object):
    """Attributes:
        ID: ``0xdef60797``

    Parameters:
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        about: ``str``

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "about"]

    ID = 0xdef60797
    QUALNAME = "functions.messages.EditChatAbout"

    def __init__(self, *, peer, about: str):
        self.peer = peer  # InputPeer
        self.about = about  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "EditChatAbout":
        # No flags
        
        peer = Object.read(b)
        
        about = String.read(b)
        
        return EditChatAbout(peer=peer, about=about)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(String(self.about))
        
        return b.getvalue()
