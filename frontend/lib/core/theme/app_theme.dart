import 'package:flutter/material.dart';

/// LegalEasy Design System Color Palette
class AppColors {
  // Brand
  static const Color brand = Color(0xFF1A3A4A);        // Navy gelap
  static const Color brand2 = Color(0xFF2E6B5E);       // Teal
  static const Color accent = Color(0xFFC8A96E);       // Gold
  static const Color accentLight = Color(0xFFE8D5B0);  // Gold muda

  // Neutral
  static const Color soft = Color(0xFFF4F0E8);         // Krem
  static const Color white = Color(0xFFFFFFFF);
  static const Color pageBackground = Color(0xFFE8E4DC);

  // Text
  static const Color text1 = Color(0xFF1A1A1A);        // Teks utama
  static const Color text2 = Color(0xFF5A5A5A);        // Teks sekunder
  static const Color text3 = Color(0xFF9A9A9A);        // Teks tersier

  // Risk levels
  static const Color danger = Color(0xFFC0392B);       // Tinggi
  static const Color warning = Color(0xFFD68910);      // Sedang
  static const Color success = Color(0xFF1E8449);      // Aman / Rendah

  // Quick action backgrounds
  static const Color uploadBg = Color(0xFFD5EDE8);
  static const Color scanBg = Color(0xFFD8E9F8);
  static const Color chatBg = Color(0xFFEDE8F8);
  static const Color historyBg = Color(0xFFF8EEE0);

  // Icon colors
  static const Color uploadIcon = Color(0xFF2E6B5E);
  static const Color scanIcon = Color(0xFF185FA5);
  static const Color chatIcon = Color(0xFF534AB7);
  static const Color historyIcon = Color(0xFFBA7517);

  // Trial gate
  static const Color gateBg = Color(0xFFFEF9E7);
  static const Color gateBorder = Color(0xFFF9CA5A);
  static const Color gateIcon = Color(0xFFBA7517);
}

/// LegalEasy Design System - Text Styles
class AppTextStyles {
  // Headings (Fraunces)
  static const splashHeadline = TextStyle(
    fontFamily: 'Fraunces',
    fontSize: 28,
    fontWeight: FontWeight.w700,
    color: AppColors.white,
    height: 1.2,
  );

  static const screenTitle = TextStyle(
    fontFamily: 'Fraunces',
    fontSize: 18,
    fontWeight: FontWeight.w700,
    color: AppColors.text1,
  );

  static const loginTitle = TextStyle(
    fontFamily: 'Fraunces',
    fontSize: 22,
    fontWeight: FontWeight.w700,
    color: AppColors.text1,
  );

  static const cardTitle = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 14,
    fontWeight: FontWeight.w500,
    color: AppColors.text1,
  );

  // Body text (DM Sans)
  static const bodyLarge = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 13,
    fontWeight: FontWeight.w400,
    color: AppColors.text1,
    height: 1.5,
  );

  static const bodyMedium = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 12,
    fontWeight: FontWeight.w400,
    color: AppColors.text2,
  );

  static const label = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 12,
    fontWeight: FontWeight.w500,
    color: AppColors.text2,
  );

  static const meta = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 11,
    fontWeight: FontWeight.w400,
    color: AppColors.text3,
  );

  static const buttonText = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 13,
    fontWeight: FontWeight.w500,
    color: AppColors.white,
  );

  static const badgeText = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 10,
    fontWeight: FontWeight.w500,
  );

  static const chipText = TextStyle(
    fontFamily: 'DM Sans',
    fontSize: 11,
    fontWeight: FontWeight.w500,
  );
}

class AppTheme {
  static ThemeData light() {
    return ThemeData(
      useMaterial3: true,
      fontFamily: 'DM Sans',
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.brand,
        primary: AppColors.brand,
        secondary: AppColors.brand2,
        surface: AppColors.pageBackground,
      ),
      scaffoldBackgroundColor: AppColors.pageBackground,
      
      // App Bar
      appBarTheme: const AppBarTheme(
        elevation: 0,
        backgroundColor: AppColors.white,
        surfaceTintColor: Colors.transparent,
        iconTheme: IconThemeData(color: AppColors.text1),
        titleTextStyle: AppTextStyles.screenTitle,
        centerTitle: false,
      ),

      // Input Fields
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: Color(0xFFE8E8E8),
            width: 1.5,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: Color(0xFFE8E8E8),
            width: 1.5,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(
            color: AppColors.brand2,
            width: 1.5,
          ),
        ),
        filled: true,
        fillColor: AppColors.white,
        contentPadding: const EdgeInsets.symmetric(
          vertical: 12,
          horizontal: 14,
        ),
        labelStyle: AppTextStyles.label,
        hintStyle: AppTextStyles.bodyMedium.copyWith(
          color: AppColors.text3,
        ),
      ),

      // Elevated Button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: AppColors.brand,
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
          minimumSize: const Size.fromHeight(50),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTextStyles.buttonText,
          elevation: 0,
        ),
      ),

      // Outlined Button
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: AppColors.white,
          side: const BorderSide(
            color: Color.fromRGBO(255, 255, 255, 0.4),
            width: 1.5,
          ),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          minimumSize: const Size.fromHeight(50),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: AppTextStyles.buttonText,
        ),
      ),

      // Text Button
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(
          foregroundColor: AppColors.brand2,
          textStyle: AppTextStyles.label,
        ),
      ),

      // Card
      cardTheme: CardThemeData(
        color: AppColors.white,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
          side: const BorderSide(
            color: Color.fromRGBO(0, 0, 0, 0.07),
            width: 0.5,
          ),
        ),
      ),

      // Dialog
      dialogTheme: DialogThemeData(
        backgroundColor: AppColors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(14),
        ),
      ),

      // Bottom Sheet
      bottomSheetTheme: const BottomSheetThemeData(
        backgroundColor: AppColors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(20),
            topRight: Radius.circular(20),
          ),
        ),
        elevation: 10,
      ),
    );
  }
}
