from utils.csv_extractor import extract_to_csv
from unittest.mock import patch, MagicMock

def test_extract_to_csv(tmp_path):

    query = "SELECT * FROM users"
    engine = MagicMock()
    csv_path = tmp_path / "output.csv"

    # Mocking pandas.read_sql to return a mock DataFrame
    with patch("utils.csv_extractor.pd.read_sql") as mock_read_sql:
        mock_df = MagicMock()
        mock_read_sql.return_value = mock_df

        # Mocking df.to_csv to prevent actual file write
        with patch.object(mock_df, "to_csv") as mock_to_csv:

            # Act
            extract_to_csv(query, engine, csv_path)

            # Assert
            mock_read_sql.assert_called_once_with(query, engine)
            mock_to_csv.assert_called_once_with(csv_path, index=False)
