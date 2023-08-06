import py.path
import numpy as np
import numpy.testing as npt
import pytest
from ..geom import cart
from ..point_source import configure

files_dir = py.path.local(__file__).dirpath() / "data" / "psp_pvs"


@pytest.mark.no_cover
def test_no_change_in_pvs(layout):
    """check that the results of the point source panner haven't changed"""
    config = configure(layout)

    azimuths, elevations = np.meshgrid(np.linspace(-180, 180, 31),
                                       np.linspace(-90, 90, 15))
    positions = cart(azimuths, elevations, 1)
    pv = np.apply_along_axis(config.handle, 2, positions)

    data_path = files_dir / (layout.name + ".npz")

    if data_path.check():
        loaded_pv = np.load(str(data_path))["pv"]
        npt.assert_allclose(pv, loaded_pv, atol=1e-6)
    else:
        data_path.dirpath().ensure_dir()
        np.savez_compressed(str(data_path), pv=pv)
        pytest.skip("generated pv file for layout {layout.name}".format(layout=layout))
