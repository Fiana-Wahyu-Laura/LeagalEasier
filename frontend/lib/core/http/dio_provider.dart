import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Global Dio provider untuk HTTP requests
final dioProvider = Provider<Dio>((ref) {
  const baseUrl = 'http://10.0.2.2:8000';  // Android emulator localhost
  
  final dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ),
  );

  // TODO: Add interceptor untuk JWT token
  // dio.interceptors.add(
  //   InterceptorsWrapper(
  //     onRequest: (options, handler) async {
  //       // Add JWT token dari SharedPreferences
  //       return handler.next(options);
  //     },
  //     onError: (error, handler) {
  //       // Handle 401 - refresh token atau logout
  //       return handler.next(error);
  //     },
  //   ),
  // );

  return dio;
});
