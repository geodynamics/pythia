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

#if !defined(pythia_journal_SeverityWarning_h)
#define pythia_journal_SeverityWarning_h


// forward declarations
namespace pythia {
    namespace journal {
        class Diagnostic;
        class SeverityWarning;
    }
}


class pythia::journal::SeverityWarning : public pythia::journal::Diagnostic {

// interface
public:
    string_t name() const { return  "warning." + facility(); }

// meta-methods
public:
    ~SeverityWarning() {}
    
    SeverityWarning(string_t name) :
        Diagnostic(name, "warning") {}

// disable these
private:
    SeverityWarning(const SeverityWarning &);
    const SeverityWarning & operator=(const SeverityWarning &);
};


#endif
// version
// $Id: SeverityWarning.h,v 1.1.1.1 2005/03/08 16:13:56 aivazis Exp $

// End of file 
