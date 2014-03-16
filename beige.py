#!/usr/bin/env python

base_alphas = (("KEY_a_A","1x1"), ("KEY_b_B","1x1"), ("KEY_c_C","1x1"), ("KEY_d_D","1x1"),
("KEY_e_E","1x1"), ("KEY_f_F","1x1"), ("KEY_g_G","1x1"), ("KEY_h_H","1x1"),
("KEY_i_I","1x1"), ("KEY_j_J","1x1"), ("KEY_k_K","1x1"), ("KEY_l_L","1x1"),
("KEY_m_M","1x1"), ("KEY_n_N","1x1"), ("KEY_o_O","1x1"), ("KEY_p_P","1x1"),
("KEY_q_Q","1x1"), ("KEY_r_R","1x1"), ("KEY_s_S","1x1"), ("KEY_t_T","1x1"),
("KEY_u_U","1x1"), ("KEY_v_V","1x1"), ("KEY_w_W","1x1"), ("KEY_x_X","1x1"),
("KEY_y_Y","1x1"), ("KEY_z_Z","1x1"))

base_numerics = (("KEY_1_Exclamation","1x1"), ("KEY_2_At","1x1"), ("KEY_3_Pound","1x1"),
("KEY_4_Dollar","1x1"), ("KEY_5_Percent","1x1"), ("KEY_6_Caret","1x1"),
("KEY_7_Ampersand","1x1"), ("KEY_8_Asterisk","1x1"), ("KEY_9_LeftParenthesis","1x1"),
("KEY_0_RightParenthesis","1x1"))

base_syms = ( ("KEY_Comma_LessThan", "1x1"), ("KEY_Period_GreaterThan", "1x1"), ("KEY_Semicolon_Colon", "1x1"),
("KEY_LeftBracket_LeftBrace", "1x1"), ("KEY_RightBracket_RightBrace", "1x1"),
("KEY_SingleQuote_DoubleQuote", "1x1"), ("KEY_GraveAccent_Tilde", "1x1"), ("KEY_Slash_Question", "1x1"), ("KEY_Backslash_Pipe", "1.5x1"),
("KEY_Dash_Underscore", "1x1"), ("KEY_Equal_Plus", "1x1"))

base_fn = (("KEY_F1","1x1"), ("KEY_F2","1x1"), ("KEY_F3","1x1"), ("KEY_F4","1x1"),
("KEY_F5","1x1"), ("KEY_F6","1x1"), ("KEY_F7","1x1"), ("KEY_F8","1x1"),
("KEY_F9","1x1"), ("KEY_F10","1x1"), ("KEY_F11","1x1"), ("KEY_F12","1x1"))

base_nav = (("KEY_Escape", "1x1"),
("KEY_PrintScreen","1x1"),
("KEY_ScrollLock","1x1"),
("KEY_Pause","1x1"),
("KEY_DeleteBackspace","2x1"),
("KEY_Tab","1.5x1"),
('KEY_ReturnEnter', '2.25x1'),
("KEY_Insert","1x1"), ("KEY_DeleteForward","1x1"),
("KEY_Home","1x1"), ("KEY_End","1x1"),
("KEY_PageUp","1x1"), ("KEY_PageDown","1x1"),
("KEY_RightArrow","1x1"), ("KEY_LeftArrow","1x1"), ("KEY_DownArrow","1x1"), ("KEY_UpArrow","1x1"))

base_mod = (('KEY_CapsLock', '1.75x1'),
		('KEY_Shift', '2.25x1'),
		('KEY_Shift', '2.75x1'),
		('KEY_Control', '1.25x1'),
		('KEY_Alt', '1.25x1'),
#		('KEY_Gui', '1.25x1'),
		('KEY_Control', '1.25x1'),
		('KEY_Alt', '1.25x1'),
#		('KEY_Gui', '1.25x1'),
		('KEY_Menu', '1.25x1'))

numpad = (
('KEYPAD_NumLock_Clear','1x1'),
('KEYPAD_Slash','1x1'),
('KEYPAD_Asterisk','1x1'),
('KEYPAD_Minus','1x1'),
('KEYPAD_Plus','1x2'),
('KEYPAD_Plus','1x1'),
('KEYPAD_Equal','1x1'),
('KEYPAD_ENTER','1x2'),
('KEYPAD_1_End','1x1'),
('KEYPAD_2_DownArrow','1x1'),
('KEYPAD_3_PageDown','1x1'),
('KEYPAD_4_LeftArrow','1x1'),
('KEYPAD_5','1x1'),
('KEYPAD_6_RightArrow','1x1'),
('KEYPAD_7_Home','1x1'),
('KEYPAD_8_UpArrow','1x1'),
('KEYPAD_9_PageUp','1x1'),
('KEYPAD_0_Insert','1x1'),
('KEYPAD_0_Insert','2x1'),
('KEYPAD_00','1x1'),
('KEYPAD_Period_Delete','1x1'))

pro_10mod = (("KEY_Control", "1x1"), ("KEY_Control", "1x1"),
		('KEY_Menu','1x1'),
		('KEY_Tab','1x1'),
		('KEY_DeleteBackspace','1x1'),
("KEY_Alt", "1x1"), ("KEY_Alt", "1x1"))


pro_15mod = (("KEY_Control", "1.5x1"), ("KEY_Control", "1.5x1"),
("KEY_Alt", "1.5x1"), ("KEY_Alt", "1.5x1"),
("KEY_DeleteBackspace", "1.5x1"), ('KEY_CapsLock', '1.5x1'), ('SPECIAL_Fn', '1.5x1'))

fullset = base_alphas + base_numerics + base_syms + base_fn + base_nav + base_mod + pro_10mod + pro_15mod
