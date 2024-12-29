import { logger } from './logger';

export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export const ErrorCodes = {
  AUDIO_PERMISSION_DENIED: 'AUDIO_PERMISSION_DENIED',
  AUDIO_DEVICE_ERROR: 'AUDIO_DEVICE_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
  LIVEKIT_ERROR: 'LIVEKIT_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR',
} as const;

export function handleError(error: unknown, context?: string): AppError {
  let appError: AppError;

  if (error instanceof AppError) {
    appError = error;
  } else if (error instanceof Error) {
    // Convert standard errors to AppError
    appError = new AppError(
      error.message,
      ErrorCodes.UNKNOWN_ERROR,
      { originalError: error }
    );
  } else {
    // Handle non-Error objects
    appError = new AppError(
      'An unknown error occurred',
      ErrorCodes.UNKNOWN_ERROR,
      { originalError: error }
    );
  }

  // Log the error with context
  logger.error(
    `Error in ${context || 'unknown context'}: ${appError.message}`,
    {
      error: appError,
      context,
    }
  );

  return appError;
}

export function isPermissionDeniedError(error: unknown): boolean {
  return error instanceof Error &&
    (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError');
}

export function handleAudioError(error: unknown): AppError {
  if (isPermissionDeniedError(error)) {
    return new AppError(
      'Microphone access was denied. Please allow microphone access to use voice features.',
      ErrorCodes.AUDIO_PERMISSION_DENIED,
      { originalError: error }
    );
  }

  return new AppError(
    'An error occurred while accessing the microphone',
    ErrorCodes.AUDIO_DEVICE_ERROR,
    { originalError: error }
  );
}
