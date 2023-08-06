# -*- coding: utf-8 -*-

#
# This file is part of pyBox0.
# Copyright (C) 2014-2018 Kuldeep Singh Dhaka <kuldeep@madresistor.com>
#
# pyBox0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyBox0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBox0.  If not, see <http://www.gnu.org/licenses/>.
#

import cffi
import codecs

ffi = cffi.FFI()

ffi.cdef("""
	/* libusb */
	typedef struct libusb_device_handle libusb_device_handle;
	typedef struct libusb_context libusb_context;
	typedef struct libusb_device libusb_device;

	/* we are less intrested in inside content */
	typedef struct b0_device b0_device;
	typedef struct b0_ain b0_ain;
	typedef struct b0_aout b0_aout;
	typedef struct b0_spi b0_spi;
	typedef struct b0_i2c b0_i2c;
	typedef struct b0_pwm b0_pwm;
	typedef struct b0_dio b0_dio;
	typedef struct b0_module b0_module;
	typedef struct b0_version b0_version;
	typedef struct b0_property b0_property;

	typedef struct b0_hbridge b0_hbridge;
	typedef struct b0_adxl345 b0_adxl345;
	typedef struct b0_mcp342x b0_mcp342x;
	typedef struct b0_ads1220 b0_ads1220;

	/* this should have been "typedef enum b0_result_code b0_result_code;"
	  but the value is interpretted as unsigned (instead of int)
	  see: https://bitbucket.org/cffi/cffi/issues/230 */
	typedef int b0_result_code;

	#define B0_ERR_UNAVAIL -10
	#define B0_OK 0

	enum b0_module_type {
		B0_DIO = 1,
		B0_AOUT = 2,
		B0_AIN = 3,
		B0_SPI = 4,
		B0_I2C = 5,
		B0_PWM = 6
	};

	typedef enum b0_module_type b0_module_type;

	struct b0_device {
		size_t modules_len;
		b0_module **modules;
		uint8_t *name;
		uint8_t *manuf;
		uint8_t *serial;
	};

	struct b0_module {
		b0_module_type type;
		int index;
		uint8_t *name;
		b0_device *device;
		void *backend_data;
		void *frontend_data;
	};

	enum b0_ref_type {
		B0_REF_VOLTAGE = 0,
		B0_REF_CURRENT = 1
	};

	typedef enum b0_ref_type b0_ref_type;

	/* modules */

	enum b0_ain_capab {
		B0_AIN_CAPAB_FORMAT_2COMPL = 0x01,
		B0_AIN_CAPAB_FORMAT_BINARY = 0x00,

		B0_AIN_CAPAB_ALIGN_LSB = 0x00,
		B0_AIN_CAPAB_ALIGN_MSB = 0x02,

		B0_AIN_CAPAB_ENDIAN_LITTLE = 0x00,
		B0_AIN_CAPAB_ENDIAN_BIG = 0x04,

		B0_AIN_CAPAB_SAMPLING_SEQUENTIAL = 0x00,
		B0_AIN_CAPAB_SAMPLING_PARALLEL = 0x10,

		B0_AIN_CAPAB_PACKED = 0x20,

		B0_AIN_CAPAB_FORMAT_MASK = 0x01,
		B0_AIN_CAPAB_ALIGN_MASK = 0x02,
		B0_AIN_CAPAB_ENDIAN_MASK = 0x04,
		B0_AIN_CAPAB_SAMPLING_MASK = 0x10,
	};

	typedef enum b0_ain_capab b0_ain_capab;

	struct b0_ain {
		b0_module header;
		unsigned int chan_count;
		size_t buffer_size;
		b0_ain_capab capab;

		struct {
			uint8_t **chan;
		} label;

		struct {
			double high, low;
			b0_ref_type type;
		} ref;

		/* Practically ADC have a relationship between bitsize and speed
		 * As the bitsize increase, the the sampling frequency (speed) decrease
		 */
		struct b0_ain_mode_bitsize_speeds {
			struct b0_ain_bitsize_speeds {
				unsigned int bitsize;
				struct {
					unsigned long *values;
					size_t count;
				} speed;
			} *values;
			size_t count;
		} stream, snapshot;
	};

	enum b0_aout_capab {
		B0_AOUT_CAPAB_FORMAT_2COMPL = 0x01,
		B0_AOUT_CAPAB_FORMAT_BINARY = 0x00,

		B0_AOUT_CAPAB_ALIGN_LSB = 0x00,
		B0_AOUT_CAPAB_ALIGN_MSB = 0x02,

		B0_AOUT_CAPAB_ENDIAN_LITTLE = 0x00,
		B0_AOUT_CAPAB_ENDIAN_BIG = 0x04,

		/* Repeat supported */
		B0_AOUT_CAPAB_REPEAT = 0x08,

		B0_AOUT_CAPAB_SAMPLING_SEQUENTIAL = 0x00,
		B0_AOUT_CAPAB_SAMPLING_PARALLEL = 0x10,

		B0_AOUT_CAPAB_PACKED = 0x20,

		B0_AOUT_CAPAB_FORMAT_MASK = 0x01,
		B0_AOUT_CAPAB_ALIGN_MASK = 0x02,
		B0_AOUT_CAPAB_ENDIAN_MASK = 0x04,
		B0_AOUT_CAPAB_REPEAT_MASK = 0x08,
		B0_AOUT_CAPAB_SAMPLING_MASK = 0x10,
	};

	typedef enum b0_aout_capab b0_aout_capab;

	struct b0_aout {
		b0_module header;

		unsigned chan_count;
		size_t buffer_size;
		b0_aout_capab capab;

		struct {
			uint8_t **chan;
		} label;

		struct {
			double high, low;
			b0_ref_type type;
		} ref;

		/* Practically DAC have a relationship between bitsize and speed
		 * As the bitsize increase, the the sampling frequency (speed) decrease
		 */
		struct b0_aout_mode_bitsize_speeds {
			struct b0_aout_bitsize_speeds {
				unsigned int bitsize;
				struct {
					unsigned long *values;
					size_t count;
				} speed;
			} *values;
			size_t count;
		} stream, snapshot;
	};

	enum b0_i2c_version {
		B0_I2C_VERSION_SM = 0,
		B0_I2C_VERSION_FM = 1,
		B0_I2C_VERSION_HS = 2,
		B0_I2C_VERSION_HS_CLEANUP1 = 3,
		B0_I2C_VERSION_FMPLUS = 4,
		B0_I2C_VERSION_UFM = 5,
		B0_I2C_VERSION_VER5 = 6,
		B0_I2C_VERSION_VER6 = 7
	};

	typedef enum b0_i2c_version b0_i2c_version;

	struct b0_pwm {
		b0_module header;

		unsigned pin_count;

		struct {
			uint8_t **pin;
		} label;

		struct {
			unsigned int *values;
			size_t count;
		} bitsize;

		struct {
			unsigned long *values;
			size_t count;
		} speed;

		struct {
			double high, low;
			b0_ref_type type;
		} ref;
	};

	typedef unsigned long long int b0_pwm_reg;

	enum b0_dio_capab {
		B0_DIO_CAPAB_OUTPUT = 0x01,
		B0_DIO_CAPAB_INPUT = 0x02,
		B0_DIO_CAPAB_HIZ = 0x04
	};

	typedef enum b0_dio_capab b0_dio_capab;

	struct b0_dio {
		b0_module header;

		unsigned int pin_count;

		b0_dio_capab capab;

		struct {
			uint8_t **pin;
		} label;

		struct {
			double high, low;
			b0_ref_type type;
		} ref;
	};

	struct b0_i2c {
		b0_module header;

		struct {
			uint8_t *sck, *sda;
		} label;

		struct {
			b0_i2c_version *values;
			size_t count;
		} version;

		struct {
			double high, low;
		} ref;
	};

	struct b0_spi {
		b0_module header;

		unsigned ss_count;

		struct {
			uint8_t *sclk, *mosi, *miso;
			uint8_t **ss;
		} label;

		struct {
			unsigned int *values;
			size_t count;
		} bitsize;

		struct {
			unsigned long *values;
			size_t count;
		} speed;

		struct {
			double high, low;
			b0_ref_type type;
		} ref;
	};

	/* constants that need to be accessed [used for b0_device_log()] */
	enum b0_log_level {
		B0_LOG_NONE = 0,
		B0_LOG_ERROR = 1,
		B0_LOG_WARN = 2,
		B0_LOG_INFO = 3,
		B0_LOG_DEBUG = 4
	};

	typedef enum b0_log_level b0_log_level;

	#define B0_DIO_HIGH 1
	#define B0_DIO_LOW 0

	#define B0_DIO_OUTPUT 1
	#define B0_DIO_INPUT 0

	#define B0_DIO_ENABLE 1
	#define B0_DIO_DISABLE 0

	/* H-Bridge values */
	enum {
		/* primitve values */
		B0_HBRIDGE_EN = 0x01,
		B0_HBRIDGE_A1 = 0x02,
		B0_HBRIDGE_A2 = 0x04,

		/* Higher level functions */
		B0_HBRIDGE_DISABLE = 0x00,
		B0_HBRIDGE_FORWARD = 0x03 /* B0_HBRIDGE_EN | B0_HBRIDGE_A1 */,
		B0_HBRIDGE_BACKWARD = 0x05 /* B0_HBRIDGE_EN | B0_HBRIDGE_A2 */,
	};

	/* MCP342x */
	enum b0_mcp342x_adr {
		B0_MCP342X_LOW = 0,
		B0_MCP342X_FLOAT = 1,
		B0_MCP342X_HIGH = 2
	};

	enum b0_mcp342x_chan {
		B0_MCP342X_CH1 = 0,
		B0_MCP342X_CH2 = 1,
		B0_MCP342X_CH3 = 2,
		B0_MCP342X_CH4 = 3
	};

	enum b0_mcp342x_gain {
		B0_MCP342X_GAIN1 = 0,
		B0_MCP342X_GAIN2 = 1,
		B0_MCP342X_GAIN4 = 2,
		B0_MCP342X_GAIN8 = 3
	};

	enum b0_mcp342x_samp_rate {
		B0_MCP342X_SAMP_RATE_240 = 0,
		B0_MCP342X_SAMP_RATE_60 = 1,
		B0_MCP342X_SAMP_RATE_15 = 2
	};

	typedef enum b0_mcp342x_adr b0_mcp342x_adr;
	typedef enum b0_mcp342x_chan b0_mcp342x_chan;
	typedef enum b0_mcp342x_gain b0_mcp342x_gain;
	typedef enum b0_mcp342x_samp_rate b0_mcp342x_samp_rate;

	/* ADS1220 */
	enum b0_ads1220_filter {
		B0_ADS1220_FILTER_NONE = 0,
		B0_ADS1220_FILTER_50HZ = 1,
		B0_ADS1220_FILTER_60HZ = 2,
		B0_ADS1220_FILTER_50HZ_60HZ = 3
	};

	enum b0_ads1220_vref_source {
		B0_ADS1220_VREF_INTERNAL = 0,
		B0_ADS1220_VREF_REFP0_REFN0 = 1,
		B0_ADS1220_VREF_REFP1_REFN1 = 2,
		B0_ADS1220_VREF_AVDD_AVSS = 3
	};

	enum b0_ads1220_gain {
		B0_ADS1220_GAIN_1 = 0,
		B0_ADS1220_GAIN_2 = 1,
		B0_ADS1220_GAIN_4 = 2,
		B0_ADS1220_GAIN_8 = 3,
		B0_ADS1220_GAIN_16 = 4,
		B0_ADS1220_GAIN_32 = 5,
		B0_ADS1220_GAIN_64 = 6,
		B0_ADS1220_GAIN_128 = 7
	};

	typedef enum b0_ads1220_filter b0_ads1220_filter;
	typedef enum b0_ads1220_gain b0_ads1220_gain;
	typedef enum b0_ads1220_vref_source b0_ads1220_vref_source;

	struct b0_version {
		uint8_t major;
		uint8_t minor;
		uint8_t patch;
	};

	#define B0V5_PS_PM5 0x01 /* ±5V power supply */
	#define B0V5_PS_P3V3 0x02 /* +3.3V power supply */

	/* I2C task */
	enum b0_i2c_task_flag {
		B0_I2C_TASK_LAST = 0x01, /**< Last task to execute */

		B0_I2C_TASK_WRITE = 0x00, /**< Perform write */
		B0_I2C_TASK_READ = 0x02, /**< Perform read */

		B0_I2C_TASK_DIR_MASK = 0x02,
	};

	typedef enum b0_i2c_task_flag b0_i2c_task_flag;

	struct b0_i2c_task {
		b0_i2c_task_flag flags; /* Transfer flags */
		uint8_t addr; /* Slave address */
		b0_i2c_version version; /* Protocol to use */
		void *data; /* Pointer to data */
		size_t count; /* Number of bytes to transfer */
	};

	typedef struct b0_i2c_task b0_i2c_task;

	struct b0_i2c_sugar_arg {
		uint8_t addr;
		b0_i2c_version version;
	};

	typedef struct b0_i2c_sugar_arg b0_i2c_sugar_arg;

	/* SPI task */
	enum b0_spi_task_flags {
		B0_SPI_TASK_LAST = 0x01, /* Last task to execute */

		B0_SPI_TASK_CPHA = 0x02,
		B0_SPI_TASK_CPOL = 0x04,

		B0_SPI_TASK_MODE0 = 0,
		B0_SPI_TASK_MODE1 = 0x02,
		B0_SPI_TASK_MODE2 = 0x04,
		B0_SPI_TASK_MODE3 = 0x06,

		B0_SPI_TASK_FD = 0x00,
		B0_SPI_TASK_HD_READ = 0x18,
		B0_SPI_TASK_HD_WRITE = 0x08,

		B0_SPI_TASK_MSB_FIRST = 0x00,
		B0_SPI_TASK_LSB_FIRST = 0x20,

		B0_SPI_TASK_MODE_MASK = 0x06,
		B0_SPI_TASK_DUPLEX_MASK = 0x18,
		B0_SPI_TASK_ENDIAN_MASK = 0x20
	};

	typedef enum b0_spi_task_flags b0_spi_task_flags;

	struct b0_spi_task {
		b0_spi_task_flags flags; /**< Task flags */
		unsigned int addr; /**< Slave address */
		unsigned long speed; /**< Communication speed */
		unsigned int bitsize; /**< Bitsize to use for transfer */
		const void *wdata; /**< Write memory */
		void *rdata; /**< Read memory */
		size_t count; /**< Number of data unit */
	};

	typedef struct b0_spi_task b0_spi_task;

	struct b0_spi_sugar_arg {
		unsigned int addr;
		b0_spi_task_flags flags;
		unsigned int bitsize;
		unsigned long speed;
	};

	typedef struct b0_spi_sugar_arg b0_spi_sugar_arg;

	/* module */
	b0_result_code b0_module_openable(b0_module *mod);

	/* user accessible method for device */
	b0_result_code b0_device_close(b0_device *dev);
	b0_result_code b0_device_log(b0_device *dev, b0_log_level level);
	b0_result_code b0_device_ping(b0_device *dev);

	/* function for result codes */
	const uint8_t* b0_result_name(b0_result_code r);
	const uint8_t* b0_result_explain(b0_result_code r);

	/* AIN related */
	b0_result_code b0_ain_close(b0_ain *mod);
	b0_result_code b0_ain_open(b0_device *dev, b0_ain **mod, int index);

	b0_result_code b0_ain_chan_seq_set(b0_ain *mod, unsigned int *values, size_t count);
	b0_result_code b0_ain_chan_seq_get(b0_ain *mod, unsigned int *values, size_t *count);
	b0_result_code b0_ain_bitsize_speed_set(b0_ain *mod, unsigned int bitsize, unsigned long speed);
	b0_result_code b0_ain_bitsize_speed_get(b0_ain *mod, unsigned int *bitsize, unsigned long *speed);

	/* AIN stream API */
	b0_result_code b0_ain_stream_prepare(b0_ain *mod);
	b0_result_code b0_ain_stream_start(b0_ain *mod);
	b0_result_code b0_ain_stream_read(b0_ain *mod, void *samples, size_t count, size_t *actual_len);
	b0_result_code b0_ain_stream_read_float(b0_ain *mod, float *samples, size_t count, size_t *actual_len);
	b0_result_code b0_ain_stream_read_double(b0_ain *mod, double *samples, size_t count, size_t *actual_len);
	b0_result_code b0_ain_stream_stop(b0_ain *mod);

	/* AIN snapshot API */
	b0_result_code b0_ain_snapshot_prepare(b0_ain *mod);
	b0_result_code b0_ain_snapshot_start(b0_ain *mod, void *buffer, size_t buffer_data);
	b0_result_code b0_ain_snapshot_start_double(b0_ain *mod, double *buffer, size_t buffer_data);
	b0_result_code b0_ain_snapshot_start_float(b0_ain *mod, float *buffer, size_t buffer_data);
	b0_result_code b0_ain_snapshot_stop(b0_ain *mod);

	/* AOUT API */
	b0_result_code b0_aout_close(b0_aout *mod);
	b0_result_code b0_aout_open(b0_device *dev, b0_aout **mod, int index);

	b0_result_code b0_aout_chan_seq_set(b0_aout *mod, unsigned int *values, size_t count);
	b0_result_code b0_aout_chan_seq_get(b0_aout *mod, unsigned int *values, size_t *count);
	b0_result_code b0_aout_bitsize_speed_set(b0_aout *mod, unsigned int bitsize, unsigned long speed);
	b0_result_code b0_aout_bitsize_speed_get(b0_aout *mod, unsigned int *bitsize, unsigned long *speed);
	b0_result_code b0_aout_repeat_set(b0_aout *mod, unsigned long value);
	b0_result_code b0_aout_repeat_get(b0_aout *mod, unsigned long *value);

	/* AOUT: stream API */
	b0_result_code b0_aout_stream_prepare(b0_aout *mod);
	b0_result_code b0_aout_stream_write(b0_aout *mod, void *data, size_t len);
	b0_result_code b0_aout_stream_write_double(b0_aout *mod, double *data, size_t len);
	b0_result_code b0_aout_stream_write_float(b0_aout *mod, float *data, size_t len);
	b0_result_code b0_aout_stream_start(b0_aout *mod);
	b0_result_code b0_aout_stream_stop(b0_aout *mod);

	/* AOUT: snapshot API */
	b0_result_code b0_aout_snapshot_prepare(b0_aout *mod);
	b0_result_code b0_aout_snapshot_start(b0_aout *mod, void *data, size_t len);
	b0_result_code b0_aout_snapshot_start_double(b0_aout *mod, double *data, size_t len);
	b0_result_code b0_aout_snapshot_start_float(b0_aout *mod, float *data, size_t len);
	b0_result_code b0_aout_snapshot_stop(b0_aout *mod);
	b0_result_code b0_aout_snapshot_calc(b0_aout *mod, double freq,
			uint8_t bitsize, size_t *count, uint32_t *speed);

	/* Module: PWM */
	b0_result_code b0_pwm_close(b0_pwm *mod);
	b0_result_code b0_pwm_open(b0_device *dev, b0_pwm **mod, int index);

	b0_result_code b0_pwm_width_set(b0_pwm *mod, uint8_t index, b0_pwm_reg width);
	b0_result_code b0_pwm_width_get(b0_pwm *mod, uint8_t index, b0_pwm_reg *width);
	b0_result_code b0_pwm_period_set(b0_pwm *mod, b0_pwm_reg period);
	b0_result_code b0_pwm_period_get(b0_pwm *mod, b0_pwm_reg *period);
	b0_result_code b0_pwm_speed_set(b0_pwm *mod, unsigned long value);
	b0_result_code b0_pwm_speed_get(b0_pwm *mod, unsigned long *value);
	b0_result_code b0_pwm_bitsize_set(b0_pwm *mod, unsigned int value);
	b0_result_code b0_pwm_bitsize_get(b0_pwm *mod, unsigned int *value);

	/* PWM: output API */
	b0_result_code b0_pwm_output_prepare(b0_pwm *mod);
	b0_result_code b0_pwm_output_calc(b0_pwm *mod, unsigned int bitsize,
						double freq_user, uint32_t *speed, b0_pwm_reg *period,
						double max_error, bool best_result);
	b0_result_code b0_pwm_output_start(b0_pwm *mod);
	b0_result_code b0_pwm_output_stop(b0_pwm *mod);

	/* Module : DIO */
	b0_result_code b0_dio_close(b0_dio *mod);
	b0_result_code b0_dio_open(b0_device *dev, b0_dio **mod, int index);

	b0_result_code b0_dio_value_get(b0_dio *mod, unsigned pin, bool *value);
	b0_result_code b0_dio_value_set(b0_dio *mod, unsigned pin, bool value);
	b0_result_code b0_dio_value_toggle(b0_dio *mod, unsigned pin);
	b0_result_code b0_dio_dir_get(b0_dio *mod, unsigned pin, bool *value);
	b0_result_code b0_dio_dir_set(b0_dio *mod, unsigned pin, bool value);
	b0_result_code b0_dio_hiz_get(b0_dio *mod, unsigned pin, bool *value);
	b0_result_code b0_dio_hiz_set(b0_dio *mod, unsigned pin, bool value);

	b0_result_code b0_dio_multiple_value_set(b0_dio *mod,
				unsigned *pins, size_t size, bool value);
	b0_result_code b0_dio_multiple_value_get(b0_dio *mod,
				unsigned *pins, bool *values, size_t size);
	b0_result_code b0_dio_multiple_value_toggle(b0_dio *mod,
				unsigned *pins, size_t size);
	b0_result_code b0_dio_multiple_dir_set(b0_dio *mod,
				unsigned *pins, size_t size, bool value);
	b0_result_code b0_dio_multiple_dir_get(b0_dio *mod,
				unsigned *pins, bool *values, size_t size);
	b0_result_code b0_dio_multiple_hiz_get(b0_dio *mod,
				unsigned *pins, bool *values, size_t size);
	b0_result_code b0_dio_multiple_hiz_set(b0_dio *mod,
				unsigned *pins, size_t size, bool value);

	b0_result_code b0_dio_all_value_set(b0_dio *mod, bool value);
	b0_result_code b0_dio_all_value_get(b0_dio *mod, bool *values);
	b0_result_code b0_dio_all_value_toggle(b0_dio *mod);
	b0_result_code b0_dio_all_dir_set(b0_dio *mod, bool value);
	b0_result_code b0_dio_all_dir_get(b0_dio *mod, bool *values);
	b0_result_code b0_dio_all_hiz_get(b0_dio *mod, bool *values);
	b0_result_code b0_dio_all_hiz_set(b0_dio *mod, bool value);

	/* DIO: basic API */
	b0_result_code b0_dio_basic_prepare(b0_dio *mod);
	b0_result_code b0_dio_basic_start(b0_dio *mod);
	b0_result_code b0_dio_basic_stop(b0_dio *mod);

	/* Module: I2C */
	b0_result_code b0_i2c_close(b0_i2c *mod);
	b0_result_code b0_i2c_open(b0_device *dev, b0_i2c **mod, int index);

	/* I2C: master API */
	b0_result_code b0_i2c_master_prepare(b0_i2c *mod);
	b0_result_code b0_i2c_master_start(b0_i2c *mod, const b0_i2c_task *tasks,
		int *failed_task_index, int *failed_task_ack);
	b0_result_code b0_i2c_master_stop(b0_i2c *mod);
	b0_result_code b0_i2c_master_read(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		void *data, size_t count);
	b0_result_code b0_i2c_master_write8_read(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		uint8_t write, void *read_data, size_t read_count);
	b0_result_code b0_i2c_master_write(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		void *data, size_t count);
	b0_result_code b0_i2c_master_write_read(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		void *write_data, size_t write_count, void *read_data, size_t read_count);
	b0_result_code b0_i2c_master_slave_id(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		uint16_t *manuf, uint16_t *part, uint8_t *rev);
	b0_result_code b0_i2c_master_slave_detect(b0_i2c *mod, const b0_i2c_sugar_arg *arg,
		bool *detected);
	b0_result_code b0_i2c_master_slaves_detect(b0_i2c *mod, b0_i2c_version version,
		uint8_t *addresses, bool *detected, size_t count, size_t *processed);

	/* Module: SPI */
	b0_result_code b0_spi_close(b0_spi *mod);
	b0_result_code b0_spi_open(b0_device *dev, b0_spi **mod, int index);

	b0_result_code b0_spi_active_state_set(b0_spi *mod, unsigned addr,
		bool value);
	b0_result_code b0_spi_active_state_get(b0_spi *mod, unsigned addr,
		bool *value);

	b0_result_code b0_spi_speed_set(b0_spi *mod, unsigned long speed);
	b0_result_code b0_spi_speed_get(b0_spi *mod, unsigned long *speed);

	b0_result_code b0_spi_master_prepare(b0_spi *mod);
	b0_result_code b0_spi_master_start(b0_spi *mod, const b0_spi_task *tasks,
		int *failed_task_index, int *failed_task_count);
	b0_result_code b0_spi_master_stop(b0_spi *mod);
	b0_result_code b0_spi_master_fd(b0_spi *mod, const b0_spi_sugar_arg *arg,
		const void *write_data, void *read_data, size_t count);
	b0_result_code b0_spi_master_hd_read(b0_spi *mod, const b0_spi_sugar_arg *arg,
		void *data, size_t count);
	b0_result_code b0_spi_master_hd_write(b0_spi *mod, const b0_spi_sugar_arg *arg,
		const void *data, size_t count);
	b0_result_code b0_spi_master_hd_write_read(b0_spi *mod, const b0_spi_sugar_arg *arg,
		const void *write_data, size_t write_count, void *read_data,
		size_t read_count);

	uint32_t b0_version_extract(b0_version *ver);

	/* USB Backend */
	b0_result_code b0_usb_open_vid_pid(b0_device **_dev, uint16_t vid, uint16_t pid);
	b0_result_code b0_usb_open(libusb_device *udevice, b0_device **_dev);
	b0_result_code b0_usb_open_handle(libusb_device_handle *uhandle, b0_device **_dev);
	b0_result_code b0_usb_open_supported(b0_device **dev);

	b0_result_code b0_usb_libusb_device_handle(b0_device *dev,
		libusb_device_handle **usbdh);
	b0_result_code b0_usb_libusb_context(b0_device *dev, libusb_context **usbc);
	b0_result_code b0_usb_libusb_device(b0_device *dev, libusb_device **usbd);

	b0_result_code b0_usb_device_bulk_timeout(b0_device *dev, unsigned timeout);
	b0_result_code b0_usb_device_ctrlreq_timeout(b0_device *dev, unsigned timeout);
	b0_result_code b0_usb_ain_stream_delay(b0_ain *mod, unsigned delay);
	b0_result_code b0_usb_aout_stream_pending(b0_aout *mod, unsigned pending);

	/* ADXL345 */
	b0_result_code b0_adxl345_open_i2c(b0_i2c *mod, b0_adxl345 **drv, bool ALT_ADDRESS);
	b0_result_code b0_adxl345_close(b0_adxl345 *drv);
	b0_result_code b0_adxl345_read(b0_adxl345 *drv, double *x, double *y, double *z);
	b0_result_code b0_adxl345_power_up(b0_adxl345 *drv);

	/* H-Bridge */
	b0_result_code b0_hbridge_open(b0_dio *mod,
		b0_hbridge **drv, unsigned int EN, unsigned int A1, unsigned int A2);
	b0_result_code b0_hbridge_close(b0_hbridge *drv);

	b0_result_code b0_hbridge_set(b0_hbridge *drv, int value);

	/* MCP342x */
	b0_result_code b0_mcp342x_open(b0_i2c *mod, b0_mcp342x **drv,
		b0_mcp342x_adr Adr1, b0_mcp342x_adr Adr0);
	b0_result_code b0_mcp342x_close(b0_mcp342x *drv);
	b0_result_code b0_mcp342x_chan_set(b0_mcp342x *drv, b0_mcp342x_chan chan);
	b0_result_code b0_mcp342x_gain_set(b0_mcp342x *drv, b0_mcp342x_gain gain);
	b0_result_code b0_mcp342x_samp_rate_set(b0_mcp342x *drv,
		b0_mcp342x_samp_rate samp_rate);
	b0_result_code b0_mcp342x_read(b0_mcp342x *drv, double *value);

	/* ADS1220 */
	b0_result_code b0_ads1220_open(b0_spi *mod, b0_ads1220 **drv, unsigned addr);
	b0_result_code b0_ads1220_close(b0_ads1220 *drv);
	b0_result_code b0_ads1220_read(b0_ads1220 *drv, double *value);
	b0_result_code b0_ads1220_reset(b0_ads1220 *drv);
	b0_result_code b0_ads1220_start(b0_ads1220 *drv);
	b0_result_code b0_ads1220_power_down(b0_ads1220 *drv);
	b0_result_code b0_ads1220_gain_set(b0_ads1220 *drv, b0_ads1220_gain gain);
	b0_result_code b0_ads1220_pga_bypass_set(b0_ads1220 *drv, bool bypass);
	b0_result_code b0_ads1220_vref_set(b0_ads1220 *drv,
		b0_ads1220_vref_source source, double low, double high);
	b0_result_code b0_ads1220_filter_set(b0_ads1220 *drv, b0_ads1220_filter type);

	/* BMP180 */
	enum b0_bmp180_over_samp {
		B0_BMP180_OVER_SAMP_1 = 0,
		B0_BMP180_OVER_SAMP_2 = 1,
		B0_BMP180_OVER_SAMP_4 = 2,
		B0_BMP180_OVER_SAMP_8 = 3
	};

	typedef enum b0_bmp180_over_samp b0_bmp180_over_samp;
	typedef struct b0_bmp180 b0_bmp180;

	b0_result_code b0_bmp180_open(b0_i2c *mod, b0_bmp180 **drv);
	b0_result_code b0_bmp180_over_samp_set(b0_bmp180 *drv,
		b0_bmp180_over_samp over_sampling);
	b0_result_code b0_bmp180_close(b0_bmp180 *drv);
	b0_result_code b0_bmp180_read(b0_bmp180 *drv, double *pressure, double *temp);

	/* box-v5 */
	b0_result_code b0v5_valid_test(b0_device *dev);

	b0_result_code b0v5_ps_en_set(b0_device *dev, uint8_t mask, uint8_t value);
	b0_result_code b0v5_ps_en_get(b0_device *dev, uint8_t *value);
	b0_result_code b0v5_ps_oc_get(b0_device *dev, uint8_t *value);
	b0_result_code b0v5_ps_oc_ack(b0_device *dev, uint8_t mask);

	b0_result_code b0v5_nvm_read(b0_device *dev,
				size_t offset, void *data, size_t size);
	b0_result_code b0v5_nvm_write(b0_device *dev, size_t offset,
				const void *data, size_t size);

	struct b0v5_calib_value {
		/* calib_output = (uncalib_input * gain) - offset */
		float offset;
		float gain;
	};

	typedef struct b0v5_calib_value b0v5_calib_value;

	struct b0v5_calib {
		struct {
			struct b0v5_calib_value *values;
			size_t count;
		} ain0, aout0;
	};

	typedef struct b0v5_calib b0v5_calib;

	b0_result_code b0v5_calib_read(b0_device *dev,
			struct b0v5_calib *calib);
	b0_result_code b0v5_calib_write(b0_device *dev,
			const struct b0v5_calib *calib);
""")

