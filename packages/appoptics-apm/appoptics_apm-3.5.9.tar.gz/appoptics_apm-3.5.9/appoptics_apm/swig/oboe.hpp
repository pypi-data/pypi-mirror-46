/**
 * @file oboe.hpp - C++ liboboe wrapper primarily for generating SWIG interfaces
 *
 * This API should follow https://github.com/tracelytics/tracelons/wiki/Instrumentation-API
 */

#ifndef OBOE_HPP
#define OBOE_HPP

#include <string>
#include <oboe.h>


class Event;
class Reporter;
class Context;

/**
 * Metadata is the X-Trace identifier and the information needed to work with it.
 */
class Metadata : private oboe_metadata_t {
    friend class Reporter;
    friend class Context;

public:
    Metadata(oboe_metadata_t *md) {
        oboe_metadata_copy(this, md);
    }

    ~Metadata() {
        oboe_metadata_destroy(this);
    }

    static Metadata* fromString(std::string s) {
        oboe_metadata_t md;
        oboe_metadata_fromstr(&md, s.data(), s.size());
        return new Metadata(&md); // copies md
    }

    // these new objects are managed by SWIG %newobject
    Event *createEvent();

    static Metadata *makeRandom(bool sampled=true) {
        oboe_metadata_t md;
        oboe_metadata_init(&md);
        oboe_metadata_random(&md);

        if (sampled) {
            md.flags |= XTR_FLAGS_SAMPLED;
        }

        return new Metadata(&md); // copies md
    }

    Metadata *copy() {
        return new Metadata(this);
    }

    bool isValid() {
        return oboe_metadata_is_valid(this);
    }

    bool isSampled() {
        return oboe_metadata_is_sampled(this);
    }

#ifdef SWIGJAVA
    std::string toStr() {
#else
    std::string toString() {
#endif
        char buf[OBOE_MAX_METADATA_PACK_LEN]; // Flawfinder: ignore

        int rc = oboe_metadata_tostr(this, buf, sizeof(buf) - 1);
        if (rc == 0) {
            return std::string(buf);
        } else {
            return std::string(); // throw exception?
        }
    }

};

/**
 * The Context class manages the metadata and the settings configuration.
 *
 * The metadata includes the X-Trace identifier fields and the information work working with it.
 * The metadata is needed before any trace messages can be sent and must either be generated for
 * new traces or derived from the X-Trace header of an existing trace.
 *
 * The settings information is used primarily to determine when a new request should be traced.
 * The information begins with configuration values for tracing_mode and sample_rate and then
 * updates are received periodically from the collector to adjust the rate at which traces
 * are generated.
 */
class Context {
public:
    /**
     * Set the tracing mode.
     *
     * @param newMode One of
     * - OBOE_TRACE_DISABLED(0) to disable tracing,
     * - OBOE_TRACE_ENABLED(1) to start a new trace if needed, or
     * - OBOE_TRACE_THROUGH(2) to only add to an existing trace.
     */
    static void setTracingMode(int newMode) {
        oboe_settings_mode_set(newMode);
    }

    /**
     * Set the default sample rate.
     *
     * This rate is used until overridden by the AppOptics servers.  If not set then the
     * value comes from settings records downloaded from AppOptics.
     *
     * The rate is interpreted as a ratio out of OBOE_SAMPLE_RESOLUTION (currently 1,000,000).
     *
     * @param newRate A number between 0 (none) and OBOE_SAMPLE_RESOLUTION (a million)
     */
    static void setDefaultSampleRate(int newRate) {
        oboe_settings_rate_set(newRate);
    }

