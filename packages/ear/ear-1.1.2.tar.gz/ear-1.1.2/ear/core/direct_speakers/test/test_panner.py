import numpy as np
import numpy.testing as npt
import pytest
from ..panner import DirectSpeakersPanner
from ...metadata_input import DirectSpeakersTypeMetadata, ExtraData
from ....fileio.adm.elements import AudioBlockFormatDirectSpeakers, BoundCoordinate, Frequency, ScreenEdgeLock
from ....fileio.adm.elements import DirectSpeakerCartesianPosition, DirectSpeakerPolarPosition
from ... import bs2051
from ...geom import cart


def tm_with_labels(labels, lfe_freq=False):
    """Get a DirectSpeakersTypeMetadata with the given speakerLabels and
    default position."""
    return DirectSpeakersTypeMetadata(
        block_format=AudioBlockFormatDirectSpeakers(
            position=DirectSpeakerPolarPosition(
                bounded_azimuth=BoundCoordinate(0.0),
                bounded_elevation=BoundCoordinate(0.0),
                bounded_distance=BoundCoordinate(1.0),
            ),
            speakerLabel=labels),
        extra_data=ExtraData(
            channel_frequency=Frequency(
                lowPass=120.0 if lfe_freq else None))
    )


def direct_pv(layout, channel):
    pv = np.zeros(len(layout.channels))
    pv[layout.channel_names.index(channel)] = 1.0
    return pv


def psp_pv(panner, position):
    pv = np.zeros(len(panner.layout.channels))
    pv[~panner.layout.is_lfe] = panner.psp.handle(position)
    return pv


def test_speaker_label():
    layout = bs2051.get_layout("4+5+0")
    p = DirectSpeakersPanner(layout)

    for prefix in ["", "urn:itu:bs:2051:0:speaker:", "urn:itu:bs:2051:1:speaker:"]:
        # normal case
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "M+000"])), direct_pv(layout, "M+000"))
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "M+030"])), direct_pv(layout, "M+030"))

        # missing channels are ignored
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "M+030", prefix + "B+000"])), direct_pv(layout, "M+030"))
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "B+000", prefix + "M+030"])), direct_pv(layout, "M+030"))

        # matching more than one channel should pick the first
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "M+000", prefix + "M+030"])), direct_pv(layout, "M+000"))
        npt.assert_allclose(p.handle(tm_with_labels([prefix + "M+030", prefix + "M+000"])), direct_pv(layout, "M+030"))


def test_speaker_label_additional_substitutions():
    layout = bs2051.get_layout("4+5+0")
    p = DirectSpeakersPanner(layout, additional_substitutions={"foo": "M+030"})

    npt.assert_allclose(p.handle(tm_with_labels(["foo"])), direct_pv(layout, "M+030"))


def test_lfe():
    """Check the various LFE labelling options."""
    layout = bs2051.get_layout("9+10+3")
    p = DirectSpeakersPanner(layout)

    # using frequency element and labels
    for lfe_option in ["LFE", "LFE1", "LFEL"]:
        npt.assert_allclose(p.handle(tm_with_labels([lfe_option], lfe_freq=True)), direct_pv(layout, "LFE1"))
    for lfe_option in ["LFE2", "LFER"]:
        npt.assert_allclose(p.handle(tm_with_labels([lfe_option], lfe_freq=True)), direct_pv(layout, "LFE2"))

    # using just frequency element
    npt.assert_allclose(p.handle(tm_with_labels([], lfe_freq=True)), direct_pv(layout, "LFE1"))

    # check warnings with mismatch between label and frequency elements
    with pytest.warns(None) as record:
        # using just labels
        for lfe_option in ["LFE", "LFE1", "LFEL"]:
            npt.assert_allclose(p.handle(tm_with_labels([lfe_option])), direct_pv(layout, "LFE1"))
        for lfe_option in ["LFE2", "LFER"]:
            npt.assert_allclose(p.handle(tm_with_labels([lfe_option])), direct_pv(layout, "LFE2"))

        # frequency element with incorrect label
        npt.assert_allclose(p.handle(tm_with_labels(["M+000"], lfe_freq=True)), direct_pv(layout, "LFE1"))

    assert len(record) == 6 and all(str(w.message) == "LFE indication from frequency element does not match speakerLabel."
                                    for w in record)


def test_one_lfe_out():
    """When there is only one LFE output, both LFE1 and LFE2 should be sent to it."""
    layout = bs2051.get_layout("4+5+0")
    p = DirectSpeakersPanner(layout)

    npt.assert_allclose(p.handle(tm_with_labels(["LFE1"], lfe_freq=True)), direct_pv(layout, "LFE1"))
    npt.assert_allclose(p.handle(tm_with_labels(["LFE2"], lfe_freq=True)), direct_pv(layout, "LFE1"))


def test_no_lfe_out():
    """When there is no LFE output, both LFE1 and LFE2 should be discarded."""
    layout = bs2051.get_layout("0+2+0")
    p = DirectSpeakersPanner(layout)

    npt.assert_allclose(p.handle(tm_with_labels(["LFE1"], lfe_freq=True)), np.zeros(len(layout.channels)))
    npt.assert_allclose(p.handle(tm_with_labels(["LFE2"], lfe_freq=True)), np.zeros(len(layout.channels)))


