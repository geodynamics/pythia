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

#if !defined(journal_SeverityInfo_h)
#define journal_SeverityInfo_h


// forward declarations
namespace journal {
    class Diagnostic;
    class SeverityInfo;
    class Index;
}


class journal::SeverityInfo : public journal::Diagnostic {

// types
public:
    typedef Index index_t;

// interface
public:
    string_t name() const { return  "info." + facility(); }
    static state_t & lookup(string_t);

// meta-methods
public:
    virtual ~SeverityInfo();
    
    SeverityInfo(string_t name) :
        Diagnostic(name, "info", lookup(name)) {}

// disable these
private:
    SeverityInfo(const SeverityInfo &);
    const SeverityInfo & operator=(const SeverityInfo &);

// data
private:
    static index_t * _index;
};


#endif
// version
// $Id: SeverityInfo.h,v 1.1.1.1 2005/03/08 16:13:55 aivazis Exp $

// End of file 