    /**
     * Ask the collector for the final tracing decisions
     *
     * call once per request
     *
     * when compiled via SWIG this function takes 1-4 arguments and returns 4 integers
     *
     * @param do_metrics, ignore when using SWIG, it will be mapped to the second return value
     * @param do_sample, ignore when using SWIG, it will be mapped to the first return value
     * @param sample_rate, ignore when using SWIG, it will be mapped to the third return value
     * @param sample_source, ignore when using SWIG, it will be mapped to the forth return value
     * @param in_xtrace(optional), a valid xtrace string
     * @param custom_sample_rate(optional), 0-1000000
     * @param custom_tracing_mode(optional), 0(disabled) or 1(enabled)
     * @param service_name(optional), only needed if there can be more than 1 service per process
     *
     * @return one of the following codes:
     *   OBOE_TRACING_DECISIONS_TRACING_DISABLED == -2
     *   OBOE_TRACING_DECISIONS_XTRACE_NOT_SAMPLED == -1
     *   OBOE_TRACING_DECISIONS_OK == 0
     *   OBOE_TRACING_DECISIONS_NULL_OUT == 1
     *   OBOE_TRACING_DECISIONS_NO_CONFIG == 2
     *   OBOE_TRACING_DECISIONS_REPORTER_NOT_READY == 3
     *   OBOE_TRACING_DECISIONS_NO_VALID_SETTINGS == 4
     */
    static void getDecisions(int *do_metrics, int *do_sample, int *sample_rate, int *sample_source, int *return_value,
                             std::string in_xtrace = "",
                             int custom_tracing_mode = OBOE_SETTINGS_UNSET,
                             int custom_sample_rate = OBOE_SETTINGS_UNSET,
                             std::string service_name = "")  {

        oboe_tracing_decisions_in_t tdi = {
                1, //version
                service_name.c_str(),
                in_xtrace.c_str(),
                custom_sample_rate,
                custom_tracing_mode
        };
        oboe_tracing_decisions_out_t tdo = {1, 0, 0, 0, 0}; // first field => version

        *return_value = oboe_tracing_decisions(&tdi, &tdo);
        
        *do_sample = tdo.do_sample;
        *do_metrics = tdo.do_metrics;
        *sample_rate = tdo.sample_rate;
        *sample_source = tdo.sample_source;
    }

    /**
     * Check if the current request should be traced based on the current settings.
     *
     * If in_xtrace is empty, or if it is identified as a foreign (ie. cross customer)
     * trace, then sampling will be considered as a new trace.
     * Otherwise sampling will be considered as adding to the current trace.
     * Different services may have special rules.
     *
     * This is designed to be called once per service per request.
     *
     *  @param service_name Name of the service being considered for tracing
     *                      if empty, the default service name will be used
     *  @param in_xtrace Incoming X-Trace ID (NULL or empty string if not present)
     *  @return Zero to not trace; otherwise return the sample rate used in the low order
     *          bytes 0 to 2 and the sample source in the higher-order byte 3.
     */
    static int sampleRequest(
        std::string service_name,
        std::string in_xtrace)
    {
        int sample_rate = 0;
        int sample_source = 0;
        int rc = (oboe_sample_layer(service_name.c_str(), in_xtrace.c_str(), &sample_rate, &sample_source));

        return (rc == 0 ? 0 : (((sample_source & 0xFF) << 24) | (sample_rate & 0xFFFFFF)));
    }

    /**
     * Get a pointer to the current context (from thread-local storage)
     */
    static oboe_metadata_t *get() {
        return oboe_context_get();
    }

