def cleaning_contents_buffer_txt_files():
    """Подпрограмма очищает все текстовые файлы от содержимого прошлого запуска при запуске"""

    open(path_buffer_massive_clamped_clamps, 'w').close()
    open(path_buffer_row_col_acceptable_clamps, 'w').close()
    open(path_buffer_highlighted_wire, 'w').close()
    open(path_buffer_id_moving_line, 'w').close()
    open(path_buffer_row_col_start_clamp, 'w').close()


path_buffer_massive_clamped_clamps = 'cache/massive_clamped_clamps.txt'
path_buffer_row_col_acceptable_clamps = 'cache/buffer_row_col_acceptable_clamps.txt'
path_buffer_highlighted_wire = 'cache/buffer_highlighted_wire.txt'
path_buffer_id_moving_line = 'cache/buffer_id_moving_line.txt'
path_buffer_row_col_start_clamp = 'cache/buffer_row_col_start_clamp.txt'
cleaning_contents_buffer_txt_files()
