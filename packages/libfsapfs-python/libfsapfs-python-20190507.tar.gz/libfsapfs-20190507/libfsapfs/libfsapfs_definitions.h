/*
 * The internal definitions
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

#if !defined( _LIBFSAPFS_INTERNAL_DEFINITIONS_H )
#define _LIBFSAPFS_INTERNAL_DEFINITIONS_H

#include <common.h>
#include <byte_stream.h>

#define LIBFSAPFS_ENDIAN_BIG					_BYTE_STREAM_ENDIAN_BIG
#define LIBFSAPFS_ENDIAN_LITTLE					_BYTE_STREAM_ENDIAN_LITTLE

/* Define HAVE_LOCAL_LIBFSAPFS for local use of libfsapfs
 */
#if !defined( HAVE_LOCAL_LIBFSAPFS )
#include <libfsapfs/definitions.h>

/* The definitions in <libfsapfs/definitions.h> are copied here
 * for local use of libfsapfs
 */
#else
#define LIBFSAPFS_VERSION					20190507

/* The version string
 */
#define LIBFSAPFS_VERSION_STRING				"20190507"

/* The file access
 * bit 1        set to 1 for read access
 * bit 2        set to 1 for write access
 * bit 3-8      not used
 */
enum LIBFSAPFS_ACCESS_FLAGS
{
	LIBFSAPFS_ACCESS_FLAG_READ				= 0x01,
/* Reserved: not supported yet */
	LIBFSAPFS_ACCESS_FLAG_WRITE				= 0x02
};

/* The file access macros
 */
#define LIBFSAPFS_OPEN_READ					( LIBFSAPFS_ACCESS_FLAG_READ )
/* Reserved: not supported yet */
#define LIBFSAPFS_OPEN_WRITE					( LIBFSAPFS_ACCESS_FLAG_WRITE )
/* Reserved: not supported yet */
#define LIBFSAPFS_OPEN_READ_WRITE				( LIBFSAPFS_ACCESS_FLAG_READ | LIBFSAPFS_ACCESS_FLAG_WRITE )

/* The path segment separator
 */
#define LIBFSAPFS_SEPARATOR					'/'

#endif /* !defined( HAVE_LOCAL_LIBFSAPFS ) */

/* The compression methods
 */
enum LIBFSAPFS_COMPRESSION_METHODS
{
	LIBFSAPFS_COMPRESSION_METHOD_NONE			= 0,
	LIBFSAPFS_COMPRESSION_METHOD_DEFLATE			= 1,
	LIBFSAPFS_COMPRESSION_METHOD_LZVN			= 2,

	LIBFSAPFS_COMPRESSION_METHOD_UNKNOWN5			= 5
};

/* The crypt modes
 */
enum LIBFSAPFS_ENCRYPTION_CRYPT_MODES
{
	LIBFSAPFS_ENCRYPTION_CRYPT_MODE_DECRYPT			= 0,
	LIBFSAPFS_ENCRYPTION_CRYPT_MODE_ENCRYPT			= 1
};

/* The encryption methods
 */
enum LIBFSAPFS_ENCRYPTION_METHODS
{
	LIBFSAPFS_ENCRYPTION_METHOD_AES_256_XTS			= 0,
	LIBFSAPFS_ENCRYPTION_METHOD_AES_128_XTS			= 2
};

/* The file system B-tree data type
 */
enum LIBFSAPFS_FILE_SYSTEM_DATA_TYPES
{
	LIBFSAPFS_FILE_SYSTEM_DATA_TYPE_INODE			= 3,
	LIBFSAPFS_FILE_SYSTEM_DATA_TYPE_EXTENDED_ATTRIBUTE	= 4,

	LIBFSAPFS_FILE_SYSTEM_DATA_TYPE_FILE_EXTENT		= 8,
	LIBFSAPFS_FILE_SYSTEM_DATA_TYPE_DIRECTORY_RECORD	= 9
};

#define LIBFSAPFS_MAXIMUM_CACHE_ENTRIES_BTREE_NODES		8192
#define LIBFSAPFS_MAXIMUM_CACHE_ENTRIES_DATA_BLOCKS		16

#define LIBFSAPFS_MAXIMUM_BTREE_NODE_RECURSION_DEPTH		256

#endif /* !defined( _LIBFSAPFS_INTERNAL_DEFINITIONS_H ) */

