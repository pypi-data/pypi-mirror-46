/*
 * The internal inline definition
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

#if !defined( _LIBFDATA_INTERNAL_INLINE_H )
#define _LIBFDATA_INTERNAL_INLINE_H

#include <common.h>

#if defined( _MSC_VER )
#define LIBFDATA_INLINE _inline

#elif defined( __BORLANDC__ )
#define LIBFDATA_INLINE /* inline */

#else
#define LIBFDATA_INLINE inline

#endif

#endif

