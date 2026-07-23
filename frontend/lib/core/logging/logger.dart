import 'dart:developer' as dev;

class Logger {
  static void debug(String message) {
    dev.log(message, name: 'DEBUG');
  }

  static void info(String message) {
    dev.log(message, name: 'INFO');
  }

  static void error(
    String message, {
    Object? error,
    StackTrace? stackTrace,
  }) {
    dev.log(
      message,
      name: 'ERROR',
      error: error,
      stackTrace: stackTrace,
    );
  }

  static void logError(
    String message, {
    Object? details,
    Object? error,
    StackTrace? stackTrace,
  }) {
    dev.log(
      details != null ? '$message: $details' : message,
      name: 'ERROR',
      error: error,
      stackTrace: stackTrace,
    );
  }

  static void logInfo(String message) => info(message);
  static void logDebug(String message) => debug(message);
}
