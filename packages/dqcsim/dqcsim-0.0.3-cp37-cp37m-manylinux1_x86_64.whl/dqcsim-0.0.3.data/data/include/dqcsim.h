#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>

/**
 * Return type for functions that normally return a boolean but can also fail.
 */
typedef enum {
  /**
   * The function has failed. More information may be obtained through
   * `dqcsim_explain()`.
   */
  DQCS_BOOL_FAILURE = -1,
  /**
   * The function did what it was supposed to and returned false.
   */
  DQCS_FALSE = 0,
  /**
   * The function did what it was supposed to and returned true.
   */
  DQCS_TRUE = 1,
} dqcs_bool_return_t;

/**
 * Enumeration of types that can be associated with a handle.
 */
typedef enum {
  /**
   * Indicates that the given handle is invalid.
   * >
   * > This indicates one of the following:
   * >
   * >  - The handle value is invalid (zero or negative).
   * >  - The handle has not been used yet.
   * >  - The object associated with the handle was deleted.
   */
  DQCS_HTYPE_INVALID = 0,
  /**
   * Indicates that the given handle belongs to an `ArbData` object.
   * >
   * > This means that the handle supports the `handle` and `arb` interfaces.
   */
  DQCS_HTYPE_ARB_DATA = 100,
  /**
   * Indicates that the given handle belongs to an `ArbCmd` object.
   * >
   * > This means that the handle supports the `handle`, `arb`, and `cmd`
   * > interfaces.
   */
  DQCS_HTYPE_ARB_CMD = 101,
  /**
   * Indicates that the given handle belongs to a queue of `ArbCmd` object.
   * >
   * > This means that the handle supports the `handle`, `arb`, `cmd`, and
   * > `cq` interfaces.
   */
  DQCS_HTYPE_ARB_CMD_QUEUE = 102,
  /**
   * Indicates that the given handle belongs to a set of qubit references.
   * >
   * > This means that the handle supports the `handle` and `qbset`
   * > interfaces.
   */
  DQCS_HTYPE_QUBIT_SET = 103,
  /**
   * Indicates that the given handle belongs to a quantum gate description.
   * >
   * > This means that the handle supports the `handle`, `gate`, and `arb`
   * > interfaces.
   */
  DQCS_HTYPE_GATE = 104,
  /**
   * Indicates that the given handle belongs to a qubit measurement result.
   * >
   * > This means that the handle supports the `handle`, `meas`, and `arb`
   * > interfaces. It can also be used in place of a qubit measurement result
   * > set by functions that consume the object.
   */
  DQCS_HTYPE_MEAS = 105,
  /**
   * Indicates that the given handle belongs to a set of qubit measurement
   * results.
   * >
   * > This means that the handle supports the `handle` and `mset` interfaces.
   */
  DQCS_HTYPE_MEAS_SET = 106,
  /**
   * Indicates that the given handle belongs to a frontend plugin process
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `pcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_FRONT_PROCESS_CONFIG = 200,
  /**
   * Indicates that the given handle belongs to an operator plugin process
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `pcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_OPER_PROCESS_CONFIG = 201,
  /**
   * Indicates that the given handle belongs to a backend plugin process
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `pcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_BACK_PROCESS_CONFIG = 203,
  /**
   * Indicates that the given handle belongs to a frontend plugin thread
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `tcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_FRONT_THREAD_CONFIG = 204,
  /**
   * Indicates that the given handle belongs to an operator plugin thread
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `tcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_OPER_THREAD_CONFIG = 205,
  /**
   * Indicates that the given handle belongs to a backend plugin thread
   * configuration object.
   * >
   * > This means that the handle supports the `handle`, `tcfg`, and `xcfg`
   * > interfaces.
   */
  DQCS_HTYPE_BACK_THREAD_CONFIG = 206,
  /**
   * Indicates that the given handle belongs to a simulator configuration
   * object.
   * >
   * > This means that the handle supports the `handle` and `scfg` interfaces.
   */
  DQCS_HTYPE_SIM_CONFIG = 207,
  /**
   * Indicates that the given handle belongs to a simulator instance.
   * >
   * > This means that the handle supports the `handle` and `sim` interfaces.
   */
  DQCS_HTYPE_SIM = 208,
  /**
   * Indicates that the given handle belongs to a frontend plugin
   * definition object.
   * >
   * > This means that the handle supports the `handle` and `pdef` interfaces.
   */
  DQCS_HTYPE_FRONT_DEF = 300,
  /**
   * Indicates that the given handle belongs to an operator plugin
   * definition object.
   * >
   * > This means that the handle supports the `handle` and `pdef` interfaces.
   */
  DQCS_HTYPE_OPER_DEF = 301,
  /**
   * Indicates that the given handle belongs to a backend plugin
   * definition object.
   * >
   * > This means that the handle supports the `handle` and `pdef` interfaces.
   */
  DQCS_HTYPE_BACK_DEF = 302,
  /**
   * Indicates that the given handle belongs to a plugin thread join handle.
   * >
   * > This means that the handle supports the `handle` and `pjoin`
   * > interfaces.
   */
  DQCS_HTYPE_PLUGIN_JOIN = 303,
} dqcs_handle_type_t;

/**
 * Enumeration of loglevels and logging modes.
 */
typedef enum {
  /**
   * Invalid loglevel. Used to indicate failure of an API that returns a
   * loglevel.
   */
  DQCS_LOG_INVALID = -1,
  /**
   * Turns logging off.
   */
  DQCS_LOG_OFF = 0,
  /**
   * This loglevel is to be used for reporting a fatal error, resulting from
   * the owner of the logger getting into an illegal state from which it
   * cannot recover. Such problems are also reported to the API caller via
   * Result::Err if applicable.
   */
  DQCS_LOG_FATAL = 1,
  /**
   * This loglevel is to be used for reporting or propagating a non-fatal
   * error caused by the API caller doing something wrong. Such problems are
   * also reported to the API caller via Result::Err if applicable.
   */
  DQCS_LOG_ERROR = 2,
  /**
   * This loglevel is to be used for reporting that a called API/function is
   * telling us we did something wrong (that we weren't expecting), but we
   * can recover. For instance, for a failed connection attempt to something
   * that really should not be failing, we can still retry (and eventually
   * report critical or error if a retry counter overflows). Since we're
   * still trying to rectify things at this point, such problems are NOT
   * reported to the API/function caller via Result::Err.
   */
  DQCS_LOG_WARN = 3,
  /**
   * This loglevel is to be used for reporting information specifically
   * requested by the user/API caller, such as the result of an API function
   * requested through the command line, or an explicitly captured
   * stdout/stderr stream.
   */
  DQCS_LOG_NOTE = 4,
  /**
   * This loglevel is to be used for reporting information NOT specifically
   * requested by the user/API caller, such as a plugin starting up or
   * shutting down.
   */
  DQCS_LOG_INFO = 5,
  /**
   * This loglevel is to be used for reporting debugging information useful
   * for debugging the user of the API provided by the logged instance.
   */
  DQCS_LOG_DEBUG = 6,
  /**
   * This loglevel is to be used for reporting debugging information useful
   * for debugging the internals of the logged instance. Such messages would
   * normally only be generated by debug builds, to prevent them from
   * impacting performance under normal circumstances.
   */
  DQCS_LOG_TRACE = 7,
  /**
   * This is intended to be used when configuring the stdout/stderr capture
   * mode for a plugin process. Selecting it will prevent the stream from
   * being captured; it will just be the same stream as DQCsim's own
   * stdout/stderr. When used as the loglevel for a message, the message
   * itself is sent to stderr instead of passing into DQCsim's log system.
   * Using this for loglevel filters leads to undefined behavior.
   */
  DQCS_LOG_PASS = 8,
} dqcs_loglevel_t;

/**
 * Qubit measurement value.
 */
typedef enum {
  /**
   * Error value used to indicate that something went wrong.
   */
  DQCS_MEAS_INVALID = -1,
  /**
   * Indicates that the qubit was measured to be zero.
   */
  DQCS_MEAS_ZERO = 0,
  /**
   * Indicates that the qubit was measured to be one.
   */
  DQCS_MEAS_ONE = 1,
  /**
   * Indicates that the measurement value is unknown for whatever reason.
   */
  DQCS_MEAS_UNDEFINED = 2,
} dqcs_measurement_t;

/**
 * Reproduction file path style.
 */
typedef enum {
  /**
   * Error value used to indicate that something went wrong.
   */
  DQCS_PATH_STYLE_INVALID = -1,
  /**
   * Specifies that paths should be saved the same way they were specified
   * on the command line.
   */
  DQCS_PATH_STYLE_KEEP = 0,
  /**
   * Specifies that all paths should be saved relative to DQCsim's working
   * directory.
   */
  DQCS_PATH_STYLE_RELATIVE = 1,
  /**
   * Specifies that all paths should be saved canonically, i.e. relative to
   * the root directory.
   */
  DQCS_PATH_STYLE_ABSOLUTE = 2,
} dqcs_path_style_t;

/**
 * Enumeration of the three types of plugins.
 */
typedef enum {
  /**
   * Invalid plugin type. Used to indicate failure of an API that returns
   * a plugin type.
   */
  DQCS_PTYPE_INVALID = -1,
  /**
   * Frontend plugin.
   */
  DQCS_PTYPE_FRONT = 0,
  /**
   * Operator plugin.
   */
  DQCS_PTYPE_OPER = 1,
  /**
   * Backend plugin.
   */
  DQCS_PTYPE_BACK = 2,
} dqcs_plugin_type_t;

/**
 * Default return type for functions that don't need to return anything.
 */
