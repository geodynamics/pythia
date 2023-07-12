#include <portinfo>

#include "catch2/catch_session.hpp"

#include <Python.h>

namespace pythia {
    class TestDriver;
}

// ------------------------------------------------------------------------------------------------
class pythia::TestDriver {
public:

    enum JournalEnum {
        JOURNAL_INFO=0,
        JOURNAL_DEBUG=1,
    };

    typedef std::vector< std::pair<JournalEnum,std::string> > journals_t;

    // PUBLIC METHODS /////////////////////////////////////////////////////////////////////////////
public:

    /// Constructor.
    TestDriver(void);

    /** Run test application.
     * @param argc[in] Number of arguments passed.
     * @param argv[in] Array of input arguments.
     *
     * @returns 1 if errors were detected, 0 otherwise.
     */
    int run(int argc,
            char* argv[]);

    // NOT IMPLEMENTED ////////////////////////////////////////////////////////////////////////////
private:

    TestDriver(const TestDriver&); ///< Not implemented
    const TestDriver& operator=(const TestDriver&); ///< Not implemented

};

// ------------------------------------------------------------------------------------------------
// Constructor
pythia::TestDriver::TestDriver(void) { }


// ---------------------------------------------------------------------------------------------------------------------
// Run info application.
int
pythia::TestDriver::run(int argc,
                                 char* argv[]) {
    Catch::Session session;

    auto cli = session.cli();
    session.cli(cli);
    int returnCode = session.applyCommandLine(argc, argv);
    if (returnCode) {
        return returnCode;
    } // if

    // Initialize Python (needed for journals).
    Py_Initialize();

    int result = session.run();

    // Finalize Python
    Py_Finalize();

    return result;
} // run


// ------------------------------------------------------------------------------------------------
int
main(int argc,
     char* argv[]) {
    return pythia::TestDriver().run(argc, argv);
} // main


// End of file
