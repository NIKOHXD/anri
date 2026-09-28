"""Test "reale": interroga davvero Windows (non apre nessuna app)."""

from anri.tools.app import trova_app_installate


def test_trova_app_installate_su_questo_pc():
    installate = trova_app_installate()
    assert len(installate) > 0
    assert all(nome == nome.lower() for nome in installate)
    assert not any("uninstall" in nome for nome in installate)