typedef enum {
  /**
   * The function has failed. More information may be obtained through
   * `dqcsim_explain()`.
   */
  DQCS_FAILURE = -1,
  /**
   * The function did what it was supposed to.
   */
  DQCS_SUCCESS = 0,
} dqcs_return_t;

/**
 * Type for a handle.
 * >
 * > Handles are like pointers into DQCsim's internal structures: all API calls
 * > use these to refer to objects. Besides the object, they contain type
 * > information. This type can be retrieved using `dqcs_handle_type()`.
 * >
 * > Handles are always positive integers, counting upwards from 1 upon
 * > allocation, and they are not reused even after being deleted. Thus, every
 * > subsequent object allocation returns a handle one greater than the
 * > previous. Note however that DQCsim may allocate objects as well without
 * > the user specifically requesting this, so external code should generally
 * > *not* rely on this behavior unless otherwise noted. The value zero is
 * > reserved for invalid references or error propagation.
 * >
 * > Note that the scope for handles is thread-local. That is, data referenced
 * > by a handle cannot be shared or moved between threads.
 * >
 * > The value zero is reserved for invalid references or error propagation.
 */
typedef unsigned long long dqcs_handle_t;

/**
 * Type for a qubit reference.
 * >
 * > Qubit references are exchanged between the frontend, operator, and backend
 * > plugins to indicate which qubits a gate operates on. Note that this makes
 * > them fundamentally different from handles, which are thread-local.
 * >
 * > Qubit references are always positive integers, counting upwards from 1 upon
 * > allocation, and they are not reused even after the qubit is deallocated.
 * > Thus, every subsequent allocation returns a qubit reference one greater
 * > than the previous. This is guaranteed behavior that external code can rely
 * > upon. The value zero is reserved for invalid references or error
 * > propagation.
 */
typedef unsigned long long dqcs_qubit_t;

/**
 * Type for a plugin state.
 * >
 * > This is an opaque type that is passed along to plugin implementation
 * > callback functions, which those callbacks can then use to interact with the
 * > plugin instance. User code shall not create or modify values of this type,
 * > and shall only use the values when calling `dqcs_plugin_*` functions.
 */
typedef void *dqcs_plugin_state_t;

/**
 * Type for a simulation cycle timestamp.
 * >
 * > Timestamps count upward from zero. The type is signed to allow usage of -1
 * > for errors, and to allow numerical differences to be represented.
 */
typedef long long dqcs_cycle_t;

/**
 * Copies the data from one object to another.
 */
dqcs_return_t dqcs_arb_assign(dqcs_handle_t dest, dqcs_handle_t src);

/**
 * Returns the JSON/CBOR object of an `ArbData` object in the form of a CBOR
 * object.
 * >
 * > If the actual size of the object differs from the specified object size,
 * > this function will copy the minimum of the actual and specified sizes
 * > number of bytes, and return what the actual size was.
 * >
 * > If the specified object size is zero, `obj` is allowed to be `NULL`. You
 * > can use this to query the size before allocating an object.
 * >
 * > This function returns -1 on failure.
 */
ssize_t dqcs_arb_cbor_get(dqcs_handle_t arb, void *obj, size_t obj_size);

/**
 * Sets the JSON/CBOR object of an `ArbData` object by means of a CBOR object.
 */
dqcs_return_t dqcs_arb_cbor_set(dqcs_handle_t arb, const void *obj, size_t obj_size);

/**
 * Clears the unstructured argument list.
 */
dqcs_return_t dqcs_arb_clear(dqcs_handle_t arb);

/**
 * Returns the unstructured string argument at the specified index.
 * >
 * > If the actual size of the object differs from the specified object size,
 * > this function will copy the minimum of the actual and specified sizes
 * > number of bytes, and return what the actual size was.
 * >
 * > If the specified object size is zero, `obj` is allowed to be `NULL`. You
 * > can use this to determine the size of the argument prior to actually
 * > reading it, so you can allocate the right buffer size first.
 * >
 * > This function returns -1 on failure.
 */
ssize_t dqcs_arb_get_raw(dqcs_handle_t arb, ssize_t index, void *obj, size_t obj_size);

/**
 * Returns the size in bytes of the unstructured string argument at the
 * specified index.
 * >
 * > Returns -1 when the function fails.
 */
ssize_t dqcs_arb_get_size(dqcs_handle_t arb, ssize_t index);

/**
 * Returns the unstructured string argument at the specified index.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_arb_get_str(dqcs_handle_t arb, ssize_t index);

/**
 * Inserts an unstructured raw argument into the list at the specified
 * index.
 */
dqcs_return_t dqcs_arb_insert_raw(dqcs_handle_t arb,
                                  ssize_t index,
                                  const void *obj,
                                  size_t obj_size);

/**
 * Inserts an unstructured string argument into the list at the specified
 * index.
 */
dqcs_return_t dqcs_arb_insert_str(dqcs_handle_t arb, ssize_t index, const char *s);

/**
 * Returns the JSON/CBOR object of an `ArbData` object in the form of a JSON
 * string.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_arb_json_get(dqcs_handle_t arb);

/**
 * Sets the JSON/CBOR object of an `ArbData` object by means of a JSON string.
 */
dqcs_return_t dqcs_arb_json_set(dqcs_handle_t arb, const char *json);

/**
 * Returns the number of unstructured arguments, or -1 to indicate failure.
 */
ssize_t dqcs_arb_len(dqcs_handle_t arb);

/**
 * Creates a new `ArbData` object.
 * >
 * > Returns the handle of the newly created `ArbData`. The `ArbData` is
 * > initialized with JSON object `{}` and an empty binary argument list.
 * >
 * > `ArbData` objects support the `handle` and `arb` APIs.
 */
dqcs_handle_t dqcs_arb_new(void);

/**
 * Pops an unstructured argument from the back of the list without returning
 * it.
 */
dqcs_return_t dqcs_arb_pop(dqcs_handle_t arb);

/**
 * Pops an unstructured raw argument from the back of the list.
 * >
 * > If the actual size of the object differs from the specified object size,
 * > this function will copy the minimum of the actual and specified sizes
 * > number of bytes, and return what the actual size was.
 * >
 * > If the specified object size is zero, `obj` is allowed to be `NULL`. You
 * > can use this if you don't need the contents of the argument and just want
 * > to delete it.
 * >
 * > Since this function removes the returned element, data will be lost if the
 * > specified size is smaller than the actual size. To avoid this, first use
 * > `dqcs_arb_get_size(handle, -1)` to query the size.
 * >
 * > This function returns -1 on failure. If this is due to a `NULL` buffer
 * > being passed, the data that was popped is lost.
 */
ssize_t dqcs_arb_pop_raw(dqcs_handle_t arb, void *obj, size_t obj_size);

/**
 * Pops an unstructured string argument from the back of the list.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`. If the failure is due to the
 * > conversion from binary object to C string (i.e., embedded nulls), the
 * > data is still popped and is thus lost.
 */
char *dqcs_arb_pop_str(dqcs_handle_t arb);

/**
 * Pushes an unstructured raw argument to the back of the list.
 */
dqcs_return_t dqcs_arb_push_raw(dqcs_handle_t arb, const void *obj, size_t obj_size);

/**
 * Pushes an unstructured string argument to the back of the list.
 */
dqcs_return_t dqcs_arb_push_str(dqcs_handle_t arb, const char *s);

/**
 * Removes the specified unstructured string argument from the list.
 */
dqcs_return_t dqcs_arb_remove(dqcs_handle_t arb, ssize_t index);

/**
 * Replaces the unstructured argument at the specified index with the
 * specified raw object.
 */
dqcs_return_t dqcs_arb_set_raw(dqcs_handle_t arb, ssize_t index, const void *obj, size_t obj_size);

/**
 * Replaces the unstructured argument at the specified index with the
 * specified string.
 */
dqcs_return_t dqcs_arb_set_str(dqcs_handle_t arb, ssize_t index, const char *s);

/**
 * Compares the interface ID of an `ArbCmd` with the given string.
 * >
 * > Returns -1 for failure, 0 for no match, or 1 for a match.
 */
dqcs_bool_return_t dqcs_cmd_iface_cmp(dqcs_handle_t cmd, const char *iface);

/**
 * Returns the interface ID of an `ArbCmd`.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_cmd_iface_get(dqcs_handle_t cmd);

/**
 * Creates a new `ArbCmd` object.
 * >
 * > Returns the handle of the newly created `ArbCmd`. The `ArbCmd` is
 * > initialized with the given interface and operation IDs, JSON object `{}`,
 * > and an empty binary argument list. Upon failure, returns 0.
 * >
 * > `ArbCmd` objects support the `handle`, `arb`, and `cmd` interfaces.
 */
dqcs_handle_t dqcs_cmd_new(const char *iface, const char *oper);

/**
 * Compares the operation ID of an `ArbCmd` with the given string.
 * >
 * > Returns -1 for failure, 0 for no match, or 1 for a match.
 */
dqcs_bool_return_t dqcs_cmd_oper_cmp(dqcs_handle_t cmd, const char *oper);

/**
 * Returns the operation ID of an `ArbCmd`.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_cmd_oper_get(dqcs_handle_t cmd);

/**
 * Returns the number of `ArbCmd` objects in the given `ArbCmd` queue.
 * >
 * > This function returns -1 to indicate failure.
 */
ssize_t dqcs_cq_len(dqcs_handle_t cq);

/**
 * Creates a new `ArbCmd` queue object.
 * >
 * > Returns the handle of the newly created `ArbCmd` queue. The queue is
 * > initially empty. Queues implement a "first-in, first-out" model.
 * >
 * > `ArbCmd` queue objects support the `handle`, `arb`, `cmd`, and `cq` APIs.
 * >
 * > The `arb` and `cmd` APIs refer to the `ArbCmd` at the front of the queue.
 * > Use `dqcs_cq_next()` to remove the front entry, allowing access to the next
 * > command.
 */