    /**
     * Get the current context as a printable string.
     */
#ifdef SWIGJAVA
    static std::string toStr() {
#else
    static std::string toString() {
#endif
        char buf[OBOE_MAX_METADATA_PACK_LEN]; // Flawfinder: ignore

        oboe_metadata_t *md = Context::get();
        int rc = oboe_metadata_tostr(md, buf, sizeof(buf) - 1);
        if (rc == 0) {
            return std::string(buf);
        } else {
            return std::string(); // throw exception?
        }
    }

    /**
     * Set the current context (this updates thread-local storage).
     */
    static void set(oboe_metadata_t *md) {
        oboe_context_set(md);
    }

    /**
     * Set the current context from a string.
     */
    static void fromString(std::string s) {
        oboe_context_set_fromstr(s.data(), s.size());
    }

    // this new object is managed by SWIG %newobject
    static Metadata *copy() {
        return new Metadata(Context::get());
    }

    static void setSampledFlag() {
        oboe_metadata_t *md = Context::get();
        md->flags |= XTR_FLAGS_SAMPLED;
    }

    static void clear() {
        oboe_context_clear();
    }

    static bool isValid() {
        return oboe_context_is_valid();
    }

    static bool isSampled() {
        return oboe_context_is_sampled();
    }

    /**
     * Initialize the Oboe subsystems.
     *
     * This should be called before any other oboe_* functions.  However, in order
     * to make the library easier to work with, checks are in place so that it
     * will be called by any of the other functions that depend on it.
     *
     * Besides initializing the oboe library, this will also initialize a
     * reporter based on the values of environment variables, configuration
     * file options.  See the oboe_init_options struct definition in oboe.h
     * for details on the full set of options.
     *
     * @param access_key Client access key
     * @param hostname_alias An optional logical/readable hostname that can be used to easily identify the host
     * @param log_level Optional parameter to configure the log level for messages logged by oboe
     * @param max_flush_wait_time Optional parameter to configure maximum wait time for flushing data before terminating in milli seconds
     * @param events_flush_interval Optional parameter to configure how frequently events are flushed
     * @param events_flush_batch_size Optional parameter to configure the batch size before events are flushed
     */
    static void init(std::string access_key = "", std::string hostname_alias = "",
            int log_level = LOGLEVEL_DEFAULT,
            int max_flush_wait_time = DEFAULT_FLUSH_MAX_WAIT_TIME,
            int events_flush_interval = OBOE_DEFAULT_EVENTS_FLUSH_INTERVAL,
            int events_flush_batch_size = OBOE_DEFAULT_EVENTS_FLUSH_BATCH_SIZE) {
        oboe_init_options_t options;
        memset(&options, 0, sizeof(options));
        options.version = 4;
        options.log_level = log_level;
        options.hostname_alias = hostname_alias.c_str();
        options.max_flush_wait_time = max_flush_wait_time;
        options.events_flush_interval = events_flush_interval;
        options.events_flush_batch_size = events_flush_batch_size;

        oboe_init(access_key.c_str(), &options);
    }

    /**
     * Perform validation and replacement of invalid characters on the given service name.
     */
    static std::string validateTransformServiceName(std::string service_name) {
        char service_name_cpy[64+256]; // Flawfinder: ignore, key=64, colon=1, name<=255
        memset(service_name_cpy, 0, sizeof(service_name_cpy));
        strncpy(service_name_cpy, service_name.c_str(), sizeof(service_name_cpy) - 1); // Flawfinder: ignore
        int len = strlen(service_name_cpy); // Flawfinder: ignore
        int ret = oboe_validate_transform_service_name(service_name_cpy, &len);

        if (ret == -1) {
            return "";
        }

        return std::string(service_name_cpy);
    }

    /**
     * Shut down the Oboe library.
     *
     * This releases any resources held by the library which may include terminating
     * child threads.
     */
    static void shutdown() {
        oboe_shutdown();
    }

    /**
     * check if oboe is ready for tracing
     *
     * @param timeout an optional timeout (in milli seconds) to block this function until ready
     * @return one of the return codes (see oboe.h):
     * - OBOE_SERVER_RESPONSE_UNKNOWN
     * - OBOE_SERVER_RESPONSE_OK
     * - OBOE_SERVER_RESPONSE_TRY_LATER
     * - OBOE_SERVER_RESPONSE_LIMIT_EXCEEDED
     * - OBOE_SERVER_RESPONSE_INVALID_API_KEY
     * - OBOE_SERVER_RESPONSE_CONNECT_ERROR
     */
    static int isReady(unsigned int timeout) {
        return oboe_is_ready(timeout);
    }

    // these new objects are managed by SWIG %newobject
    static Event *createEvent();
    static Event *startTrace();

private:

};

class Event : private oboe_event_t {
    friend class Reporter;
    friend class Context;
    friend class Metadata;

private:
    Event() {
        oboe_event_init(this, Context::get(), NULL);
    }

    Event(const oboe_metadata_t *md, bool addEdge=true) {
        // both methods copy metadata from md -> this
        if (addEdge) {
            // create_event automatically adds edge in event to md
            oboe_metadata_create_event(md, this);
        } else {
            // initializes new Event with this md's task_id & new random op_id; no edges set
            oboe_event_init(this, md, NULL);
        }
    }

public:
    ~Event() {
        oboe_event_destroy(this);
    }

    // called e.g. from Python e.addInfo("Key", None) & Ruby e.addInfo("Key", nil)
    bool addInfo(char *key, void* val) {
        // oboe_event_add_info(evt, key, NULL) does nothing
        (void) key;
        (void) val;
        return true;
    }

    bool addInfo(char *key, const std::string& val) {
        if (memchr(val.data(), '\0', val.size())) {
            return oboe_event_add_info_binary(this, key, val.data(), val.size()) == 0;
        } else {
            return oboe_event_add_info(this, key, val.data()) == 0;
        }
    }

    bool addInfo(char *key, long val) {
        int64_t val_ = val;
        return oboe_event_add_info_int64(this, key, val_) == 0;
    }

    bool addInfo(char *key, double val) {
        return oboe_event_add_info_double(this, key, val) == 0;
    }

