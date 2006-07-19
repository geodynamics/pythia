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

#if !defined(journal_Diagnostic_h)
#define journal_Diagnostic_h


// forward declarations
namespace journal {
    class Entry;
    class Facility;
    class Journal;
    class Diagnostic;
}


class journal::Diagnostic {

// types
public:
    typedef Entry entry_t;
    typedef Facility state_t;
    typedef Journal journal_t;

    typedef std::string string_t;
    typedef std::stringstream buffer_t;

// interface
public:
    void state(bool);
    bool state() const;
    
    void activate() { state(true); }
    void deactivate() { state(false); }

    string_t facility() const { return _facility; }

    // entry manipulation
    void record();
    void newline();
    void attribute(string_t, string_t);

    // access to the buffered data
    string_t str() const { return _buffer.str(); }

    // access to the journal singleton
    static journal_t & journal();

    // builtin data type injection
    template <typename item_t> 
    Diagnostic & inject(item_t datum) {
        _buffer << item;
        return *this;
    }

// meta-methods
public:
    ~Diagnostic();
    Diagnostic(string_t, string_t, state_t &);

// implementation
private:
    void _newline();

// disable these
private:
    Diagnostic(const Diagnostic &);
    const Diagnostic & operator=(const Diagnostic &);

// data
private:
    const string_t _facility;
    const string_t _severity;

    state_t & _state;
    buffer_t _buffer;
    entry_t * _entry;
};


// the injection operator
template <typename item_t>
journal::Diagnostic & operator<< (journal::Diagnostic & diagnostic, item_t item) {
    return diagnostic.inject(item);
}


#endif

// version
// $Id: Diagnostic.h,v 1.1.1.1 2005/03/08 16:13:56 aivazis Exp $

// End of file 