dqcs_handle_t dqcs_cq_new(void);

/**
 * Advances an `ArbCmd` queue to the next command.
 * >
 * > Use the `dqcs_arb_*` and `dqcs_cmd_*` interfaces to read out the command
 * > before calling this function.
 * >
 * > To iterate over a queue in C, use the following snippit:
 * >
 * > ```C
 * > for (; dqcs_cq_len(queue) > 0; dqcs_cq_next(queue)) {
 * >     dqcs_cmd_...(queue, ...)
 * >     dqcs_arb_...(queue, ...)
 * > }
 * > ```
 */
dqcs_return_t dqcs_cq_next(dqcs_handle_t cq);

/**
 * Pushes an `ArbCmd` object into the given `ArbCmd` queue.
 * >
 * > This function returns -1 to indicate failure. The `ArbCmd` object specified
 * > by `cmd` is moved into the queue. That is, the handle is consumed if and
 * > only if the function succeeds.
 */
dqcs_return_t dqcs_cq_push(dqcs_handle_t cq, dqcs_handle_t cmd);

/**
 * Returns a pointer to the latest error message.
 * >
 * > Call this to get extra information when another function returns a failure
 * > code. The returned pointer is temporary and therefore should **NOT** be
 * > `free()`d. It will become invalid when a new error occurs.
 */
const char *dqcs_error_get(void);

/**
 * Sets the latest error message string.
 * >
 * > This must be called by callback functions when an error occurs within the
 * > callback, otherwise the upstream result for `dqcs_error_get()` will be
 * > undefined.
 * >
 * > If `msg` is set to `NULL`, the error string is cleared instead.
 */
void dqcs_error_set(const char *msg);

/**
 * Returns a handle to a new qubit reference set containing the qubits
 * that control this gate.
 */
dqcs_handle_t dqcs_gate_controls(dqcs_handle_t gate);

/**
 * Returns whether the specified gate has control qubits.
 */
dqcs_bool_return_t dqcs_gate_has_controls(dqcs_handle_t gate);

/**
 * Returns whether a unitary matrix is associated with this gate.
 */
dqcs_bool_return_t dqcs_gate_has_matrix(dqcs_handle_t gate);

/**
 * Returns whether the specified gate measures any qubits.
 */
dqcs_bool_return_t dqcs_gate_has_measures(dqcs_handle_t gate);

/**
 * Returns whether the specified gate has target qubits.
 */
dqcs_bool_return_t dqcs_gate_has_targets(dqcs_handle_t gate);

/**
 * Returns whether the specified gate is a custom gate.
 * >
 * > If this returns true, the type of gate is to be determined by matching its
 * > name against a set of known gate types. If this returns false, the gate is
 * > expected to be executed as follows, in this order:
 * >
 * >  - if there are target qubits, extend the supplied unitary matrix to
 * >    include the control qubits (if any), then apply it to the control +
 * >    target qubits;
 * >  - measure each measured qubit (if any) in the Z basis.
 */
dqcs_bool_return_t dqcs_gate_is_custom(dqcs_handle_t gate);

/**
 * Returns a copy of the unitary matrix associated with this gate, if one
 * exists.
 * >
 * > If this function succeeds, the matrix is returned in row-major form, using
 * > pairs of doubles for the real vs. imaginary component of each entry. The
 * > size will be `4**len(targets)` complex numbers = `2*4**len(targets)`
 * > doubles = `16*4**len(targets)` bytes.
 * >
 * > On success, this **returns a newly allocated array containing the matrix.
 * > Free it with `free()` when you're done with it to avoid memory leaks.** On
 * > failure, or if no matrix is associated with this gate, this returns `NULL`.
 * > Use `dqcs_gate_has_matrix()` to disambiguate.
 */
double *dqcs_gate_matrix(dqcs_handle_t gate);

/**
 * Returns the size of the gate matrix associated with this gate.
 * >
 * > The size is returned in the form of the number of complex entries. That is,
 * > the number of doubles is two times the return value, and the size in bytes
 * > is 8 times the return value. 0 is returned when there is no matrix. -1 is
 * > used to report errors.
 */
ssize_t dqcs_gate_matrix_len(dqcs_handle_t gate);

/**
 * Returns a handle to a new qubit reference set containing the qubits
 * measured by this gate.
 */
dqcs_handle_t dqcs_gate_measures(dqcs_handle_t gate);

/**
 * Returns the name of a custom gate.
 * >
 * > This function fails if the gate is not a custom gate. Query
 * > `dqcs_gate_is_custom()` to disambiguate between a non-custom gate and a
 * > different error.
 * >
 * > On success, this **returns a newly allocated string containing the gate
 * > name. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_gate_name(dqcs_handle_t gate);

/**
 * Constructs a new custom gate.
 * >
 * > The functionality of custom gates is not specified by DQCsim. Instead, this
 * > is left up to the plugins. Of course, for this to work, plugins that are
 * > connected to each other must agree on the format used.
 * >
 * > `name` specifies the name of the gate. The name is used to indicate which
 * > custom operation is to be applied.
 * >
 * > `targets` optionally specifies the set of target qubits. You may pass 0 or
 * > an empty qubit set if you don't need target qubits.
 * >
 * > `controls` optionally specifies the set of control qubits. You may pass 0
 * > or an empty qubit set if you don't need control qubits.
 * >
 * > `measures` optionally specifies the set of measured qubits. You may pass 0
 * > or an empty qubit set if no qubits are measured. Note that the upstream
 * > plugin expects exactly one measurement result for each qubit specified in
 * > this set; anything else results in a warning and the measurement result
 * > being set to undefined.
 * >
 * > `matrix` can point to an appropriately sized array of doubles, or be `NULL`
 * > if no matrix is required. If a matrix is specified, at least one target
 * > qubit is required, and the matrix must be appropriately sized for the
 * > number of target qubits. The matrix is specified in row-major form, using
 * > pairs of doubles for the real vs. imaginary component of each entry. The
 * > size must thus be `4**len(targets)` complex numbers = `2*4**len(targets)`
 * > doubles = `16*4**len(targets)` bytes. `matrix_len` must be set to the
 * > number of complex numbers.
 * >
 * > In addition to the above data, gate objects implement the `arb` interface
 * > to allow user-specified classical information to be attached.
 * >
 * > This function returns the handle to the gate, or 0 to indicate failure.
 * > The specified qubit sets are consumed/deleted by this function if and only
 * > if it succeeds.
 */
dqcs_handle_t dqcs_gate_new_custom(const char *name,
                                   dqcs_handle_t targets,
                                   dqcs_handle_t controls,
                                   dqcs_handle_t measures,
                                   const double *matrix,
                                   size_t matrix_len);

/**
 * Constructs a new measurement gate.
 * >
 * > `measures` must be a handle to a qubit set. The qubits in this set are
 * > measured in the Z-basis. To measure in other bases, first apply the
 * > respective rotation, or use a custom gate.
 * >
 * > This function returns the handle to the gate, or 0 to indicate failure.
 * > The `measures` qubit set is consumed/deleted by this function if and only
 * > if it succeeds.
 */
dqcs_handle_t dqcs_gate_new_measurement(dqcs_handle_t measures);

/**
 * Constructs a new unitary gate.
 * >
 * > `targets` must be a handle to a non-empty qubit set. The qubits in this set
 * > correspond with the supplied unitary matrix.
 * >
 * > `controls` optionally specifies a set of control qubits. You may pass 0 or
 * > an empty qubit set if you don't need control qubits.
 * >
 * > `matrix` must point to an appropriately sized array of doubles,
 * > representing the unitary matrix to be applied to the qubits in the
 * > `targets` set. The matrix is specified in row-major form, using pairs of
 * > doubles for the real vs. imaginary component of each entry. The size must
 * > thus be `4**len(targets)` complex numbers = `2*4**len(targets)` doubles =
 * > `16*4**len(targets)` bytes. `matrix_len` must be set to the number of
 * > complex numbers.
 * >
 * > The supplied matrix is only applied to the target qubits if all the control
 * > qubits are or will be determined to be set. For instance, to encode a
 * > CCNOT/Toffoli gate, you can specify one target qubits, two control qubits,
 * > and [0, 1; 1, 0] (X) for the matrix. This is equivalent to extending the
 * > matrix to the full Toffoli matrix and specifying all three qubits in the
 * > targets set, or the midway solution using a CNOT matrix, but these
 * > solutions may be less efficient depending on whether the simulator can
 * > optimize its calculations for controlled gates.
 * >
 * > Simulators are not required to apply the (hidden) global phase component of
 * > the gate matrix in the same way it is specified; that is, if the simulator
 * > can optimize its calculations by altering the global phase it is allowed
 * > to.
 * >
 * > If is up to the user to ensure that the specified matrix is unitary. This
 * > is NOT checked by DQCsim. The simulator backend may or may not check this.
 * >
 * > This function returns the handle to the gate, or 0 to indicate failure.
 * > The `targets` qubit set and (if specified) the `controls` qubit set are
 * > consumed/deleted by this function if and only if it succeeds.
 */
dqcs_handle_t dqcs_gate_new_unitary(dqcs_handle_t targets,
                                    dqcs_handle_t controls,
                                    const double *matrix,
                                    size_t matrix_len);

/**
 * Returns a handle to a new qubit reference set containing the qubits
 * targetted by this gate.
 */
dqcs_handle_t dqcs_gate_targets(dqcs_handle_t gate);

/**
 * Destroys the object associated with a handle.
 * >
 * > Returns 0 when successful, -1 otherwise.
 */
dqcs_return_t dqcs_handle_delete(dqcs_handle_t handle);

