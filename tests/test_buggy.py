import os

from msl.examples.loadlib import DotNet64
from msl.loadlib import Client64

from conftest import skipif_not_windows


def test_dotnet64():
    for _ in range(10):
        dn = DotNet64()
        assert 3 == dn.add_integers(1, 2)
        dn.shutdown_server32()


@skipif_not_windows
def test_activex():

    class ActiveX(Client64):

        def __init__(self):
            super(ActiveX, self).__init__(
                module32='activex_media_player.py',
                append_sys_path=os.path.join(os.path.dirname(__file__), 'server32_comtypes'),
                timeout=10,
            )

        def this(self):
            return self.request32('this')

        def static(self):
            return self.request32('static')

        def create(self):
            return self.request32('create')

        def parent(self):
            return self.request32('parent')

        def panel(self):
            return self.request32('panel')

        def load_library(self):
            return self.request32('load_library')

        def error1(self):
            return self.request32('error1')

        def error2(self):
            return self.request32('error2')

    for _ in range(10):
        ax = ActiveX()

        # don't care whether the value is True or False only that it is a boolean
        assert isinstance(ax.this(), bool)
        assert isinstance(ax.static(), bool)
        assert isinstance(ax.create(), bool)
        assert isinstance(ax.parent(), bool)
        assert isinstance(ax.panel(), bool)
        assert isinstance(ax.load_library(), bool)
        assert ax.error1().endswith("Cannot find 'ABC.DEF.GHI' for libtype='activex'")
        assert ax.error2().endswith("Cannot find 'ABC.DEF.GHI' for libtype='activex'")

        # no numpy warnings from comtypes
        out, err = ax.shutdown_server32()
        assert not out.read()
        assert not err.read()
        out.close()
        err.close()
