import 'dart:io';
import 'package:dio/dio.dart';
import 'package:legaleasier/features/document/domain/document.dart';

/// Service untuk HTTP calls ke backend document endpoints
class DocumentService {
  final Dio dio;

  DocumentService({required this.dio});

  /// GET /documents?limit=10
  /// Fetch recent documents
  Future<List<Document>> fetchRecentDocuments({int limit = 10}) async {
    try {
      final response = await dio.get(
        '/documents',
        queryParameters: {'limit': limit},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          final List<dynamic> documentsList = data['data'] as List<dynamic>;
          return documentsList
              .map((doc) => Document.fromJson(doc as Map<String, dynamic>))
              .toList();
        }
        return [];
      }
      throw Exception('Failed to fetch recent documents: ${response.statusCode}');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// GET /documents?page=1&limit=20
  /// Fetch documents dengan pagination
  Future<List<Document>> fetchDocuments({int page = 1, int limit = 20}) async {
    try {
      final response = await dio.get(
        '/documents',
        queryParameters: {'page': page, 'limit': limit},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          final List<dynamic> documentsList = data['data'] as List<dynamic>;
          return documentsList
              .map((doc) => Document.fromJson(doc as Map<String, dynamic>))
              .toList();
        }
        return [];
      }
      throw Exception('Failed to fetch documents: ${response.statusCode}');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// GET /documents/:id
  /// Fetch single document by ID
  Future<Document?> fetchDocumentById(String id) async {
    try {
      final response = await dio.get('/documents/$id');

      if (response.statusCode == 200) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          return Document.fromJson(data['data'] as Map<String, dynamic>);
        }
        return null;
      }
      throw Exception('Failed to fetch document: ${response.statusCode}');
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        return null;
      }
      throw _handleDioError(e);
    }
  }

  /// POST /documents/upload
  /// Upload document file (multipart)
  Future<Document> uploadDocument(File file) async {
    try {
      final fileName = file.path.split('/').last;
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          file.path,
          filename: fileName,
        ),
      });

      final response = await dio.post(
        '/documents/upload',
        data: formData,
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          return Document.fromJson(data['data'] as Map<String, dynamic>);
        }
      }
      throw Exception('Failed to upload document: ${response.statusCode}');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// DELETE /documents/:id
  /// Delete document
  Future<void> deleteDocument(String id) async {
    try {
      final response = await dio.delete('/documents/$id');

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to delete document: ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// GET /documents/count
  /// Get total document count
  Future<int> getDocumentCount() async {
    try {
      final response = await dio.get('/documents/count');

      if (response.statusCode == 200) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          return data['data']['count'] as int;
        }
        return 0;
      }
      throw Exception('Failed to get document count: ${response.statusCode}');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// GET /documents/search?q=query
  /// Search documents
  Future<List<Document>> searchDocuments(String query) async {
    try {
      final response = await dio.get(
        '/documents/search',
        queryParameters: {'q': query},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        if (data['success'] == true && data['data'] != null) {
          final List<dynamic> documentsList = data['data'] as List<dynamic>;
          return documentsList
              .map((doc) => Document.fromJson(doc as Map<String, dynamic>))
              .toList();
        }
        return [];
      }
      throw Exception('Failed to search documents: ${response.statusCode}');
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  /// Handle Dio errors dengan pesan yang user-friendly
  Exception _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
        return Exception('Timeout saat berkomunikasi dengan server');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final message = error.response?.data['message'] as String?;
        return Exception('Error: ${message ?? 'Request gagal (Code: $statusCode)'}');
      case DioExceptionType.cancel:
        return Exception('Request dibatalkan');
      case DioExceptionType.unknown:
        return Exception('Kesalahan jaringan. Periksa koneksi Anda.');
      default:
        return Exception('Terjadi kesalahan: ${error.message}');
    }
  }
}
