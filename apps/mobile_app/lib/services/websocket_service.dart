import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../models/house.dart';

class WebSocketService {
  static const String _mlEngineWsUrl = 'ws://10.0.2.2:8001';

  WebSocketChannel? _channel;
  final _recommendationsController = StreamController<List<House>>.broadcast();

  Stream<List<House>> get recommendationsStream => _recommendationsController.stream;

  void connect(int userId) {
    final uri = Uri.parse('$_mlEngineWsUrl/ws/recommend/$userId');
    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
      (data) {
        final json = jsonDecode(data as String);
        if (json['event'] == 'recommendations_updated') {
          final recs = (json['recommendations'] as List)
              .map((h) => House.fromJson(h as Map<String, dynamic>))
              .toList();
          _recommendationsController.add(recs);
        }
      },
      onError: (error) {
        print('WebSocket error: $error');
        _recommendationsController.addError(error);
      },
      onDone: () {
        print('WebSocket connection closed.');
      },
    );
  }

  void sendRefresh(Map<String, dynamic> prefs) {
    _channel?.sink.add(jsonEncode(prefs));
  }

  void disconnect() {
    _channel?.sink.close();
    _recommendationsController.close();
  }
}