    bool addEdge(oboe_metadata_t *md) {
        return oboe_event_add_edge(this, md) == 0;
    }

    bool addEdgeStr(const std::string& val) {
        return oboe_event_add_edge_fromstr(this, val.c_str(), val.size()) == 0;
    }

    /**
     * Get a new copy of this metadata.
     *
     * NOTE: The returned object must be "delete"d.
     */
    Metadata* getMetadata() {
        return new Metadata(&this->metadata);
    }

    std::string metadataString() {
        char buf[OBOE_MAX_METADATA_PACK_LEN]; // Flawfinder: ignore

        int rc = oboe_metadata_tostr(&this->metadata, buf, sizeof(buf) - 1);
        if (rc == 0) {
            return std::string(buf);
        } else {
            return std::string(); // throw exception?
        }
    }

    /**
     * Report this event.
     *
     * This sends the event using the default reporter.
     *
     * @return True on success; otherwise an error message is logged.
     */
    bool send() {
        return (oboe_event_send(OBOE_SEND_EVENT, this, Context::get()) >= 0);
    }

    static Event* startTrace(const oboe_metadata_t *md);

};

class Span {
public:
    static std::string createSpan(const char *transaction, const char *domain, const int64_t duration, const char *service_name = NULL);

    static std::string createHttpSpan(const char *transaction, const char *url, const char *domain, const int64_t duration,
            const int status, const char *method, const int has_error, const char *service_name = NULL);
};

std::string Span::createSpan(const char *transaction, const char *domain, const int64_t duration, const char *service_name) {
    oboe_span_params_t params;
    memset(&params, 0, sizeof(oboe_span_params_t));
    params.version = 1;
    params.transaction = transaction;
    params.domain = domain;
    params.duration = duration;
    params.service = service_name;

    char buffer[OBOE_TRANSACTION_NAME_MAX_LENGTH + 1]; // Flawfinder: ignore
    int len = oboe_span(buffer, sizeof(buffer), &params);
    if (len > 0) {
        return std::string(buffer);
    } else {
        return "";
    }
}

std::string Span::createHttpSpan(const char *transaction, const char *url, const char *domain, const int64_t duration,
        const int status, const char *method, const int has_error, const char *service_name) {
    oboe_span_params_t params;
    memset(&params, 0, sizeof(oboe_span_params_t));
    params.version = 1;
    params.transaction = transaction;
    params.url = url;
    params.domain = domain;
    params.duration = duration;
    params.status = status;
    params.method = method;
    params.has_error = has_error;
    params.service = service_name;

    char buffer[OBOE_TRANSACTION_NAME_MAX_LENGTH + 1]; // Flawfinder: ignore
    int len = oboe_http_span(buffer, sizeof(buffer), &params);
    if (len > 0) {
        return std::string(buffer);
    } else {
        return "";
    }
}

class MetricTags {
    friend class CustomMetrics;
public:
    MetricTags(size_t count) {
        tags = new oboe_metric_tag_t[count];
        size = count;
    }
    ~MetricTags() {
        delete[] tags;
    }
    bool add(size_t index, char *k, char *v) {
        if (index < size) {
            tags[index].key = k;
            tags[index].value = v;
            return true;
        }
        return false;
    }
private:
    oboe_metric_tag_t* get() const {
        return tags;
    }

    oboe_metric_tag_t *tags;
    size_t size;
};

class CustomMetrics {
public:
    static int summary(const char *name, const double value, const int count, const int host_tag,
            const char *service_name, const MetricTags *tags, size_t tags_count) {
        if (tags->size < tags_count) {
            tags_count = tags->size;
        }
        return oboe_custom_metric_summary(name, value, count, host_tag, service_name, tags->get(), tags_count);
    }

