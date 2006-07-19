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
    typedef bool state_t;
    typedef Journal journal_t;

    typedef std::string string_t;
    typedef std::stringstream buffer_t;

// interface
public:
    void state(bool flag) { _state = flag; }
    bool state() const { return _state; }
    static state_t & lookup(string_t name) { static state_t dummy; return dummy; }
    
    void activate() { state(true); }
    void deactivate() { state(false); }

    string_t facility() const { return _facility; }

    // entry manipulation
    void record() { /**/ }
    void newline() { if (state()) _newline(); }
    void attribute(string_t key, string_t value) {
        /*(*_entry)[key] = value;*/
    }

    // access to the buffered data
    string_t str() const { return _buffer.str(); }

    // access to the journal singleton
    static journal_t & journal();

    // builtin data type injection
    template <typename item_t> 
    Diagnostic & inject(item_t item) {
        _buffer << item;
        return *this;
    }

// meta-methods
public:
    ~Diagnostic() { /*delete _entry;*/ }
    Diagnostic(string_t facility, string_t severity, state_t & state):
        _facility(facility), _severity(severity),
        _state(state), _buffer(), _entry(0 /*new entry_t*/) {}

// implementation
private:
    void _newline() {
        /*_entry->newline(str());*/
        _buffer.str(string_t());
    }

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
inline journal::Diagnostic & operator<< (journal::Diagnostic & diagnostic, item_t item) {
    return diagnostic.inject(item);
}


#endif

// version
// $Id: Diagnostic.h,v 1.1.1.1 2005/03/08 16:13:56 aivazis Exp $

// End of file 
