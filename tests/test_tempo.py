from datetime import datetime

from anri.tools.tempo import formatta_data


def test_formatta_data():
    momento = datetime(2026, 9, 28, 18, 5)
    assert formatta_data(momento) == "Sono le 18:05 di lunedì 28 settembre 2026."


def test_formatta_data_domenica_e_dicembre():
    # Casi limite: ultimo elemento di entrambe le liste
    momento = datetime(2026, 12, 27, 9, 0)
    assert formatta_data(momento) == "Sono le 09:00 di domenica 27 dicembre 2026."