    static int increment(const char *name, const int count, const int host_tag,
            const char *service_name, const MetricTags *tags, size_t tags_count) {
        if (tags->size < tags_count) {
            tags_count = tags->size;
        }
        return oboe_custom_metric_increment(name, count, host_tag, service_name, tags->get(), tags_count);
    }
};

/**
 * Create a new event object using the thread's context.
 *
 * NOTE: The returned object must be "delete"d.
 */
Event *Context::createEvent() {
    return new Event(Context::get());
}

/**
 * Create a new event object using this Metadata's context.
 *
 * NOTE: The returned object must be "delete"d.
 */
Event *Metadata::createEvent() {
    return new Event(this);
}

/**
 * Create a new event object with a new trace context.
 *
 * NOTE: The returned object must be "delete"d.
 */
Event *Context::startTrace() {
    oboe_metadata_t *md = Context::get();
    oboe_metadata_random(md);
    return new Event();
}

/**
 * Create a new event object using the given metadata context.
 *
 * NOTE: The metadata context must be unique to the new trace.
 *
 * NOTE: The returned object must be "delete"d.
 *
 * @param md The metadata object to use when creating the new event.
 */
Event *Event::startTrace(const oboe_metadata_t *md) {
    return new Event(md, false);
}

class Reporter : private oboe_reporter_t {
    friend class Context;   // Access to the private oboe_reporter_t base structure.
public:
    /**
     * Initialize a reporter structure.
     *
     * See the wrapped Context::init for more details.
     *
     * @param access_key Client access key
     * @param hostname_alias An optional logical/readable hostname that can be used to easily identify the host
     * @param log_level Optional parameter to configure the log level for messages logged by oboe
     * @param max_flush_wait_time Optional parameter to configure maximum wait time for flushing data before terminating in milli seconds
     * @param events_flush_interval Optional parameter to configure how frequently events are flushed
     * @param events_flush_batch_size Optional parameter to configure the batch size before events are flushed
     */
    Reporter(std::string access_key = "",
             std::string hostname_alias = "",
             int log_level = LOGLEVEL_DEFAULT,
             int max_flush_wait_time = DEFAULT_FLUSH_MAX_WAIT_TIME,
             int events_flush_interval = OBOE_DEFAULT_EVENTS_FLUSH_INTERVAL,
             int events_flush_batch_size = OBOE_DEFAULT_EVENTS_FLUSH_BATCH_SIZE) {

        Context::init(access_key, hostname_alias, log_level, max_flush_wait_time, events_flush_interval, events_flush_batch_size);
    }

    ~Reporter() {
        oboe_reporter_destroy(this);
    }

    bool sendReport(Event *evt) {
        return oboe_event_send(OBOE_SEND_EVENT, evt, Context::get()) >= 0;
    }

    bool sendReport(Event *evt, oboe_metadata_t *md) {
        return oboe_event_send(OBOE_SEND_EVENT, evt, md) >= 0;
    }

    bool sendStatus(Event *evt) {
        return oboe_event_send(OBOE_SEND_STATUS, evt, Context::get()) >= 0;
    }

    bool sendStatus(Event *evt, oboe_metadata_t *md) {
        return oboe_event_send(OBOE_SEND_STATUS, evt, md) >= 0;
    }
};

/**
 * Base class for a diagnostic log message handler.
 */
class DebugLogger {
public:
    virtual ~DebugLogger() {}
    virtual void log(int module, int level, const char *source_name, int source_lineno, const char *msg) = 0;
};

/**
 * "C" language wrapper for DebugLogger classes.
 *
 * A logging function that can be added to the logger chain using
 * DebugLog::addDebugLogger().
 *
 * @param context The context pointer that was registered in the call to
 *          DebugLog::addDebugLogger().  Use it to pass the pointer-to-self for
 *          objects (ie. "this" in C++) or just a structure in C,  May be
 *          NULL.
 * @param module The module identifier as passed to oboe_debug_logger().
 * @param level The diagnostic detail level as passed to oboe_debug_logger().
 * @param source_name Name of the source file as passed to oboe_debug_logger().
 * @param source_lineno Number of the line in the source file where message is
 *          logged from as passed to oboe_debug_logger().
 * @param msg The formatted message produced from the format string and its
 *          arguments as passed to oboe_debug_logger().
 */
extern "C" void oboe_debug_log_handler(void *context, int module, int level, const char *source_name, int source_lineno, const char *msg) {
    ((DebugLogger *)context)->log(module, level, source_name, source_lineno, msg);
}

class DebugLog {
public:
    /**
     * Get a printable name for a diagnostics logging level.
     *
     * @param level A detail level in the range 0 to 6 (OBOE_DEBUG_FATAL to OBOE_DEBUG_HIGH).
     */
    static std::string getLevelName(int level) {
        return std::string(oboe_debug_log_level_name(level));
    }

    /**
     * Get a printable name for a diagnostics logging module identifier.
     *
     * @param module One of the OBOE_MODULE_* values.
     */
    static std::string getModuleName(int module) {
        return std::string(oboe_debug_module_name(module));
    }

