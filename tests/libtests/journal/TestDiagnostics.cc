#include "catch2/catch_test_macros.hpp"


#include "pythia/journal/diagnostics.h" // USES journal diagnostics

// ------------------------------------------------------------------------------------------------
namespace pythia {
    namespace journal {
        class TestDiagnostics;
    } // journal
} // pythia

class pythia::journal::TestDiagnostics {
    // PUBLIC METHODS /////////////////////////////////////////////////////////////////////////////
public:

    static
    void testInfo(void);

    static
    void testDebug(void);

    static
    void testWarning(void);

    static
    void testError(void);

    static
    void testFirewall(void);

    static
    void testLocator(void);

}; // TestDiagnostics


// ------------------------------------------------------------------------------------------------
TEST_CASE("TestDiagnostics::testInfo", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testInfo();
}
TEST_CASE("TestDiagnostics::testDebug", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testDebug();
}
TEST_CASE("TestDiagnostics::testWarning", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testWarning();
}
TEST_CASE("TestDiagnostics::testError", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testError();
}
TEST_CASE("TestDiagnostics::testFirewall", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testFirewall();
}
TEST_CASE("TestDiagnostics::testLocator", "[TestDiagnostics]") {
    pythia::journal::TestDiagnostics::testLocator();
}

// ------------------------------------------------------------------------------------------------


void
pythia::journal::TestDiagnostics::testInfo(void) {
    pythia::journal::info_t info("my_info");

    CHECK(!info.state());

    info.activate();
    CHECK(info.state());
    info << journal::at(__HERE__)
         << "Info output" << journal::endl;

    info.deactivate();
    CHECK(!info.state());
    info << journal::at(__HERE__)
         << "No info output" << journal::endl;
}


// ------------------------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testDebug(void) {
    pythia::journal::debug_t debug("my_debug");

    CHECK(!debug.state());

    debug.activate();
    CHECK(debug.state());
    debug << journal::at(__HERE__)
          << "Debug output" << journal::endl;

    debug.deactivate();
    CHECK(!debug.state());
    debug << journal::at(__HERE__)
          << "No debug output" << journal::endl;
}


// ------------------------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testWarning(void) {
    pythia::journal::warning_t warning("my_warning");

    CHECK(warning.state());

    warning << journal::at(__HERE__)
            << "Warning output" << journal::endl;

    warning.deactivate();
    CHECK(!warning.state());
    warning << journal::at(__HERE__)
            << "No warning output" << journal::endl;

    warning.activate();
    CHECK(warning.state());
}


// ------------------------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testError(void) {
    pythia::journal::error_t error("my_error");

    CHECK(error.state());

    error << journal::at(__HERE__)
          << "Error output" << journal::endl;

    error.deactivate();
    CHECK(!error.state());
    error << journal::at(__HERE__)
          << "No error output" << journal::endl;

    error.activate();
    CHECK(error.state());
}


// ------------------------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testFirewall(void) {
    pythia::journal::firewall_t firewall("my_firewall");

    CHECK(firewall.state());

    firewall.deactivate();
    CHECK(!firewall.state());
    firewall << journal::at(__HERE__)
             << "No firewall output" << journal::endl;

    firewall.activate();
    CHECK(firewall.state());
}


// ------------------------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testLocator(void) {
    std::ostringstream msg;
    msg << pythia::journal::at(__HERE__);
    const std::string& here = msg.str();
    CHECK(here.find("TestDiagnostics.cc:") < here.length());
    CHECK(here.find(":159") < here.length());
}


// End of file