/**
 * Deletes all handles for the current thread.
 * >
 * > This can be used to clean stuff up at the end of `main()` or before an
 * > `abort()` of some kind. If you don't clean up properly, you might get
 * > undefined behavior or errors when DQCsim tries to do it for you.
 */
dqcs_return_t dqcs_handle_delete_all(void);

/**
 * Returns a debug dump of the object associated with the given handle.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > description. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_handle_dump(dqcs_handle_t handle);

/**
 * Succeeds only if there are no live handles in the current thread.
 * >
 * > This is intended for testing and for finding handle leaks. The error
 * > message returned when handles remain contains dumps of the first 10
 * > remaining handles.
 */
dqcs_return_t dqcs_handle_leak_check(void);

/**
 * Returns the type of object associated with the given handle.
 */
dqcs_handle_type_t dqcs_handle_type(dqcs_handle_t handle);

/**
 * Primitive API for sending a log message using the current logger.
 * >
 * > Returns `DQCS_SUCCESS` if logging was successful, or `DQCS_FAILURE` if no
 * > logger is available in the current thread or one of the arguments could not
 * > be converted. Loggers are available in the simulation host thread and in
 * > threads running plugins.
 * >
 * > ## Formatting and fallback to stderr
 * >
 * > As an alternative to this function, you can also use `dqcs_log_format()`.
 * > This function differs from `dqcs_log_raw()` in two ways:
 * >
 * >  - Instead of the `message` string, a printf-style format string and
 * >    associated varargs are passed to construct the message.
 * >  - When logging fails, this function falls back to writing to `stderr`
 * >    instead of returning the errors.
 * >
 * > ## Macros
 * >
 * > From C and C++, these functions are normally not called directly. Instead,
 * > the following macros are used:
 * >
 * > ```C
 * > dqcs_log_trace("trace message!");
 * > dqcs_log_debug("debug message!");
 * > dqcs_log_info("info message!");
 * > dqcs_log_note("notice!");
 * > dqcs_log_warn("warning!");
 * > dqcs_log_error("error!");
 * > dqcs_log_fatal("fatal error!");
 * > ```
 * >
 * > These macros automatically set `file` to the C source filename and `line`
 * > to the line number. `module` is hardcoded to "C" or "CPP" depending on
 * > source file language. They use `dqcs_log_format()`, so they also support
 * > printf-style formatting. For instance:
 * >
 * > ```C
 * > dqcs_note("answer to %s: %d", "ultimate question", 42);
 * > ```
 */
dqcs_return_t dqcs_log_raw(dqcs_loglevel_t level,
                           const char *module,
                           const char *file,
                           uint32_t line_nr,
                           const char *message);

/**
 * Constructs a new measurement object.
 * >
 * > `qubit` must be set to the qubit that was measured, `value` must be set to
 * > its value. The return value is the handle to the measurement object, or 0
 * > if something went wrong.
 * >
 * > Note that measurement objects implement the `arb` interface, so additional
 * > data can be attached to the object.
 */
dqcs_handle_t dqcs_meas_new(dqcs_qubit_t qubit, dqcs_measurement_t value);

/**
 * Returns the qubit reference associated with a measurement object.
 */
dqcs_qubit_t dqcs_meas_qubit_get(dqcs_handle_t meas);

/**
 * Sets the qubit reference associated with a measurement object.
 */
dqcs_return_t dqcs_meas_qubit_set(dqcs_handle_t meas, dqcs_qubit_t qubit);

/**
 * Returns the measurement value associated with a measurement object.
 */
dqcs_measurement_t dqcs_meas_value_get(dqcs_handle_t meas);

/**
 * Sets the measurement value associated with a measurement object.
 */
dqcs_return_t dqcs_meas_value_set(dqcs_handle_t meas, dqcs_measurement_t value);

/**
 * Returns whether the given qubit measurement set contains data for the given
 * qubit.
 */
dqcs_bool_return_t dqcs_mset_contains(dqcs_handle_t mset, dqcs_qubit_t qubit);

/**
 * Returns a copy of the measurement result for the given qubit from a
 * measurement result set.
 */
dqcs_handle_t dqcs_mset_get(dqcs_handle_t mset, dqcs_qubit_t qubit);

/**
 * Returns the number of qubits measurements in the given measurement set.
 * >
 * > This function returns -1 to indicate failure.
 */
ssize_t dqcs_mset_len(dqcs_handle_t mset);

/**
 * Creates a new set of qubit measurement results.
 * >
 * > Returns the handle of the newly created set. The set is initially empty.
 */
dqcs_handle_t dqcs_mset_new(void);

/**
 * Removes the measurement result for the given qubit from a measurement
 * result set.
 */
dqcs_return_t dqcs_mset_remove(dqcs_handle_t mset, dqcs_qubit_t qubit);

/**
 * Adds a measurement result to a measurement result set.
 * >
 * > If there was already a measurement for the specified qubit, the previous
 * > measurement result is overwritten. The measurement result object is deleted
 * > if and only if the function succeeds.
 */
dqcs_return_t dqcs_mset_set(dqcs_handle_t mset, dqcs_handle_t meas);

/**
 * Returns the measurement result for the given qubit from a measurement
 * result set and removes it from the set.
 */
dqcs_handle_t dqcs_mset_take(dqcs_handle_t mset, dqcs_qubit_t qubit);

/**
 * Returns the measurement result for any of the qubits contained in a
 * measurement result set and removes it from the set.
 * >
 * > This is useful for iteration.
 */
dqcs_handle_t dqcs_mset_take_any(dqcs_handle_t mset);

/**
 * Returns the configured timeout for the plugin process to connect to DQCsim.
 * >
 * > The time unit is in seconds. Returns positive inifinity for an infinite
 * > timeout. Returns -1 when the function fails.
 */
double dqcs_pcfg_accept_timeout_get(dqcs_handle_t pcfg);

/**
 * Configures the timeout for the plugin process to connect to DQCsim.
 * >
 * > The default is 5 seconds, so you should normally be able to leave this
 * > alone.
 * >
 * > The time unit is seconds. Use IEEE positive infinity to specify an infinite
 * > timeout.
 */
dqcs_return_t dqcs_pcfg_accept_timeout_set(dqcs_handle_t pcfg, double timeout);

/**
 * Overrides an environment variable for the plugin process.
 * >
 * > The environment variable `key` is set to `value` regardless of whether it
 * > exists in the parent environment variable scope.
 * >
 * > If value is `NULL`, the environment variable `key` is unset instead.
 */
dqcs_return_t dqcs_pcfg_env_set(dqcs_handle_t pcfg, const char *key, const char *value);

/**
 * Removes/unsets an environment variable for the plugin process.
 * >
 * > The environment variable `key` is unset regardless of whether it exists in
 * > the parent environment variable scope.
 */
dqcs_return_t dqcs_pcfg_env_unset(dqcs_handle_t pcfg, const char *key);

/**
 * Returns the configured executable path for the given plugin process.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > executable path. Free it with `free()` when you're done with it to avoid
 * > memory leaks.** On failure (i.e., the handle is invalid) this returns
 * > `NULL`.
 */
char *dqcs_pcfg_executable(dqcs_handle_t pcfg);

/**
 * Appends an `ArbCmd` to the list of initialization commands of a plugin
 * process.
 * >
 * > The `ArbCmd` handle is consumed by this function, and is thus invalidated,
 * > if and only if it is successful.
 */
dqcs_return_t dqcs_pcfg_init_cmd(dqcs_handle_t pcfg, dqcs_handle_t cmd);

/**
 * Returns the configured name for the given plugin process.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > name. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_pcfg_name(dqcs_handle_t pcfg);

/**
 * Creates a new plugin process configuration object using sugared syntax.
 * >
 * > `typ` specifies the type of plugin. `name` specifies the name used to refer
 * > to the plugin later, which much be unique within a simulation; if it is
 * > empty or `NULL`, auto-naming will be performed: "front" for the frontend,
 * > "oper&lt;i&gt;" for the operators (indices starting at 1 from frontend to
 * > backend), and "back" for the backend. `spec` specifies which plugin to use,
 * > using the same syntax that the `dqcsim` command line interface uses.
 */
dqcs_handle_t dqcs_pcfg_new(dqcs_plugin_type_t typ, const char *name, const char *spec);

/**
 * Creates a new plugin process configuration object using raw paths.
 * >
 * > This works the same as `dqcs_pcfg_new()`, but instead of the sugared,
 * > command-line style specification you have to specify the path to the plugin
 * > executable and (if applicable) the script it must execute directly. This is
 * > useful when you have a specific executable in mind and you don't want the
 * > somewhat heuristic desugaring algorithm from doing something unexpected.
 * >
 * > Pass `NULL` or an empty string to `script` to specify a native plugin
 * > executable that does not take a script argument.
 */
dqcs_handle_t dqcs_pcfg_new_raw(dqcs_plugin_type_t typ,
                                const char *name,
                                const char *executable,
                                const char *script);

/**
 * Returns the configured script path for the given plugin process.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > script path. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`. An
 * > empty string will be returned if no script is configured to distinguish it
 * > from failure.
 */
char *dqcs_pcfg_script(dqcs_handle_t pcfg);

/**
 * Returns the configured timeout for the plugin process to shut down
 * gracefully.
 * >
 * > The time unit is in seconds. Returns positive inifinity for an infinite
 * > timeout. Returns -1 when the function fails.
 */
double dqcs_pcfg_shutdown_timeout_get(dqcs_handle_t pcfg);

/**
 * Configures the timeout for the plugin process to shut down gracefully.
 * >
 * > The default is 5 seconds, so you should normally be able to leave this
 * > alone.
 * >
 * > The time unit is seconds. Use IEEE positive infinity to specify an infinite
 * > timeout.
 */
