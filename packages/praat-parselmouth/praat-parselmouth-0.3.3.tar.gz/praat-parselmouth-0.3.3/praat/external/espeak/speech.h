/*
 * Copyright (C) 2005 to 2007 by Jonathan Duddington
 * email: jonsd@users.sourceforge.net
 * Copyright (C) 2013-2015 Reece H. Dunn
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see: <http://www.gnu.org/licenses/>.
 */

#ifndef SPEECH_H
#define SPEECH_H

#if defined(BYTE_ORDER) && BYTE_ORDER == BIG_ENDIAN
#define ARCH_BIG
#endif

#ifdef __QNX__
#define NO_VARIADIC_MACROS
#endif

#undef INCLUDE_MBROLA
#undef USE_NANOSLEEP

#define PATHSEP '/'
#define N_PATH_HOME  230

// used in synthesize.h and voice.h	
#define N_PEAKS   9
#define N_PEAKS2  9 // plus Notch and Fill (not yet implemented)

#ifndef DATA_FROM_SOURCECODE_FILES
	#define DATA_FROM_SOURCECODE_FILES  1
#endif
#if DATA_FROM_SOURCECODE_FILES
	#include "espeak_io.h"
#else
	#define PATH_ESPEAK_DATA  "/usr/share/espeak-ng-data"
	extern ESPEAK_NG_API int GetFileLength(const char *filename);
#endif
	
typedef unsigned short USHORT;
typedef unsigned char UCHAR;
typedef double DOUBLEX;

typedef struct {
	const char *mnem;
	int value;
} MNEM_TAB;
int LookupMnem(MNEM_TAB *table, const char *string);
const char *LookupMnemName(MNEM_TAB *table, const int value);

void cancel_audio(void);

extern char path_home[N_PATH_HOME];    // this is the espeak-ng-data directory

extern ESPEAK_NG_API void strncpy0(char *to, const char *from, int size);

// Parselmouth: See speech.cpp
#include <wctype.h>
#include "ucd.h"
#define iswalnum(c) ucd::isalnum(c)
#define iswalpha(c) ucd::isalpha(c)
#define iswblank(c) ucd::isblank(c)
#define iswcntrl(c) ucd::iscntrl(c)
#define iswdigit(c) ucd::isdigit(c)
#define iswgraph(c) ucd::isgraph(c)
#define iswlower(c) ucd::islower(c)
#define iswprint(c) ucd::isprint(c)
#define iswpunct(c) ucd::ispunct(c)
#define iswspace(c) ucd::isspace(c)
#define iswupper(c) ucd::isupper(c)
#define iswxdigit(c) ucd::isxdigit(c)

#endif // SPEECH_H
