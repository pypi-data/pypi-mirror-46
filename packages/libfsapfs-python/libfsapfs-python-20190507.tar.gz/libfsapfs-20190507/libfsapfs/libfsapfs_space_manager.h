/*
 * The space manager functions
 *
 * Copyright (C) 2018-2019, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _LIBFSAPFS_SPACE_MANAGER_H )
#define _LIBFSAPFS_SPACE_MANAGER_H

#include <common.h>
#include <types.h>

#include "libfsapfs_libbfio.h"
#include "libfsapfs_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct libfsapfs_space_manager libfsapfs_space_manager_t;

struct libfsapfs_space_manager
{
	/* Dummy
	 */
	int dummy;
};

int libfsapfs_space_manager_initialize(
     libfsapfs_space_manager_t **space_manager,
     libcerror_error_t **error );

int libfsapfs_space_manager_free(
     libfsapfs_space_manager_t **space_manager,
     libcerror_error_t **error );

int libfsapfs_space_manager_read_file_io_handle(
     libfsapfs_space_manager_t *space_manager,
     libbfio_handle_t *file_io_handle,
     off64_t file_offset,
     libcerror_error_t **error );

int libfsapfs_space_manager_read_data(
     libfsapfs_space_manager_t *space_manager,
     const uint8_t *data,
     size_t data_size,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFSAPFS_SPACE_MANAGER_H ) */

