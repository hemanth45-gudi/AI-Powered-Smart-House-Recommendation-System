import 'package:riverpod/riverpod.dart';
import '../models/house.dart';
import '../services/api_service.dart';
import '../services/websocket_service.dart';

final apiServiceProvider = Provider((ref) => ApiService());

// WebSocket Service - lifecycle is tied to the provider
final webSocketServiceProvider = Provider.family<WebSocketService, int>((ref, userId) {
  final service = WebSocketService();
  service.connect(userId);
  ref.onDispose(() => service.disconnect());
  return service;
});

// Real-Time Stream Provider (replaces FutureProvider for live data)
final realtimeRecommendationsProvider = StreamProvider.family<List<House>, int>((ref, userId) {
  final wsService = ref.watch(webSocketServiceProvider(userId));
  return wsService.recommendationsStream;
});

// Legacy REST-based providers (kept for compatibility/fallback)
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
