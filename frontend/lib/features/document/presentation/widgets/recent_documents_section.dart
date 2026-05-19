import 'package:flutter/material.dart';
import 'package:legaleasier/core/theme/app_theme.dart';

/// Recent documents section di home screen
/// TODO: Connect dengan DocumentProvider untuk real data
class RecentDocumentsSection extends StatelessWidget {
  const RecentDocumentsSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Dokumen Terbaru',
          style: AppTextStyles.cardTitle.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        
        // Empty state untuk sekarang
        Container(
          decoration: BoxDecoration(
            color: AppColors.white,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: Colors.black.withValues(alpha: 0.08),
              width: 0.5,
            ),
          ),
          padding: const EdgeInsets.symmetric(vertical: 32, horizontal: 16),
          child: Center(
            child: Column(
              children: [
                const Icon(
                  Icons.file_copy_outlined,
                  size: 48,
                  color: AppColors.text3,
                ),
                const SizedBox(height: 12),
                Text(
                  'Belum ada dokumen',
                  style: AppTextStyles.label.copyWith(
                    color: AppColors.text2,
                  ),
                ),
                const SizedBox(height: 4),
                const Text(
                  'Upload dokumen pertama Anda sekarang',
                  style: AppTextStyles.meta,
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
