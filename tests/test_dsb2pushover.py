# -*- coding: utf-8 -*-
import pandas as pd

from src.app.dsb2pushover import render_payload


def test_render_payload():
    data = [
        {
            "class": "6a",
            "type": "entfall",
            "lesson": "3",
            "subject": "Math",
            "new_subject": "Math",
            "room": "101",
            "new_teacher": "Mr. Text",
            "text": "Some text",
        }
    ]
    expected_result = "Klasse 6a, entfall in Stunde 3, Fach Math, in Raum 101, Lehrer Mr. Text, Some text"

    result = render_payload(pd.DataFrame.from_dict(data))

    assert result == expected_result
