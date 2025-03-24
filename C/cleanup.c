#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

typedef void (*cleanup_callback_t)(); // Define a callback type for cleanup
cleanup_callback_t python_callback = NULL; // Pointer to Python's cleanup function

void handle_signal(int signum) {
    printf("Signal %d received, cleaning up...\n", signum);
    if (python_callback != NULL) {
        python_callback(); // Call the Python cleanup function if registered
    }
    exit(0); // Exit the program gracefully
}

void register_python_callback(cleanup_callback_t callback) {
    python_callback = callback; // Register Python's cleanup function
}

void setup_signal_handlers() {
    signal(SIGINT, handle_signal);    // Handle Ctrl+C
    signal(SIGTERM, handle_signal);  // Handle termination signal
}

void cleanup() {
    printf("C DLL cleanup called!\n");
    if (python_callback != NULL) {
        python_callback(); // Ensure Python's cleanup logic runs
    }
}
