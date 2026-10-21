"""Test "reale": interroga davvero il sistema operativo (non apre nessuna app)."""

from pathlib import Path

from anri.tools.app import APP, SU_WINDOWS, trova_app_installate


def test_trova_app_installate_su_questo_pc():
    installate = trova_app_installate()
    assert len(installate) > 0
    assert all(nome == nome.lower() for nome in installate)
    assert not any("uninstall" in nome for nome in installate)


def test_scorciatoie_esistono_su_questo_pc():
    if SU_WINDOWS:
        return  # su Windows le scorciatoie sono comandi (calc.exe), non percorsi
    for destinazione in APP.values():
        if not destinazione.startswith("http"):
            assert Path(destinazione).exists(), destinazione