# https://bitbucket.org/cffi/cffi/issues/219
import sys
ext = "so" if sys.platform != "win32" else "dll"
libbox0 = ffi.dlopen("libbox0." + ext)

ffi.cdef("""size_t strlen(const char *);""")
libc = ffi.dlopen(None)

def string_converter(libbox0_str):
	"""
	convert *libbox0_str* to python string

	:param libbox0_str: string buffer with utf-8 and NULL terimation
	:return: python unicode version of *libbox0_str*
	:rtype: str
	"""
	if libbox0_str == ffi.NULL:
		return None

	global libc
	bytes_count = libc.strlen(ffi.cast("char *", libbox0_str))
	buf = ffi.buffer(libbox0_str, bytes_count)
	return codecs.decode(buf, "utf-8")

def string_array_converter(libbox0_str_array, count):
	"""
	convert *libbox0_str_array* to python string array

	:param libbox0_str_array: string array of utf-8 (with entries NULL for empty)
	:param count: Number of item in *libbox0_str_array*
	:return: python unicode string array
	:rtype: array
	"""
	return [string_converter(libbox0_str_array[i]) for i in range(count)]

class DummyObject(object):
	pass

def cast_to_array(ret_type, values, count=None):
	if count is None:
		# alternative naming, values = {
		#	values: <pointer to values>,
		#	count: <number of elements>
		# }
		count = values.count
		values = values.values

	return ffi.cast("%s [%i]" % (ret_type, count), values)

def mode_bitsize_speeds(mode):
	result = []

	for i in range(mode.count):
		value = mode.values[i]
		obj = DummyObject()
		obj.bitsize = value.bitsize
		obj.speed = cast_to_array("unsigned long", value.speed)
		result.append(obj)

	return result