dqcs_return_t dqcs_pcfg_shutdown_timeout_set(dqcs_handle_t pcfg, double timeout);

/**
 * Returns the configured stderr capture mode for the specified plugin
 * process.
 */
dqcs_loglevel_t dqcs_pcfg_stderr_mode_get(dqcs_handle_t pcfg);

/**
 * Configures the capture mode for the stderr stream of the specified plugin
 * process.
 */
dqcs_return_t dqcs_pcfg_stderr_mode_set(dqcs_handle_t pcfg, dqcs_loglevel_t level);

/**
 * Returns the configured stdout capture mode for the specified plugin
 * process.
 */
dqcs_loglevel_t dqcs_pcfg_stdout_mode_get(dqcs_handle_t pcfg);

/**
 * Configures the capture mode for the stdout stream of the specified plugin
 * process.
 */
dqcs_return_t dqcs_pcfg_stdout_mode_set(dqcs_handle_t pcfg, dqcs_loglevel_t level);

/**
 * Configures a plugin process to also output its log messages to a file.
 * >
 * > `verbosity` configures the verbosity level for the file only.
 */
dqcs_return_t dqcs_pcfg_tee(dqcs_handle_t pcfg, dqcs_loglevel_t verbosity, const char *filename);

/**
 * Returns the type of the given plugin process configuration.
 */
dqcs_plugin_type_t dqcs_pcfg_type(dqcs_handle_t pcfg);

/**
 * Returns the configured verbosity for the given plugin process.
 */
dqcs_loglevel_t dqcs_pcfg_verbosity_get(dqcs_handle_t pcfg);

/**
 * Configures the logging verbosity for the given plugin process.
 */
dqcs_return_t dqcs_pcfg_verbosity_set(dqcs_handle_t pcfg, dqcs_loglevel_t level);

/**
 * Returns the configured working directory for the given plugin process.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > working directory. Free it with `free()` when you're done with it to avoid
 * > memory leaks.** On failure (i.e., the handle is invalid) this returns
 * > `NULL`.
 */
char *dqcs_pcfg_work_get(dqcs_handle_t pcfg);

/**
 * Overrides the working directory for the plugin process.
 */
dqcs_return_t dqcs_pcfg_work_set(dqcs_handle_t pcfg, const char *work);

/**
 * Returns the plugin author for the given plugin definition object.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_pdef_author(dqcs_handle_t pdef);

/**
 * Returns the plugin name for the given plugin definition object.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_pdef_name(dqcs_handle_t pdef);

/**
 * Creates a new `PluginDefinition` object.
 * >
 * > Plugin definitions contain the callback functions/closures that define the
 * > functionality of a plugin. They also contain some metadata to identify the
 * > implementation, in the form of a name, author, and version string, that
 * > must be specified when the definition is constructed. The callback
 * > functions/closures are initialized to sane defaults for the requested
 * > plugin type, but obviously one or more of these should be overridden to
 * > make the plugin do something.
 * >
 * > Once a definition object has been built, it can be used to spawn a plugin
 * > thread or run a plugin in the main thread, given a DQCsim server URL for it
 * > to connect to.
 */
dqcs_handle_t dqcs_pdef_new(dqcs_plugin_type_t typ,
                            const char *name,
                            const char *author,
                            const char *version);

/**
 * Sets the callback for advancing time for operators and backends.
 * >
 * > The default behavior for operators is to pass through to
 * > `dqcs_plugin_advance()`. The default for backends is no-op. This
 * > callback is never called for frontend plugins.
 * >
 * > Besides the common arguments, the callback receives an unsigned integer
 * > specifying the number of cycles to advance by.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning `DQCS_FAILURE`. Otherwise, it should
 * > return `DQCS_SUCCESS`.
 */
dqcs_return_t dqcs_pdef_set_advance_cb(dqcs_handle_t pdef,
                                       dqcs_return_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_cycle_t cycles),
                                       void (*user_free)(void *user_data),
                                       void *user_data);

/**
 * Sets the qubit allocation callback for operators and backends.
 * >
 * > The default for operators is to pass through to
 * > `dqcs_plugin_allocate()`. The default for backends is no-op. This
 * > callback is never called for frontend plugins.
 * >
 * > Besides the common arguments, the callback receives a handle to a qubit
 * > set containing the references that are to be used for the
 * > to-be-allocated qubits and an `ArbCmd` queue containing user-defined
 * > commands to optionally augment the behavior of the qubits. These are
 * > borrowed handles; the caller will delete them.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning `DQCS_FAILURE`. Otherwise, it should
 * > return `DQCS_SUCCESS`.
 */
dqcs_return_t dqcs_pdef_set_allocate_cb(dqcs_handle_t pdef,
                                        dqcs_return_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t qubits, dqcs_handle_t alloc_cmds),
                                        void (*user_free)(void *user_data),
                                        void *user_data);

/**
 * Sets the user logic drop/cleanup callback.
 * >
 * > This is called when a plugin is gracefully terminated. It is not
 * > recommended to execute any downstream instructions at this time, but it
 * > is supported in case this is really necessary.
 * >
 * > The default behavior is no-op.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning `DQCS_FAILURE`. Otherwise, it should
 * > return `DQCS_SUCCESS`.
 */
dqcs_return_t dqcs_pdef_set_drop_cb(dqcs_handle_t pdef,
                                    dqcs_return_t (*callback)(void *user_data, dqcs_plugin_state_t state),
                                    void (*user_free)(void *user_data),
                                    void *user_data);

/**
 * Sets the qubit deallocation callback for operators and backends.
 * >
 * > The default for operators is to pass through to `dqcs_plugin_free()`.
 * > The default for backends is no-op. This callback is never called for
 * > frontend plugins.
 * >
 * > Besides the common arguments, the callback receives a handle to a qubit
 * > set containing the qubits that are to be freed. This is a borrowed
 * > handle; the caller will delete it.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning `DQCS_FAILURE`. Otherwise, it should
 * > return `DQCS_SUCCESS`.
 */
dqcs_return_t dqcs_pdef_set_free_cb(dqcs_handle_t pdef,
                                    dqcs_return_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t qubits),
                                    void (*user_free)(void *user_data),
                                    void *user_data);

/**
 * Sets the gate execution callback for operators and backends.
 * >
 * > Besides the common arguments, the callback receives a handle to the
 * > to-be-executed gate. This is a borrowed handle; the caller will delete
 * > it.
 * >
 * > The callback must return one of the following things:
 * >
 * >  - a valid handle to a measurement set, created using
 * >    `dqcs_mset_new()` (this object is automatically deleted after the
 * >    callback returns);
 * >  - a valid handle to a single qubit measurement, created using
 * >    `dqcs_meas_new()` (this object is automatically deleted after the
 * >    callback returns);
 * >  - the handle to the supplied gate, a shortcut for not returning any
 * >    measurements (this is less clear than returning an empty measurement
 * >    set, but slightly faster); or
 * >  - 0 to report an error, after calling the error string using
 * >    `dqcs_set_error()`.
 * >
 * > Backend plugins must return a measurement result set containing exactly
 * > those qubits specified in the measurement set. For operators, however,
 * > the story is more complicated. Let's say we want to make a silly
 * > operator that inverts all measurements. The trivial way to do
 * > this would be to forward the gate, query all the measurement results
 * > using `dqcs_plugin_get_measurement()`, invert them, stick them in a
 * > measurement result set, and return that result set. However, this
 * > approach is not very efficient, because `dqcs_plugin_get_measurement()`
 * > has to wait for all downstream plugins to finish executing the gate,
 * > forcing the OS to switch threads, etc. Instead, operators are allowed
 * > to return only a subset (or none) of the measured qubits, as long as
 * > they return the measurements as they arrive through the
 * > `modify_measurement()` callback.
 * >
 * > The default implementation for this callback for operators is to pass
 * > the gate through to the downstream plugin and return an empty set of
 * > measurements. Combined with the default implementation of
 * > `modify_measurement()`, this behavior is sane. Backends must override
 * > this callback; the default is to return a not-implemented error.
 * >
 * > Note that for our silly example operator, the default behavior for this
 * > function is sufficient; you'd only have to override
 * > `modify_measurement()` to, well, modify the measurements.
 */
dqcs_return_t dqcs_pdef_set_gate_cb(dqcs_handle_t pdef,
                                    dqcs_handle_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t gate),
                                    void (*user_free)(void *user_data),
                                    void *user_data);

/**
 * Sets the callback function function for handling an arb from the host.
 * >
 * > The default behavior for this is no-op.
 * >
 * > Besides the common arguments, the callback receives a handle to the
 * > `ArbCmd` object representing the request. It must return a valid
 * > `ArbData` handle containing the response. Both objects are deleted
 * > automatically after invocation.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning 0. Otherwise, it should return a valid
 * > `ArbData` handle.
 */
dqcs_return_t dqcs_pdef_set_host_arb_cb(dqcs_handle_t pdef,
                                        dqcs_handle_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t cmd),
                                        void (*user_free)(void *user_data),
                                        void *user_data);

/**
 * Sets the user logic initialization callback.
 * >
 * > This is always called before any of the other callbacks are run. The
 * > downstream plugin has already been initialized at this stage, so it is
 * > legal to send it commands.
 * >
 * > The default behavior is no-op.
 * >
 * > Besides the common arguments, the callback receives a handle to an
 * > `ArbCmd` queue (`dqcs_cq_*`, `dqcs_cmd_*`, and `dqcs_arb_*` interfaces)
 * > containing user-defined initialization commands. This is a borrowed
 * > handle; the caller will delete it.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning `DQCS_FAILURE`. Otherwise, it should
 * > return `DQCS_SUCCESS`.
 */
