import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/recommendation_provider.dart';
import '../widgets/house_card.dart';

import '../widgets/preference_filter.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final int userId = 1; // Mock user ID
  Map<String, dynamic>? _customPrefs;

  @override
  Widget build(BuildContext context) {
    // Determine which provider to use
    final recProvider = _customPrefs == null 
        ? recommendationsProvider(userId)
        : adHocRecommendationsProvider(_customPrefs!);
        
    final recommendations = ref.watch(recProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart House Picks'),
        backgroundColor: Colors.blue.shade900,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(_customPrefs == null ? Icons.filter_alt : Icons.filter_alt_off),
            tooltip: _customPrefs == null ? 'Personalize' : 'Clear Filters',
            onPressed: () {
              if (_customPrefs != null) {
                setState(() {
                  _customPrefs = null;
                });
              } else {
                _showPreferenceFilter(context);
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.refresh(recProvider),
          ),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              _customPrefs == null 
                  ? 'Recommended for You' 
                  : 'Based on Search Filters',
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(
            child: recommendations.when(
              data: (houses) => houses.isEmpty
                  ? const Center(child: Text('No recommendations yet.'))
                  : ListView.builder(
                      itemCount: houses.length,
                      itemBuilder: (context, index) {
                        return HouseCard(house: houses[index]);
                      },
                    ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, stack) => Center(
                child: Text('Error connecting to ML Engine: $err'),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showPreferenceFilter(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => PreferenceFilter(
        onApply: (prefs) {
          setState(() {
            _customPrefs = prefs;
          });
        },
      ),
    );
  }
}
