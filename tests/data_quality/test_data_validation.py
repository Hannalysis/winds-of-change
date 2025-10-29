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

# --- check_location_format tests ---

def test_check_location_format_all_title_case():
    df = pd.DataFrame({
        "location_name": ["London", "Manchester", "Birmingham"]
    })
    result = check_location_format(df, "location_name")
    assert result is None

def test_check_location_format_mixed_case():
    df = pd.DataFrame({
        "location_name": ["London", "manchester", "Birmingham"]
    })
    result = check_location_format(df, "location_name")
    expected_series = pd.Series({1: "manchester"})
    expected_list = ["manchester"]

    if isinstance(result, list):
        assert result == expected_list
    else:
        pd.testing.assert_series_equal(result, expected_series)


def test_check_location_format_all_lower_case():
    df = pd.DataFrame({
        "location_name": ["london", "manchester", "birmingham"]
    })
    result = check_location_format(df, "location_name")
    expected_series = pd.Series({
        0: "london",
        1: "manchester",
        2: "birmingham"
    })
    expected_list = ["london", "manchester", "birmingham"]

    if isinstance(result, list):
        assert result == expected_list
    else:
        pd.testing.assert_series_equal(result, expected_series)

def test_check_location_format_with_known_exceptions():
    df = pd.DataFrame({
        "location_name": ["London", "Knight's Hill", "birmingham"]
    })
    result = check_location_format(df, "location_name")
    expected_series = pd.Series({2: "birmingham"})
    expected_list = ["birmingham"]

    if isinstance(result, list):
        assert result == expected_list
    else:
        pd.testing.assert_series_equal(result, expected_series)

# --- check_date_format tests ---

def test_check_date_format_all_valid():
    df = pd.DataFrame({
        "date": ["2023-01-01", "2023-12-31", "2024-06-15"]
    })
    result = check_date_format(df, "date")
    assert result is None

def test_check_date_format_some_invalid():
    df = pd.DataFrame({
        "date": ["2023-01-01", "2023-31-12", "2024-06-15", "15-06-2024"]
    })
    result = check_date_format(df, "date")
    expected_df = pd.DataFrame({
        "date": ["2023-31-12", "15-06-2024"]
    }, index=[1, 3])
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

def test_check_date_format_all_invalid():
    df = pd.DataFrame({
        "date": ["01-01-2023", "31-12-2023", "15-06-2024"]
    })
    result = check_date_format(df, "date")
    expected_df = pd.DataFrame({
        "date": ["01-01-2023", "31-12-2023", "15-06-2024"]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

# --- check_uk_lat tests ---
def test_check_uk_lat_all_valid():
    df = pd.DataFrame({
        "latitude": [51.5074, 53.4808, 55.9533]
    })
    result = check_uk_lat(df, "latitude")
    assert result is None

def test_check_uk_lat_some_invalid():
    df = pd.DataFrame({
        "latitude": [51.5074, 53.4808, 55.9533, 999.9999]
    })
    result = check_uk_lat(df, "latitude")
    expected_df = pd.DataFrame({
        "latitude": [999.9999]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

def test_check_uk_lat_all_invalid():
    df = pd.DataFrame({
        "latitude": [999.9999, 888.8888, 777.7777]
    })
    result = check_uk_lat(df, "latitude")
    expected_df = pd.DataFrame({
        "latitude": [999.9999, 888.8888, 777.7777]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

# --- check_uk_long tests ---
def test_check_uk_long_all_valid():
    df = pd.DataFrame({
        "longitude": [-0.1278, -2.2426, -3.1883]
    })
    result = check_uk_long(df, "longitude")
    assert result is None

def test_check_uk_long_some_invalid():
    df = pd.DataFrame({
        "longitude": [-0.1278, -2.2426, -3.1883, 999.9999]
    })
    result = check_uk_long(df, "longitude")
    expected_df = pd.DataFrame({
        "longitude": [999.9999]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

def test_check_uk_long_all_invalid():
    df = pd.DataFrame({
        "longitude": [999.9999, 888.8888, 777.7777]
    })
    result = check_uk_long(df, "longitude")
    expected_df = pd.DataFrame({
        "longitude": [999.9999, 888.8888, 777.7777]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

# --- check_wind_speed tests ---

def test_check_wind_speed_all_valid():
    df = pd.DataFrame({
        "wind_speed": [0, 15, 30, 50, 70]
    })
    result = check_wind_speed(df, "wind_speed")
    assert result is None

def test_check_wind_speed_some_invalid():
    df = pd.DataFrame({
        "wind_speed": [0, 15, 150, -10, 70]
    })
    result = check_wind_speed(df, "wind_speed")
    expected_df = pd.DataFrame({
        "wind_speed": [150, -10]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

def test_check_wind_speed_all_invalid():
    df = pd.DataFrame({
        "wind_speed": [150, -10, 200]
    })
    result = check_wind_speed(df, "wind_speed")
    expected_df = pd.DataFrame({
        "wind_speed": [150, -10, 200]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))
