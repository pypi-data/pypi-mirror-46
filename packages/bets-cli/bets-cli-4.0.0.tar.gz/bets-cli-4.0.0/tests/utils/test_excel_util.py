from bets.utils import file_sys, excel_util, log

log.init()


def test_read_write():
    output_file = file_sys.get_temp_location("sheets_output")
    output_data = {
        "Sheet1": [{"s1col_0": "s1row_0 col_0", "s1col_1": 1},
                   {"s1col_0": "s1row_1 col_0", "s1col_1": 2.5}],
        "Sheet2": [{"s2col_0": "s2row_0 col_0", "s2col_1": "s2row_0 col_1"},
                   {"s2col_0": "s2row_1 col_0", "s2col_1": "s2row_1 col_1"}]
    }

    input_file = excel_util.write_sheets(output_data, output_file)
    input_data = excel_util.read_sheets(input_file)

    assert input_data == output_data
