#include <cppunit/extensions/HelperMacros.h>

#include "pythia/journal/diagnostics.h" // USES journal diagnostics

// ----------------------------------------------------------------------
namespace pythia {
    namespace journal {
        class TestDiagnostics;
    } // journal
} // pythia

class pythia::journal::TestDiagnostics : public CppUnit::TestFixture {
    // CPPUNIT TEST SUITE /////////////////////////////////////////////////
    CPPUNIT_TEST_SUITE(TestDiagnostics);

    CPPUNIT_TEST(testInfo);
    CPPUNIT_TEST(testDebug);
    CPPUNIT_TEST(testWarning);
    CPPUNIT_TEST(testError);
    CPPUNIT_TEST(testFirewall);

    CPPUNIT_TEST_SUITE_END();

    // PUBLIC METHODS /////////////////////////////////////////////////////
public:

    void testInfo(void);

    void testDebug(void);

    void testWarning(void);

    void testError(void);

    void testFirewall(void);

}; // TestDiagnostics

CPPUNIT_TEST_SUITE_REGISTRATION(pythia::journal::TestDiagnostics);

// ---------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testInfo(void) {
    pythia::journal::info_t info("my_info");

    CPPUNIT_ASSERT_MESSAGE("Expected false default state.", !info.state());

    info.activate();
    CPPUNIT_ASSERT_MESSAGE("Expected activated state.", info.state());
    info << journal::at(__HERE__)
         << "Info output" << journal::endl;

    info.deactivate();
    CPPUNIT_ASSERT_MESSAGE("Expected deactivated state.", !info.state());
    info << journal::at(__HERE__)
         << "No info output" << journal::endl;
}


// ---------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testDebug(void) {
    pythia::journal::debug_t debug("my_debug");

    CPPUNIT_ASSERT_MESSAGE("Expected false default state.", !debug.state());

    debug.activate();
    CPPUNIT_ASSERT_MESSAGE("Expected activated state.", debug.state());
    debug << journal::at(__HERE__)
          << "Debug output" << journal::endl;

    debug.deactivate();
    CPPUNIT_ASSERT_MESSAGE("Expected deactivated state.", !debug.state());
    debug << journal::at(__HERE__)
          << "No debug output" << journal::endl;
}


// ---------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testWarning(void) {
    pythia::journal::warning_t warning("my_warning");

    CPPUNIT_ASSERT_MESSAGE("Expected true default state.", warning.state());

    warning << journal::at(__HERE__)
            << "Warning output" << journal::endl;

    warning.deactivate();
    CPPUNIT_ASSERT_MESSAGE("Expected deactivated state.", !warning.state());
    warning << journal::at(__HERE__)
            << "No warning output" << journal::endl;

    warning.activate();
    CPPUNIT_ASSERT_MESSAGE("Expected activated state.", warning.state());
}


// ---------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testError(void) {
    pythia::journal::error_t error("my_error");

    CPPUNIT_ASSERT_MESSAGE("Expected true default state.", error.state());

    error << journal::at(__HERE__)
          << "Error output" << journal::endl;

    error.deactivate();
    CPPUNIT_ASSERT_MESSAGE("Expected deactivated state.", !error.state());
    error << journal::at(__HERE__)
          << "No error output" << journal::endl;

    error.activate();
    CPPUNIT_ASSERT_MESSAGE("Expected activated state.", error.state());
}


// ---------------------------------------------------------------------------------
void
pythia::journal::TestDiagnostics::testFirewall(void) {
    pythia::journal::firewall_t firewall("my_firewall");

    CPPUNIT_ASSERT_MESSAGE("Expected true default state.", firewall.state());

    firewall.deactivate();
    CPPUNIT_ASSERT_MESSAGE("Expected deactivated state.", !firewall.state());
    firewall << journal::at(__HERE__)
             << "No firewall output" << journal::endl;

    firewall.activate();
    CPPUNIT_ASSERT_MESSAGE("Expected activated state.", firewall.state());
}


// End of file
