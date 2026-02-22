import 'package:riverpod/riverpod.dart';
import '../models/house.dart';
import '../services/api_service.dart';

final apiServiceProvider = Provider((ref) => ApiService());

final recommendationsProvider = FutureProvider.family<List<House>, int>((ref, userId) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getRecommendations(userId);
});

final adHocRecommendationsProvider = FutureProvider.family<List<House>, Map<String, dynamic>>((ref, prefs) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getAdHocRecommendations(prefs);
});

final allHousesProvider = FutureProvider<List<House>>((ref) async {
  final apiService = ref.watch(apiServiceProvider);
  return apiService.getAllHouses();
});
