import pytest
import script
import time
import mock


future_date='2025-01-01'
too_old_date='2001-12-05'
too_short_date='2018-01-1'
proper_date='2018-01-01'



@pytest.mark.parametrize('start, end, expected',[
    ('2018-01-01','2018-04-01', None),
    ('2018-04-01','2018-01-01', True),
])
def test_end_earlier_then_start(start, end, expected):
    assert script.check_end_earlier_then_start(start, end) == expected




# def test_input_future(monkeypatch):
#     monkeypatch.setattr('builtins.input', lambda x: future_date)
#     i=input('a')
#     assert i==future_date


# def test_check_format_date_date_in_future(monkeypatch):
#     i = script.check_format_date(script.first_archival_date)
#     date=monkeypatch.setattr('builtins.input', lambda x: '2025-01-01')
#     assert i==script.ERROR_FUTURE_DATE




# @pytest.mark.parametrize('date, excepted',[
#     (future_date, script.ERROR_FUTURE_DATE),
#     (too_old_date, script.ERROR_TOO_OLD_DATE),
#     (too_short_date, script.ERROR_TO_SHORT_FORMAT),
#     (proper_date, (proper_date, time.strptime(proper_date, '%Y-%m-%d')))
# ])
# def test_check_format_date_ech_case(date, excepted):
#     assert script.check_format_date(script.first_archival_date)==excepted