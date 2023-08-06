/* oo_READ_BINARY.h
 *
 * Copyright (C) 1994-2012,2013,2014,2015,2016,2017 Paul Boersma
 *
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This code is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this work. If not, see <http://www.gnu.org/licenses/>.
 */

#include "oo_undef.h"

#define oo_SIMPLE(type,storage,x)  \
	our x = binget##storage (f);

#define oo_ARRAY(type,storage,x,cap,n)  \
	if (n > cap) Melder_throw (U"Number of \"" #x U"\" (", n, U") greater than ", cap, U"."); \
	for (int i = 0; i < n; i ++) { \
		our x [i] = binget##storage (f); \
	}

#define oo_SET(type,storage,x,setType)  \
	for (int i = 0; i <= (int) setType::MAX; i ++) { \
		our x [i] = binget##storage (f); \
	}

#define oo_VECTOR(type,storage,x,min,max)  \
	if (max >= min) { \
		our x = NUMvector_readBinary_##storage (min, max, f); \
	}

#define oo_MATRIX(type,storage,x,row1,row2,col1,col2)  \
	if (row2 >= row1 && col2 >= col1) { \
	    our x = NUMmatrix_readBinary_##storage (row1, row2, col1, col2, f); \
	}

#define oo_ENUMx(kType,storage,x)  \
	our x = (kType) binget##storage (f, (int) kType::MIN, (int) kType::MAX, U"" #kType);

//#define oo_ENUMx_ARRAY(kType,storage,x,cap,n)  \
//	if (n > cap) Melder_throw (U"Number of \"" #x U"\" (", n, U") greater than ", cap, U"."); \
//	for (int i = 0; i < n; i ++) { \
//		our x [i] = (kType) binget##storage (f, (int) kType::MIN, (int) kType::MAX, U"" #kType); \
//	}

//#define oo_ENUMx_SET(kType,storage,x,setType)  \
//	for (int i = 0; i <= (int) setType::MAX; i ++) { \
//		our x [i] = (kType) binget##storage (f, (int) kType::MIN, (int) kType::MAX, U"" #kType); \
//	}

//#define oo_ENUMx_VECTOR(kType,storage,x,min,max)  \
//	if (max >= min) { \
//		our x = NUMvector <type> (min, max); \
//		for (integer i = min; i <= max; i ++) { \
//			our x [i] = (kType) binget##storage (f, (int) kType::MIN, (int) kType::MAX, U"" #kType); \
//	}

#define oo_STRINGx(storage,x)  \
	our x = binget##storage (f);

#define oo_STRINGx_ARRAY(storage,x,cap,n)  \
	if (n > cap) Melder_throw (U"Number of \"" #x U"\" (", n, U") greater than ", cap, U"."); \
	for (int i = 0; i < n; i ++) { \
		our x [i] = binget##storage (f); \
	}

#define oo_STRINGx_SET(storage,x,setType)  \
	for (int i = 0; i <= setType::MAX; i ++) { \
		our x [i] = binget##storage (f); \
	}

#define oo_STRINGx_VECTOR(storage,x,min,max)  \
	if (max >= min) { \
		our x = NUMvector <char32 *> (min, max); \
		for (integer i = min; i <= max; i ++) { \
			our x [i] = binget##storage (f); \
		} \
	}

#define oo_STRUCT(Type,x)  \
	our x. readBinary (f, formatVersion);

#define oo_STRUCT_ARRAY(Type,x,cap,n) \
	if (n > cap) Melder_throw (U"Number of \"", #x, U"\" (", n, U") greater than ", cap, U"."); \
	for (int i = 0; i < n; i ++) { \
		our x [i]. readBinary (f, formatVersion); \
	}

#define oo_STRUCT_SET(Type,x,setType) \
	for (int i = 0; i <= (int) setType::MAX; i ++) { \
		our x [i]. readBinary (f, formatVersion); \
	}

#define oo_STRUCT_VECTOR_FROM(Type,x,min,max)  \
	if (max >= min) { \
		our x = NUMvector <struct##Type> (min, max); \
		for (integer i = min; i <= max; i ++) { \
			our x [i]. readBinary (f, formatVersion); \
		} \
	}

#define oo_STRUCT_MATRIX_FROM(Type,x,row1,row2,col1,col2)  \
	if (row2 >= row1 && col2 >= col1) { \
		our x = NUMmatrix <struct##Type> (row1, row2, col1, col2); \
		for (integer i = row1; i <= row2; i ++) { \
			for (integer j = col1; j <= col2; j ++) { \
				our x [i] [j]. readBinary (f, formatVersion); \
			} \
		} \
	}

#define oo_AUTO_OBJECT(Class,formatVersion,x)  \
	if (bingetex (f)) { \
		our x = Thing_new (Class); \
		our x -> v_readBinary (f, formatVersion); \
	}

#define oo_COLLECTION_OF(Class,x,ItemClass,formatVersion)  \
	{ \
		integer n = bingetinteger (f); \
		for (integer i = 1; i <= n; i ++) { \
			auto##ItemClass item = Thing_new (ItemClass); \
			item -> v_readBinary (f, formatVersion); \
			our x.addItem_move (item.move()); \
		} \
	}

#define oo_AUTO_COLLECTION(Class,x,ItemClass,formatVersion)  \
	{ \
		integer n = bingetinteger (f); \
		our x = Class##_create (); \
		for (integer i = 1; i <= n; i ++) { \
			auto##ItemClass item = Thing_new (ItemClass); \
			item -> v_readBinary (f, formatVersion); \
			our x -> addItem_move (item.move()); \
		} \
	}

#define oo_FILE(x)

#define oo_DIR(x)

#define oo_DEFINE_STRUCT(Type)  \
	void struct##Type :: readBinary (FILE *f, int formatVersion) { \
		(void) formatVersion;

#define oo_END_STRUCT(Type)  \
	}

#define oo_DEFINE_CLASS(Class,Parent)  \
	void struct##Class :: v_readBinary (FILE *f, int formatVersion) { \
		if (formatVersion > our classInfo -> version) \
			Melder_throw (U"The format of this file is too new. Download a newer version of Praat."); \
		Class##_Parent :: v_readBinary (f, formatVersion);

#define oo_END_CLASS(Class)  \
	}

#define oo_IF(condition)  \
	if (condition) {

#define oo_ENDIF  \
	}

#define oo_FROM(from)  \
	if (formatVersion >= from) {

#define oo_ENDFROM  \
	}

#define oo_DECLARING  0
#define oo_DESTROYING  0
#define oo_COPYING  0
#define oo_COMPARING  0
#define oo_VALIDATING_ENCODING  0
#define oo_READING  1
#define oo_READING_TEXT  0
#define oo_READING_BINARY  1
#define oo_WRITING  0
#define oo_WRITING_TEXT  0
#define oo_WRITING_BINARY  0
#define oo_DESCRIBING  0

/* End of file oo_READ_BINARY.h */
