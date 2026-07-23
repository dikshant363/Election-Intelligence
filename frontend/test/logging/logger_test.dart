import 'package:election_intelligence_frontend/core/logging/logger.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Logger Tests', () {
    test('Logger methods execute without errors', () {
      expect(() => Logger.debug('Debug test message'), returnsNormally);
      expect(() => Logger.info('Info test message'), returnsNormally);
      expect(() => Logger.error('Error test message'), returnsNormally);
      expect(
        () => Logger.logError(
          'LogError test message',
          details: 'Sample details',
          error: Exception('Test exception'),
          stackTrace: StackTrace.current,
        ),
        returnsNormally,
      );
      expect(() => Logger.logInfo('LogInfo test message'), returnsNormally);
      expect(() => Logger.logDebug('LogDebug test message'), returnsNormally);
    });
  });
}
