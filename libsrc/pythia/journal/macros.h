/*
 * -*- C -*-
 * 
 *  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 *                              Michael A.G. Aivazis
 *                       California Institute of Technology
 *                       (C) 1998-2005  All Rights Reserved
 * 
 *  <LicenseText>
 * 
 *  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * 
 */

#if !defined(pythia_journal_macros_h)
#define pythia_journal_macros_h


/*
 * __HERE__ has to be a preprocessor macro
 */

#undef __FUNCTION__
#if defined(__FUNCTION_NAME__)
#define __FUNCTION__ __FUNCTION_NAME__
#else
#if defined(__func__)
#define __FUNCTION__ __func__
#endif
#endif

#if defined(__FUNCTION__)
#define __HERE__ __FILE__,__LINE__,__FUNCTION__
#define __HERE_ARGS__ filename, lineno, funcname
#define __HERE_DECL__ const char * filename, long lineno, const char * funcname
#else
#define __HERE__ __FILE__,__LINE__
#define __HERE_ARGS__ filename, lineno
#define __HERE_DECL__ const char * filename, long lineno
#endif

#endif

/* version
 * $Id: macros.h,v 1.1.1.1 2005/03/08 16:13:55 aivazis Exp $
 */

/* End of file */

