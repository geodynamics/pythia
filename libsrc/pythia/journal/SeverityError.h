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

#if !defined(pythia_journal_SeverityError_h)
#define pythia_journal_SeverityError_h


// forward declarations
namespace pythia {
    namespace journal {
        class Diagnostic;
        class SeverityError;
    }
}


class pythia::journal::SeverityError : public pythia::journal::Diagnostic {

// interface
public:
    string_t name() const { return  "error." + facility(); }

// meta-methods
public:
    ~SeverityError() {}
    
    SeverityError(string_t name) :
        Diagnostic(name, "error") {}

// disable these
private:
    SeverityError(const SeverityError &);
    const SeverityError & operator=(const SeverityError &);
};


#endif
// version
// $Id: SeverityError.h,v 1.1.1.1 2005/03/08 16:13:56 aivazis Exp $

// End of file 
