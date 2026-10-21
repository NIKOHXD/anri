"""Test della memoria su disco (già funzionante, non è un esercizio)."""

from anri import config, memoria


def test_memoria_vuota_se_il_file_non_esiste(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "MEMORIA_FILE", str(tmp_path / "non_esiste.json"))
    assert memoria.carica() == []


def test_salva_e_ricarica(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "MEMORIA_FILE", str(tmp_path / "memoria.json"))
    memoria.salva(["Si chiama Nicolò", "Ama il caffè"])
    assert memoria.carica() == ["Si chiama Nicolò", "Ama il caffè"]


def test_prompt_senza_fatti_resta_quello_base():
    assert memoria.componi_prompt([]) == config.SYSTEM_PROMPT


def test_prompt_contiene_i_fatti():
    prompt = memoria.componi_prompt(["Studia informatica"])
    assert prompt.startswith(config.SYSTEM_PROMPT)
    assert "- Studia informatica" in prompt