    /**
     * Get the maximum logging detail level for a module or for all modules.
     *
     * This level applies to the default logger only.  Added loggers get all messages
     * below their registed detail level and need to do their own module-specific
     * filtering.
     *
     * @param module One of the OBOE_MODULE_* values.  Use OBOE_MODULE_ALL (-1) to
     *          get the overall maximum detail level.
     * @return Maximum detail level value for module (or overall) where zero is the
     *          lowest and higher values generate more detailed log messages.
     */
    static int getLevel(int module) {
        return oboe_debug_log_level_get(module);
    }

    /**
     * Set the maximum logging detail level for a module or for all modules.
     *
     * This level applies to the default logger only.  Added loggers get all messages
     * below their registered detail level and need to do their own module-specific
     * filtering.
     *
     * @param module One of the OBOE_MODULE_* values.  Use OBOE_MODULE_ALL to set
     *          the overall maximum detail level.
     * @param newLevel Maximum detail level value where zero is the lowest and higher
     *          values generate more detailed log messages.
     */
    static void setLevel(int module, int newLevel) {
        oboe_debug_log_level_set(module, newLevel);
    }

    /**
     * Set the output stream for the default logger.
     *
     * @param newStream A valid, open FILE* stream or NULL to disable the default logger.
     * @return Zero on success; otherwise an error code (normally from errno).
     */
    static int setOutputStream(FILE *newStream) {
        return oboe_debug_log_to_stream(newStream);
    }

    /**
     * Set the default logger to write to the specified file.
     *
     * A NULL or empty path name will disable the default logger.
     *
     * If the file exists then it will be opened in append mode.
     *
     * @param pathname The path name of the
     * @return Zero on success; otherwise an error code (normally from errno).
     */
    static int setOutputFile(const char *pathname) {
        return oboe_debug_log_to_file(pathname);
    }

    /**
     * Add a logger that takes messages up to a given logging detail level.
     *
     * This adds the logger to a chain in order of the logging level.  Log messages
     * are passed to each logger down the chain until the remaining loggers only
     * accept messages of a lower detail level.
     *
     * @return Zero on success, one if re-registered with the new logging level, and
     *          otherwise a negative value to indicate an error.
     */
    static int addDebugLogger(DebugLogger *newLogger, int logLevel) {
        return oboe_debug_log_add(oboe_debug_log_handler, newLogger, logLevel);
    }

    /**
     * Remove a logger.
     *
     * Remove the logger from the message handling chain.
     *
     * @return Zero on success, one if it was not found, and otherwise a negative
     *          value to indicate an error.
     */
    static int removeDebugLogger(DebugLogger *oldLogger) {
        return oboe_debug_log_remove(oboe_debug_log_handler, oldLogger);
    }

    /**
     * Low-level diagnostics logging function.
     *
     * Use this to pass
     * @param module One of the numeric module identifiers defined in debug.h - used to control logging detail by module.
     * @param level Diagnostic detail level of this message - used to control logging volume by detail level.
     * @param source_name Name of the source file, if available, or another useful name, or NULL.
     * @param source_lineno Number of the line in the source file where message is logged from, if available, or zero.
     * @param format A C language printf format specification string.
     * @param args A variable argument list in VA_ARG format containing arguments for each argument specifier in the format.
     */
    static void logMessage(int module, int level, const char *source_name, int source_lineno, const char *msg) {
        oboe_debug_logger(module, level, source_name, source_lineno, "%s", msg);
    }
};

class Config {
public:
    /**
     * Check if the Oboe library is compatible with a given version.revision.
     *
     * This will succeed if the library is at least as recent as specified and if no
     * definitions have been removed since that revision.
     *
     * @param version The library's version number which increments every time the API changes.
     * @param revision The revision of the current version of the library.
     * @return Non-zero if the Oboe library is considered compatible with the specified revision.
     */
    static bool checkVersion(int version, int revision) {
        return (oboe_config_check_version(version, revision) != 0);
    }

    /**
     * Get the Oboe library version number.
     *
     * This number increments whenever an incompatible change to the API/ABI is made.
     *
     * @return The library's version number or -1 if the version is not known.
     */
    static int getVersion() {
        return oboe_config_get_version();
    }

    /**
     * Get the Oboe library revision number.
     *
     * This number increments whenever a compatible change is made to the
     * API/ABI (ie. an addition).
     *
     * @return The library's revision number or -1 if not known.
     */
    static int getRevision() {
        return oboe_config_get_revision();
    }
};

#endif      // OBOE_HPP
