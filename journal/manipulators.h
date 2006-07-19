// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Michael A.G. Aivazis
//                      California Institute of Technology
//                      (C) 1998-2005  All Rights Reserved
//
// <LicenseText>
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#if !defined(journal_manipulators_h)
#define journal_manipulators_h

// get infrastructure manipulator definitions/declaration
#if defined(JOURNAL_NON_TEMPLATED_MANIPULATORS)
#include "manip-explicit.h"
#else
#include "manip-templated.h"
#endif

// forward declarations
namespace journal {
    class Diagnostic;

    // end of entry
    inline Diagnostic & endl(Diagnostic & diag) {
        diag.record();
        return diag;
    }
    
    // add a newline
    inline Diagnostic & newline(Diagnostic & diag) {
        diag.newline();
        return diag;
    }

    // set metadata key to value
    inline Diagnostic & __diagmanip_set(Diagnostic & s, const char * key, const char * value) {
        s.attribute(key, value);
        return s;
    }

    inline set_t set(const char * key, const char * value) {
        return set_t(__diagmanip_set, key, value);
    }
    
    // location information
    inline Diagnostic & __diagmanip_loc(Diagnostic & s, const char * filename, long line) {
        s.attribute("filename", filename);

        std::stringstream tmp;
        tmp << line;

        s.attribute("line", tmp.str());

        return s;
    }

    inline loc2_t at(const char * file, long line) {
        return loc2_t(__diagmanip_loc, file, line);
    }

    inline Diagnostic & __diagmanip_loc(
        Diagnostic & s, const char * filename, long line, const char * function) 
    {
        s.attribute("filename", filename);
        s.attribute("function", function);

        std::stringstream tmp;
        tmp << line;

        s.attribute("line", tmp.str());

        return s;
    }

    inline loc3_t at(const char * file, long line, const char * function) {
        return loc3_t(__diagmanip_loc, file, line, function);
    }

}

inline journal::Diagnostic & 
operator<< (journal::Diagnostic & s, journal::Diagnostic & (m)(journal::Diagnostic &))
{
    return (*m)(s);
}


#endif

// version
// $Id: manipulators.h,v 1.1.1.1 2005/03/08 16:13:55 aivazis Exp $

// End of file 
