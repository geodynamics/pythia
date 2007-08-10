#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components import Component


# This is defined here as a do-nothing function because we can't import
# opal.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s


class WebSite(Component):


    name = "opal"


    import pyre.inventory as pyre


    ####################
    # CORE             #
    ####################

    DEBUG = pyre.bool("debug", default=False)
    TEMPLATE_DEBUG = pyre.bool("template-debug", default=False)

    USE_ETAGS = pyre.bool("use-etags", default=False)
    USE_ETAGS.meta['tip'] = """Whether to use the "Etag" header. This saves bandwidth but slows down performance."""

    ADMINS = pyre.list("admins")
    ADMINS.meta['tip'] = """People who get code error notifications."""

    INTERNAL_IPS = pyre.list("internal-ips")
    INTERNAL_IPS.meta['tip'] = """IP addresses that see debug comments (when 'debug' is true) and receive x-headers"""

    TIME_ZONE = pyre.str("time-zone", default="America/Chicago")
    TIME_ZONE.meta['tip'] = """Local time zone for this installation."""

    LANGUAGE_CODE = pyre.str("language-code", default="en-us")
    LANGUAGE_CODE.meta['tip'] = """Language code for this installation."""

    # Languages we provide translations for, out of the box. The language name
    # should be the utf-8 encoded local name for the language.
    LANGUAGES = (
        ('ar', gettext_noop('Arabic')),
        ('bn', gettext_noop('Bengali')),
        ('ca', gettext_noop('Catalan')),
        ('cs', gettext_noop('Czech')),
        ('cy', gettext_noop('Welsh')),
        ('da', gettext_noop('Danish')),
        ('de', gettext_noop('German')),
        ('el', gettext_noop('Greek')),
        ('en', gettext_noop('English')),
        ('es', gettext_noop('Spanish')),
        ('es_AR', gettext_noop('Argentinean Spanish')),
        ('fi', gettext_noop('Finnish')),
        ('fr', gettext_noop('French')),
        ('gl', gettext_noop('Galician')),
        ('hu', gettext_noop('Hungarian')),
        ('he', gettext_noop('Hebrew')),
        ('is', gettext_noop('Icelandic')),
        ('it', gettext_noop('Italian')),
        ('ja', gettext_noop('Japanese')),
        ('kn', gettext_noop('Kannada')),
        ('lv', gettext_noop('Latvian')),
        ('mk', gettext_noop('Macedonian')),
        ('nl', gettext_noop('Dutch')),
        ('no', gettext_noop('Norwegian')),
        ('pl', gettext_noop('Polish')),
        ('pt', gettext_noop('Portugese')),
        ('pt-br', gettext_noop('Brazilian')),
        ('ro', gettext_noop('Romanian')),
        ('ru', gettext_noop('Russian')),
        ('sk', gettext_noop('Slovak')),
        ('sl', gettext_noop('Slovenian')),
        ('sr', gettext_noop('Serbian')),
        ('sv', gettext_noop('Swedish')),
        ('ta', gettext_noop('Tamil')),
        ('te', gettext_noop('Telugu')),
        ('tr', gettext_noop('Turkish')),
        ('uk', gettext_noop('Ukrainian')),
        ('zh-cn', gettext_noop('Simplified Chinese')),
        ('zh-tw', gettext_noop('Traditional Chinese')),
    )

    # Languages using BiDi (right-to-left) layout
    LANGUAGES_BIDI = ("he", "ar")

    USE_I18N = pyre.bool("use-I18N", default=True)
    USE_I18N.meta['tip'] = """If you set this to False, Opal will make some optimizations so as not to load the internationalization machinery."""

    MANAGERS = pyre.list("managers")
    MANAGERS.meta['tip'] = """Not-necessarily-technical managers of the site. They get broken link notifications and other various e-mails."""

    DEFAULT_CONTENT_TYPE = pyre.str("default-content-type", default="text/html")
    DEFAULT_CONTENT_TYPE.meta['tip'] = """Default content type to use for all HttpResponse objects, if a MIME type isn't manually specified. Used to construct the Content-Type header."""
    
    DEFAULT_CHARSET = pyre.str("default-charset", default="utf-8")
    DEFAULT_CHARSET.meta['tip'] = """Default charset to use for all HttpResponse objects, if a MIME type isn't manually specified. Used to construct the Content-Type header."""

    SERVER_EMAIL = pyre.str("server-email", default="root@localhost")
    SERVER_EMAIL.meta['tip'] = """E-mail address that error messages come from."""

    SEND_BROKEN_LINK_EMAILS = pyre.bool("send-broken-link-emails", default=False)
    SEND_BROKEN_LINK_EMAILS.meta['tip'] = """Whether to send broken-link e-mails."""

    # Database connection info.
    ### Perhaps this should be a facility.
    DATABASE_ENGINE    = pyre.str("database-engine",
                                  validator=pyre.choice(['postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3', 'ado_mssql']))
    DATABASE_NAME      = pyre.str("database-name")        # Or path to database file if using sqlite3.
    DATABASE_USER      = pyre.str("database-user")        # Not used with sqlite3.
    DATABASE_PASSWORD  = pyre.str("database-password")    # Not used with sqlite3.
    DATABASE_HOST      = pyre.str("database-host")        # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT      = pyre.str("database-port")        # Set to empty string for default. Not used with sqlite3.
    DATABASE_OPTIONS   = {}                               # Set to empty dictionary for default.

    EMAIL_HOST = pyre.str("email-host", default="localhost")
    EMAIL_HOST.meta['tip'] = """Host for sending e-mail."""

    EMAIL_PORT = pyre.int("email-port", default=25)
    EMAIL_PORT.meta['tip'] = """Port for sending e-mail."""

    EMAIL_HOST_USER = pyre.str("email-host-user")
    EMAIL_HOST_USER.meta['tip'] = """Optional SMTP authentication information for 'email-host'."""
    
    EMAIL_HOST_PASSWORD = pyre.str("email-host-password")
    EMAIL_HOST_PASSWORD.meta['tip'] = """Optional SMTP authentication information for 'email-host'."""

    ### This should be done with egg metadata.
    INSTALLED_APPS = pyre.list("installed-apps")
    INSTALLED_APPS.meta['tip'] = """List of strings representing installed apps."""

    TEMPLATE_DIRS = pyre.list("template-dirs")
    TEMPLATE_DIRS.meta['tip'] = """List of locations of the template source files, in search order."""

    ### This should be done with egg metadata.
    TEMPLATE_LOADERS = pyre.list("template-loaders", default=[
        'opal.template.loaders.filesystem.load_template_source',
        'opal.template.loaders.app_directories.load_template_source',
        #'opal.template.loaders.eggs.load_template_source',
        ])
    TEMPLATE_LOADERS.meta['tip'] = """List of callables that know how to import templates from various sources. See the comments in opal/core/template/loader.py for interface documentation."""

    ### This should be done with egg metadata.
    TEMPLATE_CONTEXT_PROCESSORS = pyre.list("template-context-processors", default=[
        'opal.core.context_processors.auth',
        'opal.core.context_processors.debug',
        'opal.core.context_processors.i18n',
        #'opal.core.context_processors.request',
        ])
    TEMPLATE_CONTEXT_PROCESSORS.meta['tip'] = """List of processors used by RequestContext to populate the context. Each one should be a callable that takes the request object as its only parameter and returns a dictionary to add to the context."""

    TEMPLATE_STRING_IF_INVALID = pyre.str("template-string-if-invalid")
    TEMPLATE_STRING_IF_INVALID.meta['tip'] = """Output to use in template system for invalid (e.g. misspelled) variables."""

    ADMIN_MEDIA_PREFIX = pyre.str("admin-media-prefix", default="/media/")
    ADMIN_MEDIA_PREFIX.meta['tip'] = """URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash. Examples: "http://foo.com/media/", "/media/"."""

    DEFAULT_FROM_EMAIL = pyre.str("default-from-email", default="webmaster@localhost")
    DEFAULT_FROM_EMAIL.meta['tip'] = """Default e-mail address to use for various automated correspondence from the site managers."""

    EMAIL_SUBJECT_PREFIX = pyre.str("email-subject-prefix", default="[Opal] ")
    EMAIL_SUBJECT_PREFIX.meta['tip'] = """Subject-line prefix for email messages send with opal.core.mail.mail_admins or ...mail_managers.  Make sure to include the trailing space."""

    ### I hate this one.  It should depend upon the object being accessed.
    APPEND_SLASH = pyre.bool("append-slash", default=True)
    APPEND_SLASH.meta['tip'] = """Whether to append trailing slashes to URLs."""

    PREPEND_WWW = pyre.bool("prepend-www", default=False)
    PREPEND_WWW.meta['tip'] = """Whether to prepend the "www." subdomain to URLs that don't have it."""

    # List of compiled regular expression objects representing User-Agent strings
    # that are not allowed to visit any page, systemwide. Use this for bad
    # robots/crawlers. Here are a few examples:
    #     import re
    #     DISALLOWED_USER_AGENTS = (
    #         re.compile(r'^NaverBot.*'),
    #         re.compile(r'^EmailSiphon.*'),
    #         re.compile(r'^SiteSucker.*'),
    #         re.compile(r'^sohu-search')
    #     )
    DISALLOWED_USER_AGENTS = ()

    ABSOLUTE_URL_OVERRIDES = {}

    ALLOWED_INCLUDE_ROOTS = pyre.list("allowed-include-roots")
    ALLOWED_INCLUDE_ROOTS.meta['tip'] = """List of strings representing allowed prefixes for the {% ssi %} tag. Example: ['/home/html', '/var/www']"""

    ADMIN_FOR = pyre.list("admin-for")
    ADMIN_FOR.meta['tip'] = """If this is a admin settings module, this should be a list of settings modules (in the format 'foo.bar.baz') for which this admin is an admin."""

    IGNORABLE_404_STARTS = pyre.list("ignorable-404-starts", default=['/cgi-bin/', '/_vti_bin', '/_vti_inf'])
    IGNORABLE_404_STARTS.meta['tip'] = """404s that may be ignored."""
    
    IGNORABLE_404_ENDS = pyre.list("ignorable-404-ends", default=['mail.pl', 'mailform.pl', 'mail.cgi', 'mailform.cgi', 'favicon.ico', '.php'])
    IGNORABLE_404_ENDS.meta['tip'] = """404s that may be ignored."""

    SECRET_KEY = pyre.str("secret-key")
    SECRET_KEY.meta['tip'] = """A secret key for this particular Opal installation. Used in secret-key hashing algorithms. Set this in your settings, or Opal will complain loudly."""

    JING_PATH = pyre.str("jing-path", default="/usr/bin/jing")
    JING_PATH.meta['tip'] = """Path to the "jing" executable -- needed to validate XMLFields."""

    MEDIA_ROOT = pyre.str("media-root")
    MEDIA_ROOT.meta['tip'] = """Absolute path to the directory that holds media. Example: "/home/media/media.lawrence.com/"."""

    MEDIA_URL = pyre.str("media-url")
    MEDIA_URL.meta['tip'] = """URL that handles the media served from 'media-root'. Example: "http://media.lawrence.com"."""

    DATE_FORMAT = pyre.str("date-format", default="N j, Y")
    DATE_FORMAT.meta['tip'] = """Default formatting for date objects. See all available format strings here: http://www.djangoproject.com/documentation/templates/#now"""

    DATETIME_FORMAT = pyre.str("datetime-format", default="N j, Y, P")
    DATETIME_FORMAT.meta['tip'] = """Default formatting for datetime objects. See all available format strings here: http://www.djangoproject.com/documentation/templates/#now"""

    TIME_FORMAT = pyre.str("time-format", default="P")
    TIME_FORMAT.meta['tip'] = """Default formatting for time objects. See all available format strings here: http://www.djangoproject.com/documentation/templates/#now"""

    YEAR_MONTH_FORMAT = pyre.str("year-month-format", default="F Y")
    YEAR_MONTH_FORMAT.meta['tip'] = """Default formatting for date objects when only the year and month are relevant. See all available format strings here: http://www.djangoproject.com/documentation/templates/#now"""

    MONTH_DAY_FORMAT = pyre.str("month-day-format", default="F j")
    MONTH_DAY_FORMAT.meta['tip'] = """Default formatting for date objects when only the month and day are relevant. See all available format strings here: http://www.djangoproject.com/documentation/templates/#now"""

    TRANSACTIONS_MANAGED = pyre.bool("transactions-managed", default=False)
    TRANSACTIONS_MANAGED.meta['tip'] = """Do you want to manage transactions manually? Hint: you really don't!"""
    
    URL_VALIDATOR_USER_AGENT = pyre.str("url-validator-user-agent", default="Django/0.96pre (http://www.djangoproject.com)")
    URL_VALIDATOR_USER_AGENT.meta['tip'] = """The User-Agent string to use when checking for URL validity through the isExistingURL validator."""


    ##############
    # MIDDLEWARE #
    ##############

    MIDDLEWARE_CLASSES = pyre.list("middleware-classes", default=[
        'opal.contrib.sessions.middleware.SessionMiddleware',
        'opal.contrib.auth.middleware.AuthenticationMiddleware',
        #'opal.middleware.http.ConditionalGetMiddleware',
        #'opal.middleware.gzip.GZipMiddleware',
        'opal.middleware.common.CommonMiddleware',
        'opal.middleware.doc.XViewMiddleware',
    ])
    MIDDLEWARE_CLASSES.meta['tip'] = """List of middleware classes to use. Order is important; in the request phase, this middleware classes will be applied in the order given, and in the response phase the middleware will be applied in reverse order."""


    ############
    # SESSIONS #
    ############

    SESSION_COOKIE_NAME = pyre.str("session-cookie-name", default="sessionid")
    SESSION_COOKIE_NAME.meta['tip'] = """Cookie name. This can be whatever you want."""

    from pyre.units.time import day
    session_cookie_age = pyre.dimensional("session-cookie-age", default=(14 * day))
    session_cookie_age.meta['tip'] = """Age of cookie (default: 2 weeks)."""
    
    session_cookie_domain = pyre.str("session-cookie-domain")
    session_cookie_domain.meta['tip'] = """A string like ".lawrence.com". Leave blank for standard domain cookie."""

    SESSION_COOKIE_SECURE = pyre.bool("session-cookie-secure", default=False)
    SESSION_COOKIE_SECURE.meta['tip'] = """Whether the session cookie should be secure (https:// only)."""
    
    SESSION_SAVE_EVERY_REQUEST = pyre.bool("session-save-every-request", default=False)
    SESSION_SAVE_EVERY_REQUEST.meta['tip'] = """Whether to save the session data on every request."""
    
    SESSION_EXPIRE_AT_BROWSER_CLOSE = pyre.bool("session-expire-at-browser-close", default=False)
    SESSION_EXPIRE_AT_BROWSER_CLOSE.meta['tip'] = """Whether sessions expire when a user closes his browser."""


    #########
    # CACHE #
    #########

    CACHE_BACKEND = pyre.str("cache-backend", default="simple://")
    CACHE_BACKEND.meta['tip'] = """The cache backend to use.  See the docstring in opal.core.cache for the possible values."""
    
    CACHE_MIDDLEWARE_KEY_PREFIX = pyre.str("cache-middleware-key-prefix")


    ####################
    # COMMENTS         #
    ####################

    COMMENTS_ALLOW_PROFANITIES = pyre.bool("comments-allow-profanities", default=False)

    PROFANITIES_LIST = pyre.list("profanities-list", default=['asshat', 'asshead', 'asshole', 'cunt', 'fuck', 'gook', 'nigger', 'shit'])
    PROFANITIES_LIST.meta['tip'] = """The profanities that will trigger a validation error in the 'hasNoProfanities' validator. All of these should be in lowercase."""

    # The group ID that designates which users are banned.
    # Set to None if you're not using it.
    COMMENTS_BANNED_USERS_GROUP = None

    # The group ID that designates which users can moderate comments.
    # Set to None if you're not using it.
    COMMENTS_MODERATORS_GROUP = None

    # The group ID that designates the users whose comments should be e-mailed to MANAGERS.
    # Set to None if you're not using it.
    COMMENTS_SKETCHY_USERS_GROUP = None

    COMMENTS_FIRST_FEW = pyre.int("comments-first-few", default=0)
    COMMENTS_FIRST_FEW.meta['tip'] = """The system will e-mail 'managers' the first 'comments-first-few' comments by each user. Set this to 0 if you want to disable it."""

    BANNED_IPS = pyre.list("banned-ips")
    BANNED_IPS.meta['tip'] = """A tuple of IP addresses that have been banned from participating in various Opal-powered features."""


    ##################
    # AUTHENTICATION #
    ##################

    AUTHENTICATION_BACKENDS = pyre.list("authentication-backends", default=[
        'opal.contrib.auth.backends.ModelBackend',
        ])


    ###########
    # TESTING #
    ###########

    TEST_RUNNER = pyre.str("test-runner", default='opal.test.simple.run_tests')
    TEST_RUNNER.meta['tip'] = """The name of the method to use to invoke the test suite"""

    TEST_DATABASE_NAME = pyre.str("test-database-name")
    TEST_DATABASE_NAME.meta['tip'] = """The name of the database to use for testing purposes. If empty, a name of 'test_' + DATABASE_NAME will be assumed"""


    ############
    # FIXTURES #
    ############

    FIXTURE_DIRS = pyre.list("fixture-dirs")
    FIXTURE_DIRS.meta['tip'] = """The list of directories to search for fixtures"""


    #########
    # ????? #
    #########

    SITE_ID = pyre.int("site-id", default=1)
    #rootUrlconf = pyre.str("root-urlconf", default=None)
    rootUrlconf = pyre.facility("root", default=None)


    def _configure(self):
        super(WebSite, self)._configure()

        if False and self.rootUrlconf is None:
            raise ValueError("root-urlconf is not set")
        
        # convert to seconds
        from pyre.units.time import second
        self.SESSION_COOKIE_AGE = self.session_cookie_age / second

        self.SESSION_COOKIE_DOMAIN = None
        if self.session_cookie_domain != "":
            self.SESSION_COOKIE_DOMAIN = self.session_cookie_domain

        return


    def _init(self):
        super(WebSite, self)._init()

        self.ROOT_URLCONF = None
        
        return


    ##########


    def urlResolver(self):
        from merlin import loadObject
        from opal.core import urlresolvers

        if self.ROOT_URLCONF is None:
            self.ROOT_URLCONF = self.rootUrlconf
        return urlresolvers.RegexURLResolver(r'^/', self.ROOT_URLCONF)


# end of file