dqcs_return_t dqcs_pdef_set_initialize_cb(dqcs_handle_t pdef,
                                          dqcs_return_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t init_cmds),
                                          void (*user_free)(void *user_data),
                                          void *user_data);

/**
 * Sets the measurement modification callback for operators.
 * >
 * > This callback is called for every measurement result received from the
 * > downstream plugin, and returns the measurements that should be reported
 * > to the upstream plugin. Note that the results from our plugin's
 * > `dqcs_plugin_get_measurement()` and friends are consistent with the
 * > results received from downstream; they are not affected by this
 * > function.
 * >
 * > The callback takes a handle to a single qubit measurement object as an
 * > argument, and must return one of the following things:
 * >
 * >  - a valid handle to a measurement set, created using
 * >    `dqcs_mset_new()` (this object is automatically deleted after the
 * >    callback returns);
 * >  - a valid handle to a single qubit measurement object, which may or
 * >    may not be the supplied one (this object is automatically deleted
 * >    after the callback returns); or
 * >  - 0 to report an error, after calling the error string using
 * >    `dqcs_set_error()`.
 * >
 * > This callback is somewhat special in that it is not allowed to call
 * > any plugin command other than logging and the pseudorandom number
 * > generator functions. This is because this function is called
 * > asynchronously with respect to the downstream functions, making the
 * > timing of these calls non-deterministic based on operating system
 * > scheduling.
 * >
 * > Note that while this function is called for only a single measurement
 * > at a time, it is allowed to produce a vector of measurements. This
 * > allows you to cancel propagation of the measurement by returning an
 * > empty vector, to just modify the measurement data itself, or to
 * > generate additional measurements from a single measurement. However,
 * > if you need to modify the qubit references for operators that remap
 * > qubits, take care to only send measurement data upstream when these
 * > were explicitly requested through the associated upstream gate
 * > function's `measured` list.
 * >
 * > The default behavior for this callback is to return the measurement
 * > without modification.
 */
dqcs_return_t dqcs_pdef_set_modify_measurement_cb(dqcs_handle_t pdef,
                                                  dqcs_handle_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t meas),
                                                  void (*user_free)(void *user_data),
                                                  void *user_data);

/**
 * Sets the run callback for frontends.
 * >
 * > This is called in response to a `start()` host API call. The return
 * > value is returned through the `wait()` host API call.
 * >
 * > The default behavior is to fail with a "not implemented" error;
 * > frontends backends should always override this. This callback is never
 * > called for operator or backend plugins.
 * >
 * > Besides the common arguments, the callback receives a handle to an
 * > `ArbData` object containing the data that the host passed to `start()`.
 * > This is a borrowed handle; the caller will delete it.
 * >
 * > When the run callback is successful, it should return a valid `ArbData`
 * > handle. This can be the same as the argument, but it can also be a new
 * > object. This `ArbData` is returned to the host through `wait()`. This
 * > `ArbData` object is deleted after the callback completes.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning 0. Otherwise, it should return a
 * > valid `ArbData` handle.
 */
dqcs_return_t dqcs_pdef_set_run_cb(dqcs_handle_t pdef,
                                   dqcs_handle_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t args),
                                   void (*user_free)(void *user_data),
                                   void *user_data);

/**
 * Sets the callback function for handling an arb from upstream for
 * operators and backends.
 * >
 * > The default behavior for operators is to pass through to
 * > `dqcs_plugin_arb()`; operators that do not support the requested
 * > interface should always do this. The default for backends is no-op.
 * > This callback is never called for frontend plugins.
 * >
 * > Besides the common arguments, the callback receives a handle to the
 * > `ArbCmd` object representing the request. It must return a valid
 * > `ArbData` handle containing the response. Both objects are deleted
 * > automatically after invocation.
 * >
 * > The callback can return an error by setting an error message using
 * > `dqcs_error_set()` and returning 0. Otherwise, it should return a valid
 * > `ArbData` handle.
 */
dqcs_return_t dqcs_pdef_set_upstream_arb_cb(dqcs_handle_t pdef,
                                            dqcs_handle_t (*callback)(void *user_data, dqcs_plugin_state_t state, dqcs_handle_t cmd),
                                            void (*user_free)(void *user_data),
                                            void *user_data);

/**
 * Returns the plugin type for the given plugin definition object.
 */
dqcs_plugin_type_t dqcs_pdef_type(dqcs_handle_t pdef);

/**
 * Returns the plugin version for the given plugin definition object.
 * >
 * > On success, this **returns a newly allocated string containing the JSON
 * > string. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure, this returns `NULL`.
 */
char *dqcs_pdef_version(dqcs_handle_t pdef);

/**
 * Tells the downstream plugin to run for the specified number of cycles.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > The return value is the new cycle counter. This function uses -1 to signal
 * > an error.
 */
dqcs_cycle_t dqcs_plugin_advance(dqcs_plugin_state_t plugin, dqcs_cycle_t cycles);

/**
 * Allocate the given number of downstream qubits.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > `num_qubits` specifies the number of qubits that are to be allocated.
 * >
 * > `commands` must be 0 or a valid handle to an `ArbCmd` queue, containing a
 * > list of commands that may be used to modify the behavior of the qubit
 * > register; 0 is equivalent to zero commands. The queue is consumed by this
 * > function, i.e. the handle becomes invalid, if and only if it succeeds.
 * >
 * > If the function is successful, a new handle to the set of qubit references
 * > representing the newly allocated register is returned. When the function
 * > fails, 0 is returned.
 */
dqcs_handle_t dqcs_plugin_allocate(dqcs_plugin_state_t plugin,
                                   uintptr_t num_qubits,
                                   dqcs_handle_t cq);

/**
 * Sends an arbitrary command downstream.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > This function returns a new handle to an `ArbData` object representing the
 * > return value of the `ArbCmd` when successful. Otherwise, it returns 0.
 */
dqcs_handle_t dqcs_plugin_arb(dqcs_plugin_state_t plugin, dqcs_handle_t cmd);

/**
 * Free the given downstream qubits.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > `qubits` must be a valid set of qubit references. The set is consumed by
 * > this function, i.e. the handle becomes invalid, if and only if it succeeds.
 */
dqcs_return_t dqcs_plugin_free(dqcs_plugin_state_t plugin, dqcs_handle_t qbset);

/**
 * Tells the downstream plugin to execute a gate.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > `gate` must be a valid gate object. The object is consumed by this
 * > function, i.e. the handle becomes invalid, if and only if it succeeds.
 */
dqcs_return_t dqcs_plugin_gate(dqcs_plugin_state_t plugin, dqcs_handle_t gate);

/**
 * Returns the current value of the downstream cycle counter.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > This function uses -1 to signal an error.
 */
dqcs_cycle_t dqcs_plugin_get_cycle(dqcs_plugin_state_t plugin);

/**
 * Returns the number of downstream cycles between the last two measurements
 * of the given downstream qubit.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > This function uses -1 to signal an error.
 */
dqcs_cycle_t dqcs_plugin_get_cycles_between_measures(dqcs_plugin_state_t plugin,
                                                     dqcs_qubit_t qubit);

/**
 * Returns the number of downstream cycles since the latest measurement of the
 * given downstream qubit.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > This function uses -1 to signal an error.
 */
dqcs_cycle_t dqcs_plugin_get_cycles_since_measure(dqcs_plugin_state_t plugin, dqcs_qubit_t qubit);

/**
 * Returns the latest measurement of the given downstream qubit.
 * >
 * > Backend plugins are not allowed to call this. Doing so will result in an
 * > error.
 * >
 * > If the function succeeds, it returns a new handle to a qubit measurement
 * > result object. Otherwise it returns 0.
 */
dqcs_handle_t dqcs_plugin_get_measurement(dqcs_plugin_state_t plugin, dqcs_qubit_t qubit);

/**
 * Generates a random floating point number using the simulator random seed.
 * >
 * > The generated numbers are uniformly distributed in the range `[0,1>`.
 * >
 * > This function only fails if the `plugin` handle is invalid, in which case
 * > it returns 0. Of course, 0 is also a valid (if rare) random return value.
 */
double dqcs_plugin_random_f64(dqcs_plugin_state_t plugin);

/**
 * Generates a random unsigned 64-bit number using the simulator random seed.
 * >
 * > This function only fails if the `plugin` handle is invalid, in which case
 * > it returns 0. Of course, 0 is also a valid (if rare) random return value.
 */
dqcs_handle_t dqcs_plugin_random_u64(dqcs_plugin_state_t plugin);

/**
 * Waits for a message from the host.
 * >
 * > It is only legal to call this function from within the `run()` callback.
 * > Any other source will result in an error.
 * >
 * > When successful, this function returns a new handle to the received
 * > `ArbData` object. 0 is used to indicate that an error occurred.
 */
dqcs_handle_t dqcs_plugin_recv(dqcs_plugin_state_t plugin);

/**
 * Executes a plugin in the current thread.
 * >
 * > `pdef` must be an appropriately populated plugin definition object.
 * > Its callback functions will be called from the current thread, from within
 * > the context of this function.
 * >
 * > `simulator` must be set to the address of our endpoint of the simulator
 * > that's using the plugin; DQCsim normally passes this as the first command
 * > line argument of the plugin process.
 * >
 * > If the plugin starts, the `pdef` handle is consumed by this function,
 * > regardless of whether the plugin eventually closes normally. The handle is
 * > only left alive if `pdef` is not a plugin definition object.
 */
dqcs_return_t dqcs_plugin_run(dqcs_handle_t pdef, const char *simulator);

