import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';
import 'firebase_options.dart'; // ← tambahkan ini

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform, // ← tambahkan ini
  );
  runApp(const ProviderScope(child: LegalEasierApp()));
}

class LegalEasierApp extends StatelessWidget {
  const LegalEasierApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      debugShowCheckedModeBanner: false,
      title: 'LegalEasier',
      theme: AppTheme.light(),
      routerConfig: AppRouter.router,
    );
  }
}