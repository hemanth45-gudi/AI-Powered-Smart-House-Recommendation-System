import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/recommendation_provider.dart';
import '../widgets/house_card.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // For demo purposes, we're using userId: 1
    final recommendations = ref.watch(recommendationsProvider(1));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart House Picks'),
        backgroundColor: Colors.blue.shade900,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.refresh(recommendationsProvider(1)),
          ),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.all(16.0),
            child: Text(
              'Recommended for You',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
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
}