/**
 * Sends a message to the host.
 * >
 * > It is only legal to call this function from within the `run()` callback.
 * > Any other source will result in an error.
 * >
 * > The `cmd` handle is consumed by this function if and only if it succeeds.
 */
dqcs_return_t dqcs_plugin_send(dqcs_plugin_state_t plugin, dqcs_handle_t arb);

/**
 * Executes a plugin in a worker thread.
 * >
 * > This function behaves the same as dqcs_plugin_log(), but is asynchronous;
 * > it always returns immediately. Of course, this means that the callbacks in
 * > `pdef` will be called from a different thread.
 * >
 * > To wait for the thread to finish executing, call `dqcs_plugin_wait()` on
 * > the returned join handle. Alternatively you can delete the join handle
 * > object, which will detach the thread.
 * >
 * > Note that `dqcs_log_*()` will only be available in the thread that the
 * > plugin actually runs in.
 * >
 * > This function returns 0 to indicate failure to start the plugin. Otherwise,
 * > the join handle is returned.
 */
dqcs_handle_t dqcs_plugin_start(dqcs_handle_t pdef, const char *simulator);

/**
 * Waits for a plugin worker thread to finish executing.
 * >
 * > Unless the join handle is invalid, this function returns success/failure
 * > based on the result of the plugin execution. If the plugin thread is
 * > joined, the join handle is deleted.
 */
dqcs_return_t dqcs_plugin_wait(dqcs_handle_t pjoin);

/**
 * Returns whether the given qubit set contains the given qubit.
 */
dqcs_bool_return_t dqcs_qbset_contains(dqcs_handle_t qbset, dqcs_qubit_t qubit);

/**
 * Returns a copy of the given qubit set, intended for non-destructive
 * iteration.
 */
dqcs_handle_t dqcs_qbset_copy(dqcs_handle_t qbset);

/**
 * Returns the number of qubits in the given set.
 * >
 * > This function returns -1 to indicate failure.
 */
ssize_t dqcs_qbset_len(dqcs_handle_t qbset);

/**
 * Creates a new set of qubit references.
 * >
 * > Returns the handle of the newly created set. The set is initially empty.
 * > Qubit sets are ordered, meaning that the order in which qubits are popped
 * > from the set equals the order in which they were pushed. To iterate over a
 * > set, simply make a copy and drain the copy using pop.
 */
dqcs_handle_t dqcs_qbset_new(void);

/**
 * Pops a qubit reference off of a qubit reference set.
 * >
 * > Qubits are popped in the same order in which they were pushed. That is,
 * > they are FIFO-ordered.
 */
dqcs_qubit_t dqcs_qbset_pop(dqcs_handle_t qbset);

/**
 * Pushes a qubit reference into a qubit reference set.
 * >
 * > This function will fail if the specified qubit was already part of the set.
 */
dqcs_return_t dqcs_qbset_push(dqcs_handle_t qbset, dqcs_qubit_t qubit);

/**
 * Returns the configured verbosity for DQCsim's own messages.
 */
dqcs_loglevel_t dqcs_scfg_dqcsim_verbosity_get(dqcs_handle_t scfg);

/**
 * Configures the logging verbosity for DQCsim's own messages.
 */
dqcs_return_t dqcs_scfg_dqcsim_verbosity_set(dqcs_handle_t scfg, dqcs_loglevel_t level);

/**
 * Configures DQCsim to also output its log messages to callback function.
 * >
 * > `verbosity` specifies the minimum importance of a message required for the
 * > callback to be called.
 * >
 * > `callback` is the callback function to install. It is always called with
 * > the `user_data` pointer to make calling stuff like class member functions
 * > or closures possible. The `user_free` function, if non-null, will be called
 * > when the callback is uninstalled in any way. If `callback` is null, any
 * > current callback is uninstalled instead. For consistency, if `user_free` is
 * > non-null while `callback` is null, `user_free` is called immediately, under
 * > the assumption that the caller has allocated resources unbeknownst that the
 * > callback it's trying to install is null.
 * >
 * > **NOTE: both `callback` and `user_free` may be called from a thread spawned
 * > by the simulator. Calling any API calls from the callback is therefore
 * > undefined behavior!**
 * >
 * > The callback takes the following arguments:
 * >  - `void*`: user defined data.
 * >  - `const char*`: log message string, excluding metadata.
 * >  - `const char*`: name assigned to the logger that was used to produce the
 * >    message (= "dqcsim" or a plugin name).
 * >  - `dqcs_loglevel_t`: the verbosity level that the message was logged with.
 * >  - `const char*`: string representing the source of the log message, or
 * >    `NULL` when no source is known.
 * >  - `const char*`: string containing the filename of the source that
 * >    generated the message, or `NULL` when no source is known.
 * >  - `uint32_t`: line number within the aforementioned file, or 0 if not
 * >    known.
 * >  - `uint64_t`: Time in seconds since the Unix epoch.
 * >  - `uint32_t`: Additional time in nanoseconds since the aforementioned.
 * >  - `uint32_t`: PID of the generating process.
 * >  - `uint64_t`: TID of the generating thread.
 * >
 * > If an internal log record is particularly malformed and cannot be coerced
 * > into the above (nul bytes in the strings, invalid timestamp, whatever) the
 * > message is silently ignored.
 * >
 * > The primary use of this callback is to pipe DQCsim's messages to an
 * > external logging framework. When you do this, you probably also want to
 * > call `dqcs_scfg_stderr_verbosity_set(handle, DQCS_LOG_OFF)` to prevent
 * > DQCsim from writing the messages to stderr itself.
 */
dqcs_return_t dqcs_scfg_log_callback(dqcs_handle_t scfg,
                                     dqcs_loglevel_t verbosity,
                                     void (*callback)(void *user_data, const char *message, const char *logger, dqcs_loglevel_t level, const char *module, const char *file, uint32_t line, uint64_t time_s, uint32_t time_ns, uint32_t pid, uint64_t tid),
                                     void (*user_free)(void *user_data),
                                     void *user_data);

/**
 * Constructs an empty simulation configuration.
 * >
 * > Before the configuration can be used, at least a frontend and a backend
 * > plugin configuration must be pushed into it. This can be done with
 * > `dqcs_scfg_push_plugin()`. Failing to do this will result in an error when
 * > you try to start the simulation.
 * >
 * > The default settings correspond to the defaults of the `dqcsim` command
 * > line interface. Refer to its help for more information.
 */
dqcs_handle_t dqcs_scfg_new(void);

/**
 * Appends a plugin to a simulation configuration.
 * >
 * > Both plugin process and plugin thread configuration objects may be used.
 * > The handle is consumed by this function, and is thus invalidated, if and
 * > only if it is successful.
 * >
 * > Frontend and backend plugins will automatically be inserted at the front
 * > and back of the pipeline when the simulation is created. Operators are
 * > inserted in front to back order. This function does not provide safeguards
 * > against multiple frontends/backends; such errors will only be reported when
 * > the simulation is started.
 * >
 * > Note that it is not possible to observe or mutate a plugin configuration
 * > once it has been added to a simulator configuration handle. If you want to
 * > do this for some reason, you should maintain your own data structures, and
 * > only build the DQCsim structures from them when you're done.
 */
dqcs_return_t dqcs_scfg_push_plugin(dqcs_handle_t scfg, dqcs_handle_t xcfg);

/**
 * Disables the reproduction logging system.
 * >
 * > Calling this will disable the warnings printed when a simulation that
 * > cannot be reproduced is constructed.
 */
dqcs_return_t dqcs_scfg_repro_disable(dqcs_handle_t scfg);

/**
 * Returns the path style used when writing reproduction files.
 */
dqcs_path_style_t dqcs_scfg_repro_path_style_get(dqcs_handle_t scfg);

/**
 * Sets the path style used when writing reproduction files.
 */
dqcs_return_t dqcs_scfg_repro_path_style_set(dqcs_handle_t scfg, dqcs_path_style_t path_style);

/**
 * Returns the configured random seed.
 * >
 * > This function will return 0 when it fails, but this can unfortunately not
 * > be reliably distinguished from a seed that was set to 0.
 */
uint64_t dqcs_scfg_seed_get(dqcs_handle_t scfg);

/**
 * Configures the random seed that the simulation should use.
 * >
 * > Note that the seed is randomized by default.
 */
dqcs_return_t dqcs_scfg_seed_set(dqcs_handle_t scfg, uint64_t seed);

/**
 * Returns the configured stderr sink verbosity for a simulation.
 * >
 * > That is, the minimum loglevel that a messages needs to have for it to be
 * > printed to stderr.
 */
dqcs_loglevel_t dqcs_scfg_stderr_verbosity_get(dqcs_handle_t scfg);

/**
 * Configures the stderr sink verbosity for a simulation.
 * >
 * > That is, the minimum loglevel that a messages needs to have for it to be
 * > printed to stderr.
 */
dqcs_return_t dqcs_scfg_stderr_verbosity_set(dqcs_handle_t scfg, dqcs_loglevel_t level);

/**
 * Configures DQCsim to also output its log messages to a file.
 * >
 * > `verbosity` configures the verbosity level for the file only.
 */
dqcs_return_t dqcs_scfg_tee(dqcs_handle_t scfg, dqcs_loglevel_t verbosity, const char *filename);

/**
 * Sends an `ArbCmd` message to one of the plugins, referenced by name.
 * >
 * > `ArbCmd`s are executed immediately after yielding to the simulator, so
 * > all pending asynchronous calls are flushed and executed *before* the
 * > `ArbCmd`.
 * >
 * > When this succeeds, the received data is returned in the form of a new
 * > handle. When it fails, 0 is returned.
 * >
 * > The `ArbCmd` handle is consumed if and only if the API call succeeds.
 */
