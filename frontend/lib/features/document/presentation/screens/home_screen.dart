import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'package:legaleasier/core/theme/app_theme.dart';
import 'package:legaleasier/features/auth/presentation/providers/auth_provider.dart';
import 'package:legaleasier/features/document/domain/document.dart';
import 'package:legaleasier/features/document/presentation/widgets/quick_action_card.dart';
import 'package:legaleasier/features/document/presentation/widgets/trial_banner.dart';
import 'package:legaleasier/features/document/presentation/widgets/recent_documents_section.dart';
import 'package:legaleasier/features/document/presentation/widgets/stat_box.dart';
import 'package:legaleasier/features/document/presentation/widgets/upload_scan_bottom_sheet.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  bool _isSigningOut = false;

  Future<void> _signOut() async {
    setState(() {
      _isSigningOut = true;
    });
    try {
      await ref.read(authNotifierProvider.notifier).logout();
      if (!mounted) return;
      context.go('/login');
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            error.toString(),
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: AppColors.danger,
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          _isSigningOut = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authUser = ref.watch(authNotifierProvider).value;
    final userEmail = authUser?.email ?? 'Pengguna';
    final userInitial = userEmail.isNotEmpty ? userEmail[0].toUpperCase() : 'U';

    return Scaffold(
      backgroundColor: AppColors.pageBackground,
      appBar: AppBar(
        backgroundColor: AppColors.brand,
        title: const Text(
          'Beranda',
          style: TextStyle(
            color: Colors.white,
            fontFamily: 'Fraunces',
            fontSize: 20,
            fontWeight: FontWeight.w700,
          ),
        ),
        elevation: 0,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Center(
              child: GestureDetector(
                onTap: _isSigningOut ? null : _signOut,
                child: Container(
                  width: 36,
                  height: 36,
                  decoration: const BoxDecoration(
                    color: AppColors.white,
                    shape: BoxShape.circle,
                  ),
                  child: _isSigningOut
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(
                              AppColors.brand,
                            ),
                          ),
                        )
                      : Center(
                          child: Text(
                            userInitial,
                            style: const TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 14,
                              color: AppColors.brand,
                            ),
                          ),
                        ),
                ),
              ),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              
              // Greeting section
              Text(
                'Halo!',
                style: AppTextStyles.screenTitle.copyWith(
                  fontFamily: 'Fraunces',
                  fontSize: 24,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                'Selamat datang, $userEmail',
                style: AppTextStyles.bodyMedium,
              ),
              const SizedBox(height: 16),

              // Trial banner
              const TrialBanner(),
              const SizedBox(height: 24),

              // Quick stats (3 stat boxes)
              const Row(
                children: [
                  Expanded(
                    child: StatBox(
                      number: '0',
                      label: 'Dokumen',
                    ),
                  ),
                  SizedBox(width: 8),
                  Expanded(
                    child: StatBox(
                      number: '0',
                      label: 'Berisiko',
                    ),
                  ),
                  SizedBox(width: 8),
                  Expanded(
                    child: StatBox(
                      number: '5',
                      label: 'Sisa Gratis',
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Quick actions grid
              Text(
                'Mulai dari sini',
                style: AppTextStyles.cardTitle.copyWith(
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 12),
              GridView.count(
                crossAxisCount: 2,
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                children: [
                  QuickActionCard(
                    icon: Icons.cloud_upload_outlined,
                    iconColor: AppColors.uploadIcon,
                    bgColor: AppColors.uploadBg,
                    title: 'Upload\nDokumen',
                    onTap: () async {
                      final messenger = ScaffoldMessenger.of(context);
                      final result = await showModalBottomSheet<Document>(
                        context: context,
                        isScrollControlled: true,
                        builder: (_) => const UploadScanBottomSheet(
                          initialMethod: UploadMethod.file,
                        ),
                      );

                      if (!mounted || result == null) {
                        return;
                      }

                      messenger.showSnackBar(
                        const SnackBar(
                          content: Text('Dokumen berhasil diupload.'),
                        ),
                      );
                    },
                  ),
                  QuickActionCard(
                    icon: Icons.camera_alt_outlined,
                    iconColor: AppColors.scanIcon,
                    bgColor: AppColors.scanBg,
                    title: 'Scan\nDokumen',
                    onTap: () async {
                      final messenger = ScaffoldMessenger.of(context);
                      final result = await showModalBottomSheet<Document>(
                        context: context,
                        isScrollControlled: true,
                        builder: (_) => const UploadScanBottomSheet(),
                      );

                      if (!mounted || result == null) {
                        return;
                      }

                      messenger.showSnackBar(
                        const SnackBar(
                          content: Text('Dokumen hasil scan berhasil diupload.'),
                        ),
                      );
                    },
                  ),
                  QuickActionCard(
                    icon: Icons.chat_bubble_outline,
                    iconColor: AppColors.chatIcon,
                    bgColor: AppColors.chatBg,
                    title: 'Tanya AI\nLegalEasy',
                    onTap: () {
                      // TODO: Navigate to chat
                    },
                  ),
                  QuickActionCard(
                    icon: Icons.history,
                    iconColor: AppColors.historyIcon,
                    bgColor: AppColors.historyBg,
                    title: 'Riwayat\nDokumen',
                    onTap: () {
                      // TODO: Navigate to history
                    },
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Recent documents
              const RecentDocumentsSection(),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }
}
