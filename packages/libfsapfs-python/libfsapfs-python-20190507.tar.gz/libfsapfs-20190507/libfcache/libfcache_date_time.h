/*
 * Date and time functions
 *
 * Copyright (C) 2010-2018, Joachim Metz <joachim.metz@gmail.com>
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

#if !defined( _LIBFCACHE_DATE_TIME_H )
#define _LIBFCACHE_DATE_TIME_H

#include <common.h>

#include "libfcache_extern.h"
#include "libfcache_libcerror.h"
#include "libfcache_types.h"

#if defined( __cplusplus )
extern "C" {
#endif

LIBFCACHE_EXTERN \
int libfcache_date_time_get_timestamp(
     int64_t *timestamp,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBFCACHE_DATE_TIME_H ) */