dqcs_handle_t dqcs_sim_arb(dqcs_handle_t sim, const char *name, dqcs_handle_t cmd);

/**
 * Sends an `ArbCmd` message to one of the plugins, referenced by index.
 * >
 * > The frontend always has index 0. 1 through N are used for the operators
 * > in front to back order (where N is the number of operators). The
 * > backend is at index N+1.
 * >
 * > Python-style negative indices are supported. That is, -1 can be used to
 * > refer to the backend, -2 to the last operator, and so on.
 * >
 * > `ArbCmd`s are executed immediately after yielding to the simulator, so
 * > all pending asynchronous calls are flushed and executed *before* the
 * > `ArbCmd`.
 * >
 * > When this succeeds, the received data is returned in the form of a new
 * > handle. When it fails, 0 is returned.
 * >
 * > The `ArbCmd` handle is consumed if and only if the API call succeeds.
 */
dqcs_handle_t dqcs_sim_arb_idx(dqcs_handle_t sim, ssize_t index, dqcs_handle_t cmd);

/**
 * Queries the author of a plugin, referenced by instance name.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > author. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_author(dqcs_handle_t sim, const char *name);

/**
 * Queries the author of a plugin, referenced by index.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > author. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_author_idx(dqcs_handle_t sim, ssize_t index);

/**
 * Queries the implementation name of a plugin, referenced by instance
 * name.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > name. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_name(dqcs_handle_t sim, const char *name);

/**
 * Queries the implementation name of a plugin, referenced by index.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > name. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_name_idx(dqcs_handle_t sim, ssize_t index);

/**
 * Queries the version of a plugin, referenced by instance name.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > version. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_version(dqcs_handle_t sim, const char *name);

/**
 * Queries the version of a plugin, referenced by index.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > version. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_sim_get_version_idx(dqcs_handle_t sim, ssize_t index);

/**
 * Constructs a DQCsim simulation.
 * >
 * > The provided handle is consumed if it is a simulation configuration,
 * > regardless of whether simulation construction succeeds.
 */
dqcs_handle_t dqcs_sim_new(dqcs_handle_t scfg);

/**
 * Waits for the simulated accelerator to send a message to us.
 * >
 * > When this succeeds, the received data is returned in the form of a new
 * > handle. When it fails, 0 is returned.
 * >
 * > Deadlocks are detected and prevented by returning an error.
 */
dqcs_handle_t dqcs_sim_recv(dqcs_handle_t sim);

/**
 * Sends a message to the simulated accelerator.
 * >
 * > This is an asynchronous call: nothing happens until `yield()`,
 * > `recv()`, or `wait()` is called.
 * >
 * > The `ArbData` handle is optional; if 0 is passed, an empty data object is
 * > used. If a handle is passed, it is consumed if and only if the API call
 * > succeeds.
 */
dqcs_return_t dqcs_sim_send(dqcs_handle_t sim, dqcs_handle_t data);

/**
 * Starts a program on the simulated accelerator.
 * >
 * > This is an asynchronous call: nothing happens until `yield()`,
 * > `recv()`, or `wait()` is called.
 * >
 * > The `ArbData` handle is optional; if 0 is passed, an empty data object is
 * > used. If a handle is passed, it is consumed if and only if the API call
 * > succeeds.
 */
dqcs_return_t dqcs_sim_start(dqcs_handle_t sim, dqcs_handle_t data);

/**
 * Waits for the simulated accelerator to finish its current program.
 * >
 * > When this succeeds, the return value of the accelerator's `run()`
 * > function is returned in the form of a new handle. When it fails, 0 is
 * > returned.
 * >
 * > Deadlocks are detected and prevented by returning an error.
 */
dqcs_handle_t dqcs_sim_wait(dqcs_handle_t sim);

/**
 * Writes a reproduction file for the simulation so far.
 */
dqcs_return_t dqcs_sim_write_reproduction_file(dqcs_handle_t sim, const char *filename);

/**
 * Yields to the simulator.
 * >
 * > The simulation runs until it blocks again. This is useful if you want an
 * > immediate response to an otherwise asynchronous call through the logging
 * > system or some communication channel outside of DQCsim's control.
 * >
 * > This function silently returns immediately if no asynchronous data was
 * > pending or if the simulator is waiting for something that has not been
 * > sent yet.
 */
dqcs_return_t dqcs_sim_yield(dqcs_handle_t sim);

/**
 * Appends an `ArbCmd` to the list of initialization commands of a plugin
 * thread.
 * >
 * > The `ArbCmd` handle is consumed by this function, and is thus invalidated,
 * > if and only if it is successful.
 */
dqcs_return_t dqcs_tcfg_init_cmd(dqcs_handle_t tcfg, dqcs_handle_t cmd);

/**
 * Returns the configured name for the given plugin thread.
 * >
 * > On success, this **returns a newly allocated string containing the
 * > name. Free it with `free()` when you're done with it to avoid memory
 * > leaks.** On failure (i.e., the handle is invalid) this returns `NULL`.
 */
char *dqcs_tcfg_name(dqcs_handle_t tcfg);

/**
 * Creates a new plugin thread configuration object from a plugin definition.
 * >
 * > The plugin definition handle is consumed by this function.
 */
dqcs_handle_t dqcs_tcfg_new(dqcs_handle_t pdef, const char *name);

/**
 * Creates a new plugin thread configuration object from a callback.
 * >
 * > The callback is called by DQCsim from a dedicated thread when DQCsim wants
 * > to start the plugin. The callback must then in some way spawn a plugin
 * > process that connects to the provided simulator string. The callback should
 * > return only when the process terminates.
 */
dqcs_handle_t dqcs_tcfg_new_raw(dqcs_plugin_type_t plugin_type,
                                const char *name,
                                void (*callback)(void *user_data, const char *simulator),
                                void (*user_free)(void *user_data),
                                void *user_data);

/**
 * Configures a plugin thread to also output its log messages to a file.
 * >
 * > `verbosity` configures the verbosity level for the file only.
 */
dqcs_return_t dqcs_tcfg_tee(dqcs_handle_t tcfg, dqcs_loglevel_t verbosity, const char *filename);

/**
 * Returns the type of the given plugin thread configuration.
 */
dqcs_plugin_type_t dqcs_tcfg_type(dqcs_handle_t tcfg);

/**
 * Returns the configured verbosity for the given plugin thread.
 */
dqcs_loglevel_t dqcs_tcfg_verbosity_get(dqcs_handle_t tcfg);

/**
 * Configures the logging verbosity for the given plugin thread.
 */
dqcs_return_t dqcs_tcfg_verbosity_set(dqcs_handle_t tcfg, dqcs_loglevel_t level);

//*****************************************************************************
// Functions that cannot be implemented in Rust
//*****************************************************************************

#ifdef __cplusplus
namespace dqcsim {
#endif

/**
 * Sends a log message using the current logger using printf-like formatting.
 *
 * This function is identical to `dqcs_log_raw()`, except instead of a single
 * string it takes a printf-like format string and varargs to compose the
 * message.
 */
inline void dqcs_log_format(
  dqcs_loglevel_t level,
  const char *module,
  const char *file,
  uint32_t line,
  const char *fmt,
  ...
)
#if defined(__GNUC__)
__attribute__((format(printf,5,6)))
#endif
;
inline void dqcs_log_format(
  dqcs_loglevel_t level,
  const char *module,
  const char *file,
  uint32_t line,
  const char *fmt,
  ...
)
{
  // Figure out the buffer size we need.
  va_list ap;
  va_start(ap, fmt);
  int size = vsnprintf(NULL, 0, fmt, ap) + 1;
  va_end(ap);

  // Allocate the buffer.
  char *buffer = (char*)malloc(size);
  if (buffer == NULL) {
    fprintf(stderr, "Error: failed to allocate buffer for log message!\n");
    return;
  }

  // Perform the actual formatting operation.
  va_list ap2;
  va_start(ap2, fmt);
  vsnprintf(buffer, size, fmt, ap2);
  va_end(ap2);

  // Send to DQCsim.
  if (((int)dqcs_log_raw(level, module, file, line, buffer)) < 0) {
    fprintf(stderr, "Error while trying to log: %s\n", dqcs_error_get());
    fprintf(stderr, "The message was: %s\n", buffer);
    fprintf(stderr, "In %s, %s:%u\n", module, file, line);
  }

  // Don't leak!
  free(buffer);
}

#ifdef __cplusplus
} // namespace dqcsim
#endif

//*****************************************************************************
// Macros
//*****************************************************************************

#ifdef __cplusplus
#define DQCS_LANGUAGE "CPP"
#define DQCS_LOGLEVEL_PREFIX ::dqcsim::dqcs_loglevel_t::
#else
#define DQCS_LANGUAGE "C"
#define DQCS_LOGLEVEL_PREFIX
#endif

/**
 * Convenience macro for calling `dqcs_log_format()` with trace loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_trace(fmt, ...)          \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_TRACE,  \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with debug loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_debug(fmt, ...)          \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_DEBUG,  \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with info loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_info(fmt, ...)           \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_INFO,   \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with note loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_note(fmt, ...)           \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_NOTE,   \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with warn loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_warn(fmt, ...)           \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_WARN,   \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with error loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_error(fmt, ...)          \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_ERROR,  \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

/**
 * Convenience macro for calling `dqcs_log_format()` with fatal loglevel and
 * automatically determined function name, filename, and line number.
 */
#define dqcs_log_fatal(fmt, ...)          \
  dqcs_log_format(                        \
    DQCS_LOGLEVEL_PREFIX DQCS_LOG_FATAL,  \
    DQCS_LANGUAGE,                        \
    __FILE__,                             \
    __LINE__,                             \
    fmt,                                  \
    ##__VA_ARGS__                         \
  )

