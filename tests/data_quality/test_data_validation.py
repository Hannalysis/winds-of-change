from data_quality.data_validation import check_nulls, check_duplicates, check_location_format, check_date_format, check_uk_lat, check_uk_long, check_wind_speed
import pandas as pd

# --- check_nulls tests ---

def test_check_nulls_no_nulls():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })
    result = check_nulls(df)
    expected = pd.Series({"a": 0, "b": 0})
    pd.testing.assert_series_equal(result, expected)

def test_check_nulls_some_nulls():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": [None, None, 6]
    })
    result = check_nulls(df)
    expected = pd.Series({"a": 1, "b": 2})
    pd.testing.assert_series_equal(result, expected)

def test_check_nulls_all_nulls():
    df = pd.DataFrame({
        "a": [None, None],
        "b": [None, None]
    })
    result = check_nulls(df)
    expected = pd.Series({"a": 2, "b": 2})
    pd.testing.assert_series_equal(result, expected)

# --- check_duplicates tests ---

def test_check_duplicates_no_duplicates():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [4, 5, 6]
    })
    result = check_duplicates(df)
    assert result == 0

def test_check_duplicates_with_duplicates():
    df = pd.DataFrame({
        "a": [1, 2, 2, 3],
        "b": [4, 5, 5, 6]
    })
    result = check_duplicates(df)
    assert result == 1

def test_check_duplicates_all_duplicates():
    df = pd.DataFrame({
        "a": [1, 1, 1],
        "b": [4, 4, 4]
    })
    result = check_duplicates(df)
    assert result == 2