def test_dist_bounds_polar():
    layout = bs2051.get_layout("9+10+3")
    p = DirectSpeakersPanner(layout)
    idx = layout.channel_names.index

    # test horizontal bounds

    expected_fr = np.zeros(len(layout.channels))
    expected_fr[[idx("M+000"), idx("M+030")]] = [np.sqrt(0.5), np.sqrt(0.5)]

    # no bounds, and position not on speaker -> use psp
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(15.0),
            bounded_elevation=BoundCoordinate(0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), expected_fr)

    # lower bound expanded to speaker -> direct on that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(15.0, min=0.0),
            bounded_elevation=BoundCoordinate(0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+000"))

    # upper bound expanded to speaker -> direct on that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(15.0, max=30.0),
            bounded_elevation=BoundCoordinate(0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+030"))

    # upper and lower bounds expanded to speakers -> use psp again
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(15.0, min=0.0, max=30.0),
            bounded_elevation=BoundCoordinate(0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), expected_fr)

    # closer to one than the other -> direct to that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(14.0, min=0.0, max=30.0),
            bounded_elevation=BoundCoordinate(0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+000"))

    # test vertical bounds

    expected_mu = np.zeros(len(layout.channels))
    expected_mu[[idx("M+000"), idx("U+000")]] = [np.sqrt(0.5), np.sqrt(0.5)]

    # no bounds, and position not on speaker -> use psp
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0),
            bounded_elevation=BoundCoordinate(15.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), expected_mu)

    # lower bound expanded to speaker -> direct on that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0),
            bounded_elevation=BoundCoordinate(15.0, min=0.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+000"))

    # upper bound expanded to speaker -> direct on that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0),
            bounded_elevation=BoundCoordinate(15.0, max=30.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "U+000"))

    # upper and lower bounds expanded to speakers -> use psp again
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0),
            bounded_elevation=BoundCoordinate(15.0, min=0.0, max=30.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), expected_mu)

    # closer to one than the other -> direct to that speaker
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0),
            bounded_elevation=BoundCoordinate(14.0, min=0.0, max=30.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+000"))

    # check that pole speakers are used even if 0 is excluded by azimuth range
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(15.0, 10.0, 20.0),
            bounded_elevation=BoundCoordinate(90.0)))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "T+000"))


def test_dist_bounds_cart():
    layout = bs2051.get_layout("9+10+3")
    p = DirectSpeakersPanner(layout)

    # on speaker -> direct
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(1.0),
            bounded_Y=BoundCoordinate(0.0),
            bounded_Z=BoundCoordinate(0.0),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M-090"))

    # lower bound on speaker -> direct
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(1.0),
            bounded_Y=BoundCoordinate(0.1, min=0.0),
            bounded_Z=BoundCoordinate(0.0),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M-090"))

    # upper bound on speaker -> direct
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(1.0),
            bounded_Y=BoundCoordinate(-0.1, max=0.0),
            bounded_Z=BoundCoordinate(0.0),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M-090"))

    # pick closest within bound
    pos_30 = cart(30, 0, 1)
    pos_5 = cart(5, 0, 1)
    pos_25 = cart(25, 0, 1)

    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(pos_5[0], min=pos_30[0], max=-pos_30[0]),
            bounded_Y=BoundCoordinate(pos_5[1], min=pos_30[1], max=1.0),
            bounded_Z=BoundCoordinate(0.0),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+000"))

    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(pos_25[0], min=pos_30[0], max=-pos_30[0]),
            bounded_Y=BoundCoordinate(pos_25[1], min=pos_30[1], max=1.0),
            bounded_Z=BoundCoordinate(0.0),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)), direct_pv(layout, "M+030"))


def test_screen_edge_lock_polar():
    layout = bs2051.get_layout("4+5+0")
    p = DirectSpeakersPanner(layout)

    # no bound set -> use psp
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(-30.0),
            bounded_elevation=BoundCoordinate(0.0),
            screenEdgeLock=ScreenEdgeLock(horizontal="right"),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)),
                        psp_pv(p, cart(-29, 0, 1)))

    # bound set -> find closest to screen edge
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerPolarPosition(
            bounded_azimuth=BoundCoordinate(0.0, min=-45.0, max=10.0),
            bounded_elevation=BoundCoordinate(0.0),
            screenEdgeLock=ScreenEdgeLock(horizontal="right"),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)),
                        direct_pv(layout, "M-030"))


def test_screen_edge_lock_cart():
    layout = bs2051.get_layout("4+5+0")
    p = DirectSpeakersPanner(layout)

    # no bound set -> use psp
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(0.0),
            bounded_Y=BoundCoordinate(1.0),
            bounded_Z=BoundCoordinate(0.0),
            screenEdgeLock=ScreenEdgeLock(horizontal="right"),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)),
                        psp_pv(p, cart(-29, 0, 1)))

    # bound set -> find closest to screen edge
    bf = AudioBlockFormatDirectSpeakers(
        position=DirectSpeakerCartesianPosition(
            bounded_X=BoundCoordinate(0.0, min=-0.1, max=1.0),
            bounded_Y=BoundCoordinate(1.0, min=0.5),
            bounded_Z=BoundCoordinate(0.0),
            screenEdgeLock=ScreenEdgeLock(horizontal="right"),
        ))
    npt.assert_allclose(p.handle(DirectSpeakersTypeMetadata(bf)),
                        direct_pv(layout, "M-030"))
