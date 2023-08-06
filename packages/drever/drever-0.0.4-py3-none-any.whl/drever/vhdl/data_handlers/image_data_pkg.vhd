library ieee;
use ieee.math_real.all;

use std.textio.all;

library vunit_lib;
use vunit_lib.logger_pkg.all;

package image_data_pkg is

	type t_params is record
		width    : natural;
		height   : natural;
		bitdepth : natural;
		channels : natural;
	end record;

	constant DEFAULT_PARAMS : t_params := (
		width    => 0,
		height   => 0,
		bitdepth => 8,
		channels => 3
	);

	constant MAX_BITDEPTH : natural := 16;
	constant MAX_CHANNELS : natural :=  3;

	subtype t_pixel_range is natural range 0 to 2**MAX_BITDEPTH-1;

	type t_image is protected
		procedure set_params(width, height, bitdepth, channels : natural);
		procedure set_params(image_params : t_params);
		impure function get_params return t_params;
		procedure load(filename : string; use_bitdepth : natural := 0);
		procedure report_info(prepend : string := "");
		impure function get_entry(x, y, channel : natural := 0) return t_pixel_range;
	end protected;

end package image_data_pkg;

package body image_data_pkg is

	type t_image is protected body

		variable params : t_params := DEFAULT_PARAMS;

		type t_p_filename is access string;
		variable p_filename : t_p_filename;

		type t_pixel is array (0 to MAX_CHANNELS-1) of t_pixel_range;
		type t_image_data is array (natural range <>, natural range <>) of t_pixel;

		type t_p_image_data is access t_image_data;
		variable p_image_data : t_p_image_data;

		procedure set_filename(filename : string) is
		begin
			deallocate(p_filename);
			p_filename     := new string(filename'range);
			p_filename.all := filename;
		end procedure;

		procedure set_params(width, height, bitdepth, channels : natural) is
		begin

			if (params.width /= width or params.height /= height) then
				deallocate(p_image_data);
				p_image_data := new t_image_data(
					0 to width-1,
					0 to height-1
				);
			end if;

			params.width    := width;
			params.height   := height;
			params.bitdepth := bitdepth;
			params.channels := channels;

		end procedure set_params;

		procedure set_params(image_params : t_params) is
		begin
			set_params(
				image_params.width,
				image_params.height,
				image_params.bitdepth,
				image_params.channels
			);
		end procedure set_params;

		impure function get_params return t_params is
		begin
			return params;
		end function get_params;

		procedure load(filename : string; use_bitdepth : natural := 0) is

			file     ppm_file       : text open read_mode is filename;
			variable ppm_line       : line;
			variable readout_val    : integer;
			variable read_ok        : boolean;

			variable magic_number   : string(1 to 2) := "PX";
			variable file_params    : t_params       := DEFAULT_PARAMS;
			variable max_value      : natural        := 0;

			variable x, y, channel  : natural        := 0;
			variable chan_3_is_zero : boolean        := true;

		begin

			-- Read Magic Number
			readline(ppm_file, ppm_line);
			read(ppm_line, magic_number, read_ok);
			assert read_ok and (magic_number = "P2" or magic_number = "P3")
				report "Magic Number (" & magic_number & ") not known or not supported!"
				severity failure;

			-- Read Width and Height
			readline(ppm_file, ppm_line);
			read(ppm_line, file_params.width, read_ok);
			assert read_ok and file_params.width > 0
				report "Width (" & integer'image(file_params.width) & ") not valid!"
				severity failure;

			read(ppm_line, file_params.height, read_ok);
			assert read_ok and file_params.height > 0
				report "Height (" & integer'image(file_params.height) & ") not valid!"
				severity failure;

			-- Read Maximum Value
			readline(ppm_file, ppm_line);
			read(ppm_line, max_value, read_ok);
			assert read_ok and max_value > 0 and max_value < 2**16
				report "Maximum Value (" & integer'image(max_value) & ") not valid!"
				severity failure;

			if (use_bitdepth = 0) then
				file_params.bitdepth := integer(floor(log2(real(max_value)))) + 1;
				assert file_params.bitdepth >= 1 and file_params.bitdepth <= 16
					report "Extracted bitdepth not in range [1, 16]."
					severity failure;
			else
				file_params.bitdepth := use_bitdepth;
			end if;

			-- Create new Testvector with proper size
			if (magic_number = "P2") then
				file_params.channels := 1;
			elsif (magic_number = "P3") then
				file_params.channels := 3;
			else
				report "Only P2 and P3 PPM files are supported!" severity failure;
			end if;

			set_params(file_params);

			while not endfile(ppm_file) loop

				readline(ppm_file, ppm_line);
				read(ppm_line, readout_val, read_ok);

				while read_ok loop
					p_image_data(x, y)(channel) := readout_val;

					if (channel = 2 and readout_val /= 0) then
						chan_3_is_zero := false;
					end if;

					if channel = file_params.channels-1 then
						channel := 0;
						if x = file_params.width-1 then
							x := 0;
							if y = file_params.height-1 then
								y := 0;
							else
								y := y + 1;
							end if;
						else
							x := x + 1;
						end if;
					else
						channel := channel + 1;
					end if;

					read(ppm_line, readout_val, read_ok);

				end loop;

			end loop;

			read(ppm_line, readout_val, read_ok);

			assert read_ok = false
				report "There's still data left in the PPM file!"
				severity failure;

			if (chan_3_is_zero) then
				file_params.channels := 2;
				set_params(file_params);
			end if;

			set_filename(filename);
			report_info("Load PPM file (" & magic_number & ") done" & LF);

		end procedure;

		procedure report_info(prepend : string := "") is
		begin

			info(prepend &
				"Image Data Summary" & LF &
				"Width / Height: " & integer'image(params.width) & " / " & integer'image(params.height) & LF &
				"Bitdepth:       " & integer'image(params.bitdepth) & LF &
				"Loaded File:    " & p_filename.all
			);

		end procedure;

		impure function get_entry(x, y, channel : natural := 0) return t_pixel_range is
		begin

			if (x < params.width and y < params.height and channel < params.channels) then
				return p_image_data(x, y)(channel);
			else
				report "Error while reading testvector entry @ " & LF &
					"x / y:   " & integer'image(x) & " / " & integer'image(y) & LF &
					"channel: " & integer'image(channel)
					severity failure;
				return t_pixel_range'low;
			end if;

		end function;

	end protected body t_image;

end package body image_data_pkg;
